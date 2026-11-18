#!/bin/bash
# motion-video build/run helper.
#   mv.sh <projectDir> audio                 compile + render score.swift -> music.wav, print levels
#   mv.sh <projectDir> stills <beats>        e.g. "0.5,2,4.25,8" -> stills/ + sheet.png (SUB=1, fast)
#   mv.sh <projectDir> video [out.mp4]       full render (SUB=5 motion blur) + probe
# Settings come from <projectDir>/project.env (BPM, DURATION, W, H, FPS). Nothing here touches git.
set -e
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
P="$(cd "$1" && pwd)"; CMD="$2"
# project.env supplies defaults; variables already set in the environment win (e.g. W=1920 H=1080 mv.sh …)
for v in BPM DURATION W H FPS; do eval "_ov_$v=\${$v-}"; done
[ -f "$P/project.env" ] && set -a && source "$P/project.env" && set +a
for v in BPM DURATION W H FPS; do eval "if [ -n \"\$_ov_$v\" ]; then $v=\$_ov_$v; fi"; done
export BPM="${BPM:-96}" DURATION="${DURATION:-15}" W="${W:-1080}" H="${H:-1920}" FPS="${FPS:-60}"
B="$P/.build"; mkdir -p "$B"
build_video() {
  cat "$SKILL/engine/video_core.swift" "$P/scenes.swift" "$SKILL/engine/video_main.swift" > "$B/video.swift"
  swiftc -O "$B/video.swift" -o "$B/render" 2>&1 | grep -E "error" -A3 || true
  [ -x "$B/render" ] && [ "$B/render" -nt "$B/video.swift" ] || { echo "video build failed"; exit 1; }
}
case "$CMD" in
  audio)
    cat "$SKILL/engine/audio_core.swift" "$P/score.swift" "$SKILL/engine/audio_main.swift" > "$B/audio.swift"
    swiftc -O "$B/audio.swift" -o "$B/audio" 2>&1 | grep -E "error" -A3 || true
    [ "$B/audio" -nt "$B/audio.swift" ] || { echo "audio build failed"; exit 1; }
    "$B/audio" "$P" "$P/music.wav"
    python3 "$SKILL/scripts/levels.py" "$P/music.wav" ;;
  stills)
    build_video
    F=$(python3 -c "import sys;print(','.join(str(int(round(float(b)*60/$BPM*$FPS))) for b in '$3'.split(',')))")
    rm -rf "$P/stills"; SUB="${SUB:-1}" "$B/render" "$P" --stills "$F" >/dev/null
    python3 "$SKILL/scripts/sheet.py" "$P/sheet.png" "$P"/stills/f*.png --cols "${COLS:-4}" ;;
  video)
    build_video
    OUT="${3:-$P/out.mp4}"
    SUB="${SUB:-5}" "$B/render" "$P" "$OUT" | tail -2
    [ -x "$B/probe" ] || swiftc "$SKILL/scripts/probe.swift" -o "$B/probe" 2>/dev/null
    "$B/probe" "$OUT" "$B" ;;
  *) echo "usage: mv.sh <projectDir> audio|stills <beats>|video [out.mp4]"; exit 1 ;;
esac
