"""Web entry point for pygbag (https://pygame-web.github.io): Digestion Lab in the browser.

Build with:  python3 tools/build_web.py     (writes build/web/)
The desktop game still starts with `python3 -m digestion_lab`; nothing here changes it.
"""
import asyncio

from digestion_lab import audio  # noqa: F401  (before pygame.init, as on the desktop)
import pygame  # noqa: F401,E402  (must be imported here so pygbag loads pygame)

from digestion_lab.app import App  # noqa: E402


async def main():
    await App().run_web()


asyncio.run(main())
