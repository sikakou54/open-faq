# フェーズ0 — 対象ドキュメント棚卸し

*基準: master(クリーン)/ 全 ID 系列 欠番なし。テキスト量は .md のみ(mocks の png/html は除外)。*

## 集計(系列別)

| 系列 | フォルダ | 件数 | ID レンジ | 欠番 |
|---|---|---:|---|---|
| BR(業務要件) | 01_requirements/01_BusinessRequirement | 146 | BR-001.. | なし |
| RULE(業務ルール) | 01_requirements/01_BusinessRequirement/08_rule.md | 20 | RULE-001.. | なし |
| FR(機能要件) | 01_requirements/02_FunctionalRequirement | 194 | FR-001.. | なし |
| NFR(非機能要件) | 01_requirements/03_NonFunctionalRequirement/07_nfr.md | 79 | NFR-001.. | なし |
| UC(業務ユースケース) | 01_requirements/04_business_usecases | 88 | UC-001..088 | なし |
| SCR(画面) | 02_basic_design/01_frontend/01_screens | 31 | SCR-001..031 | なし |
| EVT(画面イベント) | 02_basic_design/01_frontend/02_screen_events | 231 | EVT-001..231 | なし |
| SYS(システム処理) | 02_basic_design/02_backend/01_system | 15 | SYS-001..015 | なし |
| SEV(システムイベント) | 02_basic_design/02_backend/02_system_events | 28 | SEV-001..028 | なし |
| API | 02_basic_design/02_backend/03_apis | 61 | API-001..061 | なし |
| TBL(テーブル) | 02_basic_design/02_backend/04_database | 32 | TBL-001..032 | なし |
| SEQ(シーケンス) | 02_basic_design/03_sequences | 122 | SEQ-001..122 | なし |
| PERM(権限) | 02_basic_design/04_permissions | 11 | PERM-001..011 | なし |
| ERR(エラー) | 02_basic_design/05_errors | 36 | ERR-001..036 | なし |
| MSG(メッセージ) | 02_basic_design/06_messages | 13 | MSG-001..013 | なし |
| 横断(課金) | 02_basic_design/05_billing-design.md | 1 | — | — |
| FUT(将来対応) | 03_future | 8 | FUT01..06 | — |

テキスト量(.md): 要件定義 ≒660KB / 基本設計 ≒2.09MB / 将来 ≒85KB / CLAUDE.md ≒36KB。

## 分類 × NotebookLM 投入対象

| No | ドキュメント(群) | 分類 | 役割 | NotebookLM投入 | バンドル | 備考 |
|---|---|---|---|---|---|---|
| 1 | CLAUDE.md | 補足(規約) | 設計ルール正本(判定基準) | 対象 | 00_rules | 全フェーズで判定基準として同梱 |
| 2 | 01_requirements/{01_BR,02_FR,03_NFR}/** | 要件定義 | 業務/機能/非機能要件・業務ルール | 対象 | 01_requirements | BR は HTML テーブル、FR/NFR/RULE は節 |
| 3 | 01_requirements/04_business_usecases/** | 要件定義 | 業務ユースケース(業務処理粒度 88) | 対象 | 02_usecases | UC 本文に基本設計情報は持たない規約 |
| 4 | 02_basic_design/01_frontend/{01_screens,02_screen_events}/** | 基本設計 | 画面・画面イベント | 対象 | 03_screens_events | mocks/*.png,*.html は除外 |
| 5 | 02_basic_design/02_backend/{01_system,02_system_events,03_apis,04_database}/** | 基本設計 | システム処理・API・テーブル | 対象 | 04_backend | システム起点(SYS/SEV)含む |
| 6 | 02_basic_design/03_sequences/** | 基本設計 | シーケンス(UC 単位 122) | 対象 | 05_sequences | mermaid 正本 |
| 7 | 02_basic_design/{04_permissions,05_errors,06_messages}/**, 05_billing-design.md | 基本設計 | 権限・エラー・メッセージ・課金 | 対象 | 06_cross | 横断設計 |
| 8 | 02_basic_design/01_frontend/01_screens/mocks/*.png, *.html | 補足 | 画面モック画像/HTML ソース | 対象外 | — | 内容は SCR 本文に反映済み。画像/装飾は文章レビュー対象外 |
| 9 | README.md | 補足 | ポータル索引(自動生成) | 対象外 | — | portal_nav.py 生成物。内容判定対象外(リンク検証は対象) |
| 10 | 03_future/** | 補足(将来) | MVP 後バックログ | 対象外(保留) | — | 要件/基本設計の品質改善スコープ外。整合性で必要なら追加投入 |
| 11 | _build/** | その他(ツール) | ナビ生成・モック描画・本レビュー作業物 | 対象外 | — | 配信対象外 |

## 詳細設計・運用設計の扱い

- 本リポジトリは **要件定義 + 基本設計** のみを管理し、**詳細設計ドキュメントは存在しない**(基本設計の粒度境界として「詳細設計へ移管すべき内容が基本設計に残っていないか」をレビュー観点に含める)。
- 独立した運用設計ドキュメントはなく、運用・監査・ログ・性能・セキュリティは NFR(`07_nfr.md`)が担う。

## 完了条件チェック

- [x] レビュー対象ドキュメントを一覧化(系列別件数・ID レンジ・欠番ゼロを確認)
- [x] 各ドキュメントの分類(要件定義/基本設計/補足/その他)を明確化
- [x] NotebookLM 投入範囲を確定(7 バンドル: 00_rules〜06_cross)
- [x] バンドル生成・ノートブック投入完了(`faqrev`、7 ソース ready)
