---
title: 收件箱索引
tags: [index, InBox]
created: 2026-06-04
type: index
status: active
summary: 临时存放未分类笔记；下方清单由构建脚本自动生成，永远与目录实际内容一致。
---

# 收件箱（00 InBox）

临时存放还没归类的笔记。整理好之后，把它移动到 `知识笔记/` 下对应分区即可。

下面的清单**不是手写的**：每次构建（网页上新建/上传、或本地 `python publish.py`）都会重新扫描这个目录，所以收件箱里有什么，页面就显示什么。

## 当前内容

```dataview
table file.name as "笔记", file.ctime as "放入时间", file.mtime as "最后修改"
from "00 InBox"
sort file.mtime desc
```

## 整理流程

1. 新内容丢进 `00 InBox/`（网页「上传」按钮，或直接放进电脑上的 vault）。
2. 想好归属后，在网页编辑器里把路径改成 `知识笔记/<分区>/文件名` 再保存，等同于移动。
3. 收件箱清单自动少一条，目标分区自动多一条。
