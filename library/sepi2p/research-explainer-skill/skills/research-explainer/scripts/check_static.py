#!/usr/bin/env python3
"""check_static.py <video.mp4> (--timeline timeline.json | --srt subs.srt) [--max 2.5] [--share 8]: find stretches where
the picture stays still while the narrator talks (viewers call it boring).

Decodes the video at 4 frames/s, small and blurred, so line boil and grain don't count as motion. A moment counts as
moving when more than 0.6 % of the picture changes clearly within 0.5 s. Speech comes from the timeline's beats
(start/end) or the subtitles. It reports every still stretch of at least 2 s under speech, the longest ones, the
share of spoken time that is still, and a per-scene breakdown when the timeline has scenes.

Exit 1 when a still stretch under speech is longer than --max seconds (default 2.5) or the still share exceeds --share
percent (default 8). The fix is in the picture, not here: give every clause a visual change cued to its words
(E.cue), move the camera at least every 5-6 s, and break mechanisms into steps that build on screen (motion.md).
Needs ffmpeg and numpy."""
import argparse, json, re, subprocess, sys
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--timeline"); ap.add_argument("--srt")
ap.add_argument("--max", type=float, default=2.5); ap.add_argument("--share", type=float, default=8.0)
ap.add_argument("--min", type=float, default=2.0, help="shortest still stretch to list (s)")
ap.add_argument("--json", help="write the stretches here")
ap.add_argument("--offset", type=float, default=0.0, help="the video starts at this time of the timeline (a clip of one scene)")
a = ap.parse_args()
FPS, W, H = 4, 214, 120
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"fps={FPS},scale={W}:{H},gblur=sigma=1.5,format=gray",
                      "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)
d = np.array([(np.abs(x[i + 2] - x[i]) > 18).mean() * 100 for i in range(len(x) - 2)])
t = np.arange(len(d)) / FPS + a.offset; moving = d > 0.6
spans, scenes = [], {}
if a.timeline:
    TL = json.load(open(a.timeline)); spans = [(b["start"], b["end"]) for b in TL["beats"]]
    scenes = {k: v["start"] for k, v in TL.get("scenes", {}).items()}
elif a.srt:
    ts = lambda s: sum(float(p) * m for p, m in zip(s.replace(",", ".").split(":"), (3600, 60, 1)))
    for m in re.finditer(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", open(a.srt).read()): spans.append((ts(m.group(1)), ts(m.group(2))))
else: sys.exit("give --timeline or --srt (when the narrator speaks)")
speak = np.zeros(len(d), bool)
for s0, s1 in spans: speak[(t >= s0) & (t < s1)] = True
runs, i = [], 0
while i < len(d):
    if speak[i] and not moving[i]:
        j = i
        while j < len(d) and speak[j] and not moving[j]: j += 1
        if (j - i) / FPS >= a.min: runs.append((float(t[i]), (j - i) / FPS))
        i = j
    else: i += 1
spoken = speak.sum() / FPS; still = sum(r[1] for r in runs if r[1] >= 3) ; share = 100 * still / max(spoken, 1)
def scene_of(tt):
    s = None
    for k, v in sorted(scenes.items(), key=lambda kv: kv[1]):
        if tt >= v - 1: s = k
    return s
print(f"spoken {spoken:.0f} s; still >= 3 s under speech: {still:.0f} s ({share:.1f} %); stretches >= {a.min:g} s: {len(runs)}")
if scenes:
    per = {}
    for s0, l in runs: k = scene_of(s0); per.setdefault(k, [0, 0.0]); per[k][0] += 1; per[k][1] += l
    for k in sorted(per, key=lambda k: scenes[k]): print(f"  {k:14s} {per[k][0]:3d} stretches {per[k][1]:6.1f} s")
for s0, l in sorted(runs, key=lambda r: -r[1])[:15]:
    print(f"  {int(s0 // 60)}:{s0 % 60:04.1f}  still {l:.1f} s" + (f"  ({scene_of(s0)})" if scenes else ""))
if a.json: json.dump([{"t": s0, "dur": l, "scene": scene_of(s0) if scenes else None} for s0, l in runs], open(a.json, "w"), indent=0)
bad = [r for r in runs if r[1] > a.max]
print("PASS" if not bad and share <= a.share else f"FAIL: {len(bad)} still stretches over {a.max:g} s under speech, still share {share:.1f} % (max {a.share:g} %)")
sys.exit(1 if bad or share > a.share else 0)
