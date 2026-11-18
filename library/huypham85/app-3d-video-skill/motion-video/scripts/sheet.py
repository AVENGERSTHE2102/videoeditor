#!/usr/bin/env python3
"""sheet.py <out.png> <pngs...> [--cols N] — contact sheet with frame/beat labels (reads BPM, FPS env)."""
import sys, os, re
from PIL import Image, ImageDraw
args = sys.argv[1:]; cols = 4
if '--cols' in args:
    i = args.index('--cols'); cols = int(args[i + 1]); del args[i:i + 2]
out, files = args[0], sorted(args[1:])
bpm = float(os.environ.get('BPM', 96)); fps = float(os.environ.get('FPS', 60))
w = 360
first = Image.open(files[0]); h = int(w * first.height / first.width)
rows = (len(files) + cols - 1) // cols
S = Image.new('RGB', (cols * (w + 8), rows * (h + 30)), 'white'); d = ImageDraw.Draw(S)
for k, f in enumerate(files):
    im = Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS)
    x, y = (k % cols) * (w + 8), (k // cols) * (h + 30)
    S.paste(im, (x, y + 26))
    m = re.search(r'f(\d+)\.png$', f)
    label = os.path.basename(f)
    if m:
        fr = int(m.group(1)); label = f'f{fr}  t{fr / fps:.2f}s  beat {fr / fps / (60 / bpm):.2f}'
    d.text((x + 4, y + 6), label, fill='black')
S.save(out); print(out)
