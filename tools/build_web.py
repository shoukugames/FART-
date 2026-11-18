#!/usr/bin/env python3
"""Build the browser version into build/web/ with pygbag (https://pygame-web.github.io).

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
