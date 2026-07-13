# 我曾拥有的物品 · belongings

用 Hugo 静态博客记录**曾经拥有过的每一件物品**及其故事，通过 GitHub Actions 自动构建并部署到 GitHub Pages。

在线地址：https://yanickxia.github.io/belongings/

## 如何添加一件物品

```bash
# 方式一：用 Hugo 命令生成（推荐，自动套用模板）
hugo new items/my-thing.md

# 方式二：直接在 content/items/ 下新建 .md 文件
```

每个物品文件的 front matter 字段：

| 字段 | 含义 | 示例 |
|------|------|------|
| `title` | 物品名称 | iPhone 12 |
| `category` | 分类 | 电子产品 / 家具 / 服饰 / 书籍 / 其他 |
| `acquired` | 拥有起始日期 | 2021-01-15 |
| `lost` | 失去日期（留空=仍拥有） | 2023-06-20 |
| `disposal` | 去向 | 卖出 / 送人 / 丢弃 / 损坏 / 丢失 |
| `source` | 来源 | 自购 / 礼物 / 继承 |
| `price` | 购入价格 | 6799 |
| `image` | 图片路径 | /images/xxx.jpg |

正文部分写这件物品的故事。图片放到 `static/images/` 目录，`image` 字段填 `/images/文件名`。

## 本地预览

```bash
hugo server -D
# 打开 http://localhost:1313
```

## 发布

提交并推送到 `main` 分支即可，GitHub Actions 会自动构建并部署：

```bash
git add .
git commit -m "add: 新物品"
git push
```

> 首次使用需在仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。
