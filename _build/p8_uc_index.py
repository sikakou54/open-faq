#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P8 業務ユースケース index.md 再構築(統合後 88 件)。

機能グループ別 + アクター別の索引を生成する。画面/API/テーブル列は持たず、
業務UC・名称・主アクター・起点種別のみ(要件・基本設計トレースはマトリクスが正本)。
各 UC セルに `<span id="UC-NNN">` を付与(索引アンカー)。

実行: python3 _build/p8_uc_index.py
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XWALK = os.path.join(ROOT, "99_management", "uc_crosswalk_v2.json")
UCDIR = os.path.join(ROOT, "01_requirements", "04_business_usecases")
OUT = os.path.join(UCDIR, "index.md")

GROUP_ORDER = ["account", "faq-ai", "usage", "widget", "notification", "security"]
GROUP_LABEL = {
    "account": "アカウント・ユーザー・アクセス制御",
    "faq-ai": "FAQ・AI回答・未解決質問",
    "usage": "利用量・課金・ダッシュボード",
    "widget": "ウィジェット・検索",
    "notification": "通知・お知らせ",
    "security": "セキュリティ・プライバシー",
}
KIND_LABEL = {"screen": "画面起点", "system": "システム起点", "requirement": "要件起点"}
# 旧アクター区分アンカー(基本設計 index 等からの互換参照を解決する)
ACT_ANCHOR = {
    "アカウント利用者": "act-account", "オーナー": "act-owner", "メンバー": "act-member",
    "ウィジェット利用者": "act-widget", "システム": "act-ops",
}


def natnum(uc):
    return int(uc.split("-")[1])


def uc_name(ucid):
    """UC ファイルの H1 から実際の名称を取得(無ければクロスウォーク名)。"""
    f = os.path.join(UCDIR, f"{ucid}.md")
    if os.path.exists(f):
        for line in open(f, encoding="utf-8"):
            m = re.match(r'#\s*<span id="' + ucid + r'"></span>' + ucid + r':\s*(.+)', line)
            if m:
                return m.group(1).strip()
    return None


def main():
    d = json.load(open(XWALK, encoding="utf-8"))
    meta = d["meta"]
    ucs = sorted(meta, key=natnum)

    L = []
    L.append("# 業務ユースケース")
    L.append("")
    L.append("> **このページは、要件定義の業務ユースケース(誰が・何の目的で・どの業務を・どのような流れで実行するか)を一覧します。**")
    L.append("")
    L.append(f"*業務処理粒度で {len(ucs)} 件。各 UC は前半が画面起点(利用者操作)、続いてシステム起点(バッチ・Webhook・非同期・通知)、要件起点(横断方針)。"
             "画面・画面イベント・API・テーブル・シーケンスとの対応は [トレーサビリティマトリクス](../../99_management/02_traceability_matrix.md) で管理する。*")
    L.append("")

    # アクター別 索引
    by_actor = {}
    for u in ucs:
        by_actor.setdefault(meta[u]["actor"], []).append(u)
    L.append("## アクター別索引")
    L.append("")
    L.append("| 主アクター | 業務ユースケース |")
    L.append("|---|---|")
    for actor in sorted(by_actor, key=lambda a: (-len(by_actor[a]), a)):
        links = " ・ ".join(f"[{u}](#{u})" for u in by_actor[actor])
        anchor = f'<span id="{ACT_ANCHOR[actor]}"></span>' if actor in ACT_ANCHOR else ""
        L.append(f"| {anchor}{actor} | {links} |")
    # 未使用の互換アンカー(該当アクターが索引に無い場合)も末尾に保持し参照を解決
    used = {ACT_ANCHOR[a] for a in by_actor if a in ACT_ANCHOR}
    rest = [v for v in ACT_ANCHOR.values() if v not in used]
    if rest:
        L.append("")
        L.append("".join(f'<span id="{a}"></span>' for a in rest))
    L.append("")

    # 機能グループ別 一覧(本体・アンカー保持)
    L.append("## 機能グループ別一覧")
    L.append("")
    for g in GROUP_ORDER:
        members = [u for u in ucs if meta[u]["group"] == g]
        if not members:
            continue
        L.append(f"### {GROUP_LABEL[g]}")
        L.append("")
        L.append("| 業務UC | 業務ユースケース名 | 主アクター | 起点 |")
        L.append("|---|---|---|---|")
        for u in members:
            name = uc_name(u) or meta[u]["name"]
            cell = f'<span id="{u}"></span>[{u}]({u}.md#{u})'
            L.append(f"| {cell} | {name} | {meta[u]['actor']} | {KIND_LABEL[meta[u]['kind']]} |")
        L.append("")

    open(OUT, "w", encoding="utf-8").write("\n".join(L).rstrip() + "\n")
    print(f"UC index regenerated: {len(ucs)} UCs across {len(by_actor)} actors")


if __name__ == "__main__":
    main()
