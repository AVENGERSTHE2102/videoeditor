# App 3D video — reference

Values from the example project in `template/` (20 s, 96 BPM swing, E major). Change content, not the look.
Colours marked "sample app" belong to the example's UI; take yours from the user's code.

## Look

| Element | Value |
|---|---|
| World (2D) | `PAPER` 0xFAF6EF ivory; soft sun top-right 0xFFFCF1 → 0xFBEBC4; oat glow bottom-left 0xEDE1CE; sand glow right 0xF1E6D6; 18 drifting confetti sprites (mini two-tone capsules + dots) in 0xE8C9A0, 0xF3D67A, 0xBFD6C2, 0xF2B98C, 0xCFE0E6, 6 of them blurred |
| Headlines | SF Pro Rounded heavy, ≤ 96 pt, centred at y 330, line 2 at +1.06·size; line 1 ink 0x33302C, line 2 gradient 0xEC6A2C → 0xF4A12E; words on 0.15-beat steps, `.mask` reveal; exit = blur 20 + fade + rise over 0.45 beat |
| Sub line | Rounded semibold 36, ink 72 %, 76 px under line 2; PRO chip fill 0x00897B, white heavy 22 |
| Label | `LABEL` ("COMING IN MYAPP x.y"), rounded heavy 30, kern 6, 0xEC6A2C |
| Scrim | cream gradient over the phone under the copy: 0.99 → 0.98 at 68 % → 0 at 720 px (830 px when the clock sits under the copy) |
| Phone | neutral titanium rim (0.74, 0.70, 0.64) metal 1 rough 0.3; floats ±1.1 mm; rises from −240 mm with raise-to-wake, sinks −420 mm for the end card |
| Wallpaper | user-photo style: beige wall 0xEEE6DA → 0xDCD0BF, window light, blurred plant shadow at 16 %; never saturated pink or dark presets |
| Lock Screen | iOS clock + widgets in dark ink 0x3B342E (light photo); flashlight/camera discs black 10 % |
| Live Activity | sample app light palette: 0xFFFFFF → 0xE3F5F1, primary 0x0D2B27, accent/button 0x00897B, glow 22 % |
| Pill box | sample app geometry in u = 1.675 pt, ink 0x252A3B, lids 0xF4A3A0 0xF7C08A 0xF2D875 0xA6DB9C 0x9CC8F0 0xB8A6EC 0xF0A6CF, past days 50 %, today's lid −9° and lifted 5 u |
| Mascot | `MASCOT_TOP` / `MASCOT_BOTTOM` / `MASCOT_SEAM` from the app icon (example: teal (0.05, 0.62, 0.55) top, green (0.26, 0.86, 0.55) bottom), clearcoat; unit r 1, length 3.6; sizes mm/unit: hero 9.5, on Live Activity 4.2, on phone top 3.4, on lids 2.9 |
| 3D version | `s3dHeadline(APP_VERSION)`, SFProRounded-Heavy, `MASCOT_TOP` face + clearcoat, scale 0.000205, camera-space (0, −0.041, −0.30), oBack pop |
| Light | warm bright HDR probe (`warmEnvironment`), key directional 700 with soft shadows (radius 16, 32 samples, colour (0.40, 0.32, 0.25, 0.30)), fill 260; no DOF, no bloom |
| End card | mascot lands on the floor + chime on the downbeat, `APP_NAME` rounded heavy 150 at y 1300, 3D version, `END_PILL` gradient pill at y 1700; fade to ivory over the last 0.35 s |

## Story grammar (one phone, one morning, one data set)

Mascot bounces in → jumps into the phone → each feature is one interaction with its real UI → camera pulls back to
the whole phone → value tagline → mascot jumps out to the end card. Interactions used so far:
ride a card and tap its foot to the countdown; stomp a button (button squashes, sparkles, state flips);
head-bump a widget from below (widget pops and updates); sit on the phone's top edge while time-lapses run;
hop across pill-box lids on the swung 8ths (each lid dips, rising marimba scale); land on today's lid as it pops open.
In-app scenes (built in a later project, not in `template/`): leap to the phone's top edge while the Lock Screen slides up to reveal the app (app
scaled 0.94 → 1, dimmed until revealed); stomp a toolbar glass button (it squashes and becomes the next state's
button); type a query by hopping key to key, one swung 8th per letter (key dips and greys, rising marimba + click),
with the list filtering after each letter (removed rows fade 0.2 beat, the rest slide up 0.42 beat); land on the
result card. Draw the app screen into the wallpaper canvas per frame; the Lock Screen layers slide up inside their
own full-screen canvases.

Copy: headline = what the user gets ("Your meds, right where you look.", "\"Did I take it?\" Just glance."),
never a feature name; feature names only implied by the visuals; a PRO chip on the sub line of any paid-only thing.
Run a humanizer pass on all copy if one is available.

## Music (score.swift)

96 BPM, swing 0.6, 8 bars = 20 s, E major. The end card closes on a synthesized E-major chime (marimba arpeggio + bell
on the downbeat). An app's own sound can replace it: `sampleOneShot(file, at: bt(downbeat) - onset, ...)`, with the
score in the sound's key. Instruments written in score.swift: Karplus-Strong ukulele strums, marimba,
whistled melody (octave 6), plucked bass, finger snaps, shaker, tambourine, soft triangle pad, `bloop` landings,
`fwip` jumps, `twinkle` sparkles. Every mascot landing = a marimba note + bloop on the same beat as the visual;
lid hops and foot taps use the same swing (`sw()` in scenes.swift). Target −13…−15 dBFS RMS, 0 % over 0.98
(`MIX.drive` 1.7 tames the transient peaks). When the user asks for different music, write a new score, don't tweak.

## Pipeline pitfalls (all measured)

- Two 3D passes per frame: pass 1 phone + floor + shadows with the mascot invisible (`colorBufferWriteMask = []`,
  `writesToDepthBuffer = true`, `renderingOrder = 100`), then the 2D scrim, then pass 2 mascot + 3D version only.
  Without depth writes the mascot casts no shadow; without the late rendering order it punches holes in the phone.
- Shadows: `lightingModel = .shadowOnly` planes (glass catcher just above the screen layers, floor plane); key light
  node re-aimed at the mascot every frame (orthographicScale 0.09) so the shadow map stays sharp.
- Keep DOF off: transparent planes turn blocky under DOF.
- Never fade a mesh with node.opacity (turns see-through); move it out of frame, scale it, or hide it.
- A hop must not start the instant it lands if the landing is the point (give the stomp ~0.2 beat on the button).
- Put a standing/stomping mascot beside the info it would cover (stomp left of the "8:00 AM" timer).
- Anything that jumps high crosses the copy zone: keep arcs low or let pass 2 draw it above the scrim.
- A hop with a large `bulge` (z toward the camera) throws a long, dark shadow smear onto the glass; keep bulge ≤ 5
  for hops across the screen.
- Push the camera in before a small interaction (a toolbar button at the top corner): at the whole-phone distance
  (0.49 m) the stomp reads as a speck. App text needs ~0.37 m to be legible; keep the top row below the 720 px scrim.
- Don't leave a gap between headlines while the scene changes: start the next headline during the transition hop.
- `frames` (probe) takes SECONDS; `stills` takes BEATS. 20 s = 32 beats at 96 BPM.
- Render cost: 20 s at 60 fps, SUB=5, two passes ≈ 5 min on an Apple-silicon Mac; run it in the background.

## Second device (not built yet; plan for these)

The template has one phone. `s3dPhone(screen:w:h:d:corner:finish:)` takes any size in mm, so a Watch or iPad is
another call with its own dimensions and its own `S3DCanvas` screen (a band or stand is extra geometry).
- Shadows: the key light's `orthographicScale` 0.09 covers one phone; widen it while both devices are in frame
  (tune on stills) and give the new glass its own `.shadowOnly` catcher.
- Text: a Watch face at phone scale is unreadable at 1080 wide; push the camera in for its scene.
- Time: drive every screen from `simTime` so all clocks agree.
- A Watch face is black in real life; keep it, the ivory world and titanium case carry the warmth.
- Render time grows with each device and pass; measure one still's time before promising a delivery time.

## Real vs illustrative (say this at delivery)

Real: UI layouts, palettes, strings and states read from the repo for each feature shown; app icon colours; the app's
own sound if used.
Illustrative: the photo, iOS clock tint, all times and sample data, time-lapses, the mascot and every bounce, UI
reacting to the mascot, anything animated that is a still image in the real app.
