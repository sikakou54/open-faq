# 要件↔UC 被覆ギャップ 精査レポート(P7 後続・判断材料)

> **このページは、再構成 P7 で検出した要件↔ユースケースの被覆ギャップを精査し、未対応要素ごとの対応候補と妥当性所見・推奨方針を提示します(オーナー判断の材料)。**
> - 一時管理ディレクトリ `99_management/` 内の作業用ドキュメント。最終成果物ではない。
> - データ出典: `p7_linkgraph.json`(順引き/逆引きリンク)・`p7_gaps.json`(ギャップ分類)。検証対象外(本文リンクは設計書を指す)。

*版数 v1.0 ・ 作成 2026-06-21 ・ ステータス 判断待ち*

## 1. 要旨

P7 で「要件→UC」「UC→要件」双方向のトレースを照合した結果、被覆ギャップの**実数**は当初の概算と異なり、内訳は次の通り。**大半は真の被覆漏れではなく、画面イベント由来 UC が親画面の要件参照を引き継いでいない「トレース連結漏れ」**であることが判明した。

- **FR**: 194 中 **132 が UC 未対応**(対応 62)。本ギャップの主対象。
- **BR**: 146 中 **6 のみ未対応**(対応 140)。軽微。
- **NFR**: 79 すべて未対応。**性質上 UC 直結しない**(品質特性・横断要件)— 想定どおりで受容可。
- **RULE**: 20 すべて未対応。業務ルールは UC の事前/事後条件で参照されるべき連結漏れ。
- **UC→要件 未対応**: 247 中 **128**。ただし **128 件すべてに「同一画面で要件を保有する兄弟 UC」が存在**し、候補要件を機械導出できる(下表)。

> [!IMPORTANT]
> **結論(所見)**: ギャップの主因は、画面 1 イベント = 1 UC へ細分化した際に、親画面を駆動する FR 参照を各 EVT 由来 UC に**転記しなかった**こと。よって解消は「新規要件の創出」ではなく **既存 FR の機械的な再連結 + 一部 FR の UC 割当**で大部分が片付く。下表の候補をレビューのうえ採否を確定すれば、追加設計を最小化して被覆を引き上げられる。

## 2. 被覆サマリ

各 `##`/`###` 節は表の前に1〜2文の説明を置く(本書の作法に準拠)。下表は系列別の被覆状況。

| 系列 | 全件 | UC対応 | UC未対応 | 所見 |
|---|---|---|---|---|
| BR | 146 | 140 | 6 | 軽微。§4 に列挙し個別判断 |
| FR | 194 | 62 | 132 | **主対象**。§3 の候補で再連結 |
| NFR | 79 | 0 | 79 | 想定どおり(品質特性)。受容 |
| RULE | 20 | 0 | 20 | UC 事前/事後条件で参照すべき。§4 |

## 3. 未対応 UC → 候補要件(同一画面の兄弟 UC から導出)

画面操作を伴う UC は、同じ画面 `SCR-*` に紐づく他 UC が保有する要件を共有する蓋然性が高い。下表は未対応 UC ごとに、同一画面の兄弟 UC が参照する要件を頻度順に候補提示する。**候補要件はそのまま当該 UC の「対応要件」へ再連結する第一候補**である。

| UC | 名称 | 画面 | 候補FR | 候補BR | 所見 |
|---|---|---|---|---|---|
| [UC-029](../01_requirements/02_business_usecases/UC-029.md#UC-029) | 「+ 新規プロジェクトを作成」を押下 | SCR-004 SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-030](../01_requirements/02_business_usecases/UC-030.md#UC-030) | プロジェクト名リンクを押下 | SCR-004 SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-031](../01_requirements/02_business_usecases/UC-031.md#UC-031) | 管理範囲を切り替え | SCR-004 SCR-012 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) / [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-032](../01_requirements/02_business_usecases/UC-032.md#UC-032) | 空状態の「+ 新規プロジェクトを作成」を押下 | SCR-004 SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-034](../01_requirements/02_business_usecases/UC-034.md#UC-034) | 初期表示(編集モード) | SCR-005 SCR-004 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-035](../01_requirements/02_business_usecases/UC-035.md#UC-035) | プロジェクト名を入力 | SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-036](../01_requirements/02_business_usecases/UC-036.md#UC-036) | 許可ドメインを入力 | SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-037](../01_requirements/02_business_usecases/UC-037.md#UC-037) | プロジェクト連絡先メールを入力 | SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-040](../01_requirements/02_business_usecases/UC-040.md#UC-040) | 「確認メールを再送」を押下 | SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-041](../01_requirements/02_business_usecases/UC-041.md#UC-041) | 削除確認名称を入力 | SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-042](../01_requirements/02_business_usecases/UC-042.md#UC-042) | 「プロジェクトを削除」を押下 | SCR-005 SCR-004 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-043](../01_requirements/02_business_usecases/UC-043.md#UC-043) | 「キャンセル」を押下 | SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-044](../01_requirements/02_business_usecases/UC-044.md#UC-044) | 「コピー」を押下(プロジェクト ID) | SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-045](../01_requirements/02_business_usecases/UC-045.md#UC-045) | × を押下 | SCR-005 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) | — | 兄弟UCの要件を再連結 |
| [UC-047](../01_requirements/02_business_usecases/UC-047.md#UC-047) | 状況フィルタをチェック | SCR-006 | [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |
| [UC-048](../01_requirements/02_business_usecases/UC-048.md#UC-048) | 期間フィルタを入力 | SCR-006 | [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |
| [UC-049](../01_requirements/02_business_usecases/UC-049.md#UC-049) | 「CSV エクスポート」を押下 | SCR-006 | [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |
| [UC-050](../01_requirements/02_business_usecases/UC-050.md#UC-050) | 問い合わせ ID リンクを押下 | SCR-006 SCR-007 | [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) / [FR-075](../01_requirements/01_specifications/FR-075.md#FR-075) | — | 兄弟UCの要件を再連結 |
| [UC-051](../01_requirements/02_business_usecases/UC-051.md#UC-051) | 検索ボックスに入力 | SCR-006 | [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |
| [UC-052](../01_requirements/02_business_usecases/UC-052.md#UC-052) | ページを選択 | SCR-006 | [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |
| [UC-053](../01_requirements/02_business_usecases/UC-053.md#UC-053) | 「ウィジェット設定を見る」を押下 | SCR-006 SCR-011 | [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) / [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-058](../01_requirements/02_business_usecases/UC-058.md#UC-058) | 確認ダイアログの「キャンセル」を押下 | SCR-007 | [FR-075](../01_requirements/01_specifications/FR-075.md#FR-075) / [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |
| [UC-059](../01_requirements/02_business_usecases/UC-059.md#UC-059) | 登録先 FAQ リンクを押下 | SCR-007 SCR-008 | [FR-075](../01_requirements/01_specifications/FR-075.md#FR-075) / [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |
| [UC-060](../01_requirements/02_business_usecases/UC-060.md#UC-060) | 候補 FAQ リンクを押下 | SCR-007 SCR-008 | [FR-075](../01_requirements/01_specifications/FR-075.md#FR-075) / [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |
| [UC-061](../01_requirements/02_business_usecases/UC-061.md#UC-061) | 「FAQ 登録へ」を押下 | SCR-007 SCR-009 | [FR-075](../01_requirements/01_specifications/FR-075.md#FR-075) / [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) | — | 兄弟UCの要件を再連結 |
| [UC-062](../01_requirements/02_business_usecases/UC-062.md#UC-062) | 初期表示 | SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-063](../01_requirements/02_business_usecases/UC-063.md#UC-063) | キーワードを入力 | SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-064](../01_requirements/02_business_usecases/UC-064.md#UC-064) | カテゴリを選択 | SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-065](../01_requirements/02_business_usecases/UC-065.md#UC-065) | 並び順を変更 | SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-067](../01_requirements/02_business_usecases/UC-067.md#UC-067) | 「+ 新規作成」を押下 | SCR-008 SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) / [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) | — | 兄弟UCの要件を再連結 |
| [UC-068](../01_requirements/02_business_usecases/UC-068.md#UC-068) | FAQ ID リンクを押下 | SCR-008 SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) / [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) | — | 兄弟UCの要件を再連結 |
| [UC-069](../01_requirements/02_business_usecases/UC-069.md#UC-069) | 「公開する」を押下 | SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-070](../01_requirements/02_business_usecases/UC-070.md#UC-070) | 「非公開化する」を押下 | SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-072](../01_requirements/02_business_usecases/UC-072.md#UC-072) | 「選択を解除」を押下 | SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-073](../01_requirements/02_business_usecases/UC-073.md#UC-073) | 「CSV をインポート」を押下 | SCR-008 SCR-010 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-074](../01_requirements/02_business_usecases/UC-074.md#UC-074) | 「CSV をエクスポート」を押下 | SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-075](../01_requirements/02_business_usecases/UC-075.md#UC-075) | 空状態の「+ 新規作成」を押下 | SCR-008 SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) / [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) | — | 兄弟UCの要件を再連結 |
| [UC-077](../01_requirements/02_business_usecases/UC-077.md#UC-077) | 質問を入力 | SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) | — | 兄弟UCの要件を再連結 |
| [UC-078](../01_requirements/02_business_usecases/UC-078.md#UC-078) | 回答を入力 | SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) | — | 兄弟UCの要件を再連結 |
| [UC-079](../01_requirements/02_business_usecases/UC-079.md#UC-079) | カテゴリを入力 | SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) | — | 兄弟UCの要件を再連結 |
| [UC-081](../01_requirements/02_business_usecases/UC-081.md#UC-081) | 自動保存 | SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) | — | 兄弟UCの要件を再連結 |
| [UC-083](../01_requirements/02_business_usecases/UC-083.md#UC-083) | 削除ボタン押下 | SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) | — | 兄弟UCの要件を再連結 |
| [UC-084](../01_requirements/02_business_usecases/UC-084.md#UC-084) | 削除確認 OK | SCR-009 SCR-008 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) / [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) | — | 兄弟UCの要件を再連結 |
| [UC-085](../01_requirements/02_business_usecases/UC-085.md#UC-085) | キャンセル押下 | SCR-009 SCR-008 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) / [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) | — | 兄弟UCの要件を再連結 |
| [UC-086](../01_requirements/02_business_usecases/UC-086.md#UC-086) | 登録元未解決質問へ遷移 | SCR-009 SCR-007 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-075](../01_requirements/01_specifications/FR-075.md#FR-075) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) | — | 兄弟UCの要件を再連結 |
| [UC-087](../01_requirements/02_business_usecases/UC-087.md#UC-087) | 削除確認キャンセル | SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) | — | 兄弟UCの要件を再連結 |
| [UC-088](../01_requirements/02_business_usecases/UC-088.md#UC-088) | キャンセル確認 OK | SCR-009 SCR-008 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) / [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) | — | 兄弟UCの要件を再連結 |
| [UC-089](../01_requirements/02_business_usecases/UC-089.md#UC-089) | キャンセル確認キャンセル | SCR-009 | [FR-053](../01_requirements/01_specifications/FR-053.md#FR-053) / [FR-047](../01_requirements/01_specifications/FR-047.md#FR-047) | — | 兄弟UCの要件を再連結 |
| [UC-091](../01_requirements/02_business_usecases/UC-091.md#UC-091) | 「テンプレートをダウンロード」を押下 | SCR-010 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) | — | 兄弟UCの要件を再連結 |
| [UC-092](../01_requirements/02_business_usecases/UC-092.md#UC-092) | ファイル選択にファイルを投入 | SCR-010 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) | — | 兄弟UCの要件を再連結 |
| [UC-094](../01_requirements/02_business_usecases/UC-094.md#UC-094) | 「キャンセル」を押下 | SCR-010 SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-095](../01_requirements/02_business_usecases/UC-095.md#UC-095) | 「×」を押下 | SCR-010 SCR-008 | [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) / [FR-174](../01_requirements/01_specifications/FR-174.md#FR-174) | — | 兄弟UCの要件を再連結 |
| [UC-097](../01_requirements/02_business_usecases/UC-097.md#UC-097) | 「コピー」を押下(公開キー) | SCR-011 | [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-098](../01_requirements/02_business_usecases/UC-098.md#UC-098) | 「コードをコピー」を押下(埋め込みコード) | SCR-011 | [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-099](../01_requirements/02_business_usecases/UC-099.md#UC-099) | テーマカラーを選択 | SCR-011 | [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-100](../01_requirements/02_business_usecases/UC-100.md#UC-100) | 主色(HEX)を入力 | SCR-011 | [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-101](../01_requirements/02_business_usecases/UC-101.md#UC-101) | 表示位置を選択 | SCR-011 | [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-102](../01_requirements/02_business_usecases/UC-102.md#UC-102) | 見出しを入力 | SCR-011 | [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-103](../01_requirements/02_business_usecases/UC-103.md#UC-103) | 初期メッセージを入力 | SCR-011 | [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-104](../01_requirements/02_business_usecases/UC-104.md#UC-104) | 「公開キーを再発行する」を押下 | SCR-011 | [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-105](../01_requirements/02_business_usecases/UC-105.md#UC-105) | 「設定を保存」を押下 | SCR-011 | [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) | — | 兄弟UCの要件を再連結 |
| [UC-106](../01_requirements/02_business_usecases/UC-106.md#UC-106) | 「概要」を押下 | SCR-011 SCR-012 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-040](../01_requirements/01_specifications/FR-040.md#FR-040) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-108](../01_requirements/02_business_usecases/UC-108.md#UC-108) | 期間を選択 | SCR-012 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) / [FR-100](../01_requirements/01_specifications/FR-100.md#FR-100) | — | 兄弟UCの要件を再連結 |
| [UC-109](../01_requirements/02_business_usecases/UC-109.md#UC-109) | 質問数カードを押下 | SCR-012 SCR-006 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-110](../01_requirements/02_business_usecases/UC-110.md#UC-110) | 未解決数カードを押下 | SCR-012 SCR-006 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-111](../01_requirements/02_business_usecases/UC-111.md#UC-111) | 公開 FAQ 件数カードを押下 | SCR-012 SCR-008 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-169](../01_requirements/01_specifications/FR-169.md#FR-169) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-112](../01_requirements/02_business_usecases/UC-112.md#UC-112) | 「支払方法を更新」を押下(オーナー) | SCR-012 SCR-028 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-090](../01_requirements/01_specifications/FR-090.md#FR-090) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-113](../01_requirements/02_business_usecases/UC-113.md#UC-113) | 「支払い方法を登録」を押下(オーナー) | SCR-012 SCR-028 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-090](../01_requirements/01_specifications/FR-090.md#FR-090) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-114](../01_requirements/02_business_usecases/UC-114.md#UC-114) | 「利用量と上限へ」を押下 | SCR-012 SCR-026 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-088](../01_requirements/01_specifications/FR-088.md#FR-088) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-115](../01_requirements/02_business_usecases/UC-115.md#UC-115) | 初期表示 | SCR-013 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-116](../01_requirements/02_business_usecases/UC-116.md#UC-116) | 検索を入力 | SCR-013 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-117](../01_requirements/02_business_usecases/UC-117.md#UC-117) | 招待状態フィルタを選択 | SCR-013 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-118](../01_requirements/02_business_usecases/UC-118.md#UC-118) | 「+ メンバーを招待」を押下 | SCR-013 SCR-014 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-119](../01_requirements/02_business_usecases/UC-119.md#UC-119) | (空状態)「+ メンバーを招待」を押下 | SCR-013 SCR-014 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-120](../01_requirements/02_business_usecases/UC-120.md#UC-120) | 利用者表示名リンクを押下 | SCR-013 SCR-014 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-121](../01_requirements/02_business_usecases/UC-121.md#UC-121) | 権限なしで URL 直アクセス | SCR-013 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-122](../01_requirements/02_business_usecases/UC-122.md#UC-122) | 「ダッシュボードへ戻る」を押下 | SCR-013 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-124](../01_requirements/02_business_usecases/UC-124.md#UC-124) | 初期表示 — 編集モード | SCR-014 SCR-013 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-125](../01_requirements/02_business_usecases/UC-125.md#UC-125) | メールアドレスを入力 | SCR-014 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-127](../01_requirements/02_business_usecases/UC-127.md#UC-127) | 「招待メールを再送する」を押下 | SCR-014 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-131](../01_requirements/02_business_usecases/UC-131.md#UC-131) | 「×」を押下してモーダルを閉じる | SCR-014 SCR-013 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-132](../01_requirements/02_business_usecases/UC-132.md#UC-132) | 「キャンセル」を押下 | SCR-014 SCR-013 | [FR-027](../01_requirements/01_specifications/FR-027.md#FR-027) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-036](../01_requirements/01_specifications/FR-036.md#FR-036) | — | 兄弟UCの要件を再連結 |
| [UC-134](../01_requirements/02_business_usecases/UC-134.md#UC-134) | 「再同意へ」リンクを押下 | SCR-015 SCR-020 | [FR-139](../01_requirements/01_specifications/FR-139.md#FR-139) / [FR-010](../01_requirements/01_specifications/FR-010.md#FR-010) / [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) | — | 兄弟UCの要件を再連結 |
| [UC-137](../01_requirements/02_business_usecases/UC-137.md#UC-137) | クイックフィルタチップを選択 | SCR-016 | [FR-156](../01_requirements/01_specifications/FR-156.md#FR-156) / [FR-155](../01_requirements/01_specifications/FR-155.md#FR-155) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) | — | 兄弟UCの要件を再連結 |
| [UC-138](../01_requirements/02_business_usecases/UC-138.md#UC-138) | 「すべてクリア」を押下 | SCR-016 | [FR-156](../01_requirements/01_specifications/FR-156.md#FR-156) / [FR-155](../01_requirements/01_specifications/FR-155.md#FR-155) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) | — | 兄弟UCの要件を再連結 |
| [UC-139](../01_requirements/02_business_usecases/UC-139.md#UC-139) | 詳細フィルタを適用 | SCR-016 | [FR-156](../01_requirements/01_specifications/FR-156.md#FR-156) / [FR-155](../01_requirements/01_specifications/FR-155.md#FR-155) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) | — | 兄弟UCの要件を再連結 |
| [UC-145](../01_requirements/02_business_usecases/UC-145.md#UC-145) | 「次のページ」を押下 | SCR-016 | [FR-156](../01_requirements/01_specifications/FR-156.md#FR-156) / [FR-155](../01_requirements/01_specifications/FR-155.md#FR-155) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) | — | 兄弟UCの要件を再連結 |
| [UC-146](../01_requirements/02_business_usecases/UC-146.md#UC-146) | 「選択を解除」を押下 | SCR-016 | [FR-156](../01_requirements/01_specifications/FR-156.md#FR-156) / [FR-155](../01_requirements/01_specifications/FR-155.md#FR-155) / [FR-173](../01_requirements/01_specifications/FR-173.md#FR-173) | — | 兄弟UCの要件を再連結 |
| [UC-148](../01_requirements/02_business_usecases/UC-148.md#UC-148) | 「一覧へ戻る」を押下 | SCR-017 SCR-016 | [FR-156](../01_requirements/01_specifications/FR-156.md#FR-156) / [FR-157](../01_requirements/01_specifications/FR-157.md#FR-157) / [FR-155](../01_requirements/01_specifications/FR-155.md#FR-155) | — | 兄弟UCの要件を再連結 |
| [UC-149](../01_requirements/02_business_usecases/UC-149.md#UC-149) | 「前のお知らせ」を押下 | SCR-017 | [FR-156](../01_requirements/01_specifications/FR-156.md#FR-156) / [FR-157](../01_requirements/01_specifications/FR-157.md#FR-157) | — | 兄弟UCの要件を再連結 |
| [UC-150](../01_requirements/02_business_usecases/UC-150.md#UC-150) | 「次のお知らせ」を押下 | SCR-017 | [FR-156](../01_requirements/01_specifications/FR-156.md#FR-156) / [FR-157](../01_requirements/01_specifications/FR-157.md#FR-157) | — | 兄弟UCの要件を再連結 |
| [UC-153](../01_requirements/02_business_usecases/UC-153.md#UC-153) | 「メールアドレスを変更する」を押下 | SCR-018 SCR-002 | [FR-003](../01_requirements/01_specifications/FR-003.md#FR-003) / [FR-001](../01_requirements/01_specifications/FR-001.md#FR-001) / [FR-149](../01_requirements/01_specifications/FR-149.md#FR-149) | — | 兄弟UCの要件を再連結 |
| [UC-154](../01_requirements/02_business_usecases/UC-154.md#UC-154) | 「新規登録からやり直す」を押下 | SCR-018 SCR-002 | [FR-003](../01_requirements/01_specifications/FR-003.md#FR-003) / [FR-001](../01_requirements/01_specifications/FR-001.md#FR-001) / [FR-149](../01_requirements/01_specifications/FR-149.md#FR-149) | — | 兄弟UCの要件を再連結 |
| [UC-157](../01_requirements/02_business_usecases/UC-157.md#UC-157) | 退会理由を入力 | SCR-019 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-138](../01_requirements/01_specifications/FR-138.md#FR-138) | — | 兄弟UCの要件を再連結 |
| [UC-158](../01_requirements/02_business_usecases/UC-158.md#UC-158) | 「退会を申請する」を押下 | SCR-019 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-138](../01_requirements/01_specifications/FR-138.md#FR-138) | — | 兄弟UCの要件を再連結 |
| [UC-160](../01_requirements/02_business_usecases/UC-160.md#UC-160) | 「個人設定へ戻る」を押下 | SCR-019 SCR-022 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-005](../01_requirements/01_specifications/FR-005.md#FR-005) / [FR-001](../01_requirements/01_specifications/FR-001.md#FR-001) | — | 兄弟UCの要件を再連結 |
| [UC-161](../01_requirements/02_business_usecases/UC-161.md#UC-161) | 契約名を入力 | SCR-019 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-138](../01_requirements/01_specifications/FR-138.md#FR-138) | — | 兄弟UCの要件を再連結 |
| [UC-162](../01_requirements/02_business_usecases/UC-162.md#UC-162) | パスワードを入力(再認証) | SCR-019 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-138](../01_requirements/01_specifications/FR-138.md#FR-138) | — | 兄弟UCの要件を再連結 |
| [UC-163](../01_requirements/02_business_usecases/UC-163.md#UC-163) | 「キャンセル」を押下 | SCR-019 SCR-022 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-005](../01_requirements/01_specifications/FR-005.md#FR-005) / [FR-001](../01_requirements/01_specifications/FR-001.md#FR-001) | — | 兄弟UCの要件を再連結 |
| [UC-165](../01_requirements/02_business_usecases/UC-165.md#UC-165) | 「利用規約」リンクを押下 | SCR-020 SCR-015 | [FR-010](../01_requirements/01_specifications/FR-010.md#FR-010) / [FR-139](../01_requirements/01_specifications/FR-139.md#FR-139) / [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) | — | 兄弟UCの要件を再連結 |
| [UC-166](../01_requirements/02_business_usecases/UC-166.md#UC-166) | 「プライバシーポリシー」リンクを押下 | SCR-020 SCR-025 | [FR-010](../01_requirements/01_specifications/FR-010.md#FR-010) / [FR-139](../01_requirements/01_specifications/FR-139.md#FR-139) / [FR-137](../01_requirements/01_specifications/FR-137.md#FR-137) | — | 兄弟UCの要件を再連結 |
| [UC-171](../01_requirements/02_business_usecases/UC-171.md#UC-171) | 「請求を確認」を押下 | SCR-021 SCR-028 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-090](../01_requirements/01_specifications/FR-090.md#FR-090) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-172](../01_requirements/02_business_usecases/UC-172.md#UC-172) | 「プロジェクトへ」を押下 | SCR-021 SCR-004 | [FR-037](../01_requirements/01_specifications/FR-037.md#FR-037) / [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-007](../01_requirements/01_specifications/FR-007.md#FR-007) | — | 兄弟UCの要件を再連結 |
| [UC-174](../01_requirements/02_business_usecases/UC-174.md#UC-174) | タブを押下 | SCR-022 | [FR-005](../01_requirements/01_specifications/FR-005.md#FR-005) / [FR-001](../01_requirements/01_specifications/FR-001.md#FR-001) / [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) | — | 兄弟UCの要件を再連結 |
| [UC-179](../01_requirements/02_business_usecases/UC-179.md#UC-179) | 「変更を破棄」を押下 | SCR-022 | [FR-005](../01_requirements/01_specifications/FR-005.md#FR-005) / [FR-001](../01_requirements/01_specifications/FR-001.md#FR-001) / [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) | — | 兄弟UCの要件を再連結 |
| [UC-180](../01_requirements/02_business_usecases/UC-180.md#UC-180) | 参加プロジェクト名リンクを押下 | SCR-022 SCR-012 | [FR-005](../01_requirements/01_specifications/FR-005.md#FR-005) / [FR-001](../01_requirements/01_specifications/FR-001.md#FR-001) / [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) | — | 兄弟UCの要件を再連結 |
| [UC-186](../01_requirements/02_business_usecases/UC-186.md#UC-186) | 利用規約の「全文を見る」を押下 | SCR-023 SCR-015 | [FR-137](../01_requirements/01_specifications/FR-137.md#FR-137) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-018](../01_requirements/01_specifications/FR-018.md#FR-018) | — | 兄弟UCの要件を再連結 |
| [UC-188](../01_requirements/02_business_usecases/UC-188.md#UC-188) | プライバシーポリシーの「全文を見る」を押下 | SCR-023 SCR-025 | [FR-137](../01_requirements/01_specifications/FR-137.md#FR-137) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) / [FR-018](../01_requirements/01_specifications/FR-018.md#FR-018) | — | 兄弟UCの要件を再連結 |
| [UC-191](../01_requirements/02_business_usecases/UC-191.md#UC-191) | 「ログインする」を押下(完了画面) | SCR-023 SCR-001 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-137](../01_requirements/01_specifications/FR-137.md#FR-137) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) | — | 兄弟UCの要件を再連結 |
| [UC-192](../01_requirements/02_business_usecases/UC-192.md#UC-192) | 「ログインへ」を押下(トークン無効 / 期限切れエラー画面) | SCR-023 SCR-001 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-137](../01_requirements/01_specifications/FR-137.md#FR-137) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) | — | 兄弟UCの要件を再連結 |
| [UC-193](../01_requirements/02_business_usecases/UC-193.md#UC-193) | 「ログインへ」を押下(既使用エラー画面) | SCR-023 SCR-001 | [FR-004](../01_requirements/01_specifications/FR-004.md#FR-004) / [FR-137](../01_requirements/01_specifications/FR-137.md#FR-137) / [FR-022](../01_requirements/01_specifications/FR-022.md#FR-022) | — | 兄弟UCの要件を再連結 |
| [UC-197](../01_requirements/02_business_usecases/UC-197.md#UC-197) | 「再同意する」を押下 | SCR-025 SCR-020 | [FR-010](../01_requirements/01_specifications/FR-010.md#FR-010) / [FR-137](../01_requirements/01_specifications/FR-137.md#FR-137) / [FR-139](../01_requirements/01_specifications/FR-139.md#FR-139) | — | 兄弟UCの要件を再連結 |
| [UC-198](../01_requirements/02_business_usecases/UC-198.md#UC-198) | 「利用規約」を押下 | SCR-025 SCR-015 | [FR-139](../01_requirements/01_specifications/FR-139.md#FR-139) / [FR-137](../01_requirements/01_specifications/FR-137.md#FR-137) | — | 兄弟UCの要件を再連結 |
| [UC-200](../01_requirements/02_business_usecases/UC-200.md#UC-200) | 「アラート設定」を押下 | SCR-026 SCR-027 | [FR-088](../01_requirements/01_specifications/FR-088.md#FR-088) / [FR-089](../01_requirements/01_specifications/FR-089.md#FR-089) / [FR-092](../01_requirements/01_specifications/FR-092.md#FR-092) | — | 兄弟UCの要件を再連結 |
| [UC-201](../01_requirements/02_business_usecases/UC-201.md#UC-201) | URL へ直接アクセス(権限不足) | SCR-026 | [FR-088](../01_requirements/01_specifications/FR-088.md#FR-088) / [FR-089](../01_requirements/01_specifications/FR-089.md#FR-089) | — | 兄弟UCの要件を再連結 |
| [UC-203](../01_requirements/02_business_usecases/UC-203.md#UC-203) | 上限設定トグルを切り替え | SCR-027 | [FR-088](../01_requirements/01_specifications/FR-088.md#FR-088) / [FR-089](../01_requirements/01_specifications/FR-089.md#FR-089) / [FR-092](../01_requirements/01_specifications/FR-092.md#FR-092) | — | 兄弟UCの要件を再連結 |
| [UC-207](../01_requirements/02_business_usecases/UC-207.md#UC-207) | 「キャンセル」を押下 | SCR-027 SCR-026 | [FR-088](../01_requirements/01_specifications/FR-088.md#FR-088) / [FR-089](../01_requirements/01_specifications/FR-089.md#FR-089) / [FR-092](../01_requirements/01_specifications/FR-092.md#FR-092) | — | 兄弟UCの要件を再連結 |
| [UC-210](../01_requirements/02_business_usecases/UC-210.md#UC-210) | 「領収書」リンクを押下 | SCR-028 | [FR-090](../01_requirements/01_specifications/FR-090.md#FR-090) / [FR-089](../01_requirements/01_specifications/FR-089.md#FR-089) | — | 兄弟UCの要件を再連結 |
| [UC-211](../01_requirements/02_business_usecases/UC-211.md#UC-211) | 「利用量と上限を確認」リンクを押下 | SCR-028 SCR-026 | [FR-089](../01_requirements/01_specifications/FR-089.md#FR-089) / [FR-090](../01_requirements/01_specifications/FR-090.md#FR-090) / [FR-088](../01_requirements/01_specifications/FR-088.md#FR-088) | — | 兄弟UCの要件を再連結 |
| [UC-212](../01_requirements/02_business_usecases/UC-212.md#UC-212) | 「退会手続きへ」リンクを押下 | SCR-028 SCR-029 | [FR-090](../01_requirements/01_specifications/FR-090.md#FR-090) / [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-089](../01_requirements/01_specifications/FR-089.md#FR-089) | — | 兄弟UCの要件を再連結 |
| [UC-214](../01_requirements/02_business_usecases/UC-214.md#UC-214) | 「プランを変更」を押下 | SCR-028 | [FR-090](../01_requirements/01_specifications/FR-090.md#FR-090) / [FR-089](../01_requirements/01_specifications/FR-089.md#FR-089) | — | 兄弟UCの要件を再連結 |
| [UC-216](../01_requirements/02_business_usecases/UC-216.md#UC-216) | 請求・重要通知メールを入力 | SCR-029 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-138](../01_requirements/01_specifications/FR-138.md#FR-138) | — | 兄弟UCの要件を再連結 |
| [UC-218](../01_requirements/02_business_usecases/UC-218.md#UC-218) | 「退会手続きへ」を押下 | SCR-029 SCR-019 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-138](../01_requirements/01_specifications/FR-138.md#FR-138) | — | 兄弟UCの要件を再連結 |
| [UC-219](../01_requirements/02_business_usecases/UC-219.md#UC-219) | 「請求」を押下 | SCR-029 SCR-028 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-090](../01_requirements/01_specifications/FR-090.md#FR-090) / [FR-138](../01_requirements/01_specifications/FR-138.md#FR-138) | — | 兄弟UCの要件を再連結 |
| [UC-220](../01_requirements/02_business_usecases/UC-220.md#UC-220) | タイムゾーンを選択 | SCR-029 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-138](../01_requirements/01_specifications/FR-138.md#FR-138) | — | 兄弟UCの要件を再連結 |
| [UC-221](../01_requirements/02_business_usecases/UC-221.md#UC-221) | 「変更を破棄」を押下 | SCR-029 | [FR-009](../01_requirements/01_specifications/FR-009.md#FR-009) / [FR-138](../01_requirements/01_specifications/FR-138.md#FR-138) | — | 兄弟UCの要件を再連結 |
| [UC-224](../01_requirements/02_business_usecases/UC-224.md#UC-224) | ヘッダーの閉じるボタンを押下 | SCR-030 | [FR-057](../01_requirements/01_specifications/FR-057.md#FR-057) / [FR-061](../01_requirements/01_specifications/FR-061.md#FR-061) / [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |
| [UC-229](../01_requirements/02_business_usecases/UC-229.md#UC-229) | 処理エラーを受信 | SCR-030 | [FR-057](../01_requirements/01_specifications/FR-057.md#FR-057) / [FR-061](../01_requirements/01_specifications/FR-061.md#FR-061) / [FR-068](../01_requirements/01_specifications/FR-068.md#FR-068) | — | 兄弟UCの要件を再連結 |

## 4. 未対応要件の分類と対応候補

UC 未対応の要件を性質別に分類する。NFR は UC 直結を要しないため受容、RULE/BR は UC への参照付与、FR は UC 割当を要する。

### 4.1 FR(132件・UC 割当が必要)

操作要件のうち UC 未連結のもの。各 FR を実現する操作 UC へ割り当てる(または未実現なら UC 新設を検討)。下表は判断用の一覧。

| FR | 要件名 | 対応候補 |
|---|---|---|
| [FR-012](../01_requirements/01_specifications/FR-012.md#FR-012) | FR-012: オーナーおよび当該プロジェクトのメンバーは、自分が割り当てられたプロジェ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-013](../01_requirements/01_specifications/FR-013.md#FR-013) | FR-013: オーナーはアカウント新規登録時に自動的に決まり、全プロジェクトに対する全 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-015](../01_requirements/01_specifications/FR-015.md#FR-015) | FR-015: 契約単位の課金情報・支払方法・請求履歴・退会申請・規約再同意・契約設定、 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-016](../01_requirements/01_specifications/FR-016.md#FR-016) | FR-016: メンバーは割り当てられたプロジェクトに属するデータ(FAQ・要対応の質問 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-017](../01_requirements/01_specifications/FR-017.md#FR-017) | FR-017: プロジェクト作成時、オーナーは作成したプロジェクトに対して全権を持つ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-019](../01_requirements/01_specifications/FR-019.md#FR-019) | FR-019: 招待時に指定されたプロジェクト割当は、招待対象者が有効化(氏名入力・パス | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-020](../01_requirements/01_specifications/FR-020.md#FR-020) | FR-020: 招待リンクの再送信は、オーナーまたは当該プロジェクトのメンバーのみが行え | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-021](../01_requirements/01_specifications/FR-021.md#FR-021) | FR-021: 有効化前のメンバーは、招待時に指定されたプロジェクト割当を予約状態として | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-023](../01_requirements/01_specifications/FR-023.md#FR-023) | FR-023: 有効化の完了時には、本人が入力した氏名・初回パスワード・規約同意(利用規 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-024](../01_requirements/01_specifications/FR-024.md#FR-024) | FR-024: アカウント利用者は、現在開いているプロジェクトに割り当てられたメンバーの | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-025](../01_requirements/01_specifications/FR-025.md#FR-025) | FR-025: オーナーおよび当該プロジェクトのメンバーは、自分(オーナー)に紐づくメン | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-026](../01_requirements/01_specifications/FR-026.md#FR-026) | FR-026: 当該プロジェクトのメンバー(オーナーを含む)は、当該プロジェクトのメンバ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-028](../01_requirements/01_specifications/FR-028.md#FR-028) | FR-028: オーナーは、メンバーを別プロジェクトへ追加で割り当てる場合、当該プロジェ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-029](../01_requirements/01_specifications/FR-029.md#FR-029) | FR-029: メンバーの利用終了は「プロジェクトから外す」操作に統合 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-032](../01_requirements/01_specifications/FR-032.md#FR-032) | FR-032: 招待リンクには有効期限を設ける | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-033](../01_requirements/01_specifications/FR-033.md#FR-033) | FR-033: メンバー数に固定の上限を設けず、利用量のしきい値に基づいて上限への接近や | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-034](../01_requirements/01_specifications/FR-034.md#FR-034) | FR-034: メンバー数のしきい値接近・超過時のアラート通知先は、オーナーおよび同一契 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-035](../01_requirements/01_specifications/FR-035.md#FR-035) | FR-035: 契約にメンバーが 1 人も登録されていない状態でも、オーナーが単独で契約 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-038](../01_requirements/01_specifications/FR-038.md#FR-038) | FR-038: プロジェクト作成時には、作成者であるオーナー自身が当該プロジェクトに対し | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-039](../01_requirements/01_specifications/FR-039.md#FR-039) | FR-039: プロジェクト削除時のメンバー割当と関連データの取扱いを次のとおり定める | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-041](../01_requirements/01_specifications/FR-041.md#FR-041) | FR-041: プロジェクトごとに FAQ、質問ログ、未解決質問を分けて管理 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-042](../01_requirements/01_specifications/FR-042.md#FR-042) | FR-042: 許可する Web サイトのドメインを複数設定 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-045](../01_requirements/01_specifications/FR-045.md#FR-045) | FR-045: プロジェクト削除時の関連データ(FAQ、質問ログ、未解決質問)の取扱いを | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-046](../01_requirements/01_specifications/FR-046.md#FR-046) | FR-046: プロジェクト数に固定の上限を設けず、利用状況を監視し急激な増加を検知して | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-048](../01_requirements/01_specifications/FR-048.md#FR-048) | FR-048: FAQ・プロジェクト・メンバーユーザー・お知らせ・契約の削除は管理画面か | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-049](../01_requirements/01_specifications/FR-049.md#FR-049) | FR-049: FAQ に質問と回答を登録 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-050](../01_requirements/01_specifications/FR-050.md#FR-050) | FR-050: FAQ を下書き、公開中、非公開の状態で管理 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-051](../01_requirements/01_specifications/FR-051.md#FR-051) | FR-051: FAQ をカテゴリで整理 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-052](../01_requirements/01_specifications/FR-052.md#FR-052) | FR-052: FAQ の検索、並び替え、絞り込みが | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-054](../01_requirements/01_specifications/FR-054.md#FR-054) | FR-054: FAQ 件数および 1 件あたりの文字数の上限は契約共通の基準とし、極端 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-055](../01_requirements/01_specifications/FR-055.md#FR-055) | FR-055: FAQ 更新時、同時編集による競合を検出 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-056](../01_requirements/01_specifications/FR-056.md#FR-056) | FR-056: FAQ の登録元(未解決質問からの登録か手動登録か)を保持 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-058](../01_requirements/01_specifications/FR-058.md#FR-058) | FR-058: FAQ に根拠がない内容を AI が独自に作成しない | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-059](../01_requirements/01_specifications/FR-059.md#FR-059) | FR-059: AI は FAQ の内容を要約・言い換え・整理できるが、新しい事実・数値 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-060](../01_requirements/01_specifications/FR-060.md#FR-060) | FR-060: 回答に利用した FAQ を記録し、ウィジェット利用者にも参照 FAQ を | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-062](../01_requirements/01_specifications/FR-062.md#FR-062) | FR-062: 回答可否の判定に信頼度・関連度のしきい値をグローバル / 契約別 / プ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-063](../01_requirements/01_specifications/FR-063.md#FR-063) | FR-063: FAQ 登録済みデータでは回答できなかった場合、管理用の問い合わせ ID | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-064](../01_requirements/01_specifications/FR-064.md#FR-064) | FR-064: 処理エラーの場合は、未解決質問登録ではなくエラー表示を行える | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-065](../01_requirements/01_specifications/FR-065.md#FR-065) | FR-065: ウィジェット利用者の入力により AI の動作方針(FAQ 限定回答方針) | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-066](../01_requirements/01_specifications/FR-066.md#FR-066) | FR-066: 利用する AI モデルや基盤の変更時に、動作確認・切替・品質回帰確認・必 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-067](../01_requirements/01_specifications/FR-067.md#FR-067) | FR-067: AI 回答の出力前に検査を行える | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-069](../01_requirements/01_specifications/FR-069.md#FR-069) | FR-069: ウィジェット利用者が「解決しなかった」を選択した場合、未解決質問として登 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-070](../01_requirements/01_specifications/FR-070.md#FR-070) | FR-070: 未解決質問には、質問・未解決理由・発生日時・関連プロジェクト・関連質問ロ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-071](../01_requirements/01_specifications/FR-071.md#FR-071) | FR-071: 未解決質問には問い合わせ ID を付与 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-072](../01_requirements/01_specifications/FR-072.md#FR-072) | FR-072: 未解決質問の状況は「対応中 / 対応済み」の 2 区分とし、保持 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-073](../01_requirements/01_specifications/FR-073.md#FR-073) | FR-073: 状況は未解決質問の登録時に「対応中」と | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-074](../01_requirements/01_specifications/FR-074.md#FR-074) | FR-074: 未解決質問について、現在の状況(対応中 / 対応済み)を一覧画面・詳細画 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-076](../01_requirements/01_specifications/FR-076.md#FR-076) | FR-076: アカウント利用者は未解決質問から FAQ 登録を開始 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-077](../01_requirements/01_specifications/FR-077.md#FR-077) | FR-077: 未解決質問の質問文を、新しい FAQ の質問欄へ初期反映 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-078](../01_requirements/01_specifications/FR-078.md#FR-078) | FR-078: FAQ 回答はアカウント利用者が入力・編集でき、未解決質問の質問文以外を | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-079](../01_requirements/01_specifications/FR-079.md#FR-079) | FR-079: FAQ 登録前に、アカウント利用者が質問・回答・公開状態を確認・編集 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-080](../01_requirements/01_specifications/FR-080.md#FR-080) | FR-080: FAQ の下書き初回保存・公開は、未解決質問の状況を変更しない | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-081](../01_requirements/01_specifications/FR-081.md#FR-081) | FR-081: 未解決質問から登録先 FAQ を参照 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-082](../01_requirements/01_specifications/FR-082.md#FR-082) | FR-082: 処理エラー(通信障害・上流障害・入力不備・認可エラー等)を検知し、ウィジ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-083](../01_requirements/01_specifications/FR-083.md#FR-083) | FR-083: 処理エラーは未解決登録分岐(FAQ なし・信頼度不足・FAQ 矛盾)と区 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-084](../01_requirements/01_specifications/FR-084.md#FR-084) | FR-084: 再試行案内を表示 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-085](../01_requirements/01_specifications/FR-085.md#FR-085) | FR-085: サーバー内部起因のエラーは運用確認できるように記録 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-086](../01_requirements/01_specifications/FR-086.md#FR-086) | FR-086: エラー記録の機密を保護 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-095](../01_requirements/01_specifications/FR-095.md#FR-095) | FR-095: 各機能に対して契約・種別別のレート制限を DDoS / Bot / 暴走 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-099](../01_requirements/01_specifications/FR-099.md#FR-099) | FR-099: 課金プロバイダからの通知(イベント)を受信し、送信元の正当性確認、重複処 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-101](../01_requirements/01_specifications/FR-101.md#FR-101) | FR-101: 要対応の質問の状況を、アカウント利用者向けには「対応中 / 対応済み」で | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-102](../01_requirements/01_specifications/FR-102.md#FR-102) | FR-102: よく聞かれる質問や未解決傾向を確認 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-103](../01_requirements/01_specifications/FR-103.md#FR-103) | FR-103: 期間絞り込みが | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-104](../01_requirements/01_specifications/FR-104.md#FR-104) | FR-104: 通知失敗・バウンス件数を確認 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-105](../01_requirements/01_specifications/FR-105.md#FR-105) | FR-105: 管理範囲とユーザー種別に応じて表示範囲を切り替えられる | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-106](../01_requirements/01_specifications/FR-106.md#FR-106) | FR-106: 利用状況と概要の間を、迷わず行き来 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-107](../01_requirements/01_specifications/FR-107.md#FR-107) | FR-107: 概要画面と利用状況画面は、冒頭に目的を 1 行で宣言 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-108](../01_requirements/01_specifications/FR-108.md#FR-108) | FR-108: 集計時点を明示し、リアルタイム値との誤認を防ぐ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-109](../01_requirements/01_specifications/FR-109.md#FR-109) | FR-109: 主要指標(KPI)カード(質問数 / 未解決数 / 公開 FAQ 件数等 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-110](../01_requirements/01_specifications/FR-110.md#FR-110) | FR-110: 比較値の表記を統一 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-111](../01_requirements/01_specifications/FR-111.md#FR-111) | FR-111: KPI / 一覧 / アラートの各表示要素は、0 件・未集計・集計中・取 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-112](../01_requirements/01_specifications/FR-112.md#FR-112) | FR-112: 利用状況でプロジェクトが 0 件の場合は、複雑なセットアップチェックリス | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-116](../01_requirements/01_specifications/FR-116.md#FR-116) | FR-116: アカウント利用者のアカウント認証関連通知(パスワード再設定等)はオプトア | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-117](../01_requirements/01_specifications/FR-117.md#FR-117) | FR-117: 契約 / プロジェクト単位で送信レート制限・バウンス率・苦情率を監視し、 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-118](../01_requirements/01_specifications/FR-118.md#FR-118) | FR-118: ウィジェット利用者が入力した文字列を、メール件名・送信元情報など外部に露 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-119](../01_requirements/01_specifications/FR-119.md#FR-119) | FR-119: 通知配信状態(送信待ち / 送信済み / 配信済み / 失敗 / バウン | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-124](../01_requirements/01_specifications/FR-124.md#FR-124) | FR-124: バウンス・苦情検知時のメール配信停止リストは全契約横断で共有し、宛先別に | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-126](../01_requirements/01_specifications/FR-126.md#FR-126) | FR-126: アカウント利用者は埋め込みコードを取得し、自社サイトに設置 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-127](../01_requirements/01_specifications/FR-127.md#FR-127) | FR-127: ウィジェットは指定された許可ドメイン上でのみ動作 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-128](../01_requirements/01_specifications/FR-128.md#FR-128) | FR-128: ウィジェットの基本的な見た目をプロジェクトごとに設定 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-129](../01_requirements/01_specifications/FR-129.md#FR-129) | FR-129: ウィジェットはモバイル端末でも利用 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-130](../01_requirements/01_specifications/FR-130.md#FR-130) | FR-130: ウィジェットがアクセシビリティ要件(キーボード操作、スクリーンリーダー、 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-131](../01_requirements/01_specifications/FR-131.md#FR-131) | FR-131: ウィジェットはサポート対象ブラウザで動作 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-132](../01_requirements/01_specifications/FR-132.md#FR-132) | FR-132: ウィジェット配信は高速化(CDN / キャッシュ) | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-133](../01_requirements/01_specifications/FR-133.md#FR-133) | FR-133: ウィジェットは初期状態で丸型のランチャーバッジ(メッセージアイコン)とし | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-134](../01_requirements/01_specifications/FR-134.md#FR-134) | FR-134: チャット UI のヘッダーはウィジェットタイトル、現在状態、チャット U | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-135](../01_requirements/01_specifications/FR-135.md#FR-135) | FR-135: 質問数の月次上限到達または支払方法ゲートにより新規質問を受け付けない場合 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-136](../01_requirements/01_specifications/FR-136.md#FR-136) | FR-136: AI が質問を解決できなかった場合、未解決質問として登録しつつウィジェッ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-140](../01_requirements/01_specifications/FR-140.md#FR-140) | FR-140: 必要なデータ保存リージョン(例:日本国内など)を選択またはサービス側で明 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-141](../01_requirements/01_specifications/FR-141.md#FR-141) | FR-141: 退会猶予期間中は、アカウント利用者の管理画面ログインを許可しつつ新規書込 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-142](../01_requirements/01_specifications/FR-142.md#FR-142) | FR-142: ウィジェットで Cookie 利用について同意取得バナーを表示 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-143](../01_requirements/01_specifications/FR-143.md#FR-143) | FR-143: 通信は暗号化されること(HTTPS) | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-144](../01_requirements/01_specifications/FR-144.md#FR-144) | FR-144: 保存データのうち機密度の高い項目(パスワード、トークン、課金情報等)は暗 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-145](../01_requirements/01_specifications/FR-145.md#FR-145) | FR-145: API・ウィジェットに対してレート制限が | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-146](../01_requirements/01_specifications/FR-146.md#FR-146) | FR-146: ウィジェットの埋め込み元ドメインを検証できること(許可ドメイン以外からの | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-148](../01_requirements/01_specifications/FR-148.md#FR-148) | FR-148: アクセス制御は最小権限の原則に従うこと(オーナー境界によるデータ分離、ユ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-150](../01_requirements/01_specifications/FR-150.md#FR-150) | FR-150: 不審なリクエスト(大量アクセス、未許可ドメイン等)を検知・記録 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-151](../01_requirements/01_specifications/FR-151.md#FR-151) | FR-151: メンバー管理に関する操作を監査ログに記録 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-152](../01_requirements/01_specifications/FR-152.md#FR-152) | FR-152: ウィジェット公開キーのローテーション機能を管理者操作で提供 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-153](../01_requirements/01_specifications/FR-153.md#FR-153) | FR-153: ウィジェット公開キーには有効期限を設けないこと(無期限) | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-154](../01_requirements/01_specifications/FR-154.md#FR-154) | FR-154: 不正利用(大量送信・Bot 疑い・規約違反)の検知と自動ブロックを行う | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-158](../01_requirements/01_specifications/FR-158.md#FR-158) | FR-158: アカウント利用者はお知らせを種別(請求確定 / 運営お知らせ / システ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-159](../01_requirements/01_specifications/FR-159.md#FR-159) | FR-159: 管理画面ヘッダの通知ベルに、未読件数のバッジを表示できること(0 件時は | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-160](../01_requirements/01_specifications/FR-160.md#FR-160) | FR-160: 管理画面ヘッダの通知ベルから、直近 10 件のお知らせをドロップダウンで | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-161](../01_requirements/01_specifications/FR-161.md#FR-161) | FR-161: お知らせはアカウント利用者のみ閲覧可能とし、ウィジェット利用者は閲覧でき | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-162](../01_requirements/01_specifications/FR-162.md#FR-162) | FR-162: 月次請求の確定タイミングで、アカウント利用者の受信箱に請求確定のお知らせ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-163](../01_requirements/01_specifications/FR-163.md#FR-163) | FR-163: お知らせを配信したタイミングで、対象アカウント利用者の受信箱にお知らせを | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-165](../01_requirements/01_specifications/FR-165.md#FR-165) | FR-165: お知らせ受信箱はアカウント利用者ごとに保持し、アカウント無効化・退会時に | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-166](../01_requirements/01_specifications/FR-166.md#FR-166) | FR-166: お知らせの未読件数は管理画面遷移時に取得し、画面滞在中も過大な負荷を生ま | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-167](../01_requirements/01_specifications/FR-167.md#FR-167) | FR-167: 一括既読操作は監査ログに記録できること(操作者・対象件数・実行日時) | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-168](../01_requirements/01_specifications/FR-168.md#FR-168) | FR-168: アカウント利用者が FAQ 検索および質問ログ検索を行える | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-170](../01_requirements/01_specifications/FR-170.md#FR-170) | FR-170: FAQ を CSV 形式(UTF-8)で書き出し(エクスポート) | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-171](../01_requirements/01_specifications/FR-171.md#FR-171) | FR-171: FAQ 編集は同時編集時の衝突を検出 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-172](../01_requirements/01_specifications/FR-172.md#FR-172) | FR-172: FAQ 下書きは自動保存し、未保存の変更がある状態でページ離脱を試みた際 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-175](../01_requirements/01_specifications/FR-175.md#FR-175) | FR-175: 利用者向け管理コンソールは、管理スコープ(契約範囲 / プロジェクト範囲 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-176](../01_requirements/01_specifications/FR-176.md#FR-176) | FR-176: 利用状況でプロジェクトが 0 件の場合は、説明文と「新規プロジェクトを作 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-177](../01_requirements/01_specifications/FR-177.md#FR-177) | FR-177: 契約スコープの参照表示には、影響範囲を示す「利用中のプロジェクト: N」 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-178](../01_requirements/01_specifications/FR-178.md#FR-178) | FR-178: 主ナビゲーションはユーザーの目的語を優先して構成 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-179](../01_requirements/01_specifications/FR-179.md#FR-179) | FR-179: 一覧では名称を主リンク、システム識別子をコピー可能な補助情報として表示 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-180](../01_requirements/01_specifications/FR-180.md#FR-180) | FR-180: 個人設定・契約設定・プロジェクト編集を分離し、設定対象と影響範囲を画面タ | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-181](../01_requirements/01_specifications/FR-181.md#FR-181) | FR-181: 画面見出しは画面名だけを表示し、契約名・プロジェクト名・サイト名を連結し | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-182](../01_requirements/01_specifications/FR-182.md#FR-182) | FR-182: 同一アカウントの複数デバイス同時ログインを可能と | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-183](../01_requirements/01_specifications/FR-183.md#FR-183) | FR-183: オーナーに対する次の操作を不可と | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-184](../01_requirements/01_specifications/FR-184.md#FR-184) | FR-184: アカウント利用者は自分自身への次の操作を行えない | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-185](../01_requirements/01_specifications/FR-185.md#FR-185) | FR-185: メールアドレスは 1 アカウント(`M_USER`)に一意と | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-186](../01_requirements/01_specifications/FR-186.md#FR-186) | FR-186: プロジェクトごとのメンバー割当を「割当しない / メンバー」から選んで行 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-187](../01_requirements/01_specifications/FR-187.md#FR-187) | FR-187: ダッシュボード(自分の通知・お知らせ受信箱)を、オーナーおよびメンバーが | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-188](../01_requirements/01_specifications/FR-188.md#FR-188) | FR-188: プロジェクト割当の追加・剥奪は、アクティブセッションを即時失効させず、次 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-189](../01_requirements/01_specifications/FR-189.md#FR-189) | FR-189: メンバーの最後の有効なプロジェクト割当を解除した場合の挙動を定める | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-191](../01_requirements/01_specifications/FR-191.md#FR-191) | FR-191: 権限外の主ナビゲーションと操作の表示を制御 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-192](../01_requirements/01_specifications/FR-192.md#FR-192) | FR-192: AI 推論のタイムアウト上限は 8 秒 とし、超過時は処理エラーとして扱 | 操作 UC へ割当 / 未実現なら UC 新設 |
| [FR-194](../01_requirements/01_specifications/FR-194.md#FR-194) | FR-194: プロンプトテンプレートの編集を、品質を担保したうえで行える | 操作 UC へ割当 / 未実現なら UC 新設 |

### 4.2 RULE(20件・UC 参照付与)

業務ルールは UC の事前条件・事後条件・例外フローで参照されるべき。下表のルールを関連 UC へ紐付ける。

| RULE | ルール名 | 対応候補 |
|---|---|---|
| [RULE-001](../01_requirements/01_specifications/RULE-001.md#RULE-001) | RULE-001: ログイン失敗ロックアウト | 関連 UC の事前/事後条件で参照 |
| [RULE-002](../01_requirements/01_specifications/RULE-002.md#RULE-002) | RULE-002: 再認証の有効範囲 | 関連 UC の事前/事後条件で参照 |
| [RULE-003](../01_requirements/01_specifications/RULE-003.md#RULE-003) | RULE-003: パスワードポリシー | 関連 UC の事前/事後条件で参照 |
| [RULE-004](../01_requirements/01_specifications/RULE-004.md#RULE-004) | RULE-004: 無操作タイムアウト | 関連 UC の事前/事後条件で参照 |
| [RULE-005](../01_requirements/01_specifications/RULE-005.md#RULE-005) | RULE-005: 絶対タイムアウト | 関連 UC の事前/事後条件で参照 |
| [RULE-006](../01_requirements/01_specifications/RULE-006.md#RULE-006) | RULE-006: 規約改定の予告・同意期限 | 関連 UC の事前/事後条件で参照 |
| [RULE-007](../01_requirements/01_specifications/RULE-007.md#RULE-007) | RULE-007: 招待リンク有効期限 | 関連 UC の事前/事後条件で参照 |
| [RULE-008](../01_requirements/01_specifications/RULE-008.md#RULE-008) | RULE-008: アカウント論理削除の猶予 | 関連 UC の事前/事後条件で参照 |
| [RULE-009](../01_requirements/01_specifications/RULE-009.md#RULE-009) | RULE-009: プロジェクト連絡先確認メール有効期限 | 関連 UC の事前/事後条件で参照 |
| [RULE-010](../01_requirements/01_specifications/RULE-010.md#RULE-010) | RULE-010: FAQ 件数上限 | 関連 UC の事前/事後条件で参照 |
| [RULE-011](../01_requirements/01_specifications/RULE-011.md#RULE-011) | RULE-011: FAQ 文字数上限 | 関連 UC の事前/事後条件で参照 |
| [RULE-012](../01_requirements/01_specifications/RULE-012.md#RULE-012) | RULE-012: AI しきい値既定値 | 関連 UC の事前/事後条件で参照 |
| [RULE-013](../01_requirements/01_specifications/RULE-013.md#RULE-013) | RULE-013: 質問数上限の停止・追加通知 | 関連 UC の事前/事後条件で参照 |
| [RULE-014](../01_requirements/01_specifications/RULE-014.md#RULE-014) | RULE-014: 質問数アラート閾値 | 関連 UC の事前/事後条件で参照 |
| [RULE-015](../01_requirements/01_specifications/RULE-015.md#RULE-015) | RULE-015: 無料枠 | 関連 UC の事前/事後条件で参照 |
| [RULE-016](../01_requirements/01_specifications/RULE-016.md#RULE-016) | RULE-016: 決済失敗の猶予期間 | 関連 UC の事前/事後条件で参照 |
| [RULE-017](../01_requirements/01_specifications/RULE-017.md#RULE-017) | RULE-017: 課金通知の受信履歴保持 | 関連 UC の事前/事後条件で参照 |
| [RULE-018](../01_requirements/01_specifications/RULE-018.md#RULE-018) | RULE-018: 公開キーローテーション猶予 | 関連 UC の事前/事後条件で参照 |
| [RULE-019](../01_requirements/01_specifications/RULE-019.md#RULE-019) | RULE-019: 一括操作の上限 | 関連 UC の事前/事後条件で参照 |
| [RULE-020](../01_requirements/01_specifications/RULE-020.md#RULE-020) | RULE-020: AI 推論タイムアウト | 関連 UC の事前/事後条件で参照 |

### 4.3 BR(6件・個別判断)

業務要件で UC 未連結の残り。下表を個別に確認し UC へ連結する。

| BR | 業務要件名 | 対応候補 |
|---|---|---|
| [BR-006](../01_requirements/01_specifications/BR-006.md#BR-006) | BR-006: 同時ログイン | 関連 UC へ連結 |
| [BR-009](../01_requirements/01_specifications/BR-009.md#BR-009) | BR-009: なりすまし・改ざん対策 | 関連 UC へ連結 |
| [BR-059](../01_requirements/01_specifications/BR-059.md#BR-059) | BR-059: 課金モデル | 関連 UC へ連結 |
| [BR-144](../01_requirements/01_specifications/BR-144.md#BR-144) | BR-144: 利用者向け管理コンソールは契約範囲とプロジェクト範囲に分離し、ヘッダーの | 関連 UC へ連結 |
| [BR-145](../01_requirements/01_specifications/BR-145.md#BR-145) | BR-145: 管理者ユーザーは、未解決質問の状況(対応中 / 対応済み)を一覧および詳 | 関連 UC へ連結 |
| [BR-146](../01_requirements/01_specifications/BR-146.md#BR-146) | BR-146: 未解決質問の「対応済みにする」操作および再オープン操作は詳細画面からの手 | 関連 UC へ連結 |

### 4.4 NFR(79件・受容)

非機能要件は品質特性・制約であり業務 UC へ直接対応しない。トレーサビリティ上は受容し、関連する設計横断仕様(性能/可用性/セキュリティ)で担保する。個別列挙は `01_requirements/01_specifications/index.md` の NFR カタログを参照。

## 5. 付随する構造ギャップ(API/TBL)

要件↔UC 以外に P7 が検出した下流の連結欠落。被覆ギャップ解消に合わせて点検する。

| 区分 | 件数 | 対象 | 所見 |
|---|---|---|---|
| API→UC 無し | 2 | API-031 API-032 | 未使用/連結漏れを要確認 |
| API→EVT 無し | 6 | API-003 API-031 API-032 API-057 API-058 API-059 | 未使用/連結漏れを要確認 |
| TBL→UC 無し | 6 | TBL-008 TBL-011 TBL-016 TBL-028 TBL-029 TBL-031 | 未使用/連結漏れを要確認 |
| TBL→API 無し | 10 | TBL-008 TBL-010 TBL-011 TBL-012 TBL-015 TBL-016 TBL-021 TBL-028 TBL-029 TBL-031 | 未使用/連結漏れを要確認 |

## 6. 推奨対応方針

被覆ギャップは「新規要件創出」より「既存 FR の再連結」が主であるため、次の段階的解消を推奨する。

1. **第1段(機械的再連結・低リスク)**: §3 の候補に従い、未対応 UC 128 件へ同一画面の FR/BR を「対応要件」として転記。これだけで UC→要件 ギャップは大幅縮小し、FR→UC も連動して改善する。
2. **第2段(FR 割当の精査)**: §4.1 の FR 132 件を §3 連結後に再集計し、なお UC 未割当の FR を個別に操作 UC へ割当。実現操作が存在しない FR は UC 新設可否を判断(needs-review)。
3. **第3段(RULE/BR 参照付与)**: §4.2/§4.3 を関連 UC の事前/事後条件へ参照付与。
4. **NFR**: §4.4 のとおり受容(対応不要)。
5. **構造ギャップ**: §5 の API/TBL 連結漏れ・未使用候補を点検し、不要なら削除 Issue、必要なら連結を補完。

> [!NOTE]
> 第1段は決定論的に実施可能(候補が機械導出済み)。第2段以降は設計判断を伴うため、本レポートのレビュー後に着手する。GitHub MCP 復旧後、各段を `[設計再構成][トレーサビリティ]` Issue として起票・消化する。
