#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Commit2 後処理: SYS/SEV を走査して索引を生成し、SEQ 索引へ新行を挿入、
参照された既存 API/TBL へ 対応業務UC 逆引きを追記する。冪等。"""
import os, re, glob

ROOT = "/Users/sasakikouhei/trunk/project/faq"
SYSDIR = f"{ROOT}/02_basic_design/02_backend/01_system"
SEVDIR = f"{ROOT}/02_basic_design/02_backend/02_system_events"
SEQDIR = f"{ROOT}/02_basic_design/03_sequences"
APIDIR = f"{ROOT}/02_basic_design/02_backend/03_apis"
TBLDIR = f"{ROOT}/02_basic_design/02_backend/04_database"

def read(p): return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8").write(s)
def natkey(s): return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]

def h1name(t, idp):
    m = re.search(r'#\s*<span id="' + idp + r'"></span>' + idp + r':\s*(.+)', t)
    return m.group(1).strip() if m else idp

def cell(t, label):
    m = re.search(r'\|\s*' + re.escape(label) + r'\s*\|\s*([^|]*?)\s*\|', t)
    return m.group(1).strip() if m else ""

def first_uc(t):
    m = re.search(r'(UC-\d+)', cell(t, "対応業務UC"))
    return m.group(1) if m else ""

# ---- SYS 走査 ----
sysrows = []
for f in sorted(glob.glob(f"{SYSDIR}/SYS-*.md"), key=natkey):
    t = read(f); sid = os.path.basename(f)[:-3]
    name = h1name(t, sid)
    mrow = re.search(r'\|\s*`' + sid + r'`\s*\|([^|]*)\|([^|]*)\|([^|]*)\|', t)
    typ = mrow.group(2).strip() if mrow else ""
    trig = mrow.group(3).strip() if mrow else ""
    uc = first_uc(t)
    sysrows.append((sid, name, typ, trig, uc))

# ---- SEV 走査 ----
sevrows = []
for f in sorted(glob.glob(f"{SEVDIR}/SEV-*.md"), key=natkey):
    t = read(f); vid = os.path.basename(f)[:-3]
    name = h1name(t, vid)
    msys = re.search(r'(SYS-\d+)', cell(t, "対応システムID"))
    sysid = msys.group(1) if msys else ""
    uc = first_uc(t)
    sevrows.append((vid, name, sysid, uc))

# ---- 01_system/index.md ----
L = ["# システム設計書", "",
     f"> **メインシステムの全システム処理(`SYS-001`〜`SYS-{sysrows[-1][0][-3:]}`)を一覧する独立設計書です。** 無人で動く処理(バッチ / Webhook / 非同期 / 監視 / 通知)を、画面設計の backend 版として 1 処理 = 1 ファイルで管理します。各処理は対応する業務ユースケース・[システムイベント](../02_system_events/index.md)(`SEV-*`)・API・テーブル・[シーケンス](../../03_sequences/index.md)へトレースします。",
     "", f"*版数 v1.0 ・ 更新 2026-06-23 ・ システム処理 {len(sysrows)} ・ ステータス ドラフト*", "",
     "## 一覧", "",
     "| システムID | 処理名 | 種別 | トリガー | 対応業務UC |", "|---|---|---|---|---|"]
for sid, name, typ, trig, uc in sysrows:
    ucl = f"[{uc}](../../../01_requirements/04_business_usecases/{uc}.md#{uc})" if uc else "—"
    L.append(f"| <span id=\"{sid}\"></span>[`{sid}`]({sid}.md#{sid}) | {name} | {typ} | {trig} | {ucl} |")
L.append("")
write(f"{SYSDIR}/index.md", "\n".join(L))

# ---- 02_system_events/index.md(システム別) ----
byss = {}
for vid, name, sysid, uc in sevrows:
    byss.setdefault(sysid, []).append((vid, name, uc))
sysname = {sid: name for sid, name, *_ in sysrows}
L = ["# システムイベント設計書", "",
     f"> **全システムイベント(`SEV-001`〜`SEV-{sevrows[-1][0][-3:]}`)を対応システム別に一覧します。** 各システムイベントは [システム設計](../01_system/index.md)(`SYS-*`)の 1 処理に属し、複数のイベントが 1 つの業務ユースケースを実現します(システムイベント → 業務UC は多:1)。処理内容の正本は各システム設計 §6 です。",
     "", f"*版数 v1.0 ・ 更新 2026-06-23 ・ システムイベント {len(sevrows)} ・ ステータス ドラフト*", "",
     "## 一覧(システム別)", ""]
for sid in sorted(byss, key=natkey):
    L.append(f"### <span id=\"{sid}\"></span>{sid} {sysname.get(sid,'')}")
    L.append("")
    L.append("| SEV-ID | イベント名 | 対応業務UC |")
    L.append("|---|---|---|")
    for vid, name, uc in byss[sid]:
        ucl = f"[{uc}](../../../01_requirements/04_business_usecases/{uc}.md#{uc})" if uc else "—"
        L.append(f"| [`{vid}`]({vid}.md#{vid}) | {name} | {ucl} |")
    L.append("")
write(f"{SEVDIR}/index.md", "\n".join(L))

# ---- 03_sequences/index.md へ SEQ-108.. を挿入 ----
seqidx = f"{SEQDIR}/index.md"; s = read(seqidx)
newrows = []
for f in sorted(glob.glob(f"{SEQDIR}/SEQ-*.md"), key=natkey):
    sid = os.path.basename(f)[:-3]
    n = int(sid.split("-")[1])
    if n < 108: continue
    t = read(f)
    m = re.search(r'#\s*<span id="' + sid + r'"></span>' + sid + r':\s*(.+)', t)
    name = m.group(1).strip() if m else sid
    mu = re.search(r'対応業務ユースケース\s*\|\s*\[(UC-\d+)\]', t)
    uc = mu.group(1) if mu else ""
    ucl = f"[{uc}](../../01_requirements/04_business_usecases/{uc}.md#{uc})" if uc else "—"
    newrows.append(f"| <span id=\"{sid}\"></span>[{sid}]({sid}.md#{sid}) | {name} | {ucl} | — |")
if newrows and "SEQ-108" not in s:
    # SEQ-107 行の直後に挿入
    lines = s.split("\n")
    out = []
    for ln in lines:
        out.append(ln)
        if re.match(r'\|\s*<span id="SEQ-107">', ln):
            out.extend(newrows)
    s = "\n".join(out)
    s = re.sub(r'シーケンス 107', f'シーケンス {107+len(newrows)}', s)
    write(seqidx, s)

# ---- 既存 API/TBL へ逆引き 対応業務UC 追記 ----
def patch_cell(path, label, uc):
    if not os.path.exists(path): return False
    s = read(path)
    m = re.search(r'(\|\s*' + re.escape(label) + r'\s*\|\s*)([^|]*?)(\s*\|)', s)
    if not m: return False
    c = m.group(2).strip()
    if uc in c: return False
    link = f"[{uc}](../../../01_requirements/04_business_usecases/{uc}.md#{uc})"
    newc = link if c == "—" or c == "" else c + " ・ " + link
    write(path, s[:m.start(2)] + newc + s[m.end(2):])
    return True

patched = 0
for f in sorted(glob.glob(f"{SYSDIR}/SYS-*.md"), key=natkey):
    t = read(f); uc = first_uc(t)
    if not uc: continue
    apis = sorted(set(re.findall(r'/03_apis/(API-\d+)\.md', t)), key=natkey)
    tbls = sorted(set(re.findall(r'/04_database/(TBL-\d+)\.md', t)), key=natkey)
    for a in apis:
        if patch_cell(f"{APIDIR}/{a}.md", "対応業務UC", uc): patched += 1
    for tb in tbls:
        if patch_cell(f"{TBLDIR}/{tb}.md", "対応業務UC(逆引き)", uc): patched += 1

print(f"SYS {len(sysrows)} / SEV {len(sevrows)} / new SEQ {len(newrows)} indexed; reverse-links patched {patched}")
