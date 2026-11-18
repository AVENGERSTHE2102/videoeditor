# Motion direction

## Contents
1. Tone presets
2. Easing and springs
3. Transitions
4. Layout and type
5. Storytelling patterns
6. Stills review checklist
7. Engine gotchas

## 1. Tone presets

| Tone | BPM | Scenes in 15 s | Reveal length | Springs | Transitions | Accents |
|---|---|---|---|---|---|---|
| Calm / health / finance / wellbeing | 84–100 | 4–5 | 0.8–1.0 beat | `k 5, w 6` (barely any overshoot) | rack focus, iris, slow dissolve, camera push through a logo | soft ring pulses, bokeh, light sweeps |
| Confident product launch | 110–120 | 5–6 | 0.6–0.8 beat | `k 6.5, w 11` | whip pans with motion blur, focus pulls | flashes on downbeats, particle bursts |
| Energetic / trailer / gaming | 124–130 | 6–8 | 0.4–0.55 beat | `k 7, w 15` (lively overshoot) | whips, iris, hard cuts on drops, a silent drop-out before the last hit | shockwave rings, particles, camera bumps on every kick |

Medical and health products read as untrustworthy when frantic: fewer, longer shots; no
bounce on anything carrying data; confirmations are a check plus a soft ring, not confetti.

## 2. Easing and springs

- `pr(b, start, dur)` gives 0…1 progress in beats; wrap it in an easing curve.
- Entrances: `oExpo` (UI and type), `oCubic` (soft fades). Exits: `ioCubic`. Camera pushes: `iExpo`.
- `spring(secs(b - start), k:, w:)` for physical things (phones rising, cards dropping). The ratio
  k/w sets overshoot: ≈0.9 is calm, ≈0.5 lively.
- Stagger words by 0.1–0.25 beat; stagger list rows/cards by 0.5–0.75 beat.
- Anything that "lands" should land *on* a beat: start its move one reveal-length earlier.
- Keep something alive in every frame: slow camera breath (`1 + 0.006·sin(b·0.4)`), drifting
  bokeh, a glow reacting to `energy(t)`. A frozen frame reads as a slideshow.

## 3. Transitions

- **Rack focus**: `focus(sigma)` the outgoing world up to ~34 px while fading it, and bring the
  next world from ~30 px to sharp. The calmest option that still looks expensive.
- **Iris**: clip a growing circle around the subject to reveal the next background. Use it for
  light↔dark changes; a plain crossfade between light and dark goes grey and muddy halfway.
- **Push through a logo**: zoom about a flat-coloured region of the icon (`iExpo`, ×20–26) and
  fade into a background of that colour.
- **Continuity**: keep one device on screen across scenes and change the world around it (the
  reminder lock screen became the Siri screen). It explains more than any cut.
- **Whip**: translate by a full frame with `ioExpo` over 0.45 beat; sub-frame motion blur makes it read.
- Pair every transition with a sound (swell, whoosh, bell) at the same beat.

## 4. Layout and type

- 1080-wide frame: side margin 80, header label at y≈180–260 (28 pt, tracking 5–9, small caps),
  headline 84–112 pt heavy with tracking −2.5…−3.5, sub-copy 32–40 pt regular at 70% alpha.
- Nothing a viewer must read under ~30 px at 1080 wide (≈ 17 pt iOS text at a 2.2× phone scale).
  Put the phone at 860–880 px wide when its screen content is the story.
- One accent per headline word (brand gradient on the key word). A product's own colour (Apple
  Health pink, Siri gradient) earns its place only on that product's name.
- Check spring overshoot positions: a phone that rests at y 740 can overshoot to 690 and hit
  the second line of a headline. Leave ~60 px of air.
- `kinetic(.mask)` clips each word to its line box; that clip has to fit descenders and the gap
  above the next element.

## 5. Storytelling patterns

- **Logo open**: rack-focus the icon in, one light sweep, headline words on the next beats,
  version pill, then push through the icon into the first scene.
- **Feature on a device**: headline states the benefit ("Take it or skip it from the
  reminder."); the device shows the real flow with product copy (notification → long-press →
  action → confirmation); one sticker points at the *new* part.
- **Voice assistant / Siri**: people must see it's the assistant *and* what the app says back.
  Same phone, assistant glow around the screen, the spoken request transcribed word by word,
  then the app's real answer as the assistant presents it (app attribution, spoken sentence,
  snippet). Two exchanges: one read (the question users actually worry about) and one write
  (the action it saves). Headline carries the value ("Just ask Siri. The app answers. No need to
  open it."), closing line restates it ("Check and log doses, hands-free.").
- **"Also new"**: 2–3 cards in one system (same size, tile icon, title + one-line benefit),
  arriving 0.6 beat apart. Never a row of mismatched screenshots.
- **End card**: icon in focus, wordmark, tagline over 3 half-bars, CTA pill with one shimmer,
  fade the last 0.3–0.4 s with the music tail.

## 6. Stills review checklist

Shoot at: each scene's resting state, the middle of every transition, the beat where each
element lands, and just after (spring overshoot).
- Text overlapping other text, the phone, or the frame edge? Descenders clipped by a mask?
- Every word legible at phone size? Anything important under 30 px?
- Alpha stacking right (things fading as a group, not popping)?
- Mid-transition frames clean — no grey mud, no half-drawn layers?
- UI consistent: same time, same names, same wallpaper, same device everywhere?
- Is it obvious *what the feature does* from the frames alone?
- Any empty third of the frame that should hold the composition?
- Claims true to the code? Illustrative values plausible and consistent across scenes?

## 7. Engine gotchas

- Use `setA()`, not `ctx.setAlpha()`: CoreGraphics alpha replaces rather than multiplies, and
  `save {}` restores the multiplied value. Nested fades only work through `setA`.
- `CGContext.drawConicGradient` isn't available from Swift here; the engine rotates a prebuilt
  `CONIC` image clipped to a stroke (see `siriEdge2`).
- `focus`/`renderLayer` nest up to 4 deep (layer pool). Layers are half-resolution, which is
  fine for anything being blurred and the reason sharp layers skip the pool.
- `frosted()` snapshots what's already drawn, so draw backgrounds before glass.
- Coordinates are top-left, y down, in full-res pixels, including inside layers.
- `energy(t)` reads `music.wav`: render audio first or it returns zeros.
- Stills use `SUB=1`; motion blur (`SUB=5`) only matters for the final render.
