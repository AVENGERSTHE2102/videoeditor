#!/usr/bin/env python3
"""check_glitch.py <video.mp4> [--list]: find glitch frames, single frames that were captured wrong.

A glitch frame differs clearly from BOTH its neighbours while the two neighbours agree with each other (A-B-A). Real
animation does not do that; a half-painted screenshot does. Viewers see it as flicker (on YouTube more than locally).
Cause found 2026-11-14: the browser renderer took the screenshot before the new frame was fully painted (1440p,
full-screen mix-blend-mode layer). The renderers now wait two animation frames before each screenshot.

Decodes the whole video at 320x180 grey. A pixel "changes" when it moves by more than 14 levels; a frame is a glitch
when over 3 % of the picture changes against each neighbour and the neighbours differ by less than 30 % of that.
Prints the count and where they are (10 s bins). Exit 1 if any glitch frame is found. Run it on every final render
(it takes about a minute per 10 minutes of video)."""
import sys, argparse, subprocess, collections
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--list", action="store_true", help="print every glitch frame")
a = ap.parse_args()
W, H = 320, 180
fps_s = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", a.video],
                       capture_output=True, text=True).stdout.strip() or "30/1"
n_, d_ = fps_s.split("/"); FPS = float(n_) / float(d_)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
fs = W * H; prev2 = prev1 = None; i = 0; hits = []
while True:
    b = p.stdout.read(fs)
    if len(b) < fs: break
    cur = np.frombuffer(b, np.uint8).astype(np.int16)
    if prev2 is not None:
        x = (np.abs(prev1 - prev2) > 14).mean(); y = (np.abs(cur - prev1) > 14).mean(); z = (np.abs(cur - prev2) > 14).mean()
        if x > 0.03 and y > 0.03 and z < 0.3 * min(x, y): hits.append((i - 1, x, y, z))
    prev2, prev1 = prev1, cur; i += 1
fmt = lambda s: f"{int(s // 60)}:{s % 60:05.2f}"
print(f"{i} frames, {len(hits)} glitch frames" + (" -> OK" if not hits else " -> re-render with the paint wait (render_seg.mjs)"))
by = collections.Counter(int(h[0] / FPS // 10 * 10) for h in hits)
for k in sorted(by): print(f"  {k // 60}:{k % 60:02d}-{(k + 10) // 60}:{(k + 10) % 60:02d}  {by[k]}")
if a.list:
    for h in hits: print(f"  frame {h[0]} ({fmt(h[0] / FPS)}): {h[1]*100:.1f} % / {h[2]*100:.1f} % changed vs neighbours, neighbours {h[3]*100:.1f} %")
sys.exit(1 if hits else 0)
