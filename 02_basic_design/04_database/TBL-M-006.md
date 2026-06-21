<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-M-006 M_FAQS**
<!-- /portal-top -->

# TBL-M-006 M_FAQS

マスタ <span id="39-M_FAQS"></span>

FAQ 本体(質問・回答・公開状態)を保持します。契約境界は `project_id` → `M_PROJECTS.contract_id` で導出します。

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
<li><code>project_id</code> → <code>M_PROJECTS(id)</code></li>
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
| 2 | プロジェクト ID | `project_id` | TEXT | \- | NO |  | `M_PROJECTS(id)` |  |  |  |
| 3 | 質問(タイトル) | `title` | TEXT | \- | NO |  |  |  |  | `length(title) BETWEEN 1 AND 500`(FAQ 質問、FR-025) |
| 4 | 回答(本文) | `body` | TEXT | \- | NO |  |  |  |  | `length(body) BETWEEN 1 AND 5000`(FAQ 回答、FR-025) |
| 5 | カテゴリ | `category` | TEXT | \- | YES |  |  |  |  |  |
| 6 | 状態 | `status` | TEXT | \- | NO |  |  |  | `'draft'` | `status IN ('draft','published','hidden','deleted')` |
| 7 | バージョン | `version` | INTEGER | \- | NO |  |  |  | `1` |  |
| 8 | タグ | `tags` | TEXT | \- | YES |  |  |  |  |  |
| 9 | 有効フラグ | `valid` | INTEGER | \- | NO |  |  |  | `1` | `valid IN (0,1)` |
| 10 | 作成者種別 | `created_by_type` | TEXT | \- | YES |  |  |  |  | `created_by_type IN ('owner','project_user')` |
| 11 | 作成者 ID | `created_by_id` | TEXT | \- | YES |  |  |  |  | `created_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 12 | 更新者種別 | `updated_by_type` | TEXT | \- | YES |  |  |  |  | `updated_by_type IN ('owner','project_user')` |
| 13 | 更新者 ID | `updated_by_id` | TEXT | \- | YES |  |  |  |  | `updated_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 14 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 15 | 更新日時 | `updated_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="395-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_faqs_project_status` | `(project_id, status)` |  | プロジェクト × 状態 |
| 2 | `idx_faqs_category` | `(project_id, category)` WHERE `category IS NOT NULL` |  | カテゴリ別 |
| 3 | `idx_faqs_valid` | `valid` WHERE `valid = 0` |  | 論理削除対象抽出 |

### <span id="397-コード値区分値"></span>コード値・区分値

| カラム名 | 値          | 意味     |
|----------|-------------|----------|
| `status` | `draft`     | 下書き   |
| `status` | `published` | 公開中   |
| `status` | `hidden`    | 非公開   |
| `status` | `deleted`   | 論理削除 |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-004-001](../01_screens/SCR-004-001.md) [SCR-004](../01_screens/SCR-004.md) [SCR-005-001](../01_screens/SCR-005-001.md) [SCR-006-001](../01_screens/SCR-006-001.md) [SCR-006-002](../01_screens/SCR-006-002.md) [SCR-006](../01_screens/SCR-006.md) [SCR-007](../01_screens/SCR-007.md) [SCR-008](../01_screens/SCR-008.md) [SCR-WIDGET](../01_screens/SCR-WIDGET.md) **API** [API-FAQ-001](../03_apis/index.md#API-FAQ-001) [API-FAQ-002](../03_apis/index.md#API-FAQ-002) [API-FAQ-003](../03_apis/index.md#API-FAQ-003) [API-FAQ-004](../03_apis/index.md#API-FAQ-004) [API-FAQ-006](../03_apis/index.md#API-FAQ-006) [API-FAQ-007](../03_apis/index.md#API-FAQ-007) [API-PRJ-001](../03_apis/index.md#API-PRJ-001) [API-PRJ-003](../03_apis/index.md#API-PRJ-003) [API-BIL-001](../03_apis/index.md#API-BIL-001) [API-BIL-002](../03_apis/index.md#API-BIL-002) [API-WGT-002](../03_apis/index.md#API-WGT-002)

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
