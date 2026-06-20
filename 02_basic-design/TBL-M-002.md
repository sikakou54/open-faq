<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **M_CONTRACT**
<!-- /portal-top -->

# M_CONTRACT

マスタ 新規

**契約を管理する契約マスタ**です。`id` が契約境界キー本体であり、`M_PROJECTS` など契約スコープのテーブルはこの契約を親に持ちます。**オーナー判定**は `user_id` と一致するユーザーを当該契約のオーナーとみなします(1 契約 = 1 オーナー)。

### <span id="概要"></span>概要

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
<td><code>M_CONTRACT</code></td>
</tr>
<tr>
<td>論理名</td>
<td>契約マスタ</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>user_id → M_USER(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|----|----|----|----|----|----|----|----|----|----|----|
| 1 | 契約ID | `id` | TEXT |  | NOT NULL | ○ |  |  |  |  |
| 2 | オーナーユーザーID | `user_id` | TEXT |  | NOT NULL |  | `M_USER(id)` |  |  |  |
| 3 | 契約状態 | `status` | TEXT |  | NOT NULL |  |  |  | `'active'` | `status IN ('active','suspended','deleted_pending','deleted')` |
| 4 | データ削除モード | `data_deletion_mode` | TEXT |  | NULL可 |  |  |  |  |  |
| 5 | 作成日時 | `created_at` | TEXT |  | NOT NULL |  |  |  |  |  |
| 6 | 更新日時 | `updated_at` | TEXT |  | NOT NULL |  |  |  |  |  |

### <span id="インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|----|----|----|----|----|
| 1 | `idx_contract_owner` | `user_id` |  | オーナーユーザーからの契約逆引き(オーナー判定) |
| 2 | `idx_status` | `status` |  | 契約状態での抽出(サスペンション / 退会バッチ) |

### <span id="コード値"></span>コード値・区分値

| カラム   | 値                | 意味                 |
|----------|-------------------|----------------------|
| `status` | `active`          | 有効                 |
| `status` | `suspended`       | 停止(決済失敗等)     |
| `status` | `deleted_pending` | 退会申請中(猶予期間) |
| `status` | `deleted`         | 削除済               |

### <span id="使用元"></span>使用元(画面 / API)

**画面** [SCR-016](SCR-016.md) [SCR-022](SCR-022.md) [SCR-023](SCR-023.md) [SCR-014](SCR-014.md) **API** [API-AUTH-001](02_api-design.md#API-AUTH-001) [API-BIL-003](02_api-design.md#API-BIL-003) [API-TRM-005](02_api-design.md#API-TRM-005)

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
