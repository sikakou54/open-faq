<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **M_PRJ_USERS**
<!-- /portal-top -->

# M_PRJ_USERS

マスタ

**プロジェクトメンバー**(プロジェクト管理者 / メンバー)を管理します。ユーザー(`M_USER`)をプロジェクト(`M_PROJECTS`)へ割り当て、プロジェクト別ロールを保持します。**旧 `M_PRJ_USER_ASGN` を統合**し、認証情報は `M_USER` に分離しました。

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
<td><code>M_PRJ_USERS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>プロジェクトメンバー(割当 + ロール)</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>contract_id → M_CONTRACT(id)</code></li>
<li><code>project_id → M_PROJECTS(id)</code></li>
<li><code>user_id → M_USER(id)</code></li>
<li><code>granted_by_user_id → M_USER(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|----|----|----|----|----|----|----|----|----|----|----|
| 1 | 割当ID | `id` | TEXT |  | NOT NULL | ○ |  |  |  |  |
| 2 | 契約ID | `contract_id` | TEXT |  | NOT NULL |  | `M_CONTRACT(id)` |  |  |  |
| 3 | プロジェクトID | `project_id` | TEXT |  | NOT NULL |  | `M_PROJECTS(id)` |  |  |  |
| 4 | ユーザーID | `user_id` | TEXT |  | NOT NULL |  | `M_USER(id)` |  |  |  |
| 5 | ロール | `role` | TEXT |  | NOT NULL |  |  |  |  | `role IN ('admin','member')` |
| 6 | 付与日時 | `granted_at` | TEXT |  | NOT NULL |  |  |  |  |  |
| 7 | 付与者ユーザーID | `granted_by_user_id` | TEXT |  | NULL可 |  | `M_USER(id)` |  |  |  |
| 8 | 有効フラグ | `valid` | INTEGER |  | NOT NULL |  |  |  | `1` | `valid IN (0,1)` |

### <span id="インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|----|----|----|----|----|
| 1 | `uq_prj_user` | `(project_id, user_id)` | ○ | 同一プロジェクトへの重複割当防止 |
| 2 | `idx_prj_users_contract` | `contract_id` |  | 契約境界クエリ |
| 3 | `idx_prj_users_user` | `user_id` |  | ユーザーの参加プロジェクト一覧 |

### <span id="コード値"></span>コード値・区分値

| カラム | 値       | 意味               |
|--------|----------|--------------------|
| `role` | `admin`  | プロジェクト管理者 |
| `role` | `member` | メンバー           |

### <span id="使用元"></span>使用元(画面 / API)

**画面** [SCR-009](SCR-009.md) [SCR-009-001](SCR-009-001.md) **API** [API-MBR-001](02_api-design.md#API-MBR-001) [API-MBR-002](02_api-design.md#API-MBR-002) [API-MBR-003](02_api-design.md#API-MBR-003)

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
