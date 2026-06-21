#!/usr/bin/env python3
"""P7 トレーサビリティ確立ツール(決定論的・冪等)。

役割:
  1. 全ファイルの構造化リンク・項目表を正規表現で解析し、リンクグラフを構築。
     UC→FR/BR、UC→SCR/EVT/API/TBL、EVT→SCR/API/UC、API→UC/SCR/EVT/TBL、TBL→UC/API。
  2. 要件ファイル(FR-/BR-NNN.md)の `## 関連` 「対応業務UC」プレースホルダを、
     当該要件を `対応要件ID` に持つ UC-NNN へのリンク群で充足(逆引き)。
  3. 一気通貫マトリクス(99_management/02_traceability_matrix.md)を生成。
  4. ギャップ検出(分類別)。
  5. 確定 ID は変更しない(逆引き欄の充足のみ本文編集)。

実行: python3 _build/p7_traceability.py   (リポジトリルートで)
"""
import os
import re
import glob
import json
import html
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "01_requirements", "01_specifications")
UCDIR = os.path.join(ROOT, "01_requirements", "02_business_usecases")
EVTDIR = os.path.join(ROOT, "02_basic_design", "02_screen_events")
APIDIR = os.path.join(ROOT, "02_basic_design", "03_apis")
TBLDIR = os.path.join(ROOT, "02_basic_design", "04_database")
SCRDIR = os.path.join(ROOT, "02_basic_design", "01_screens")
MGMT = os.path.join(ROOT, "99_management")

PLACEHOLDER = "(P2 で付与)"
GAP_LABEL = "(該当UCなし=ギャップ)"


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def ids_in(text, prefix):
    """本文中に出現する <prefix>-NNN を出現順に重複排除して返す。"""
    seen = []
    for m in re.finditer(rf'(?<![A-Za-z0-9])({prefix}-\d+)(?![0-9])', text):
        v = m.group(1)
        if v not in seen:
            seen.append(v)
    return seen


def natkey(s):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]


def row_cell(text, label):
    """| <label> | <cell> | 形式の行から cell を返す(無ければ '')。"""
    m = re.search(rf'\|\s*{re.escape(label)}\s*\|\s*(.*?)\s*\|', text)
    return m.group(1) if m else ""


# ---------------------------------------------------------------------------
# 1. 解析
# ---------------------------------------------------------------------------
def parse():
    g = {
        "uc": {},   # UC-NNN -> dict(req, scr, evt, api, tbl, name)
        "evt": {},  # EVT-NNN -> dict(scr, uc, api)
        "api": {},  # API-NNN -> dict(uc, scr, evt, tbl)
        "tbl": {},  # TBL-NNN -> dict(uc, api)
        "fr": set(),
        "br": set(),
        "fr_to_br": {},  # FR-NNN -> [BR-NNN, ...](関連業務要件)
    }

    for f in glob.glob(os.path.join(SPEC, "FR-*.md")):
        frid = os.path.basename(f)[:-3]
        g["fr"].add(frid)
        # FR の `関連業務要件` 列 = 親 BR(複数あり得る)。本文全体から BR を抽出。
        g["fr_to_br"][frid] = ids_in(read(f), "BR")
    for f in glob.glob(os.path.join(SPEC, "BR-*.md")):
        g["br"].add(os.path.basename(f)[:-3])

    for f in sorted(glob.glob(os.path.join(UCDIR, "UC-*.md")), key=lambda x: natkey(x)):
        ucid = os.path.basename(f)[:-3]
        t = read(f)
        name = ""
        m = re.search(r'#\s*<span id="' + ucid + r'"></span>' + ucid + r':\s*(.+)', t)
        if m:
            name = m.group(1).strip()
        reqcell = row_cell(t, "対応要件ID")
        req = ids_in(reqcell, "FR") + ids_in(reqcell, "BR")
        scr = ids_in(row_cell(t, "関連画面ID"), "SCR")
        evt = ids_in(row_cell(t, "関連画面イベントID"), "EVT")
        api = ids_in(row_cell(t, "関連API ID"), "API")
        tbl = ids_in(row_cell(t, "関連テーブルID"), "TBL")
        g["uc"][ucid] = dict(req=req, scr=scr, evt=evt, api=api, tbl=tbl, name=name)

    for f in sorted(glob.glob(os.path.join(EVTDIR, "EVT-*.md")), key=lambda x: natkey(x)):
        eid = os.path.basename(f)[:-3]
        t = read(f)
        g["evt"][eid] = dict(
            scr=ids_in(row_cell(t, "対応画面ID"), "SCR"),
            uc=ids_in(row_cell(t, "対応業務UC"), "UC"),
            api=ids_in(row_cell(t, "呼出API"), "API"),
        )

    for f in sorted(glob.glob(os.path.join(APIDIR, "API-*.md")), key=lambda x: natkey(x)):
        aid = os.path.basename(f)[:-3]
        t = read(f)
        # 利用テーブルは `## 利用テーブル` 以降のセクションに出現
        tblsec = t.split("## 利用テーブル", 1)
        tbl = ids_in(tblsec[1], "TBL") if len(tblsec) > 1 else []
        g["api"][aid] = dict(
            uc=ids_in(row_cell(t, "対応業務UC"), "UC"),
            scr=ids_in(row_cell(t, "対応画面ID"), "SCR"),
            evt=ids_in(row_cell(t, "対応画面イベントID"), "EVT"),
            tbl=tbl,
        )

    for f in sorted(glob.glob(os.path.join(TBLDIR, "TBL-*.md")), key=lambda x: natkey(x)):
        tid = os.path.basename(f)[:-3]
        t = read(f)
        g["tbl"][tid] = dict(
            uc=ids_in(row_cell(t, "対応業務UC(逆引き)"), "UC"),
            api=ids_in(row_cell(t, "利用API(逆引き)"), "API"),
        )

    return g


# ---------------------------------------------------------------------------
# 2. 要件→UC 逆引き
# ---------------------------------------------------------------------------
def build_req_to_uc(g):
    """要件→UC 逆引きを構築。

    - FR→UC: UC の `対応要件ID` が FR を直接参照する(順引き)逆引き。
    - BR→UC: UC は BR を直接参照しないため、BR を親に持つ FR の UC を継承する
      (FR の `関連業務要件` = 親 BR を経由した推移トレース)。
    """
    r2u = defaultdict(list)
    # FR の直接逆引き
    for ucid, d in g["uc"].items():
        for rid in d["req"]:
            r2u[rid].append(ucid)
    # BR は親子(FR→BR)を経由して FR の UC を継承
    for frid, brs in g["fr_to_br"].items():
        for brid in brs:
            r2u[brid].extend(r2u.get(frid, []))
    for rid in list(r2u):
        r2u[rid] = sorted(set(r2u[rid]), key=natkey)
    return r2u


def uc_link_spec(ucid):
    return f"[{ucid}](../02_business_usecases/{ucid}.md#{ucid})"


def fill_requirements(g, r2u):
    """各 FR/BR の 対応業務UC プレースホルダを逆引き UC 群で置換。"""
    filled = 0
    gap_files = []
    for f in sorted(glob.glob(os.path.join(SPEC, "FR-*.md")) +
                    glob.glob(os.path.join(SPEC, "BR-*.md")), key=lambda x: natkey(x)):
        rid = os.path.basename(f)[:-3]
        t = read(f)
        if PLACEHOLDER not in t:
            continue
        ucs = r2u.get(rid, [])
        if ucs:
            repl = " ・ ".join(uc_link_spec(u) for u in ucs)
        else:
            repl = GAP_LABEL
            gap_files.append(rid)
        t = t.replace(PLACEHOLDER, repl)
        write(f, t)
        filled += 1
    return filled, gap_files


# ---------------------------------------------------------------------------
# 3. マトリクス生成
# ---------------------------------------------------------------------------
def fmt_list(items):
    return " ".join(items) if items else "—"


def build_matrix(g, r2u):
    rows = []
    # UC 単位で行を起こし、チェーンを結線
    for ucid in sorted(g["uc"], key=natkey):
        d = g["uc"][ucid]
        req = d["req"]
        evt = d["evt"]
        scr = d["scr"]
        api = d["api"]
        tbl = d["tbl"]
        # 状態判定
        notes = []
        if not req:
            state = "要件定義未反映"
            notes.append("対応要件ID 無し")
        elif not (scr or evt or api or tbl):
            state = "基本設計未反映"
            notes.append("画面/EVT/API/TBL いずれも無し")
        else:
            state = "OK"
        # 双方向確認: UC が参照する要件が逆引きで UC を含むか
        for rid in req:
            if ucid not in r2u.get(rid, []):
                notes.append(f"{rid} 逆引き不整合")
                state = "要確認"
        rows.append(dict(uc=ucid, req=req, scr=scr, evt=evt, api=api, tbl=tbl,
                         state=state, note=" / ".join(notes) if notes else "—"))
    return rows


def write_matrix(rows, g, gaps):
    out = []
    out.append("<!-- portal-top -->")
    out.append("[設計ポータル](../README.md) ／ [保守・運用](index.md) ／ **トレーサビリティマトリクス**")
    out.append("<!-- /portal-top -->")
    out.append("")
    out.append("# トレーサビリティマトリクス(要件→業務UC→画面→画面イベント→API→テーブル)")
    out.append("")
    out.append("> **このページは 要件→業務UC→画面→画面イベント→API→テーブル の一気通貫トレーサビリティを定義します。** "
               "業務ユースケース(UC)単位で 1 行を起こし、各 UC が参照する 対応要件 / 画面 / 画面イベント / API / テーブルを結線します。")
    out.append("")
    out.append("*版数 v1.0 ・ 更新 2026-06-21 ・ 再構成 P7 ・ 生成 `_build/p7_traceability.py`(決定論的・冪等)*")
    out.append("")
    out.append("> [!NOTE]")
    out.append("> **本マトリクスは自動生成物です。** 各 ID 定義の正本は各層のファイル(要件仕様 / 業務UC / 画面イベント / API / DB)です。"
               "本ページは結線(リンクグラフ)の俯瞰であり、ID の変更は行いません。再生成は `python3 _build/p7_traceability.py`。")
    out.append("")
    # 状態凡例
    out.append("## 状態凡例")
    out.append("")
    out.append("| 状態 | 意味 |")
    out.append("|---|---|")
    out.append("| OK | 要件・基本設計まで結線済み |")
    out.append("| 要確認 | 逆引き不整合など要確認 |")
    out.append("| 要件定義未反映 | UC に対応要件ID が無い(要件トレース欠落) |")
    out.append("| 基本設計未反映 | UC に画面/EVT/API/TBL がいずれも無い |")
    out.append("")
    # サマリ
    from collections import Counter
    cnt = Counter(r["state"] for r in rows)
    out.append("## サマリ")
    out.append("")
    out.append(f"- 行数(UC 単位): {len(rows)}")
    out.append(f"- 状態内訳: " + " / ".join(f"{k} {v}" for k, v in sorted(cnt.items())))
    out.append("")
    # 本体
    out.append("## マトリクス")
    out.append("")
    out.append("UC 単位の行。各セルは当該 UC が参照する ID 群(リンクは正本へ)。")
    out.append("")
    out.append("| 業務UC | 要件ID | 画面ID | 画面イベントID | API ID | テーブルID | 状態 | 備考 |")
    out.append("|---|---|---|---|---|---|---|---|")
    for r in rows:
        uc_l = f"[{r['uc']}](../01_requirements/02_business_usecases/{r['uc']}.md#{r['uc']})"
        req_l = " ".join(req_link(x) for x in r["req"]) or "—"
        scr_l = " ".join(f"[{x}](../02_basic_design/01_screens/{x}.md#{x})" for x in r["scr"]) or "—"
        evt_l = " ".join(f"[{x}](../02_basic_design/02_screen_events/{x}.md#{x})" for x in r["evt"]) or "—"
        api_l = " ".join(f"[{x}](../02_basic_design/03_apis/{x}.md#{x})" for x in r["api"]) or "—"
        tbl_l = " ".join(f"[{x}](../02_basic_design/04_database/{x}.md#{x})" for x in r["tbl"]) or "—"
        out.append(f"| {uc_l} | {req_l} | {scr_l} | {evt_l} | {api_l} | {tbl_l} | {r['state']} | {r['note']} |")
    out.append("")
    out.append("<!-- portal-bottom -->")
    out.append("[← 保守・運用](index.md) ・ [↑ 設計ポータル](../README.md)")
    out.append("<!-- /portal-bottom -->")
    out.append("")
    write(os.path.join(MGMT, "02_traceability_matrix.md"), "\n".join(out))


def req_link(rid):
    return f"[{rid}](../01_requirements/01_specifications/{rid}.md#{rid})"


# ---------------------------------------------------------------------------
# 4. ギャップ検出
# ---------------------------------------------------------------------------
def detect_gaps(g, r2u):
    gaps = defaultdict(list)

    # FR/BR で UC 無し
    for rid in sorted(g["fr"] | g["br"], key=natkey):
        if not r2u.get(rid):
            gaps["要件→UC 無し(逆引きギャップ)"].append(rid)

    # UC で 対応要件ID 無し
    for ucid in sorted(g["uc"], key=natkey):
        if not g["uc"][ucid]["req"]:
            gaps["UC→要件 無し"].append(ucid)

    # UC が参照する要件が逆引きで自分を含まない(整合性)
    for ucid in sorted(g["uc"], key=natkey):
        for rid in g["uc"][ucid]["req"]:
            if rid not in (g["fr"] | g["br"]):
                gaps["UC→要件 リンク先不在"].append(f"{ucid}→{rid}")

    # EVT で UC 無し
    for eid in sorted(g["evt"], key=natkey):
        if not g["evt"][eid]["uc"]:
            gaps["EVT→UC 無し"].append(eid)

    # API で EVT 無し / UC 無し
    for aid in sorted(g["api"], key=natkey):
        if not g["api"][aid]["uc"]:
            gaps["API→UC 無し"].append(aid)
        if not g["api"][aid]["evt"]:
            gaps["API→EVT 無し"].append(aid)

    # TBL で API 無し / UC 無し
    for tid in sorted(g["tbl"], key=natkey):
        if not g["tbl"][tid]["uc"]:
            gaps["TBL→UC 無し"].append(tid)
        if not g["tbl"][tid]["api"]:
            gaps["TBL→API 無し"].append(tid)

    # 欠番チェック(連番)
    def missing(prefix, items):
        nums = sorted(int(x.split("-")[1]) for x in items)
        if not nums:
            return []
        full = set(range(1, nums[-1] + 1))
        return [f"{prefix}-{n:03d}" for n in sorted(full - set(nums))]

    for prefix, items in (("FR", g["fr"]), ("BR", g["br"]),
                          ("UC", set(g["uc"])), ("EVT", set(g["evt"])),
                          ("API", set(g["api"])), ("TBL", set(g["tbl"]))):
        mz = missing(prefix, items)
        if mz:
            gaps[f"{prefix} 欠番"].extend(mz)

    return gaps


def main():
    g = parse()
    r2u = build_req_to_uc(g)
    filled, gap_files = fill_requirements(g, r2u)
    rows = build_matrix(g, r2u)
    gaps = detect_gaps(g, r2u)
    write_matrix(rows, g, gaps)

    # 機械可読リンクグラフを出力(再現性 / 後続フェーズ用)
    graph_out = {
        "uc": g["uc"], "evt": g["evt"], "api": g["api"], "tbl": g["tbl"],
        "req_to_uc": {k: r2u[k] for k in sorted(r2u, key=natkey)},
    }
    write(os.path.join(MGMT, "p7_linkgraph.json"),
          json.dumps(graph_out, ensure_ascii=False, indent=1))

    # サマリ標準出力
    print(f"matrix rows (UC): {len(rows)}")
    print(f"requirements filled (対応業務UC): {filled}")
    print(f"  of which gap (該当UCなし): {len(gap_files)}")
    if gap_files:
        print("  gap requirement IDs:", " ".join(gap_files))
    print("gap categories:")
    for k in sorted(gaps):
        print(f"  {k}: {len(gaps[k])}  {' '.join(gaps[k][:15])}{' ...' if len(gaps[k])>15 else ''}")

    # ギャップを JSON でも残す
    write(os.path.join(MGMT, "p7_gaps.json"),
          json.dumps({k: gaps[k] for k in sorted(gaps)}, ensure_ascii=False, indent=1))
    return g, r2u, rows, gaps, filled, gap_files


if __name__ == "__main__":
    main()
