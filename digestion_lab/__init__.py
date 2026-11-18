"""Digestion Lab: feed a wireframe body and predict burp, fart, or smooth ride."""
import os

__version__ = '0.1.4'

# True when running in a web browser (pygbag / WebAssembly).
WEB = __import__('sys').platform == 'emscripten'

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
