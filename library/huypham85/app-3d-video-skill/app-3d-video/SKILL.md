---
name: app-3d-video
description: Use when the user asks for a 3D promo, teaser, launch, "coming soon", "what's new" or feature video for their iOS app, with a real 3D iPhone and a mascot character that hops around and presses the app's UI, or a revision or localized cut of such a video.
---

# App 3D video

## Overview

A 20 s vertical video rendered entirely on this Mac: a real SceneKit iPhone in a bright ivory world, the app's
mascot as a character that hops on and presses the real UI, value-first headlines, and an original swing score that
lands every hop on a marimba note. `template/` is a complete example project (a medication-reminder app called
"MyApp") and runs as is. Change the story, UI, data, brand and music; keep the look unless the user asks otherwise.

**REQUIRED SUB-SKILL:** motion-video (engine, beat-grid planning, stills review). Every value (palette, sizes, light,
music, pitfalls, second devices, real vs illustrative) is in `reference.md` next to this file.

Where the two skills differ, this one wins: copy `template/`, run `bash mv3d.sh` (not `mv.sh`), and the mascot's
bounces, sparkles and confetti are part of the look even though motion-video's health preset avoids them. UI that
carries data still only dips and pops; the mascot does the bouncing.

## Start from the template

```bash
cp -R ~/.claude/skills/app-3d-video/template ~/Movies/MotionVideo/<slug>
cd ~/Movies/MotionVideo/<slug>
bash mv3d.sh audio                   # score.swift -> music.wav, prints levels; run before stills
bash mv3d.sh stills 0.5,4.6,10.1     # BEATS -> stills/ + sheet.png
bash mv3d.sh video                   # out.mp4, about 5 min for 20 s with one phone: run in the background
bash mv3d.sh frames out.mp4 2.5,6.3  # SECONDS -> check/ + check_sheet.png
```

Branding lives in the `BRAND` block at the top of `scenes.swift`: `APP_NAME` (end-card wordmark), `APP_VERSION`
(the 3D number; re-check its size and position on stills when the length changes), `LABEL` (small label over the
first headline), `END_PILL` (gradient pill on the end card), and the mascot colours. Then replace every
`headline(...)` call in `render()`, the header comments and `plan.md`. "COMING IN …" and "COMING SOON" are teaser
wording; for a launch, ask the user for the label and end-card text.

The sample scenes (Live Activity card, Lock Screen widget, a week pill box wallpaper) belong to the example app.
Replace them with the user's own UI, keeping the techniques: per-frame 2D canvases mapped onto the phone screen,
the mascot standing on and pressing elements, time-lapses driven by one clock.

## Workflow

1. **Facts.** Read the user's repo for each feature: real strings, layout, palette, states, paid-tier gating, the
   app icon's colours (they become the mascot's). Ask what the code can't answer (which features, exact names, free
   or paid, teaser or launch, length; default 20 s vertical). A feature with no UI in the repo yet: ask for a design
   or screenshot. Without one, draw it from the app's design system, list it as illustrative, and show it on the
   first stills sheet.
2. **Mascot.** Default is the two-tone capsule in the app's brand colours. If the app has its own mascot or a simple
   icon shape, build it from SceneKit primitives in `buildCapsule()` (keep `CAP_HALF`, the unit size and the
   material list so shadows and the two passes still work).
3. **Plan** `plan.md` on the beat grid (96 BPM swing, 8 bars = 20 s). One feature = one mascot interaction with its
   real UI. One morning, one data set, one clock. The phone is the stage; a second device (Watch, iPad) comes in
   only for a feature that lives there (reference.md, "Second device"). List real vs illustrative.
4. **Copy.** Headline = what the user gets, never a feature name. A PRO chip on the sub line for paid things.
   If a humanizer skill is installed, run it on every line, then re-check the facts.
5. **Score.** Keep the sound (ukulele, marimba, whistle, snaps, E major, the synth chime on the end-card downbeat)
   but write new chords, melody and hits for the new choreography: every landing is a marimba note on its visual
   beat. If the app has its own notification sound, it can replace the synth chime (see the end of `score.swift`);
   match the score's key to it (motion-video `references/score-guide.md`). If the user asks for different music,
   change the instruments too. Target −13…−15 dBFS, 0 % clipping.
6. **Stills, two rounds minimum**, including mid-jump beats. Check: the mascot never covers info, it pauses on what
   it presses, shadows are visible, the phone top sits below the headline, nothing shows through the copy, and no
   real UI colour fights the orange headline.
7. **Render** in the background, then `frames` on the MP4 and look at them.
8. **Deliver** to `~/Downloads/<App>_<Topic>_3D_<N>s[_vN].mp4` and send or show the file to the user.
   Report beat by beat in seconds, real vs illustrative, and that the audio was judged by measurement. Keep earlier
   versions in `v1/`. Keep the video in one language until the user approves it; each extra locale is a full
   re-render, so ask which locales they want.

## Look contract

- Ivory/oat world with a soft sun. No dark studio background, no saturated pink.
- Neutral titanium phone, photo-style beige wallpaper, dark ink clock, light palettes for on-screen cards.
- SF Pro Rounded **heavy** headlines; line 2 is the orange gradient.
- The mascot interacts (lands, stomps, head-bumps, hops across elements). It never just orbits or poses.
- Real soft shadows. No DOF, no bloom.

## Common mistakes

| Mistake | Fix |
|---|---|
| Passing beats to `frames` or seconds to `stills` | `frames` = seconds, `stills` = beats (20 s = 32 beats) |
| Mascot leaves a button the instant it lands | Dwell about 0.2 beat so the press reads |
| Mascot stands on the time or label | Place it beside the info it would cover |
| Fading a mesh with `opacity` | Move, scale or hide it |
| Brand colour clashes with the orange headline gradient | Keep the brand on the mascot and version number; change the headline gradient only if the user asks |
