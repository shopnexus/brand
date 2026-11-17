"""Cut a generated image off its flat magenta background and frame it.

    python3 tools/key.py <in.png> <out.png> [--pad 0.06]

The image model draws transparency badly (noisy halos), so drawings are
generated on #FF00FF and keyed here. Pixels near magenta become transparent,
edge pixels get partial alpha and lose their magenta tint, and the result is
cropped to the drawing and centred on a 1024 px square with `pad` margin.
"""
import sys

import numpy as np
from PIL import Image


def key(path, out, pad=0.06, size=1024):
    rgb = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    # How magenta a pixel is: red and blue high, green low.
    m = np.clip((np.minimum(r, b) - g) / 255.0, 0, 1)
    alpha = np.clip(1 - (m - 0.25) / 0.45, 0, 1)
    # Remove the magenta cast left on edge pixels.
    spill = np.minimum(r, b) - g
    fix = np.clip(spill, 0, None) * (1 - alpha)
    rgb[..., 0] -= fix * 0.9
    rgb[..., 2] -= fix * 0.9
    rgba = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
    im = Image.fromarray(rgba, "RGBA")
    bbox = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
    im = im.crop(bbox)
    inner = int(size * (1 - 2 * pad))
    im.thumbnail((inner, inner), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(im, ((size - im.width) // 2, (size - im.height) // 2), im)
    canvas.save(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    pad = 0.06
    if "--pad" in args:
        i = args.index("--pad"); pad = float(args[i + 1]); del args[i:i + 2]
    key(args[0], args[1], pad)
