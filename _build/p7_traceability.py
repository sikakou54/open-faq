#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P7 トレーサビリティマトリクス生成(業務UC統合後・新方式)。

旧版は UC 本文の `## 関連`(関連画面ID 等)を読んでいたが、業務UC再編成で UC 本文から
基本設計 ID を除去したため、設計列は **基本設計側の逆引き** から集計する方式へ改修した。

ソース:
  - 要件列(FR/BR/RULE): 新 UC 本文の `## 対応する機能要件ID / ## 対応する業務要件ID /
    ## 関連する業務ルールID` を解析。
  - 設計列(SCR/EVT/API/TBL/SEQ): 各基本設計ファイルの `対応業務UC`(TBL は逆引き、
    SEQ は `対応業務ユースケース`)を新UC単位に反転集計。

出力: 99_management/02_traceability_matrix.md(1 行 = 1 業務UC) + p7_linkgraph.json。
実行: python3 _build/p7_traceability.py
"""
import os, re, json, glob
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UCDIR = os.path.join(ROOT, "01_requirements", "04_business_usecases")
FRDIR = os.path.join(ROOT, "01_requirements", "02_FunctionalRequirement")
BRDIR = os.path.join(ROOT, "01_requirements", "01_BusinessRequirement")
RULEFILE = os.path.join(BRDIR, "08_rule.md")
SCRDIR = os.path.join(ROOT, "02_basic_design", "01_screens")
EVTDIR = os.path.join(ROOT, "02_basic_design", "02_screen_events")
APIDIR = os.path.join(ROOT, "02_basic_design", "03_apis")
TBLDIR = os.path.join(ROOT, "02_basic_design", "04_database")
SEQDIR = os.path.join(ROOT, "02_basic_design", "05_sequences")
PERMDIR = os.path.join(ROOT, "02_basic_design", "06_permissions")
MGMT = os.path.join(ROOT, "99_management")


def read(p):
    return open(p, encoding="utf-8").read()


def natkey(s):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]


def ids_in(text, prefix):
    seen = []
    for m in re.finditer(rf'(?<![A-Za-z0-9])({prefix}-\d+)(?![0-9])', text):
        if m.group(1) not in seen:
            seen.append(m.group(1))
    return seen


def section(text, heading):
    """`## <heading>` 直後〜次の `## ` 直前のテキストを返す。"""
    m = re.search(rf'^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)', text, re.M | re.S)
    return m.group(1) if m else ""


def row_cell(text, label):
    m = re.search(rf'\|\s*{re.escape(label)}\s*\|\s*(.*?)\s*\|', text)
    return m.group(1) if m else ""


def scan_id_file(directory, prefix, suffix):
    out = {}
    for f in sorted(glob.glob(os.path.join(directory, f"*{suffix}"))):
        for mid in re.findall(rf'id="({prefix}-\d+)"', read(f)):
            out[mid] = os.path.basename(f)
    return out


def parse():
    g = dict(uc={}, fr=set(), br=set(), rule=set())
    fr_file = scan_id_file(FRDIR, "FR", "-fr.md")
    br_file = scan_id_file(BRDIR, "BR", "-br.md")
    g["fr_file"], g["br_file"] = fr_file, br_file
    g["fr"], g["br"] = set(fr_file), set(br_file)
    g["rule"] = set(ids_in(read(RULEFILE), "RULE"))

    # UC 本文: 要件列
    for f in sorted(glob.glob(os.path.join(UCDIR, "UC-*.md")), key=natkey):
        ucid = os.path.basename(f)[:-3]
        t = read(f)
        m = re.search(r'#\s*<span id="' + ucid + r'"></span>' + ucid + r':\s*(.+)', t)
        name = m.group(1).strip() if m else ""
        g["uc"][ucid] = dict(
            name=name,
            fr=ids_in(section(t, "対応する機能要件ID"), "FR"),
            br=ids_in(section(t, "対応する業務要件ID"), "BR"),
            rule=ids_in(section(t, "関連する業務ルールID"), "RULE"),
            scr=[], evt=[], api=[], tbl=[], seq=[], perm=[],
        )

    # 基本設計の逆引きを UC 単位へ反転
    def attach(directory, suffix, label, key):
        for f in sorted(glob.glob(os.path.join(directory, f"{suffix}-*.md")), key=natkey):
            did = os.path.basename(f)[:-3]
            for uc in ids_in(row_cell(read(f), label), "UC"):
                if uc in g["uc"] and did not in g["uc"][uc][key]:
                    g["uc"][uc][key].append(did)

    attach(SCRDIR, "SCR", "対応業務UC", "scr")
    attach(EVTDIR, "EVT", "対応業務UC", "evt")
    attach(APIDIR, "API", "対応業務UC", "api")
    attach(TBLDIR, "TBL", "対応業務UC(逆引き)", "tbl")
    attach(SEQDIR, "SEQ", "対応業務ユースケース", "seq")
    attach(PERMDIR, "PERM", "対応業務UC", "perm")
    for uc in g["uc"]:
        for k in ("scr", "evt", "api", "tbl", "seq", "perm"):
            g["uc"][uc][k].sort(key=natkey)
    return g


def main():
    g = parse()
    fr_file, br_file = g["fr_file"], g["br_file"]

    def req_links(d):
        out = []
        for x in d["br"]:
            out.append(f"[{x}](../01_requirements/01_BusinessRequirement/{br_file.get(x,'')}#{x})")
        for x in d["fr"]:
            out.append(f"[{x}](../01_requirements/02_FunctionalRequirement/{fr_file.get(x,'')}#{x})")
        for x in d["rule"]:
            out.append(f"[{x}](../01_requirements/01_BusinessRequirement/08_rule.md#{x})")
        return " ".join(out) or "—"

    def dlinks(ids, sub, sd):
        return " ".join(f"[{x}](../02_basic_design/{sd}/{x}.md#{x})" for x in ids) or "—"

    rows = []
    for ucid in sorted(g["uc"], key=natkey):
        d = g["uc"][ucid]
        has_req = bool(d["fr"] or d["br"])
        has_design = bool(d["scr"] or d["evt"] or d["api"] or d["tbl"] or d["seq"] or d["perm"])
        if not has_req:
            state, note = "要件未反映", "対応要件ID 無し"
        elif not has_design:
            state, note = "基本設計未反映", "SCR/EVT/API/TBL/SEQ/PERM いずれも無し"
        else:
            state, note = "OK", "—"
        rows.append((ucid, d, state, note))

    out = []
    out.append("<!-- portal-top -->")
    out.append("[設計ポータル](../README.md) ／ [保守・運用](index.md) ／ **トレーサビリティマトリクス**")
    out.append("<!-- /portal-top -->")
    out.append("")
    out.append("# トレーサビリティマトリクス(業務UC→要件 / 基本設計)")
    out.append("")
    out.append("> **このページは 業務UC を起点に、要件(BR/FR/RULE)と基本設計(画面 / 画面イベント / API / テーブル / シーケンス)の対応を一覧します。** "
               "業務ユースケース(UC)単位で 1 行を起こします。要件列は UC 本文、基本設計列は各設計ファイルの逆引き(`対応業務UC`)から集計します。")
    out.append("")
    out.append("*再構成 P8(業務UC統合) ・ 生成 `_build/p7_traceability.py`(決定論的・冪等)*")
    out.append("")
    out.append("> [!NOTE]")
    out.append("> **本マトリクスは自動生成物です。** UC 本文は要件(BR/FR/RULE)のみを保持し、画面・API・DB・シーケンスとの対応は本表(基本設計側の逆引き集計)で管理します。"
               "再生成は `python3 _build/p7_traceability.py`。")
    out.append("")
    from collections import Counter
    cnt = Counter(s for _, _, s, _ in rows)
    out.append("## サマリ")
    out.append("")
    out.append(f"- 行数(業務UC 単位): {len(rows)}")
    out.append("- 状態内訳: " + " / ".join(f"{k} {v}" for k, v in sorted(cnt.items())))
    out.append("")
    out.append("## マトリクス")
    out.append("")
    out.append("| 業務UC | 要件(BR/FR/RULE) | 画面 | 画面イベント | API | テーブル | シーケンス | 権限 | 状態 |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for ucid, d, state, note in rows:
        uc_l = f"[{ucid}](../01_requirements/04_business_usecases/{ucid}.md#{ucid})"
        out.append("| " + " | ".join([
            uc_l, req_links(d),
            dlinks(d["scr"], "SCR", "01_screens"),
            dlinks(d["evt"], "EVT", "02_screen_events"),
            dlinks(d["api"], "API", "03_apis"),
            dlinks(d["tbl"], "TBL", "04_database"),
            dlinks(d["seq"], "SEQ", "05_sequences"),
            dlinks(d["perm"], "PERM", "06_permissions"),
            state,
        ]) + " |")
    out.append("")
    out.append("<!-- portal-bottom -->")
    out.append("[← 保守・運用](index.md) ・ [↑ 設計ポータル](../README.md)")
    out.append("<!-- /portal-bottom -->")
    out.append("")
    open(os.path.join(MGMT, "02_traceability_matrix.md"), "w", encoding="utf-8").write("\n".join(out))

    graph = {uc: {k: v for k, v in d.items()} for uc, d in g["uc"].items()}
    open(os.path.join(MGMT, "p7_linkgraph.json"), "w", encoding="utf-8").write(
        json.dumps(graph, ensure_ascii=False, indent=1))

    print(f"matrix rows (業務UC): {len(rows)}")
    print("  state:", dict(cnt))
    # 簡易ギャップ列挙
    no_design = [u for u, d, s, n in rows if s == "基本設計未反映"]
    no_req = [u for u, d, s, n in rows if s == "要件未反映"]
    if no_req:
        print("  要件未反映:", " ".join(no_req))
    if no_design:
        print("  基本設計未反映:", " ".join(no_design))


if __name__ == "__main__":
    main()
