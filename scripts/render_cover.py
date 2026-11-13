#!/usr/bin/env python3
"""Stamp this issue's date onto the date-free cover (template/cover-base.png) -> full-size PNG.

Usage:
    render_cover.py 2026-11-09 2026-11-15 out.png
      -> "2026年11月9日 —11月15日" (thin space before the dash, as on the original cover);
         a range crossing the new year repeats the year: "2026年12月28日 —2027年1月3日"

Defaults (size 45 / weight 600 / letter-spacing 4.5 / stroke 1.2, PingFang SC) were tuned so the
ink box matches the original Noto Sans CJK date (599x42px at x=115,y=613) within a few pixels.

The base is the original weekly cover with its date line removed. The date is rendered by
headless Chrome (PingFang SC, white) and placed so its ink box starts exactly where the
original date's ink started (x=115, y=613 on the 1902x827 base). Feed the output to
process_imgs.py as image 01 (COVER), like any other downloaded image.
"""
import argparse
import os
import subprocess
import sys
import tempfile
from html import escape

from PIL import Image, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import TEMPLATE, find_chrome  # noqa: E402

BASE = os.path.join(TEMPLATE, "cover-base.png")
INK_X, INK_Y = 115, 613          # top-left of the original date's ink on the base
FONT = "'PingFang SC','Hiragino Sans GB','Noto Sans CJK SC',sans-serif"


def shoot(html, w, h, out):
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "p.html")
        open(page, "w", encoding="utf-8").write(html)
        subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={w},{h}",
                        f"--screenshot={out}", "file://" + page],
                       check=True, capture_output=True)


def page(date, size, weight, left, top, base_url=None, spacing=0.0, stroke=0.0):
    bg = (f'<img src="{base_url}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;">'
          if base_url else "")
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;'
            f'background:#000;width:{W}px;height:{H}px;overflow:hidden;position:relative;'
            f'-webkit-font-smoothing:antialiased;}}</style></head><body>{bg}'
            f'<div style="position:absolute;left:{left}px;top:{top}px;white-space:nowrap;line-height:1;'
            f'font-family:{FONT};font-size:{size}px;font-weight:{weight};color:#FFFFFF;'
            f'letter-spacing:{spacing}px;-webkit-text-stroke:{stroke}px #FFFFFF;">{escape(date)}</div>'
            f'</body></html>')


def ink_box(path):
    im = Image.open(path).convert("RGB")
    return ImageChops.difference(im, Image.new("RGB", im.size, (0, 0, 0))).point(
        lambda v: 255 if v > 90 else 0).getbbox()


def date_label(start, end):
    s, e = date.fromisoformat(start), date.fromisoformat(end)
    tail = f"{e.year}年{e.month}月{e.day}日" if e.year != s.year else f"{e.month}月{e.day}日"
    return f"{s.year}年{s.month}月{s.day}日 —{tail}"


if __name__ == "__main__":
    from datetime import date
    ap = argparse.ArgumentParser()
    ap.add_argument("start", help="first day of the issue, YYYY-MM-DD")
    ap.add_argument("end", help="last day of the issue, YYYY-MM-DD")
    ap.add_argument("out")
    ap.add_argument("--size", type=float, default=45)
    ap.add_argument("--weight", type=int, default=600)
    ap.add_argument("--spacing", type=float, default=4.5)
    ap.add_argument("--stroke", type=float, default=1.2)
    a = ap.parse_args()
    a.date = date_label(a.start, a.end)
    W, H = Image.open(BASE).size
    kw = dict(spacing=a.spacing, stroke=a.stroke)
    with tempfile.TemporaryDirectory() as tmp:
        probe = os.path.join(tmp, "probe.png")
        shoot(page(a.date, a.size, a.weight, 200, 200, **kw), W, H, probe)   # measure where the ink lands
        x0, y0, x1, y1 = ink_box(probe)
        left, top = 200 + (INK_X - x0), 200 + (INK_Y - y0)
        shoot(page(a.date, a.size, a.weight, left, top, "file://" + BASE, **kw), W, H, a.out)
    out = Image.open(a.out).convert("RGB")
    out.save(a.out, optimize=True)
    print(f"{a.out} {out.size} date ink {x1 - x0}x{y1 - y0}px at ({INK_X},{INK_Y})")
