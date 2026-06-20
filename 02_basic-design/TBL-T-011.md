<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-T-011 T_WITHDRAW_REQ**
<!-- /portal-top -->

# TBL-T-011 T_WITHDRAW_REQ

トランザクション <span id="329-T_WITHDRAW_REQ"></span>

退会申請レコード(90 日猶予)を保持します。

### <span id="3291-概要"></span>概要

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
<td><code>T_WITHDRAW_REQ</code></td>
</tr>
<tr>
<td>論理名</td>
<td>退会申請</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>contract_id</code> → <code>M_CONTRACT(id)</code></li>
<li><code>applied_by_type</code> + <code>applied_by_id</code> → <code>M_CONTRACT(id)</code> / <code>M_PRJ_USERS(id)</code>(論理参照)</li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3292-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 契約 owner ID | `contract_id` | TEXT | \- | NO |  | `M_CONTRACT(id)` |  |  |  |
| 3 | 申請日時 | `applied_at` | TEXT | \- | NO |  |  |  |  |  |
| 4 | 申請者種別 | `applied_by_type` | TEXT | \- | NO |  |  |  |  | `applied_by_type IN ('owner','project_user')` |
| 5 | 申請者 ID | `applied_by_id` | TEXT | \- | NO |  |  |  |  | `applied_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 6 | 理由 | `reason` | TEXT | \- | YES |  |  |  |  |  |
| 7 | 削除予定日 | `scheduled_deletion_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3295-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_withdrawal_owner_scheduled` | `(contract_id, scheduled_deletion_at)` |  | 削除予定日順 |

### <span id="3297-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-014](SCR-014.md) **API** [API-TRM-005](02_api-design.md#API-TRM-005)

---

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
