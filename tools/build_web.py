#!/usr/bin/env python3
"""Build the browser version into build/web/ with pygbag (https://pygame-web.github.io).

1. Makes the synthesised sounds once, at the browser's 48000 Hz, into web_sounds/*.ogg (making
   them in the browser takes seconds and stalls the game).
2. Runs pygbag, which packs the game folder into build/web/.

Needs pygame-ce, pygbag (python3 -m pip install pygbag) and ffmpeg on PATH (or FFMPEG=/path):
pygbag converts the .wav sounds and music to .ogg for the browser with it.
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = dict(os.environ)
ffmpeg = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
if not ffmpeg:
    sys.exit("ffmpeg not found (set FFMPEG=/path/to/ffmpeg)")
env["PATH"] = os.path.dirname(os.path.abspath(ffmpeg)) + os.pathsep + env.get("PATH", "")


def render_web_sounds():
    import array
    import tempfile
    import wave
    sys.path.insert(0, ROOT)
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    from digestion_lab import audio
    audio.SR = 48000  # what browsers mix at
    out = str(audio.WEB_SOUNDS)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    built = audio._build_all()
    assert sorted(built) == sorted(audio.WEB_NAMES), "update WEB_NAMES in digestion_lab/audio.py"
    with tempfile.TemporaryDirectory() as tmp:
        for name, samples in built.items():
            wav = os.path.join(tmp, name + ".wav")
            data = array.array("h", (int(max(-1.0, min(1.0, v)) * 32000) for v in samples))
            with wave.open(wav, "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(audio.SR)
                handle.writeframes(data.tobytes())
            subprocess.run([ffmpeg, "-loglevel", "error", "-y", "-i", wav, "-c:a", "libvorbis", "-q:a", "4",
                            os.path.join(out, name + ".ogg")], check=True)
    print(f"web_sounds: {len(built)} sounds")


render_web_sounds()
subprocess.run([sys.executable, "-m", "pygbag", "--build", "--title", "Digestion Lab", "--app_name", "digestion-lab", "."],
               cwd=ROOT, env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if not os.path.exists(os.path.join(ROOT, "build", "web", "index.html")):
    sys.exit("pygbag did not write build/web/index.html")
print("build/web ready: upload the folder as-is")

# pygbag sometimes sizes the canvas before the game has opened its window, squeezing the game
# into a square: add a small script that keeps it the game's shape (tools/web_canvas_fix.py).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web_canvas_fix  # noqa: E402

web_canvas_fix.apply(os.path.join(ROOT, "build", "web", "index.html"))
