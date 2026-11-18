#!/usr/bin/env python3
"""check_cadence.py <video.mp4> [--start S] [--dur D] [--fps F]: find stepped animation that does not divide the frame
rate (it flickers on YouTube).

Stylised animation steps some things on a clock: line boil, characters on twos, sparkles. If a step rate does not
divide the frame rate (8/s or 12/s at 30 fps), the frames with a big change land at uneven gaps (4,4,4,3 and 3,2,3,2).
The eye reads that irregular 6-12 Hz pulse as flicker, and YouTube's low-bitrate encodes make it worse.

The check decodes a few seconds at 480p and marks every frame where more than 2 % of the pixels change. It reports the gaps between those frames
in three stretches. On a steady grid the gaps repeat, or are multiples of each other (2 and 4). An uneven step
alternates between neighbouring gaps (3 and 4). Exit 1 when that happens.

Fix: pick step rates that divide the fps. At 30 fps: boil 7.5/s (every 4 frames), characters 15/s (every 2), 10/s or
6/s. Add 1e-6 before Math.floor so t = i/fps does not land a hair below a step. Needs ffmpeg and numpy."""
import argparse, subprocess, sys
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--start", type=float, default=None)
ap.add_argument("--dur", type=float, default=8.0); ap.add_argument("--fps", type=float, default=None)
a = ap.parse_args()
probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate:format=duration",
                        "-of", "default=nw=1", a.video], capture_output=True, text=True).stdout
info = dict(l.split("=", 1) for l in probe.split() if "=" in l)
num, den = info["r_frame_rate"].split("/"); fps = a.fps or float(num) / float(den); total = float(info["duration"])
starts = [a.start] if a.start is not None else [total * f for f in (0.2, 0.45, 0.7)]
bad = 0
for s0 in starts:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{s0:.2f}", "-t", f"{a.dur:.2f}", "-i", a.video, "-vf", "scale=854:480,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.uint8).reshape(-1, 480, 854).astype(np.int16)
    ch = (np.abs(np.diff(x, axis=0)) > 12).mean((1, 2)) * 100
    big = np.where(ch > 2.0)[0] + 1
    if len(big) < 6: print(f"{s0:8.1f} s: too few stepped changes to judge"); continue
    gaps = np.diff(big); g = gaps[gaps > 1]                       # runs of 1 = smooth motion, not a step clock
    if len(g) < 10: print(f"{s0:8.1f} s: not enough stepped changes to judge (busy or very still shot); try another --start"); continue
    vals, cnt = np.unique(g, return_counts=True)
    # a steady clock gives gaps of one length, or multiples of it (2 and 4 = characters on twos + boil every 4 frames);
    # a rate that does not divide the fps alternates between two NEIGHBOURING lengths (3 and 4, or 2 and 3)
    sh = {int(v): c / cnt.sum() for v, c in zip(vals, cnt) if v <= 8}
    ok = not any(sh.get(k, 0) >= 0.1 and sh.get(k + 1, 0) >= 0.1 for k in range(2, 8))
    bad += not ok
    print(f"{s0:8.1f} s: step gaps {dict(zip(vals.tolist(), cnt.tolist()))} -> {'steady' if ok else 'UNEVEN: a step rate does not divide %g fps' % fps}")
sys.exit(1 if bad else 0)
