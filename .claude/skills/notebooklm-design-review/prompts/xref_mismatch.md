<!-- TEMPLATE: 相互参照取り違えレビュー. NotebookLM excels at this (semantic ID↔title mismatch). Scope to requirements (and optionally + basic design to check inline citations). Verify EACH against the real `## ID: title` headings before fixing. -->
あなたは設計ドキュメントの外部レビュアです。提供ソースのみに基づき、事実に忠実に。推測禁止。

# タスク(網羅的に1回で)
ドキュメント本文中の「他の識別子への相互参照」(例: 『FR-xxx に従う』『FR-xxx を正本』『(FR-xxx)』『NFR-xxx』『RULE-xxx』等)のうち、**参照先IDの主題(見出し `## ID: タイトル` の内容)と、参照している文脈の意味が一致しないもの(取り違え)を全て列挙**してください。各IDの実際の主題を見出しで確認し、文脈と食い違うIDを検出します。これは採番変更の修正漏れ(renumbering residue)で頻出し、リンク検証では検出できない(参照先IDは実在するが意味が違う)ため、意味照合が必要です。

# 出力(厳守)
最初に「総合判定: 取り違えなし / 取り違えあり」。ありの場合のみ表:
| No | 参照元(実在ID/相対パス) | 誤って参照しているID | 文脈上正しいID | 根拠(両IDのタイトル) |
実在IDのタイトルで裏付けられるもののみ挙げる。推測・表空欄系の指摘は挙げない。
