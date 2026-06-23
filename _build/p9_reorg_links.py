#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P9: 基本設計フォルダ再編(frontend/backend グルーピング + システム層新設)に伴うリンク一括張替。

各 .md のリンクを「移動前の位置基準で絶対解決 → 旧→新サブフォルダ写像 → 移動後の位置基準で
relpath 再出力」する。移動後ターゲットがディスク上に実在する場合のみ書き換えるため、
既に新形式のリンク(= 旧基準で解決すると実在しない)はそのまま残り、再実行しても変化しない(冪等)。

対象: 01_requirements/** 02_basic_design/** 03_future/** 99_management/** README.md
非対象: CLAUDE.md(ディレクトリツリー・テンプレートのパス例は手動更新), *.json
前提: 先に git mv で 8 サブフォルダを新階層へ移動済みであること。
"""
import os, re, glob, html

# 旧(repo root 相対 absolute)→ 新
OLDMAP = {
    "02_basic_design/01_screens":       "02_basic_design/01_frontend/01_screens",
    "02_basic_design/02_screen_events": "02_basic_design/01_frontend/02_screen_events",
    "02_basic_design/03_apis":          "02_basic_design/02_backend/03_apis",
    "02_basic_design/04_database":      "02_basic_design/02_backend/04_database",
    "02_basic_design/05_sequences":     "02_basic_design/03_sequences",
    "02_basic_design/06_permissions":   "02_basic_design/04_permissions",
    "02_basic_design/07_errors":        "02_basic_design/05_errors",
    "02_basic_design/08_messages":      "02_basic_design/06_messages",
}
NEWMAP = {v: k for k, v in OLDMAP.items()}  # 新 → 旧(ファイルの現在地から移動前パスを復元)

def remap_target(t):
    """絶対ターゲット t の先頭サブフォルダを旧→新へ写像。"""
    for old, new in sorted(OLDMAP.items(), key=lambda kv: -len(kv[0])):
        if t == old or t.startswith(old + "/"):
            return new + t[len(old):]
    return t

def old_path_of(fnew):
    """ファイルの現在地(新)から移動前パス(旧)を復元。移動していなければ同一。"""
    for new, old in sorted(NEWMAP.items(), key=lambda kv: -len(kv[0])):
        if fnew == new or fnew.startswith(new + "/"):
            return old + fnew[len(new):]
    return fnew

LINK_RES = [
    re.compile(r'(\]\()([^)\s]+)(\))'),
    re.compile(r'(href=")([^"]+)(")'),
]

def rewrite_file(fnew):
    s = open(fnew, encoding="utf-8").read()
    dold = os.path.dirname(old_path_of(fnew))
    dnew = os.path.dirname(fnew)
    changed = [0]

    def fix(raw):
        h = html.unescape(raw)
        if h.startswith(("http://", "https://", "mailto:")):
            return None
        path, sep, frag = h.partition("#")
        if path == "":
            return None  # ページ内アンカー
        tgt_new = remap_target(os.path.normpath(os.path.join(dold, path)))
        if not os.path.exists(tgt_new):
            return None  # 旧基準で実在しない = 既に新形式 or 対象外。触らない
        newrel = os.path.relpath(tgt_new, dnew).replace(os.sep, "/")
        return newrel + (("#" + frag) if sep else "")

    def repl(m):
        pre, raw, post = m.group(1), m.group(2), m.group(3)
        out = fix(raw)
        if out is None or out == raw:
            return m.group(0)
        changed[0] += 1
        return pre + out + post

    for rx in LINK_RES:
        s = rx.sub(repl, s)
    if changed[0]:
        open(fnew, "w", encoding="utf-8").write(s)
    return changed[0]

def main():
    files = []
    for g in ("01_requirements", "02_basic_design", "03_future", "99_management"):
        files += glob.glob(f"{g}/**/*.md", recursive=True)
    files.append("README.md")
    files = sorted(set(f for f in files if os.path.exists(f)))
    tot_links = tot_files = 0
    for f in files:
        n = rewrite_file(f)
        if n:
            tot_files += 1; tot_links += n
    print(f"rewrote {tot_links} links across {tot_files} files (scanned {len(files)})")

if __name__ == "__main__":
    main()
