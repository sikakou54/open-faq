<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-M-012 M_TERMS_VER**
<!-- /portal-top -->

# TBL-M-012 M_TERMS_VER

マスタ <span id="330-M_TERMS_VER"></span>

利用規約・プライバシーポリシーの版を保持します。

### <span id="3301-概要"></span>概要

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
<td><code>M_TERMS_VER</code></td>
</tr>
<tr>
<td>論理名</td>
<td>規約版数(全契約横断)</td>
</tr>
<tr>
<td>主キー</td>
<td><ul>
<li><code>doc_type</code></li>
<li><code>version</code></li>
</ul></td>
</tr>
<tr>
<td>外部キー</td>
<td>—</td>
</tr>
</tbody>
</table>

### <span id="3302-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | 文書種別 | `doc_type` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 版 | `version` | TEXT | \- | NO | ○ |  |  |  |  |
| 3 | 発効日 | `effective_date` | TEXT | \- | NO |  |  |  |  |  |
| 4 | 本文(HTML) | `body_html` | TEXT | \- | NO |  |  |  |  |  |
| 5 | 差分サマリ | `diff_summary` | TEXT | \- | YES |  |  |  |  |  |
| 6 | 通知送信日時 | `notification_sent_at` | TEXT | \- | YES |  |  |  |  |  |
| 7 | 同意期限日数 | `consent_deadline_days` | INTEGER | \- | NO |  |  |  | `14` |  |
| 8 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3305-インデックス"></span>インデックス

(なし、PK 検索のみ)

### <span id="3307-コード値区分値"></span>コード値・区分値

| カラム     | 値                 | 意味                 |
|------------|--------------------|----------------------|
| `doc_type` | `terms_of_service` | 利用規約             |
| `doc_type` | `privacy_policy`   | プライバシーポリシー |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-010](SCR-010.md) [SCR-015](SCR-015.md) [SCR-020](SCR-020.md) **API** —

---

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
