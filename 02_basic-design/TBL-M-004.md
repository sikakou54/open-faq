<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **M_PROJECTS**
<!-- /portal-top -->

# M_PROJECTS

マスタ

FAQ プロジェクトとウィジェット設定を保持します。**契約マスタ `M_CONTRACT` の子テーブル**であり、契約境界は `contract_id` で表します(旧 `contract_id` を置換)。

### <span id="概要"></span>概要

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th>項目</th>
<th>内容</th>
</tr>
</thead>
<tbody>
<tr>
<td>テーブル名</td>
<td><code>M_PROJECTS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>プロジェクト</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>contract_id → M_CONTRACT(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|----|----|----|----|----|----|----|----|----|----|----|
| 1 | プロジェクトID | `id` | TEXT |  | NOT NULL | ○ |  |  |  |  |
| 2 | 契約ID | `contract_id` | TEXT |  | NOT NULL |  | `M_CONTRACT(id)` |  |  |  |
| 3 | プロジェクト名 | `name` | TEXT |  | NOT NULL |  |  |  |  | `length(name) BETWEEN 1 AND 100` |
| 4 | 説明 | `description` | TEXT |  | NULL可 |  |  |  |  |  |
| 5 | 状態 | `status` | TEXT |  | NOT NULL |  |  |  | `'active'` | `status IN ('active','deleted')` |
| 6 | ウィジェット公開鍵 | `widget_public_key` | TEXT |  | NOT NULL |  |  | ○ |  |  |
| 7 | 連絡先メール | `contact_email` | TEXT |  | NULL可 |  |  |  |  |  |
| 8 | 連絡先確認日時 | `contact_verified_at` | TEXT |  | NULL可 |  |  |  |  |  |
| 9 | 設定JSON | `settings` | TEXT |  | NOT NULL |  |  |  | `'{}'` |  |
| 10 | 有効フラグ | `valid` | INTEGER |  | NOT NULL |  |  |  | `1` | `valid IN (0,1)` |
| 11 | 作成日時 | `created_at` | TEXT |  | NOT NULL |  |  |  |  |  |
| 12 | 更新日時 | `updated_at` | TEXT |  | NOT NULL |  |  |  |  |  |

### <span id="インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|----|----|----|----|----|
| 1 | `idx_projects_status` | `(contract_id, status)` |  | 契約別プロジェクト一覧 |
| 2 | `idx_projects_widget_key` | `widget_public_key` | ○ | ウィジェット鍵検索 |

### <span id="コード値"></span>コード値・区分値

| カラム   | 値        | 意味     |
|----------|-----------|----------|
| `status` | `active`  | 有効     |
| `status` | `deleted` | 論理削除 |

### <span id="使用元"></span>使用元(画面 / API)

**画面** [SCR-004](SCR-004.md) [SCR-004-001](SCR-004-001.md) [SCR-007](SCR-007.md) [SCR-008](SCR-008.md) **API** [API-PRJ-001](02_api-design.md#API-PRJ-001) [API-PRJ-002](02_api-design.md#API-PRJ-002) [API-PRJ-003](02_api-design.md#API-PRJ-003)

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
