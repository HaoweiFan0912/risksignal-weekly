"""Shared paths and config for the RiskSignal weekly pipeline. Everything is resolved relative to the
package folder (周报整套流程/), so the folder can be moved or handed to another machine as-is."""
import json
import os
import shutil

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(PKG, "scripts")
TEMPLATE = os.path.join(PKG, "template")
VENDOR = os.path.join(PKG, "vendor", "gzh-design", "scripts")
EXAMPLES = os.path.join(PKG, "examples")

CONFIG = json.load(open(os.path.join(PKG, "config.json"), encoding="utf-8"))
_LOCAL = os.path.join(PKG, "config.local.json")   # private overrides (Drive ids), not committed
if os.path.exists(_LOCAL):
    for _k, _v in json.load(open(_LOCAL, encoding="utf-8")).items():
        if isinstance(_v, dict) and isinstance(CONFIG.get(_k), dict):
            CONFIG[_k].update(_v)
        elif not _k.startswith("_"):
            CONFIG[_k] = _v


def pkg_path(p):
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(PKG, p))


OUTPUT_ROOT = pkg_path(CONFIG["output_root"])
OUTPUT_NAME = CONFIG["output_name"]


def find_chrome():
    for c in CONFIG["chrome_candidates"]:
        hit = c if os.path.isfile(c) else shutil.which(c)
        if hit:
            return hit
    raise SystemExit("找不到 Chrome/Chromium（封面日期与结尾卡渲染需要）。安装 Chrome，或在 config.json 的 "
                     "chrome_candidates 里加上可执行文件路径。")
