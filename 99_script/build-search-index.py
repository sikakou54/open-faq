#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-search-index.py — HTML 設計書(正本)から全文検索インデックスを再生成する。

ポータルは HTML を正本とし、サイドバー / 検索 / 目次は assets/js/portal.js が
読み込み時に構築する。検索だけは事前構築インデックスが必要なため、本スクリプトで
nav-data.js に登録された各ページの本文を走査し assets/js/search-index.js を生成する。

使い方(リポジトリルートで):
    python3 99_script/build-search-index.py

ページを追加・改名したら、(1) HTML を作成/編集 →(2) assets/js/nav-data.js に登録 →
(3) 本スクリプトを実行、の順で更新する。nav-data.js 未登録ページは警告のうえ索引対象外。
"""
import os, re, sys, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAV_JS = os.path.join(ROOT, "assets/js/nav-data.js")
OUT_JS = os.path.join(ROOT, "assets/js/search-index.js")


def load_nav():
    txt = open(NAV_JS, encoding="utf-8").read()
    m = re.search(r"window\.NAV\s*=\s*(\[.*\]);", txt, re.S)
    if not m:
        sys.exit("nav-data.js の window.NAV 定義が解析できません")
    return json.loads(m.group(1))


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def extract(html_path):
    txt = open(html_path, encoding="utf-8").read()
    m = re.search(r'<article[^>]*class="content"[^>]*>(.*?)</article>', txt, re.S)
    body = m.group(1) if m else txt
    heads = [strip_tags(h.group(2))
             for h in re.finditer(r"<h([1-3])[^>]*>(.*?)</h\1>", body, re.S)]
    # 本文は全文を索引対象にする(上限は安全弁)。大きなページでも末尾の
    # NFR / BR / FR 定義まで検索に乗るよう、最大ページを十分に上回る値にする。
    return heads, strip_tags(body)[:40000]


def main():
    nav = load_nav()
    index = []
    missing = []
    def iter_pages(cat):
        # pages とその children(グループ)を平坦化して列挙する
        for p in cat["pages"]:
            yield p
            for c in p.get("children", []):
                yield c

    for sysd in nav:
        for cat in sysd["cats"]:
            for p in iter_pages(cat):
                path = os.path.join(ROOT, p["url"])
                if not os.path.exists(path):
                    missing.append(p["url"])
                    continue
                heads, body = extract(path)
                index.append({
                    "u": p["url"], "t": p["title"],
                    "s": sysd["label"],
                    "c": cat["label"] if cat["key"] != "__root__" else "",
                    "h": heads, "b": body if p.get("kind") != "diagram" else p["title"],
                })

    # nav 未登録の本文ページを検出(警告のみ)
    listed = {p["url"] for s in nav for c in s["cats"] for p in iter_pages(c)}
    orphans = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in (".git", ".claude", "PDF出力", "node_modules", "assets")]
        for fn in fns:
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dp, fn), ROOT).replace(os.sep, "/")
            txt = open(os.path.join(dp, fn), encoding="utf-8").read()
            if 'data-page-id=' in txt and rel not in listed and rel != "index.html":
                orphans.append(rel)

    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write("window.SEARCH_INDEX=" + json.dumps(index, ensure_ascii=False) + ";")

    print("検索インデックス再生成: %d ページ" % len(index))
    if missing:
        print("  警告: nav-data.js にあるが実体が無いページ %d 件: %s"
              % (len(missing), ", ".join(missing[:10])))
    if orphans:
        print("  警告: nav-data.js 未登録の本文ページ %d 件(索引対象外):" % len(orphans))
        for o in sorted(orphans)[:20]:
            print("    - %s" % o)


if __name__ == "__main__":
    main()
