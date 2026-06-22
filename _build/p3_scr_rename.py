#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 step1: SCR をフラット採番へ一括張替。
- 01_screens/SCR-*.md をリネーム(scrmap)
- mocks/*.html, *.png をリネーム(例 SCR-004-001-1.png -> SCR-005-1.png)
- リポジトリ全 .md(99_management / CLAUDE.md / _build を除く)の SCR 参照(リンク・テキスト・アンカー)を新IDへ置換
決定論的・冪等(scrmap は旧->新の単射。SCR-001..004 は不変)。
"""
import os, re, json, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
cw = json.load(open("99_management/crosswalk.json", encoding="utf-8"))
scrmap = dict(cw["scrmap"])
# 内部キーは "SCR-WIDGET"。ファイル/アンカー上の旧IDは "SCR-WIDGET"。
# crosswalk の cross では旧アンカーが "WIDGET"(SCR- なし)である点に注意。

SCR_DIR = "02_basic_design/01_screens"
MOCK_DIR = f"{SCR_DIR}/mocks"

# 置換から除外するパス(正本・ルールブック・ツール)
EXCLUDE_PREFIX = ("99_management/", "_build/", "CLAUDE.md")

def git_mv(a, b):
    if a == b:
        return
    subprocess.run(["git", "mv", a, b], check=True)

SENTINEL = "_build/.p3_scr_renamed"

def rename_files():
    # SCR md ファイル: 旧名 -> 新名。衝突回避のため一旦 tmp へ。
    moves = []
    for old, new in scrmap.items():
        # ファイル名は SCR-WIDGET.md。scrmap キーは "SCR-WIDGET"。
        op = f"{SCR_DIR}/{old}.md"
        np = f"{SCR_DIR}/{new}.md"
        if os.path.exists(op):
            moves.append((op, np))
    # 2段リネーム(全 tmp -> 全 new)で循環/衝突を回避
    tmp = []
    for i, (op, np) in enumerate(moves):
        t = f"{SCR_DIR}/__tmp_scr_{i}.md"
        git_mv(op, t); tmp.append((t, np))
    for t, np in tmp:
        git_mv(t, np)

    # mocks: <旧SCR>-<n>.(html|png) -> <新SCR>-<n>.(html|png)
    mmoves = []
    for f in sorted(glob.glob(f"{MOCK_DIR}/*")):
        b = os.path.basename(f)
        m = re.match(r'^(SCR-(?:WIDGET|\d{3}(?:-\d{3})?))-(\d+)\.(html|png)$', b)
        if not m:
            continue
        oldscr, n, ext = m.group(1), m.group(2), m.group(3)
        if oldscr in scrmap:
            newscr = scrmap[oldscr]
            mmoves.append((f, f"{MOCK_DIR}/{newscr}-{n}.{ext}"))
    mtmp = []
    for i, (op, np) in enumerate(mmoves):
        t = f"{MOCK_DIR}/__tmp_mock_{i}"
        git_mv(op, t); mtmp.append((t, np))
    for t, np in mtmp:
        git_mv(t, np)
    return len(moves), len(mmoves)

def build_replacer():
    # 旧->新。longest-key-first で SCR-004-001 を SCR-004 より先に処理する。
    # SCR-WIDGET も含む。SCR-001..004 は自分自身へ(no-op)。
    pairs = sorted(scrmap.items(), key=lambda kv: -len(kv[0]))
    # 単一パスで衝突を避けるためプレースホルダ方式
    def repl(text):
        # 1) old -> placeholder
        for i, (old, new) in enumerate(pairs):
            # 識別子境界: 直前は英数・ハイフン以外。直後は数字でなく、かつ
            # さらに長い SCR セグメント(-\d{3})でもないこと(mock の -<n> 接尾は許可)。
            pat = re.compile(r'(?<![A-Za-z0-9-])' + re.escape(old) + r'(?![0-9])(?!-\d{3}(?![0-9]))')
            text = pat.sub(f"\x00{i}\x00", text)
        # 2) placeholder -> new
        for i, (old, new) in enumerate(pairs):
            text = text.replace(f"\x00{i}\x00", new)
        return text
    return repl

def widget_fixups(text):
    # 旧 WIDGET 画面は ID/アンカーが bare "WIDGET"(SCR- なし)。SCR-030 へ。
    # 英単語 widget / ウィジェット は壊さないよう、ID 文脈のみを置換する。
    text = text.replace('id="WIDGET"', 'id="SCR-030"')   # アンカー定義
    # アンカー参照(同一ページ #WIDGET / 他ページ ....md#WIDGET)。後続が識別子文字でない断片のみ。
    text = re.sub(r'#WIDGET(?![A-Za-z0-9_-])', '#SCR-030', text)
    text = text.replace('`WIDGET`', '`SCR-030`')          # コード表記の ID
    text = re.sub(r'(?m)^# WIDGET ', '# SCR-030 ', text)  # H1 接頭辞
    text = text.replace('**WIDGET ', '**SCR-030 ')        # 旧パンくず(再生成で上書きされるが念のため)
    return text

def replace_refs():
    repl = build_replacer()
    targets = []
    for g in ("01_requirements", "02_basic_design", "03_future"):
        targets += glob.glob(f"{g}/**/*.md", recursive=True)
    targets.append("README.md")
    changed = 0
    for p in sorted(set(targets)):
        if any(p == e or p.startswith(e) for e in EXCLUDE_PREFIX):
            continue
        s = open(p, encoding="utf-8").read()
        ns = widget_fixups(repl(s))
        if ns != s:
            open(p, "w", encoding="utf-8").write(ns)
            changed += 1
    return changed

if __name__ == "__main__":
    # 新フラットID(SCR-005..SCR-029)は旧キー(SCR-005..SCR-023)と文字列衝突するため、
    # rename も replace_refs も「一度だけ」適用しなければ ID が多重シフトする。
    # 完了マーカで全体を冪等(再実行は no-op)にする。
    if os.path.exists(SENTINEL):
        print("p3_scr_rename: already applied (sentinel present) -> skip")
    else:
        nf, nm = rename_files()
        nc = replace_refs()
        open(SENTINEL, "w").write("done\n")
        print(f"renamed SCR md: {nf}, renamed mocks: {nm}, files with ref updates: {nc}")
