#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-screen-mock-css.py — 画面遷移図の <style> を `.scr-mock` 配下へスコープして
`assets/css/screen-mock.css` を生成する。

なぜ必要か:
    画面設計書(02_基本設計/01_画面設計/SCR_*.html)の §2 画面レイアウトは、画面遷移図の
    リッチなワイヤーフレーム(.app-layout 等)を各ページに inline で取り込む。画面遷移図は
    独自のデザイントークン(:root の --accent-500 / --surface 等)とコンポーネント CSS を持ち、
    一部はポータル本体のトークン名(--surface / --border / --text)と衝突する。そのまま読み込むと
    ポータル全体の見た目を壊すため、本スクリプトで全セレクタを `.scr-mock` にスコープし
    (:root も `.scr-mock` に閉じる)、ワイヤーフレームを `<div class="scr-mock">` 配下に限定する。

使い方(リポジトリルートで):
    python3 99_script/build-screen-mock-css.py 01_メインシステム/画面遷移図_プロジェクト管理者.html
"""
import os
import re
import sys

SCOPE = ".scr-mock"


def split_top_rules(css):
    """波括弧をバランスしてトップレベルのルール文字列に分割する。"""
    rules = []
    depth = 0
    buf = ""
    for ch in css:
        buf += ch
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                rules.append(buf)
                buf = ""
    return rules


def scope_selector(sel):
    out = []
    for p in (x.strip() for x in sel.split(",")):
        if not p:
            continue
        if p == ":root" or p == "html" or p == "body":
            out.append(SCOPE)
        else:
            out.append(SCOPE + " " + p)
    return ", ".join(out)


def scope_rules(css):
    res = []
    for rule in split_top_rules(css):
        m = re.match(r"\s*([^{]*)\{(.*)\}\s*$", rule, re.S)
        if not m:
            continue
        prelude = m.group(1).strip()
        body = m.group(2)
        low = prelude.lower()
        if low.startswith("@keyframes") or low.startswith("@-webkit-keyframes"):
            res.append(prelude + "{" + body + "}")        # 一意名のグローバル keyframes は維持
        elif low.startswith("@page") or low.startswith("@font-face"):
            continue                                        # 印刷ページ枠は破棄(ポータルに影響させない)
        elif low.startswith("@media") or low.startswith("@supports"):
            res.append(prelude + "{" + scope_rules(body) + "}")   # 内側を再帰スコープ
        elif low.startswith("@"):
            res.append(prelude + "{" + body + "}")
        else:
            res.append(scope_selector(prelude) + "{" + body + "}")
    return "".join(res)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(src):
        sys.exit("  エラー: 入力ファイルが無い: %s" % src)
    text = open(src, encoding="utf-8").read()
    styles = re.findall(r"<style[^>]*>(.*?)</style>", text, re.S)
    if not styles:
        sys.exit("  エラー: <style> ブロックが見つかりません")
    css = "\n".join(styles)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)        # コメント除去
    scoped = scope_rules(css)
    header = (
        "/* screen-mock.css — 自動生成(99_script/build-screen-mock-css.py)。直接編集しない。\n"
        "   画面遷移図のワイヤーフレーム CSS を .scr-mock 配下へスコープしたもの。元: %s */\n"
        % os.path.relpath(src, root)
    )
    # inline 埋め込みフィット(印刷用 min-height/page-break を打ち消す。スコープ後ルールの末尾に置き優先)
    fit = (
        "\n/* inline 埋め込みフィット(自動付与) */\n"
        ".scr-mock{display:block;background:var(--bg-canvas);overflow:hidden}\n"
        ".scr-mock .screen{page-break-after:auto;min-height:0;margin:0;border:none;"
        "border-radius:0;box-shadow:none;padding:12px}\n"
    )
    out = os.path.join(root, "assets/css/screen-mock.css")
    open(out, "w", encoding="utf-8").write(header + scoped + fit + "\n")
    print("生成: assets/css/screen-mock.css (%d bytes, スコープ後ルール)" % len(scoped))


if __name__ == "__main__":
    main()
