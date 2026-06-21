<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-T-002 T_ACCESS_TOKENS**
<!-- /portal-top -->

# TBL-T-002 T_ACCESS_TOKENS

トランザクション <span id="35-T_ACCESS_TOKENS"></span>

招待・パスワード再設定・メール確認などの短期トークンを保持します。

### <span id="351-概要"></span>概要

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
<td><code>T_ACCESS_TOKENS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>アクセストークン</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>user_id → M_USER(id)</code>(<code>contact_verify</code> は主体ユーザーが無く NULL。対象プロジェクトは <code>meta</code>)</li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="352-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | ユーザーID | `user_id` | TEXT | \- | YES |  | `M_USER(id)` |  |  | `contact_verify` は主体ユーザーが無く NULL(対象は `meta`) |
| 3 | トークンハッシュ | `token_hash` | TEXT | \- | NO |  |  | ○ |  |  |
| 4 | 用途 | `purpose` | TEXT | \- | NO |  |  |  |  | `purpose IN ('email_verify','password_reset','activation','contact_verify')` |
| 5 | メタ情報 | `meta` | TEXT | \- | YES |  |  |  |  |  |
| 6 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 7 | 有効期限 | `expires_at` | TEXT | \- | NO |  |  |  |  |  |
| 8 | 使用日時 | `used_at` | TEXT | \- | YES |  |  |  |  |  |

### <span id="355-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `uq_access_tokens_hash` | `token_hash` | ○ | トークン検索 |
| 2 | `idx_access_tokens_expires` | `expires_at` WHERE `used_at IS NULL` |  | 未使用トークン期限切れ抽出 |

### <span id="357-コード値区分値"></span>コード値・区分値

| カラム名  | 値               | 意味                         |
|-----------|------------------|------------------------------|
| `purpose` | `email_verify`   | メール確認                   |
| `purpose` | `password_reset` | パスワード再設定             |
| `purpose` | `activation`     | メンバーアカウント有効化     |
| `purpose` | `contact_verify` | プロジェクト連絡先メール確認 |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-002](../01_screens/SCR-002.md) [SCR-003](../01_screens/SCR-003.md) [SCR-005](../01_screens/SCR-005.md) [SCR-011](../01_screens/SCR-011.md) [SCR-014](../01_screens/SCR-014.md) [SCR-018](../01_screens/SCR-018.md) [SCR-019](../01_screens/SCR-019.md) [SCR-023](../01_screens/SCR-023.md) [SCR-024](../01_screens/SCR-024.md) **API** [API-AUTH-001](../03_apis/index.md#API-AUTH-001) [API-AUTH-004](../03_apis/index.md#API-AUTH-004) [API-AUTH-005](../03_apis/index.md#API-AUTH-005) [API-AUTH-006](../03_apis/index.md#API-AUTH-006) [API-AUTH-007](../03_apis/index.md#API-AUTH-007) [API-AUTH-008](../03_apis/index.md#API-AUTH-008) [API-AUTH-009](../03_apis/index.md#API-AUTH-009) [API-MBR-002](../03_apis/index.md#API-MBR-002) [API-MBR-004](../03_apis/index.md#API-MBR-004) [API-MBR-005](../03_apis/index.md#API-MBR-005) [API-PRJ-003](../03_apis/index.md#API-PRJ-003)

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
