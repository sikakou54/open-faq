<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-T-008 T_USAGE_METER**
<!-- /portal-top -->

# TBL-T-008 T_USAGE_METER

トランザクション 課金 7年保持 <span id="322-T_USAGE_METER"></span>

質問数・FAQ 件数をプロジェクト単位で計測し、請求はオーナーで SUM 集計します。

### <span id="3221-概要"></span>概要

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
<td><code>T_USAGE_METER</code></td>
</tr>
<tr>
<td>論理名</td>
<td>利用量計測(プロジェクト単位)</td>
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
</ul></td>
</tr>
</tbody>
</table>

### <span id="3222-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 契約 owner ID | `contract_id` | TEXT | \- | NO |  | `M_CONTRACT(id)` | ① |  |  |
| 3 | プロジェクト ID | `project_id` | TEXT | \- | NO |  | `M_PROJECTS(id)` | ② |  |  |
| 4 | 請求年月 | `billing_ym` | TEXT | \- | NO |  |  | ② |  |  |
| 5 | 質問数 | `question_count` | INTEGER | \- | NO |  |  |  | `0` |  |
| 6 | FAQ 数(スナップショット) | `faq_cnt_snapshot` | INTEGER | \- | NO |  |  |  | `0` |  |
| 7 | AI 入力トークン | `ai_token_input` | INTEGER | \- | NO |  |  |  | `0` |  |
| 8 | AI 出力トークン | `ai_token_output` | INTEGER | \- | NO |  |  |  | `0` |  |
| 9 | AI コスト(円) | `ai_cost_yen` | INTEGER | \- | NO |  |  |  | `0` |  |
| 10 | 確定日時 | `finalized_at` | TEXT | \- | YES |  |  |  |  |  |
| 11 | 更新日時 | `updated_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3225-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `uq_usage_metering_owner_project_month` | `(contract_id, project_id, billing_ym)` | ○ | プロジェクト × 月次一意 |
| 2 | `idx_usage_metering_owner_month` | `(contract_id, billing_ym)` |  | 契約集計(請求 SUM)用 |

### <span id="3227-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-008](SCR-008.md) [SCR-016](SCR-016.md) [SCR-021-001](SCR-021-001.md) [SCR-021](SCR-021.md) [SCR-022](SCR-022.md) [SCR-WIDGET](SCR-WIDGET.md) **API** [API-DASH-001](02_api-design.md#API-DASH-001) [API-BIL-001](02_api-design.md#API-BIL-001) [API-BIL-002](02_api-design.md#API-BIL-002) [API-BIL-003](02_api-design.md#API-BIL-003) [API-BIL-006](02_api-design.md#API-BIL-006) [API-WGT-002](02_api-design.md#API-WGT-002)

---

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
