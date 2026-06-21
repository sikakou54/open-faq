#!/usr/bin/env python3
"""再構成 P5 — DB設計 index.md に TBL↔API/UC 対応表 と 読み順 を追加。

ER 図・テーブル一覧はそのまま保持し、§3(ER 図)の直後に
  - 「テーブル↔API/UC 対応表」(逆引きの集約)
  - 「読み順」
を `<!-- p5-cross -->` 〜 `<!-- /p5-cross -->` マーカで挿入/更新する(冪等)。
"""
import os, re, glob, collections, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(ROOT, "02_basic_design/04_database")
IDX = os.path.join(DB_DIR, "index.md")


def catalog():
    idx = open(IDX, encoding="utf-8").read()
    out = []
    for m in re.finditer(
        r'<span id="(TBL-\d+)"></span>\[`([A-Z_]+)`\]\(TBL-\d+\.md\)\s*\|\s*([^|]+?)\s*\|',
        idx,
    ):
        out.append((m.group(1), m.group(2), m.group(3).strip()))
    return out


def reverse():
    tbl_api = collections.defaultdict(set)
    for f in glob.glob(os.path.join(ROOT, "02_basic_design/03_apis/API-*.md")):
        a = re.search(r"(API-\d+)", os.path.basename(f)).group(1)
        s = open(f, encoding="utf-8").read()
        m = re.search(r"## 利用テーブル(.*?)(?:\n## |\Z)", s, re.S)
        for t in set(re.findall(r"TBL-\d+", m.group(1) if m else "")):
            tbl_api[t].add(a)
    tbl_uc = collections.defaultdict(set)
    for f in glob.glob(os.path.join(ROOT, "01_requirements/02_business_usecases/UC-*.md")):
        u = re.search(r"(UC-\d+)", os.path.basename(f)).group(1)
        s = open(f, encoding="utf-8").read()
        m = re.search(r"関連テーブルID\s*\|(.*?)\|", s)
        for t in set(re.findall(r"TBL-\d+", m.group(1) if m else "")):
            tbl_uc[t].add(u)
    return tbl_api, tbl_uc


def main():
    cat = catalog()
    tbl_api, tbl_uc = reverse()
    n = lambda x: int(x.split("-")[-1])
    rows = []
    for tid, phys, lg in cat:
        apis = sorted(tbl_api.get(tid, []), key=n)
        ucs = sorted(tbl_uc.get(tid, []), key=n)
        api_links = (
            " ".join(f"[{a}](../03_apis/{a}.md#{a})" for a in apis) if apis else "—"
        )
        uc_cnt = (
            f"{len(ucs)} 件"
            + (
                "(例 "
                + " ".join(
                    f"[{u}](../../01_requirements/02_business_usecases/{u}.md#{u})"
                    for u in ucs[:3]
                )
                + ("…)" if len(ucs) > 3 else ")")
            )
            if ucs
            else "—"
        )
        rows.append(
            f"| [`{phys}`](#{tid}) | {len(apis)} | {api_links} | {uc_cnt} |"
        )

    block = "\n".join(
        [
            "<!-- p5-cross -->",
            '## <span id="cross"></span>4.テーブル↔API / 業務UC 対応表(逆引き)',
            "",
            "各テーブルを読み書きする API と、参照する業務ユースケースの逆引きです。"
            "API は `## 利用テーブル`、UC は `関連テーブルID` から決定論的に集計しています。"
            "個別の対応は各テーブルページの「項目」セクションを参照してください。",
            "",
            "| テーブル | API 数 | 利用API | 対応業務UC |",
            "|---|---:|---|---|",
        ]
        + rows
        + [
            "",
            '## <span id="readorder"></span>5.読み順',
            "",
            "1. 本ページ §2 テーブル一覧でドメイン全体像を把握する。",
            "2. §3 ER 図で親子(契約境界 `M_CONTRACT` → `M_PROJECTS` → 各テーブル)を確認する。",
            "3. §4 対応表で対象テーブルの利用 API / 業務UC を逆引きする。",
            "4. 各テーブルページ(`TBL-NNN.md`)で 項目 / カラム定義 / 制約 / インデックス / コード値 を確認する。",
            "<!-- /p5-cross -->",
        ]
    )

    s = open(IDX, encoding="utf-8").read()
    if "<!-- p5-cross -->" in s:
        s = re.sub(r"<!-- p5-cross -->.*?<!-- /p5-cross -->", lambda _: block, s, flags=re.S)
    else:
        # §4命名・分類規約 の直前に挿入(無ければ末尾の `---` 前)
        anchor = re.search(r"\n## <span id=\"rule\">", s)
        if anchor:
            s = s[: anchor.start()] + "\n\n" + block + "\n" + s[anchor.start():]
        else:
            s = s.replace("\n---\n", "\n\n" + block + "\n\n---\n", 1)
    open(IDX, "w", encoding="utf-8").write(s)
    print("index.md cross-table updated:", len(rows), "rows")


if __name__ == "__main__":
    main()
