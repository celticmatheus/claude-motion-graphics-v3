#!/bin/bash
# One-time setup (free, no sudo, ~1.5 GB with torch). Everything goes to ~/.cache/motion-graphics-v3,
# so running it again finishes in seconds.
set -e
V="$HOME/.cache/motion-graphics-v3"; mkdir -p "$V/kokoro"
command -v uv >/dev/null || { curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"; }
VPY="$V/venv/bin/python"; [ -x "$V/venv/Scripts/python.exe" ] && VPY="$V/venv/Scripts/python.exe"
[ -x "$VPY" ] || { uv venv --python 3.11 "$V/venv"; [ -x "$V/venv/Scripts/python.exe" ] && VPY="$V/venv/Scripts/python.exe"; }
uv pip install --python "$VPY" kokoro-onnx soundfile numpy scipy pillow playwright torch torchaudio librosa matplotlib faster-whisper demucs
"$VPY" -m playwright install chromium
for f in kokoro-v1.0.onnx voices-v1.0.bin; do [ -f "$V/kokoro/$f" ] || curl -L -o "$V/kokoro/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"; done
SK="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$SK/kit/vendor"
[ -f "$SK/kit/vendor/gsap.min.js" ] || curl -L -o "$SK/kit/vendor/gsap.min.js" https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js
[ -f "$SK/kit/sfx/whoosh.mp3" ] || "$VPY" "$SK/tools/synth_sfx.py" "$SK/kit/sfx"
[ -f "$SK/kit/img/grain.png" ] || "$VPY" "$SK/tools/make_textures.py" "$SK/kit/img"
ok=1
node -e 'process.exit(+process.versions.node.split(".")[0] >= 22 ? 0 : 1)' 2>/dev/null && echo "node $(node -v) ok" || { echo "need Node 22+ (nodejs.org or brew install node)"; ok=0; }
command -v ffmpeg >/dev/null && echo "ffmpeg ok" || { echo "need ffmpeg (brew install ffmpeg / winget install ffmpeg)"; ok=0; }
[ $ok = 1 ] && echo "All set. Next: source tools/env.sh" || { echo "fix the items above, then run setup.sh again"; exit 1; }
