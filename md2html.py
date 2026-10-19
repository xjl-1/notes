"""
md2html.py — Obsidian flavoured Markdown -> HTML

Deliberately dependency-free: no `markdown`, no `mistune`. The vault uses a
small, well-known subset of Obsidian syntax, so a purpose-built parser gives us
exact control over the output (heading levels, wikilinks, callouts, dataview).

Block level : fenced code, headings, hr, tables, blockquotes/callouts,
              ordered/unordered lists (tab or space indented), paragraphs
Inline level: code spans, math, images, links, wikilinks, bold/italic/strike/
              highlight, autolinks, inline tags (only if tag is known)

Unresolved wikilinks are reported back to the caller instead of silently
producing dead links.
"""

from __future__ import annotations

import html
import re
from datetime import date

# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

CJK = r"\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef"
CJK_RE = re.compile(f"[{CJK}]")

HTML_ESC = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}


def esc(text: str) -> str:
    return "".join(HTML_ESC.get(c, c) for c in text)


def is_cjk(ch: str) -> bool:
    return bool(ch) and bool(CJK_RE.match(ch))


def smart_join(lines: list[str]) -> str:
    """Join soft-wrapped lines: no space across CJK boundaries, space otherwise."""
    out = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not out:
            out = line
            continue
        if is_cjk(out[-1]) or is_cjk(line[0]):
            out += line
        else:
            out += " " + line
    return out


SLUG_DROP = re.compile(r'[\\/:*?"<>|#%&{}^~`\[\]\x00-\x1f]')


def slugify(text: str, fallback: str = "section") -> str:
    s = re.sub(r"[\s\u3000]+", "-", text.strip())
    s = SLUG_DROP.sub("-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-.")
    return s or fallback


def text_of(fragment: str) -> str:
    """Strip html tags to plain text (used for search snippets / word count)."""
    t = re.sub(r"<[^>]+>", "", fragment)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


# --------------------------------------------------------------------------- #
# frontmatter
# --------------------------------------------------------------------------- #

FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", re.S)


def split_frontmatter(text: str):
    m = FM_RE.match(text)
    if not m:
        return {}, text, ""
    raw = m.group(1)
    meta: dict = {}
    key = None
    for line in raw.splitlines():
        if re.match(r"^\s*#", line) or not line.strip():
            continue
        item = re.match(r"^\s*-\s+(.*)$", line)
        if item and key:
            meta.setdefault(key, [])
            if isinstance(meta[key], list):
                meta[key].append(item.group(1).strip().strip("\"'"))
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                meta[key] = [
                    p.strip().strip("\"'") for p in re.split(r"[,\u3001]", inner) if p.strip()
                ]
            elif val == "":
                meta[key] = []  # may become a block list
            else:
                meta[key] = val.strip("\"'")
    # normalise: empty list that never got items -> drop
    for k, v in list(meta.items()):
        if isinstance(v, list) and not v:
            meta.pop(k)
    return meta, text[m.end():], raw


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [p.strip() for p in re.split(r"[,\u3001]", str(value)) if p.strip()]


# --------------------------------------------------------------------------- #
# inline renderer
# --------------------------------------------------------------------------- #

class Inline:
    """Renders inline markdown. `resolve` maps a wikilink target -> url|None."""

    PLACEHOLDER = "\x00{}\x00"
    PH_RE = re.compile(r"\x00(\d+)\x00")

    def __init__(self, resolve, known_tags: set[str], tag_url=None, image_map=None):
        self.resolve = resolve
        self.known_tags = known_tags
        self.tag_url = tag_url
        self.assets = image_map or {}

    def render(self, text: str) -> str:
        store: list[str] = []

        def keep(fragment: str) -> str:
            store.append(fragment)
            return self.PLACEHOLDER.format(len(store) - 1)

        # 1. protect code spans ------------------------------------------------
        def code_span(m):
            body = m.group(1).strip() if m.group(1).startswith(" ") else m.group(1)
            return keep(f"<code>{esc(body)}</code>")

        text = re.sub(r"`([^`\n]+)`", code_span, text)

        # 1b. backslash escapes — pandoc writes \* \` \[ for literal characters
        text = re.sub(
            r"\\([\\`*_{}\[\]()#+\-.!~=|$<>])",
            lambda m: keep(f"&#{ord(m.group(1))};"),
            text,
        )

        # 1c. inline HTML copied over from the vault ---------------------------
        # docx exports leave things like <mark style="background: #ADCCFFA6;">;
        # keep a small whitelist of tags but drop every attribute, so no stray
        # #colour ever reaches the tag parser.
        INLINE_TAG = re.compile(
            r"</?(mark|span|sup|sub|u|s|del|ins|kbd|small|b|i|em|strong|br)"
            r"(?:\s[^<>\n]{0,200})?/?>",
            re.IGNORECASE,
        )

        def inline_tag(m):
            name = m.group(1).lower()
            if m.group(0).startswith("</"):
                return keep(f"</{name}>")
            if name == "br":
                return keep("<br>")
            return keep(f"<{name}>")

        text = INLINE_TAG.sub(inline_tag, text)

        # 2. protect block/inline math ----------------------------------------
        def inline_math(m):
            body = m.group(1)
            if len(body) > 120:
                return m.group(0)
            if not (
                re.search(r"[\\^_{}=]", body)
                or re.fullmatch(r"[A-Za-z\\][A-Za-z0-9'′]*", body)
            ):
                return m.group(0)
            return keep(f'<span class="math-inline" data-tex="{esc(body)}"></span>')

        text = re.sub(r"(?<![\\$])\$(?!\$)([^\n$]{2,120}?)\$(?!\$)", inline_math, text)

        # 3. protect raw <br> --------------------------------------------------
        text = re.sub(r"<br\s*/?>", lambda m: keep("<br>"), text, flags=re.I)

        # 4. escape what is left ----------------------------------------------
        text = esc(text)

        # 5. images ------------------------------------------------------------
        def image(m):
            alt, src = html.unescape(m.group(1)), html.unescape(m.group(2).strip())
            src = self.assets.get(src, src)
            title = f' title="{esc(alt)}"' if alt else ""
            if not re.match(r"^(https?:)?//", src) and not src.startswith("data:"):
                src = re.sub(r"\s+", "%20", src)
            return keep(
                f'<img src="{esc(src)}" alt="{esc(alt)}"{title} loading="lazy" decoding="async">'
            )

        text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", image, text)

        # 6. markdown links ----------------------------------------------------
        def link(m):
            label, url = m.group(1), html.unescape(m.group(2).strip())
            external = bool(re.match(r"^https?:", url))
            attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
            return keep(f'<a href="{esc(url)}"{attrs}>{label}</a>')

        text = re.sub(r"\[([^\]\n]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", link, text)

        # 7. wikilinks ---------------------------------------------------------
        text = re.sub(
            r"\[\[\]\]", lambda m: keep('<code class="wl-raw">[[]]</code>'), text
        )

        def wikilink(m):
            inner = html.unescape(m.group(1))
            inner = inner.replace("\\|", "\x01")
            target, _, alias = inner.partition("|")
            target, _, anchor = target.partition("#")
            target = target.strip()
            anchor = anchor.strip()
            url = self.resolve(target) if target else None
            label = (alias or target or anchor).replace("\x01", "|").strip()
            label = re.sub(r"/index$", "", label) or label
            if url:
                href = url + ("#" + anchor if anchor else "")
                return keep(f'<a class="wl" href="{esc(href)}">{esc(label)}</a>')
            # unresolved: show the source syntax as a literal, so instructional
            # notes read correctly and broken links stay visible but quiet
            shown = "[[" + inner.replace("\x01", "|") + "]]"
            return keep(f'<code class="wl-raw" title="未找到笔记">{esc(shown)}</code>')

        text = re.sub(r"\[\[([^\[\]\n]+?)\]\]", wikilink, text)

        # 8. emphasis ----------------------------------------------------------
        # `<` / `>` are excluded from the payload so a malformed nest cannot
        # swallow markup produced by an earlier pass.
        text = re.sub(r"\*\*\*(?=\S)([^<>\n]+?)(?<=\S)[ \t]*\*\*\*", r"<strong><em>\1</em></strong>", text)
        text = re.sub(r"\*\*(?=\S)([^<>\n]+?)(?<=\S)[ \t]*\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![\w*])\*([^\s*<>\n][^*<>\n]*?)(?<=\S)\*(?![\w*])", r"<em>\1</em>", text)
        text = re.sub(r"(?<![\w_])__(?=\S)([^<>\n]+?)(?<=\S)[ \t]*__(?![\w_])", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![\w_])_([^_<>\n]+?)_(?![\w_])", r"<em>\1</em>", text)
        text = re.sub(r"~~(?=\S)([^<>\n]+?)(?<=\S)~~", r"<del>\1</del>", text)
        text = re.sub(r"==(?=\S)([^<>\n]+?)(?<=\S)==", r"<mark>\1</mark>", text)

        # stray markers left over from overlapping nests, e.g. "**a|*(b)***"
        text = re.sub(r"\*(?=</(?:strong|em|del|mark)>)", "", text)
        text = re.sub(r"(</(?:strong|em|del|mark)>)[ \t]*\*+(?![\w*])", r"\1", text)

        # any surviving ** is unpaired (a typo in the source). Drop it when it
        # sits next to CJK so notes read cleanly; keep it next to latin words,
        # where ** is pointer syntax (int** p).
        text = re.sub(r"\*\*(?=[\u4e00-\u9fa5])", "", text)
        text = re.sub(r"(?<=[\u4e00-\u9fa5])\*\*", "", text)

        # 9. autolinks (bare urls not already inside a tag) ---------------------
        def autolink(m):
            url = html.unescape(m.group(1)).rstrip(".,;:)]）")
            return keep(
                f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(url)}</a>'
            )

        text = re.sub(r"(?<![\"=>])(https?://[^\s<>\"）]+)", autolink, text)

        # 10. inline tags (only tags that actually exist in the vault) --------
        if self.known_tags and self.tag_url:
            def tag(m):
                raw = m.group(1)
                if raw not in self.known_tags:
                    return m.group(0)
                url = self.tag_url(raw)
                if not url:
                    return m.group(0)
                return keep(f'<a class="taglink" href="{esc(url)}">#{esc(raw)}</a>')

            text = re.sub(r"(?:^|(?<=\s))#([\w\u4e00-\u9fa5][\w\u4e00-\u9fa5/+-]*)", tag, text)

        # restore -------------------------------------------------------------
        for _ in range(3):  # nested placeholders
            def restore(m):
                idx = int(m.group(1))
                return store[idx] if idx < len(store) else m.group(0)

            new = self.PH_RE.sub(restore, text)
            if new == text:
                break
            text = new
        return text


# --------------------------------------------------------------------------- #
# block parser
# --------------------------------------------------------------------------- #

LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
FENCE_RE = re.compile(r"^\s*```\s*([\w+#.-]*)\s*$")
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
CALLOUT_RE = re.compile(r"^\s*\[!([\w-]+)\]([+-]?)\s*(.*)$")

CALLOUT_ICONS = {
    "note": "note", "info": "info", "tip": "tip", "hint": "tip", "important": "tip",
    "success": "tip", "check": "tip", "done": "tip", "warning": "warning",
    "caution": "warning", "attention": "warning", "danger": "danger", "error": "danger",
    "bug": "danger", "fail": "danger", "failure": "danger", "missing": "danger",
    "question": "info", "help": "info", "faq": "info", "quote": "quote", "cite": "quote",
    "example": "note", "abstract": "note", "summary": "note", "tldr": "note",
}


def indent_of(line: str) -> int:
    width = 0
    for ch in line:
        if ch == " ":
            width += 1
        elif ch == "\t":
            width += 4
        else:
            break
    return width


class BlockParser:
    def __init__(self, inline: Inline, heading_shift: int = 0, dataview=None):
        self.inline = inline
        self.shift = heading_shift
        self.dataview = dataview  # callable(folder_query) -> html string
        self.headings: list[dict] = []
        self.used_ids: dict[str, int] = {}
        self.flat_text: list[str] = []

    # -- public ------------------------------------------------------------
    def parse(self, lines: list[str]) -> str:
        return self._blocks(lines)

    def _id(self, text: str) -> str:
        base = slugify(text, "h")
        n = self.used_ids.get(base, 0)
        self.used_ids[base] = n + 1
        return base if n == 0 else f"{base}-{n}"

    def _heading(self, level: int, text: str) -> str:
        level = max(2, min(6, level + self.shift))
        plain = text_of(self.inline.render(text))
        hid = self._id(plain)
        if level <= 4:
            self.headings.append({"level": level, "text": plain, "id": hid})
        self.flat_text.append(plain)
        anchor = f'<a class="anchor" href="#{esc(hid)}" aria-hidden="true">#</a>'
        return f'<h{level} id="{esc(hid)}">{self.inline.render(text)}{anchor}</h{level}>'

    # -- blocks ------------------------------------------------------------
    def _blocks(self, lines: list[str]) -> str:
        out: list[str] = []
        i, n = 0, len(lines)
        while i < n:
            line = lines[i]
            if not line.strip():
                i += 1
                continue

            # fenced code
            fm = FENCE_RE.match(line)
            if fm:
                lang = fm.group(1)
                body: list[str] = []
                i += 1
                while i < n and not FENCE_RE.match(lines[i]):
                    body.append(lines[i])
                    i += 1
                i += 1  # closing fence
                if lang in ("dataview", "dataviewjs", "tasks") and self.dataview:
                    rendered = self.dataview("\n".join(body), lang)
                    out.append(rendered if rendered is not None else self._code("\n".join(body), lang))
                else:
                    out.append(self._code("\n".join(body), lang))
                continue

            # heading
            hm = HEAD_RE.match(line)
            if hm:
                out.append(self._heading(len(hm.group(1)), hm.group(2)))
                i += 1
                continue

            # horizontal rule
            if HR_RE.match(line):
                out.append("<hr>")
                i += 1
                continue

            # table
            if line.lstrip().startswith("|") and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]):
                html_table, i = self._table(lines, i)
                out.append(html_table)
                continue

            # blockquote / callout
            if line.lstrip().startswith(">"):
                block, i = self._quote(lines, i)
                out.append(block)
                continue

            # list
            if LIST_RE.match(line):
                block, i = self._list(lines, i)
                out.append(block)
                continue

            # math block
            if line.strip() == "$$":
                body: list[str] = []
                i += 1
                while i < n and lines[i].strip() != "$$":
                    body.append(lines[i])
                    i += 1
                i += 1
                tex = "\n".join(body).strip()
                out.append(f'<div class="math-block" data-tex="{esc(tex)}"></div>')
                continue

            # paragraph
            para: list[str] = []
            while i < n:
                cur = lines[i]
                if not cur.strip():
                    break
                if (
                    FENCE_RE.match(cur)
                    or HEAD_RE.match(cur)
                    or HR_RE.match(cur)
                    or cur.lstrip().startswith(">")
                    or LIST_RE.match(cur)
                    or (cur.lstrip().startswith("|") and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]))
                ):
                    break
                para.append(cur)
                i += 1
            self.flat_text.append(smart_join(para))
            out.append(f"<p>{self.inline.render(smart_join(para))}</p>")
        return "\n".join(out)

    def _code(self, body: str, lang: str) -> str:
        attr = f' data-lang="{esc(lang)}"' if lang else ""
        return f"<pre{attr}><code>{esc(body)}</code></pre>"

    def _table(self, lines: list[str], i: int):
        def cells(row: str) -> list[str]:
            row = row.strip()
            if row.startswith("|"):
                row = row[1:]
            if row.endswith("|"):
                row = row[:-1]
            row = row.replace("\\|", "\x01")
            return [c.replace("\x01", "|").strip() for c in row.split("|")]

        header = cells(lines[i])
        sep = cells(lines[i + 1])
        align = []
        for c in sep:
            c = c.strip()
            if c.startswith(":") and c.endswith(":"):
                align.append("center")
            elif c.endswith(":"):
                align.append("right")
            elif c.startswith(":"):
                align.append("left")
            else:
                align.append("")
        i += 2
        rows: list[list[str]] = []
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            rows.append(cells(lines[i]))
            i += 1

        def cell(tag, content, idx, is_head=False):
            a = align[idx] if idx < len(align) else ""
            style = f' style="text-align:{a}"' if a else ""
            return f"<{tag}{style}>{content}</{tag}>"

        head = "".join(cell("th", self.inline.render(c), k, True) for k, c in enumerate(header))
        body = ""
        for r in rows:
            padded = r + [""] * (len(header) - len(r))
            body += "<tr>" + "".join(
                cell("td", self.inline.render(c), k) for k, c in enumerate(padded[: len(header)])
            ) + "</tr>"
            self.flat_text.append(" ".join(text_of(self.inline.render(c)) for c in r))
        return (
            '<div class="tablewrap"><table><thead><tr>'
            + head
            + "</tr></thead><tbody>"
            + body
            + "</tbody></table></div>"
        ), i

    def _quote(self, lines: list[str], i: int):
        n = len(lines)
        raw: list[str] = []
        while i < n and lines[i].lstrip().startswith(">"):
            raw.append(re.sub(r"^\s*>\s?", "", lines[i]))
            i += 1

        cm = CALLOUT_RE.match(raw[0]) if raw else None
        if cm:
            kind = cm.group(1).lower()
            fold = cm.group(2)
            title = cm.group(3).strip() or kind.capitalize()
            inner = self._blocks(raw[1:])
            cls = f"callout callout--{CALLOUT_ICONS.get(kind, 'note')}"
            icon = f'<span class="callout__icon">{svg_icon(CALLOUT_ICONS.get(kind, "note"))}</span>'
            if fold:
                return (
                    f'<details class="{cls}"><summary><div class="callout__head">{icon}'
                    f"{self.inline.render(title)}</div></summary>"
                    f'<div class="callout__body">{inner}</div></details>'
                ), i
            return (
                f'<div class="{cls}"><div class="callout__head">{icon}'
                f'{self.inline.render(title)}</div><div class="callout__body">{inner}</div></div>'
            ), i

        return f"<blockquote>{self._blocks(raw)}</blockquote>", i

    def _list(self, lines: list[str], i: int):
        """Indentation based list parser producing nested <ul>/<ol>."""
        n = len(lines)
        root: list[dict] = []
        stack: list[dict] = []  # each: {"indent", "tag", "items"}

        def new_ul(tag: str, indent: int) -> dict:
            node = {"indent": indent, "tag": tag, "items": []}
            if stack:
                stack[-1]["items"][-1]["children"].append(node)
            else:
                root.append(node)
            return node

        while i < n:
            line = lines[i]
            if not line.strip():
                # blank: look ahead for continuation of the current item
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                if j >= n:
                    break
                if stack and indent_of(lines[j]) > stack[-1]["indent"] and not LIST_RE.match(lines[j]):
                    stack[-1]["items"][-1]["extra"].append("")
                    i = j
                    continue
                break

            m = LIST_RE.match(line)
            if m:
                indent = indent_of(line)
                marker = m.group(2)
                tag = "ol" if marker[0].isdigit() else "ul"
                content = m.group(3)

                while stack and indent < stack[-1]["indent"]:
                    stack.pop()
                if not stack or indent > stack[-1]["indent"]:
                    node = new_ul(tag, indent)
                    stack.append(node)
                else:
                    node = stack[-1]
                    if node["tag"] != tag and not node["items"]:
                        node["tag"] = tag

                check = re.match(r"^\[([ xX])\]\s*(.*)$", content)
                checked = None
                if check:
                    checked = check.group(1).lower() == "x"
                    content = check.group(2)

                node["items"].append(
                    {"text": [content], "checked": checked, "children": [], "extra": []}
                )
                i += 1
                continue

            # continuation line inside a list
            if stack and indent_of(line) > stack[-1]["indent"]:
                stack[-1]["items"][-1]["text"].append(line.strip())
                i += 1
                continue
            break

        def render_nodes(nodes: list[dict]) -> str:
            html_out = []
            for node in nodes:
                items = []
                for item in node["items"]:
                    parts: list[str] = []
                    text = smart_join(item["text"])
                    prefix = ""
                    if item["checked"] is not None:
                        prefix = (
                            '<input type="checkbox" disabled'
                            + (" checked" if item["checked"] else "")
                            + "> "
                        )
                    if text:
                        parts.append(prefix + self.inline.render(text))
                        self.flat_text.append(text)
                    for extra in item["extra"]:
                        if extra.strip():
                            parts.append(self._blocks([extra]))
                    if item["children"]:
                        parts.append(render_nodes(item["children"]))
                    items.append("<li>" + "".join(parts) + "</li>")
                html_out.append(f"<{node['tag']}>" + "".join(items) + f"</{node['tag']}>")
            return "".join(html_out)

        return render_nodes(root), i


# --------------------------------------------------------------------------- #
# svg icons used by callouts
# --------------------------------------------------------------------------- #

ICONS = {
    "note": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 4h9l5 5v11H5z" stroke-linejoin="round"/><path d="M14 4v5h5"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.6v.1" stroke-linecap="round"/></svg>',
    "tip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 17h6M10 20h4" stroke-linecap="round"/><path d="M12 3.5a5.5 5.5 0 0 0-3.2 9.9c.5.4.7.9.7 1.5V15h5v-.1c0-.6.2-1.1.7-1.5A5.5 5.5 0 0 0 12 3.5z" stroke-linejoin="round"/></svg>',
    "warning": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 4l8.5 15h-17z"/><path d="M12 9.5v4.2M12 16.7v.1" stroke-linecap="round"/></svg>',
    "danger": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M6.5 6.5l11 11"/></svg>',
    "quote": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M9 7H5.5v5H9c0 3-1.5 4.5-3.5 5M19 7h-3.5v5H19c0 3-1.5 4.5-3.5 5"/></svg>',
}


def svg_icon(name: str) -> str:
    return ICONS.get(name, ICONS["note"])


# --------------------------------------------------------------------------- #
# document
# --------------------------------------------------------------------------- #

def convert(text: str, inline: Inline, dataview=None, min_heading_shift=True):
    """Return dict(html, headings, words, plain, title_guess)."""
    meta, body, _ = split_frontmatter(text)

    headings = [
        len(m.group(1))
        for m in re.finditer(
            r"(?m)^(#{1,6})\s+\S",
            re.sub(r"(?ms)^[ \t]*(```|~~~).*?^[ \t]*\1[^\n]*$", "", body),
        )
    ]
    shift = 0
    if min_heading_shift and headings:
        # body h1 would clash with the page title h1; a body whose shallowest
        # heading is h3 gets promoted so the outline has no gap under the title
        shift = 2 - min(headings)

    parser = BlockParser(inline, heading_shift=shift, dataview=dataview)
    html_out = parser.parse(body.replace("\r\n", "\n").split("\n"))
    # a bare "- " line in the source leaves an empty bullet; drop those
    html_out = html_out.replace("<li><p></p></li>", "").replace("<li></li>", "")
    html_out = re.sub(r"<ul>\s*</ul>|<ol>\s*</ol>", "", html_out)

    plain = "\n".join(parser.flat_text)
    words = len(re.findall(r"[\u4e00-\u9fff]", plain)) + len(re.findall(r"[A-Za-z0-9_+#]+", plain))
    return {
        "meta": meta,
        "html": html_out,
        "headings": parser.headings,
        "plain": plain,
        "words": words,
    }
