#!/usr/bin/env python3
"""Fetch remote repository directories via uithub and save them as NotebookLM
source bundle files.

Supports two bundle config formats:

  Format A — URL per bundle (recommended)
  ----------------------------------------
  Each bundle value is a URL string. The URL is fetched directly and the
  response body is saved as `<key>.md` in the output directory.
  Use this when the uithub URL already scopes to the desired directory.

    {
      "bundles": {
        "01_requirements": "https://uithub.com/owner/repo/tree/master/01_requirements?maxTokens=10000000",
        "02_basic_design":  "https://uithub.com/owner/repo/tree/master/02_basic_design?maxTokens=10000000",
        "03_detail_design": "https://uithub.com/owner/repo/tree/master/03_detail_design?maxTokens=10000000"
      }
    }

  Format B — single URL + glob split (legacy)
  --------------------------------------------
  Each bundle value is a list of glob patterns. Requires --url for the
  whole-repo plain-text dump which is split by the glob patterns.

    {
      "bundles": {
        "requirements": ["01_requirements/**/*.md"],
        "apis":         ["02_basic_design/02_backend/03_apis/**/*.md"]
      }
    }

Usage
-----
  # Format A (URL per bundle) — just specify --config and --out
  python3 fetch_and_bundle.py \\n      --config remote-bundles.json --out _nlm/bundles

  # Format B (glob split) — also specify --url for the whole-repo dump
  python3 fetch_and_bundle.py \\n      --url "https://uithub.com/owner/repo?maxTokens=10000000&accept=text%2Fplain" \\n      --config glob-bundles.json --out _nlm/bundles

  # Common options
  --token TOKEN   Bearer token for uithub auth (or set UITHUB_TOKEN env var)
  --cache FILE    Cache the raw fetch to FILE; reuse on next run

Authentication
--------------
  export UITHUB_TOKEN="your-uithub-session-token"
  The token is sent as: Authorization: Bearer <token>
"""
import os, re, sys, json, fnmatch, argparse
from pathlib import Path
from urllib.request import Request, urlopen
from typing import Optional
from urllib.error import HTTPError, URLError


# ---------------------------------------------------------------------------
# HTTP fetch
# ---------------------------------------------------------------------------

def _fetch(url: str, token: Optional[str]) -> str:
    """Fetch a URL and return the response body as text."""
    # Append accept=text/plain if not already present
    sep = "&" if "?" in url else "?"
    if "accept=" not in url:
        url = url + sep + "accept=text%2Fplain"

    headers = {"Accept": "text/plain", "User-Agent": "Mozilla/5.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=120) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except HTTPError as e:
        sys.exit(
            f"HTTP {e.code} fetching {url}\n"
            f"  401: set UITHUB_TOKEN or pass --token\n"
            f"  403: check repo visibility / token scope"
        )
    except URLError as e:
        sys.exit(f"Network error fetching {url}: {e.reason}")


# ---------------------------------------------------------------------------
# Format A: URL-per-bundle mode
# ---------------------------------------------------------------------------

def fetch_url_bundles(
    bundles_cfg: dict[str, str],
    token: Optional[str],
    out_dir: str,
    cache_dir: Optional[str],
) -> None:
    """Fetch each URL and save as <key>.md in out_dir."""
    os.makedirs(out_dir, exist_ok=True)
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)

    for key, url in bundles_cfg.items():
        cache_path = os.path.join(cache_dir, f"{key}.txt") if cache_dir else None

        if cache_path and os.path.exists(cache_path):
            print(f"[{key}] using cache: {cache_path}")
            text = open(cache_path, encoding="utf-8").read()
        else:
            print(f"[{key}] fetching {url} ...")
            text = _fetch(url, token)
            b = len(text.encode())
            print(f"[{key}] fetched {b:,} chars (~{b//6:,} words)")
            if cache_path:
                open(cache_path, "w", encoding="utf-8").write(text)

        out_path = os.path.join(out_dir, f"{key}.md")
        open(out_path, "w", encoding="utf-8").write(text)
        b = len(text.encode())
        print(f"[{key}] saved -> {out_path}  bytes={b:,} (~{b//6:,} words)")
        if b // 6 > 480_000:
            print(f"  WARNING: {key} approaches NotebookLM ~500k words/source limit.")


# ---------------------------------------------------------------------------
# Format B: glob-split mode (legacy)
# ---------------------------------------------------------------------------

def _detect_and_split(text: str) -> dict[str, str]:
    _SEP_PATTERNS = [
        re.compile(r"^={4,}\s*File:\s*(.+?)\s*={4,}$", re.MULTILINE),
        re.compile(r"^-{4,}\s*(.+?)\s*-{4,}$", re.MULTILINE),
        re.compile(r"^={5}\s*(.+?)\s*={5}$", re.MULTILINE),
        re.compile(r"^(?:File|file|PATH|path):\s*(.+)$", re.MULTILINE),
    ]
    for pat in _SEP_PATTERNS:
        matches = list(pat.finditer(text))
        if len(matches) >= 2:
            files: dict[str, str] = {}
            for i, m in enumerate(matches):
                path = m.group(1).strip()
                start = m.end()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                files[path] = text[start:end].lstrip("\n").rstrip()
            print(f"[glob-split] detected {len(files)} files")
            return files
    print("[glob-split] WARNING: no separators detected; treating as single file.", file=sys.stderr)
    return {"__full_dump__.md": text}


def _matches_any(relpath: str, patterns: list[str]) -> bool:
    p = relpath.lstrip("/")
    for pat in patterns:
        pat = pat.lstrip("./")
        if fnmatch.fnmatch(p, pat):
            return True
        if "**" in pat:
            regex = re.escape(pat).replace(r"\*\*", ".*").replace(r"\*", "[^/]*")
            if re.fullmatch(regex, p):
                return True
    return False


def fetch_glob_bundles(
    url: str,
    token: Optional[str],
    bundles_cfg: dict[str, list[str]],
    out_dir: str,
    cache: Optional[str],
) -> None:
    """Fetch the whole-repo dump and split into bundles by glob patterns."""
    if cache and os.path.exists(cache):
        print(f"[glob-split] using cache: {cache}")
        raw = open(cache, encoding="utf-8").read()
    else:
        print(f"[glob-split] fetching {url} ...")
        raw = _fetch(url, token)
        print(f"[glob-split] fetched {len(raw):,} chars")
        if cache:
            os.makedirs(os.path.dirname(cache) or ".", exist_ok=True)
            open(cache, "w", encoding="utf-8").write(raw)

    files = _detect_and_split(raw)
    os.makedirs(out_dir, exist_ok=True)

    for key, patterns in bundles_cfg.items():
        matched = [(p, c) for p, c in sorted(files.items()) if _matches_any(p, patterns)]
        parts = [
            f"# NotebookLM source bundle: {key} ({len(matched)} files)\n",
            "# Files are separated by `===== <relative path> =====`.\n",
            "# When reporting findings, cite the relative path of the file.\n",
        ]
        for relpath, content in matched:
            parts.append(f"\n\n===== {relpath} =====\n\n{content}")
        text = "".join(parts)
        out_path = os.path.join(out_dir, f"{key}.md")
        open(out_path, "w", encoding="utf-8").write(text)
        b = len(text.encode())
        print(f"  {key:20s} files={len(matched):4d}  bytes={b:,} (~{b//6:,} words) -> {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Fetch uithub directory URLs and save as NotebookLM bundle files.")
    ap.add_argument("--config", required=True,
                    help="Bundle config JSON (see module docstring for formats)")
    ap.add_argument("--out", default="_nlm/bundles",
                    help="Output directory for bundle .md files")
    ap.add_argument("--token", default=os.environ.get("UITHUB_TOKEN"),
                    help="Bearer token for uithub auth (env: UITHUB_TOKEN)")
    ap.add_argument("--url", default=os.environ.get("UITHUB_URL"),
                    help="Whole-repo URL for glob-split mode (env: UITHUB_URL)")
    ap.add_argument("--cache-dir", default=None,
                    help="Directory to cache per-bundle fetches (Format A)")
    ap.add_argument("--cache", default=None,
                    help="Cache file for whole-repo fetch (Format B / glob-split)")
    a = ap.parse_args()

    cfg = json.load(open(a.config, encoding="utf-8"))
    bundles_raw: dict = cfg.get("bundles", {})
    if not bundles_raw:
        sys.exit(f"No 'bundles' key in {a.config}")

    # Detect format by inspecting first value
    first_val = next(iter(bundles_raw.values()))
    if isinstance(first_val, str):
        # Format A: URL-per-bundle
        print(f"[fetch_and_bundle] mode=URL-per-bundle  bundles={len(bundles_raw)}  out={a.out}")
        fetch_url_bundles(bundles_raw, a.token, a.out, a.cache_dir)
    else:
        # Format B: glob-split
        if not a.url:
            sys.exit("glob-split mode requires --url or UITHUB_URL env var")
        print(f"[fetch_and_bundle] mode=glob-split  bundles={len(bundles_raw)}  out={a.out}")
        fetch_glob_bundles(a.url, a.token, bundles_raw, a.out, a.cache)

    print("[fetch_and_bundle] done.")


if __name__ == "__main__":
    main()
