#!/usr/bin/env python3
"""P6a: Generate per-file sequence diagrams 02_basic_design/05_sequences/SEQ-NNN.md.

Deterministic. Re-runnable (idempotent): regenerates SEQ-*.md + index.md from
historical UC files preserved at commit a412652 and the crosswalk maps.

Source of truth for diagrams: git a412652
  01_requirements/02_business_usecases/UC-SCR-*.md / UC-SYSTEM-*.md
Maps:
  99_management/uc_crosswalk.json : old UC key -> new UC-NNN
  99_management/crosswalk.json    : scrmap / apimap / tblmap

A SEQ file is emitted for every old UC key that has a mermaid sequenceDiagram
in its heading block. SEQ-001.. are numbered in new-UC order (UC-001..UC-247),
which puts screen-origin (UC-SCR-*) before system-origin (UC-SYSTEM-*).
"""
import json
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------------------
# SUPERSEDED / 再実行禁止 (2026-06-23)
# SEQ-*.md は基本設計レベル(ユーザー / 画面 / サーバー の 3 系統)へ手保守移行済み。
# 本生成器は旧 5 系統モデル(利用者 / 画面 / API / DB / 外部・バッチ・通知)を
# git a412652 から再生成するため、再実行すると現行の図・書式を巻き戻す。
# provenance 保持のためコードは残すが、既定では実行を中止する。
# 意図して再生成する場合のみ環境変数 SEQ_GEN_FORCE=1 を付ける。
# ---------------------------------------------------------------------------
if os.environ.get("SEQ_GEN_FORCE") != "1":
    sys.exit(
        "[p6a_gen_sequences] 実行中止: SEQ は手保守へ移行済み(再実行で巻き戻し)。"
        " 意図的に再生成する場合のみ SEQ_GEN_FORCE=1 を設定してください。"
    )

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = "a412652"
UC_DIR_HIST = "01_requirements/02_business_usecases"
OUT_DIR = os.path.join(ROOT, "02_basic_design", "05_sequences")

uc_cw = json.load(open(os.path.join(ROOT, "99_management", "uc_crosswalk.json")))
cw = json.load(open(os.path.join(ROOT, "99_management", "crosswalk.json")))
scrmap = cw["scrmap"]
apimap = cw["apimap"]
tblmap = cw["tblmap"]  # old TBL-id -> new TBL-id (not used directly; we map by name)


def newnum(uc):  # "UC-007" -> 7
    return int(uc.split("-")[1])


# ---- table name -> new TBL-NNN (from current DB design files) -----------------
def build_tbl_name_map():
    m = {}
    db = os.path.join(ROOT, "02_basic_design", "04_database")
    for fn in os.listdir(db):
        mo = re.match(r"(TBL-\d+)\.md$", fn)
        if not mo:
            continue
        tid = mo.group(1)
        h1 = ""
        for line in open(os.path.join(db, fn), encoding="utf-8"):
            if line.startswith("# "):
                h1 = line
                break
        nm = re.search(r"</span>([A-Z_]+)", h1)
        if nm:
            m[nm.group(1)] = tid
    return m


TBL_NAME = build_tbl_name_map()


# ---- source file for an old UC key -------------------------------------------
def srcfile(key):
    if key.startswith("UC-SYSTEM-"):
        return key + ".md"
    mo = re.match(r"(UC-SCR-.+)-EV\d+$", key)
    return mo.group(1) + ".md"


def hist_text(fn):
    return subprocess.run(
        ["git", "show", f"{HIST}:{UC_DIR_HIST}/{fn}"],
        capture_output=True, text=True, cwd=ROOT,
    ).stdout


_cache = {}


def get_hist(fn):
    if fn not in _cache:
        _cache[fn] = hist_text(fn)
    return _cache[fn]


# ---- extract the heading block + its diagram for an old key ------------------
def extract(key):
    """Return (title, related_line, diagram_body) or None if no diagram."""
    txt = get_hist(srcfile(key))
    if key.startswith("UC-SYSTEM-"):
        # whole file is one UC; title from H1
        m = re.search(r'^#\s+<span id="%s"></span>%s:?\s*(.+)$' % (re.escape(key), re.escape(key)),
                      txt, re.M)
        title = m.group(1).strip() if m else key
        block = txt
        rel = ""
        rm = re.search(r"\|\s*関連 API\s*\|(.+?)\|", txt)
        if rm:
            rel = rm.group(1)
    else:
        # locate "### <span id="KEY"></span>KEY name" .. next "### " or EOF
        pat = re.compile(
            r'^###\s+<span id="%s"></span>%s\s*(.*?)\s*$' % (re.escape(key), re.escape(key)),
            re.M,
        )
        m = pat.search(txt)
        if not m:
            return None
        title = m.group(1).strip()
        start = m.end()
        nxt = re.search(r"^###\s", txt[start:], re.M)
        block = txt[start:start + nxt.start()] if nxt else txt[start:]
        rel = ""
        rm = re.search(r"\|\s*関連\s*\|(.+?)\|", block)
        if rm:
            rel = rm.group(1)
    dm = re.search(r"```mermaid\s*\n(sequenceDiagram.*?)\n```", block, re.S)
    if not dm:
        return None
    return title, rel, dm.group(1)


# ---- collect references for the relation table ------------------------------
def collect_refs(related_line, diagram):
    # SCR: from related line + diagram tokens
    olds = set(re.findall(r"SCR-\d+(?:-\d+)?", related_line))
    olds |= set(re.findall(r"SCR-\d+(?:-\d+)?", diagram))
    new_scr = sorted({scrmap[s] for s in olds if s in scrmap},
                     key=lambda x: int(x.split("-")[1]))
    # API: old API-* in related line
    old_api = re.findall(r"API-[A-Z]+-\d+", related_line)
    new_api = sorted({apimap[a] for a in old_api if a in apimap},
                     key=lambda x: int(x.split("-")[1]))
    # tables: names in diagram
    names = re.findall(r"\b(?:[MTH]|TP)_[A-Z_]+\b", diagram)
    new_tbl = sorted({TBL_NAME[n] for n in names if n in TBL_NAME},
                     key=lambda x: int(x.split("-")[1]))
    unresolved = sorted(set(n for n in names if n not in TBL_NAME))
    return new_scr, new_api, new_tbl, unresolved


def rewrite_diagram(diagram):
    """Replace old SCR-xxx tokens with new SCR ids. Longest-first to avoid
    partial overlap (SCR-004-001 before SCR-004)."""
    count = 0
    for old in sorted(scrmap, key=len, reverse=True):
        new = scrmap[old]
        if old == new:
            # still count occurrences for reporting only when different
            continue
        pat = re.compile(re.escape(old) + r"(?![\d-])")
        diagram, n = pat.subn(new, diagram)
        count += n
    return diagram, count


# ---- build ordered list of SEQ entries --------------------------------------
# new UC -> old key (1:1)
new2old = {v: k for k, v in uc_cw.items()}

entries = []  # (new_uc, old_key, title, rel, diagram)
for n in range(1, 248):
    uc = f"UC-{n:03d}"
    old = new2old[uc]
    ex = extract(old)
    if ex is None:
        continue
    title, rel, diagram = ex
    entries.append((uc, old, title, rel, diagram))

# ---- emit SEQ files ----------------------------------------------------------
os.makedirs(OUT_DIR, exist_ok=True)
total_scr_sub = 0
unresolved_all = {}
seq_rows = []  # for index

for i, (uc, old, title, rel, diagram) in enumerate(entries, start=1):
    seq = f"SEQ-{i:03d}"
    new_scr, new_api, new_tbl, unresolved = collect_refs(rel, diagram)
    if unresolved:
        unresolved_all[seq] = unresolved
    new_diag, nsub = rewrite_diagram(diagram)
    total_scr_sub += nsub

    uc_link = f"[{uc}](../../01_requirements/02_business_usecases/{uc}.md#{uc})"
    scr_cell = " ・ ".join(
        f"[{s}](../01_screens/{s}.md#{s})" for s in new_scr) or "—"
    api_cell = " ・ ".join(
        f"[{a}](../03_apis/{a}.md#{a})" for a in new_api) or "—"
    tbl_cell = " ・ ".join(
        f"[{t}](../04_database/{t}.md#{t})" for t in new_tbl) or "—"

    md = []
    md.append("<!-- portal-top -->")
    md.append("<!-- /portal-top -->")
    md.append("")
    md.append(f'# <span id="{seq}"></span>{seq}: {title}')
    md.append("")
    md.append(f"> **このページは、業務ユースケース {uc}（{title}）のシーケンス図を定義します。**")
    md.append("")
    md.append("*版数 v1.0 ・ 更新 2026-06-21 ・ ステータス ドラフト*")
    md.append("")
    md.append("## 項目")
    md.append("")
    md.append("シーケンス図の対応ユースケースと、図に登場する画面・API・テーブルを示します。")
    md.append("")
    md.append("| 項目 | 内容 |")
    md.append("|---|---|")
    md.append(f"| SEQ ID | `{seq}` |")
    md.append(f"| 対応業務ユースケース | {uc_link} |")
    md.append(f"| 関連画面 | {scr_cell} |")
    md.append(f"| 関連 API | {api_cell} |")
    md.append(f"| 関連テーブル | {tbl_cell} |")
    md.append("")
    md.append("## シーケンス図")
    md.append("")
    md.append("```mermaid")
    md.append(new_diag)
    md.append("```")
    md.append("")
    md.append("## 備考")
    md.append("")
    md.append(f"- 本図は基本設計レベルの抽象度（利用者 / 画面 / API / DB / 外部・バッチ・通知、`テーブル名(CRUD)` 表記）で記述する。")
    md.append(f"- 図の出典は業務ユースケース {uc_link}。画面イベントとの対応は {uc} を参照。")
    md.append("")
    md.append("<!-- portal-bottom -->")
    md.append("<!-- /portal-bottom -->")
    md.append("")
    open(os.path.join(OUT_DIR, f"{seq}.md"), "w", encoding="utf-8").write("\n".join(md))

    seq_rows.append((seq, title, uc, new_scr))

# ---- emit index.md -----------------------------------------------------------
idx = []
idx.append("<!-- portal-top -->")
idx.append("<!-- /portal-top -->")
idx.append("")
idx.append("# シーケンス設計")
idx.append("")
idx.append("> **このセクションは、業務ユースケースに対応するシーケンス図を 1 図 1 ファイル（`SEQ-NNN`）で管理します。**")
idx.append("")
idx.append(f"*版数 v1.0 ・ 更新 2026-06-21 ・ シーケンス {len(seq_rows)} ・ ステータス ドラフト*")
idx.append("")
idx.append("## 1. 読み順")
idx.append("")
idx.append("シーケンス図は業務ユースケース順（画面起点 → システム起点）に `SEQ-001` から採番しています。各図は対応する業務ユースケース・画面・API・テーブルへトレースします。")
idx.append("")
idx.append("## 2. シーケンス一覧 / ユースケース対応")
idx.append("")
idx.append("各シーケンス図と対応する業務ユースケース・主な関連画面の一覧です。")
idx.append("")
idx.append("| SEQ ID | 名称 | 対応業務ユースケース | 主な関連画面 |")
idx.append("|---|---|---|---|")
for seq, title, uc, new_scr in seq_rows:
    seq_link = f'<span id="{seq}"></span>[{seq}]({seq}.md#{seq})'
    uc_link = f"[{uc}](../../01_requirements/02_business_usecases/{uc}.md#{uc})"
    scr_cell = " ・ ".join(
        f"[{s}](../01_screens/{s}.md#{s})" for s in new_scr) or "—"
    idx.append(f"| {seq_link} | {title} | {uc_link} | {scr_cell} |")
idx.append("")
idx.append("<!-- portal-bottom -->")
idx.append("<!-- /portal-bottom -->")
idx.append("")
open(os.path.join(OUT_DIR, "index.md"), "w", encoding="utf-8").write("\n".join(idx))

# ---- report ------------------------------------------------------------------
print(f"SEQ files generated: {len(seq_rows)}")
print(f"old UC keys with diagrams: {len(entries)} / 247")
print(f"diagram SCR token substitutions: {total_scr_sub}")
print(f"unresolved table tokens: {unresolved_all if unresolved_all else 'none'}")
