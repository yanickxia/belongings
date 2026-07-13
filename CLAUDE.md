# CLAUDE.md — belongings 物品记录站维护指南

基于 Hugo 的静态站,记录「拥有过 / 仍在用」的物品。每件物品一个 Markdown 文件,自动生成首页卡片、分类页与时间线。GitHub Actions 自动构建并部署到 GitHub Pages。

- 线上地址:https://belongings.pages.yanick.site/
- 仓库:https://github.com/yanickxia/belongings
- 本地路径:`/data/userdata/codes/belongings`

---

## 一、如何添加一件物品

### 1. 创建 Markdown 文件

路径:`content/items/<英文-slug>.md`(slug 用小写英文 + 连字符,如 `shure-srh840.md`)。

Front matter 模板:

```yaml
---
title: "舒尔 Shure SRH840"   # 显示名称,中英皆可
date: 2026-07-13             # 记录日期,填当天即可
draft: false                # 必须 false 才会发布
category: "电子产品"          # 分类:电子产品 / 机械键盘 / 生活用品 …
acquired: "2021"            # 入手年份,字符串,留空则归入「未知年份」
lost: ""                    # 空 = 仍拥有;填年份 = 已失去
disposal: ""               # 去向,如「闲鱼出售 ¥360」;仍拥有留空
source: "自购"              # 来源:自购 / 闲鱼二手 / 京东 / 天猫 / 老婆送的 …
price: 0                    # 购入价格(数字,无货币符号);未知填 0
image: "/images/shure-srh840.webp"   # 首页缩略图(生成的示意图),必须 .webp
photos:                    # 可选:实拍图列表,详情页展示在示意图之后
  - "/images/real-shure-srh840.webp"
switch: "Cherry 青轴"       # 可选(键盘专用):轴体
mode: "三模"                # 可选(键盘专用):连接方式,如 有线 / 三模 / 有线 + 2.4G
lighting: "下灯位"          # 可选(键盘专用):灯位
---

一段简短的中文故事,写入手经过、手感、状态等。仍在服役但有损坏的,直接在正文说明。
```

字段规则:
- `acquired` / `lost` 一律用**带引号的字符串年份**(如 `"2022"`),避免时间线分组出错。
- `lost` 为空即「仍拥有」,填年份即「已失去」,同时补 `disposal` 说明去向。
- `image` 是首页/卡片用的**生成示意图**;`photos` 是可选的**实拍图**,只在详情页显示并标注「实拍」。
- `switch` / `mode` / `lighting` 仅键盘需要,其他物品可省略。

### 2. 准备图片

- **首页示意图**:用 AI 生成产品图(白底、微俯视、棚拍风格),命名与 slug 对应,如 `rk987.webp`。
- **实拍图**:命名加 `real-` 前缀,如 `real-shure-srh840.webp`。
- 所有图片放 `static/images/`,**必须转成 WebP**(见第二节)。

### 3. 本地构建

```bash
export PATH="$HOME/bin:$PATH"
cd /data/userdata/codes/belongings
hugo --gc --minify        # 成功后 public/ 更新,Pages 数应增加
```

### 4. 提交并部署

```bash
git add -A
git commit -m "添加 <物品名>"
git push origin main
```

推送后 GitHub Actions 自动构建部署。可轮询 Actions 状态直到 `completed success`。

---

## 二、图片必须转 WebP(重要)

原始 PNG/JPG 通常 ~1MB 一张,几十张就几十 MB,拖慢仓库和加载。**所有图片入库前一律转 WebP**,体积可压到原来的 ~2%,肉眼无损。

- 生成/示意图不要用 SVG:这些是照片,矢量化会糊成色块,且不省空间。WebP 才是正解。

转换脚本(生成图边长压到 800、实拍图 1100,转 WebP 后删原图):

```python
# scripts/to_webp.py  —  用法: python3 scripts/to_webp.py
import glob, os
from PIL import Image

IMG_DIR = "static/images"
for p in glob.glob(os.path.join(IMG_DIR, "*")):
    ext = os.path.splitext(p)[1].lower()
    if ext not in (".png", ".jpg", ".jpeg"):
        continue
    name = os.path.basename(p)
    im = Image.open(p).convert("RGB")
    max_edge = 1100 if name.startswith("real-") else 800
    q = 80 if name.startswith("real-") else 82
    w, h = im.size
    s = min(1.0, max_edge / max(w, h))
    if s < 1.0:
        im = im.resize((int(w * s), int(h * s)), Image.LANCZOS)
    out = os.path.splitext(p)[0] + ".webp"
    im.save(out, "WEBP", quality=q, method=6)
    os.remove(p)
    print(f"{name} -> {os.path.basename(out)}")
```

依赖:`pip install --user --break-system-packages pillow`(Pillow 需带 WebP 支持)。

转换后记得把 front matter 里的 `image` / `photos` 后缀改成 `.webp`。

---

## 三、目录速览

| 路径 | 说明 |
|---|---|
| `content/items/*.md` | 每件物品一个文件 |
| `static/images/*.webp` | 所有图片(仅 WebP) |
| `layouts/items/single.html` | 物品详情页(含图库、轴体/连接/灯位表) |
| `layouts/index.html` | 首页卡片网格 + 统计 |
| `layouts/_default/{list,categories,timeline}.html` | 分类页 / 时间线 |
| `assets/css/style.css` | 样式 |
| `hugo.yaml` | 站点配置 |

图片路径解析统一用 `{{ strings.TrimPrefix "/" . | relURL }}`,新增模板引用图片时沿用此写法。
