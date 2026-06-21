#!/usr/bin/env python3
"""再構成 P5 (DB設計) — TBL フラット採番。

`99_management/crosswalk.json` の `tblmap`(旧 `TBL-<分類>-<nnn>` → 新 `TBL-<NNN>`)に従い、
リポジトリ全 .md(99_management / CLAUDE.md / _build は除外)の TBL ID を一括張替する。
- ファイル名(02_basic_design/04_database/TBL-*.md)を新 ID へ rename(git mv)。
- 本文中の TBL ID(リンク・プレーンテキスト・`#TBL-...` アンカー・`<span id="TBL-...">` ・パンくず)をすべて新 ID へ。

決定論的・冪等。長い ID から先に置換して部分一致を防ぐ。
"""
import json, os, re, glob, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TBLMAP = json.load(open(os.path.join(ROOT, "99_management/crosswalk.json")))["tblmap"]
DB_DIR = os.path.join(ROOT, "02_basic_design/04_database")


def target_md_files():
    files = set(glob.glob(os.path.join(ROOT, "**/*.md"), recursive=True))
    out = []
    for f in files:
        rel = os.path.relpath(f, ROOT)
        top = rel.split(os.sep)[0]
        if top in ("99_management", "_build") or rel == "CLAUDE.md":
            continue
        out.append(f)
    return sorted(out)


def rewrite_text(s):
    # 旧 ID を長い順(分類接頭辞の長さ違い)で置換。TBL-TP-/TBL-M-/TBL-T-/TBL-H- いずれも
    # 完全トークン一致なので順序非依存だが安全のためキー長で降順ソート。
    for old in sorted(TBLMAP, key=len, reverse=True):
        new = TBLMAP[old]
        # トークン境界: 後続が数字・英字でないこと(TBL-T-001 が TBL-T-0011 を巻き込まない)
        s = re.sub(re.escape(old) + r"(?![0-9A-Za-z])", new, s)
    return s


def main():
    # 1) 本文置換(全対象 .md)
    changed = 0
    for f in target_md_files():
        s = open(f, encoding="utf-8").read()
        ns = rewrite_text(s)
        if ns != s:
            open(f, "w", encoding="utf-8").write(ns)
            changed += 1
    print(f"content rewritten in {changed} files")

    # 2) DB ディレクトリの TBL ファイル rename
    renamed = 0
    for old, new in TBLMAP.items():
        src = os.path.join(DB_DIR, f"{old}.md")
        dst = os.path.join(DB_DIR, f"{new}.md")
        if os.path.exists(src):
            subprocess.run(["git", "mv", src, dst], cwd=ROOT, check=True)
            renamed += 1
        elif not os.path.exists(dst):
            print(f"WARN: missing {src}", file=sys.stderr)
    print(f"renamed {renamed} TBL files")


if __name__ == "__main__":
    main()
