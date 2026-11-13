"""Process downloaded images to WeChat specs: flatten transparency on white, item images -> 1080px JPEG,
每日一图 (infographic) -> 1600px PNG, strip metadata.

Size budget: the delivered preview page embeds every image as base64 (+33%) and must stay under the
Drive connector limit (request ≤ 10,000,000 bytes after base64 → preview file ≤ ~7.2 MB), so all JPEGs share TOTAL_BUDGET_KB (reserve for the infographic PNG and the
ending card): per-image cap = min(MAX_KB, (TOTAL_BUDGET_KB - RESERVE_KB) / number of JPEGs).

usage: process_imgs.py <src_dir> <out_dir> <manifest.json>
"""
import json, os, sys
from PIL import Image
src_dir, out_dir, manifest = sys.argv[1:4]
os.makedirs(out_dir, exist_ok=True)
items = json.load(open(manifest, encoding="utf-8"))
MAX_KB = 400            # never larger than this per image
TOTAL_BUDGET_KB = 5400  # all images together -> preview ≈ 6.8 MB (Drive connector: request ≤ 10,000,000 bytes after base64, so file ≤ ~7.2 MB)
RESERVE_KB = 700        # 每日一图 PNG (~550 KB) + ending card (~85 KB)
n_jpg = sum(1 for it in items if it["key"] != "DAILY") or 1
CAP_KB = min(MAX_KB, (TOTAL_BUDGET_KB - RESERVE_KB) // n_jpg)
for it in items:
    im = Image.open(os.path.join(src_dir, it["file"]))
    im.load()
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    infographic = it["key"] == "DAILY"
    target_w = 1600 if infographic else 1080
    if im.width > target_w:
        im = im.resize((target_w, round(im.height * target_w / im.width)), Image.LANCZOS)
    stem = f'{it["n"]:02d}'
    if infographic:
        name = stem + ".png"
        path = os.path.join(out_dir, name)
        im.save(path, "PNG", optimize=True)
    else:
        name = stem + ".jpg"
        path = os.path.join(out_dir, name)
        for q in (88, 84, 82, 80, 78, 76, 74, 72, 70, 66, 62):
            im.save(path, "JPEG", quality=q, optimize=True, progressive=True, subsampling=0 if q >= 84 else 2)
            if os.path.getsize(path) <= CAP_KB * 1024:
                break
        it["q"] = q
    it.update(out=name, w=im.width, h=im.height, kb=round(os.path.getsize(path) / 1024))
json.dump(items, open(manifest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for it in items:
    print(f'{it["out"]:8} {it["w"]}x{it["h"]:<5} {it["kb"]:>4}KB  {it["key"][:22]}')
qs = [i["q"] for i in items if "q" in i]
print("total", sum(i["kb"] for i in items), "KB; max", max(i["kb"] for i in items), f"KB; cap {CAP_KB} KB/jpg;",
      f"JPEG quality {min(qs)}–{max(qs)}" if qs else "")
