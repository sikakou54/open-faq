<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-T-001 T_SESSIONS**
<!-- /portal-top -->

# TBL-T-001 T_SESSIONS

トランザクション <span id="34-T_SESSIONS"></span>

複数デバイス対応のログインセッションを管理します。

### <span id="341-概要"></span>概要

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
<td><code>T_SESSIONS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>セッション</td>
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

### <span id="342-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | ユーザーID | `user_id` | TEXT | \- | NO |  | `M_USER(id)` |  |  |  |
| 3 | IP アドレス | `ip_address` | TEXT | \- | NO |  |  |  |  |  |
| 4 | ユーザーエージェント | `user_agent` | TEXT | \- | YES |  |  |  |  |  |
| 5 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 6 | 最終アクセス日時 | `last_accessed_at` | TEXT | \- | NO |  |  |  |  |  |
| 7 | 有効期限 | `expires_at` | TEXT | \- | NO |  |  |  |  |  |
| 8 | 失効日時 | `revoked_at` | TEXT | \- | YES |  |  |  |  |  |

### <span id="345-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_sessions_user` | `user_id` WHERE `revoked_at IS NULL` |  | ユーザーの有効セッション抽出 |
| 2 | `idx_sessions_expires` | `expires_at` WHERE `revoked_at IS NULL` |  | 期限切れ抽出 |

### <span id="347-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-001](SCR-001.md) [SCR-004-001](SCR-004-001.md) [SCR-007](SCR-007.md) [SCR-009-001](SCR-009-001.md) **API** [API-AUTH-002](02_api-design.md#API-AUTH-002) [API-AUTH-003](02_api-design.md#API-AUTH-003) [API-MBR-004](02_api-design.md#API-MBR-004) [API-PRJ-003](02_api-design.md#API-PRJ-003)

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
