<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-M-009 M_PRJ_QUOTA_LIMITS**
<!-- /portal-top -->

# TBL-M-009 M_PRJ_QUOTA_LIMITS

マスタ <span id="324-M_PRJ_QUOTA_LIMITS"></span>

質問数の月次上限件数・無料枠・アラート、および FAQ 件数無料枠をプロジェクト単位で保持します。

### <span id="3241-概要"></span>概要

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
<td><code>M_PRJ_QUOTA_LIMITS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>プロジェクト別利用上限・無料枠</td>
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

### <span id="3242-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  | （複合）`(resource_kind = 'q_monthly_limit' AND (threshold IS NOT NULL OR alert_thresholds = '[]')) OR (resource_kind = 'faq_monthly_limit' AND threshold IS NULL AND alert_thresholds = '[]')` |
| 2 | プロジェクト ID | `project_id` | TEXT | \- | NO |  | `M_PROJECTS(id)` | ① |  |  |
| 3 | リソース種別 | `resource_kind` | TEXT | \- | NO |  |  | ① |  | `resource_kind IN ('q_monthly_limit','faq_monthly_limit')` |
| 4 | 月次上限件数 | `threshold` | INTEGER | \- | YES |  |  |  |  |  |
| 5 | 月次無料枠 | `free_quota` | INTEGER | \- | YES |  |  |  |  |  |
| 6 | アラート閾値 | `alert_thresholds` | TEXT | \- | NO |  |  |  | `'[]'` | `json_valid(alert_thresholds) AND json_type(alert_thresholds) = 'array'`。要素の許可値・重複排除・昇順化はAPI層で保証 |
| 7 | 設定元 | `source` | TEXT | \- | NO |  |  | ① | `'owner'` | `source IN ('owner')` |
| 8 | 理由 | `reason` | TEXT | \- | YES |  |  |  |  |  |
| 9 | 有効期限 | `valid_until` | TEXT | \- | YES |  |  |  |  |  |
| 10 | 有効フラグ | `valid` | INTEGER | \- | NO |  |  |  | `1` | `valid IN (0,1)` |
| 11 | 設定者種別 | `created_by_type` | TEXT | \- | YES |  |  |  |  | `created_by_type IN ('owner','project_user')` |
| 12 | 設定者 ID | `created_by_id` | TEXT | \- | YES |  |  |  |  | `created_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 13 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 14 | 更新日時 | `updated_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3245-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `uq_pql_project_kind_source` | `(project_id, resource_kind, source)` WHERE `valid = 1` | ○ | プロジェクト × 課金対象 × 設定元で一意(有効行のみ) |
| 2 | `idx_pql_project_kind` | `(project_id, resource_kind)` |  | プロジェクト別利用設定解決 |
| 3 | `idx_pql_valid` | `valid` WHERE `valid = 0` |  | 論理削除対象抽出 |

### <span id="3247-コード値区分値"></span>コード値・区分値

| カラム名 | 値 | 意味 | デフォルト推奨値(プロジェクト単位) |
|----|----|----|----|
| `resource_kind` | `q_monthly_limit` | 質問数の月次上限件数 | 上限=KV `usage-limit:default:question` / 無料枠=KV `usage-limit:free-default:question`(初期 1,000) |
| `resource_kind` | `faq_monthly_limit` | FAQ 件数の無料枠 | 無料枠=KV `usage-limit:free-default:faq`(初期 100) |

質問数上限の最小 / 最大件数は KV `usage-limit:min` / `usage-limit:max` を入力ガードに用いる。FAQには上限値を保持しない。KV ミラーは `usage-limit:<contract_id>:<project_id>`(30s TTL)。

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-021](../01_screens/SCR-021.md) [SCR-027](../01_screens/SCR-027.md) [SCR-026](../01_screens/SCR-026.md) **API** [API-046](../03_apis/index.md#API-046) [API-047](../03_apis/index.md#API-047)

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
