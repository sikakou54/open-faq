<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-M-006 M_FAQS**
<!-- /portal-top -->

# TBL-M-006 M_FAQS

マスタ <span id="39-M_FAQS"></span>

FAQ 本体(質問・回答・公開状態)を保持します。

### <span id="391-概要"></span>概要

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
<td><code>M_FAQS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>FAQ</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>contract_id</code> → <code>M_CONTRACT(id)</code></li>
<li><code>project_id</code> → <code>M_PROJECTS(id)</code></li>
<li><code>source_inquiry_id</code> → <code>T_INQUIRIES(id)</code></li>
<li><code>created_by_type</code> + <code>created_by_id</code> → <code>M_CONTRACT(id)</code> / <code>M_PRJ_USERS(id)</code>(論理参照)</li>
<li><code>updated_by_type</code> + <code>updated_by_id</code> → <code>M_CONTRACT(id)</code> / <code>M_PRJ_USERS(id)</code>(論理参照)</li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="392-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 契約 owner ID | `contract_id` | TEXT | \- | NO |  | `M_CONTRACT(id)` |  |  |  |
| 3 | プロジェクト ID | `project_id` | TEXT | \- | NO |  | `M_PROJECTS(id)` |  |  |  |
| 4 | 質問(タイトル) | `title` | TEXT | \- | NO |  |  |  |  | `length(title) BETWEEN 1 AND 500`(FAQ 質問、FR-040) |
| 5 | 回答(本文) | `body` | TEXT | \- | NO |  |  |  |  | `length(body) BETWEEN 1 AND 5000`(FAQ 回答、FR-040) |
| 6 | カテゴリ | `category` | TEXT | \- | YES |  |  |  |  |  |
| 7 | 状態 | `status` | TEXT | \- | NO |  |  |  | `'draft'` | `status IN ('draft','published','hidden','deleted')` |
| 8 | バージョン | `version` | INTEGER | \- | NO |  |  |  | `1` |  |
| 9 | タグ | `tags` | TEXT | \- | YES |  |  |  |  |  |
| 10 | 元未解決質問 ID | `source_inquiry_id` | TEXT | \- | YES |  | `T_INQUIRIES(id)` |  |  |  |
| 11 | 有効フラグ | `valid` | INTEGER | \- | NO |  |  |  | `1` | `valid IN (0,1)` |
| 12 | 作成者種別 | `created_by_type` | TEXT | \- | YES |  |  |  |  | `created_by_type IN ('owner','project_user')` |
| 13 | 作成者 ID | `created_by_id` | TEXT | \- | YES |  |  |  |  | `created_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 14 | 更新者種別 | `updated_by_type` | TEXT | \- | YES |  |  |  |  | `updated_by_type IN ('owner','project_user')` |
| 15 | 更新者 ID | `updated_by_id` | TEXT | \- | YES |  |  |  |  | `updated_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 16 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 17 | 更新日時 | `updated_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="395-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_faqs_owner_project` | `(contract_id, project_id)` |  | 契約境界 + プロジェクト |
| 2 | `idx_faqs_project_status` | `(project_id, status)` |  | プロジェクト × 状態 |
| 3 | `idx_faqs_source_inquiry` | `source_inquiry_id` |  | 元未解決質問逆引き |
| 4 | `idx_faqs_category` | `(project_id, category)` WHERE `category IS NOT NULL` |  | カテゴリ別 |
| 5 | `idx_faqs_valid` | `valid` WHERE `valid = 0` |  | 論理削除対象抽出 |

### <span id="397-コード値区分値"></span>コード値・区分値

| カラム名 | 値          | 意味     |
|----------|-------------|----------|
| `status` | `draft`     | 下書き   |
| `status` | `published` | 公開中   |
| `status` | `hidden`    | 非公開   |
| `status` | `deleted`   | 論理削除 |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-004-001](SCR-004-001.md) [SCR-004](SCR-004.md) [SCR-005-001](SCR-005-001.md) [SCR-006-001](SCR-006-001.md) [SCR-006-002](SCR-006-002.md) [SCR-006](SCR-006.md) [SCR-007](SCR-007.md) [SCR-008](SCR-008.md) [SCR-WIDGET](SCR-WIDGET.md) **API** [API-FAQ-001](02_api-design.md#API-FAQ-001) [API-FAQ-002](02_api-design.md#API-FAQ-002) [API-FAQ-003](02_api-design.md#API-FAQ-003) [API-FAQ-004](02_api-design.md#API-FAQ-004) [API-FAQ-006](02_api-design.md#API-FAQ-006) [API-FAQ-007](02_api-design.md#API-FAQ-007) [API-PRJ-001](02_api-design.md#API-PRJ-001) [API-PRJ-003](02_api-design.md#API-PRJ-003) [API-BIL-001](02_api-design.md#API-BIL-001) [API-BIL-002](02_api-design.md#API-BIL-002) [API-WGT-002](02_api-design.md#API-WGT-002)

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
