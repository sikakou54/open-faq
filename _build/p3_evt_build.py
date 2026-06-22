#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 step2/3: 画面イベントを EVT 個別ファイル化し、SCR §6 に EVT 列を付与する。
前提: p3_scr_rename.py 実行済み(SCR はフラットID、ファイル名・アンカーは新ID)。
- 各新SCRの §6 <tbody> を解析(EV-code / 項目ID / イベント名 / 処理)。
- evtmap("<旧SCR>/EV-<nn>" -> EVT-NNN)・uc_crosswalk(UC-SCR-<旧SCR>-EV<nn> -> UC-PPP)で結線。
- 02_basic_design/02_screen_events/EVT-NNN.md を生成。
- SCR §6 の <thead>/<tbody> 各行に EVT-ID 列を追加(冪等)。
- SCR §1 表へ「対応業務UC」行を追加(当該画面の EVT 群経由 UC、冪等)。
- 02_screen_events/index.md(画面別 EVT 一覧 + EVT↔UC 対応表)を生成。
決定論的・冪等。
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
cw = json.load(open("99_management/crosswalk.json", encoding="utf-8"))
ucw = json.load(open("99_management/uc_crosswalk.json", encoding="utf-8"))
scrmap = cw["scrmap"]            # 旧SCR -> 新SCR
evtmap = cw["evtmap"]            # "旧SCR/EV-nn" -> EVT-NNN
new2old = {v: k for k, v in scrmap.items()}   # 新SCR -> 旧SCR(単射)

SCR_DIR = "02_basic_design/01_screens"
EVT_DIR = "02_basic_design/02_screen_events"

# ---- §6 テーブル解析 ----------------------------------------------------
def split_section6(text):
    """§6 見出しから次の '---'(末尾区切り)までを返す。"""
    m = re.search(r'## <span id="6-画面イベント一覧"></span>6\. 画面イベント一覧', text)
    if not m:
        return None, None, None
    start = m.start()
    # §6 内の <table>...</table>
    tm = re.search(r'<table>.*?</table>', text[start:], re.S)
    if not tm:
        return start, None, None
    tab_start = start + tm.start()
    tab_end = start + tm.end()
    return tab_start, tab_end, text[tab_start:tab_end]

ROW_RE = re.compile(r'<tr>\s*<td><code>(EV-\d+)</code></td>\s*(.*?)</tr>', re.S)

def strip_evt_column(table):
    """既に付与された EVT 列(ヘッダ・各行セル・colgroup の追加 col)を除去し、正準形に戻す。"""
    if table is None:
        return None
    t = table
    # 行頭の EVT セルを除去
    t = re.sub(
        r'<tr>\s*<td><a href="\.\./02_screen_events/EVT-\d+\.md#EVT-\d+">EVT-\d+</a></td>\s*(<td><code>EV-\d+</code></td>)',
        r'<tr>\n\1', t)
    # ヘッダの EVT 列を除去
    t = t.replace("<th>EVT-ID</th>\n<th>イベント ID</th>", "<th>イベント ID</th>")
    t = t.replace("<th>EVT-ID</th><th>イベント ID</th>", "<th>イベント ID</th>")
    # colgroup に追加した EVT 用 col を除去
    t = t.replace('<colgroup>\n<col style="width: 10%" />', "<colgroup>", 1)
    return t

def parse_rows(table_html):
    """tbody の各行(先頭セルが <code>EV-nn</code>)を抽出。
    返り値: list of dict(ev, item_html, name_html, proc_html)。
    EV-code の <td> は『行頭セル』のみ対象(処理セル内の <code>EV-..</code> 参照は除外)。"""
    rows = []
    for m in ROW_RE.finditer(table_html):
        ev = m.group(1)
        rest = m.group(2)
        cells = re.findall(r'<td>(.*?)</td>', rest, re.S)
        # rest は EV セルの後ろ。期待: [項目ID, イベント名, 処理]
        if len(cells) < 3:
            continue
        item_html = cells[0].strip()
        name_html = cells[1].strip()
        proc_html = cells[2].strip()
        rows.append(dict(ev=ev, item=item_html, name=name_html, proc=proc_html))
    return rows

def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', s).strip()

# ---- EVT 本文生成 -------------------------------------------------------
def item_ids(item_html):
    ids = re.findall(r'IT-\d+', item_html)
    seen = set(); out = []
    for i in ids:
        if i not in seen:
            seen.add(i); out.append(i)
    return out

def api_refs(proc_html):
    # (表示名, 相対パス#ID) を抽出。SCR ページからの相対は ../03_apis/...
    refs = []
    for m in re.finditer(r'<a href="(\.\./03_apis/[^"]+)">([^<]+)</a>', proc_html):
        refs.append((m.group(2).strip(), m.group(1).strip()))
    # 重複除去(順序保持)
    seen = set(); out = []
    for nm, href in refs:
        if href not in seen:
            seen.add(href); out.append((nm, href))
    return out

def transitions(proc_html, self_scr):
    ids = []
    for sid in re.findall(r'SCR-\d{3}', proc_html):
        if sid != self_scr and sid not in ids:
            ids.append(sid)
    return ids

def evt_label(name_html):
    lbl = strip_tags(name_html)
    return lbl if lbl else "(無題)"

def fix_evt_links(proc_html):
    """処理セルは SCR ページ基準の相対リンク。EVT ページ(同じ深さ ../03_apis 等は不変、
    ただし #IT- 同一ページ参照は SCR ページ側の項目なので絶対参照へ書き換える)。"""
    # EVT ファイルは 02_basic_design/02_screen_events/ にある。
    # SCR §6 内の '../03_apis/' '../04_database/' '../../01_requirements/' は深さ同一なのでそのまま有効。
    # '#IT-xx'(同一ページ内アンカー)・'#API-...'(SCR内ではなくAPIページ参照は既に相対付き)は、
    #   #IT- は当該 SCR ページの項目なので EVT からは解決できない -> プレーンテキスト化。
    proc_html = re.sub(r'<a href="#(IT-\d+)">([^<]+)</a>', r'\2', proc_html)
    # 兄弟参照 SCR-NNN.md(SCR フォルダ基準)は EVT フォルダから ../01_screens/ へ。
    proc_html = re.sub(r'href="(SCR-\d{3}\.md)', r'href="../01_screens/\1', proc_html)
    proc_html = re.sub(r'\]\((SCR-\d{3}\.md)', r'](../01_screens/\1', proc_html)
    return proc_html

def build_evt_body(evt, ev, name, scr_new, uc_new, item_html, proc_html):
    label = evt_label(name)
    its = item_ids(item_html)
    apis = api_refs(proc_html)
    trans = transitions(proc_html, scr_new)
    proc_fixed = fix_evt_links(proc_html)

    scr_link = f"[{scr_new}](../01_screens/{scr_new}.md#{scr_new})"
    if uc_new:
        uc_link = f"[{uc_new}](../../01_requirements/02_business_usecases/{uc_new}.md#{uc_new})"
    else:
        uc_link = "—"
    it_cell = " ・ ".join(f"[{i}](../01_screens/{scr_new}.md#{i})" for i in its) if its else "—"
    if apis:
        api_cell = " ・ ".join(f"[{nm}]({href})" for nm, href in apis)
    else:
        api_cell = "—"
    if trans:
        tr_cell = " ・ ".join(f"[{t}](../01_screens/{t}.md#{t})" for t in trans)
    else:
        tr_cell = "—"

    L = []
    L.append(f'# <span id="{evt}"></span>{evt}: {label}')
    L.append("")
    L.append(f"> **画面 {scr_new} のイベント「{label}」を定義します。** 対応画面・対応業務UC・対象項目・呼出API・遷移先と、処理内容を記述します。")
    L.append("")
    L.append("*版数 v1.0 ・ 更新 2026-06-21 ・ 再構成 P3*")
    L.append("")
    L.append("## 項目")
    L.append("")
    L.append("| 項目 | 内容 |")
    L.append("|---|---|")
    L.append(f"| 画面イベントID | `{evt}` |")
    L.append(f"| イベント名 | {label} |")
    L.append(f"| 対応画面ID | {scr_link} |")
    L.append(f"| 対応業務UC | {uc_link} |")
    L.append(f"| 対象項目ID | {it_cell} |")
    L.append(f"| 呼出API | {api_cell} |")
    L.append(f"| 遷移先 | {tr_cell} |")
    L.append("")
    L.append("## 処理")
    L.append("")
    L.append(proc_fixed)
    L.append("")
    L.append("## 備考")
    L.append("")
    old_scr = new2old[scr_new]
    L.append(f"再構成 P3 で旧画面イベント `{old_scr}/{ev}`(現 {scr_new} §6 の `{ev}`)から導出。処理内容の正本は {scr_new} §6 と本ページ。")
    L.append("")
    return "\n".join(L)

# ---- §6 へ EVT 列を付与 -------------------------------------------------
def inject_evt_column(text, scr_new, ev2evt):
    tab_start, tab_end, table = split_section6(text)
    if table is None:
        return text, 0
    new_table = table
    # thead: イベント ID 列の前に EVT 列ヘッダを追加(冪等: 既に EVT 列があればスキップ)
    if "<th>EVT-ID</th>" not in new_table:
        new_table = new_table.replace(
            "<th>イベント ID</th>",
            "<th>EVT-ID</th>\n<th>イベント ID</th>", 1)
        # colgroup があれば 1 列追加
        if "<colgroup>" in new_table:
            new_table = new_table.replace(
                "<colgroup>",
                '<colgroup>\n<col style="width: 10%" />', 1)
    # tbody: 各行の先頭 <td><code>EV-nn</code></td> の前に EVT セルを挿入
    def row_sub(m):
        ev = m.group(1)
        evt = ev2evt.get(ev)
        if not evt:
            return m.group(0)
        evt_cell = f'<td><a href="../02_screen_events/{evt}.md#{evt}">{evt}</a></td>'
        # 既に直前に EVT セルがあれば二重付与しない(冪等)はループ外で担保
        return f'<tr>\n{evt_cell}\n<td><code>{ev}</code></td>'
    # 冪等: まず既存の EVT セルを除去してから再付与
    new_table = re.sub(
        r'<tr>\s*<td><a href="\.\./02_screen_events/EVT-\d+\.md#EVT-\d+">EVT-\d+</a></td>\s*(<td><code>EV-\d+</code></td>)',
        r'<tr>\n\1', new_table)
    new_table = re.sub(r'<tr>\s*(<td><code>(EV-\d+)</code></td>)',
                       lambda m: f'<tr>\n<td><a href="../02_screen_events/{ev2evt[m.group(2)]}.md#{ev2evt[m.group(2)]}">{ev2evt[m.group(2)]}</a></td>\n{m.group(1)}'
                                 if m.group(2) in ev2evt else m.group(0),
                       new_table)
    text = text[:tab_start] + new_table + text[tab_end:]
    return text, 1

# ---- SCR §1 へ「対応業務UC」行を追加 -----------------------------------
def inject_scr_ucs(text, scr_new, uc_list):
    if not uc_list:
        return text
    cell = " ・ ".join(
        f"[{uc}](../../01_requirements/02_business_usecases/{uc}.md#{uc})" for uc in uc_list)
    row = f"| 対応業務UC | {cell} |"
    # 既存行を置換(冪等)。
    if re.search(r'^\|\s*対応業務UC\s*\|', text, re.M):
        text = re.sub(r'^\|\s*対応業務UC\s*\|.*$', row, text, count=1, flags=re.M)
        return text
    # 「関連画面」行の直後に挿入する(同一の関連表内)。空白パディング許容。
    m = re.search(r'(?m)^\|\s*関連画面\s*\|.*$', text)
    if m:
        text = text[:m.end()] + "\n" + row + text[m.end():]
        return text
    # 関連画面行が無い場合は「FR / BR」行の直後へ。
    m = re.search(r'(?m)^\|\s*FR\s*/\s*BR\s*\|.*$', text)
    if m:
        text = text[:m.end()] + "\n" + row + text[m.end():]
    return text

# ---- メイン ------------------------------------------------------------
def main():
    os.makedirs(EVT_DIR, exist_ok=True)
    # 既存 EVT-*.md を一旦削除(再生成・冪等)
    for f in glob.glob(f"{EVT_DIR}/EVT-*.md"):
        os.remove(f)

    # evtmap を 新SCR 単位へ整理
    per_scr = {}   # new_scr -> list of (ev, evt)
    for key, evt in evtmap.items():
        old_scr, ev = key.split("/")
        new_scr = scrmap[old_scr]
        per_scr.setdefault(new_scr, []).append((ev, evt))
    for k in per_scr:
        per_scr[k].sort(key=lambda t: int(t[0].split("-")[1]))

    evt_records = []   # (evt, scr_new, label, uc_new)
    uc_link_count = 0
    issues_uc_missing = []

    for new_scr in sorted(per_scr, key=lambda s: int(s.split("-")[1])):
        scr_path = f"{SCR_DIR}/{new_scr}.md"
        text = open(scr_path, encoding="utf-8").read()
        # 既存の EVT 列があれば正準形へ戻してから解析(冪等・再実行安全)
        ts, te, table = split_section6(text)
        if table is not None:
            table = strip_evt_column(table)
            text = text[:ts] + table + text[te:]
        rows = parse_rows(table) if table else []
        rowmap = {r["ev"]: r for r in rows}
        old_scr = new2old[new_scr]
        ev2evt = {}
        scr_ucs = []
        for ev, evt in per_scr[new_scr]:
            r = rowmap.get(ev)
            if r is None:
                # §6 に該当行が無い(データ不整合)。空 EVT を生成。
                r = dict(ev=ev, item="—", name=f"{ev}", proc="—")
            # uc_crosswalk のキーは旧SCR id から先頭 'SCR-' を除いた形
            #   例 SCR-001 -> "001"、SCR-004-001 -> "004-001"、SCR-WIDGET -> "WIDGET"
            old_suffix = old_scr[len("SCR-"):]
            uc_old = f"UC-SCR-{old_suffix}-EV{ev.split('-')[1]}"
            uc_new = ucw.get(uc_old)
            if not uc_new:
                issues_uc_missing.append(f"{evt} ({new_scr}/{ev}) 旧UCキー {uc_old} が uc_crosswalk に無い")
            else:
                uc_link_count += 1
                scr_ucs.append(uc_new)
            ev2evt[ev] = evt
            body = build_evt_body(evt, ev, r["name"], new_scr, uc_new, r["item"], r["proc"])
            open(f"{EVT_DIR}/{evt}.md", "w", encoding="utf-8").write(body)
            evt_records.append((evt, new_scr, evt_label(r["name"]), uc_new))
        # §6 に EVT 列付与
        text, _ = inject_evt_column(text, new_scr, ev2evt)
        # §1 に 対応業務UC 行
        text = inject_scr_ucs(text, new_scr, scr_ucs)
        open(scr_path, "w", encoding="utf-8").write(text)

    write_index(evt_records, per_scr)
    print(f"EVT files: {len(evt_records)}")
    print(f"UC links (EVT with UC): {uc_link_count}")
    if issues_uc_missing:
        print("ISSUES (EVT without UC):")
        for x in issues_uc_missing:
            print("  -", x)
    else:
        print("ISSUES (EVT without UC): none")

def write_index(evt_records, per_scr):
    # 画面名取得
    def scr_h1(scr):
        for line in open(f"{SCR_DIR}/{scr}.md", encoding="utf-8"):
            if line.startswith("# "):
                return re.sub(r'<span[^>]*></span>', '', line[2:]).strip()
        return scr
    L = []
    L.append("# 画面イベント設計")
    L.append("")
    L.append("> **このセクションは、各画面(SCR)の画面イベントを `EVT-NNN` として個別に定義します。** 1 画面イベント = 1 ファイル。各 EVT は対応画面・対応業務UC(UC)・対象項目・呼出API・遷移先・処理内容を持ちます。")
    L.append("")
    L.append(f"*版数 v1.0 ・ 更新 2026-06-21 ・ イベント数 {len(evt_records)} ・ 再構成 P3*")
    L.append("")
    L.append("## 1. 画面別 EVT 一覧")
    L.append("")
    L.append("画面(SCR)ごとに、その画面イベント `EVT-NNN` を列挙します。")
    L.append("")
    by_scr = {}
    for evt, scr, label, uc in evt_records:
        by_scr.setdefault(scr, []).append((evt, label, uc))
    for scr in sorted(by_scr, key=lambda s: int(s.split("-")[1])):
        title = scr_h1(scr)
        L.append(f"### <span id=\"{scr}\"></span>{title}")
        L.append("")
        L.append("| EVT-ID | イベント名 | 対応業務UC |")
        L.append("|---|---|---|")
        for evt, label, uc in by_scr[scr]:
            uc_cell = f"[{uc}](../../01_requirements/02_business_usecases/{uc}.md#{uc})" if uc else "—"
            L.append(f"| [`{evt}`]({evt}.md#{evt}) | {label} | {uc_cell} |")
        L.append("")
    L.append("## 2. EVT ↔ 業務UC 対応表")
    L.append("")
    L.append("画面イベント `EVT-NNN` と業務ユースケース `UC-PPP` の 1:1 対応です。")
    L.append("")
    L.append("| EVT-ID | 対応画面 | 対応業務UC |")
    L.append("|---|---|---|")
    for evt, scr, label, uc in sorted(evt_records, key=lambda r: int(r[0].split("-")[1])):
        uc_cell = f"[{uc}](../../01_requirements/02_business_usecases/{uc}.md#{uc})" if uc else "—"
        L.append(f"| [`{evt}`]({evt}.md#{evt}) | [{scr}](../01_screens/{scr}.md#{scr}) | {uc_cell} |")
    L.append("")
    open(f"{EVT_DIR}/index.md", "w", encoding="utf-8").write("\n".join(L))

if __name__ == "__main__":
    main()
