#!/usr/bin/env python3
"""Offline self-test: proves this folder reproduces the approved weekly exactly.

    python3 scripts/selftest.py            # check
    python3 scripts/selftest.py --preview  # also build a preview page of the example week to look at
    python3 scripts/selftest.py --accept   # after an intended template/style change: adopt current output as standard

1. dependencies: Python 3.8+, Pillow, curl, Chrome/Chromium
2. rebuild examples/11.9.2026-11.15.2026 (doc text + marks + processed images) and compare with
   expected.html byte for byte — this is the issue the owner approved and verified in WeChat
3. WeChat compliance check (vendor/gzh-design validate_gzh_html.py)
4. re-render the cover date and the ending card and compare with the template images
   (small differences = different fonts on this machine; see docs/04-公众号与环境踩坑.md)
Exit code 0 = everything that must match matches.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import EXAMPLES, SCRIPTS, TEMPLATE, VENDOR, find_chrome  # noqa: E402

EX = os.path.join(EXAMPLES, "11.9.2026-11.15.2026")
ACCEPT = "--accept" in sys.argv   # after an intended template change: store current output as the new standard
PREVIEW = "--preview" in sys.argv  # also write a self-contained preview page of the example week
fails = []


def ok(msg):
    print("  ✅", msg)


def bad(msg):
    print("  ❌", msg)
    fails.append(msg)


def warn(msg):
    print("  ⚠️ ", msg)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


print("1. 依赖")
if sys.version_info >= (3, 8):
    ok(f"Python {sys.version.split()[0]}")
else:
    bad("需要 Python 3.8+")
try:
    import PIL
    from PIL import Image, ImageChops, ImageStat
    ok(f"Pillow {PIL.__version__}")
except ImportError:
    bad("缺 Pillow：pip install pillow")
    sys.exit(1)
ok("curl") if shutil.which("curl") else bad("缺 curl（fetch 下载文档与图片用）")
try:
    ok(f"Chrome: {find_chrome()}")
    chrome = True
except SystemExit as e:
    bad(str(e))
    chrome = False

print("2. 用示例数据完整重建，对比 expected.html")
import make_weekly  # noqa: E402

with tempfile.TemporaryDirectory() as tmp:
    marked = os.path.join(tmp, "weekly.marked.md")
    n, unmarked, n_hl = make_weekly.apply_marks(os.path.join(EX, "weekly.md"), os.path.join(EX, "marks.txt"), marked)
    ok(f"marks.txt 套用成功：{n} 处下划线，{n_hl} 条看点，未标注快讯 {len(unmarked)} 条")
    imgs = os.path.join(tmp, "配图", "公众号")
    shutil.copytree(os.path.join(EX, "配图", "公众号"), imgs)
    out = os.path.join(tmp, "out.html")
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "build_weekly.py"), marked, out,
                        os.path.join(EX, "manifest.json"), imgs, "rel", "配图/公众号/"], capture_output=True, text=True)
    if r.returncode:
        bad("build_weekly.py 失败：" + r.stderr[-400:])
    else:
        exp = os.path.join(EX, "expected.html")
        if ACCEPT:
            shutil.copy(out, exp)
            ok("--accept：已用当前输出更新 expected.html")
        if ACCEPT or PREVIEW:   # self-contained preview page of the example week, for a visual check
            pv_dir = tempfile.mkdtemp(prefix="rs-weekly-preview-")
            pv = os.path.join(pv_dir, "示例周预览.html")
            subprocess.run([sys.executable, os.path.join(SCRIPTS, "build_weekly.py"), marked, pv,
                            os.path.join(EX, "manifest.json"), imgs, "b64"], check=True, capture_output=True)
            subprocess.run([sys.executable, os.path.join(VENDOR, "wrap_preview.py"), pv], check=True, capture_output=True)
            print(f"     目视检查：用浏览器打开 {os.path.join(pv_dir, '示例周预览_预览.html')}")
        if sha(out) == sha(exp):
            ok(f"与 expected.html 完全一致（sha256 {sha(out)}）")
        else:
            bad("输出与 expected.html 不一致——脚本或模板被改动过；若是有意修改，确认效果后用新输出替换 expected.html")
        if shutil.which(sys.executable):
            v = subprocess.run([sys.executable, os.path.join(VENDOR, "validate_gzh_html.py"), out],
                               capture_output=True, text=True)
            print("3. 公众号合规校验")
            ok("validate_gzh_html：完全合规") if v.returncode == 0 and "完全合规" in v.stdout \
                else bad("validate_gzh_html 未通过：\n" + v.stdout[-600:])

    print("4. 模板图重新渲染（需 Chrome）")
    if chrome:
        cov = os.path.join(tmp, "cover.png")
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "render_cover.py"), "2026-11-09", "2026-11-15", cov],
                           capture_output=True, text=True)
        if r.returncode:
            bad("render_cover.py 失败：" + r.stderr[-300:])
        else:
            ref_path = os.path.join(EX, "cover-reference-1080.png")  # lossless reference
            if ACCEPT:
                Image.open(cov).convert("RGB").resize((1080, 470), Image.LANCZOS).save(ref_path, optimize=True)
                ok("--accept：已更新封面参考图 cover-reference-1080.png")
            ref = Image.open(ref_path).convert("RGB")
            got = Image.open(cov).convert("RGB").resize(ref.size, Image.LANCZOS)
            d = sum(ImageStat.Stat(ImageChops.difference(ref, got)).mean) / 3
            (ok if d < 1.5 else warn)(f"封面日期渲染与示例差异 {d:.2f}（<1.5 视为一致；偏大多半是本机没有苹方字体）")
        # ending card: render into a temp copy of template so the real template is untouched
        t2 = os.path.join(tmp, "tpl")
        shutil.copytree(TEMPLATE, t2)
        page = os.path.join(t2, "ending-card.html")
        raw = os.path.join(tmp, "end.png")
        subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=3", "--window-size=360,400", f"--screenshot={raw}",
                        "file://" + page], capture_output=True)
        if os.path.exists(raw):
            ref = Image.open(os.path.join(TEMPLATE, "ending-card.png")).convert("RGB")
            got = Image.open(raw).convert("RGB").crop((0, 0, ref.width, ref.height))
            d = sum(ImageStat.Stat(ImageChops.difference(ref, got)).mean) / 3
            (ok if d < 1.5 else warn)(f"结尾卡渲染与模板差异 {d:.2f}（只在修改 ending-card.html 后才需要重新出图）")
        else:
            warn("结尾卡渲染失败（不影响每周生成：周报直接使用 template/ending-card.png）")

print("\n结果：", "全部通过 ✅" if not fails else f"{len(fails)} 项失败 ❌")
sys.exit(1 if fails else 0)
