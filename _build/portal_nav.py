#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""設計ドキュメントに Markdown 版ポータルナビを付与し、README を生成する(入れ子構成対応)。
- 各ページ上部: パンくず(設計ポータル / グループ / (サブ) / 現在地)
- 各ページ下部: 戻り導線
- ルート README.md: 全文書ツリー
グループ(01_requirements / 02_basic_design / 03_future)は直下 .md + サブフォルダ(index.md + 配下)を持つ。
冪等: <!-- portal-top --> / <!-- portal-bottom --> マーカ間を入れ替える。
"""
import os, re, glob

GROUPS = [("01_requirements", "要件定義"),
          ("02_basic_design", "基本設計"),
          ("03_future", "将来対応")]
LABELS = {
    "01_requirements/01_BusinessRequirement": "業務要件",
    "01_requirements/02_FunctionalRequirement": "機能要件",
    "01_requirements/03_NonFunctionalRequirement": "非機能要件",
    "01_requirements/04_business_usecases": "業務ユースケース",
    "02_basic_design/01_frontend": "フロントエンド設計",
    "02_basic_design/01_frontend/01_screens": "画面設計",
    "02_basic_design/01_frontend/02_screen_events": "画面イベント設計",
    "02_basic_design/02_backend": "バックエンド設計",
    "02_basic_design/02_backend/01_system": "システム設計",
    "02_basic_design/02_backend/02_system_events": "システムイベント設計",
    "02_basic_design/02_backend/03_apis": "API設計",
    "02_basic_design/02_backend/04_database": "DB設計",
    "02_basic_design/03_sequences": "シーケンス設計",
    "02_basic_design/04_permissions": "権限設計",
    "02_basic_design/05_errors": "エラー設計",
    "02_basic_design/06_messages": "メッセージ設計",
}
GLABEL = dict(GROUPS)
# サブフォルダの表示順(数値接頭辞の自然順)
def subdirs_of(gdir):
    return sorted([d for d in glob.glob(f"{gdir}/*") if os.path.isdir(d)])

def natkey(s):
    if s.endswith(".md"): s = s[:-3]
    return [int(t) if t.isdigit() else t for t in re.findall(r'\d+|\D+', s)]

def h1(path):
    for line in open(path, encoding="utf-8"):
        if line.startswith("# "):
            return re.sub(r'<span[^>]*></span>', '', line[2:]).strip()
    return os.path.basename(path)

def label_of(d):
    return LABELS.get(d, h1(f"{d}/index.md") if os.path.exists(f"{d}/index.md") else os.path.basename(d))

def rel(frm, to):
    return os.path.relpath(to, os.path.dirname(frm)).replace(os.sep, "/")

def group_of(p):
    return p.split("/")[0]

def dirchain(p):
    """グループを除く、ファイルが属するディレクトリ列(上位→下位)。入れ子任意段に対応。
    例: 02_basic_design/01_frontend/01_screens/SCR-001.md
        → ['02_basic_design/01_frontend', '02_basic_design/01_frontend/01_screens']"""
    g = group_of(p); d = os.path.dirname(p); chain = []
    while d and d != g:
        chain.append(d); d = os.path.dirname(d)
    chain.reverse()
    return chain

def breadcrumb(p, title):
    g = group_of(p); gl = GLABEL.get(g, g)
    home = f"[設計ポータル]({rel(p, 'README.md')})"
    if p == f"{g}/index.md":
        return f"{home} ／ **{gl}**"
    parts = [home, f"[{gl}]({rel(p, g+'/index.md')})"]
    for sub in dirchain(p):
        sidx = f"{sub}/index.md"; sl = label_of(sub)
        if p == sidx:
            parts.append(f"**{sl}**"); return " ／ ".join(parts)
        parts.append(f"[{sl}]({rel(p, sidx)})")
    parts.append(f"**{title}**")
    return " ／ ".join(parts)

def footer(p):
    g = group_of(p); gl = GLABEL.get(g, g)
    home = f"[↑ 設計ポータル]({rel(p, 'README.md')})"
    if p == f"{g}/index.md":
        return home
    links = []
    chain = dirchain(p)
    if chain:
        parent = chain[-1]
        if p == f"{parent}/index.md":
            if len(chain) >= 2:        # サブフォルダ index は親フォルダ index へ戻る
                up = chain[-2]
                links.append(f"[← {label_of(up)}]({rel(p, up+'/index.md')})")
        else:                          # 個別ページは所属フォルダ index へ戻る
            links.append(f"[← {label_of(parent)}]({rel(p, parent+'/index.md')})")
    links.append(f"[{gl}]({rel(p, g+'/index.md')})")
    links.append(home)
    return " ・ ".join(links)

NAV_RE = re.compile(r'^<!-- portal-top -->.*?<!-- /portal-top -->\n+', re.S)
FOOT_RE = re.compile(r'\n+(?:---\n+)*<!-- portal-bottom -->.*?<!-- /portal-bottom -->\n*$', re.S)

def inject(path):
    s = open(path, encoding="utf-8").read()
    s = NAV_RE.sub("", s); s = FOOT_RE.sub("", s); s = s.lstrip("\n")
    title = h1(path)
    top = f"<!-- portal-top -->\n{breadcrumb(path, title)}\n<!-- /portal-top -->\n\n"
    bot = f"\n\n---\n\n<!-- portal-bottom -->\n{footer(path)}\n<!-- /portal-bottom -->\n"
    open(path, "w", encoding="utf-8").write(top + s.rstrip("\n") + bot)

def all_md():
    files = []
    for g, _ in GROUPS:
        files += glob.glob(f"{g}/**/*.md", recursive=True)
    return sorted(set(files))

def li(path, label=None, ind=0):
    return f"{'  '*ind}- [{label or h1(path)}]({path})"

def dirfiles(d):
    return sorted([p for p in glob.glob(f"{d}/*.md")
                   if os.path.basename(p) != "index.md"], key=lambda p: natkey(os.path.basename(p)))

def build_readme():
    L = ["# FAQ AI ウィジェット SaaS / メインシステム 設計ポータル(Markdown 版)", "",
         "本リポジトリは設計ドキュメントを **Markdown** で管理する。Markdown を正本とし、本書がポータルのトップ(全文書索引)である。",
         "", "- 図は ` ```mermaid ` で保持。相互参照は `<span id=\"…\">` アンカー。各ページにパンくず・戻り導線を付与。",
         "- 読み順: 要件定義 ＞ 業務ユースケース ＞ 画面設計 ＞ 画面イベント ＞ API設計 ＞ DB設計 ＞ シーケンス ＞ 権限/エラー/メッセージ。", ""]
    def walk_dir(d, level):                         # サブフォルダを再帰的に出力(入れ子任意段)
        if os.path.exists(f"{d}/index.md"):
            L.append(li(f"{d}/index.md", "一覧"))
        for f in dirfiles(d):
            L.append(li(f))
        L.append("")
        for sd in subdirs_of(d):
            L.append(f"{'#'*level} {label_of(sd)}"); L.append("")
            walk_dir(sd, level + 1)
    for g, gl in GROUPS:
        L.append(f"## {gl}"); L.append("")
        if os.path.exists(f"{g}/index.md"):
            L.append(li(f"{g}/index.md", "概要・一覧"))
        for f in dirfiles(g):                       # グループ直下の .md(移行中の暫定含む)
            L.append(li(f))
        L.append("")
        for d in subdirs_of(g):
            L.append(f"### {label_of(d)}"); L.append("")
            walk_dir(d, 4)
    L += ["---", "", "保守・編集のルールは [CLAUDE.md](CLAUDE.md) を参照。", ""]
    open("README.md", "w", encoding="utf-8").write("\n".join(L))

def main():
    n = 0
    for p in all_md():
        inject(p); n += 1
    build_readme()
    print(f"nav injected into {n} pages; README.md generated")

if __name__ == "__main__":
    main()
