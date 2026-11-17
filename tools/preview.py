"""Draw preview.png: every exported asset on one sheet, for review.

    python3 tools/preview.py         (run after tools/export.py)
"""
import glob
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = [("android/app/res/drawable-xxxhdpi/ic_launcher_foreground.png", (185, 231, 225)),
         ("android/app/res/drawable-xxxhdpi/ic_launcher_monochrome.png", (185, 231, 225)),
         ("android/app-live/res/drawable-xxxhdpi/ic_notification.png", (6, 106, 97)),
         ("web/icon-192.png", None)]


def main(cell=200, cols=8):
    items = [(f, None) for f in sorted(glob.glob(os.path.join(ROOT, "web", "*.webp")))]
    items += [(os.path.join(ROOT, f), bg) for f, bg in ICONS]
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cell * cols, (cell + 16) * rows), (236, 240, 238))
    draw = ImageDraw.Draw(sheet)
    for i, (f, bg) in enumerate(items):
        x, y = (i % cols) * cell, (i // cols) * (cell + 16)
        if bg:
            sheet.paste(bg, (x, y, x + cell, y + cell))
        im = Image.open(f).convert("RGBA").resize((cell, cell), Image.LANCZOS)
        sheet.paste(im, (x, y), im)
        draw.text((x + 4, y + cell + 1), os.path.basename(f).rsplit(".", 1)[0], fill=(30, 30, 30))
    sheet.save(os.path.join(ROOT, "preview.png"))


if __name__ == "__main__":
    main()
