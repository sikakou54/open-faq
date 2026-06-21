<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [データベース設計](index.md) ／ **TBL-TP-001 TP_FAQ_FTS**
<!-- /portal-top -->

# TBL-TP-001 TP_FAQ_FTS

ワーク <span id="311-TP_FAQ_FTS"></span>

FAQ 全文検索用の FTS5 仮想テーブル(trigram トークナイザ)です。

### <span id="3111-概要"></span>概要

| 項目       | 内容                            |
|------------|---------------------------------|
| テーブル名 | `TP_FAQ_FTS`                    |
| 論理名     | FAQ 全文検索(FTS5 仮想テーブル) |
| 主キー     | rowid(`M_FAQS.rowid` と一致)    |
| 外部キー   | —                               |

### <span id="3112-カラム定義"></span>カラム定義

|  No | 論理名   | 物理名     | データ型 | 桁数 | NULL | PK  | FK  | UNIQUE | DEFAULT | 制約 |
|----:|----------|------------|----------|-----:|------|-----|-----|--------|---------|------|
|   1 | タイトル | `title`    | TEXT     |   \- | \-   |     |     |        |         |      |
|   2 | 本文     | `body`     | TEXT     |   \- | \-   |     |     |        |         |      |
|   3 | カテゴリ | `category` | TEXT     |   \- | \-   |     |     |        |         |      |
|   4 | タグ     | `tags`     | TEXT     |   \- | \-   |     |     |        |         |      |

### <span id="3115-インデックス"></span>インデックス

(FTS5 内部インデックス、明示作成なし)

### <span id="3116-制約トリガ"></span>制約・トリガ

FTS5 contentless 同期トリガ 3 個(基本設計が正本):

| No | トリガ名 | 種別 | 対象 | 条件・内容 |
|---:|----|----|----|----|
| 1 | `faq_search_fts_ai` | AFTER INSERT トリガ | `M_FAQS` | 新規行を `TP_FAQ_FTS` に INSERT |
| 2 | `faq_search_fts_ad` | AFTER DELETE トリガ | `M_FAQS` | `'delete'` コマンドで削除行を FTS から除去 |
| 3 | `faq_search_fts_au` | AFTER UPDATE トリガ | `M_FAQS` | 旧行を `'delete'` コマンドで除去 → 新行を INSERT |

### <span id="3117-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** — **API** [API-FAQ-007](../02_api-design/index.md#API-FAQ-007)

---

<!-- portal-bottom -->
[← データベース設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
