<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-T-006 T_BILL_SUBS**
<!-- /portal-top -->

# TBL-T-006 T_BILL_SUBS

トランザクション 課金 7年保持 <span id="320-T_BILL_SUBS"></span>

Stripe のサブスクリプションと連動する、課金サブスクリプション情報を保持します。

### <span id="3201-概要"></span>概要

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
<td><code>T_BILL_SUBS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>課金サブスクリプション</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>contract_id</code> → <code>M_CONTRACT(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3202-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 契約 owner ID | `contract_id` | TEXT | \- | NO |  | `M_CONTRACT(id)` |  |  |  |
| 3 | Stripe サブスク ID | `stripe_sub_id` | TEXT | \- | YES |  |  | ○ |  |  |
| 4 | 状態 | `status` | TEXT | \- | NO |  |  |  |  | `status IN ('active','past_due','canceled','unpaid','incomplete')` |
| 5 | プラン ID | `plan_id` | TEXT | \- | NO |  |  |  |  |  |
| 6 | 当期開始 | `period_start` | TEXT | \- | YES |  |  |  |  |  |
| 7 | 当期終了 | `period_end` | TEXT | \- | YES |  |  |  |  |  |
| 8 | 解約予定日 | `cancel_at` | TEXT | \- | YES |  |  |  |  |  |
| 9 | 有効フラグ | `valid` | INTEGER | \- | NO |  |  |  | `1` | `valid IN (0,1)` |
| 10 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 11 | 更新日時 | `updated_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3205-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_billing_subs_owner` | `contract_id` |  | オーナー検索 |
| 2 | `idx_billing_subs_status` | `status` |  | 状態別集計 |
| 3 | `idx_billing_subs_valid` | `valid` WHERE `valid = 0` |  | 論理削除済み参照(物理削除対象外) |

### <span id="3207-コード値区分値"></span>コード値・区分値

| カラム名 | 値           | 意味           |
|----------|--------------|----------------|
| `status` | `active`     | 有効           |
| `status` | `past_due`   | 支払遅延       |
| `status` | `canceled`   | 解約済み       |
| `status` | `unpaid`     | 未払い         |
| `status` | `incomplete` | 初回支払未完了 |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-016](SCR-016.md) [SCR-022](SCR-022.md) **API** [API-BIL-003](02_api-design.md#API-BIL-003) [API-BIL-005](02_api-design.md#API-BIL-005)

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
