#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ルート配置(01_/02_/03_)の Markdown に Markdown 版ポータルナビを付与し、README を生成する。
- 各ページ上部: パンくず(設計ポータル / グループ / (サブ) / 現在地)
- 各ページ下部: 区切り + ナビゲーション(戻り導線)
- ルート README.md: 全文書ツリー(旧サイドバー相当)
冪等: <!-- portal-top --> / <!-- portal-bottom --> マーカ間を入れ替える。
"""
import os, re, glob

ROOT = os.getcwd()
GROUPS = [("01_requirements", "要件定義"),
          ("02_basic-design", "基本設計"),
          ("03_future", "将来対応")]
SUBIDX = {"01_screen-design.md": "画面設計",
          "02_api-design.md": "API設計",
          "03_database-design.md": "データベース設計"}
API_ORDER = ["common","auth","project","member","faq","inquiry","widget",
             "dashboard","billing","inbox","terms","ai","mail","webhook"]
TBL_ORDER = ([f"M-{i:03d}" for i in range(1,13)] +
             [f"T-{i:03d}" for i in range(1,13)] +
             [f"H-{i:03d}" for i in range(1,7)] +
             ["TP-001","TP-002"])
CROSS = ["04_usecase-design.md","05_billing-design.md",
         "06_mail-design.md","07_auth-design.md"]

def natkey(s):
    if s.endswith(".md"):
        s = s[:-3]                       # 親(SCR-004)を子(SCR-004-001)より前にする
    return [int(t) if t.isdigit() else t for t in re.findall(r'\d+|\D+', s)]

def h1(path):
    for line in open(path, encoding="utf-8"):
        if line.startswith("# "):
            t = line[2:].strip()
            t = re.sub(r'<span[^>]*></span>', '', t).strip()  # 埋め込みアンカー除去
            return t
    return os.path.basename(path)

def subsection_of(fname):
    if fname in SUBIDX:
        return (SUBIDX[fname], fname)
    if fname.startswith("SCR-"): return ("画面設計", "01_screen-design.md")
    if fname.startswith("API-"): return ("API設計", "02_api-design.md")
    if fname.startswith("TBL-"): return ("データベース設計", "03_database-design.md")
    return None

def breadcrumb(gdir, glabel, fname, title):
    home = "[設計ポータル](../README.md)"
    if fname == "index.md":
        return f"{home} ／ **{glabel}**"
    parts = [home, f"[{glabel}](index.md)"]
    if gdir == "02_basic-design":
        sub = subsection_of(fname)
        if sub:
            slabel, sidx = sub
            if fname == sidx:
                parts.append(f"**{slabel}**")
                return " ／ ".join(parts)
            parts.append(f"[{slabel}]({sidx})")
    parts.append(f"**{title}**")
    return " ／ ".join(parts)

def footer(gdir, glabel, fname):
    home = "[↑ 設計ポータル](../README.md)"
    if fname == "index.md":
        return home
    links = []
    if gdir == "02_basic-design":
        sub = subsection_of(fname)
        if sub and fname != sub[1]:
            links.append(f"[← {sub[0]}]({sub[1]})")
    links.append(f"[{glabel}](index.md)")
    links.append(home)
    return " ・ ".join(links)

NAV_RE = re.compile(r'^<!-- portal-top -->.*?<!-- /portal-top -->\n+', re.S)
FOOT_RE = re.compile(r'\n+(?:---\n+)*<!-- portal-bottom -->.*?<!-- /portal-bottom -->\n*$', re.S)

def inject(path, gdir, glabel):
    fname = os.path.basename(path)
    s = open(path, encoding="utf-8").read()
    s = NAV_RE.sub("", s); s = FOOT_RE.sub("", s)        # 既存ナビ除去(冪等)
    s = s.lstrip("\n")
    title = h1(path)
    top = f"<!-- portal-top -->\n{breadcrumb(gdir,glabel,fname,title)}\n<!-- /portal-top -->\n\n"
    bot = f"\n\n---\n\n<!-- portal-bottom -->\n{footer(gdir,glabel,fname)}\n<!-- /portal-bottom -->\n"
    open(path, "w", encoding="utf-8").write(top + s.rstrip("\n") + bot)

def collect(gdir):
    return [os.path.basename(p) for p in glob.glob(os.path.join(gdir, "*.md"))]

def li(gdir, fname, label=None):
    p = f"{gdir}/{fname}"
    return f"- [{label or h1(p)}]({p})"

def build_readme():
    L = []
    L.append("# FAQ AI ウィジェット SaaS / メインシステム 設計ポータル(Markdown 版)")
    L.append("")
    L.append("本リポジトリは「FAQ AI ウィジェット SaaS / メインシステム」の設計ドキュメントを **Markdown** で管理する。")
    L.append("かつての静的 HTML ポータルを Markdown へ全面変換し、Markdown を正本とした。本書がポータルのトップ(旧サイドバー相当の全文書索引)である。")
    L.append("")
    L.append("- 図は ` ```mermaid ` コードブロックで保持(GitHub 等でそのまま描画)。")
    L.append("- 画面モック(ワイヤーフレーム)は PNG 画像で表示(元の HTML は `<details>` 内に保持)。")
    L.append("- 相互参照は `<span id=\"…\">` アンカーで保持(例 `FR-005` / `BR-028` / `API-AUTH-001` / `TBL-M-001`)。")
    L.append("- 各ページ上部にパンくず、下部に戻り導線を付与。")
    L.append("")

    # 要件定義
    L.append("## 要件定義")
    L.append("")
    L.append(li("01_requirements", "index.md", "概要・一覧"))
    for f in sorted([x for x in collect("01_requirements") if x.startswith("FR")], key=natkey):
        L.append(li("01_requirements", f))
    L.append("")

    # 基本設計
    L.append("## 基本設計")
    L.append("")
    L.append(li("02_basic-design", "index.md", "概要"))
    L.append("")
    L.append("### 画面設計")
    L.append("")
    L.append(li("02_basic-design", "01_screen-design.md"))
    for f in sorted([x for x in collect("02_basic-design") if x.startswith("SCR-")], key=natkey):
        L.append(li("02_basic-design", f))
    L.append("")
    L.append("### API設計")
    L.append("")
    L.append(li("02_basic-design", "02_api-design.md"))
    for key in API_ORDER:
        f = f"API-{key}.md"
        if os.path.exists(f"02_basic-design/{f}"):
            L.append(li("02_basic-design", f))
    L.append("")
    L.append("### データベース設計")
    L.append("")
    L.append(li("02_basic-design", "03_database-design.md"))
    for key in TBL_ORDER:
        f = f"TBL-{key}.md"
        if os.path.exists(f"02_basic-design/{f}"):
            L.append(li("02_basic-design", f))
    L.append("")
    L.append("### 横断設計")
    L.append("")
    for f in CROSS:
        if os.path.exists(f"02_basic-design/{f}"):
            L.append(li("02_basic-design", f))
    L.append("")

    # 将来対応
    L.append("## 将来対応")
    L.append("")
    L.append(li("03_future", "index.md", "概要・一覧"))
    for f in sorted([x for x in collect("03_future") if x.startswith("FUT")], key=natkey):
        L.append(li("03_future", f))
    L.append("")
    L.append("---")
    L.append("")
    L.append("保守・編集のルールは [CLAUDE.md](CLAUDE.md) を参照。")
    L.append("")
    open("README.md", "w", encoding="utf-8").write("\n".join(L))

def main():
    n = 0
    for gdir, glabel in GROUPS:
        for p in glob.glob(os.path.join(gdir, "*.md")):
            inject(p, gdir, glabel); n += 1
    build_readme()
    print(f"nav injected into {n} pages; README.md generated")

if __name__ == "__main__":
    main()
