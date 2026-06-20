<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-H-005 H_ERROR_LOGS**
<!-- /portal-top -->

# TBL-H-005 H_ERROR_LOGS

履歴 <span id="319-H_ERROR_LOGS"></span>

サーバーエラーを記録するエラーログです。

### <span id="3191-概要"></span>概要

| 項目       | 内容           |
|------------|----------------|
| テーブル名 | `H_ERROR_LOGS` |
| 論理名     | エラーログ     |
| 主キー     | `id`           |
| 外部キー   | —              |

### <span id="3192-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 契約 owner ID | `contract_id` | TEXT | \- | YES |  |  |  |  |  |
| 3 | 操作者種別 | `actor_type` | TEXT | \- | YES |  |  |  |  | `actor_type IN ('owner','project_user')` |
| 4 | 操作者 ID | `actor_id` | TEXT | \- | YES |  |  |  |  | `actor_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 5 | URL | `url` | TEXT | \- | YES |  |  |  |  |  |
| 6 | エラー種別 | `error_type` | TEXT | \- | YES |  |  |  |  |  |
| 7 | スタック | `stack` | TEXT | \- | YES |  |  |  |  |  |
| 8 | 発生日時 | `occurred_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3195-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_error_logs_owner_occurred` | `(contract_id, occurred_at DESC)` |  | オーナー別新着 |

### <span id="3197-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** — **API** —

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
