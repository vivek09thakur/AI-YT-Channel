#!/usr/bin/env python3
"""sheet.py <dir of jpgs> <out.jpg> [cols=6] : contact sheet with frame numbers"""
import sys, glob, os
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
fs = sorted(p for p in glob.glob(os.path.join(d, "*.jpg")) if not os.path.basename(p).startswith("sheet") and not os.path.basename(p).startswith("qa_"))
w0, h0 = Image.open(fs[0]).size if fs else (1080, 1920); tw = 270 if h0 > w0 else 480; th = int(tw * h0 / w0)
rows = (len(fs) + cols - 1) // cols; im = Image.new("RGB", (cols * tw, rows * th), (20, 16, 30))
for i, p in enumerate(fs):
    t = Image.open(p).convert("RGB").resize((tw, th)); dr = ImageDraw.Draw(t); dr.rectangle([0, 0, 92, 24], fill=(0, 0, 0)); dr.text((6, 5), os.path.basename(p)[:-4], fill=(255, 255, 255))
    im.paste(t, ((i % cols) * tw, (i // cols) * th))
im.save(out, quality=88); print(out, im.size)
