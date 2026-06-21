<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-H-005 H_INQUIRY_FAQ**
<!-- /portal-top -->

# TBL-H-005 H_INQUIRY_FAQ

履歴 <span id="316-H_INQUIRY_FAQ"></span>

未解決質問から FAQ への移行(FAQ 化)履歴を保持します。

### <span id="3161-概要"></span>概要

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
<td><code>H_INQUIRY_FAQ</code></td>
</tr>
<tr>
<td>論理名</td>
<td>未解決質問 FAQ 化履歴</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>project_id</code> → <code>M_PROJECTS(id)</code></li>
<li><code>inquiry_id</code> → <code>T_INQUIRIES(id)</code></li>
<li><code>faq_id</code> → <code>M_FAQS(id)</code></li>
<li><code>created_by_type</code> + <code>created_by_id</code> → <code>M_CONTRACT(id)</code> / <code>M_PRJ_USERS(id)</code>(論理参照)</li>
</ul></td>
</tr>
<tr>
<td>契約境界</td>
<td><code>project_id</code> → <code>M_PROJECTS.contract_id</code> で導出(本テーブルに <code>contract_id</code> は保持しません)</td>
</tr>
</tbody>
</table>

### <span id="3162-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | プロジェクト ID | `project_id` | TEXT | \- | NO |  | `M_PROJECTS(id)` |  |  |  |
| 3 | 元未解決質問 ID | `inquiry_id` | TEXT | \- | NO |  | `T_INQUIRIES(id)` |  |  |  |
| 4 | 作成 FAQ ID | `faq_id` | TEXT | \- | NO |  | `M_FAQS(id)` |  |  |  |
| 5 | 質問スナップショット | `question_snapshot` | TEXT | \- | NO |  |  |  |  | FAQ 化時点の未解決質問本文のコピー |
| 6 | 実行者種別 | `created_by_type` | TEXT | \- | NO |  |  |  |  | `created_by_type IN ('owner','project_user')` |
| 7 | 実行者 ID | `created_by_id` | TEXT | \- | NO |  |  |  |  | `created_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 8 | 移行日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3165-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_inq_faq_inquiry` | `inquiry_id` |  | 未解決質問からの逆引き |
| 2 | `idx_inq_faq_faq` | `faq_id` |  | FAQ からの逆引き |
| 3 | `idx_inq_faq_project` | `(project_id, created_at DESC)` |  | プロジェクト別の移行新着 |

### <span id="3167-コード値区分値"></span>コード値・区分値

| カラム名 | 値 | 意味 |
|----------|------|------|
| `created_by_type` | `owner` | オーナー |
| `created_by_type` | `project_user` | プロジェクトメンバー |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-007](../01_screens/SCR-007.md) **API** [API-FAQ-001](../03_apis/index.md#API-FAQ-001)

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
