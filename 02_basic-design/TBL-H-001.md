<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-H-001 H_FAQ_REV**
<!-- /portal-top -->

# TBL-H-001 H_FAQ_REV

履歴 <span id="310-H_FAQ_REV"></span>

FAQ の改訂履歴を全文スナップショットで最大 50 件保持します。

### <span id="3101-概要"></span>概要

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
<td><code>H_FAQ_REV</code></td>
</tr>
<tr>
<td>論理名</td>
<td>FAQ 改訂履歴</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>faq_id</code> → <code>M_FAQS(id)</code></li>
<li><code>created_by_type</code> + <code>created_by_id</code> → <code>M_CONTRACT(id)</code> / <code>M_PRJ_USERS(id)</code>(論理参照)</li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3102-カラム定義-1"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | FAQ ID | `faq_id` | TEXT | \- | NO |  | `M_FAQS(id)` |  |  |  |
| 3 | バージョン | `version` | INTEGER | \- | NO |  |  |  |  |  |
| 4 | タイトル | `title` | TEXT | \- | NO |  |  |  |  |  |
| 5 | 本文 | `body` | TEXT | \- | NO |  |  |  |  |  |
| 6 | カテゴリ | `category` | TEXT | \- | YES |  |  |  |  |  |
| 7 | タグ | `tags` | TEXT | \- | YES |  |  |  |  |  |
| 8 | 状態スナップショット | `status_snapshot` | TEXT | \- | NO |  |  |  |  | `status_snapshot IN ('draft','published','hidden','deleted')` |
| 9 | 由来 | `source` | TEXT | \- | NO |  |  |  | `'manual'` | `source IN ('manual','import')` |
| 10 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 11 | 作成者種別 | `created_by_type` | TEXT | \- | NO |  |  |  |  | `created_by_type IN ('owner','project_user')` |
| 12 | 作成者 ID | `created_by_id` | TEXT | \- | NO |  |  |  |  | `created_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |

### <span id="3105-インデックス-1"></span>インデックス

|  No | インデックス名             | 対象カラム               | UNIQUE | 用途         |
|----:|----------------------------|--------------------------|--------|--------------|
|   1 | `idx_faq_revisions_faq`    | `(faq_id, version DESC)` |        | 版数降順抽出 |
|   2 | `idx_faq_revisions_source` | `source`                 |        | 由来別集計   |

### <span id="3107-コード値区分値-1"></span>コード値・区分値

| カラム名 | 値       | 意味                 |
|----------|----------|----------------------|
| `source` | `manual` | 手動編集             |
| `source` | `import` | インポートによる作成 |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-006-001](SCR-006-001.md) [SCR-006-002](SCR-006-002.md) **API** [API-FAQ-002](02_api-design.md#API-FAQ-002) [API-FAQ-004](02_api-design.md#API-FAQ-004)

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
