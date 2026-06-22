#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2: 操作粒度の業務ユースケースを UC-NNN.. のフラット連番・1ファイルで確立する。
入力: 01_requirements/02_business_usecases/UC-SCR-*.md(画面イベント節)/ UC-SYSTEM-*.md
出力: UC-001..UC-NNN.md(15項目テンプレ)/ index.md / 99_management/uc_crosswalk.json
採番: 画面順(自然順)×イベント順 → UC-SYSTEM 順。ゼロ詰め3桁・欠番なし。
決定論的: 既存節の内容を流用・再構成する。
"""
import glob, re, os, json

BIZUC = "01_requirements/02_business_usecases"


def natkey(s):
    if s.endswith(".md"):
        s = s[:-3]
    return [int(t) if t.isdigit() else t for t in re.findall(r"\d+|\D+", s)]


# ---- 論理テーブル名 -> TBL-ID マップ(DB 設計の各 TBL ファイル H1 主名から) ----
def build_tbl_map():
    m = {}
    for f in glob.glob("02_basic_design/04_database/TBL-*.md"):
        tid = os.path.basename(f)[:-3]
        s = open(f, encoding="utf-8").read()
        h1 = re.search(r"^# (?:<span[^>]*></span>)?(.+)$", s, re.M)
        if not h1:
            continue
        for name in re.findall(r"\b((?:M|T|H|TP)_[A-Z0-9_]+)\b", h1.group(1)):
            m[name] = tid
    return m


TBL_MAP = build_tbl_map()


# ---- API-ID -> ファイル名 マップ(API 設計ファイルの実アンカーから) ----
def build_api_map():
    m = {}
    for f in glob.glob("02_basic_design/03_apis/API-*.md"):
        s = open(f, encoding="utf-8").read()
        for aid in re.findall(r'id="(API-[A-Z]+-\d+)"', s):
            m[aid] = os.path.basename(f)
    return m


API_MAP = build_api_map()


def split_event_sections(text):
    """UC-SCR ファイル本文を ### イベント節に分割して返す [(ucid, name, body), ...]"""
    out = []
    # 見出し: ### <span id="UC-SCR-XXX-EVnn"></span>UC-SCR-XXX-EVnn 名称
    pat = re.compile(
        r'^### <span id="(UC-SCR-[A-Z0-9-]+-EV\d+)"></span>\1\s*(.*?)\s*$', re.M
    )
    ms = list(pat.finditer(text))
    for i, mm in enumerate(ms):
        ucid = mm.group(1)
        name = mm.group(2).strip()
        start = mm.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        body = text[start:end]
        # 末尾のナビ/区切りを除去
        body = re.split(r"\n---\n", body)[0]
        body = re.sub(r"<!-- portal-bottom -->.*$", "", body, flags=re.S)
        out.append((ucid, name, body.strip()))
    return out


def parse_meta_table(body):
    """| 項目 | 内容 | 形式の行から各キー値を取り出す"""
    d = {}
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$", body, re.M):
        k = m.group(1).strip()
        v = m.group(2).strip()
        if k in ("利用者", "事前条件", "トリガー", "事後条件", "関連", "アクター", "目的"):
            d[k] = v
    return d


def grab_block(body, label):
    """**ラベル** 直後のブロック本文(次の **ラベル** か末尾まで)"""
    m = re.search(
        r"\*\*" + re.escape(label) + r"\*\*\s*\n(.*?)(?=\n\*\*[^*\n]+\*\*\s*\n|\Z)",
        body,
        re.S,
    )
    return m.group(1).strip() if m else ""


def grab_section(body, num_label):
    """## N. ラベル 直後のブロック本文(次の ## まで)"""
    m = re.search(
        r"^## " + re.escape(num_label) + r"\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M
    )
    return m.group(1).strip() if m else ""


def first_quote_summary(body):
    m = re.search(r"^>\s*\*\*概要\*\*\s*(.+?)\s*$", body, re.M)
    if m:
        return m.group(1).strip()
    return ""


def collect_refs(*texts):
    """テキスト群から FR / API / SCR / 論理テーブル名 を収集"""
    fr, api, scr, tbl = [], [], [], []
    joined = "\n".join(t for t in texts if t)
    for r in re.findall(r"\b(FR-\d+)\b", joined):
        if r not in fr:
            fr.append(r)
    for r in re.findall(r"\b(API-[A-Z]+-\d+)\b", joined):
        if r in API_MAP and r not in api:  # 実在する API アンカーのみ採用
            api.append(r)
    for r in re.findall(r"\b(SCR-(?:WIDGET|\d{3}(?:-\d{3})?))\b", joined):
        if r not in scr:
            scr.append(r)
    for name in re.findall(r"\b((?:M|T|H|TP)_[A-Z0-9_]+)\b", joined):
        tid = TBL_MAP.get(name)
        if tid and tid not in [t[1] for t in tbl]:
            tbl.append((name, tid))
    return fr, api, scr, tbl


def fr_link(fr):
    return f"[{fr}](../01_specifications/{fr}.md#{fr})"


def api_link(a):
    fn = API_MAP[a]  # 実在アンカーのみ呼ばれる(collect_refs でフィルタ済み)
    return f"[{a}](../../02_basic_design/03_apis/{fn}#{a})"


def scr_link(s):
    anchor = "WIDGET" if s == "SCR-WIDGET" else s
    return f"[{s}](../../02_basic_design/01_screens/{s}.md#{anchor})"


def tbl_link(name, tid):
    # 注: 現行の TBL ファイルには #TBL-xxx アンカーが未付与(P5 で付与予定)のため、
    # 壊れアンカーを避けてファイルへリンクする(フラグメント無し)。
    return f"`{name}` = [{tid}](../../02_basic_design/04_database/{tid}.md)"


def md_escape_pipe(s):
    return s.replace("|", "\\|")


def render_uc(num, src):
    """src: dict with keys uc_name, actor, purpose, frs, pre, basic, alt, exc, post,
    scrs, apis, tbls, ev_notes, summary, src_id"""
    ucid = f"UC-{num:03d}"
    L = []
    L.append(f'# <span id="{ucid}"></span>{ucid}: {src["uc_name"]}')
    L.append("")
    L.append(f"> **{src['summary']}**")
    L.append("")
    L.append(f"*主アクター {src['actor']} ・ ステータス ドラフト ・ 再構成 P2*")
    L.append("")
    # 項目表
    fr_cell = " ・ ".join(fr_link(f) for f in src["frs"]) if src["frs"] else "—"
    L.append("| 項目 | 内容 |")
    L.append("|---|---|")
    L.append(f"| 業務ユースケースID | {ucid} |")
    L.append(f"| 業務ユースケース名 | {md_escape_pipe(src['uc_name'])} |")
    L.append(f"| 対応要件ID | {fr_cell} |")
    L.append(f"| 主アクター | {md_escape_pipe(src['actor'])} |")
    L.append(f"| 目的 | {md_escape_pipe(src['purpose'])} |")
    L.append("")
    # 事前条件
    L.append("## 事前条件")
    L.append("")
    L.append(src["pre"] if src["pre"] else "—")
    L.append("")
    # 基本フロー
    L.append("## 基本フロー")
    L.append("")
    L.append(src["basic"] if src["basic"] else "—")
    L.append("")
    # 代替フロー
    L.append("## 代替フロー")
    L.append("")
    L.append(src["alt"] if src["alt"] else "—")
    L.append("")
    # 例外フロー
    L.append("## 例外フロー")
    L.append("")
    L.append(src["exc"] if src["exc"] else "—")
    L.append("")
    # 事後条件
    L.append("## 事後条件")
    L.append("")
    L.append(src["post"] if src["post"] else "—")
    L.append("")
    # 関連
    L.append("## 関連")
    L.append("")
    L.append("| 関連区分 | 内容 |")
    L.append("|---|---|")
    scr_cell = " ・ ".join(scr_link(s) for s in src["scrs"]) if src["scrs"] else "—"
    L.append(f"| 関連画面ID | {scr_cell} |")
    L.append(f"| 関連画面イベントID | {src['ev_notes']} |")
    api_cell = " ・ ".join(api_link(a) for a in src["apis"]) if src["apis"] else "—"
    L.append(f"| 関連API ID | {api_cell} |")
    tbl_cell = (
        " ・ ".join(tbl_link(n, t) for n, t in src["tbls"]) if src["tbls"] else "—"
    )
    L.append(f"| 関連テーブルID | {tbl_cell} |")
    L.append("")
    # 備考
    L.append("## 備考")
    L.append("")
    L.append(src["remark"])
    L.append("")
    return ucid, "\n".join(L)


def main():
    records = []  # (old_id, src_dict)

    # ---- 画面起点 UC-SCR ----
    scr_files = sorted(
        glob.glob(f"{BIZUC}/UC-SCR-*.md"), key=lambda p: natkey(os.path.basename(p))
    )
    for f in scr_files:
        text = open(f, encoding="utf-8").read()
        scr_of_file = re.search(r"UC-SCR-([A-Z0-9-]+)\.md", os.path.basename(f)).group(1)
        for ucid_old, name, body in split_event_sections(text):
            meta = parse_meta_table(body)
            summary = first_quote_summary(body) or f"画面イベント {ucid_old} に対応する業務ユースケースを定義します。"
            basic = grab_block(body, "基本フロー")
            exc = grab_block(body, "異常系フロー")
            pre = meta.get("事前条件", "—")
            post = meta.get("事後条件", "—")
            actor = meta.get("利用者", "—")
            trigger = meta.get("トリガー", "")
            related = meta.get("関連", "")
            # 目的: 概要文をそのまま目的に流用(末尾整形)
            purpose = summary
            # refs
            frs, apis, scrs, tbls = collect_refs(related, basic, exc, body)
            # 画面: ファイルの SCR を先頭に
            this_scr = "SCR-" + scr_of_file
            if this_scr not in scrs:
                scrs = [this_scr] + scrs
            else:
                scrs = [this_scr] + [s for s in scrs if s != this_scr]
            # EV 番号
            evnum = re.search(r"-EV(\d+)$", ucid_old).group(1)
            ev_notes = f"(P3 で EVT 付与)/ 現行 {this_scr} `EV-{evnum}`"
            # 代替フロー: 基本フロー内の条件分岐(正常処理)を抽出。決定論のためプレースホルダ。
            alt = "—(本イベントは単一の正常フロー。条件分岐は基本フローに含む)"
            trig_txt = re.sub(r"\s+", " ", trigger).strip().rstrip("。")
            remark = f"再構成 P2 で旧 `{ucid_old}`(画面 {this_scr} のイベント `EV-{evnum}`)から導出。トリガー: {trig_txt}。シーケンス図は P6(SEQ)で保持する。"
            records.append(
                (
                    ucid_old,
                    dict(
                        uc_name=name,
                        actor=actor,
                        purpose=purpose,
                        frs=frs,
                        pre=pre,
                        basic=basic or "—",
                        alt=alt,
                        exc=exc or "—",
                        post=post,
                        scrs=scrs,
                        apis=apis,
                        tbls=tbls,
                        ev_notes=ev_notes,
                        summary=summary,
                        remark=remark,
                    ),
                )
            )

    # ---- システム起点 UC-SYSTEM ----
    sys_files = sorted(
        glob.glob(f"{BIZUC}/UC-SYSTEM-*.md"), key=lambda p: natkey(os.path.basename(p))
    )
    for f in sys_files:
        text = open(f, encoding="utf-8").read()
        old_id = re.search(r"(UC-SYSTEM-\d+)", text).group(1)
        h1 = re.search(r"^# (?:<span[^>]*></span>)?UC-SYSTEM-\d+:\s*(.+)$", text, re.M)
        name = h1.group(1).strip() if h1 else old_id
        summ = re.search(r"^>\s*\*\*このページは、(.+?)\*\*", text, re.M | re.S)
        summary = (
            re.sub(r"\s+", " ", summ.group(1)).strip()
            if summ
            else f"システム処理 {old_id} を定義します。"
        )
        overview = grab_section(text, "1. 概要")
        actors = grab_section(text, "2. 利用者(アクター)")
        pre = grab_section(text, "3. 事前条件")
        trigger = grab_section(text, "4. トリガー")
        basic = grab_section(text, "5. 基本フロー")
        exc = grab_section(text, "6. 異常系フロー")
        post = grab_section(text, "7. 事後条件")
        # 目的: 概要表の「目的」行があれば優先
        pm = re.search(r"^\|\s*目的\s*\|\s*(.+?)\s*\|\s*$", overview, re.M)
        purpose = pm.group(1).strip() if pm else summary
        # 主アクター: アクター表の先頭行ラベル
        am = re.search(r"^\|\s*([^|]+?)\s*\|\s*(?:システム|.+?)\s*\|", actors, re.M)
        # アクター表のヘッダを飛ばして最初の実データ行
        actor = "システム"
        for m in re.finditer(r"^\|\s*([^|]+?)\s*\|", actors, re.M):
            cand = m.group(1).strip()
            if cand not in ("アクター", "---", ""):
                actor = cand
                break
        frs, apis, scrs, tbls = collect_refs(overview, basic, exc, post, pre, text)
        ev_notes = "—(システム起点・画面イベントなし)"
        alt = "—(システム処理の条件分岐は基本フローに含む)"
        trig_txt = re.sub(r"\s+", " ", trigger).strip().rstrip("。")[:200]
        remark = f"再構成 P2 で旧 `{old_id}`(システム起点)から導出。トリガー: {trig_txt}。シーケンス図は P6(SEQ)で保持する。"
        records.append(
            (
                old_id,
                dict(
                    uc_name=name,
                    actor=actor,
                    purpose=purpose,
                    frs=frs,
                    pre=pre or "—",
                    basic=basic or "—",
                    alt=alt,
                    exc=exc or "—",
                    post=post or "—",
                    scrs=scrs,
                    apis=apis,
                    tbls=tbls,
                    ev_notes=ev_notes,
                    summary=summary,
                    remark=remark,
                ),
            )
        )

    # ---- 採番・書き出し ----
    crosswalk = {}
    written = []
    for i, (old_id, src) in enumerate(records, start=1):
        ucid, content = render_uc(i, src)
        crosswalk[old_id] = ucid
        path = f"{BIZUC}/{ucid}.md"
        open(path, "w", encoding="utf-8").write(content + "\n")
        written.append((old_id, ucid))

    os.makedirs("99_management", exist_ok=True)
    with open("99_management/uc_crosswalk.json", "w", encoding="utf-8") as fh:
        json.dump(crosswalk, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    # ---- 後処理: 流用本文に残る旧 UC マークダウンリンクを新 UC-NNN へリライト ----
    # (備考の `旧 \`UC-...\`` プロベナンス記述はバッククォートのため対象外)
    link_re = re.compile(
        r"\[(UC-SYSTEM-\d+)\]\((UC-SYSTEM-\d+)\.md(?:#UC-SYSTEM-\d+)?\)"
    )

    def repl(m):
        label_old, target_old = m.group(1), m.group(2)
        new = crosswalk.get(target_old)
        if not new:
            return m.group(0)
        return f"[{new}({label_old})]({new}.md#{new})"

    for old_id, ucid in written:
        path = f"{BIZUC}/{ucid}.md"
        s = open(path, encoding="utf-8").read()
        ns = link_re.sub(repl, s)
        if ns != s:
            open(path, "w", encoding="utf-8").write(ns)

    return crosswalk, written


if __name__ == "__main__":
    cw, w = main()
    print(f"generated {len(w)} UC files: UC-001 .. UC-{len(w):03d}")
