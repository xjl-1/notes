"""docx2md.py — turn Word ``.docx`` files into markdown for the site build.

Two backends:

1. **pandoc** (preferred) — full fidelity: headings, lists, tables, footnotes,
   images (extracted next to the markdown).
2. **python-docx** (fallback) — a small, predictable subset: headings, lists,
   paragraphs, tables, inline images.  Good enough for ordinary notes.

The public entry point is :func:`docx_to_markdown`, which caches the result by
content hash so repeated builds are cheap.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from pathlib import Path

# --------------------------------------------------------------------------- #
# pandoc discovery
# --------------------------------------------------------------------------- #

_PANDOC: object = None  # sentinel: None = not looked up yet, False = missing

CANDIDATES = [
    r"C:\Program Files\Pandoc\pandoc.exe",
    r"C:\Program Files (x86)\Pandoc\pandoc.exe",
    "/usr/bin/pandoc",
    "/usr/local/bin/pandoc",
    "/opt/homebrew/bin/pandoc",
]


def find_pandoc() -> str | None:
    global _PANDOC
    if _PANDOC is None:
        found = shutil.which("pandoc")
        if not found:
            found = next((c for c in CANDIDATES if Path(c).exists()), None)
        _PANDOC = found or False
    return _PANDOC if isinstance(_PANDOC, str) else None  # type: ignore[return-value]


# --------------------------------------------------------------------------- #
# markdown clean-up after pandoc
# --------------------------------------------------------------------------- #

_IMG_RE = re.compile(r"<img\b[^>]*?src=\"([^\"]+)\"[^>]*>", re.I)
_TAG_RE = re.compile(
    r"</?(?:span|sup|sub|u|s|em|strong|mark|div|p|br|o:p|w:[a-z]+)\b[^>]*>", re.I
)


def _tidy(text: str) -> str:
    """Replace pandoc's raw HTML images / leftover inline tags with markdown."""
    text = _IMG_RE.sub(lambda m: f"\n![]({m.group(1)})\n", text)
    text = _TAG_RE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


# --------------------------------------------------------------------------- #
# backend 1: pandoc
# --------------------------------------------------------------------------- #

def _pandoc_convert(src: Path, dest: Path) -> str:
    exe = find_pandoc()
    if not exe:
        raise RuntimeError("pandoc not found")
    md = dest / "note.md"
    cmd = [
        exe, str(src),
        "-f", "docx",
        "-t", "gfm+pipe_tables",
        "--wrap=none",
        "--extract-media=media",
        "-o", str(md),
    ]
    proc = subprocess.run(
        cmd, cwd=str(dest), capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=120,
    )
    if proc.returncode != 0 or not md.exists():
        tail = (proc.stderr or "pandoc failed").strip().splitlines()
        raise RuntimeError(tail[-1][:300] if tail else "pandoc failed")
    return md.read_text(encoding="utf-8", errors="replace")


# --------------------------------------------------------------------------- #
# backend 2: python-docx
# --------------------------------------------------------------------------- #

_HEADING_STYLE = re.compile(r"^(?:heading|标题)\s*(\d)$", re.I)
_LIST_STYLE = re.compile(r"^(?:list\s*(?:bullet|number)|列表段落|列表)", re.I)


def _iter_block_items(doc):
    """Yield paragraphs and tables in document order."""
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    body = doc.element.body
    for child in body.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, doc)
        elif child.tag.endswith("}tbl"):
            yield Table(child, doc)


def _save_inline_images(para, media_dir: Path, counter: list[int]) -> list[str]:
    """Extract `a:blip` images referenced by a paragraph, return markdown lines."""
    out: list[str] = []
    xml = para._p.xml
    for rid in re.findall(r'r:embed="(rId\d+)"', xml):
        try:
            part = para.part.related_parts[rid]
        except KeyError:
            continue
        blob = getattr(part, "blob", None)
        if not blob:
            continue
        ext = Path(str(part.partname)).suffix or ".png"
        counter[0] += 1
        name = f"image{counter[0]}{ext}"
        media_dir.mkdir(parents=True, exist_ok=True)
        (media_dir / name).write_bytes(blob)
        out.append(f"![]({media_dir.name}/{name})")
    return out


def _table_to_md(table) -> str:
    rows: list[list[str]] = []
    for row in table.rows:
        cells = [re.sub(r"\s+", " ", c.text).strip().replace("|", "\\|") for c in row.cells]
        rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    head = "| " + " | ".join(rows[0]) + " |"
    sep = "|" + "|".join([" --- "] * width) + "|"
    body = ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join([head, sep, *body])


def _python_docx_convert(src: Path, dest: Path) -> str:
    from docx import Document

    doc = Document(str(src))
    media_dir = dest / "media"
    counter = [0]
    lines: list[str] = []

    for block in _iter_block_items(doc):
        if hasattr(block, "rows"):
            md = _table_to_md(block)
            if md:
                lines += ["", md, ""]
            continue

        para = block
        text = re.sub(r"[ \t]+", " ", para.text).strip()
        images = _save_inline_images(para, media_dir, counter)
        style = (para.style.name or "") if para.style is not None else ""

        if not text and not images:
            continue
        if images:
            lines += ["", *images, ""]
            if not text:
                continue

        m = _HEADING_STYLE.match(style)
        if m:
            level = min(6, max(1, int(m.group(1))))
            lines += ["", "#" * level + " " + text, ""]
        elif _LIST_STYLE.match(style):
            bullet = "1. " if "number" in style.lower() else "- "
            lines.append(bullet + text)
        else:
            lines += ["", text, ""]

    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# public API
# --------------------------------------------------------------------------- #

def docx_to_markdown(src: Path, cache_root: Path) -> tuple[str, Path]:
    """Convert *src* to markdown, caching under *cache_root*.

    Returns ``(markdown_text, media_dir)`` where *media_dir* is the directory
    the markdown's relative image paths are resolved against.
    """
    digest = hashlib.sha1(src.read_bytes()).hexdigest()[:16]
    dest = cache_root / digest
    md_file = dest / "note.md"

    if md_file.exists():
        return md_file.read_text(encoding="utf-8", errors="replace"), dest

    dest.mkdir(parents=True, exist_ok=True)
    text: str | None = None
    if find_pandoc():
        try:
            text = _pandoc_convert(src, dest)
        except Exception:
            text = None
    if text is None:
        text = _python_docx_convert(src, dest)

    text = _tidy(text)
    md_file.write_text(text, encoding="utf-8", newline="\n")
    return text, dest
