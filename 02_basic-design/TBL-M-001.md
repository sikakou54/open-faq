<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **M_USER**
<!-- /portal-top -->

# M_USER

マスタ 新規

オーナー・プロジェクト管理者・メンバーを含む**すべてのユーザー**の認証情報(メール / パスワード / 氏名)を一元保持するユーザーマスタです。オーナーかどうかの判定は `M_CONTRACT.user_id` 参照で行い、本テーブルには契約属性を持ちません。

### <span id="概要"></span>概要

| 項目       | 内容           |
|------------|----------------|
| テーブル名 | `M_USER`       |
| 論理名     | ユーザーマスタ |
| 主キー     | `id`           |
| 外部キー   | なし           |

### <span id="カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|----|----|----|----|----|----|----|----|----|----|----|
| 1 | ユーザーID | `id` | TEXT |  | NOT NULL | ○ |  |  |  |  |
| 2 | メールアドレス | `email` | TEXT |  | NOT NULL |  |  | ○ |  |  |
| 3 | パスワードハッシュ | `password_hash` | TEXT |  | NOT NULL |  |  |  |  |  |
| 4 | 氏名 | `name` | TEXT |  | NOT NULL |  |  |  |  |  |
| 5 | メール確認日時 | `email_verified_at` | TEXT |  | NULL可 |  |  |  |  |  |
| 6 | 状態 | `status` | TEXT |  | NOT NULL |  |  |  | `'active'` | `status IN ('active','suspended','deleted')` |
| 7 | 有効フラグ | `valid` | INTEGER |  | NOT NULL |  |  |  | `1` | `valid IN (0,1)` |
| 8 | 作成日時 | `created_at` | TEXT |  | NOT NULL |  |  |  |  |  |
| 9 | 更新日時 | `updated_at` | TEXT |  | NOT NULL |  |  |  |  |  |

### <span id="インデックス"></span>インデックス

| No  | インデックス名  | 対象カラム | UNIQUE | 用途                                   |
|-----|-----------------|------------|--------|----------------------------------------|
| 1   | `uq_user_email` | `email`    | ○      | メールアドレスの一意制約・ログイン照会 |

### <span id="コード値"></span>コード値・区分値

| カラム   | 値          | 意味     |
|----------|-------------|----------|
| `status` | `active`    | 有効     |
| `status` | `suspended` | 停止     |
| `status` | `deleted`   | 論理削除 |

### <span id="使用元"></span>使用元(画面 / API)

**画面** [SCR-001](SCR-001.md) [SCR-002](SCR-002.md) [SCR-017](SCR-017.md) [SCR-018](SCR-018.md) **API** [API-AUTH-001](02_api-design.md#API-AUTH-001) [API-AUTH-002](02_api-design.md#API-AUTH-002) [API-MBR-002](02_api-design.md#API-MBR-002)

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
