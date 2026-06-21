<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-T-005 T_INQUIRIES**
<!-- /portal-top -->

# TBL-T-005 T_INQUIRIES

トランザクション <span id="314-T_INQUIRIES"></span>

FAQ 登録前の未解決質問を保持します。

### <span id="3141-概要"></span>概要

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
<td><code>T_INQUIRIES</code></td>
</tr>
<tr>
<td>論理名</td>
<td>未解決質問</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>project_id</code> → <code>M_PROJECTS(id)</code></li>
<li><code>question_log_id</code> → <code>H_QUESTION_LOGS(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3142-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | プロジェクト ID | `project_id` | TEXT | \- | NO |  | `M_PROJECTS(id)` |  |  |  |
| 3 | 問い合わせコード | `inquiry_code` | TEXT | \- | NO |  |  | ○ |  |  |
| 4 | 元質問ログ ID | `question_log_id` | TEXT | \- | YES |  | `H_QUESTION_LOGS(id)` |  |  |  |
| 5 | 質問本文 | `user_question` | TEXT | \- | NO |  |  |  |  |  |
| 6 | 状況 | `status` | TEXT | \- | NO |  |  |  | `'open'` | `status IN ('open','closed')` |
| 7 | 有効フラグ | `valid` | INTEGER | \- | NO |  |  |  | `1` | `valid IN (0,1)` |
| 8 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 9 | 更新日時 | `updated_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3145-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_inquiries_project_status_created` | `(project_id, status, created_at DESC)` |  | プロジェクト × 状況別新着 |
| 2 | `uq_inquiries_code` | `inquiry_code` | ○ | 問い合わせコード一意 |
| 3 | `idx_inquiries_valid` | `valid` WHERE `valid = 0` |  | 論理削除対象抽出 |

### <span id="3147-コード値区分値"></span>コード値・区分値

| カラム名 | 値       | 意味     |
|----------|----------|----------|
| `status` | `open`   | 対応必要 |
| `status` | `closed` | 終了     |

状態は `status`(`open` / `closed`)で管理する。

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-004-001](../01_screens/SCR-004-001.md) [SCR-005-001](../01_screens/SCR-005-001.md) [SCR-005](../01_screens/SCR-005.md) [SCR-006-001](../01_screens/SCR-006-001.md) [SCR-007](../01_screens/SCR-007.md) [SCR-008](../01_screens/SCR-008.md) [SCR-WIDGET](../01_screens/SCR-WIDGET.md) **API** [API-DASH-001](../03_apis/index.md#API-DASH-001) [API-INQ-001](../03_apis/index.md#API-INQ-001) [API-INQ-002](../03_apis/index.md#API-INQ-002) [API-PRJ-003](../03_apis/index.md#API-PRJ-003) [API-WGT-002](../03_apis/index.md#API-WGT-002) [API-WGT-003](../03_apis/index.md#API-WGT-003)

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
