<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **M_PRJ_USERS**
<!-- /portal-top -->

# M_PRJ_USERS

マスタ

**プロジェクトメンバー**(ユーザー × プロジェクトの割当)を管理します。ユーザー(`M_USER`)をプロジェクト(`M_PROJECTS`)へ割り当てます。プロジェクト内の役割差は持たず、割り当てられた利用者は全員「メンバー」として同一権限です。認証情報は `M_USER` が保持します。オーナーは作成した各プロジェクトに自動的にメンバー割当行を持ちます(認可権威は `M_CONTRACT` の isOwner であり、本テーブルは一覧表示・担当割当・通知宛先の網羅に用います)。契約境界は `project_id` → `M_PROJECTS.contract_id` で導出するため、本テーブルに `contract_id` は保持しません。

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
<td>プロジェクトメンバー(割当)</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>project_id → M_PROJECTS(id)</code></li>
<li><code>user_id → M_USER(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|----|----|----|----|----|----|----|----|----|----|----|
| 1 | 割当ID | `id` | TEXT |  | NOT NULL | ○ |  |  |  |  |
| 2 | プロジェクトID | `project_id` | TEXT |  | NOT NULL |  | `M_PROJECTS(id)` |  |  |  |
| 3 | ユーザーID | `user_id` | TEXT |  | NOT NULL |  | `M_USER(id)` |  |  |  |
| 4 | 付与日時 | `granted_at` | TEXT |  | NOT NULL |  |  |  |  |  |
| 5 | 有効フラグ | `valid` | INTEGER |  | NOT NULL |  |  |  | `1` | `valid IN (0,1)` |

### <span id="インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|----|----|----|----|----|
| 1 | `uq_prj_user` | `(project_id, user_id)` | ○ | 同一プロジェクトへの重複割当防止 |
| 2 | `idx_prj_users_user` | `user_id` |  | ユーザーの参加プロジェクト一覧 |

### <span id="使用元"></span>使用元(画面 / API)

**画面** [SCR-013](../01_screens/SCR-013.md) [SCR-014](../01_screens/SCR-014.md) **API** [API-MBR-001](../03_apis/index.md#API-MBR-001) [API-MBR-002](../03_apis/index.md#API-MBR-002) [API-MBR-003](../03_apis/index.md#API-MBR-003)

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
