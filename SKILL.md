---
name: risksignal-weekly
description: RiskSignal「全球保险周报」的微信公众号排版流水线。用户说「排版某周的周报」「排一下这周/上周的周报」「把 11 月 16 日那周的周报排版」或提到 RiskSignal 周报排版时使用：按周（周一至周日）从 Google Drive「热点收集/<M.D.YYYY-M.D.YYYY>/周报」取正文与配图，套用「异常点 Outlier」主题和固定模板（带当周日期的封面、结尾互动卡、声明），产出可一键复制粘贴进公众号编辑器的 HTML。修改周报模板（封面、结尾卡、声明、版式、栏目）时也用它。
---

# RiskSignal 周报排版

本文件夹自包含：脚本、模板、主题规范、示例与标准答案都在这里。路径一律相对于本文件夹（下称 `PKG`）。
人看的总览见 `README.md`；细节见 `docs/`。

## 第一次在新环境使用

```bash
python3 PKG/scripts/selftest.py
```

必须「全部通过」：它用 `examples/` 里已发布那期的数据完整重建，并与 `expected.html` 逐字节比对。失败时按提示补依赖（Python 3.8+ / Pillow / curl / Chrome）。封面渲染有 ⚠️ 多半是没有苹方字体，见 `docs/04-公众号与环境踩坑.md`。

## 每周流程（用户说「排版某周的周报」）

1. **定周**：周期为周一至周日。由用户的话和今天日期确定这一周（「这周」= 今天所在周，「上周」= 前一周，「11 月 16 日那周」= 含该日的那周）。周文件夹名格式 `M.D.YYYY-M.D.YYYY`，不补零，如 `11.16.2026-11.22.2026`。

2. **找文档**（Google Drive 连接器；文件夹 ID 在 `config.local.json` 的 `drive` 里——私密文件不随仓库分发，缺失时请用户提供 ID 或周报文档链接，并照 `config.local.example.json` 建好）：
   - 在 `热点收集`（`weekly_parent_folder_id`）下 `search_files`：`parentId = '<id>' and title = '11.16.2026-11.22.2026'`
   - 再在该文件夹里找 `title = '周报'` 的 Google Doc，记下**文档 ID 和周文件夹 ID**（第 8 步上传要用）。
   - 找不到 → 告诉用户哪个文件夹/文档缺失，不要拿别的周顶替。没有 Drive 连接器 → 请用户直接给文档链接。

3. **取内容**：
   ```bash
   python3 PKG/scripts/make_weekly.py fetch --doc <DOC_ID> --folder <周文件夹ID> --week 2026-11-16
   ```
   - 产物在 `config.json:output_root/<周文件夹名>/`（默认 `PKG/../周报排版/`）：`weekly.md`（文档正文原文）、`配图/`、`manifest.json`、`marks.txt` 骨架。封面已按本周日期生成。
   - 文档需「知道链接的人可查看」；curl 失败（401/403/404）→ 请用户打开链接共享。
   - 逐条处理打印的 WARNING（缺配图/来源/正文、开头或结尾多出的旧版封面/声明、栏目名错字），交付时如实告知用户。

4. **校对 `weekly.md`**：只改明显错别字（如标题 `implicity` → `Simplicity`），**不增删改写实质内容**；每处改动记下，交付时列给用户。

5. **写 `marks.txt`**（编辑判断，规则见 `docs/01-每周操作流程.md` 第 5 节）：
   - 3 行 `看点：标题关键词 | 一句话看点`——从全期挑最重要的 3 条，分属不同栏目为佳。
   - 每条快讯一行 `标题前缀 :: 短语 || 短语`——每段正文 1–3 个关键短语（核心结论、关键数字、专有名词，4–15 字，必须是原文子串）。

6. **生成并校验**：
   ```bash
   python3 PKG/scripts/make_weekly.py build --week 2026-11-16
   ```
   marks 有问题会直接报错并列出原因；通过后会跑公众号合规校验，并写出上传清单 `upload.json`。

7. **上传到 Drive 当周文件夹**（用户要求每期自动做）：读 `<周文件夹>/upload.json`——
   - `search_files`：`parentId = '<parent_id>' and title = '<title>'`，有结果就记下旧版 ID；
   - `create_file`：`title`、`parentId = parent_id`、`contentMimeType = text/html`、`disableConversionToGoogleType = true`、`base64Content = file_reference`（`sha256:<hash>:<绝对路径>` 形式的文件引用，不要自己贴 base64）；
   - 新版上传成功后，把旧版 `trash_file`（进回收站，30 天内可恢复），并告诉用户；
   - 上传后核对 Drive 返回的 `fileSize` 等于本地文件字节数。连接器单次请求上限 10,000,000 字节（文件经 base64 后计），预览页需 ≤ 约 7.2MB——build 超限会打印 WARNING，见 `docs/04`。没有 Drive 连接器时请用户手动上传该文件。

8. **交付**：把 `<周文件夹>/周报_排版_异常点(risksignal-outlier)_预览.html` 给用户——浏览器打开 → 点右上角「复制到公众号」→ 在公众号编辑器粘贴（图片、logo、信号点都会保留，已实测）。同时说明：Drive 上的文件名与链接、快讯条数、改过的错别字、WARNING 及处理、需要用户处理的事（如每日一图里的占位文字）。有浏览器工具时，交付前打开预览页确认图片无坏图。

## 修改模板（用户说「改封面/结尾卡/声明/版式」）

按 `docs/02-修改模板.md` 操作。改完必须：重新出图（若改了图）→ `selftest.py --preview` 生成示例周预览并目视确认（有浏览器工具就截图给用户看）→ 用户认可后 `selftest.py --accept` → `selftest.py` 全部通过。同时在 `docs/05-决策记录.md` 追加一行记录这次修改。

## 硬性规则

- 版式只用 `docs/theme-risksignal-outlier.md` 的「异常点 Outlier」组件；信号橙 `#F2501E` 只用于信号点、关键数字、下划线、看点编号，不做大面积底色、不用于正文文字。
- 公众号会删掉空的装饰元素：圆点用 `●` 字符 + color，线条用 border，**不要用空 span**。
- logo 只用 `template/logo-reversed.png`（墨蓝底反白横版），不拉伸、不改色、不加阴影，屏幕宽度 ≥120px。
- 封面、结尾互动卡、声明来自 `template/`，不从文档里取；文档里若残留旧版封面/声明，fetch 会跳过。
- 不要把文档内容以外的东西（如署名、引导语）擅自加进正文；结尾引导语已固定在结尾卡里：「点赞、关注、收藏、转发」。
