#!/usr/bin/env python3
"""再構成 P5 — TBL リンクのフラグメント補完。

P4 保留分の解消。`../04_database/TBL-NNN.md`(フラグメント無し)を
`../04_database/TBL-NNN.md#TBL-NNN` に更新する。対象:
- API ファイルの `## 利用テーブル`(`02_basic_design/03_apis/API-*.md`)
- UC ファイルの `関連テーブルID`(`01_requirements/02_business_usecases/UC-*.md`)

既に `#TBL-NNN` を持つリンクは変更しない(冪等)。
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def add_fragment(s):
    # ](<相対パス>/TBL-NNN.md)  ->  ](<相対パス>/TBL-NNN.md#TBL-NNN)
    def repl(m):
        path = m.group(1)
        tid = re.search(r"(TBL-\d+)\.md$", path).group(1)
        return f"]({path}#{tid})"

    return re.sub(r"\]\(([^)#]*?TBL-\d+\.md)\)", repl, s)


def main():
    n = 0
    targets = glob.glob(os.path.join(ROOT, "02_basic_design/03_apis/API-*.md")) + glob.glob(
        os.path.join(ROOT, "01_requirements/02_business_usecases/UC-*.md")
    )
    for f in targets:
        s = open(f, encoding="utf-8").read()
        ns = add_fragment(s)
        if ns != s:
            open(f, "w", encoding="utf-8").write(ns)
            n += 1
    print(f"fragment-completed TBL links in {n} files")


if __name__ == "__main__":
    main()
