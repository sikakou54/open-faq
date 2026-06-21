<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-H-001 H_QUESTION_LOGS**
<!-- /portal-top -->

# TBL-H-001 H_QUESTION_LOGS

履歴 <span id="312-H_QUESTION_LOGS"></span>

ウィジェット利用者からの質問と AI 推論結果を記録する質問ログです。

### <span id="3121-概要"></span>概要

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
<td><code>H_QUESTION_LOGS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>質問ログ</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>project_id</code> → <code>M_PROJECTS(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3122-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | プロジェクト ID | `project_id` | TEXT | \- | NO |  | `M_PROJECTS(id)` |  |  |  |
| 3 | 質問本文 | `user_question` | TEXT | \- | NO |  |  |  |  | `length(user_question) BETWEEN 1 AND 2000` |
| 4 | AI 応答 | `ai_response` | TEXT | \- | YES |  |  |  |  |  |
| 5 | 解決フラグ | `is_resolved` | INTEGER | \- | NO |  |  |  | `0` |  |
| 6 | 課金確定フラグ | `metering_billable` | INTEGER | \- | NO |  |  |  | `0` |  |
| 7 | 信頼度スコア | `confidence_score` | REAL | \- | YES |  |  |  |  |  |
| 8 | 関連度スコア | `relevance_score` | REAL | \- | YES |  |  |  |  |  |
| 9 | AI モデル | `ai_model` | TEXT | \- | YES |  |  |  |  |  |
| 10 | 入力トークン数 | `ai_token_count_input` | INTEGER | \- | YES |  |  |  |  |  |
| 11 | 出力トークン数 | `ai_token_count_output` | INTEGER | \- | YES |  |  |  |  |  |
| 12 | 結果種別 | `result_type` | TEXT | \- | YES |  |  |  |  | `result_type IN ('answered','unanswered','error')`(NULL 許容) |
| 13 | 結果理由コード | `result_reason_code` | TEXT | \- | YES |  |  |  |  |  |
| 14 | PII マスク済 | `pii_masked` | INTEGER | \- | NO |  |  |  | `0` |  |
| 15 | セッション ID | `session_id` | TEXT | \- | YES |  |  |  |  |  |
| 16 | IP アドレス | `ip_address` | TEXT | \- | YES |  |  |  |  |  |
| 17 | 有効フラグ | `valid` | INTEGER | \- | NO |  |  |  | `1` | `valid IN (0,1)` |
| 18 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 19 | 更新日時 | `updated_at` | TEXT | \- | NO |  |  |  | `datetime('now')` |  |

### <span id="3125-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_qlog_project_created` | `(project_id, created_at DESC)` |  | プロジェクト別新着 |
| 2 | `idx_qlog_project_billable_created` | `(project_id, metering_billable, created_at DESC)` |  | プロジェクト × 課金確定 |
| 3 | `idx_qlog_valid` | `valid` WHERE `valid = 0` |  | 論理削除対象抽出 |

### <span id="3127-コード値区分値"></span>コード値・区分値

| カラム名      | 値           | 意味      |
|---------------|--------------|-----------|
| `result_type` | `answered`   | 解答あり  |
| `result_type` | `unanswered` | 該当なし  |
| `result_type` | `error`      | AI エラー |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-004-001](SCR-004-001.md) [SCR-005-001](SCR-005-001.md) [SCR-005](SCR-005.md) [SCR-007](SCR-007.md) [SCR-008](SCR-008.md) [SCR-WIDGET](SCR-WIDGET.md) **API** [API-DASH-001](02_api-design.md#API-DASH-001) [API-FAQ-008](02_api-design.md#API-FAQ-008) [API-PRJ-003](02_api-design.md#API-PRJ-003) [API-WGT-002](02_api-design.md#API-WGT-002) [API-WGT-003](02_api-design.md#API-WGT-003)

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
