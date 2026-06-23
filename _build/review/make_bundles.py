#!/usr/bin/env python3
"""NotebookLM 投入用バンドル生成(冪等)。

約 700 個の Markdown を NotebookLM のソース数上限に収めるため、レイヤ別に
連結した少数ソースへまとめる。各ファイルの先頭に `===== <相対パス> =====`
区切りを入れ、NotebookLM 回答が「対象箇所」を相対パスで返せるようにする。

使い方(リポジトリルートで):  python3 _build/review/make_bundles.py [bundle_key ...]
引数なしで全バンドル再生成。bundle_key 指定で対象のみ再生成(修正後の差分用)。
出力先: _build/review/bundles/<key>.md
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "_build", "review", "bundles")

# bundle_key -> (見出し, [glob パターン...])  ※ glob はリポジトリルート相対
BUNDLES = {
    "00_rules": ("設計ルール正本(CLAUDE.md)", [
        "CLAUDE.md",
    ]),
    "01_requirements": ("要件定義: 業務要件 BR / 機能要件 FR / 非機能要件 NFR / 業務ルール RULE", [
        "01_requirements/index.md",
        "01_requirements/01_business_requirement/*.md",
        "01_requirements/02_functional_requirement/*.md",
        "01_requirements/03_non_functional_requirement/*.md",
    ]),
    "02_usecases": ("要件定義: 業務ユースケース UC", [
        "01_requirements/04_business_usecases/*.md",
    ]),
    "03_screens_events": ("基本設計(フロント): 画面 SCR / 画面イベント EVT", [
        "02_basic_design/01_frontend/index.md",
        "02_basic_design/01_frontend/01_screens/*.md",
        "02_basic_design/01_frontend/02_screen_events/*.md",
    ]),
    "04_backend": ("基本設計(バック): システム SYS / システムイベント SEV / API / テーブル TBL", [
        "02_basic_design/02_backend/index.md",
        "02_basic_design/02_backend/01_system/*.md",
        "02_basic_design/02_backend/02_system_events/*.md",
        "02_basic_design/02_backend/03_apis/*.md",
        "02_basic_design/02_backend/04_database/*.md",
    ]),
    "05_sequences": ("基本設計: シーケンス SEQ", [
        "02_basic_design/03_sequences/*.md",
    ]),
    "06_cross": ("基本設計(横断): 権限 PERM / エラー ERR / メッセージ MSG / 課金", [
        "02_basic_design/index.md",
        "02_basic_design/04_permissions/*.md",
        "02_basic_design/05_errors/*.md",
        "02_basic_design/06_messages/*.md",
        "02_basic_design/05_billing-design.md",
    ]),
}


def natkey(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p)]


def expand(patterns):
    seen, files = set(), []
    for pat in patterns:
        for f in sorted(glob.glob(os.path.join(ROOT, pat), recursive=True), key=natkey):
            rel = os.path.relpath(f, ROOT)
            if os.path.isfile(f) and rel not in seen:
                seen.add(rel)
                files.append((rel, f))
    return files


def build(key):
    heading, patterns = BUNDLES[key]
    files = expand(patterns)
    parts = [f"# NotebookLM ソース: {heading}\n",
             f"# バンドルキー: {key} / 収録 {len(files)} ファイル\n",
             "# 各ファイルは `===== <相対パス> =====` で区切られる。指摘時はこの相対パスで対象箇所を示すこと。\n"]
    for rel, full in files:
        with open(full, encoding="utf-8", errors="replace") as fh:
            body = fh.read()
        parts.append(f"\n\n===== {rel} =====\n\n{body}")
    text = "".join(parts)
    os.makedirs(OUT, exist_ok=True)
    outp = os.path.join(OUT, f"{key}.md")
    with open(outp, "w", encoding="utf-8") as fh:
        fh.write(text)
    b = len(text.encode())
    print(f"{key:18s} files={len(files):4d} bytes={b:>9,} (~{b/1024:.0f}KB) ~words={b//6:,}")


def main():
    keys = sys.argv[1:] or list(BUNDLES)
    for k in keys:
        if k not in BUNDLES:
            print(f"unknown bundle key: {k} (valid: {', '.join(BUNDLES)})"); sys.exit(2)
        build(k)


if __name__ == "__main__":
    main()
