# 熊佳乐的笔记 · 源仓库

这个仓库是**笔记源码 + 构建脚本**，不是最终的网页产物。每次推送到 `main`，GitHub Actions 会自动把 `vault/` 里的笔记编译成静态站点并发布到
<https://xjl-1.github.io/notes/>。

## 目录

```
vault/                 笔记本体（md / txt / docx，按文件夹分类）
assets/                style.css、app.js、edit.js、图标
build.py               构建：笔记 → 静态站点（site/）
md2html.py             无依赖的 Obsidian 风格 Markdown 渲染器
docx2md.py             .docx → markdown（优先 pandoc，缺失时用 python-docx）
publish.py             本地 → GitHub 的增量推送 / 拉取（纯 REST，不需要 git）
.github/workflows/     自动构建并部署到 GitHub Pages
```

## 在浏览器里改笔记

打开 <https://xjl-1.github.io/notes/edit.html>，粘一个带 `repo` + `workflow` 权限的
Classic token（只保存在本机浏览器），之后就能：

- 改已有笔记（md / txt 直接编辑）
- 新建笔记（自动带 frontmatter 头）
- 移动 / 重命名（改路径框里的路径再保存）
- 删除

保存后 GitHub 自动重建，约一分钟生效。每篇笔记页底部也有「编辑此页」直达链接。

## 在本机改笔记

`vault/` 是 `E:\Obsidian Vault` 的镜像，两种用法：

```powershell
# 把电脑上 vault 的改动推上去（会先镜像 E:\Obsidian Vault → ./vault）
python publish.py

# 把手机/网页上改的内容拉回电脑（同时写回 E:\Obsidian Vault）
python publish.py --pull

# 只看会改什么，不推送
python publish.py --dry
```

`E:\Obsidian Vault` 里改完，也可以只跑 `python publish.py`，一条命令搞定。

## 本地预览

```powershell
python build.py --vault vault --out site
python -m http.server 8765 --bind 127.0.0.1 --directory site
# 打开 http://127.0.0.1:8765/
```

## 支持的格式

| 后缀 | 处理方式 |
| --- | --- |
| `.md` / `.markdown` | 直接渲染（Obsidian 语法：wikilink、callout、dataview、任务列表） |
| `.txt` | 按纯文本渲染，首行自动当标题 |
| `.docx` | 用 pandoc 转成 markdown 再渲染，内嵌图片一起抽取 |
| `.doc` | **不支持**，构建时会跳过并提示；用 Word 另存为 `.docx` 即可 |

显式排除的目录/文件：`.obsidian/`、`.claude/`、`.trash/`、`模板/`、`node_modules/`、`CLAUDE.md`。

## 注意

- 仓库里**不要**提交 `site/`（构建产物，已在 `.gitignore` 中）。
- 图片放在笔记旁边即可，构建时会一起复制，路径写相对路径。
- 站内搜索索引 `search.json` 也是构建时生成的。
