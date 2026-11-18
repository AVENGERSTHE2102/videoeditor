# Score guide

The score is code (`score.swift`), concatenated between `engine/audio_core.swift` and
`engine/audio_main.swift`. Top-level statements place notes on the beat grid with `bt(beats)`;
`mixdown()` then applies sidechain, ping-pong delay, Freeverb, soft clip and normalization, and
writes 48 kHz 16-bit stereo `music.wav`. MIDI note numbers throughout (60 = C4).

## 1. Structure first
- Length is exact: `DURATION = bars × 4 × 60 / BPM`. 15 s → 6 bars @ 96, 8 bars @ 128, 5 bars @ 80.
- Give each scene a bar (or two), and put the harmonic change on the scene change.
- Plan the arc: sparse intro (pad/arp swelling, no drums) → groove when the first feature
  appears → the most motion under the hero feature → resolve on the tonic for the end card with
  a long tail. The last ~0.8 s fades (`MIX.fadeStart`).

## 2. Key: match the product's own sound
If the product has a notification/brand sound, build the score in its key so it can be dropped
in as the sonic logo. Find its pitches:
```python
import numpy as np
d=open('assets/sound.wav','rb').read(); i=d.find(b'data'); x=np.frombuffer(d[i+8:],dtype='<f4'); sr=48000
for a,b in [(0,.6),(.6,1.2),(1.2,2)]:
    s=x[int(a*sr):int(b*sr)]*np.hanning(int((b-a)*sr)); S=np.abs(np.fft.rfft(s)); f=np.fft.rfftfreq(len(s),1/sr)
    print(a,b,sorted(f[np.argsort(S)[-6:]].round(1)))
```
Map the peak frequencies to notes (415 Hz = G#4, 494 Hz = B4, 659 Hz = E5 → E major). Also check
the envelope for the onset offset (a chime often starts 0.3–0.5 s into the file), then place it with
`sampleOneShot(file, at: bt(beat) - onset, from: 0, len:, gain: 0.5…0.7)` so the attack lands on the beat.

## 3. Recipes

**Calm (health, wellbeing, productivity)**
- 90–100 BPM, major-key extended chords (maj9, m9, sus): e.g. I – vi – IV – V(sus→maj) – IV/V – I.
- `supersaw` pad (fc ≈ 1400, attack 0.35 s, long release), `ep` electric-piano comp voicing each
  chord, `sub` bass on roots, a sparse singable `bell` melody on chord tones.
- Drums only from the first feature: `softKick` on 1 and 3, `rim` on 2 and 4 in the hero
  section, swung `shaker` 8ths. No impacts, no risers — `swell` + `whoosh` into scene changes,
  a quick upward `bell` shimmer when an assistant wakes, a soft two-note bell for each answer.
- `MIX`: sidechainDepth 0.3, reverbWet 1.2–1.3, drive 0.8, ceiling 0.89 → about −13 dBFS RMS.

**Energetic (launch, trailer)** — `examples/scores/energetic-128bpm.swift`
- 124–130 BPM, minor → relative major: i – VI – III – VII.
- Intro: clock `tick`s, filtered `pluck` arp opening up, `riser` into the first drop.
- Drops: `impact` + a `supersaw` stab; 4-on-the-floor `kick`, `clap` on 2/4, 16th `hat`s with an
  open hat on the off-beat, offbeat `bass`, 16th `pluck` arp; `snare` rolls before each drop; a
  half-beat of silence (only a `swell`) before the final hit.
- `MIX`: sidechainDepth 0.75–0.8, release 0.11, drive 1.1, ceiling 0.93 → about −9.5 dBFS RMS.

**Premium / cinematic** — 70–84 BPM; long `supersaw` swells, low `sub`, `bell` motifs with
delay, one `impact` at the reveal, no drums or only `softKick` on downbeats.

## 4. Sync points to hit
- Every scene change on a downbeat; a transition sound starting ~1 beat before it.
- An audible event under each visual "landing": notification (brand sound), confirmation
  (bell), logo (drop or chord bloom).
- Words appearing: keep them on 8ths/16ths of the grid so they feel spoken to the rhythm.

## 5. Checking what you can't hear
`scripts/levels.py` prints RMS, peak, clipping share and per-beat loudness. Targets: calm −12…−15
dBFS, energetic −9…−10; 0% samples over 0.98; the intro several dB under the groove; a clear dip
at any drop-out. `peak before norm` ≫ 1 means the bus is saturating — lower `MIX.drive` or
instrument gains. Always tell the user you judged the mix by numbers and ask them to listen.
