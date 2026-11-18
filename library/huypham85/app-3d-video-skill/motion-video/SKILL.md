---
name: motion-video
description: Produce a finished, professional motion-graphics video (MP4 with an original synthesized music track, motion cut to the beat) entirely on this Mac — no ffmpeg, no stock footage, no downloads. Use this whenever the user wants a promo, launch, "what's new", release-notes, feature, App Store preview-style, social (Reels/TikTok/Shorts), showreel or explainer video for an app, product or update — including phrasings like "làm video", "make a video", "motion graphics", "animated promo", "video giới thiệu tính năng", "clip cho bản cập nhật", or "turn these release notes into a video". Also use it to revise a video made with this skill earlier (slower pacing, different music mood, new aspect ratio, another language).
---

# Motion video

Makes a 10–30 s motion-graphics spot as real code: a Swift synth writes the score, a Swift
CoreGraphics/CoreImage renderer draws every frame on the same beat grid (with sub-frame motion
blur, real gaussian blur, frosted glass, film grain) and AVFoundation encodes H.264 + AAC.
Everything needed is in this skill folder; macOS + Xcode command-line tools are the only deps.

The bar is "a motion designer's showreel", not a demo: every cue lands on the music, nothing
on screen is decorative noise, and every claim is true.

## Folder map

- `engine/` — `audio_core.swift` + `audio_main.swift` (score engine), `video_core.swift` + `video_main.swift` (render engine). Don't edit per project; project code goes in the project folder.
- `scripts/mv.sh` — build + run: `audio`, `stills <beats>`, `video [out]`. `levels.py`, `sheet.py`, `probe.swift` are used by it.
- The complete worked project lives in the companion skill `app-3d-video` (`template/`: `score.swift`, `scenes.swift`, `project.env`, plus the SceneKit layer `s3d.swift`). For a 2D-only video, copy its `project.env` and `score.swift` and write a fresh `scenes.swift` against `references/engine-api.md`.
- `examples/scores/energetic-128bpm.swift` — high-energy launch score (drops, fills, drop-out).
- `references/motion-direction.md` — pacing by tone, easing, transitions, layout, storytelling patterns, review checklist. **Read before planning scenes.**
- `references/score-guide.md` — tempo/key/arrangement recipes, matching a brand sound's key, loudness targets. **Read before writing the score.**
- `references/engine-api.md` — every drawing/audio function with its signature. Read when writing code.

## Workflow

### 1. Brief (keep questions to what changes the result)
Settle: purpose and audience, duration, aspect (default 1080×1920 vertical; 1920×1080 or
1080×1350 via `W`/`H`), tone, language of on-screen copy. Defaults if the user doesn't care:
15 s, vertical, English copy, tone matched to the product's domain. If the requested content won't
fit the duration at a pace that suits the tone, say so and ask which to give up — duration or
content — rather than cramming. (A health app wanted calm pacing *and* 15 s; the answer was to
drop scenes, not speed up.)

### 2. Research what's true
Everything on screen must be defensible:
- What shipped: `git log` since the last few version bumps, CHANGELOG, release notes.
- Exact product copy: read the code for notification titles/bodies, button labels, Siri/intent
  dialog strings, snippet headings, onboarding text. Quote it; don't paraphrase it into a promise.
- Mark anything illustrative (sample names, counts, times) and tell the user at delivery.
- Keep the story internally consistent: if scene 1 logs Metformin at 9:41, scene 2 can't ask
  when Metformin was last taken and hear "13 hours ago" — use another medication.

### 3. Assets
Collect real brand assets: app icon (largest PNG), logo, brand colours (design tokens/asset
catalog), official badges the product already uses (e.g. "Works with Apple Health"), and the
product's own sounds (notification/sonic-logo WAVs). Convert one-shots for the synth:
`afconvert -f WAVE -d LEF32@48000 -c 1 in.wav assets/name.wav`; SVG → PNG with `sharp`/`resvg`
if the repo has them, or `qlmanage -t -s 1024`.

Prefer **recreated vector UI with one data set** (one wallpaper, one clock time, one set of
names) over raw screenshots. Screenshots from different sources (different times, devices, data,
frames) side by side look wrong; viewers notice at once. If you
do use screenshots, capture them in one session with `xcrun simctl status_bar booted override
--time 9:41 …`, clear it afterwards, and never capture another app that happens to be open.

### 4. Plan on the beat grid
Duration = bars × 4 × 60 / BPM, so pick BPM and bar count together (15 s = 6 bars @ 96, 8 bars @ 128).
Write `plan.md` in the project: a table of bars → scene → the cue on each beat (word reveals,
card lands, check pops, transition). One idea per bar; the big moments (logo, key feature, end
card) sit on downbeats. See `references/motion-direction.md` for tone presets and patterns.

### 5. Project folder
Work in `~/Movies/MotionVideo/<slug>/` (persists for later revisions):
```
mkdir -p ~/Movies/MotionVideo/<slug> && cp ~/.claude/skills/app-3d-video/template/{project.env,score.swift} ~/Movies/MotionVideo/<slug>/
```
Edit `project.env` (BPM, DURATION, W, H, FPS), put brand assets in `assets/`, then rewrite `score.swift` and
write `scenes.swift`. Reassign the palette vars (`INK`, `TEAL`, `MINT`, `GREEN`, `GLOW`, `PAPER`,
`DARKTEXT`, `ORANGE`, `DARK_MID`, `LIGHT_GLOW_A/B`) at the top of `scenes.swift` for the brand.

### 6. Score first
Write `score.swift` (recipes in `references/score-guide.md`), then run `mv.sh <dir> audio`. You
can't hear it — read the levels printout: RMS in the target range for the tone, no clipping,
section contrast where you intended (quiet intro, lift at the drop, a dip for any drop-out).
The video reads `music.wav` for audio-reactive elements, so render audio before stills.

### 7. Scenes, then stills review — at least two rounds
Write `scenes.swift` defining `func render(_ t: Double, frame: Int)`, then:
```
~/.claude/skills/motion-video/scripts/mv.sh <dir> stills 0.5,2,4.25,6,8.5,10,13,16,20,22.5
```
Open `<dir>/sheet.png` with Read and go through the checklist in `references/motion-direction.md`
(overlaps at spring overshoot, clipped descenders, text too small, muddy crossfades,
inconsistent UI, dead space). Also pick mid-transition beats, not only resting states. Fix and
re-shoot until a round comes back clean. Stills render at ~0.1 s/frame, so iterate freely.

### 8. Final render and verify
`mv.sh <dir> video <dir>/out.mp4` — about 0.3–0.5 s/frame with `SUB=5` motion blur (15 s @ 60 fps
≈ 5–8 min), so run it in the background. The probe prints duration and tracks; also extract a
few frames (`.build/probe out.mp4 <dir> 2,5,9,12`) and look at them.

### 9. Deliver
Copy to `~/Downloads/<Product>_<Topic>_<duration>s[_vN].mp4`, send it with SendUserFile, and
report: the story beat by beat (seconds), which assets and strings are real, what's illustrative,
that you judged the audio by measurement only, and a short checklist for the user (listen at
volume, legibility on a phone, brand/badge usage). Keep previous versions (`v1/`) when revising.

## Revising
Most feedback maps to one knob: *slower/calmer* → lower BPM + fewer scenes + damped springs
(`k≈5, w≈6`) + longer reveals (0.9–1 beat) + rack-focus/iris transitions instead of whips;
*more energy* → the energetic score, springs with overshoot, whips, flashes on drops;
*"I don't get feature X"* → show the full cause-and-effect on one device (request → response →
result) with the product's real response copy, and title it with the value, not the feature name.
