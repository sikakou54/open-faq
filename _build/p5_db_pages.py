#!/usr/bin/env python3
"""再構成 P5 (DB設計) — TBL ページ整備。

各 TBL-NNN.md に対して:
  1. H1 を `# <span id="TBL-NNN"></span><物理名>(<論理名>)` に統一(`#TBL-NNN` 参照を解決)。
  2. リード文直後に `### 項目` セクションを挿入/更新。
     - テーブル基本情報(テーブルID / 物理名 / 論理名 / 概要)
     - 対応業務UC(UC 逆引き) / 利用API(API 逆引き) ※ crosswalk + 現行参照から決定論的に算出
     - 論理削除(`valid` / `status='deleted'` 列の有無から判定) / 監査項目(`created_at` 等の有無から判定)
  3. パンくず(portal-top)はそのまま(portal_nav.py が後で再生成)。

冪等。マーカ `<!-- p5-item -->` 〜 `<!-- /p5-item -->` で項目セクションを毎回入れ替える。
"""
import json, os, re, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(ROOT, "02_basic_design/04_database")
TBLMAP = json.load(open(os.path.join(ROOT, "99_management/crosswalk.json")))["tblmap"]
NEW2OLD = {v: k for k, v in TBLMAP.items()}


def index_logical_names():
    """index.md のテーブル一覧から 新ID -> (物理名, 論理名) を取得(カタログ正本)。"""
    idx = open(os.path.join(DB_DIR, "index.md"), encoding="utf-8").read()
    out = {}
    for m in re.finditer(
        r'<span id="(TBL-\d+)"></span>\[`([A-Z_]+)`\]\(TBL-\d+\.md\)\s*\|\s*([^|]+?)\s*\|',
        idx,
    ):
        out[m.group(1)] = (m.group(2), m.group(3).strip())
    return out


CATALOG = index_logical_names()


def srt_id(ids):
    return sorted(ids, key=lambda x: int(x.split("-")[-1]))


def build_reverse_index():
    """現行参照から TBL(新ID) -> 利用API / 対応業務UC を算出。"""
    tbl_to_api = collections.defaultdict(set)
    for f in glob.glob(os.path.join(ROOT, "02_basic_design/03_apis/API-*.md")):
        apiid = re.search(r"(API-\d+)", os.path.basename(f)).group(1)
        s = open(f, encoding="utf-8").read()
        m = re.search(r"## 利用テーブル(.*?)(?:\n## |\Z)", s, re.S)
        seg = m.group(1) if m else ""
        for t in set(re.findall(r"TBL-\d+", seg)):
            tbl_to_api[t].add(apiid)
    tbl_to_uc = collections.defaultdict(set)
    for f in glob.glob(os.path.join(ROOT, "01_requirements/02_business_usecases/UC-*.md")):
        ucid = re.search(r"(UC-\d+)", os.path.basename(f)).group(1)
        s = open(f, encoding="utf-8").read()
        m = re.search(r"関連テーブルID\s*\|(.*?)\|", s)
        seg = m.group(1) if m else ""
        for t in set(re.findall(r"TBL-\d+", seg)):
            tbl_to_uc[t].add(ucid)
    return tbl_to_api, tbl_to_uc


def parse_page(newid, s):
    """物理名・論理名・主キー・列名リストを抽出。

    物理名は概要テーブルの「テーブル名」、論理名は index カタログ正本を使う。
    """
    phys, lg = CATALOG.get(newid, (None, None))
    if phys is None:
        m = re.search(r"テーブル名\s*\|\s*`([A-Z_]+)`", s) or re.search(
            r"<td>テーブル名</td>\s*<td><code>([A-Z_]+)</code>", s
        )
        phys = m.group(1) if m else newid
    # 主キー(HTML / MD 両形式)
    pk = None
    m = re.search(r"<td>主キー</td>\s*<td>(.*?)</td>", s, re.S)
    if m:
        pk = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    else:
        m = re.search(r"主キー\s*\|\s*`?([^|\n]+?)`?\s*\|", s)
        if m:
            pk = m.group(1).strip().strip("`")
    # カラム定義の物理名(`col`)を収集
    cols = re.findall(r"\|\s*`([a-z_][a-z0-9_]*)`\s*\|", s)
    return phys, lg, pk, set(cols)


def del_mode(s, cols):
    if "valid" in cols and re.search(r"`valid`.*`valid IN \(0,1\)`", s):
        return "あり(`valid` フラグ 0/1)"
    if "valid" in cols:
        return "あり(`valid` フラグ)"
    if "status" in cols and "deleted" in s:
        return "あり(`status='deleted'`)"
    if "deleted_at" in cols:
        return "あり(`deleted_at`)"
    return "なし(物理削除 / 追記専用)"


def audit_cols(cols):
    parts = []
    if "created_at" in cols:
        parts.append("`created_at`")
    if "updated_at" in cols:
        parts.append("`updated_at`")
    who = []
    if {"created_by_id", "created_by_type"} & cols:
        who.append("`created_by_*`")
    if {"updated_by_id", "updated_by_type"} & cols:
        who.append("`updated_by_*`")
    if "actor_id" in cols:
        who.append("`actor_id`")
    ts = " / ".join(parts) if parts else "—"
    wh = " / ".join(who) if who else "—"
    return ts, wh


def item_section(newid, phys, lg, pk, lead, cols, s, apis, ucs):
    api_links = (
        " ・ ".join(f"[{a}](../03_apis/{a}.md#{a})" for a in apis) if apis else "—"
    )
    uc_links = (
        " ・ ".join(f"[{u}](../../01_requirements/02_business_usecases/{u}.md#{u})" for u in ucs)
        if ucs
        else "—"
    )
    dm = del_mode(s, cols)
    ats, awho = audit_cols(cols)
    lead1 = lead.strip()
    rows = [
        f"| テーブルID | `{newid}` |",
        f"| 物理名 | `{phys}` |",
        f"| 論理名 | {lg or '—'} |",
        f"| 概要 | {lead1} |",
        f"| 主キー | {('`'+pk+'`') if pk and pk!='—' else '—'} |",
        f"| 論理削除 | {dm} |",
        f"| 監査項目(日時) | {ats} |",
        f"| 監査項目(実施者) | {awho} |",
        f"| 対応業務UC(逆引き) | {uc_links} |",
        f"| 利用API(逆引き) | {api_links} |",
    ]
    body = "\n".join(
        [
            "<!-- p5-item -->",
            '### <span id="item"></span>項目',
            "",
            "本テーブルの基本情報と、参照元の業務ユースケース / API(逆引き)です。",
            "",
            "| 項目 | 内容 |",
            "|---|---|",
        ]
        + rows
        + ["<!-- /p5-item -->"]
    )
    return body


def process(path):
    newid = os.path.splitext(os.path.basename(path))[0]
    s = open(path, encoding="utf-8").read()
    # 既存の項目セクションを先に除去(冪等・リード文誤抽出防止)
    s = re.sub(r"<!-- p5-item -->.*?<!-- /p5-item -->\n*", "", s, flags=re.S)
    phys, lg, pk, cols = parse_page(newid, s)

    # H1 を統一
    new_h1 = f'# <span id="{newid}"></span>{phys}({lg})' if lg else f'# <span id="{newid}"></span>{phys}'
    s = re.sub(r"^# .+$", new_h1.replace("\\", "\\\\"), s, count=1, flags=re.M)

    # リード文(分類行の次の段落)を抽出。
    # 構造: H1 \n\n 分類行(マスタ等, 末尾の orphan span 除去) \n\n リード文 \n\n ### ...
    # 分類行から orphan の <span id="..."></span> を除去
    s = re.sub(r'(\n(?:マスタ|トランザクション|履歴|ワーク)[^\n]*?)\s*<span id="[^"]*"></span>', r"\1", s)

    # リード文 = H1ブロック後、最初の `### ` 直前の段落
    m = re.search(r"^# [^\n]+\n+(.*?)\n+### ", s, re.M | re.S)
    block = m.group(1) if m else ""
    # block 内の最後の非空行群がリード文。分類行を除いた残りを連結。
    lines = [ln for ln in block.split("\n") if ln.strip()]
    classline = ""
    lead_lines = []
    for ln in lines:
        if re.match(r"^(マスタ|トランザクション|履歴|ワーク)", ln) and not lead_lines:
            classline = ln.strip()
        else:
            lead_lines.append(ln.strip())
    lead = " ".join(lead_lines) if lead_lines else (lg or phys)

    apis = srt_id(REV_API.get(newid, []))
    ucs = srt_id(REV_UC.get(newid, []))
    item = item_section(newid, phys, lg, pk, lead, cols, s, apis, ucs)

    # 最初の `### ` の前に挿入(項目セクションは冒頭で除去済み)
    s = re.sub(r"(\n)(### )", lambda m: "\n" + item + "\n\n### ", s, count=1)

    open(path, "w", encoding="utf-8").write(s)
    return newid, len(apis), len(ucs)


REV_API, REV_UC = build_reverse_index()


def main():
    rows = []
    for newid in sorted(NEW2OLD):
        p = os.path.join(DB_DIR, f"{newid}.md")
        rows.append(process(p))
    tot_api = sum(r[1] for r in rows)
    tot_uc = sum(r[2] for r in rows)
    print(f"processed {len(rows)} TBL pages; API links={tot_api} UC links={tot_uc}")
    for nid, na, nu in rows:
        flag = "" if (na or nu) else "  <-- 用途不明(API/UC逆引き不可)"
        print(f"  {nid}: API={na} UC={nu}{flag}")


if __name__ == "__main__":
    main()
