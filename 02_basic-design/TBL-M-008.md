<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-M-008 M_OWNER_QUOTA_OVR**
<!-- /portal-top -->

# TBL-M-008 M_OWNER_QUOTA_OVR

マスタ <span id="323-M_OWNER_QUOTA_OVR"></span>

契約単位のレート制限上書きを保持します。

### <span id="3231-概要"></span>概要

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
<td><code>M_OWNER_QUOTA_OVR</code></td>
</tr>
<tr>
<td>論理名</td>
<td>契約別レート制限上書き</td>
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

### <span id="3232-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 契約 owner ID | `contract_id` | TEXT | \- | NO |  | `M_CONTRACT(id)` |  |  |  |
| 3 | リソース種別 | `resource_kind` | TEXT | \- | NO |  |  |  |  | `resource_kind IN ('widget_ask_per_min','widget_inquiry_per_min','email_per_hour','admin_api_per_min')` |
| 4 | しきい値 | `threshold` | INTEGER | \- | NO |  |  |  |  |  |
| 5 | 窓秒 | `window_sec` | INTEGER | \- | YES |  |  |  |  |  |
| 6 | 有効期限 | `valid_until` | TEXT | \- | NO |  |  |  |  |  |
| 7 | 理由 | `reason` | TEXT | \- | YES |  |  |  |  |  |
| 8 | 作成者種別 | `created_by_type` | TEXT | \- | YES |  |  |  |  | `created_by_type IN ('owner','project_user')` |
| 9 | 作成者 ID | `created_by_id` | TEXT | \- | YES |  |  |  |  | `created_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 10 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3235-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_tqo_owner_kind` | `(contract_id, resource_kind, valid_until)` |  | オーナー × リソース × 有効期限 |

### <span id="3237-コード値区分値"></span>コード値・区分値

| カラム名        | 値                       | 意味                             |
|-----------------|--------------------------|----------------------------------|
| `resource_kind` | `widget_ask_per_min`     | ウィジェット質問レート           |
| `resource_kind` | `widget_inquiry_per_min` | ウィジェット未解決質問送信レート |
| `resource_kind` | `email_per_hour`         | メール送信レート                 |
| `resource_kind` | `admin_api_per_min`      | 管理 API レート                  |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** — **API** —

---

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
