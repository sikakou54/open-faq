<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-H-004 H_AUDIT_LOGS**
<!-- /portal-top -->

# TBL-H-004 H_AUDIT_LOGS

履歴 一部課金保持 <span id="318-H_AUDIT_LOGS"></span>

メイン管理者向けの API 操作ログを保持します。

### <span id="3181-概要"></span>概要

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
<td><code>H_AUDIT_LOGS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>監査ログ(メイン側、API 操作ログ専用)</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>contract_id</code> → <code>M_CONTRACT(id)</code></li>
<li><code>actor_type</code> + <code>actor_id</code> → <code>M_CONTRACT(id)</code> / <code>M_PRJ_USERS(id)</code>(論理参照)</li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3182-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 契約 owner ID | `contract_id` | TEXT | \- | YES |  | `M_CONTRACT(id)` |  |  |  |
| 3 | 操作者種別 | `actor_type` | TEXT | \- | YES |  |  |  |  | `actor_type IN ('owner','project_user')` |
| 4 | 操作者 ID | `actor_id` | TEXT | \- | YES |  |  |  |  | `actor_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 5 | 操作者ロール | `actor_role` | TEXT | \- | YES |  |  |  |  | `actor_role IS NULL OR actor_role IN ('admin','system')` |
| 6 | アクション | `action` | TEXT | \- | NO |  |  |  |  |  |
| 7 | 対象種別 | `target_type` | TEXT | \- | YES |  |  |  |  |  |
| 8 | 対象 ID | `target_id` | TEXT | \- | YES |  |  |  |  |  |
| 9 | IP(マスク済) | `ip_address_masked` | TEXT | \- | YES |  |  |  |  |  |
| 10 | ユーザーエージェント | `user_agent` | TEXT | \- | YES |  |  |  |  |  |
| 11 | メタデータ | `metadata` | TEXT | \- | YES |  |  |  |  |  |
| 12 | 保持クラス | `retention_class` | TEXT | \- | NO |  |  |  | `'general'` | `retention_class IN ('general','billing')` |
| 13 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3185-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_audit_owner_action_created` | `(contract_id, action, created_at DESC)` |  | オーナー × アクション × 新着 |
| 2 | `idx_audit_retention_created` | `(retention_class, created_at)` |  | 保持期間バッチ用 |
| 3 | `idx_audit_actor_created` | `(actor_type, actor_id, created_at DESC)` |  | 管理者操作の操作者別新着 |

### <span id="3187-コード値区分値"></span>コード値・区分値

| カラム名     | 値       | 意味         |
|--------------|----------|--------------|
| `actor_role` | `admin`  | 利用者管理者 |
| `actor_role` | `system` | システム     |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-004-001](SCR-004-001.md) [SCR-007](SCR-007.md) [SCR-011](SCR-011.md) [SCR-018](SCR-018.md) [SCR-019](SCR-019.md) **API** [API-AUTH-008](02_api-design.md#API-AUTH-008) [API-AUTH-009](02_api-design.md#API-AUTH-009) [API-ANN-003](02_api-design.md#API-ANN-003) [API-PRJ-003](02_api-design.md#API-PRJ-003) [API-WHK-001](02_api-design.md#API-WHK-001)

---

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
