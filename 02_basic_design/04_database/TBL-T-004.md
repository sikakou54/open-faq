<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-T-004 T_QLOG_FAQ_REFS**
<!-- /portal-top -->

# TBL-T-004 T_QLOG_FAQ_REFS

トランザクション <span id="313-T_QLOG_FAQ_REFS"></span>

質問ログと参照 FAQ の M:N 関係を保持する中間テーブルです。

### <span id="3131-概要"></span>概要

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
<td><code>T_QLOG_FAQ_REFS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>参照 FAQ(M:N)</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>question_log_id</code> → <code>H_QUESTION_LOGS(id)</code></li>
<li><code>faq_id</code> → <code>M_FAQS(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3132-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 質問ログ ID | `question_log_id` | TEXT | \- | NO |  | `H_QUESTION_LOGS(id)` | ① |  |  |
| 3 | FAQ ID | `faq_id` | TEXT | \- | NO |  | `M_FAQS(id)` | ② |  |  |
| 4 | 関連度スコア | `relevance_score` | REAL | \- | YES |  |  |  |  |  |
| 5 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3135-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `uq_question_log_faq_refs_pair` | `(question_log_id, faq_id)` | ○ | M:N ペア一意 |
| 2 | `idx_question_log_faq_refs_faq` | `faq_id` |  | FAQ 別逆引き |

### <span id="3137-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** — **API** —

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
