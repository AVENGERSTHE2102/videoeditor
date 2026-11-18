# Example — "MyApp 2.0" teaser (3D), 20 s

20 s · 1080×1920 · 60 fps · 96 BPM with swing (beat 0.625 s) · 32 beats / 8 bars · E major · cheerful, bright, gentle
Teaser: "Coming in MyApp 2.0". Value first, not a feature tour. Real 3D (SceneKit through `s3d.swift`).
The sample app is a medication reminder. Its mascot, a two-tone capsule, is a little character that hops around one
phone's Lock Screen on one morning (Saturday, October 17). Neutral, warm world: ivory paper, soft sun, drifting
confetti; the phone shows a photo wallpaper (a beige wall with a plant's shadow), dark iOS clock, a Live Activity in
a light palette. Replace this file with your own plan before you touch `scenes.swift`.

| Bar | Beats | Scene | Cues |
|---|---|---|---|
| 1 | 0–4 | Mascot bounces in | 0 falls in · lands 1.0, 1.75, 2.25 (marimba + bloop, dust puff) · 0.6 LABEL · 1.25 "Your meds, / right where you look." · 2.7 phone rises, screen wakes (raise to wake) · 3.25 mascot jumps into the phone |
| 2–3 | 4–12 | Live Activity | 3.95 card slides up · 4.5 mascot lands on the card (card dips) · 4.4 "A little heads-up / before each dose." · 5–8 countdown time-lapse 7:45 → 0:02, mascot taps its foot on the woodblock 8ths · 8 "Took it? Tap Taken on the Lock Screen." + PRO · 8, 9 tick, tock (0:02, 0:01), mascot crouches · 9.5 leaps · 10 stomps Taken at 8:00 (sparkles, chord) · card turns Taken, 8:00 AM, collapses · 10.7 back on the card, happy wiggle |
| 4 | 12–16 | Last Dose widget | 11.5 jumps · 12 head-bumps the widget from below, it flips to "now" · 12.15 ""Did I take it?" / Just glance." · 12.75 flips up onto the top of the phone · 13–13.5 Taken card leaves · 13.6–15.2 time-lapse to 10:00, "now" → "2 hours ago", the sun climbs · 14.8 pill box builds in |
| 5–6 | 16–24 | Pill box wallpaper | 15.25 drops onto Sunday's lid · 16–18.6 hops Sun → Fri on the swung 8ths, each lid dips (rising E-major marimba scale) · 16.15 "Your whole week, / always in sight." · 18 "Your pill box, as your wallpaper." + PRO · 19.25 big hop · 20 lands on today's lid, it pops open, today's column lights up (sparkles) · 21.6–23.4 camera pulls back to the whole phone |
| 7 | 24–28 | Tagline | 24 "Less to remember. / Your Lock Screen has it." · little hop in place · 26 mascot jumps out toward the camera, phone sinks away (swell) |
| 8 | 28–32 | End card | 28 mascot lands (synth chime) · 28.25 APP_NAME · 28.75 3D APP_VERSION pops in · 29.4 END_PILL · fade to ivory over the last 0.35 s |

Real vs illustrative: in your own plan, list which layouts, palettes, strings and states you read from your app's code,
and which parts are illustrative (photo, times, sample data, time-lapses, the mascot and every bounce).

Score (score.swift): Karplus-Strong ukulele strums, marimba, whistled melody, plucked bass, finger snaps, shaker,
tambourine, soft pad; mascot landings are tuned marimba notes; the end card closes on a synthesized E-major chime.
Build: `bash mv3d.sh audio` · `bash mv3d.sh stills <beats>` · `bash mv3d.sh video` · `bash mv3d.sh frames out.mp4 <seconds>`.
3D is rendered in two passes: phone + shadows (mascot invisible but casting) under the cream scrim, mascot on top.
