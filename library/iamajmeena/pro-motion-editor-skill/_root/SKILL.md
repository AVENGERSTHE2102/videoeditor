---
name: pro-motion-editor
license: PolyForm Noncommercial 1.0.0 (derivative of onetake — see LICENSE / NOTICE)
metadata:
  version: 0.3.0
  engine: onetake (feitangyuan/onetake, synced to 4157581 / 2026-10-12)
description: "Pro-Motion Editor — Claude Code skill for promo videos, reels, YouTube videos, ads and product motion graphics (9:16 and 16:9) the glyph-motions way — onetake's deterministic HTML composition + shutter-blur render pipeline, plus a hard-won rule set: every visual built in stages on the spoken word (no prefilled cards), fast larger-than-life pacing, camera that travels to every click, 3D perspective that changes per beat, glass panels that FORM, full-screen / overlay / text-behind-speaker layer mix, blood-red impact on negative words, per-format safe zones, real UIs, SFX as a separate WAV, HD draft before 4K. Use for any animation / motion graphic / ad / reel for a talking-head or product, Hinglish voice-driven cuts, YouTube launch films, and when the user says 'one take', 'glyph', 'animation', 'ad', 'reel graphics'."
---

# Pro-Motion Editor (glyph-motions) · v0.3.0

onetake (Patrick, feitangyuan/onetake) is the engine; glyph-motions is the taste. Read `RULES.md` first — it is the
curated list of rules that came from real corrections. Then `TECHNIQUES.md`, `GOTCHAS.md`. `CORRECTIONS.md` and
`REFERENCES.md` are the evidence logs. `CHANGELOG.md` says what changed per version.

## Layout of this skill
- `lib/motion.js`, `lib/ui_kit.js` — onetake's move library (window.OM). `lib/glyph.js` — ours (window.GM): `cameraToClicks`,
  `applyTilt`, `glass`, `formBox`, `chip`, `words`, `wordList`, `rollTo`, `frameIndex`, `motionBudget`.
- `scripts/` — onetake's `render.py` (frame-by-frame + shutter blur), `stills.py`, `probe.py`, `verify_promo.py`, `analyze_ref.py`,
  `look.py`, `sfx_palette.py`, `vo_tools.py`, `gallery.py`; ours: `vstills.py` (vertical contact sheet; stills.py is 16:9 only),
  `new_reel.py`, `transcribe.py`, `make_preview.py`.
- `looks/` — onetake's six measured looks (`looks.json`) + OFL faces; `python scripts/look.py sheet` / `apply <look> comp.html`.
- `gallery/` — one live demo per onetake move (`gallery/gallery.html?demo=iris&play`) and `gallery/sheets/<move>.png`: pick moves by looking.
- `templates/reel9x16/comp.html` — vertical starter built on lib/glyph.js (test render passed); `templates/comp.html` — onetake landscape DOM example. `references/*.md` — onetake's docs (composition, motion-library, rhythm, sound, product-demo, reference-deconstruction).
- `examples/` — real builds (code only, no media): `juno/` (patching a ChatGPT film to v2 with camera+glass+words),
  `ddr/` (series ident with real-3D icons + reel comp), `screenlark/` (shared kit sl.js, 3 concepts, morph-chain ad B2, UI-rebuild Q1).

## Protocol (in order, no skipping)
1. Read RULES.md + GOTCHAS.md, and the project's own AGENTS.md / RULES.md (they win). Confirm the FORMAT (9:16 reel or 16:9 YouTube) and its safe zone (RULES #31). New reel? Transcribe immediately (rule 5), show cleaned transcript + timestamps. Start a `NOTES.md` in the project (rule 38).
2. Beat-by-beat plan (layer per range: speaker full-screen / overlay / text behind speaker / split / recording; voice-synced). Ask everything unclear in ONE message.
3. Reference deconstruction (`analyze_ref.py`) -> 3 concepts that differ in their central idea, each with its look (RULES #30) -> user picks.
4. Beat sheet with CARRY (one container morphs through beats; nothing just replaces) + a WORD -> ACTION table per beat (RULES #24).
5. `stills` (use `vstills.py` for 9:16): check early / mid / final construction frames of each beat (RULES #25) -> ONE beat as a 5-9 s trial -> light preview copy -> approval -> next beat.
6. Full render in Full HD -> approval -> 4K. SFX as a separate WAV (RULES #4, section 8). Log every correction/learning into this folder immediately.

## Non-negotiables (short form; full list in RULES.md)
- Everything is a pure function of time; real video only as jpg sequence; never `<video>`.
- No prefilled cards: text -> container draws -> objects travel in -> labels build. Every spoken word = one construction action.
- Fast, larger than life: slams, floods, irises, whips, punches, shakes; no slow drifts. Rest-leg FAIL under this is intended — report it.
- Camera travels to every click; perspective tilts differently each beat; shutter blur on fast moves.
- Hook = most advanced part. Variety of layouts and layers (full-screen / overlay / text behind speaker). Gradient-only moving background (no particles). Nothing on the face.
- Blood red only as a ~0.8 s background impact on a negative word, never on the person, never held.
- Safe zone per format (RULES #31). Original UIs and real logos only.
- Original voice untouched; SFX always a separate WAV; HD draft before 4K; VO scripts paste-ready plain text.

## New video? (install -> edit)
`INSTALL.md` installs this skill; `WORKFLOW.md` is the step-by-step. One-liners: `scripts/new_reel.py <Name> <source>` (frames + audio + transcript),
`scripts/transcribe.py` (no-VAD, auto re-chunks stretched words/gaps into flags.txt), `scripts/make_preview.py` (preview / GIF), `scripts/vstills.py` (vertical contact sheet).
Landscape/YouTube: same loop at 1920x1080 (see WORKFLOW.md).

## Minimal use of lib/glyph.js
```js
const { keys, moves } = GM.cameraToClicks([{ at: 42.62, x: 786, y: 240 }]);
const cam = OM.camera(t, keys, { W: 1080, H: 1920 });
GM.applyTilt(canvas, cam, beatIndex, k);
GM.formBox(g, t, 36.55, 37.4, {x:395,y:226,w:110,h:64,r:32}, {x:54,y:184,w:792,h:115,r:24});
GM.words(g, t, GM.wordList(transcriptWords, 40, 4), 83, 253, 32, 450, '#fff');
window.__motion = GM.motionBudget(moves);
```
