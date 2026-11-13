# 公众号排版组件库 —— 异常点 Outlier

> 本文件的唯一存放位置是 `周报整套流程/docs/theme-risksignal-outlier.md`；gzh-design 技能里的同名文件是指向这里的链接。格式遵循 gzh-design 主题库规范（设计变量 / 组件 / 骨架 / 配方 / 映射）。

> **使用说明**：本组件库为「异常点 Outlier」主题，所有组件使用**内联样式**，可直接复制粘贴到微信公众号编辑器。
>
> **设计风格**：源自 RiskSignal 品牌规范——“圆环是全球市场，跳出圆环的点是值得关注的风险信号”。墨蓝 `#0E1726` 做骨架与深色块，信号橙 `#F2501E` **只用于“点”和少量强调**（信号点、关键数字、关键词下划线），纸白 `#F6F4EF` 做卡片衬底。白底、扁平无阴影、小圆角，气质理性克制，像一份金融情报简报。信息密度中高，适合周报/快讯合集、行业动态、数据点评、风险案例分析。
>
> **品牌用色铁律**（来自 RiskSignal 标志使用规范）：
> - 信号橙不做大面积底色、**不用于正文文字**（白底对比度仅 3.5:1）；只出现在信号点、编号/关键数字、下划线、少量标签上。
> - 墨蓝深色块全文 ≤3 处（头图/刊头、结尾互动区、可选的墨蓝摘要框），其余靠纸白衬底 + 细分隔线分层。
> - 不加阴影、不加渐变。字体倾向 Inter + 思源黑体，不用衬线体和手写体。
>
> **公众号平台限制**：不用 `<style>`/`<script>`/`<div>`、class/id、`position`、`float`、`display:grid`、CSS 变量；所有文字节点包 `<span leaf="">`；字号 ≤24px；**不用空的装饰元素**：公众号粘贴时会删掉只含 `&nbsp;`、`font-size:0` 的空 span（实测信号点整体消失），圆点一律用 `●` 字符 + `color` 绘制，线条用 `border`。

---

## 设计变量速查表

```
墨蓝 Ink（标题/骨架/深色块）：      #0E1726
信号橙 Signal（点/关键数字/下划线）： #F2501E
纸白 Paper（卡片衬底）：            #F6F4EF
深色块内次级层（暗环色）：          #1C2A40
正文色：                          #1F2937
次要文字（说明/来源/英文标签）：     #5B6575
深色块上的弱化文字：                #9AA6B8
分隔线：                          #E5E2DA
占位虚线：                        #D9D5CC
背景：                            #FFFFFF
正文字号 / 行高：                  15px / 1.85，letter-spacing 0.3px，两端对齐
条目标题：                        17px / 700 / 左侧 3px 墨蓝竖条
章节标题：                        编号 24px/800 + 中文 20px/700 + 英文标签 10px
圆角：                            8px（大块/图片）、6px（条目配图）、4px（标签）
阴影：                            无
最大宽度 / 容器内边距：             677px / 8px
```

字体栈：`'Inter','Source Han Sans SC','Noto Sans SC','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif`

**正文关键词下划线**（对应 theme-index“正文下划线 CSS”列）：`border-bottom:2px solid #F2501E;font-weight:600;color:#0E1726;`

**信号点**（本主题的核心视觉符号，出现在标签行、章节编号右上、刊头）——用 `●` 字符绘制，墨迹直径约 0.76×字号（字号 10px ≈ 7.6px 点、11px ≈ 8.4px 点）：

```html
<span style="color:#F2501E;font-size:11px;line-height:1;"><span leaf="">●</span></span>
```

---

## 组件 1 全局容器

```html
<section style="max-width:677px;margin:0 auto;padding:8px;box-sizing:border-box;background:#FFFFFF;color:#1F2937;font-family:'Inter','Source Han Sans SC','Noto Sans SC','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;line-height:1.75;">

  <!-- 第一个子元素：组件 2 封面图 或 组件 3 文字刊头（二选一，不设 margin-top） -->

</section>
```

---

## 组件 2 封面图 cover-image

**用途**：作者有品牌封面横幅时用作文章开头（优先于组件 3）。全文唯一、放最前。

```html
<section style="margin:0;">
  <img src="{{封面图URL}}" alt="{{封面说明}}" style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:8px;">
</section>
```

---

## 组件 3 文字刊头 masthead（无封面图时用）

**用途**：墨蓝刊头卡，呼应 RiskSignal 公众号封面。顶部信号点 + 刊名 + 细线 + 期号；中部英文眉题 + 主标题 + 栏目串；底部三格数据条（第一格数字用信号橙，即“跳出的那个点”）。

**可替换字段**：`{{刊名}}` `{{期号或日期}}` `{{英文眉题}}` `{{主标题}}` `{{栏目串}}` `{{数字1}}/{{说明1}}` … `{{数字3}}/{{说明3}}`（数据条无内容时整段删除）

```html
<section style="background:#0E1726;border-radius:8px;padding:24px 22px 20px;">
  <section style="display:flex;align-items:center;margin-bottom:24px;padding-bottom:12px;border-bottom:1px solid #1C2A40;">
    <span style="color:#F2501E;font-size:11px;line-height:1;"><span leaf="">●</span></span>
    <span style="margin-left:8px;font-size:11px;font-weight:700;letter-spacing:3px;color:#FFFFFF;"><span leaf="">{{刊名}}</span></span>
    <span style="margin-left:auto;font-size:11px;color:#9AA6B8;letter-spacing:1px;"><span leaf="">{{期号或日期}}</span></span>
  </section>
  <p style="margin:0 0 8px;font-size:11px;font-weight:600;color:#9AA6B8;letter-spacing:2.5px;"><span leaf="">{{英文眉题}}</span></p>
  <p style="margin:0 0 12px;font-size:24px;font-weight:700;color:#FFFFFF;line-height:1.35;letter-spacing:0.5px;"><span leaf="">{{主标题}}</span></p>
  <p style="margin:0;font-size:13px;color:#9AA6B8;line-height:1.8;"><span leaf="">{{栏目串}}</span></p>
  <section style="display:flex;margin-top:22px;padding-top:16px;border-top:1px solid #1C2A40;">
    <section style="flex:1;">
      <p style="margin:0;font-size:20px;font-weight:700;color:#F2501E;line-height:1.2;"><span leaf="">{{数字1}}</span></p>
      <p style="margin:4px 0 0;font-size:11px;color:#9AA6B8;letter-spacing:1px;"><span leaf="">{{说明1}}</span></p>
    </section>
    <section style="flex:1;border-left:1px solid #1C2A40;padding-left:14px;">
      <p style="margin:0;font-size:20px;font-weight:700;color:#FFFFFF;line-height:1.2;"><span leaf="">{{数字2}}</span></p>
      <p style="margin:4px 0 0;font-size:11px;color:#9AA6B8;letter-spacing:1px;"><span leaf="">{{说明2}}</span></p>
    </section>
    <section style="flex:1;border-left:1px solid #1C2A40;padding-left:14px;">
      <p style="margin:0;font-size:20px;font-weight:700;color:#FFFFFF;line-height:1.2;"><span leaf="">{{数字3}}</span></p>
      <p style="margin:4px 0 0;font-size:11px;color:#9AA6B8;letter-spacing:1px;"><span leaf="">{{说明3}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 4 栏目标签行 label-row

**用途**：小板块的标题行（每日一图、本期看点、延伸阅读等）。信号点 + 中文 + 英文标签。也可单独作为 `###` 级小标题使用。

```html
<section style="display:flex;align-items:center;margin-bottom:12px;">
  <span style="color:#F2501E;font-size:9px;line-height:1;"><span leaf="">●</span></span>
  <span style="margin-left:8px;font-size:15px;font-weight:700;color:#0E1726;"><span leaf="">{{中文标签}}</span></span>
  <span style="margin-left:8px;font-size:10px;font-weight:600;color:#5B6575;letter-spacing:2px;"><span leaf="">{{英文标签}}</span></span>
</section>
```

---

## 组件 5 图表板块 chart-block（每日一图 / 数据图）

**用途**：独立的信息图、数据图板块：组件 4 标签行 + 图片。信息图字小，图片建议保留 PNG、宽 1600px，方便读者点开放大。

```html
<section style="margin-top:28px;">
  <!-- 组件 4 标签行：如「每日一图 DAILY CHART」 -->
  <section style="margin:0;">
    <img src="{{图URL}}" alt="{{图说明}}" style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:8px;">
  </section>
</section>
```

---

## 组件 6 本期看点卡 highlights（导读 / 目录）

**用途**：开篇导读，**精选 3 条**核心看点（不是全量目录）。橙色编号 + 一句话看点 + 所属栏目；底部可选“栏目索引药丸”列出各栏目与条数。

```html
<section style="margin-top:28px;background:#F6F4EF;border-radius:8px;padding:18px 18px 12px;">
  <!-- 组件 4 标签行：「本期看点 HIGHLIGHTS」 -->
  <section style="display:flex;align-items:flex-start;padding:12px 0;">
    <span style="flex-shrink:0;width:34px;font-size:18px;font-weight:700;color:#F2501E;line-height:1.4;"><span leaf="">01</span></span>
    <section style="flex:1;">
      <p style="margin:0;font-size:14px;font-weight:600;color:#0E1726;line-height:1.65;"><span leaf="">{{看点1}}</span></p>
      <p style="margin:2px 0 0;font-size:11px;color:#5B6575;letter-spacing:1px;"><span leaf="">{{所属栏目1}}</span></p>
    </section>
  </section>
  <section style="display:flex;align-items:flex-start;padding:12px 0;border-top:1px solid #E5E2DA;">
    <span style="flex-shrink:0;width:34px;font-size:18px;font-weight:700;color:#F2501E;line-height:1.4;"><span leaf="">02</span></span>
    <section style="flex:1;">
      <p style="margin:0;font-size:14px;font-weight:600;color:#0E1726;line-height:1.65;"><span leaf="">{{看点2}}</span></p>
      <p style="margin:2px 0 0;font-size:11px;color:#5B6575;letter-spacing:1px;"><span leaf="">{{所属栏目2}}</span></p>
    </section>
  </section>
  <section style="display:flex;align-items:flex-start;padding:12px 0;border-top:1px solid #E5E2DA;">
    <span style="flex-shrink:0;width:34px;font-size:18px;font-weight:700;color:#F2501E;line-height:1.4;"><span leaf="">03</span></span>
    <section style="flex:1;">
      <p style="margin:0;font-size:14px;font-weight:600;color:#0E1726;line-height:1.65;"><span leaf="">{{看点3}}</span></p>
      <p style="margin:2px 0 0;font-size:11px;color:#5B6575;letter-spacing:1px;"><span leaf="">{{所属栏目3}}</span></p>
    </section>
  </section>
  <!-- 可选：栏目索引药丸，每个栏目一个 -->
  <section style="margin-top:8px;padding-top:12px;border-top:1px solid #E5E2DA;">
    <span style="display:inline-block;margin:0 6px 6px 0;padding:3px 9px;background:#FFFFFF;border:1px solid #E5E2DA;border-radius:4px;font-size:12px;color:#0E1726;"><span leaf="">01 {{栏目名}} · {{条数}}</span></span>
  </section>
</section>
```

---

## 组件 7 章节标题 chapter-head

**用途**：`##` 大章节 / 周报栏目。粗编号 + 右上信号点（跳出圆环的点）+ 英文标签 + 中文标题 + 右侧条数（非合集文章可删条数）。底部 2px 墨蓝实线。

```html
<section style="margin-top:44px;margin-bottom:20px;display:flex;align-items:flex-end;border-bottom:2px solid #0E1726;padding-bottom:12px;">
  <span style="font-size:24px;font-weight:800;color:#0E1726;line-height:1;letter-spacing:-0.5px;"><span leaf="">{{编号}}</span></span>
  <span style="align-self:flex-start;margin:0 12px 0 3px;color:#F2501E;font-size:9px;line-height:1;"><span leaf="">●</span></span>
  <section style="flex:1;">
    <p style="margin:0;font-size:10px;font-weight:600;color:#5B6575;letter-spacing:2.5px;"><span leaf="">{{英文标签}}</span></p>
    <p style="margin:3px 0 0;font-size:20px;font-weight:700;color:#0E1726;line-height:1.3;"><span leaf="">{{章节标题}}</span></p>
  </section>
  <span style="font-size:12px;color:#5B6575;"><span leaf="">{{条数}} 条</span></span>
</section>
```

---

## 组件 8 快讯条目 news-item（本主题主力组件）

**用途**：一条新闻/案例/要点 = 条目标题（组件 9）+ 配图（组件 11，可选）+ 正文（组件 10）+ 来源行（组件 12）。同一章节内，第一条不加顶部分隔，其后每条加 `border-top` 细线。

```html
<!-- 章节内第一条：去掉 border-top 与 padding-top -->
<section style="margin-bottom:22px;border-top:1px solid #E5E2DA;padding-top:22px;">
  <!-- 组件 9 条目标题 -->
  <!-- 组件 11 条目配图（原文有图才放，位置在标题下、正文上） -->
  <!-- 组件 10 正文段落 ×N -->
  <!-- 组件 12 来源行（原文有来源才放） -->
</section>
```

---

## 组件 9 条目标题 item-title（也用于 `###` 子标题）

```html
<p style="margin:0 0 12px;padding-left:10px;border-left:3px solid #0E1726;font-size:17px;font-weight:700;color:#0E1726;line-height:1.5;"><span leaf="">{{条目标题}}</span></p>
```

---

## 组件 10 正文段落 + 文字强调

```html
<p style="margin:0 0 12px;font-size:15px;line-height:1.85;color:#1F2937;letter-spacing:0.3px;text-align:justify;"><span leaf="">普通文字</span><span style="border-bottom:2px solid #F2501E;font-weight:600;color:#0E1726;"><span leaf="">关键短语</span></span><span leaf="">普通文字。</span></p>
```

**文字强调变体**（插在段落内）：

- a 关键词下划线（标记层，默认，每段 1–3 处）：`<span style="border-bottom:2px solid #F2501E;font-weight:600;color:#0E1726;"><span leaf="">文字</span></span>`
- b 墨蓝加粗（`**加粗**`）：`<span style="font-weight:700;color:#0E1726;"><span leaf="">文字</span></span>`
- c 纸白高亮（`==高亮==`）：`<span style="background:#F6F4EF;color:#0E1726;padding:1px 4px;border-radius:3px;font-weight:600;"><span leaf="">文字</span></span>`
- d 信号橙数字（仅限大字号的关键数字，全文 ≤5 处，不用于整句）：`<span style="color:#F2501E;font-weight:700;"><span leaf="">+109%</span></span>`
- e 行内代码 / 术语标签：`<span style="background:#F6F4EF;border:1px solid #E5E2DA;color:#0E1726;padding:0 5px;border-radius:4px;font-size:13px;font-family:Menlo,Consolas,monospace;"><span leaf="">code</span></span>`

---

## 组件 11 配图 picture

**用途**：条目配图 / 正文插图。按自身尺寸自适应、居中，不强制铺满。图片规格见下方“图片处理规范”。

```html
<section style="margin:0 0 14px;">
  <img src="{{图URL}}" alt="{{条目标题或图说明}}" style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:6px;">
</section>
```

有图片说明（`![说明](url)` 中有说明）时，在 img 后追加：

```html
<p style="margin:8px 0 0;font-size:12px;color:#5B6575;text-align:center;line-height:1.6;"><span leaf="">{{图片说明}}</span></p>
```

---

## 组件 12 来源行 source-line

```html
<p style="margin:0;font-size:12px;color:#5B6575;line-height:1.6;"><span style="display:inline-block;margin-right:8px;padding:1px 6px;background:#F6F4EF;border-radius:3px;color:#0E1726;font-weight:600;"><span leaf="">来源</span></span><span leaf="">{{媒体名}} · {{日期}}</span></p>
```

原文为 `来源：媒体，日期` 时拆成“媒体 · 日期”。

---

## 组件 13 指标卡组 metric-cards

**用途**：一组关键数据（2–3 个）。第一个数字用信号橙，其余墨蓝——只让一个点“跳出来”。

```html
<section style="display:flex;margin:4px 0 16px;background:#F6F4EF;border-radius:8px;padding:14px 4px;">
  <section style="flex:1;padding:0 12px;">
    <p style="margin:0;font-size:22px;font-weight:700;color:#F2501E;line-height:1.2;"><span leaf="">{{数字1}}</span></p>
    <p style="margin:4px 0 0;font-size:12px;color:#5B6575;line-height:1.5;"><span leaf="">{{说明1}}</span></p>
  </section>
  <section style="flex:1;padding:0 12px;border-left:1px solid #E5E2DA;">
    <p style="margin:0;font-size:22px;font-weight:700;color:#0E1726;line-height:1.2;"><span leaf="">{{数字2}}</span></p>
    <p style="margin:4px 0 0;font-size:12px;color:#5B6575;line-height:1.5;"><span leaf="">{{说明2}}</span></p>
  </section>
  <section style="flex:1;padding:0 12px;border-left:1px solid #E5E2DA;">
    <p style="margin:0;font-size:22px;font-weight:700;color:#0E1726;line-height:1.2;"><span leaf="">{{数字3}}</span></p>
    <p style="margin:4px 0 0;font-size:12px;color:#5B6575;line-height:1.5;"><span leaf="">{{说明3}}</span></p>
  </section>
</section>
```

---

## 组件 14 观点引用卡 quote-card（`> 引用`）

```html
<section style="margin:4px 0 16px;padding:14px 16px;background:#F6F4EF;border-left:3px solid #0E1726;border-radius:0 6px 6px 0;">
  <p style="margin:0;font-size:15px;line-height:1.8;color:#0E1726;font-weight:500;"><span leaf="">{{引用内容}}</span></p>
  <p style="margin:8px 0 0;font-size:12px;color:#5B6575;"><span leaf="">—— {{出处}}</span></p>
</section>
```

（无出处时删除第二个 `<p>`。）

---

## 组件 15 口径提示卡 note-card

**用途**：“注意口径 / 不等于 / 尚未生效”这类提醒——本主题内容常见的风险提示。小标签 + 说明。

```html
<section style="margin:4px 0 16px;padding:12px 14px;background:#FFFFFF;border:1px solid #E5E2DA;border-radius:6px;">
  <p style="margin:0;font-size:13px;line-height:1.75;color:#1F2937;"><span style="display:inline-block;margin-right:8px;padding:0 6px;background:#0E1726;color:#FFFFFF;border-radius:3px;font-size:11px;font-weight:700;letter-spacing:1px;"><span leaf="">{{提示标签，如：注意口径}}</span></span><span leaf="">{{提示内容}}</span></p>
</section>
```

---

## 组件 16 要点列表 dot-list（无序 / 有序列表）

```html
<section style="margin:0 0 14px;">
  <section style="display:flex;align-items:flex-start;margin-bottom:8px;">
    <span style="flex-shrink:0;margin:11px 10px 0 2px;color:#0E1726;font-size:8px;line-height:1;"><span leaf="">●</span></span>
    <p style="flex:1;margin:0;font-size:15px;line-height:1.85;color:#1F2937;"><span leaf="">{{列表项}}</span></p>
  </section>
</section>
```

有序列表：把圆点换成编号 `<span style="flex-shrink:0;width:22px;font-size:14px;font-weight:700;color:#0E1726;line-height:1.85;"><span leaf="">1.</span></span>`。

---

## 组件 17 事件时间线 timeline

**用途**：进展/事件按时间排列（案例复盘、监管进程）。最新或最关键的一个节点用信号橙点，其余墨蓝。

```html
<section style="margin:4px 0 16px;padding-left:4px;">
  <section style="display:flex;align-items:flex-start;">
    <span style="flex-shrink:0;margin:8px 12px 0 0;color:#0E1726;font-size:12px;line-height:1;"><span leaf="">●</span></span>
    <section style="flex:1;padding-bottom:12px;border-bottom:1px solid #E5E2DA;margin-bottom:12px;">
      <p style="margin:0;font-size:12px;font-weight:700;color:#5B6575;letter-spacing:1px;"><span leaf="">{{时间1}}</span></p>
      <p style="margin:2px 0 0;font-size:14px;line-height:1.75;color:#1F2937;"><span leaf="">{{事件1}}</span></p>
    </section>
  </section>
  <section style="display:flex;align-items:flex-start;">
    <span style="flex-shrink:0;margin:8px 12px 0 0;color:#F2501E;font-size:12px;line-height:1;"><span leaf="">●</span></span>
    <section style="flex:1;">
      <p style="margin:0;font-size:12px;font-weight:700;color:#F2501E;letter-spacing:1px;"><span leaf="">{{时间2（关键节点）}}</span></p>
      <p style="margin:2px 0 0;font-size:14px;line-height:1.75;color:#1F2937;"><span leaf="">{{事件2}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 18 对照表 compare-rows（Markdown 表格）

**用途**：两三列的数据对照。用 flex 仿表格，首行墨蓝表头。

```html
<section style="margin:4px 0 16px;border:1px solid #E5E2DA;border-radius:6px;overflow:hidden;font-size:13px;">
  <section style="display:flex;background:#0E1726;color:#FFFFFF;font-weight:700;">
    <p style="flex:1;margin:0;padding:8px 10px;"><span leaf="">{{表头1}}</span></p>
    <p style="flex:1;margin:0;padding:8px 10px;"><span leaf="">{{表头2}}</span></p>
    <p style="flex:1;margin:0;padding:8px 10px;"><span leaf="">{{表头3}}</span></p>
  </section>
  <section style="display:flex;color:#1F2937;border-top:1px solid #E5E2DA;">
    <p style="flex:1;margin:0;padding:8px 10px;font-weight:600;color:#0E1726;"><span leaf="">{{行名}}</span></p>
    <p style="flex:1;margin:0;padding:8px 10px;"><span leaf="">{{值}}</span></p>
    <p style="flex:1;margin:0;padding:8px 10px;"><span leaf="">{{值}}</span></p>
  </section>
  <section style="display:flex;color:#1F2937;border-top:1px solid #E5E2DA;background:#F6F4EF;">
    <p style="flex:1;margin:0;padding:8px 10px;font-weight:600;color:#0E1726;"><span leaf="">{{行名}}</span></p>
    <p style="flex:1;margin:0;padding:8px 10px;"><span leaf="">{{值}}</span></p>
    <p style="flex:1;margin:0;padding:8px 10px;"><span leaf="">{{值}}</span></p>
  </section>
</section>
```

（行底色白 / 纸白交替。）

---

## 组件 19 分割线 divider（`---`）

```html
<p style="margin:28px 0;text-align:center;line-height:1;"><span style="color:#D9D5CC;font-size:12px;letter-spacing:6px;"><span leaf="">· · ·</span></span><span style="color:#F2501E;font-size:9px;margin:0 8px;"><span leaf="">●</span></span><span style="color:#D9D5CC;font-size:12px;letter-spacing:6px;"><span leaf="">· · ·</span></span></p>
```

---

## 组件 20 墨蓝摘要框 dark-summary（锚点层，全文 ≤1 处）

**用途**：观点/分析类文章的结论收束，或“本期一句话”。

```html
<section style="margin:28px 0 8px;background:#0E1726;border-radius:8px;padding:20px 20px 18px;">
  <section style="display:flex;align-items:center;margin-bottom:10px;">
    <span style="color:#F2501E;font-size:9px;line-height:1;"><span leaf="">●</span></span>
    <span style="margin-left:8px;font-size:10px;font-weight:700;letter-spacing:2.5px;color:#9AA6B8;"><span leaf="">{{英文标签，如：TAKEAWAY}}</span></span>
  </section>
  <p style="margin:0;font-size:16px;font-weight:600;line-height:1.75;color:#FFFFFF;"><span leaf="">{{结论/金句}}</span></p>
</section>
```

---

## 组件 21 结尾互动区 ending（本主题的签名/CTA 区，全文唯一）

**Logo 规则**（RiskSignal 标志使用规范）：墨蓝底上用**反白横版**（白色圆环与字标 + 橙色信号点）；屏幕显示宽度 ≥120px（此处 150px）；四周留出 ≥1 个信号点直径的空白（块内边距 22px、logo 下方 16px，均大于显示尺寸下约 8px 的点径）；不拉伸、不旋转、不改色、不加阴影或描边。logo 文件用 `周报整套流程/template/logo-reversed.png`（已裁切并铺墨蓝底，450×100，3 倍图）。公众号正文不支持 SVG，只用 PNG。

```html
<section style="margin-top:48px;background:#0E1726;border-radius:8px;padding:22px 22px 20px;">
  <section style="margin:0 0 16px;">
    <img src="{{logo-reversed.png 的 URL}}" alt="RiskSignal" style="width:150px;max-width:100%;height:auto;display:block;">
  </section>
  <p style="margin:0 0 12px;font-size:16px;font-weight:600;color:#FFFFFF;line-height:1.75;"><span leaf="">如果你觉得这期内容有收获，欢迎</span><span style="color:#F2501E;font-weight:700;"><span leaf="">点赞、关注、收藏、转发</span></span><span leaf="">，我们下期见。</span></p>
  <p style="margin:0;font-size:13px;color:#9AA6B8;line-height:1.8;"><span leaf="">{{联系方式 / 署名，原文有则沿用}}</span></p>
</section>
```

**RiskSignal 周报固定做法：整块直接插图片** `周报整套流程/template/ending-card.png`（1080px 宽，按手机版面 360px ×3 预渲染，logo、文案断行、底色都固定，不受公众号改色和换行影响）。改文案时编辑 `template/ending-card.html`（及 `ending-card-alt.txt`），运行 `python3 scripts/render_ending_card.py` 重新出图。插入写法：

```html
<section style="margin-top:48px;">
  <img src="{{ending-card.png 的 URL}}" alt="RiskSignal：如果你觉得这期周报有收获，欢迎点赞、关注、收藏、转发，我们下周见。如有合作意向或建议，欢迎联系：……" style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:8px;">
</section>
```

下面的 HTML 版本仅用于非 RiskSignal 品牌的文章或需要临时改文案时。原文末尾已有联系/署名段时并入第二个 `<p>`，不另起签名区；周报可把“下期见”改为“下周见”。没有 logo 图片可用时，用“信号点 + `RISKSIGNAL` 字样”的文字标签代替（同组件 4 结构，白字），不要用文字或 CSS 拼凑仿制 logo。

---

## 组件 22 声明区 notice（版权 / 免责 / AI 配图说明）

```html
<section style="margin-top:14px;background:#F6F4EF;border-radius:8px;padding:16px 18px;">
  <p style="margin:0 0 8px;font-size:10px;font-weight:600;color:#5B6575;letter-spacing:2.5px;"><span leaf="">NOTICE · 声明</span></p>
  <p style="margin:0;font-size:12px;color:#5B6575;line-height:1.8;text-align:justify;"><span leaf="">{{声明段落1}}</span></p>
  <p style="margin:8px 0 0;font-size:12px;color:#5B6575;line-height:1.8;text-align:justify;"><span leaf="">{{声明段落2}}</span></p>
</section>
```

---

## 组件 23 待补素材占位 placeholder

原文图片暂缺时使用（虚线仅用于“待补”语义）：

```html
<section style="padding:34px 20px;border:1.5px dashed #D9D5CC;border-radius:8px;background:#F6F4EF;text-align:center;">
  <p style="margin:0 0 10px;font-size:24px;line-height:1;"><span leaf="">🖼</span></p>
  <p style="margin:0;font-size:14px;font-weight:700;color:#5B6575;letter-spacing:1px;"><span leaf="">待补素材</span></p>
  <p style="margin:8px 0 0;font-size:13px;color:#9AA6B8;line-height:1.7;"><span leaf="">此处插入：{{素材说明}}</span></p>
</section>
```

---

## 多行代码块 → 用通用增量库

本主题不设专属代码块；用 gzh-design 通用库 `common-components.md` 的 1a 深色代码块（底色换墨蓝 `#0E1726`）或 1b 浅色代码块（底色换纸白 `#F6F4EF`），左竖条用墨蓝。

---

## 图片处理规范（公众号）

| 类型 | 格式 | 宽度 | 体积目标 |
|---|---|---|---|
| 条目配图 / 插画 / 照片 | JPEG（渐进式，去元数据，RGB） | 1080px（手机实际显示宽度） | ≤400KB；RiskSignal 周报按总预算约 ≤140KB（成品需能上传 Drive，见周报整套流程 docs/01 §7） |
| 封面横幅 | JPEG | 1080px | ≤200KB |
| 信息图 / 数据图（字小） | PNG（透明底铺白） | 1600px（读者可点开放大） | ≤1MB |

- 公众号单图上限 10MB，但大图会被二次压缩，按上表先处理好画质更可控。
- 透明 PNG 一律铺白底，避免深色模式下出现黑底。
- 本地预览页把图片内嵌为 base64，点「复制到公众号」后粘贴进编辑器，图片会随正文一起保留（2026-11 实测通过）。若个别图片未显示，按编号到编辑器里补插。

---

## 完整文章模板骨架

```html
<section style="（组件 1 全局容器样式）">

  <!-- 1. 开头：组件 2 封面图（有品牌封面时，优先）或 组件 3 文字刊头（二选一，全文唯一） -->

  <!-- 2. 组件 5 图表板块（可选：原文开头有“每日一图”/核心数据图时） -->

  <!-- 3. 组件 6 本期看点卡（导读：精选 3 条；合集类加栏目索引药丸） -->

  <!-- 4. 第一章：组件 7 章节标题（编号 01） -->
  <!--    章内：合集/快讯类 → 组件 8 快讯条目 ×N（= 组件 9 标题 + 组件 11 配图 + 组件 10 正文 + 组件 12 来源） -->
  <!--          普通长文 → 组件 9 小标题 / 组件 10 正文 / 组件 13 指标卡 / 组件 14 引用 / 组件 15 口径提示 / 组件 16 列表 / 组件 17 时间线 / 组件 18 对照表 -->

  <!-- 5. 第二章…第 N 章（同上，编号递增） -->

  <!-- 6. 组件 20 墨蓝摘要框（可选，观点/分析类结论收束，全文 ≤1 处） -->

  <!-- 7. 组件 21 结尾互动区（全文唯一） -->

  <!-- 8. 组件 22 声明区（原文有版权/免责/AI 配图声明时） -->

</section>
```

**骨架铁律**：
- 开头只用组件 2 或组件 3 之一；有作者封面图时用封面图，不再叠加文字刊头。
- 墨蓝深色块（组件 3/20/21）全文合计 ≤3 处。
- 信号橙只出现在：信号点、看点编号、章节编号旁的点、下划线、指标卡第一个数字、结尾“点赞、关注、收藏、转发”。不要给整句正文或大面积底色上橙色。
- 条目配图位置固定为“标题下、正文上”。

---

## 视觉层级（3 层递进）

| 层级 | 样式 | 用途 | 频率 |
|------|------|------|------|
| **锚点层** | 封面/刊头、墨蓝摘要框、结尾互动区、看点橙色编号 | 开篇与收束、导读 | 全文 ≤5 处 |
| **标记层** | 信号橙下划线（文字强调 a） | 正文关键短语（数字、结论、专有名词） | 每段 1–3 处 |
| **容器层** | 纸白衬底卡（看点、指标、引用、声明）、条目左竖条标题、来源标签 | 结构与信息分组 | 按需 |

---

## 文章类型 → 组件组合配方

| 文章类型 | 核心组件组合 | 点缀组件 |
|---|---|---|
| 周报 / 快讯合集（默认） | 封面图2（或刊头3）+ 本期看点6 + 章节标题7 + 快讯条目8（9+11+10+12）+ 结尾互动21 + 声明22 | 图表板块5（每日一图）、口径提示15 |
| 数据复盘 / 报告 | 刊头3（含数据条）+ 章节标题7 + 指标卡13 + 对照表18 + 图表板块5 + 墨蓝摘要框20 | 口径提示15、时间线17 |
| 风险案例分析 | 封面图2 + 章节标题7 + 条目标题9 + 正文10 + 时间线17 + 口径提示15 + 墨蓝摘要框20 | 指标卡13、引用14 |
| 观点 / 深度分析 | 刊头3 + 章节标题7 + 正文10 + 引用14 + 墨蓝摘要框20 | 指标卡13、分割线19 |
| 政策解读 | 刊头3 + 章节标题7 + 要点列表16 + 口径提示15 + 时间线17 | 对照表18、来源行12 |
| 教程 / 方法 | 刊头3 + 章节标题7 + 条目标题9 + 正文10 + 要点列表16 + 通用库代码块 | 口径提示15 |

所有类型共用：结尾互动区 21（唯一）。

---

## Markdown → 异常点 Outlier 映射规则

| Markdown 元素 | 对应组件 | 说明 |
|---|---|---|
| 文首封面图 | 组件 2 封面图 | 没有封面时用组件 3 刊头 |
| `# 标题`（文章标题） | 组件 3 刊头主标题 | 有封面图时标题在封面里，不重复 |
| `# 栏目`（周报一级栏目） | 组件 7 章节标题 | 编号 01/02…，自动生成英文标签与条数 |
| `## 章节标题` | 组件 7（普通长文）/ 组件 9（周报里的单条新闻标题） | 周报：`##` = 一条快讯 |
| `### 子标题` | 组件 9 条目标题 或 组件 4 标签行 | |
| 普通段落 | 组件 10 | 每段 1–3 处信号橙下划线 |
| `**加粗**` / `==高亮==` | 文字强调 b / c | |
| `<u>文字</u>` / `++文字++` | 文字强调 a | |
| 行内 `` `code` `` | 文字强调 e | |
| `来源：媒体，日期` | 组件 12 来源行 | 拆成“媒体 · 日期” |
| `![说明](图)` / `![](图)` | 组件 11 配图（有说明才加说明行） | 条目图放标题下 |
| 文首“每日一图”等独立大图 | 组件 5 图表板块 | |
| 无序 / 有序列表 | 组件 16 | |
| 表格 | 组件 18 对照表 | flex 仿表格，不用 table/grid |
| `> 引用` | 组件 14 引用卡（观点）/ 组件 15 口径提示（提醒、限制条件） | |
| `---` | 组件 19 分割线 | |
| 文末结论 | 组件 20 墨蓝摘要框 | ≤1 处 |
| 文末联系/署名 | 并入组件 21 结尾互动区 | |
| 文末版权/免责/AI 配图说明 | 组件 22 声明区 | |
