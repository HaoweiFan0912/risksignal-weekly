#!/usr/bin/env python3
"""Render a RiskSignal weekly (source markdown) into WeChat-safe HTML, theme: 异常点 Outlier.

Usage:
    build_weekly.py weekly.md out.html manifest.json image_dir rel|b64 [rel_prefix]

  weekly.md     see README.md for the format (# 栏目 | EN, ## 标题, 正文 with ++下划线++, 来源：…, 看点：…)
  manifest.json image list from process_imgs.py; pass "-" to build without images
  rel|b64       rel = <img src="{rel_prefix}{file}"> ; b64 = images embedded (for the copy preview)
"""
import base64
import json
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import TEMPLATE  # noqa: E402

SRC, OUT, MANIFEST, IMG_DIR, MODE = sys.argv[1:6]
REL_PREFIX = sys.argv[6] if len(sys.argv) > 6 else ""
IMAGES = {} if MANIFEST == "-" else {i["n"]: i for i in json.load(open(MANIFEST, encoding="utf-8"))}


def img_src(n):
    name = IMAGES[n]["out"]
    if MODE == "b64":
        mime = "image/png" if name.endswith(".png") else "image/jpeg"
        data = base64.b64encode(open(os.path.join(IMG_DIR, name), "rb").read()).decode()
        return f"data:{mime};base64,{data}"
    return REL_PREFIX + name


# 结尾互动卡：logo + 点赞关注收藏转发 + 联系方式，整体预渲染成一张图（源文件 template/ending-card.html，
# 重新出图用 scripts/render_ending_card.py）。1080px 宽 = 手机版面 360px ×3。
ENDING_CARD = "ending-card.png"
# alt 文字（读屏/图片加载失败时显示）与卡片文案保持一致：template/ending-card-alt.txt
ENDING_ALT = open(os.path.join(TEMPLATE, "ending-card-alt.txt"), encoding="utf-8").read().strip()


def asset_src(name):
    """Template images (template/) are copied into the image dir so relative builds can reference them.
    Without an image dir (manifest "-") they are embedded instead."""
    import shutil
    src = os.path.join(TEMPLATE, name)
    if IMG_DIR == "-":
        return "data:image/png;base64," + base64.b64encode(open(src, "rb").read()).decode()
    os.makedirs(IMG_DIR, exist_ok=True)
    local = os.path.join(IMG_DIR, name)
    shutil.copy(src, local)
    if MODE == "b64":
        return "data:image/png;base64," + base64.b64encode(open(local, "rb").read()).decode()
    return REL_PREFIX + name


def picture(n, alt, radius=6, margin="0 0 14px"):
    return (f'<section style="margin:{margin};">'
            f'<img src="{img_src(n)}" alt="{escape(alt)}" '
            f'style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:{radius}px;"></section>')

INK = "#0E1726"
SIGNAL = "#F2501E"
PAPER = "#F6F4EF"
BODY = "#1F2937"
MUTED = "#5B6575"
SOFT = "#9AA6B8"
DEEP = "#1C2A40"
LINE = "#E5E2DA"
FONT = ("'Inter','Source Han Sans SC','Noto Sans SC','PingFang SC',"
        "'Hiragino Sans GB','Microsoft YaHei',sans-serif")
UNDERLINE = f"border-bottom:2px solid {SIGNAL};font-weight:600;color:{INK};"

HIGHLIGHTS = []  # filled from "看点：标题关键词 | 一句话看点" lines in the source


def leaf(text):
    return f'<span leaf="">{escape(text, quote=False)}</span>'


def dot(size=8, extra="", color=SIGNAL):
    """Signal dot drawn with the ● glyph. WeChat strips empty decorative spans
    (background + font-size:0 + &nbsp;) on paste, so the dot must be real text.
    The glyph's ink is ~0.76em, so font-size = size / 0.76."""
    return (f'<span style="color:{color};font-size:{round(size / 0.76)}px;line-height:1;{extra}">'
            f'{leaf("●")}</span>')


def rich(text):
    parts = re.split(r"\+\+(.+?)\+\+", text)
    out = []
    for i, part in enumerate(parts):
        if not part:
            continue
        out.append(f'<span style="{UNDERLINE}">{leaf(part)}</span>' if i % 2 else leaf(part))
    return "".join(out)


# ---------- parse ----------
chapters = []
META = {"期号": "", "期间": ""}  # only used by the text masthead (no cover image)
for line in open(SRC, encoding="utf-8").read().splitlines():
    line = line.strip()
    if not line:
        continue
    if line.startswith("看点："):
        key, _, text = line[3:].partition("|")
        HIGHLIGHTS.append((key.strip(), text.strip()))
    elif not chapters and line[:3] in ("期号：", "期间："):
        META[line[:2]] = line[3:].strip()
    elif line.startswith("# "):
        zh, _, en = [s.strip() for s in line[2:].partition("|")]
        chapters.append({"zh": zh, "en": en, "items": []})
    elif line.startswith("## "):
        chapters[-1]["items"].append({"title": line[3:], "body": [], "src": None})
    elif line.startswith("来源："):
        name, _, date = line[3:].rpartition("，")
        chapters[-1]["items"][-1]["src"] = (name, date)
    else:
        chapters[-1]["items"][-1]["body"].append(line)

total = sum(len(c["items"]) for c in chapters)
for c in chapters:
    for it in c["items"]:
        assert it["body"], f"item has no body text: {it['title']}"

# ---------- components ----------
def masthead():
    stats = [(str(total), "条信号", SIGNAL), (str(len(chapters)), "个栏目", "#FFFFFF"),
             (META["期间"] or "—", "收录区间", "#FFFFFF")]
    cells = []
    for i, (num, label, color) in enumerate(stats):
        sep = "" if i == 0 else f"border-left:1px solid {DEEP};padding-left:14px;"
        cells.append(
            f'<section style="flex:1;{sep}">'
            f'<p style="margin:0;font-size:20px;font-weight:700;color:{color};line-height:1.2;letter-spacing:-0.3px;">{leaf(num)}</p>'
            f'<p style="margin:4px 0 0;font-size:11px;color:{SOFT};letter-spacing:1px;">{leaf(label)}</p></section>')
    return (
        f'<section style="background:{INK};border-radius:8px;padding:24px 22px 20px;">'
        f'<section style="display:flex;align-items:center;margin-bottom:24px;padding-bottom:12px;border-bottom:1px solid {DEEP};">'
        f'{dot(8)}'
        f'<span style="margin-left:8px;font-size:11px;font-weight:700;letter-spacing:3px;color:#FFFFFF;">{leaf("RISKSIGNAL WEEKLY")}</span>'
        f'<span style="margin-left:auto;font-size:11px;color:{SOFT};letter-spacing:1px;">{leaf(META["期号"])}</span>'
        f'</section>'
        f'<p style="margin:0 0 8px;font-size:11px;font-weight:600;color:{SOFT};letter-spacing:2.5px;">{leaf("GLOBAL INSURANCE RISK SIGNALS")}</p>'
        f'<p style="margin:0 0 12px;font-size:24px;font-weight:700;color:#FFFFFF;line-height:1.35;letter-spacing:0.5px;">{leaf("全球保险风险信号周报")}</p>'
        f'<p style="margin:0;font-size:13px;color:{SOFT};line-height:1.8;">{leaf(" · ".join(c["zh"] for c in chapters))}</p>'
        f'<section style="display:flex;margin-top:22px;padding-top:16px;border-top:1px solid {DEEP};">{"".join(cells)}</section>'
        f'</section>')


def label_row(zh, en):
    return (f'<section style="display:flex;align-items:center;margin-bottom:12px;">'
            f'{dot(7)}'
            f'<span style="margin-left:8px;font-size:15px;font-weight:700;color:{INK};">{leaf(zh)}</span>'
            f'<span style="margin-left:8px;font-size:10px;font-weight:600;color:{MUTED};letter-spacing:2px;">{leaf(en)}</span>'
            f'</section>')


def daily_chart():
    return (f'<section style="margin-top:28px;">{label_row("每日一图", "DAILY CHART")}'
            f'{picture(special["DAILY"], "每日一图", radius=8, margin="0")}</section>')


def highlights():
    rows = []
    for i, (key, text) in enumerate(HIGHLIGHTS, 1):
        chap = next(c for c in chapters if any(key in it["title"] for it in c["items"]))
        border = "" if i == 1 else f"border-top:1px solid {LINE};"
        rows.append(
            f'<section style="display:flex;align-items:flex-start;padding:12px 0;{border}">'
            f'<span style="flex-shrink:0;width:34px;font-size:18px;font-weight:700;color:{SIGNAL};line-height:1.4;">{leaf(f"{i:02d}")}</span>'
            f'<section style="flex:1;">'
            f'<p style="margin:0;font-size:14px;font-weight:600;color:{INK};line-height:1.65;">{leaf(text)}</p>'
            f'<p style="margin:2px 0 0;font-size:11px;color:{MUTED};letter-spacing:1px;">{leaf(chap["zh"])}</p>'
            f'</section></section>')
    chips = "".join(
        f'<span style="display:inline-block;margin:0 6px 6px 0;padding:3px 9px;background:#FFFFFF;'
        f'border:1px solid {LINE};border-radius:4px;font-size:12px;color:{INK};">'
        f'{leaf(f"{n:02d} {c["zh"]} · {len(c["items"])}")}</span>'
        for n, c in enumerate(chapters, 1))
    return (f'<section style="margin-top:28px;background:{PAPER};border-radius:8px;padding:18px 18px 12px;">'
            f'{label_row("本期看点", "HIGHLIGHTS")}{"".join(rows)}'
            f'<section style="margin-top:8px;padding-top:12px;border-top:1px solid {LINE};">{chips}</section>'
            f'</section>')


def chapter_head(n, c):
    return (f'<section style="margin-top:44px;margin-bottom:20px;display:flex;align-items:flex-end;'
            f'border-bottom:2px solid {INK};padding-bottom:12px;">'
            f'<span style="font-size:24px;font-weight:800;color:{INK};line-height:1;letter-spacing:-0.5px;">{leaf(f"{n:02d}")}</span>'
            f'{dot(7, "align-self:flex-start;margin:0 12px 0 3px;")}'
            f'<section style="flex:1;">'
            f'<p style="margin:0;font-size:10px;font-weight:600;color:{MUTED};letter-spacing:2.5px;">{leaf(c["en"])}</p>'
            f'<p style="margin:3px 0 0;font-size:20px;font-weight:700;color:{INK};line-height:1.3;">{leaf(c["zh"])}</p>'
            f'</section>'
            f'<span style="font-size:12px;color:{MUTED};">{leaf(f"{len(c["items"])} 条")}</span>'
            f'</section>')


def item(it, first):
    sep = "" if first else f"border-top:1px solid {LINE};padding-top:22px;"
    pic = picture(it["img"], it["title"]) if it.get("img") else ""
    body = "".join(
        f'<p style="margin:0 0 12px;font-size:15px;line-height:1.85;color:{BODY};letter-spacing:0.3px;text-align:justify;">{rich(p)}</p>'
        for p in it["body"])
    source = ""
    if it["src"]:
        name, date = it["src"]
        source = (f'<p style="margin:0;font-size:12px;color:{MUTED};line-height:1.6;">'
                  f'<span style="display:inline-block;margin-right:8px;padding:1px 6px;background:{PAPER};border-radius:3px;color:{INK};font-weight:600;">{leaf("来源")}</span>'
                  f'{leaf(f"{name} · {date}" if name else date)}</p>')
    return (f'<section style="margin-bottom:22px;{sep}">'
            f'<p style="margin:0 0 12px;padding-left:10px;border-left:3px solid {INK};font-size:17px;font-weight:700;color:{INK};line-height:1.5;">{leaf(it["title"])}</p>'
            f'{pic}{body}{source}'
            f'</section>')


def ending():
    # 固定声明（模板）：每行一段，编辑 notice.txt 即可
    notice_path = os.path.join(TEMPLATE, "notice.txt")
    notes = [l.strip() for l in open(notice_path, encoding="utf-8") if l.strip()]
    note_html = "".join(
        f'<p style="margin:{"0" if i == 0 else "8px"} 0 0;font-size:12px;color:{MUTED};line-height:1.8;text-align:justify;">{leaf(t)}</p>'
        for i, t in enumerate(notes))
    # 结尾互动卡是一整张图（logo + CTA + 联系方式），避免公众号改动背景色或断行
    return (f'<section style="margin-top:48px;">'
            f'<img src="{asset_src(ENDING_CARD)}" alt="{escape(ENDING_ALT)}" '
            f'style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:8px;"></section>'
            f'<section style="margin-top:14px;background:{PAPER};border-radius:8px;padding:16px 18px;">'
            f'<p style="margin:0 0 8px;font-size:10px;font-weight:600;color:{MUTED};letter-spacing:2.5px;">{leaf("NOTICE · 声明")}</p>'
            f'{note_html}</section>')


# ---------- attach images ----------
# manifest keys: "COVER", "DAILY", or the H2 title the image sits under in the source doc.
# Item images are matched by title; a title edited in weekly.md (e.g. a typo fix) falls back
# to document order, with a warning so the pairing can be eyeballed.
special = {i["key"]: n for n, i in IMAGES.items() if i["key"] in ("COVER", "DAILY")}
item_imgs = [n for n in sorted(IMAGES) if n not in special.values()]
by_title = {IMAGES[n]["key"]: n for n in item_imgs}
all_items = [it for c in chapters for it in c["items"]]
if item_imgs:
    if len(item_imgs) != len(all_items):
        print(f"WARNING: {len(item_imgs)} item images vs {len(all_items)} items", file=sys.stderr)
    for idx, it in enumerate(all_items):
        n = by_title.get(it["title"])
        if n is None and idx < len(item_imgs):
            n = item_imgs[idx]
            print(f"WARNING: no exact title match, using image #{n} ({IMAGES[n]['key']}) for: {it['title']}",
                  file=sys.stderr)
        it["img"] = n

head = (picture(special["COVER"], "封面", radius=8, margin="0") if "COVER" in special else masthead())
parts = [head]
if "DAILY" in special:
    parts.append(daily_chart())
if HIGHLIGHTS:
    parts.append(highlights())
for n, c in enumerate(chapters, 1):
    parts.append(chapter_head(n, c))
    parts.extend(item(it, i == 0) for i, it in enumerate(c["items"]))
parts.append(ending())

html = (f'<section style="max-width:677px;margin:0 auto;padding:8px;box-sizing:border-box;background:#FFFFFF;'
        f'color:{BODY};font-family:{FONT};line-height:1.75;">\n' + "\n".join(parts) + "\n</section>\n")
open(OUT, "w", encoding="utf-8").write(html)
print(f"chapters={len(chapters)} items={total} -> {OUT}")
