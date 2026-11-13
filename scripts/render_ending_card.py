#!/usr/bin/env python3
"""Render template/ending-card.html -> template/ending-card.png
(1080px wide = 360 CSS px phone column x3, cropped to the card). Run after editing ending-card.html."""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import TEMPLATE, find_chrome  # noqa: E402

src = os.path.join(TEMPLATE, "ending-card.html")
out = os.path.join(TEMPLATE, "ending-card.png")
with tempfile.TemporaryDirectory() as tmp:
    raw = os.path.join(tmp, "raw.png")
    subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=3", "--window-size=360,400",
                    f"--screenshot={raw}", "file://" + src], check=True, capture_output=True)
    im = Image.open(raw).convert("RGB")
box = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
im = im.crop((0, 0, im.width, box[3]))     # drop the white page below the card
im.save(out, optimize=True)
print(out, im.size)
