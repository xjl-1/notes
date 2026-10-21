#!/usr/bin/env python3
"""
build.py — compile the Obsidian vault into a static site.

    python build.py            # build into ./site
    python build.py --clean    # wipe ./site first

Everything is pre-rendered: no runtime markdown, no framework, no CDN except
KaTeX on the (single) page that actually contains formulas.

Source formats: ``.md`` / ``.markdown`` / ``.txt`` are read as markdown,
``.docx`` is converted through docx2md.py (pandoc, python-docx as fallback).
Legacy ``.doc`` files are skipped with a hint.
"""

from __future__ import annotations

import json
import posixpath
import re
import shutil
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from docx2md import docx_to_markdown  # noqa: E402
from md2html import (  # noqa: E402
    Inline,
    as_list,
    convert,
    esc,
    slugify,
    split_frontmatter,
    text_of,
)

# --------------------------------------------------------------------------- #
# configuration
# --------------------------------------------------------------------------- #

CONFIG = {
    "vault": Path(r"D:\Notes"),
    "out": HERE / "site",
    "title": "lemishui",
    "short": "lemishui",
    "mark": "L",
    "hero_name": "lemishui",
    "hero_mark": "_",
    "tagline": "个人知识库 · 持续更新",
    "url": "https://xjl-1.github.io/notes",
    "desc": "个人知识库：编程、金融、通识、办公软件与英语学习。",
    "author": "lemishui",
}

EXCLUDE_DIRS = {".obsidian", ".claude", ".git", ".trash", "模板", "node_modules", "_setup"}
EXCLUDE_FILES = {"claude.md", "agents.md", "readme.md"}

# extension -> how to read it
SUPPORTED = {".md": "md", ".markdown": "md", ".txt": "txt", ".docx": "docx"}
DOCX_CACHE = HERE / ".cache" / "docx"

TOP_ORDER = ["知识笔记", "00 InBox", "Dataview", "归档"]

MONTH = {"01": "1", "02": "2", "03": "3", "04": "4", "05": "5", "06": "6",
         "07": "7", "08": "8", "09": "9", "10": "10", "11": "11", "12": "12"}


def log(msg: str) -> None:
    print(msg, flush=True)


def q(path: str) -> str:
    return urllib.parse.quote(path, safe="/")


# --------------------------------------------------------------------------- #
# icons
# --------------------------------------------------------------------------- #

def svg(path: str, size: int = 16, extra: str = "") -> str:
    return (
        f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
        f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true"{extra}>{path}</svg>'
    )


I = {
    "search": svg('<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4 4"/>'),
    "menu": svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "close": svg('<path d="m6 6 12 12M18 6 6 18"/>'),
    "sun": svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
    "moon": svg('<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a6.8 6.8 0 0 0 10.5 10.5z"/>'),
    "calendar": svg('<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10h17"/>'),
    "clock": svg('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>'),
    "hash": svg('<path d="M9.5 4 8 20M16 4l-1.5 16M4.5 9h15M3.5 15h15"/>'),
    "doc": svg('<path d="M6 3.5h7l5 5v12H6z"/><path d="M13 3.5v5h5"/><path d="M9 13h6M9 16.5h6"/>'),
    "chevron": svg('<path d="m9 6 6 6-6 6"/>'),
    "chev": svg('<path d="m9 6 6 6-6 6"/>', 12),
    "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "up": svg('<path d="M12 19V5M6 11l6-6 6 6"/>'),
    "folder": svg('<path d="M3.5 7.5A2 2 0 0 1 5.5 5.5h3.4l1.7 2h7.4a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5.5a2 2 0 0 1-2-2z"/>'),
    "tag": svg('<path d="M11.6 3.5H20v8.4l-8.7 8.7-8.4-8.4z"/><circle cx="16.3" cy="7.7" r="1.3"/>'),
    "layers": svg('<path d="M12 3.5 3.5 8l8.5 4.5L20.5 8z"/><path d="m3.5 12.5 8.5 4.5 8.5-4.5"/>'),
    "home": svg('<path d="M4 10.5 12 4l8 6.5"/><path d="M6.5 9.5V20h11V9.5"/>'),
    "A": svg('<path d="M5 19 12 5l7 14"/><path d="M8.2 14h7.6"/>'),
    "book": svg('<path d="M4 5.5A2 2 0 0 1 6 3.5h5v17H6a2 2 0 0 0-2 2z"/><path d="M20 5.5a2 2 0 0 0-2-2h-5v17h5a2 2 0 0 1 2 2z"/>'),
    "check": svg('<path d="m5 12.5 4.5 4.5L19 6.5"/>'),
    "edit": svg('<path d="M4.5 19.5h4L19 9a2.1 2.1 0 0 0-3-3L5.5 16.5z"/><path d="m14.5 7.5 3 3"/>'),
}


# --------------------------------------------------------------------------- #
# model
# --------------------------------------------------------------------------- #

class Note:
    __slots__ = (
        "src", "path_noext", "dir", "stem", "slug_parts", "out", "title", "tags",
        "created", "ntype", "status", "summary", "raw", "html", "headings", "plain",
        "words", "is_index", "links", "unresolved", "images", "mtime", "incoming",
        "kind", "media_root",
    )

    def __init__(self, src: str, raw: str, mtime: float):
        self.src = src
        self.raw = raw
        self.mtime = mtime
        self.path_noext = posixpath.splitext(src)[0]
        self.kind = "md"
        self.media_root: Path | None = None
        self.dir = posixpath.dirname(self.path_noext)
        self.stem = posixpath.basename(self.path_noext)
        parts = self.path_noext.split("/")
        self.slug_parts = [slugify(p) for p in parts]
        if self.stem == "index":
            self.out = "notes/" + "/".join(self.slug_parts[:-1] + ["index.html"])
        else:
            self.out = "notes/" + "/".join(self.slug_parts[:-1] + [self.slug_parts[-1] + ".html"])
        self.out = posixpath.normpath(self.out)
        self.is_index = self.stem == "index"
        self.title = self.stem
        self.tags: list[str] = []
        self.created = ""
        self.ntype = ""
        self.status = ""
        self.summary = ""
        self.html = ""
        self.headings: list[dict] = []
        self.plain = ""
        self.words = 0
        self.links: list[Note] = []
        self.unresolved: list[tuple[str, str]] = []
        self.images: list[str] = []
        self.incoming: list[Note] = []


class Folder:
    __slots__ = ("key", "name", "out", "notes", "children", "index_note", "depth")

    def __init__(self, key: str):
        self.key = key
        self.name = posixpath.basename(key) if key else ""
        self.out = ""
        self.notes: list[Note] = []
        self.children: dict[str, Folder] = {}
        self.index_note: Note | None = None

    def total(self) -> int:
        return len([n for n in self.notes if not n.is_index]) + sum(c.total() for c in self.children.values())


def folder_out(key: str) -> str:
    if not key:
        return "index.html"
    return "notes/" + "/".join(slugify(p) for p in key.split("/")) + "/index.html"


def rel_url(cur_out: str, target_out: str) -> str:
    start = posixpath.dirname(cur_out) or "."
    rel = posixpath.relpath(target_out, start)
    return q(rel)


def base_of(out: str) -> str:
    d = posixpath.dirname(out)
    return "../" * len(d.split("/")) if d else ""


def human_date(value: str) -> str:
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", value or "")
    if not m:
        return value or ""
    return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"


def parse_date(meta: dict, mtime: float) -> str:
    for key in ("created", "date", "updated"):
        raw = meta.get(key)
        if isinstance(raw, str) and raw.strip():
            m = re.search(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", raw)
            if m:
                return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")


# --------------------------------------------------------------------------- #
# discovery
# --------------------------------------------------------------------------- #

def discover(vault: Path):
    notes: list[Note] = []
    legacy_doc: list[str] = []
    for path in sorted(vault.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(vault).as_posix()
        parts = rel.split("/")
        if any(p.startswith(".") or p in EXCLUDE_DIRS for p in parts[:-1]):
            continue
        name = parts[-1]
        if name.startswith(".") or name.startswith("~$") or name.lower() in EXCLUDE_FILES:
            continue
        suffix = path.suffix.lower()
        if suffix == ".doc":
            legacy_doc.append(rel)
            continue
        kind = SUPPORTED.get(suffix)
        if kind is None:
            continue
        media_root = None
        if kind == "docx":
            try:
                raw, media_root = docx_to_markdown(path, DOCX_CACHE)
            except Exception as exc:  # noqa: BLE001 - one bad file must not stop the build
                log(f"! skipped {rel}: {exc}")
                continue
        else:
            try:
                raw = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                raw = path.read_text(encoding="utf-8", errors="replace")
            raw = raw.lstrip("\ufeff")
        note = Note(rel, raw, path.stat().st_mtime)
        note.kind = kind
        note.media_root = media_root
        notes.append(note)

    if legacy_doc:
        log(f"! skipped {len(legacy_doc)} legacy .doc file(s) (Word 97-2003)")
        for rel in legacy_doc[:6]:
            log(f"    {rel}")
        log("    → 用 Word 打开后「另存为 .docx」再放进来即可")
    return notes


def first_h1(body: str) -> str:
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    m = re.search(r"(?m)^#\s+(.+?)\s*#*\s*$", body)
    return text_of(m.group(1)).strip() if m else ""


def first_para(body: str) -> str:
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block or block.startswith(("#", "|", "-", "*", ">", "!", "$$", "[![")):
            continue
        block = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", block)
        block = re.sub(r"\[\[([^\]]+)\]\]", r"\1", block)
        block = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", block)
        block = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", block)
        text = re.sub(r"[*_`~=]+", "", block)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > 12:
            return text
    return ""


def collect_inline_tags(body: str) -> list[str]:
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    body = re.sub(r"`[^`\n]*`", "", body)
    # <mark style="background: #FF5582A6;"> must not register a tag called FF5582A6
    body = re.sub(r"<[^<>\n]{0,200}>", " ", body)
    found = re.findall(r"(?:(?<=\s)|^)#([\w\u4e00-\u9fa5][\w\u4e00-\u9fa5/+-]*)", body, re.M)
    out = []
    for t in found:
        if t.isdigit() or re.fullmatch(r"[0-9A-Fa-f]{6,8}", t):
            continue
        if t.lower() in {"include", "define", "if", "endif", "pragma", "else"}:
            continue
        if t not in out:
            out.append(t)
    return out


# --------------------------------------------------------------------------- #
# link resolution
# --------------------------------------------------------------------------- #

class Resolver:
    def __init__(self, notes: list[Note]):
        self.by_path: dict[str, Note] = {}
        self.by_stem: dict[str, list[Note]] = {}
        for n in notes:
            self.by_path[n.path_noext] = n
            self.by_stem.setdefault(n.stem, []).append(n)
        self.notes = notes

    def find(self, target: str, from_note: Note):
        t = target.strip().replace("\\", "/")
        t = re.sub(r"\.md$", "", t)
        if not t:
            return None, "empty"
        cands: list[str] = []
        if t.startswith("/"):
            cands.append(t.lstrip("/"))
        else:
            cands.append(posixpath.normpath(posixpath.join(from_note.dir, t)))
            cands.append(posixpath.normpath(t))
        for c in cands:
            c = c[2:] if c.startswith("./") else c
            if c in self.by_path:
                return self.by_path[c], "path"

        # suffix match: "办公三件/index" -> "知识笔记/办公三件/index"
        hits = [n for n in self.notes if n.path_noext.endswith("/" + t) or n.path_noext == t]
        if len(hits) == 1:
            return hits[0], "suffix"
        if len(hits) > 1:
            hits.sort(key=lambda n: len(n.path_noext))
            return hits[0], "suffix-ambig"

        stem = posixpath.basename(t)
        hits = self.by_stem.get(stem, [])
        if len(hits) == 1:
            return hits[0], "stem"
        if len(hits) > 1:
            hits.sort(key=lambda n: len(n.path_noext))
            return hits[0], "stem-ambig"
        return None, "missing"


# --------------------------------------------------------------------------- #
# page shell
# --------------------------------------------------------------------------- #

def render_page(
    *,
    out: str,
    page_title: str,
    meta_desc: str,
    main: str,
    nav_html: str,
    toc_html: str = "",
    head_extra: str = "",
    body_class: str = "",
    og_type: str = "website",
    html_extra: str = "",
    wide: bool = False,
) -> str:
    base = base_of(out)
    css = rel_url(out, "assets/style.css")
    js = rel_url(out, "assets/app.js")
    icon = rel_url(out, "assets/icon-192.png")
    full_title = page_title if page_title == CONFIG["title"] else f"{page_title} · {CONFIG['title']}"
    full_url = CONFIG["url"] + "/" + q(posixpath.relpath(out, "index.html").replace("\\", "/"))
    if out == "index.html":
        full_url = CONFIG["url"] + "/"

    return f"""<!doctype html>
<html lang="zh-CN" data-theme="dark" data-base="{base}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(meta_desc)}">
<meta name="color-scheme" content="dark light">
<meta name="theme-color" content="#0b0d10">
<meta name="author" content="{esc(CONFIG['author'])}">
<link rel="canonical" href="{esc(full_url)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(CONFIG['title'])}">
<meta property="og:title" content="{esc(page_title)}">
<meta property="og:description" content="{esc(meta_desc)}">
<meta property="og:url" content="{esc(full_url)}">
<meta name="twitter:card" content="summary">
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;var s=localStorage.getItem('size');var m={{s:'0.94',m:'1',l:'1.08'}};if(m[s])document.documentElement.style.setProperty('--step',m[s]);}}catch(e){{}}</script>
<link rel="stylesheet" href="{css}">
<link rel="icon" href="{icon}" type="image/png">
<link rel="apple-touch-icon" href="{rel_url(out, 'assets/apple-touch-icon.png')}">
<link rel="manifest" href="{rel_url(out, 'manifest.webmanifest')}">
{head_extra}</head>
<body class="{body_class}">
<a class="skip" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><div class="progress__bar"></div></div>
<header class="topbar">
  <button class="iconbtn" data-drawer-toggle aria-label="打开目录">{I['menu']}</button>
  <span class="topbar__title">{esc(CONFIG['short'])}</span>
  <button class="iconbtn" data-search-open aria-label="搜索">{I['search']}</button>
</header>
<div class="shell">
<aside class="sidebar" id="sidebar">
  <a class="brand" href="{rel_url(out, 'index.html')}">
    <span class="brand__mark">{esc(CONFIG['mark'])}</span>
    <span class="brand__text"><strong>{esc(CONFIG['title'])}</strong><span>{esc(CONFIG['tagline'])}</span></span>
  </a>
  <button class="searchbtn" type="button" data-search-open>
    {I['search']}<span>搜索笔记</span><kbd>/</kbd>
  </button>
  <nav class="nav" aria-label="导航">{nav_html}</nav>
  <div class="sidebar__foot">
    <div class="iconrow">
      <button class="iconbtn" data-theme-toggle aria-label="切换深浅色" title="切换深浅色"></button>
      <button class="iconbtn" data-size-toggle aria-label="切换字号" title="切换字号">{I["A"]}</button>
      <a class="iconbtn" href="{rel_url(out, 'tags/index.html')}" aria-label="标签" title="标签">{I["tag"]}</a>
      <a class="iconbtn" href="{rel_url(out, 'edit.html')}" aria-label="编辑笔记" title="编辑笔记">{I["edit"]}</a>
    </div>
  </div>
</aside>
<div class="scrim" data-drawer-close></div>
<main class="main{(' main--wide') if wide else ''}" id="main">
{main}
{toc_html}
</main>
</div>
<button class="totop" data-totop aria-label="回到顶部">{I['up']}</button>
<script src="{js}" defer></script>
{html_extra}</body>
</html>
"""


# --------------------------------------------------------------------------- #
# navigation
# --------------------------------------------------------------------------- #

def build_nav(root: Folder, current_folders: set[str], current_out: str, out: str) -> str:
    parts: list[str] = ['<p class="nav__label">浏览</p>', "<ul>"]
    home = rel_url(out, "index.html")
    parts.append(
        f'<li><a class="nav__link{" is-active" if out == "index.html" else ""}" href="{home}">'
        f'<span class="nav__dot"></span>首页</a></li>'
    )
    parts.append(
        f'<li><a class="nav__link{" is-active" if out.startswith("tags/") else ""}" '
        f'href="{rel_url(out, "tags/index.html")}"><span class="nav__dot"></span>标签</a></li>'
    )
    parts.append("</ul>")
    parts.append('<p class="nav__label">目录</p>')

    def render_folder(folder: Folder) -> str:
        active = folder.key in current_folders
        sub = "".join(render_folder(c) for c in sorted_folders(folder))
        notes = "".join(
            f'<a class="nav__link{" is-active" if n.out == current_out else ""}" href="{rel_url(out, n.out)}">'
            f'<span class="nav__dot"></span>{esc(n.title)}</a>'
            for n in sorted_notes(folder.notes)
            if not n.is_index
        )
        count = folder.total()
        badge = f'<span class="nav__count">{count}</span>' if count else ""
        if not sub and not notes:
            # 只有 index 的空分区（比如刚整理干净的收件箱）也要留一个入口
            return (
                f'<a class="nav__link{" is-active" if folder.out == current_out else ""}" '
                f'href="{rel_url(out, folder.out)}"><span class="nav__dot"></span>{esc(folder.name)}</a>'
            )
        overview = (
            f'<a class="nav__link" href="{rel_url(out, folder.out)}">'
            f'<span class="nav__dot"></span>总览</a>'
            if folder.out != current_out
            else ""
        )
        return (
            f'<details class="nav__tree"{(" open" if active else "")}>'
            f'<summary><span class="chev">{I["chev"]}</span>{esc(folder.name)}{badge}</summary>'            f"<div>{overview}{notes}{sub}</div></details>"
        )

    for folder in sorted_folders(root):
        parts.append(render_folder(folder))
    return "".join(p for p in parts if p)


def sorted_folders(folder: Folder) -> list[Folder]:
    def key(f: Folder):
        try:
            return (0, TOP_ORDER.index(f.name), "")
        except ValueError:
            return (1, 0, f.name)

    return sorted(folder.children.values(), key=key)


def sorted_notes(notes: list[Note]) -> list[Note]:
    idx = [n for n in notes if n.is_index]
    rest = sorted([n for n in notes if not n.is_index], key=lambda n: (n.created, n.title), reverse=True)
    return idx + rest


def ancestors(key: str) -> set[str]:
    out = set()
    parts = key.split("/") if key else []
    for i in range(len(parts) + 1):
        out.add("/".join(parts[:i]))
    return out


# --------------------------------------------------------------------------- #
# dataview — build-time subset of the Obsidian plugin
# --------------------------------------------------------------------------- #
#
# Obsidian runs Dataview queries inside the app; a static site can't. Instead we
# evaluate them while building and bake the result into the page, so every push
# (web editor or `publish.py`) re-runs the query and the list is always current.
#
# Supported: LIST / TABLE [expr as "alias", …] / FROM "folder" or #tag /
#            WHERE <expr> / SORT <expr> [asc|desc] / LIMIT n
# Queries only run on pages with `type: index`; elsewhere (tutorial notes) the
# code block is shown verbatim so syntax examples stay readable.

DV_CLAUSE = re.compile(r"(?i)\s+(from|where|sort|limit)\s+")


def dv_date(ts: float) -> str:
    try:
        return time.strftime("%Y-%m-%d", time.localtime(ts))
    except (OverflowError, OSError, ValueError):
        return ""


def dv_value(note: Note, expr: str):
    key = re.sub(r"\s+", "", expr).lower()
    if key in ("file.name", "file.basename", "filename", "name"):
        return posixpath.basename(note.src)
    if key in ("file.path", "path"):
        return note.src
    if key in ("file.folder", "folder"):
        return note.dir
    if key == "file.link":
        return note
    if key in ("file.ctime", "file.created", "file.day", "created", "date"):
        return note.created
    if key in ("file.mtime", "file.modified", "updated", "modified"):
        return dv_date(note.mtime)
    if key in ("file.size",):
        return f"{note.words} 字"
    if key in ("title", "file.frontmatter.title"):
        return note.title
    if key in ("type", "file.frontmatter.type"):
        return note.ntype
    if key in ("status", "file.frontmatter.status"):
        return note.status
    if key in ("summary", "description"):
        return note.summary
    if key in ("tags", "file.tags"):
        return note.tags
    if key == "words":
        return note.words
    if key == "file.outlinks":
        return len(note.links)
    if key == "file.inlinks":
        return len(note.incoming)
    return ""


def dv_top_split(text: str, sep: str) -> list[str]:
    """Split on `sep` ignoring anything inside quotes or parentheses."""
    out: list[str] = []
    buf: list[str] = []
    depth = 0
    quote = ""
    i = 0
    low = text.lower()
    needle = sep.lower()
    while i < len(text):
        ch = text[i]
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if depth <= 0 and low.startswith(needle, i):
            out.append("".join(buf))
            buf = []
            i += len(needle)
            continue
        buf.append(ch)
        i += 1
    out.append("".join(buf))
    return [p.strip() for p in out if p.strip()]


def dv_operand(text: str, note: Note):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    if re.match(r"(?i)^(true|false)$", text):
        return text.lower() == "true"
    if re.match(r"^-?\d+(\.\d+)?$", text):
        return float(text) if "." in text else int(text)
    return dv_value(note, text)


def dv_compare(left, op: str, right) -> bool:
    if isinstance(left, list):
        left = ", ".join(str(x) for x in left)
    if isinstance(right, list):
        right = ", ".join(str(x) for x in right)
    a, b = str(left), str(right)
    if op == "=":
        return a.strip().lower() == b.strip().lower()
    if op == "!=":
        return a.strip().lower() != b.strip().lower()
    try:
        fa, fb = float(a), float(b)
        a, b = fa, fb  # type: ignore[assignment]
    except (TypeError, ValueError):
        pass
    if op in (">", "<", ">=", "<="):
        try:
            return {">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]  # type: ignore[operator]
        except TypeError:
            return False
    return False


def dv_eval(cond: str, note: Note) -> bool:
    cond = cond.strip()
    while cond.startswith("(") and cond.endswith(")") and len(dv_top_split(cond[1:-1], " or ")) == 1:
        inner = cond[1:-1]
        if inner.count("(") == inner.count(")"):
            cond = inner.strip()
        else:
            break
    parts = dv_top_split(cond, " or ")
    if len(parts) > 1:
        return any(dv_eval(p, note) for p in parts)
    parts = dv_top_split(cond, " and ")
    if len(parts) > 1:
        return all(dv_eval(p, note) for p in parts)
    if cond.startswith("!"):
        return not dv_eval(cond[1:], note)
    if re.match(r"(?i)^not\s+", cond):
        return not dv_eval(re.sub(r"(?i)^not\s+", "", cond), note)
    m = re.match(r"(?is)^(?:i?contains)\(\s*(.+?)\s*,\s*(.+?)\s*\)$", cond)
    if m:
        left = dv_operand(m.group(1), note)
        right = dv_operand(m.group(2), note)
        needle = str(right).lower()
        if isinstance(left, list):
            return needle in [str(x).lower() for x in left]
        return needle in str(left).lower()
    m = re.match(r"(?is)^(.+?)\s*(!=|>=|<=|=|>|<)\s*(.+)$", cond)
    if m:
        return dv_compare(dv_operand(m.group(1), note), m.group(2), dv_operand(m.group(3), note))
    return False


def dv_parse(text: str) -> dict | None:
    lines = [ln.strip() for ln in text.splitlines()]
    body = " ".join(ln for ln in lines if ln and not ln.startswith("%%"))
    m = re.match(r"(?is)^(table|list)\b(.*)$", body.strip())
    if not m:
        return None
    mode = m.group(1).lower()
    rest = m.group(2)
    found = list(DV_CLAUSE.finditer(rest))
    head = rest[: found[0].start()] if found else rest
    clauses: dict[str, str] = {}
    for i, hit in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(rest)
        clauses[hit.group(1).lower()] = rest[hit.end():end].strip()

    columns: list[tuple[str, str]] = []
    if mode == "table":
        head = re.sub(r"(?i)^\s*without\s+id\s*", "", head).strip()
        for part in dv_top_split(head, ","):
            alias = re.match(r"(?is)^(.*?)\s+as\s+(.+)$", part)
            if alias:
                expr = alias.group(1).strip()
                label = alias.group(2).strip().strip("\"'")
            else:
                expr, label = part.strip(), part.strip()
            columns.append((expr, label or expr))

    sources: list[str] = []
    from_text = clauses.get("from", "")
    sources += re.findall(r'"([^"]+)"', from_text)
    sources += ["#" + t for t in re.findall(r"#([\w\u4e00-\u9fa5/-]+)", from_text)]
    if not sources and from_text:
        sources = [s.strip().strip("\"'") for s in re.split(r"(?i)\s+or\s+", from_text) if s.strip()]

    sorts: list[tuple[str, bool]] = []
    for part in dv_top_split(clauses.get("sort", ""), ","):
        desc = bool(re.search(r"(?i)\s+desc$", part))
        expr = re.sub(r"(?i)\s+(asc|desc)$", "", part).strip()
        if expr:
            sorts.append((expr, desc))

    limit = 0
    if clauses.get("limit"):
        try:
            limit = int(clauses["limit"].split()[0])
        except (ValueError, IndexError):
            limit = 0

    return {
        "mode": mode,
        "columns": columns,
        "sources": sources,
        "where": clauses.get("where", ""),
        "sort": sorts,
        "limit": limit,
        "source": body.strip(),
    }


def dv_collect(folders: dict[str, Folder], notes: list[Note], sources: list[str], skip: Note | None) -> list[Note]:
    picked: list[Note] = []
    seen: set[str] = set()
    for spec in sources:
        spec = spec.strip()
        if spec.startswith("#"):
            tag = spec[1:].lower()
            hits = [n for n in notes if tag in [t.lower() for t in n.tags]]
        else:
            key = spec.strip("/")
            node = folders.get(key)
            if node is None:
                cands = [k for k in folders if k and (k == key or k.endswith("/" + key))]
                node = folders[cands[0]] if cands else None
            if node is None:
                continue
            hits = []
            stack = [node]
            while stack:
                cur = stack.pop()
                hits.extend(cur.notes)
                stack.extend(cur.children.values())
        for n in hits:
            if n is skip or n.is_index or n.out in seen:
                continue
            seen.add(n.out)
            picked.append(n)
    return picked


def dv_cell(note: Note, expr: str, out: str, folders: dict[str, Folder]) -> str:
    value = dv_value(note, expr)
    if isinstance(value, Note):
        return f'<a href="{rel_url(out, value.out)}">{esc(value.title)}</a>'
    if isinstance(value, list):
        if not value:
            return ""
        if all(isinstance(v, str) and v.startswith("#") for v in value):
            return " ".join(f'<span class="chip chip--soft">{esc(v)}</span>' for v in value)
        return "、".join(esc(str(v)) for v in value)
    if isinstance(value, int):
        return f"{value:,}"
    return esc(str(value))


def make_dataview(folders: dict[str, Folder], out: str, notes: list[Note], current: Note | None):
    def handler(body: str, lang: str) -> str | None:
        if lang != "dataview":
            return None
        if current is not None and current.ntype != "index":
            return None  # tutorial pages: leave the query visible as code
        query = dv_parse(body)
        if query is None or not query["sources"]:
            return None
        picked = dv_collect(folders, notes, query["sources"], current)
        if query["where"]:
            picked = [n for n in picked if dv_eval(query["where"], n)]
        for expr, desc in reversed(query["sort"]):
            picked.sort(key=lambda n, e=expr: str(dv_value(n, e)), reverse=desc)
        if query["limit"]:
            picked = picked[: query["limit"]]

        src = f'<details class="dv-source"><summary>查询语句</summary><pre><code>{esc(query["source"])}</code></pre></details>'
        if not picked:
            return (
                '<div class="dv-block"><p class="dv-empty">这个查询当前没有匹配到笔记。</p>' + src + "</div>"
            )

        if query["mode"] == "list":
            items = "".join(
                f'<li><a href="{rel_url(out, n.out)}">{esc(n.title)}</a>'
                f'<span class="dv__meta">{esc(n.created or dv_date(n.mtime))}</span></li>'
                for n in picked
            )
            inner = f'<ul class="dv">{items}</ul>'
        else:
            head = '<th scope="col">笔记</th>' + "".join(f'<th scope="col">{esc(label)}</th>' for _, label in query["columns"])
            rows = []
            for n in picked:
                cells = "".join(f"<td>{dv_cell(n, expr, out, folders)}</td>" for expr, _ in query["columns"])
                rows.append(f'<tr><td><a href="{rel_url(out, n.out)}">{esc(n.title)}</a></td>{cells}</tr>')
            inner = (
                '<div class="tablewrap"><table class="dv-table"><thead><tr>'
                + head
                + "</tr></thead><tbody>"
                + "".join(rows)
                + "</tbody></table></div>"
            )
        return (
            f'<div class="dv-block"><p class="dv-count">数据视图 · {len(picked)} 条</p>'
            f"{inner}{src}</div>"
        )

    return handler


# --------------------------------------------------------------------------- #
# article / components
# --------------------------------------------------------------------------- #

def article_html(note: Note, out: str, all_notes: list[Note], folders: dict[str, Folder], pager: tuple) -> str:
    home = rel_url(out, "index.html")
    crumbs = [f'<a href="{home}">首页</a>']
    acc = ""
    for part in note.dir.split("/") if note.dir else []:
        acc = part if not acc else f"{acc}/{part}"
        fo = folder_out(acc)
        crumbs.append(f'<span>/</span><a href="{rel_url(out, fo)}">{esc(part)}</a>')

    chips = []
    for tag in note.tags:
        chips.append(
            f'<a class="chip" href="{rel_url(out, f"tags/{slugify(tag)}.html")}">{esc(tag)}</a>'
        )
    if note.ntype and note.ntype not in ("note",):
        chips.append(f'<span class="chip chip--soft">{esc(note.ntype)}</span>')
    if note.status and note.status not in ("active",):
        chips.append(f'<span class="chip chip--soft">{esc(note.status)}</span>')

    minutes = max(1, round(note.words / 350))
    meta_bits = [
        f'<span class="meta__item">{I["calendar"]}{esc(human_date(note.created))}</span>' if note.created else "",
        f'<span class="meta__item">{I["clock"]}{minutes} 分钟</span>',
        f'<span class="meta__item">{I["doc"]}{note.words:,} 字</span>',
    ]
    meta_html = '<span class="sep"></span>'.join(m for m in meta_bits if m)

    related: list[Note] = []
    seen = {note.out}
    for n in sorted(note.incoming, key=lambda x: x.created, reverse=True):
        if n.out not in seen:
            related.append(n)
            seen.add(n.out)
    for n in sorted(folders.get(note.dir).notes if folders.get(note.dir) else [], key=lambda x: x.created, reverse=True):
        if len(related) >= 6:
            break
        if n.out not in seen:
            related.append(n)
            seen.add(n.out)

    parent_out = folders[note.dir].out if note.dir in folders else "index.html"
    related_html = ""
    if related:
        items = "".join(
            f'<a class="related__item" href="{rel_url(out, n.out)}">'
            f'<span class="related__title">{esc(n.title)}</span>'
            + (f'<span class="related__desc">{esc((n.summary or "")[:70])}</span>' if n.summary else "")
            + "</a>"
            for n in related[:6]
        )
        related_html = (
            '<div class="noteend__head"><span class="noteend__title">相关笔记</span>'
            f'<a class="section__more" href="{rel_url(out, parent_out)}">所属目录 →</a></div>'
            f'<div class="related">{items}</div>'
        )
    else:
        related_html = (
            '<div class="noteend__head"><span class="noteend__title">笔记结束</span>'
            f'<a class="section__more" href="{rel_url(out, parent_out)}">返回目录 →</a></div>'
        )

    prev_note, next_note = pager
    pager_html = ""
    if prev_note or next_note:
        cells = []
        if prev_note:
            cells.append(
                f'<a class="pager__item" href="{rel_url(out, prev_note.out)}">'
                f'<span class="pager__dir">← 上一篇</span>'
                f'<span class="pager__title">{esc(prev_note.title)}</span></a>'
            )
        if next_note:
            cells.append(
                f'<a class="pager__item pager__item--next" href="{rel_url(out, next_note.out)}">'
                f'<span class="pager__dir">下一篇 →</span>'
                f'<span class="pager__title">{esc(next_note.title)}</span></a>'
            )
        pager_html = '<nav class="pager" aria-label="翻页">' + "".join(cells) + "</nav>"

    head = f"""<article class="article">
<nav class="crumbs" aria-label="位置">{"".join(crumbs)}</nav>
<header>
<h1 class="article__title">{esc(note.title)}</h1>
{f'<p class="lede">{esc(note.summary)}</p>' if note.summary else ""}
{f'<div class="meta">{meta_html}</div>' if meta_html else ""}
{f'<div class="chips">{"".join(chips)}</div>' if chips else ""}
<p class="article__tools"><a class="editlink" href="{rel_url(out, 'edit.html')}?path={q('vault/' + note.src)}">{I['edit']}编辑此页</a></p>
</header>
<div class="prose">"""

    foot = f"""</div>
<footer class="noteend">
{related_html}
</footer>
{pager_html}
</article>"""

    return head + note.html + foot


def toc_html(headings: list[dict], out: str) -> str:
    if not headings:
        return ""
    h2 = [h for h in headings if h["level"] == 2]
    h3 = [h for h in headings if h["level"] == 3]
    items = h2 if (len(h2) + len(h3) > 28) else [h for h in headings if h["level"] <= 3]
    if len(items) < 2:
        return ""
    links = "".join(
        f'<li class="lvl-{h["level"]}"><a href="#{esc(h["id"])}">{esc(h["text"])}</a></li>'
        for h in items
    )
    return (
        '<nav class="toc" aria-label="本页目录">'
        '<p class="toc__label">本页目录</p>'
        f"<ul>{links}</ul></nav>"
    )


def note_row(n: Note, out: str) -> str:
    sub = esc((n.summary or "")[:64])
    folder = esc(n.dir.split("/")[-1]) if n.dir else ""
    return (
        f'<a class="list__row" href="{rel_url(out, n.out)}">'
        f'<span class="list__title">{esc(n.title)}</span>'
        f'<span class="list__date">{esc(human_date(n.created)[5:].replace("-", ".") if n.created else "")}</span>'
        f'<span class="list__desc">{sub}</span>'
        + (f'<span class="list__folder">{folder}</span>' if out in ("index.html", "tags/index.html") else "")
        + "</a>"
    )


def folder_card(c: "Folder", out: str, width: int = 56) -> str:
    desc = ""
    if c.index_note and c.index_note.summary:
        desc = esc(c.index_note.summary[:width])
    return (
        f'<a class="card" href="{rel_url(out, c.out)}">'
        f'<span class="card__top"><span class="card__icon">{I["folder"]}</span>'
        f'<span class="card__meta">{c.total()} 篇</span></span>'
        f'<span class="card__title">{esc(c.name)}</span>'
        + (f'<span class="card__desc">{desc}</span>' if desc else "")
        + "</a>"
    )


def tag_cloud(tag_items, out: str, tag_out: dict[str, str]) -> str:
    return "".join(
        f'<a href="{rel_url(out, tag_out[t])}">{esc(t)}<span>{len(v)}</span></a>'
        for t, v in tag_items
    )


def section_head(title: str, more: str = "") -> str:
    return (
        f'<div class="section__head"><h2 class="section__title">{esc(title)}</h2>{more}</div>'
    )


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #

USAGE = """\
usage: python build.py [options]

  --vault PATH   source folder (default: D:\\Notes, else ./vault)
  --out PATH     output folder (default: ./site)
  --url URL      public site url (default: %s)
  --clean        wipe the output folder first
""" % CONFIG["url"]


def parse_args(argv: list[str]) -> dict:
    opts = {
        # edit notes where they live (D:\Notes); fall back to the ./vault mirror
        "vault": CONFIG["vault"] if CONFIG["vault"].is_dir() else HERE / "vault",
        "out": CONFIG["out"],
        "url": CONFIG["url"],
        "clean": False,
        "help": False,
    }
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("-c", "--clean"):
            opts["clean"] = True
        elif arg in ("-h", "--help"):
            opts["help"] = True
        elif arg.split("=", 1)[0] in ("--vault", "--out", "--url"):
            key, sep, value = arg.partition("=")
            if not sep:
                i += 1
                if i >= len(argv):
                    raise SystemExit(f"{key} needs a value\n{USAGE}")
                value = argv[i]
            key = key[2:]
            opts[key] = Path(value).expanduser() if key != "url" else value.rstrip("/")
        else:
            raise SystemExit(f"unknown option: {arg}\n{USAGE}")
        i += 1
    return opts


def main() -> int:
    opts = parse_args(sys.argv[1:])
    if opts["help"]:
        print(USAGE)
        return 0
    CONFIG["url"] = opts["url"]

    OUT: Path = opts["out"]
    if opts["clean"] and OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    vault: Path = opts["vault"]
    if not vault.exists():
        log(f"! vault not found: {vault}")
        return 1
    log(f"· vault: {vault}")
    log(f"· out:   {OUT}")

    notes = discover(vault)
    log(f"· {len(notes)} notes found")

    # ---- metadata pass -----------------------------------------------------
    for n in notes:
        meta, body, _ = split_frontmatter(n.raw)
        title = meta.get("title")
        n.title = str(title).strip() if isinstance(title, str) and title.strip() else ""
        if not n.title:
            n.title = first_h1(body) or (posixpath.basename(n.dir) if n.is_index else n.stem)
            if n.kind in ("txt", "docx") and not first_h1(body) and not n.is_index:
                lines = body.splitlines()
                for idx, line in enumerate(lines):
                    head = line.strip()
                    if not head:
                        continue
                    if 0 < len(head) <= 40 and not head.startswith(("#", "-", "|", "!", ">", "<!--")):
                        head = re.sub(r"[*_`~=]+", "", head).strip()
                        if head:
                            n.title = head
                            # the first line served as the title: don't repeat it
                            del lines[idx]
                            n.raw = split_frontmatter(n.raw)[2] + "\n".join(lines)
                    break
        tags = as_list(meta.get("tags"))
        for t in collect_inline_tags(body):
            if t not in tags:
                tags.append(t)
        n.tags = tags
        n.created = parse_date(meta, n.mtime)
        n.ntype = str(meta.get("type", "") or "")
        n.status = str(meta.get("status", "") or "")
        sm = meta.get("summary")
        n.summary = str(sm).strip() if isinstance(sm, str) else ""
        if not n.summary:
            n.summary = first_para(body)[:110]

    bodies = {}

    # ---- folder tree -------------------------------------------------------
    root = Folder("")
    folders: dict[str, Folder] = {"": root}
    for n in notes:
        key = n.dir
        while True:
            if key not in folders:
                folders[key] = Folder(key)
            if key == "":
                break
            key = posixpath.dirname(key)
    for key, f in folders.items():
        f.out = folder_out(key)
    for key in folders:
        if not key:
            continue
        parent = folders[posixpath.dirname(key)]
        parent.children[posixpath.basename(key)] = folders[key]
    for n in notes:
        folders[n.dir].notes.append(n)
        if n.is_index:
            folders[n.dir].index_note = n

    # ---- resolve links ------------------------------------------------------
    resolver = Resolver(notes)
    for n in notes:
        folders[n.dir].out = n.out if n.is_index else folders[n.dir].out

    # ---- render notes -------------------------------------------------------
    known_tags = {t for n in notes for t in n.tags}
    tag_slug = {t: slugify(t, "tag") for t in known_tags}
    tag_out = {t: f"tags/{tag_slug[t]}.html" for t in known_tags}

    for n in notes:
        body = split_frontmatter(n.raw)[1]
        bodies[n.out] = body

        def make_resolve(note=n):
            def resolve(target: str):
                hit, how = resolver.find(target, note)
                if hit is None:
                    note.unresolved.append((target, how))
                    return None
                if hit is not note:
                    if hit not in note.links:
                        note.links.append(hit)
                    if note not in hit.incoming:
                        hit.incoming.append(note)
                return rel_url(note.out, hit.out)

            return resolve

        inline = Inline(
            make_resolve(),
            known_tags,
            tag_url=lambda tag, note=n: rel_url(note.out, tag_out[tag]) if tag in tag_out else None,
        )
        result = convert(
            n.raw,
            inline,
            dataview=make_dataview(folders, n.out, notes, n),
            min_heading_shift=True,
        )
        n.html = result["html"]
        n.headings = result["headings"]
        n.plain = result["plain"]
        n.words = result["words"]

        # local images -> report
        for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)", body):
            src = m.group(1)
            if re.match(r"^(https?:)?//", src) or src.startswith("data:"):
                continue
            n.images.append(src)

    # ---- write pages -------------------------------------------------------
    pages: list[str] = []

    def write(out: str, html: str) -> None:
        path = OUT / out
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8", newline="\n")
        pages.append(out)

    # note + folder pages
    for n in notes:
        folder = folders[n.dir]
        cur_folders = ancestors(n.dir)
        nav = build_nav(root, cur_folders, n.out, n.out)
        main = article_html(n, n.out, notes, folders, pager_for(n, notes))
        if n.is_index:
            siblings = [x for x in sorted_notes(folder.notes) if x is not n]
            subdirs = sorted_folders(folder)
            extra = ""
            if subdirs:
                cards = "".join(folder_card(c, n.out) for c in subdirs)
                extra += (
                    '<section class="section">'
                    + section_head("子目录")
                    + f'<div class="cards">{cards}</div></section>'
                )
            if siblings:
                rows = "".join(note_row(x, n.out) for x in siblings)
                extra += (
                    '<section class="section">'
                    + section_head("本目录笔记", f'<span class="section__more">{len(siblings)} 篇</span>')
                    + f'<div class="list">{rows}</div></section>'
                )
            if extra:
                main = main.replace('<footer class="noteend">', extra + '<footer class="noteend">', 1)
        write(n.out, render_page(
            out=n.out,
            page_title=n.title,
            meta_desc=n.summary or CONFIG["desc"],
            main=main,
            nav_html=nav,
            toc_html=toc_html(n.headings, n.out),
            og_type="article",
            body_class="page-note",
        ))

    # folder pages without an index note
    def folder_page(folder: Folder) -> str:
        out = folder.out
        cur_folders = ancestors(folder.key)
        nav = build_nav(root, cur_folders, out, out)
        crumbs = [f'<a href="{rel_url(out, "index.html")}">首页</a>']
        acc = ""
        for part in folder.key.split("/"):
            acc = part if not acc else f"{acc}/{part}"
            crumbs.append(f'<span>/</span><a href="{rel_url(out, folder_out(acc))}">{esc(part)}</a>')
        subdirs = sorted_folders(folder)
        own = [x for x in sorted_notes(folder.notes) if not x.is_index]
        cards = "".join(folder_card(c, out) for c in subdirs)
        rows = "".join(note_row(x, out) for x in own)
        cards_sec = (
            '<section class="section">' + section_head("子目录")
            + f'<div class="cards">{cards}</div></section>'
            if cards else ""
        )
        rows_sec = (
            '<section class="section">'
            + section_head("笔记", f'<span class="section__more">{len(own)} 篇</span>')
            + f'<div class="list">{rows}</div></section>'
            if rows else ""
        )
        main = f"""<article class="article">
<nav class="crumbs" aria-label="位置">{"".join(crumbs)}</nav>
<header>
<h1 class="article__title">{esc(folder.name)}</h1>
<p class="lede">{folder.total()} 篇笔记 · 持续整理中</p>
</header>
{cards_sec}
{rows_sec}
</article>"""
        html = render_page(
            out=out,
            page_title=folder.name,
            meta_desc=f"{folder.name}：{folder.total()} 篇笔记",
            main=main,
            nav_html=nav,
            body_class="page-folder",
        )
        return html

    for key, folder in sorted(folders.items()):
        if key == "" or folder.index_note:
            continue
        write(folder.out, folder_page(folder))

    # ---- tag pages ---------------------------------------------------------
    tag_notes: dict[str, list[Note]] = {}
    for n in notes:
        for t in n.tags:
            tag_notes.setdefault(t, []).append(n)
    tag_notes = {t: v for t, v in tag_notes.items() if v}

    tags_out = "tags/index.html"
    tags_nav = build_nav(root, {"tags"}, tags_out, tags_out)
    tag_items = sorted(tag_notes.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    cloud = tag_cloud(tag_items, tags_out, tag_out)
    main_tags = f"""<article class="article">
<nav class="crumbs" aria-label="位置"><a href="{rel_url(tags_out, 'index.html')}">首页</a><span>/</span><span>标签</span></nav>
<header>
<h1 class="article__title">标签</h1>
<p class="lede">共 {len(tag_notes)} 个标签，{sum(len(v) for v in tag_notes.values())} 次引用。</p>
</header>
<section class="section">{section_head("全部标签")}<div class="cloud">{cloud or '<p class="empty">还没有标签。</p>'}</div></section>
</article>"""
    write(tags_out, render_page(
        out=tags_out, page_title="标签", meta_desc="全部标签",
        main=main_tags, nav_html=tags_nav, body_class="page-tags", wide=True,
    ))

    for tag, items in tag_items:
        out = tag_out[tag]
        nav = build_nav(root, {"tags"}, out, out)
        rows = "".join(note_row(x, out) for x in sorted(items, key=lambda n: n.created, reverse=True))
        main_tag = f"""<article class="article">
<nav class="crumbs" aria-label="位置"><a href="{rel_url(out, 'index.html')}">首页</a><span>/</span><a href="{rel_url(out, tags_out)}">标签</a></nav>
<header>
<h1 class="article__title">{esc(tag)}</h1>
<p class="lede">{len(items)} 篇笔记</p>
</header>
<section class="section">{section_head("笔记", f'<span class="section__more">{len(items)} 篇</span>')}<div class="list">{rows}</div></section>
</article>"""
        write(out, render_page(
            out=out, page_title=f"#{tag}", meta_desc=f"标签 {tag} 下的笔记",
            main=main_tag, nav_html=nav, body_class="page-tag",
        ))

    # ---- home --------------------------------------------------------------
    home_out = "index.html"
    home_nav = build_nav(root, set(), home_out, home_out)
    by_date = sorted([n for n in notes if not n.is_index], key=lambda n: (n.created, n.title), reverse=True)
    recent = by_date[:7]
    recent_rows = "".join(note_row(n, home_out) for n in recent)

    top_cards = "".join(folder_card(c, home_out, 60) for c in sorted_folders(root))

    total_words = sum(n.words for n in notes)
    updated = max((n.created for n in notes if n.created), default="")
    note_count = len([n for n in notes if not n.is_index])

    main_home = f"""<div class="hero">
<p class="hero__eyebrow">{esc(CONFIG['tagline'])}</p>
<h1 class="hero__title hero__title--mono">{esc(CONFIG['hero_name'])}<em>{esc(CONFIG['hero_mark'])}</em></h1>
<div class="hero__stats">
<span><b>{note_count}</b> 篇笔记</span>
<span><b>{len(tag_notes)}</b> 个标签</span>
<span><b>{total_words // 1000}k</b> 字</span>
<span><b>{esc(updated[2:].replace('-', '.')) if updated else '—'}</b> 最近更新</span>
</div>
</div>
<section class="section">
{section_head("最近更新", f'<span class="section__more">按更新时间排序</span>')}
<div class="list">{recent_rows}</div>
</section>
<section class="section">
{section_head("分类")}
<div class="cards">{top_cards}</div>
</section>
<section class="section">
{section_head("标签云", f'<a class="section__more" href="{rel_url(home_out, "tags/index.html")}">全部标签 →</a>')}
<div class="cloud">{tag_cloud(tag_items, home_out, tag_out)}</div>
</section>
<section class="section">
{section_head("全部笔记", f'<span class="section__more">{note_count} 篇</span>')}
<div class="list">{''.join(note_row(n, home_out) for n in by_date)}</div>
</section>
<footer class="foot">
<span>纯静态站点 · GitHub Pages 托管</span>
<span>{esc(CONFIG['author'])} · 持续整理中</span>
</footer>"""

    write(home_out, render_page(
        out=home_out, page_title=CONFIG["title"], meta_desc=CONFIG["desc"],
        main=main_home, nav_html=home_nav, body_class="page-home", wide=True,
    ))

    # ---- in-browser editor -------------------------------------------------
    edit_out = "edit.html"
    main_edit = f"""<article class="article article--editor">
<nav class="crumbs" aria-label="位置"><a href="{rel_url(edit_out, 'index.html')}">首页</a><span>/</span><span>编辑</span></nav>
<header>
<h1 class="article__title">编辑笔记</h1>
<p class="lede">在这里直接改 md / txt，或者新建、移动、删除笔记。保存后 GitHub 会自动重新生成站点，大约一分钟生效。</p>
</header>
<div id="editor" class="editor"><p class="ed-status">正在加载…</p></div>
</article>"""
    write(edit_out, render_page(
        out=edit_out, page_title="编辑笔记", meta_desc="在浏览器里直接修改笔记",
        main=main_edit, nav_html=build_nav(root, set(), edit_out, edit_out),
        body_class="page-editor", wide=True,
        html_extra=f'<script src="{rel_url(edit_out, "assets/edit.js")}" defer></script>\n',
    ))

    # ---- assets ------------------------------------------------------------
    assets_src = HERE / "assets"
    assets_dst = OUT / "assets"
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(assets_src, assets_dst)

    # local images referenced by notes
    copied = 0
    for n in notes:
        for src in n.images:
            clean = urllib.parse.unquote(src)
            candidates = [
                vault / n.dir / clean if n.dir else vault / clean,
                vault / clean,
            ]
            if n.media_root is not None:
                candidates.append(n.media_root / clean)
            for cand in candidates:
                if cand.exists() and cand.is_file():
                    dest = OUT / posixpath.dirname(n.out) / clean
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(cand, dest)
                    copied += 1
                    break
    log(f"· copied {copied} local images")

    # ---- search index ------------------------------------------------------
    search = {
        "notes": [
            {
                "t": n.title,
                "u": n.out,
                "s": n.summary,
                "k": n.tags,
                "f": n.dir or "根目录",
                "d": n.created,
                "p": "vault/" + n.src,
                "x": re.sub(r"\s+", " ", n.plain)[:2200],
            }
            for n in sorted(notes, key=lambda n: (n.created, n.title), reverse=True)
        ],
        "tags": [[t, tag_out[t], len(v)] for t, v in tag_items],
    }
    (OUT / "search.json").write_text(
        json.dumps(search, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )

    # ---- misc files --------------------------------------------------------
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {CONFIG['url']}/sitemap.xml\n", encoding="utf-8"
    )
    urls = []
    for p in pages:
        if p == "index.html":
            urls.append(CONFIG["url"] + "/")
        else:
            urls.append(CONFIG["url"] + "/" + q(p))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sitemap.append(f"<url><loc>{esc(u)}</loc></url>")
    sitemap.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    notfound = render_page(
        out="404.html",
        page_title="页面走丢了",
        meta_desc="没有找到这个页面",
        main=f"""<article class="article"><div class="notfound">
<p class="notfound__code">404</p>
<h1 class="article__title">这页笔记不在</h1>
<p class="lede">可能链接写错了，或者它已经被合并到别处。</p>
<p style="margin-top:1.6rem"><a class="btn" href="{rel_url('404.html', 'index.html')}">回到首页</a></p>
</div></article>""",
        nav_html=build_nav(root, set(), "404.html", "404.html"),
        body_class="page-404",
    )
    write("404.html", notfound)

    (OUT / "manifest.webmanifest").write_text(json.dumps({
        "name": CONFIG["title"],
        "short_name": CONFIG["short"],
        "description": CONFIG["desc"],
        "start_url": "./",
        "display": "standalone",
        "background_color": "#0b0d10",
        "theme_color": "#0b0d10",
        "icons": [
            {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "assets/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
        ],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    make_icons(assets_dst)

    # ---- report ------------------------------------------------------------
    log(f"· {len(pages)} pages written to {OUT}")
    missing = [(n.title, t) for n in notes for t in n.unresolved]
    if missing:
        log(f"! {len(missing)} unresolved wikilinks:")
        for title, (target, how) in missing[:20]:
            log(f"    {title} -> [[{target}]] ({how})")
    leftovers = check_artifacts(OUT, notes)
    if leftovers:
        log("! possible unconverted syntax:")
        for item in leftovers[:12]:
            log(f"    {item}")
    log("done.")
    return 0


def pager_for(note: Note, notes: list[Note]):
    """prev / next within the same folder."""
    same = sorted_notes([n for n in notes if n.dir == note.dir and not n.is_index])
    if note not in same:
        return None, None
    i = same.index(note)
    prev_n = same[i + 1] if i + 1 < len(same) else None
    next_n = same[i - 1] if i > 0 else None
    return prev_n, next_n


def check_artifacts(out: Path, notes: list[Note]) -> list[str]:
    problems = []
    for n in notes:
        # ignore code blocks/spans: they legitimately contain **, [[, ``` etc.
        probe = re.sub(r"<pre[^>]*>.*?</pre>", "", n.html, flags=re.S)
        probe = re.sub(r"<code[^>]*>.*?</code>", "", probe, flags=re.S)
        if re.search(r"\*\*[^\s*<>][^*\n]{0,40}\*\*", probe):
            problems.append(f"{n.out}: 残留 ** 加粗")
        if "[[" in probe or "]]" in probe:
            problems.append(f"{n.out}: 残留 [[ ]]")
        if "```" in probe:
            problems.append(f"{n.out}: 残留 ``` 围栏")
        if re.search(r"(?m)^\s*>\s*\[!", probe):
            problems.append(f"{n.out}: 残留 callout 标记")
    return problems


def make_icons(assets: Path) -> None:
    try:
        from PIL import Image, ImageDraw
    except Exception:
        log("· pillow missing, skip icons")
        return

    def icon(size: int) -> "Image.Image":
        img = Image.new("RGBA", (size * 4, size * 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        s = size * 4
        r = int(s * 0.22)
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=r, fill=(255, 180, 84, 255))
        # three "text" bars: a slim notebook mark
        bar = int(s * 0.085)
        left = int(s * 0.26)
        widths = [0.42, 0.30, 0.36]
        top = int(s * 0.30)
        gap = int(s * 0.115)
        for i, w in enumerate(widths):
            y = top + i * gap
            d.rounded_rectangle(
                [left, y, left + int(s * w), y + bar],
                radius=bar // 2,
                fill=(20, 22, 26, 255),
            )
        return img.resize((size, size), Image.LANCZOS)

    for size, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
        icon(size).save(assets / name)
    try:
        icon(32).save(assets / "icon-32.png")
    except Exception:
        pass
    log("· icons generated")


if __name__ == "__main__":
    raise SystemExit(main())
