"""
publish.py — sync the local vault into GitHub and let Actions build the site.

The repo holds **sources**, not the built site:

    vault/          the notes (md / txt / docx + images)
    assets/         css + js, copied into the build
    build.py        the generator (same file you run locally)
    .github/…       the workflow that builds + deploys on every push

So editing a note on github.com (or in the site's editor) rebuilds the site
automatically — no commands needed. This script is only for pushing the local
folder in one shot, and for pulling back edits made elsewhere.

Usage
    python publish.py                 # mirror D:\\Notes → vault/, push
    python publish.py --dry           # show what would change
    python publish.py --check         # validate token / repo only
    python publish.py --pull          # download the repo's vault → local + E:\\
    python publish.py --from "D:\\notes"   # mirror a different folder

No git, no gh: everything goes through the REST API.
The token (Classic PAT, `repo` scope) comes from --token, GH_TOKEN,
GITHUB_TOKEN, or a `.token` file next to this script.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import http.client
import json
import os
import random
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = HERE / "vault"
DEFAULT_SOURCE = Path(r"D:\Notes")

API = "https://api.github.com"
OWNER = "xjl-1"
REPO = "notes"
BRANCH = "main"
DESCRIPTION = "个人笔记站：编程、金融、通识、办公软件与英语学习"
HOMEPAGE = f"https://{OWNER}.github.io/{REPO}/"
PAGES_URL = "https://xjl-1.github.io/notes"

UA = "notes-site-publisher/2.0"

# what goes into the repo
TOP_FILES = {"build.py", "md2html.py", "docx2md.py", "publish.py", ".gitignore", "README.md"}
TOP_DIRS = ("vault", "assets", ".github")

# what never does
SKIP_DIRS = {
    "site", ".cache", ".tmp", "__pycache__", ".git", ".backup", ".sync-state.json",
    ".obsidian", ".claude", ".trash", "node_modules", "模板", ".github/workflows/__pycache__",
}
SKIP_FILES = {".token", ".DS_Store", "Thumbs.db", ".sync-state.json"}

# note source formats + assets that go with them
NOTE_SUFFIXES = {".md", ".markdown", ".txt", ".docx", ".doc"}
MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif"}


def log(msg: str) -> None:
    print(msg, flush=True)


# --------------------------------------------------------------------------- #
# http
# --------------------------------------------------------------------------- #

def request(
    method: str,
    path: str,
    token: str,
    payload=None,
    *,
    ok=(200, 201, 204),
    timeout: int = 60,
):
    url = path if path.startswith("http") else API + path
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    last: Exception | None = None
    for attempt in range(6):
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", UA)
        if data:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                status = resp.status
            break
        except urllib.error.HTTPError as exc:
            body = exc.read()
            status = exc.code
            if status in ok:
                break
            if status in (502, 503, 504) and attempt < 5:
                last = RuntimeError(f"{method} {path} -> {status}")
                time.sleep(1.5 * (attempt + 1))
                continue
            detail = body.decode("utf-8", "replace")[:500]
            raise RuntimeError(f"{method} {path} -> {status}: {detail}") from None
        except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
            # OSError covers ssl.SSLError / RemoteDisconnected / resets, which this
            # TLS stack produces when requests bunch up
            last = exc
            if attempt < 5:
                time.sleep(1.2 * (attempt + 1) + random.random())
                continue
            reason = getattr(exc, "reason", exc)
            raise RuntimeError(f"{method} {path} -> network error: {reason}") from None
    else:
        raise RuntimeError(f"{method} {path} -> giving up: {last}")

    if not body:
        return status, None
    try:
        return status, json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        return status, body.decode("utf-8", "replace")


# --------------------------------------------------------------------------- #
# local files
# --------------------------------------------------------------------------- #

def blob_sha(data: bytes) -> str:
    """Git's own blob id: sha1('blob <len>\\0' + data)."""
    header = b"blob %d\0" % len(data)
    return hashlib.sha1(header + data).hexdigest()


def _skip(rel: str) -> bool:
    parts = rel.split("/")
    if any(p in SKIP_DIRS or p.startswith(".") and p not in {".github", ".gitignore"} for p in parts[:-1]):
        return True
    name = parts[-1]
    return name in SKIP_FILES


def mirror_vault(source: Path) -> None:
    """Copy notes + media from *source* into ./vault, deleting stale files."""
    if not source.exists():
        raise SystemExit(f"! source vault not found: {source}")
    want: dict[str, Path] = {}
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(source).as_posix()
        parts = rel.split("/")
        if any(p in SKIP_DIRS or (p.startswith(".") and p != ".github") for p in parts[:-1]):
            continue
        name = parts[-1]
        if name.startswith(".") or name.startswith("~$") or name.lower() in SKIP_FILES:
            continue
        suffix = path.suffix.lower()
        if suffix not in NOTE_SUFFIXES and suffix not in MEDIA_SUFFIXES:
            continue
        want[rel] = path

    VAULT.mkdir(parents=True, exist_ok=True)
    added = updated = 0
    for rel, src in want.items():
        dest = VAULT / rel
        old = dest.read_bytes() if dest.exists() else None
        data = src.read_bytes()
        if old == data:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        added += old is None
        updated += old is not None

    removed = 0
    for path in sorted(VAULT.rglob("*"), reverse=True):
        rel = path.relative_to(VAULT).as_posix()
        if path.is_file() and rel not in want:
            path.unlink()
            removed += 1
        elif path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    log(f"· mirrored {source} → vault/: +{added} new, ~{updated} changed, -{removed} removed")


def collect() -> list[tuple[str, Path, str]]:
    files: list[tuple[str, Path, str]] = []
    for name in TOP_FILES:
        path = HERE / name
        if path.is_file():
            files.append((name, path, blob_sha(path.read_bytes())))
    for top in TOP_DIRS:
        base = HERE / top
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(HERE).as_posix()
            if _skip(rel):
                continue
            files.append((rel, path, blob_sha(path.read_bytes())))
    if not any(rel.endswith((".md", ".txt", ".docx")) for rel, _, _ in files):
        raise SystemExit("! no notes found under ./vault — nothing to publish")
    return files


# --------------------------------------------------------------------------- #
# repository plumbing
# --------------------------------------------------------------------------- #

def ensure_repo(token: str) -> dict:
    status, repo = request("GET", f"/repos/{OWNER}/{REPO}", token, ok=(200, 404))
    if status == 200:
        return repo
    log(f"· creating repo {OWNER}/{REPO}")
    _, repo = request(
        "POST",
        "/user/repos",
        token,
        {
            "name": REPO,
            "description": DESCRIPTION,
            "homepage": HOMEPAGE,
            "private": False,
            "has_issues": False,
            "has_wiki": False,
            "has_projects": False,
            "auto_init": False,
        },
    )
    return repo


def remote_tree(token: str) -> dict[str, str]:
    """path -> blob sha for the current branch head (empty repo -> {})."""
    status, data = request(
        "GET", f"/repos/{OWNER}/{REPO}/git/trees/{BRANCH}?recursive=1", token, ok=(200, 404, 409)
    )
    if status != 200 or not isinstance(data, dict):
        return {}
    return {
        item["path"]: item["sha"]
        for item in data.get("tree", [])
        if item.get("type") == "blob"
    }


def head_sha(token: str, branch: str = BRANCH) -> str | None:
    status, data = request(
        "GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{branch}", token, ok=(200, 404, 409)
    )
    if status != 200 or not isinstance(data, dict):
        return None
    return data.get("object", {}).get("sha")


def upload_blobs(token: str, jobs: list[tuple[str, Path]]) -> dict[str, str]:
    """Upload changed files in parallel; returns path -> sha."""
    done: dict[str, str] = {}
    total = len(jobs)
    if not jobs:
        return done

    def one(item: tuple[str, Path]) -> tuple[str, str]:
        rel, path = item
        time.sleep(0.05)
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        _, res = request(
            "POST", f"/repos/{OWNER}/{REPO}/git/blobs", token,
            {"content": data, "encoding": "base64"},
        )
        return rel, res["sha"]

    with ThreadPoolExecutor(max_workers=2) as pool:
        for i, (rel, sha) in enumerate(pool.map(one, jobs), 1):
            done[rel] = sha
            if i % 25 == 0 or i == total:
                log(f"  uploaded {i}/{total} blobs")
    return done


def download_blobs(token: str, jobs: list[tuple[str, str]]) -> dict[str, bytes]:
    """Download blobs by sha; returns path -> bytes."""
    out: dict[str, bytes] = {}

    def one(item: tuple[str, str]) -> tuple[str, bytes]:
        rel, sha = item
        time.sleep(0.05)
        _, res = request("GET", f"/repos/{OWNER}/{REPO}/git/blobs/{sha}", token)
        return rel, base64.b64decode(res["content"])

    if not jobs:
        return out
    with ThreadPoolExecutor(max_workers=2) as pool:
        for rel, data in pool.map(one, jobs):
            out[rel] = data
    return out


def bootstrap_empty_repo(token: str) -> None:
    """A repo with no commits rejects git/blobs with 409, so lay down one commit
    through the Contents API first; the real tree lands on top of it."""
    log("· empty repo: seeding an initial commit")
    payload = {
        "message": "初始化笔记仓库",
        "content": base64.b64encode(b"").decode("ascii"),
        "branch": BRANCH,
    }
    request("PUT", f"/repos/{OWNER}/{REPO}/contents/.nojekyll", token, payload, ok=(200, 201, 409))
    log("  seeded")


# --------------------------------------------------------------------------- #
# pull
# --------------------------------------------------------------------------- #

def pull(token: str, source: Path) -> int:
    tree = remote_tree(token)
    wanted = {p: s for p, s in tree.items() if p.startswith("vault/")}
    if not wanted:
        log("! remote has no vault/ folder yet")
        return 1
    log(f"· downloading {len(wanted)} files from {OWNER}/{REPO}")
    data = download_blobs(token, list(wanted.items()))

    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = HERE / ".backup" / stamp
    wrote = 0
    for rel, blob in data.items():
        local_rel = rel[len("vault/"):]
        for base in (VAULT, source):
            if base is None:
                continue
            dest = base / local_rel
            if dest.exists() and dest.read_bytes() == blob:
                continue
            if dest.exists():
                keep = backup / base.name / local_rel
                keep.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dest, keep)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(blob)
            wrote += 1
    log(f"· wrote {wrote} files (overwrites backed up in {backup})")

    # drop files that exist locally but were deleted on the repo side
    known = {rel[len("vault/"):] for rel in data}
    for base in (VAULT, source):
        if not base.exists():
            continue
        for path in sorted(base.rglob("*"), reverse=True):
            if not path.is_file():
                continue
            rel = path.relative_to(base).as_posix()
            if any(p in SKIP_DIRS for p in rel.split("/")[:-1]):
                continue
            if path.suffix.lower() not in NOTE_SUFFIXES | MEDIA_SUFFIXES:
                continue
            if rel not in known:
                keep = backup / base.name / rel
                keep.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, keep)
                path.unlink()
                log(f"  - removed {rel}")
    log("· pulled. run `python build.py` to preview, or push with no flags.")
    return 0


# --------------------------------------------------------------------------- #
# pages
# --------------------------------------------------------------------------- #

def ensure_pages_actions(token: str) -> None:
    """Make Pages build from the workflow instead of the branch."""
    status, pages = request("GET", f"/repos/{OWNER}/{REPO}/pages", token, ok=(200, 404, 409))
    if status != 200:
        log("· enabling GitHub Pages (workflow builds)")
        try:
            request(
                "POST", f"/repos/{OWNER}/{REPO}/pages", token,
                {"build_type": "workflow"}, ok=(201, 409, 422),
            )
        except RuntimeError as exc:
            log(f"! could not enable Pages automatically: {exc}")
        return
    if pages.get("build_type") == "workflow":
        log(f"· Pages already on (workflow): {pages.get('html_url', HOMEPAGE)}")
        return
    log("· switching Pages to build from Actions")
    try:
        request(
            "PUT", f"/repos/{OWNER}/{REPO}/pages", token,
            {"build_type": "workflow", "source": {"branch": BRANCH, "path": "/"}},
            ok=(200, 204, 409, 422),
        )
    except RuntimeError as exc:
        log(f"! could not switch Pages build type: {exc}")


def watch_run(token: str, commit: str, tries: int = 40) -> None:
    """Print the workflow run that corresponds to *commit*."""
    seen = False
    for _ in range(tries):
        time.sleep(6)
        status, data = request(
            "GET", f"/repos/{OWNER}/{REPO}/actions/runs?branch={BRANCH}&per_page=8", token,
            ok=(200, 404, 403),
        )
        if status != 200 or not isinstance(data, dict):
            return
        run = next(
            (r for r in data.get("workflow_runs", []) if r.get("head_sha") == commit), None
        )
        if run is None:
            continue
        seen = True
        state = run.get("status")
        if state == "completed":
            conclusion = run.get("conclusion")
            log(f"  workflow: {conclusion}")
            if conclusion == "success":
                log(f"· live at {PAGES_URL}/")
            else:
                log(f"! build failed — see {run.get('html_url')}")
            return
        log(f"  workflow: {state}")
    if not seen:
        log("! no workflow run found yet (Actions may be busy or degraded)")


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description="sync notes + sources to GitHub Pages")
    ap.add_argument("--token", default=None)
    ap.add_argument("--from", dest="source", default=str(DEFAULT_SOURCE),
                    help="folder to mirror into ./vault (default: D:\\Notes)")
    ap.add_argument("--check", action="store_true", help="validate token and repo only")
    ap.add_argument("--dry", action="store_true", help="report changes without pushing")
    ap.add_argument("--pull", action="store_true", help="download the repo's vault/ to local")
    ap.add_argument("--no-sync", action="store_true", help="push ./vault as-is")
    ap.add_argument("--message", default="")
    args = ap.parse_args()

    token = args.token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        token_file = HERE / ".token"
        if token_file.exists():
            token = token_file.read_text(encoding="utf-8").strip()
    if not token:
        log("! no token: pass --token, set GH_TOKEN, or write it to .token")
        return 2

    log("· verifying token")
    try:
        _, me = request("GET", "/user", token)
    except RuntimeError as exc:
        log(f"! {exc}")
        return 1
    log(f"  authenticated as {me.get('login', '?')}")

    repo = ensure_repo(token)
    branch = repo.get("default_branch") or BRANCH

    source = Path(args.source)
    if args.pull:
        return pull(token, source if source.exists() else None)

    if not args.no_sync:
        mirror_vault(source)

    files = collect()
    log(f"· {len(files)} files to publish, {sum(p.stat().st_size for _, p, _ in files) / 1024:.0f} KB")

    old = remote_tree(token)
    changed = [(rel, path) for rel, path, sha in files if old.get(rel) != sha]
    removed = sorted(set(old) - {rel for rel, _, _ in files})
    log(f"· {len(changed)} changed, {len(files) - len(changed)} unchanged, {len(removed)} removed")

    # warn about notes that also changed upstream (e.g. edited from a phone)
    state_file = HERE / ".sync-state.json"
    state = {}
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            state = {}
    if state:
        drifted = [
            rel for rel, path, sha in files
            if rel.startswith("vault/") and old.get(rel) and old.get(rel) not in (sha, state.get(rel))
        ]
        if drifted:
            log(f"! {len(drifted)} note(s) changed both here and on GitHub — local wins:")
            for rel in drifted[:8]:
                log(f"    {rel}")
            log("    run `python publish.py --pull` first if the remote version is the newer one")

    if args.check or args.dry:
        for rel, _ in changed[:20]:
            log(f"    + {rel}")
        for rel in removed[:20]:
            log(f"    - {rel}")
        log("dry run — nothing was pushed")
        return 0

    if not head_sha(token):
        bootstrap_empty_repo(token)

    uploaded = upload_blobs(token, changed)
    parent = head_sha(token)
    message = args.message or time.strftime("更新笔记 %Y-%m-%d %H:%M")

    # Build on top of the existing tree instead of replacing it wholesale: files we
    # did not touch (notably .github/workflows/*, which a repo-scoped token may not
    # rewrite) are inherited untouched, and deletions become explicit sha=null entries.
    if parent:
        _, head_commit = request("GET", f"/repos/{OWNER}/{REPO}/git/commits/{parent}", token)
        entries = [
            {"path": rel, "mode": "100644", "type": "blob", "sha": uploaded[rel]}
            for rel, _ in changed
        ]
        entries += [
            {"path": rel, "mode": "100644", "type": "blob", "sha": None} for rel in removed
        ]
        tree_payload = {"base_tree": head_commit["tree"]["sha"], "tree": entries}
    else:
        entries = [
            {"path": rel, "mode": "100644", "type": "blob", "sha": uploaded.get(rel, sha)}
            for rel, _, sha in files
        ]
        tree_payload = {"tree": entries}

    log("· creating tree")
    _, tree = request("POST", f"/repos/{OWNER}/{REPO}/git/trees", token, tree_payload)
    log("· creating commit")
    commit_payload = {"message": message, "tree": tree["sha"]}
    if parent:
        commit_payload["parents"] = [parent]
    _, commit = request("POST", f"/repos/{OWNER}/{REPO}/git/commits", token, commit_payload)

    if parent:
        request("PATCH", f"/repos/{OWNER}/{REPO}/git/refs/heads/{branch}", token,
                {"sha": commit["sha"], "force": False})
    else:
        request("POST", f"/repos/{OWNER}/{REPO}/git/refs", token,
                {"ref": f"refs/heads/{branch}", "sha": commit["sha"]})
    log(f"· pushed {commit['sha'][:9]} ({len(changed)} files updated, {len(removed)} removed)")

    state_file.write_text(
        json.dumps({rel: sha for rel, _, sha in files}, ensure_ascii=False), encoding="utf-8"
    )

    ensure_pages_actions(token)
    watch_run(token, commit["sha"])

    log("done.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except RuntimeError as exc:
        log(f"! {exc}")
        sys.exit(1)
