# 設計書品質改善プロジェクト — 進捗管理盤(STATUS)

*正本: 本ファイル。各フェーズの依頼文 `phaseN_prompt.md`・生回答 `results/phaseN*.json/_answer.md`・整理表 `phaseN_findings.md`・横断対応表 `correspondence.md`。*

> [!NOTE]
> **追加ラウンド(EVT/SEV 独立ページ廃止・アンカー化レビュー)= 合格(収束)。** 報告は [`evtsev_review_report.md`](evtsev_review_report.md)。変更起因の不整合・回帰はゼロ(テンプレ13 / MSG13 / CLAUDE.md / apis index を修正)。
> **既存課題 P2〜P7 も対応完了**: P2/P4/P5/P6/P7 を修正、P3 は設計判断で据置、P1 は偽陽性。NotebookLM ピンポイント再確認(`pconfirm`)で全項目「解消/妥当・新たな不整合なし」を確認。

## 連携方式(確定)

- **方式B: NotebookLM CLI(`nlm`)直接駆動。** ユーザー指示によりローカル CLI を使用(human-bridge は不要化)。
- ノートブック: alias `faqrev` / id `3caccb80-db1e-46e9-878a-1b0b0b83f35c` / 応答長 longer。
- ソース: 7 バンドル(00_rules〜06_cross)を `--file` 投入済み(全 ready)。ID は `source_ids.txt`。
- 実行: `python3 _build/review/ask.py <name> [--sources k1,k2,...]`(依頼文 `<name>_prompt.md` → `results/<name>.json` + `_answer.md`)。
- 修正後の再レビュー: 変更レイヤのみ `make_bundles.py <key>` 再生成 → 旧ソース `nlm source delete` → 新ソース `nlm source add --file --wait` 差し替え → 再 query。
- 認証: セッション約20分・自動回復あり。失敗時 `nlm login`。

## フェーズ進捗

| フェーズ | 内容 | 状態 | 成果物 |
|---|---|---|---|
| 0 | 棚卸し・バンドル・投入 | 完了 | phase0_inventory.md / bundles/ / source_ids.txt |
| 1 | 逆参照レビュー | 完了 | phase1_*_prompt.md / phase1_findings.md |
| 2 | 構成・記載粒度レビュー | 完了 | phase2_*_prompt.md / phase2_findings.md |
| 3 | 抜け漏れレビュー | 完了 | phase3_*_prompt.md / phase3_findings.md |
| 4 | ドキュメント間整合性レビュー | 完了 | phase4_*_prompt.md / phase4_findings.md |
| 5 | 総合レビュー | 完了 | phase5_prompt.md / phase5_findings.md |
| 6 | 指摘対応(修正) | 完了 | correspondence.md(バケットA/B 修正、検証 0/0) |
| 7 | 再レビュー・収束 | 完了 | phase7_prompt.md / results/phase7_answer.md(全解消) |
| 8 | 最終報告 | 完了 | phase8_final_report.md |

**収束**: Phase7 NotebookLM 再レビュー = 全解消・新規なし。残課題 C1-C3/D5/D7/B2 は設計方針判断(要ユーザー)。最終判定: 条件付き合格。

## 重要原則(逸脱禁止)

- レビュー判定は必ず NotebookLM。エージェントは依頼文作成・結果整理・方針決定・修正のみ。
- 要件に無い仕様を足さない/推測補完しない/不明は「要確認」明示。
- 修正後は `python3 _build/portal_nav.py` → CLAUDE.md §検証 で 壊れリンク/アンカー 0/0。
- 欠番禁止・ID 一括張替・各層テンプレ準拠(CLAUDE.md)。


## 第2サイクル(残課題 C1-C3/D5/D7/B2)= 完了
- C1: SYS-016〜033 + SEV-029〜064(18 UC)/ C2: SYS-034(保持削除)/ C3-1: SYS-035(課金再処理)/ C3-2: API-059 順序 / C3-3: NFR-066 方針注記 / D5: FR↔RULE 整合確認(不一致なし)/ D7: 用語統一 / B2: TBL-015 結線。
- SYS 001..035 / SEV 001..068 欠番なし、リンク 0/0。Phase7b NotebookLM 再レビュー = 全解消・新規なし。**最終判定: 合格**。


## 第4サイクル(残課題 #2 検索API結線)= 完了
- FAQ検索を API-031 に整理(EVT-063→API-031、API-025 はキーワード非保持、SEQ-024/025 整合)。質問ログ画面 SCR-032 新設 + EVT-232〜236 + モックPNG + API-032 結線。SCR/EVT index 更新。
- SCR 001..032 / EVT 001..236 欠番なし、リンク 0/0、設計層 要確認 0。phase_c2 NotebookLM 再レビュー = 全解消・新規なし。
- **残る実質課題 = 0。最終判定: 合格(残課題ゼロ)。**
