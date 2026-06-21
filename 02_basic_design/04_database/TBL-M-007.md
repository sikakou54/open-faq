<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-M-007 M_EMAIL_SUPPRESS**
<!-- /portal-top -->

# TBL-M-007 M_EMAIL_SUPPRESS

マスタ <span id="317-M_EMAIL_SUPPRESS"></span>

バウンス・苦情を起こしたメールアドレスを全契約横断で管理するサプレスリストです。

### <span id="3171-概要"></span>概要

| 項目       | 内容                             |
|------------|----------------------------------|
| テーブル名 | `M_EMAIL_SUPPRESS`               |
| 論理名     | メールサプレスリスト(全契約横断) |
| 主キー     | `id`                             |
| 外部キー   | —                                |

### <span id="3172-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | メール HMAC | `email_hmac` | TEXT | \- | NO |  |  | ○ |  |  |
| 3 | 理由 | `reason` | TEXT | \- | NO |  |  |  |  | `reason IN ('bounced_hard','bounced_soft_5x','complained','manual')` |
| 4 | 永久フラグ | `is_permanent` | INTEGER | \- | NO |  |  |  | `1` |  |
| 5 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 6 | 解除日時 | `released_at` | TEXT | \- | YES |  |  |  |  |  |

### <span id="3175-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_suppression_permanent` | `(is_permanent, email_hmac)` |  | 永久 / 一時別検索 |

### <span id="3177-コード値区分値"></span>コード値・区分値

| カラム名 | 値                | 意味                  |
|----------|-------------------|-----------------------|
| `reason` | `bounced_hard`    | ハードバウンス        |
| `reason` | `bounced_soft_5x` | ソフトバウンス 5 連続 |
| `reason` | `complained`      | スパム苦情            |
| `reason` | `manual`          | 手動追加              |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** — **API** [API-WHK-001](../03_apis/index.md#API-WHK-001)

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
