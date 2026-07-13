---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: false
# ==== 物品信息（按需填写）====
category: "未分类"        # 电子产品 / 家具 / 服饰 / 书籍 / 其他
acquired: ""              # 拥有起始日期，如 2021-01-15
lost: ""                 # 失去日期，如 2023-06-20
disposal: ""             # 卖出 / 送人 / 丢弃 / 损坏 / 丢失
source: ""               # 自购 / 礼物 / 继承
price: 0                 # 购入价格
image: ""                # 图片路径，如 /images/xxx.jpg
---

在这里写下这件物品的故事：它如何来到你身边，陪你度过了什么，又为何离开。
