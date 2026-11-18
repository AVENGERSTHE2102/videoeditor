# Engine API

Signatures as they appear in `engine/`. Coordinates: top-left origin, y down, full-res pixels.
Time: `t` in seconds, `b = t / BEAT` in beats. The worked project `~/.claude/skills/app-3d-video/template/scenes.swift`
uses most of this and is the best reference for idiom.

## Contents
- Video: globals · colour · easing · drawing · type · symbols · textures & reactive · looks · devices & UI · optics · finishing · entry points
- Audio: globals · helpers · instruments · mix

## Video (`video_core.swift`)

### Globals
`W, H, FW, FH, CX, CY, FPS, DURATION, FRAMES, BEAT, SUB, DIR` (from env / argv). Palette vars
(reassign at top of scenes.swift): `INK, TEAL, MINT, GREEN, GLOW, PAPER, DARKTEXT, ORANGE, DARK_MID, LIGHT_GLOW_A, LIGHT_GLOW_B` (`UInt32` hex).
`ctx` is the current CGContext (swapped automatically inside layers).

### Colour
- `C(_ hex: UInt32, _ a: Double = 1) -> CGColor`
- `mix(_ a: UInt32, _ b: UInt32, _ t: Double, _ alpha: Double = 1) -> CGColor`
- `grad(_ cs: [CGColor], _ locs: [CGFloat]? = nil) -> CGGradient`

### Easing and time
`cl, pr(b, start, dur), lerp, oExpo, iExpo, ioExpo, oCubic, iCubic, ioCubic, oBack(x, s)`,
`spring(_ seconds, k: 7, w: 15)` (0→1 damped), `secs(_ beats) -> seconds`.

### Drawing
- `save { … }`: push/pop state, including the multiplied alpha. `setA(_ a)` multiplies alpha; always use it instead of `ctx.setAlpha`.
- `rr(rect, radius) -> CGPath`, `fill(path, color)`, `fillRect(rect, color)`
- `radial(center, radius, colors, locs?)`, `linear(path?, colors, from, to, locs?)` (clipped to path if given)
- `scaleAbout(x, y, s)`, `img(cgImage, rect, alpha:)`, `load("assets/x.png") -> CGImage`
- `ring(center, r, lineWidth, color)`, `flash(b, at:, strength)` (full-frame flash decaying over 0.4 beat)

### Type
- `font(size, .heavy, rounded: false, mono: false) -> NSFont` (SF Pro; `mono` gives monospaced digits)
- `tp(string, font, kern:) -> TP` (cached glyph path + width/asc/desc). `drawTP(tp, x, baselineY, Fill, alpha:)`
- `text(string, font, x, baselineY, align: 0|0.5|1, Fill, kern:, alpha:)`
- `Fill.solid(color)` / `Fill.grad([colors])` (diagonal gradient across the word)
- `fitSize(lines, size, weight, maxW:, kern:) -> CGFloat` (largest size that fits)
- `kinetic([(word, startBeat)], font, x:, y:, align:, b:, kern:, style: .mask | .rise, dur: 0.55) { index in Fill }`: word-by-word reveal. `.mask` slides up inside the line box; `.rise` scales and fades in (good for transcripts).

### SF Symbols
- `drawSymbol("checkmark.circle.fill", pt, center:, color, scale:, alpha:, weight:)`: tinted, cached.

### Textures and audio-reactive
- `GRAIN` (film grain tile), `CONIC` (assistant palette sweep), `energy(t) -> 0…1` (smoothed music RMS).

### Looks
- `bgDark(b, glow: 1, tint:)`: dark base with breathing glows. `bgLight(b)`: light base with soft glows.
- `bokeh(b, alpha:)`: drifting out-of-focus discs (additive). `vignette(strength)`.
- `miniPill(center, len, rot, color, alpha:)`: two-tone capsule (a particle shape; swap in your own).
- `burst(seed:, n, spread:) -> [Particle]`, `drawBurst(particles, origin, b, startBeat, durBeats)`

### Devices and UI
- `phone(shot: CGImage?, cx:, top:, w:, rot:, alpha:, shadow:, dark:, screen: ((CGRect) -> Void)?)`: iPhone-style body, titanium rim, island, sheen. Pass a screenshot, or a `screen` closure that draws vector UI into the screen rect (scale `s = rect.width / 402` for iOS points).
- `glass(rect, radius, dark:, alpha:, shadow:)`: card with highlight, border, shadow.
- `iconTile(icon, center, size, alpha:, glowCol:, glowA:)`: app icon with a coloured glow.
- `header(num, label, b, start, y:, dark:)`: numbered section label.
- `siriEdge2(intensity, b, rect:, radius:, ws:)`: assistant glow around a rounded rect. Scale `ws` with the phone.
- `siriOrb(center, r, b, energy, alpha:)`: an orb made of additive blobs.

### Optics
- `focus(sigma, alpha:) { draw }`: draws the closure through a real gaussian blur (rack focus). Below 0.6 px it draws sharp.
- `frosted(path, sigma:, tint:)`: blurs what's already under `path` (glass), then tints it.
- `renderLayer { draw } -> CGImage` (half-res offscreen), `blurImg(image, sigma, scale:)`.
- `makeImage(w, h) { rect in draw } -> CGImage`: bake static art once (wallpapers etc.), e.g. `let WALL = makeImage(804, 1748) { r in … }` and `let WALL_BLUR = blurImg(WALL, 28)`.

### Finishing
- `finish(frame:, t:, vignetteStrength:, fadeOutFrom:)`: vignette, grain and the final fade. Call at the end of `render`.

### Entry point you write
```swift
func render(_ t: Double, frame: Int) {
    let b = t / BEAT
    ctx.saveGState()
    scaleAbout(CX, CY, CGFloat(1 + 0.006 * sin(b * 0.4)))   // camera breath
    if b < 4 { worldIntro(b) } else if … { … }
    ctx.restoreGState()
    finish(frame: frame, t: t, vignetteStrength: 0.4, fadeOutFrom: DURATION - 0.4)
}
```
`video_main.swift` calls it `SUB` times per frame at sub-frame offsets (shutter 180°) and averages
the results, which is where the motion blur comes from. It also handles `--stills` and the H.264
(28 Mbps, BT.709) + AAC 256k encode.

## Audio (`audio_core.swift`)

### Globals
`SR = 48000, BPM, B (beat seconds), TOTAL, N`, `assets` = project dir, buses `dryL/R` (unducked),
`duckL/R` (sidechained to kicks), `revL/R` (reverb send), `dlyL/R` (delay send), `MIX` settings.

### Helpers
`hz(midi)`, `idx(seconds) -> sample`, `bt(beats) -> seconds`, `SVF().run(x, cutoff, q) -> (lp, bp, hp)`,
`add(&L, &R, sampleIndex, value, pan:)`.

### Instruments (time args in seconds; use `bt()`)
- Calm: `ep(t, midi, dur, gain, pan:)` FM electric piano · `bell(t, midi, gain, pan:)` · `softKick(t, g)` · `rim(t, g)` · `shaker(t, g, pan:)` · `sub(t, midi, dur, g)`
- Energetic: `kick(t, g)` · `clap(t, g)` · `hat(t, open:, g, pan:)` · `snare(t, g, pitch:)` · `bass(t, midi, dur, g)` · `pluck(t, midi, g, bright:, pan:)` · `tick(t, tock:, g)`
- Both: `supersaw(t, notes, dur, att:, rel:, g:, fc: { t in cutoff }, toDuck:, rev:)` · `impact(t, g)` · `riser(t0, t1, g)` · `swell(t0, t1, g)` · `whoosh(t, dur, g)` · `sampleOneShot(path, at:, from:, len:, gain:)` (48 kHz mono float32 WAV)
- `kick`/`softKick` register sidechain triggers.

### Mix
`MIX.sidechainDepth, sidechainRelease, delayBeats, delayFeedback, reverbWet, drive, ceiling, fadeStart`.
`audio_main.swift` calls `mixdown()`.
