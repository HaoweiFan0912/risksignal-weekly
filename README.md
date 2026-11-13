# 周报整套流程 —— RiskSignal 全球保险周报 · 公众号排版

把每周写在 Google Doc 里的周报正文，排成可以一键复制进微信公众号编辑器的成品：带当周日期的品牌封面 → 每日一图 → 本期看点 → 六个栏目的快讯（标题 / 配图 / 正文 / 来源）→ 结尾互动卡 → 声明。版式主题为「异常点 Outlier」（RiskSignal 品牌：墨蓝 + 信号橙）。

**这个文件夹是自包含的**：交给另一个 AI 或换一台电脑，按 `SKILL.md` 就能完整复刻。AI 读 `SKILL.md`；人读本文件。

---

## 从 GitHub 获取与首次配置

```bash
git clone https://github.com/HaoweiFan0912/risksignal-weekly.git 周报整套流程
cd 周报整套流程
pip install pillow                                  # 另需 curl 与 Google Chrome
cp config.local.example.json config.local.json      # 填入 Drive 文件夹 ID（私密，不提交）
python3 scripts/selftest.py                         # 必须全部通过
```

- 作为 Claude Code 技能使用：把文件夹放到（或链接到）`~/.claude/skills/risksignal-weekly`，`SKILL.md` 会被自动识别。
- 默认输出到本文件夹的上一级 `周报排版/`，可在 `config.json` 的 `output_root` 修改。
- `config.local.json` 缺失时流程仍可运行，只是 AI 需要用户直接提供周报文档链接与周文件夹 ID。

## 快速开始

```bash
# 0) 新环境先自检（必须全部通过）
python3 scripts/selftest.py

# 1) 取当周文档的正文与配图（文档 ID 从 Drive 找，见下）
python3 scripts/make_weekly.py fetch --doc <DOC_ID> --folder <周文件夹ID> --week 2026-11-16

# 2) 编辑 周报排版/<周>/marks.txt：3 条看点 + 每段关键词下划线

# 3) 生成 + 校验（同时写出上传清单 upload.json）
python3 scripts/make_weekly.py build --week 2026-11-16

# 4) AI 用 Drive 连接器把 _预览.html 上传到当周文件夹（见 docs/01 §7）
```

成品：`周报排版/11.16.2026-11.22.2026/周报_排版_异常点(risksignal-outlier)_预览.html` → 浏览器打开 → 右上角「复制到公众号」→ 公众号编辑器粘贴。
同一文件会上传到 Drive 当周文件夹，名为 `周报_公众号排版_11.16.2026-11.22.2026.html`（Drive 里点开只显示源代码，下载后用浏览器打开）。

对 AI 只需说：**「排版 11 月 16 日那周的周报」**。

## 需要的环境

| 依赖 | 用途 |
|---|---|
| Python 3.8+ 与 Pillow（`pip install pillow`） | 全部脚本、图片处理 |
| curl | 下载文档正文与配图 |
| Google Chrome / Chromium | 渲染封面日期、结尾卡（无界面模式） |
| 苹方字体（macOS 自带） | 封面日期字体；其他系统见 `docs/04` |
| Google Drive 访问（AI 用 Drive 连接器） | 按周找到文档；没有连接器时把文档链接直接给 AI |

Drive 中的周报文档须开启「知道链接的人可查看」。

## 文件夹结构

```
周报整套流程/
├── SKILL.md                 AI 入口：触发条件 + 每周步骤 + 硬性规则
├── README.md                本文件
├── config.json              输出位置、上传文件名、Chrome 路径、栏目英文标签、栏目错字更正
├── config.local.json        私密：Drive 文件夹 ID（不提交；照 config.local.example.json 新建）
├── scripts/
│   ├── make_weekly.py       主流程：fetch（取文档/配图/生成封面/处理图片）、build（套标注/生成/校验/预览页）
│   ├── build_weekly.py      源文本 + 图片清单 → 公众号 HTML（全部组件样式在这里）
│   ├── process_imgs.py      图片按公众号规范处理
│   ├── render_cover.py      无日期封面 + 当周日期 → 封面图
│   ├── render_ending_card.py  ending-card.html → ending-card.png
│   ├── selftest.py          自检：依赖 + 示例周逐字节重建 + 合规校验 + 模板图渲染
│   └── common.py            路径与配置
├── template/                主内容之外的固定部分（改模板就改这里）
│   ├── cover-base.png       无日期封面（1902×827）
│   ├── ending-card.html/.png  结尾互动卡（logo + 点赞、关注、收藏、转发 + 联系方式）及其成图
│   ├── ending-card-alt.txt  结尾卡的替代文字
│   ├── logo-reversed.png    反白横版 logo（结尾卡用）
│   └── notice.txt           三段声明，每行一段
├── docs/
│   ├── 01-每周操作流程.md     详细步骤、marks 写法、交付话术
│   ├── 02-修改模板.md        每个模板部件怎么改、改完怎么验证
│   ├── 03-设计规范.md        品牌色、logo 规则、版式结构、图片规格
│   ├── 04-公众号与环境踩坑.md  已实测的坑与对策
│   ├── 05-决策记录.md        用户确认过的每项决定及原因
│   └── theme-risksignal-outlier.md  完整组件库（gzh-design 主题格式）
├── examples/11.9.2026-11.15.2026/   已发布的一期：原文、标注、图片、标准答案 expected.html
└── vendor/gzh-design/       合规校验与预览页脚本（AGPL-3.0，见其 LICENSE）
```

## 怎么改

| 想改 | 改哪里 | 详见 |
|---|---|---|
| 声明文字 | `template/notice.txt` | docs/02 §1 |
| 结尾卡文案 / 联系方式 | `template/ending-card.html` + `ending-card-alt.txt`，再运行 `render_ending_card.py` | docs/02 §2 |
| 封面标题、栏目串、图形 | 换 `template/cover-base.png`，按需改 `render_cover.py` 的日期坐标 | docs/02 §3 |
| 封面日期格式 / 字号 | `scripts/render_cover.py` | docs/02 §3 |
| 新栏目 / 英文标签 | `config.json` 的 `section_en` | docs/02 §4 |
| 颜色、字号、组件样式 | `scripts/build_weekly.py` + `docs/theme-risksignal-outlier.md` | docs/02 §5 |
| Drive 位置 | `config.local.json`（私密） | docs/02 §6 |
| 输出位置 | `config.json` 的 `output_root` | docs/02 §6 |

**改完任何东西**：用示例周重建看效果 → 满意后用新输出替换 `examples/…/expected.html` → `selftest.py` 全部通过。

最省事：直接对 AI 说要改什么（「声明第二段改成……」「结尾卡加个二维码」）。
