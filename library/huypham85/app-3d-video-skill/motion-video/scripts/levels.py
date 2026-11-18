#!/usr/bin/env python3
"""levels.py <music.wav> — overall RMS, clipping, and per-beat loudness (reads BPM env). You can't listen: read this."""
import sys, os, numpy as np
d = open(sys.argv[1], 'rb').read(); i = d.find(b'data')
x = np.frombuffer(d[i + 8:], dtype='<i2').reshape(-1, 2) / 32768
m = x.mean(1); sr = 48000; B = 60 / float(os.environ.get('BPM', 96))
db = lambda s: 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9)
print(f'duration {len(m) / sr:.2f}s  rms {db(m):.1f} dBFS  peak {np.abs(x).max():.2f}  samples>0.98: {(np.abs(x) > 0.98).mean() * 100:.3f}%')
n = int(len(m) / sr / B)
row = []
for b in range(n):
    s = m[int(b * B * sr):int((b + 1) * B * sr)]
    row.append(f'{b}:{db(s):.0f}')
for k in range(0, n, 8): print('  '.join(row[k:k + 8]))
