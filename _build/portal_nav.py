#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""設計ドキュメント(01_/02_/03_)に Markdown 版ポータルナビを付与し、README を生成する。
- 各ページ上部: パンくず(設計ポータル / グループ / (サブ) / 現在地)
- 各ページ下部: 区切り + ナビゲーション(戻り導線)
- ルート README.md: 全文書ツリー(旧サイドバー相当)
基本設計はフォルダ入れ子(画面設計 / API設計 / データベース設計 / ユースケース設計 の各サブフォルダ +
横断設計の単独ファイル)。冪等: <!-- portal-top --> / <!-- portal-bottom --> マーカ間を入れ替える。
"""
import os, re, glob

ROOT = os.getcwd()
GROUPS = [("01_requirements", "要件定義"),
          ("02_basic-design", "基本設計"),
          ("03_future", "将来対応")]
BD = "02_basic-design"
SUBDIRS = [("01_screen-design", "画面設計"),
           ("02_api-design", "API設計"),
           ("03_database-design", "データベース設計"),
           ("04_usecase-design", "ユースケース設計")]
SUBLABEL = dict(SUBDIRS)
CROSS_FLAT = ["05_billing-design.md", "06_mail-design.md", "07_auth-design.md"]
API_ORDER = ["common","auth","project","member","faq","inquiry","widget",
             "dashboard","billing","inbox","terms","ai","mail","webhook"]
TBL_ORDER = ([f"M-{i:03d}" for i in range(1,13)] +
             [f"T-{i:03d}" for i in range(1,13)] +
             [f"H-{i:03d}" for i in range(1,6)] +
             ["TP-001","TP-002"])

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

def rel(frm, to):
    return os.path.relpath(to, os.path.dirname(frm)).replace(os.sep, "/")

def group_of(p):
    g = p.split("/")[0]
    for gd, gl in GROUPS:
        if gd == g:
            return gd, gl
    return g, g

def subdir_of(p):
    """basic-design 配下のサブフォルダ名(なければ None)。"""
    if not p.startswith(BD + "/"):
        return None
    rest = p[len(BD)+1:].split("/")
    if len(rest) > 1 and rest[0] in SUBLABEL:
        return rest[0]
    return None

def breadcrumb(p, title):
    gd, gl = group_of(p)
    home = f"[設計ポータル]({rel(p, 'README.md')})"
    if p == f"{gd}/index.md":
        return f"{home} ／ **{gl}**"
    parts = [home, f"[{gl}]({rel(p, gd+'/index.md')})"]
    sub = subdir_of(p)
    if sub:
        slabel = SUBLABEL[sub]
        sidx = f"{BD}/{sub}/index.md"
        if p == sidx:
            parts.append(f"**{slabel}**")
            return " ／ ".join(parts)
        parts.append(f"[{slabel}]({rel(p, sidx)})")
    parts.append(f"**{title}**")
    return " ／ ".join(parts)

def footer(p):
    gd, gl = group_of(p)
    home = f"[↑ 設計ポータル]({rel(p, 'README.md')})"
    if p == f"{gd}/index.md":
        return home
    links = []
    sub = subdir_of(p)
    if sub and p != f"{BD}/{sub}/index.md":
        links.append(f"[← {SUBLABEL[sub]}]({rel(p, f'{BD}/{sub}/index.md')})")
    links.append(f"[{gl}]({rel(p, gd+'/index.md')})")
    links.append(home)
    return " ・ ".join(links)

NAV_RE = re.compile(r'^<!-- portal-top -->.*?<!-- /portal-top -->\n+', re.S)
FOOT_RE = re.compile(r'\n+(?:---\n+)*<!-- portal-bottom -->.*?<!-- /portal-bottom -->\n*$', re.S)

def inject(path):
    s = open(path, encoding="utf-8").read()
    s = NAV_RE.sub("", s); s = FOOT_RE.sub("", s)        # 既存ナビ除去(冪等)
    s = s.lstrip("\n")
    title = h1(path)
    top = f"<!-- portal-top -->\n{breadcrumb(path, title)}\n<!-- /portal-top -->\n\n"
    bot = f"\n\n---\n\n<!-- portal-bottom -->\n{footer(path)}\n<!-- /portal-bottom -->\n"
    open(path, "w", encoding="utf-8").write(top + s.rstrip("\n") + bot)

def all_md():
    files = []
    for gd, _ in GROUPS:
        if gd == BD:
            files += glob.glob(f"{gd}/**/*.md", recursive=True)
        else:
            files += glob.glob(f"{gd}/*.md")
    return sorted(set(files))

def li(path, label=None):
    return f"- [{label or h1(path)}]({path})"

def names(d, prefix):
    return sorted([os.path.basename(p) for p in glob.glob(f"{d}/*.md")
                   if os.path.basename(p).startswith(prefix)], key=natkey)

def build_readme():
    L = []
    L.append("# FAQ AI ウィジェット SaaS / メインシステム 設計ポータル(Markdown 版)")
    L.append("")
    L.append("本リポジトリは「FAQ AI ウィジェット SaaS / メインシステム」の設計ドキュメントを **Markdown** で管理する。")
    L.append("かつての静的 HTML ポータルを Markdown へ全面変換し、Markdown を正本とした。本書がポータルのトップ(旧サイドバー相当の全文書索引)である。")
    L.append("")
    L.append("- 図は ` ```mermaid ` コードブロックで保持(GitHub 等でそのまま描画)。")
    L.append("- 画面モック(ワイヤーフレーム)は PNG 画像で表示。")
    L.append("- 相互参照は `<span id=\"…\">` アンカーで保持(例 `FR-005` / `BR-028` / `API-AUTH-001` / `TBL-M-001` / `UC-SCR-001-EV01`)。")
    L.append("- 各ページ上部にパンくず、下部に戻り導線を付与。")
    L.append("")

    # 要件定義
    L.append("## 要件定義"); L.append("")
    L.append(li("01_requirements/index.md", "概要・一覧"))
    for f in names("01_requirements", "FR"):
        L.append(li(f"01_requirements/{f}"))
    L.append("")

    # 基本設計(入れ子)
    L.append("## 基本設計"); L.append("")
    L.append(li(f"{BD}/index.md", "概要")); L.append("")

    L.append("### 画面設計"); L.append("")
    sd = f"{BD}/01_screen-design"
    L.append(li(f"{sd}/index.md", "画面一覧"))
    for f in names(sd, "SCR-"):
        L.append(li(f"{sd}/{f}"))
    L.append("")

    L.append("### API設計"); L.append("")
    ad = f"{BD}/02_api-design"
    L.append(li(f"{ad}/index.md", "API一覧"))
    for key in API_ORDER:
        f = f"{ad}/API-{key}.md"
        if os.path.exists(f): L.append(li(f))
    L.append("")

    L.append("### データベース設計"); L.append("")
    dd = f"{BD}/03_database-design"
    L.append(li(f"{dd}/index.md", "テーブル一覧"))
    for key in TBL_ORDER:
        f = f"{dd}/TBL-{key}.md"
        if os.path.exists(f): L.append(li(f))
    L.append("")

    L.append("### ユースケース設計"); L.append("")
    ud = f"{BD}/04_usecase-design"
    L.append(li(f"{ud}/index.md", "ユースケース一覧"))
    if os.path.exists(f"{ud}/sequence-design.md"):
        L.append(li(f"{ud}/sequence-design.md"))
    for f in names(ud, "UC-SCR-"):
        L.append(li(f"{ud}/{f}"))
    for f in names(ud, "UC-SYSTEM-"):
        L.append(li(f"{ud}/{f}"))
    L.append("")

    L.append("### 横断設計"); L.append("")
    for f in CROSS_FLAT:
        if os.path.exists(f"{BD}/{f}"): L.append(li(f"{BD}/{f}"))
    L.append("")

    # 将来対応
    L.append("## 将来対応"); L.append("")
    L.append(li("03_future/index.md", "概要・一覧"))
    for f in names("03_future", "FUT"):
        L.append(li(f"03_future/{f}"))
    L.append("")
    L.append("---"); L.append("")
    L.append("保守・編集のルールは [CLAUDE.md](CLAUDE.md) を参照。")
    L.append("")
    open("README.md", "w", encoding="utf-8").write("\n".join(L))

def main():
    n = 0
    for p in all_md():
        inject(p); n += 1
    build_readme()
    print(f"nav injected into {n} pages; README.md generated")

if __name__ == "__main__":
    main()
