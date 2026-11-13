#!/usr/bin/env python3
"""RiskSignal weekly, end to end (theme 异常点 Outlier).

The weekly Google Doc ("周报" in Drive: 热点收集/<M.D.YYYY-M.D.YYYY>/周报) holds only the main content:
每日一图 -> 栏目 (H1) -> 快讯 (H2 + image + body + 来源：…) ... -> 相关新闻.
Everything around it comes from template/ (see docs/02-修改模板.md):
  cover   = template/cover-base.png + this week's Mon–Sun dates (render_cover.py)
  ending  = template/ending-card.png (logo + 点赞、关注、收藏、转发 + contact)
  notice  = template/notice.txt (copyright / disclaimer / AI-image lines)

Two steps, because the keyword underlines and 本期看点 are editorial choices made in between:

  make_weekly.py fetch --doc <DOC_ID> --folder <WEEK_FOLDER_ID> --week 2026-11-16
      -> <root>/<11.16.2026-11.22.2026>/ : weekly.md (doc text, no marks), 配图/原图 + 配图/公众号 (processed),
         manifest.json, marks.txt (skeleton to fill in). Prints titles and any warnings.

  make_weekly.py build --week 2026-11-16
      -> applies marks.txt, builds 周报_排版_异常点(risksignal-outlier).html (+ _预览.html with a copy
         button and embedded images), validates both, writes upload.json for the Drive upload step.

marks.txt:
  看点：<title keyword> | <one-line takeaway>          (3 lines; keyword must occur in one item title)
  <item title prefix> :: <phrase> || <phrase>         (1–3 underline phrases per paragraph, exact substrings)

The doc must be shared "anyone with the link can view" (images are read from its public mobilebasic view).
"""
import argparse
import hashlib
import html as htmllib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CONFIG, OUTPUT_NAME, OUTPUT_ROOT, VENDOR  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DEFAULT = OUTPUT_ROOT          # config.json "output_root"
OUT_NAME = OUTPUT_NAME
EN = CONFIG["section_en"]            # 栏目 -> 英文标签
H1_FIX = CONFIG["section_name_fix"]   # recurring typos in section names


def week_of(day):
    d = date.fromisoformat(day)
    mon = d - timedelta(days=d.weekday())
    return mon, mon + timedelta(days=6)


def week_dir(root, mon, sun):
    return os.path.join(root, f"{mon.month}.{mon.day}.{mon.year}-{sun.month}.{sun.day}.{sun.year}")


def text_of(fragment):
    t = htmllib.unescape(re.sub(r"<[^>]+>", "", fragment)).replace("\xa0", " ")
    return re.sub(r"[ \t\r\n]+", " ", t).strip()


def parse_doc(doc_html):
    """-> (sections, images, warnings). images: list of (key, url) in document order."""
    body = doc_html[doc_html.find("<body"):]
    blocks = re.finditer(r"<(h1|h2|p)\b[^>]*>(.*?)</\1>", body, re.S)
    sections, images, warnings = [], [], []
    pending_daily, item = False, None
    for m in blocks:
        tag, inner = m.group(1), m.group(2)
        imgs = [htmllib.unescape(u) for u in re.findall(r'<img[^>]*src="([^"]+)"', inner)]
        text = text_of(inner)
        if tag == "h1":
            name = H1_FIX.get(text, text)
            if name != text:
                warnings.append(f"栏目名已更正：{text} → {name}")
            if name not in EN:
                warnings.append(f"栏目「{name}」没有英文标签映射，章节标题里英文标签留空")
            sections.append({"zh": name, "en": EN.get(name, ""), "items": []})
            item = None
            continue
        if tag == "h2":
            if not sections:
                warnings.append(f"标题「{text}」出现在第一个栏目之前，已忽略")
                continue
            item = {"title": text, "body": [], "src": None, "after_src": []}
            sections[-1]["items"].append(item)
            continue
        # <p>
        if not sections:                                   # before the first 栏目: 每日一图 area
            if text == "每日一图":
                pending_daily = True
            for u in imgs:
                if pending_daily:
                    images.append(("DAILY", u))
                    pending_daily = False
                else:
                    warnings.append("开头有一张非「每日一图」的图片（旧版封面？），已跳过——封面由模板生成")
            if text and text != "每日一图":
                warnings.append(f"开头有未识别的文字，已忽略：{text[:30]}")
            continue
        if item is None:
            if text or imgs:
                warnings.append(f"栏目「{sections[-1]['zh']}」下、第一条快讯前有内容，已忽略：{text[:30]}")
            continue
        for u in imgs:
            images.append((item["title"], u))
        if not text:
            continue
        if text.startswith("来源：") or text.startswith("来源:"):
            item["src"] = "来源：" + text[3:].strip()
        elif item["src"]:
            item["after_src"].append(text)                 # e.g. legacy contact/disclaimer after the last item
        else:
            item["body"].append(text)
    for s in sections:
        for it in s["items"]:
            if it["after_src"]:
                warnings.append(f"「{it['title'][:20]}」来源行之后还有 {len(it['after_src'])} 段文字（旧版结尾/声明？），"
                                f"已忽略，开头：{it['after_src'][0][:24]}")
            if not it["body"]:
                warnings.append(f"「{it['title']}」没有正文")
            if not it["src"]:
                warnings.append(f"「{it['title']}」没有来源行")
    titles = {it["title"] for s in sections for it in s["items"]}
    with_img = {k for k, _ in images}
    for t in sorted(titles - with_img):
        warnings.append(f"「{t}」没有配图")
    return sections, images, warnings


def write_md(sections, path):
    out = []
    for s in sections:
        out.append(f"# {s['zh']} | {s['en']}".rstrip(" |"))
        out.append("")
        for it in s["items"]:
            out.append(f"## {it['title']}")
            out.extend(it["body"])
            if it["src"]:
                out.append(it["src"])
            out.append("")
    open(path, "w", encoding="utf-8").write("\n".join(out))


def save_drive(wd, **ids):
    """Remember this week's Drive ids in drive.json (doc_id, folder_id) for the upload step."""
    path = os.path.join(wd, "drive.json")
    data = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    data.update({k: v for k, v in ids.items() if v})
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def write_upload(wd, preview):
    """upload.json = everything the AI needs for the Drive connector call (create_file with a file reference)."""
    drive = json.load(open(os.path.join(wd, "drive.json"), encoding="utf-8")) if os.path.exists(
        os.path.join(wd, "drive.json")) else {}
    digest = hashlib.sha256(open(preview, "rb").read()).hexdigest()
    week_folder = os.path.basename(wd)
    up = {
        "local_path": preview,
        "size_mb": round(os.path.getsize(preview) / 1048576, 2),
        "sha256": digest,
        "file_reference": f"sha256:{digest}:{preview}",
        "title": CONFIG["drive"]["upload_title_format"].format(week_folder=week_folder),
        "parent_id": drive.get("folder_id"),
        "contentMimeType": "text/html",
        "disableConversionToGoogleType": True,
    }
    json.dump(up, open(os.path.join(wd, "upload.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if up["size_mb"] > 7.2:   # Drive connector: request ≤ 10,000,000 bytes after base64 (+33%)
        print(f"WARNING: 预览页 {up['size_mb']} MB，超过 Drive 上传上限（约 7.2 MB）。降低 process_imgs.py 的 "
              f"TOTAL_BUDGET_KB 后重新 fetch，或请用户手动上传。")
    print(f"upload {up['title']} ({up['size_mb']} MB) -> Drive folder {up['parent_id'] or '（未知：用 --folder 指定）'}"
          f"\n       详情见 {os.path.join(wd, 'upload.json')}")


def cmd_fetch(a):
    mon, sun = week_of(a.week)
    wd = week_dir(a.root, mon, sun)
    raw, pub = os.path.join(wd, "配图", "原图"), os.path.join(wd, "配图", "公众号")
    for d in (raw, pub):
        os.makedirs(d, exist_ok=True)
    doc_html = os.path.join(wd, "doc-mobilebasic.html")
    subprocess.run(["curl", "-sSLf", "-o", doc_html,
                    f"https://docs.google.com/document/d/{a.doc}/mobilebasic"], check=True)
    sections, images, warnings = parse_doc(open(doc_html, encoding="utf-8").read())
    if not sections:
        sys.exit("文档里没有找到任何栏目（H1）——确认链接共享已打开、文档是周报正文")
    write_md(sections, os.path.join(wd, "weekly.md"))
    save_drive(wd, doc_id=a.doc, folder_id=a.folder)

    manifest = [{"n": 1, "key": "COVER", "file": "01.png"}]
    subprocess.run([sys.executable, os.path.join(HERE, "render_cover.py"),
                    mon.isoformat(), sun.isoformat(), os.path.join(raw, "01.png")], check=True)
    for i, (key, url) in enumerate(images, start=2):
        name = f"{i:02d}.png"
        url = re.sub(r"=s\d+\?", "=s0?", url)
        subprocess.run(["curl", "-sSLf", "-o", os.path.join(raw, name), url], check=True)
        manifest.append({"n": i, "key": key, "file": name})
    mpath = os.path.join(wd, "manifest.json")
    json.dump(manifest, open(mpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "process_imgs.py"), raw, pub, mpath],
                   check=True, stdout=subprocess.DEVNULL)

    marks = os.path.join(wd, "marks.txt")
    if not os.path.exists(marks):
        lines = ["# 本期看点（3 条）：看点：标题关键词 | 一句话看点", "看点：", "看点：", "看点：", "",
                 "# 下划线：标题前缀 :: 短语 || 短语（每段 1–3 处，须是正文原文）"]
        lines += [f"{it['title'][:14]} :: " for s in sections for it in s["items"]]
        open(marks, "w", encoding="utf-8").write("\n".join(lines) + "\n")

    n_items = sum(len(s["items"]) for s in sections)
    print(f"week   {mon} – {sun}\ndir    {wd}")
    print(f"found  {len(sections)} 栏目, {n_items} 条快讯, {len(images)} 张图"
          f"（每日一图：{'有' if any(k == 'DAILY' for k, _ in images) else '无'}）")
    for s in sections:
        print(f"  # {s['zh']}（{len(s['items'])}）")
        for it in s["items"]:
            print(f"    - {it['title']}")
    for w in warnings:
        print("WARNING:", w)


def apply_marks(md_path, marks_path, out_path):
    highlights, marks = [], {}
    for line in open(marks_path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("看点："):
            if line[3:].strip():
                highlights.append(line)
            continue
        key, _, phrases = line.partition("::")
        phrases = [p.strip() for p in phrases.split("||") if p.strip()]
        if phrases:
            marks[key.strip()] = phrases
    lines = open(md_path, encoding="utf-8").read().splitlines()
    errors, used, title, n_marked = [], set(), None, 0
    for i, line in enumerate(lines):
        if line.startswith("## "):
            title = line[3:]
            continue
        if line.startswith("#") or not line.strip() or line.startswith("来源") or title is None:
            continue
        for key, phrases in marks.items():
            if title.startswith(key):
                used.add(key)
                for p in phrases:
                    if p in line and f"++{p}++" not in line:
                        lines[i] = line = line.replace(p, f"++{p}++", 1)
                        n_marked += 1
    md = "\n".join(lines)
    for key, phrases in marks.items():
        if key not in used:
            errors.append(f"marks 里的标题前缀没有匹配到任何快讯：{key}")
        for p in phrases:
            if f"++{p}++" not in md:
                errors.append(f"下划线短语在「{key}」正文里找不到：{p}")
    titles = re.findall(r"^## (.+)$", md, re.M)
    for h in highlights:
        kw = h[3:].partition("|")[0].strip()
        if not any(kw in t for t in titles):
            errors.append(f"看点关键词不在任何标题里：{kw}")
    if errors:
        sys.exit("marks.txt 有问题：\n  " + "\n  ".join(errors))
    unmarked = [t for t in titles if not any(t.startswith(k) for k in marks)]
    open(out_path, "w", encoding="utf-8").write("\n".join(highlights) + "\n\n" + md + "\n")
    return n_marked, unmarked, len(highlights)


def cmd_build(a):
    mon, sun = week_of(a.week)
    wd = week_dir(a.root, mon, sun)
    pub = os.path.join(wd, "配图", "公众号")
    marked = os.path.join(wd, "weekly.marked.md")
    n_marked, unmarked, n_hl = apply_marks(os.path.join(wd, "weekly.md"), os.path.join(wd, "marks.txt"), marked)
    mpath = os.path.join(wd, "manifest.json")
    out = os.path.join(wd, OUT_NAME + ".html")
    build = [sys.executable, os.path.join(HERE, "build_weekly.py"), marked]
    validate = [sys.executable, os.path.join(VENDOR, "validate_gzh_html.py")]
    subprocess.run(build + [out, mpath, pub, "rel", "配图/公众号/"], check=True)
    subprocess.run(validate + [out], check=True)
    tmp = os.path.join(wd, ".b64")
    os.makedirs(tmp, exist_ok=True)
    b64 = os.path.join(tmp, OUT_NAME + ".html")
    subprocess.run(build + [b64, mpath, pub, "b64"], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(validate + [b64], check=True, stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, os.path.join(VENDOR, "wrap_preview.py"), b64],
                   check=True, stdout=subprocess.DEVNULL)
    shutil.move(os.path.join(tmp, OUT_NAME + "_预览.html"), os.path.join(wd, OUT_NAME + "_预览.html"))
    shutil.rmtree(tmp)
    print(f"marks  {n_marked} 处下划线，看点 {n_hl} 条")
    for t in unmarked:
        print("WARNING: 这条快讯没有下划线标注：", t)
    print(f"done   {out}\n       {os.path.join(wd, OUT_NAME + '_预览.html')}")
    if a.folder:
        save_drive(wd, folder_id=a.folder)
    write_upload(wd, os.path.join(wd, OUT_NAME + "_预览.html"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--doc", required=True, help="Google Doc ID of this week's 周报")
    f.add_argument("--week", required=True, help="any date in the week (YYYY-MM-DD); weeks run Mon–Sun")
    f.add_argument("--root", default=ROOT_DEFAULT)
    f.add_argument("--folder", help="Drive ID of this week's folder (for the upload step)")
    b = sub.add_parser("build")
    b.add_argument("--week", required=True)
    b.add_argument("--root", default=ROOT_DEFAULT)
    b.add_argument("--folder", help="Drive ID of this week's folder, if not given at fetch")
    a = ap.parse_args()
    cmd_fetch(a) if a.cmd == "fetch" else cmd_build(a)
