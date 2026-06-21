<!-- portal-top -->
[設計ポータル](../../README.md) ／ [要件定義](../index.md) ／ **業務ユースケース**
<!-- /portal-top -->

# 業務ユースケース一覧

> **このページは、操作粒度の業務ユースケース(UC-001〜)を一元的に索引する正本カタログです。** 各 UC は「1 画面イベント = 1 UC」または「1 システム処理 = 1 UC」の操作粒度で、`UC-NNN.md`(1 UC = 1 ファイル・フラット連番)に定義します。

*版数 v1.0 ・ 更新 2026-06-21 ・ 総数 247(画面起点 229 ・ システム起点 18)・ ステータス ドラフト ・ 再構成 P2*

> [!NOTE]
> **採番** 画面順(自然順)×イベント順で UC-001〜UC-229、続いてシステム起点を UC-230〜UC-247 に割り当てます(ゼロ詰め3桁・欠番なし)。旧 ID(`UC-SCR-*-EV*` / `UC-SYSTEM-*`)との対応は `99_management/uc_crosswalk.json` を正本とします。下流の画面・API・テーブル ID(`SCR-*` / `API-*` / `TBL-*`)は現行のままで、後続フェーズ(P3〜P5)でリナンバします。画面イベント ID(`EVT-*`)は P3 で付与します。

## <span id="actors"></span>1. アクター別索引

アクター(役割)が達成する業務目的ごとに、対応する操作粒度 UC(UC-NNN)群へリンクします。業務目的の単位は、旧業務ユースケース(UC-BIZ)の括りを踏襲します。

### <span id="act-account"></span>アカウント利用者(共通)

| 業務目的 | 対応する操作粒度 UC |
|---|---|
| サービスにアクセスする(ログイン・規約同意) | UC-001〜UC-006 ・ UC-019〜UC-027 ・ UC-164〜UC-169 ・ UC-242〜UC-243 |
| アカウント設定と通知を管理する | UC-133〜UC-155 ・ UC-173〜UC-180 ・ UC-196〜UC-198 |

### <span id="act-owner"></span>契約オーナー

| 業務目的 | 対応する操作粒度 UC |
|---|---|
| サービス利用を開始する(契約開設・本人確認) | UC-007〜UC-018 ・ UC-151〜UC-155 ・ UC-194〜UC-195 |
| FAQ 提供基盤を構築する(プロジェクト・ウィジェット設置) | UC-028〜UC-045 ・ UC-096〜UC-114 |
| チームを編成して共同運用する(メンバー招待・権限) | UC-115〜UC-132 ・ UC-181〜UC-193 ・ [UC-236](UC-236.md#UC-236) |
| 利用量と費用を管理する(利用状況・上限・請求) | UC-170〜UC-172 ・ UC-199〜UC-214 ・ [UC-233](UC-233.md#UC-233) ・ [UC-237](UC-237.md#UC-237) ・ UC-239〜UC-241 |
| サービス利用を終了する(退会・データ消去) | UC-156〜UC-163 ・ UC-215〜UC-221 ・ [UC-232](UC-232.md#UC-232) |

### <span id="act-member"></span>プロジェクトメンバー

| 業務目的 | 対応する操作粒度 UC |
|---|---|
| FAQ を整備して公開する(作成・編集・一括・CSV) | UC-062〜UC-095 ・ [UC-230](UC-230.md#UC-230) |
| 問い合わせから FAQ を改善する(未解決→FAQ化) | UC-046〜UC-061 ・ UC-076〜UC-089 |
| ウィジェットの応答を最適化する(設定・しきい値・許可ドメイン) | UC-028〜UC-032 ・ UC-096〜UC-106 ・ UC-202〜UC-207 ・ [UC-245](UC-245.md#UC-245) |

### <span id="act-widget"></span>ウィジェット利用者

| 業務目的 | 対応する操作粒度 UC |
|---|---|
| 疑問をその場で自己解決する | UC-222〜UC-229 ・ [UC-240](UC-240.md#UC-240) |

### <span id="act-ops"></span>運営

| 業務目的 | 対応する操作粒度 UC |
|---|---|
| 利用者へ重要連絡を届ける(お知らせ配信・通知・再送) | UC-136〜UC-150 ・ [UC-231](UC-231.md#UC-231) ・ UC-234〜UC-235 ・ [UC-238](UC-238.md#UC-238) ・ [UC-246](UC-246.md#UC-246) |
| データ保護と健全性を維持する(削除・監査・アクセス制御) | [UC-232](UC-232.md#UC-232) ・ UC-241〜UC-244 ・ [UC-247](UC-247.md#UC-247) |

## <span id="screen"></span>2. 画面起点ユースケース(画面別)

全 30 画面の画面イベントを操作粒度 UC として索引します。各画面の UC は当該画面の `EV-xx` と 1 対 1 で対応します(現行 EV 番号は各 UC の備考・関連欄に注記)。

### <span id="ws-auth"></span>認証・規約フロー

| 画面 | 画面名 | UC 数 | 操作粒度 UC |
|---|---|---|---|
| [SCR-001](../../02_basic_design/01_screens/SCR-001.md#SCR-001) | ログイン | 6 | UC-001〜UC-006 |
| [SCR-002](../../02_basic_design/01_screens/SCR-002.md#SCR-002) | アカウント登録 | 12 | UC-007〜UC-018 |
| [SCR-003](../../02_basic_design/01_screens/SCR-003.md#SCR-003) | パスワード再設定 | 9 | UC-019〜UC-027 |
| [SCR-018](../../02_basic_design/01_screens/SCR-018.md#SCR-018) | メール確認 | 5 | UC-151〜UC-155 |
| [SCR-020](../../02_basic_design/01_screens/SCR-020.md#SCR-020) | 規約再同意割込み | 6 | UC-164〜UC-169 |
| [SCR-023](../../02_basic_design/01_screens/SCR-023.md#SCR-023) | メンバーアカウント有効化 | 13 | UC-181〜UC-193 |
| [SCR-024](../../02_basic_design/01_screens/SCR-024.md#SCR-024) | プロジェクト連絡先メール確認完了 | 2 | UC-194〜UC-195 |

### <span id="ws-owner"></span>契約ワークスペース

| 画面 | 画面名 | UC 数 | 操作粒度 UC |
|---|---|---|---|
| [SCR-004](../../02_basic_design/01_screens/SCR-004.md#SCR-004) | プロジェクト | 5 | UC-028〜UC-032 |
| [SCR-005](../../02_basic_design/01_screens/SCR-005.md#SCR-005) | プロジェクト作成・編集モーダル | 13 | UC-033〜UC-045 |
| [SCR-019](../../02_basic_design/01_screens/SCR-019.md#SCR-019) | 退会申請 | 8 | UC-156〜UC-163 |
| [SCR-021](../../02_basic_design/01_screens/SCR-021.md#SCR-021) | 利用状況 | 3 | UC-170〜UC-172 |
| [SCR-028](../../02_basic_design/01_screens/SCR-028.md#SCR-028) | 請求 | 7 | UC-208〜UC-214 |
| [SCR-029](../../02_basic_design/01_screens/SCR-029.md#SCR-029) | 設定 | 7 | UC-215〜UC-221 |

### <span id="ws-project"></span>プロジェクトワークスペース

| 画面 | 画面名 | UC 数 | 操作粒度 UC |
|---|---|---|---|
| [SCR-006](../../02_basic_design/01_screens/SCR-006.md#SCR-006) | 要対応の質問一覧 | 8 | UC-046〜UC-053 |
| [SCR-007](../../02_basic_design/01_screens/SCR-007.md#SCR-007) | 要対応の質問詳細 | 8 | UC-054〜UC-061 |
| [SCR-008](../../02_basic_design/01_screens/SCR-008.md#SCR-008) | FAQ 一覧 | 14 | UC-062〜UC-075 |
| [SCR-009](../../02_basic_design/01_screens/SCR-009.md#SCR-009) | FAQ 編集 | 14 | UC-076〜UC-089 |
| [SCR-010](../../02_basic_design/01_screens/SCR-010.md#SCR-010) | FAQ CSV インポートモーダル | 6 | UC-090〜UC-095 |
| [SCR-011](../../02_basic_design/01_screens/SCR-011.md#SCR-011) | ウィジェット設定 | 11 | UC-096〜UC-106 |
| [SCR-012](../../02_basic_design/01_screens/SCR-012.md#SCR-012) | 概要(プロジェクト) | 8 | UC-107〜UC-114 |
| [SCR-013](../../02_basic_design/01_screens/SCR-013.md#SCR-013) | メンバー(プロジェクト) | 8 | UC-115〜UC-122 |
| [SCR-014](../../02_basic_design/01_screens/SCR-014.md#SCR-014) | メンバー招待 / 編集モーダル | 10 | UC-123〜UC-132 |
| [SCR-026](../../02_basic_design/01_screens/SCR-026.md#SCR-026) | 利用量と上限(プロジェクト単位) | 3 | UC-199〜UC-201 |
| [SCR-027](../../02_basic_design/01_screens/SCR-027.md#SCR-027) | 質問数上限設定モーダル | 6 | UC-202〜UC-207 |

### <span id="ws-common"></span>共通領域

| 画面 | 画面名 | UC 数 | 操作粒度 UC |
|---|---|---|---|
| [SCR-015](../../02_basic_design/01_screens/SCR-015.md#SCR-015) | 利用規約閲覧 | 3 | UC-133〜UC-135 |
| [SCR-016](../../02_basic_design/01_screens/SCR-016.md#SCR-016) | お知らせ一覧 | 11 | UC-136〜UC-146 |
| [SCR-017](../../02_basic_design/01_screens/SCR-017.md#SCR-017) | お知らせ詳細 | 4 | UC-147〜UC-150 |
| [SCR-022](../../02_basic_design/01_screens/SCR-022.md#SCR-022) | 個人設定 | 8 | UC-173〜UC-180 |
| [SCR-025](../../02_basic_design/01_screens/SCR-025.md#SCR-025) | プライバシーポリシー閲覧 | 3 | UC-196〜UC-198 |

### <span id="ws-widget"></span>ウィジェット

| 画面 | 画面名 | UC 数 | 操作粒度 UC |
|---|---|---|---|
| [SCR-030](../../02_basic_design/01_screens/SCR-030.md#SCR-030) | エンドユーザー向け FAQ ウィジェット | 8 | UC-222〜UC-229 |

## <span id="system"></span>3. システム起点ユースケース

画面操作を伴わず、定期・イベント駆動・非同期・Webhook 受信で実行する処理です。1 処理 = 1 UC で索引します。

| UC | 名称 | トリガー種別 | 関連(機能グループ) |
|---|---|---|---|
| [UC-230](UC-230.md#UC-230) | 非同期 CSV インポートジョブ | 非同期ジョブ | FR17 インポート・エクスポート |
| [UC-231](UC-231.md#UC-231) | Resend Webhook 受信(配信状態更新) | Webhook 受信 | FR11 通知 |
| [UC-232](UC-232.md#UC-232) | 90 日物理削除バッチ | 定期バッチ | FR13 プライバシー・データ管理 |
| [UC-233](UC-233.md#UC-233) | 月次請求確定バッチ | 定期バッチ(月次) | FR09 利用量・課金 |
| [UC-234](UC-234.md#UC-234) | 運営お知らせ配信 | スケジュール/イベント | FR15 お知らせ |
| [UC-235](UC-235.md#UC-235) | 運用イベントのシステム通知自動生成 | イベントドリブン | FR11 通知 |
| [UC-236](UC-236.md#UC-236) | メンバー割当変更通知 | イベントドリブン | FR02 ユーザー管理 |
| [UC-237](UC-237.md#UC-237) | 質問数上限アラート通知 | イベントドリブン | FR09 利用量・課金 |
| [UC-238](UC-238.md#UC-238) | 通知再送 | 定期バッチ(失敗検出) | FR11 通知 |
| [UC-239](UC-239.md#UC-239) | 利用量リアルタイム集計・UI 反映 | 同期内部処理 | FR09 / FR10 |
| [UC-240](UC-240.md#UC-240) | 上限到達ウィジェット受付停止 | 同期内部処理 | FR09 / FR12 |
| [UC-241](UC-241.md#UC-241) | 決済失敗→猶予→サスペンション | イベント+定期 | FR09 利用量・課金 |
| [UC-242](UC-242.md#UC-242) | セッション失効・再認証 | 定期/検証時 | FR01 / FR14 |
| [UC-243](UC-243.md#UC-243) | ログイン失敗ロックアウト・解除 | イベント+時間 | FR14 セキュリティ |
| [UC-244](UC-244.md#UC-244) | 契約停止時セッション一斉無効化 | イベント(状態遷移) | FR01 / FR14 |
| [UC-245](UC-245.md#UC-245) | AI しきい値変更の伝播・フォールバック | イベント | FR20 AI 推論動作 |
| [UC-246](UC-246.md#UC-246) | 受信箱の重複集約 | 定期/集約 | FR11 / FR15 |
| [UC-247](UC-247.md#UC-247) | 監査ログ整合性検証(日次) | 定期バッチ(日次) | NFR(監査) |

## <span id="trace"></span>4. 要件トレーサビリティ(機能グループ別)

各機能要件グループ(FR01〜FR21)が、少なくとも 1 つ以上の操作粒度 UC に対応していることを示します。UC は新フラット ID(UC-NNN)で表記します。

| 機能グループ | 対応する画面起点 UC | 対応するシステム起点 UC |
|---|---|---|
| FR01 アカウント管理 | UC-001〜UC-027 ・ UC-151〜UC-163 ・ UC-215〜UC-221 | [UC-232](UC-232.md#UC-232) ・ [UC-242](UC-242.md#UC-242) ・ [UC-244](UC-244.md#UC-244) |
| FR02 ユーザー管理 | UC-115〜UC-132 ・ UC-181〜UC-193 | [UC-236](UC-236.md#UC-236) |
| FR03 プロジェクト管理 | UC-028〜UC-045 | — |
| FR04 FAQ 管理 | UC-062〜UC-089 | — |
| FR05 AI 回答 | UC-222〜UC-229 | [UC-245](UC-245.md#UC-245) |
| FR06 未解決質問登録 | UC-046〜UC-061 ・ UC-222〜UC-229 | — |
| FR07 未解決質問から FAQ 登録 | UC-054〜UC-061 ・ UC-076〜UC-089 | — |
| FR08 処理エラー | — | [UC-238](UC-238.md#UC-238) |
| FR09 利用量・課金 | UC-170〜UC-172 ・ UC-199〜UC-214 | [UC-233](UC-233.md#UC-233) ・ [UC-237](UC-237.md#UC-237) ・ [UC-239](UC-239.md#UC-239) ・ [UC-240](UC-240.md#UC-240) ・ [UC-241](UC-241.md#UC-241) |
| FR10 管理ダッシュボード | UC-107〜UC-114 ・ UC-170〜UC-172 | [UC-239](UC-239.md#UC-239) |
| FR11 通知 | UC-136〜UC-150 | [UC-231](UC-231.md#UC-231) ・ [UC-235](UC-235.md#UC-235) ・ [UC-236](UC-236.md#UC-236) ・ [UC-238](UC-238.md#UC-238) ・ [UC-246](UC-246.md#UC-246) |
| FR12 ウィジェット | UC-096〜UC-106 ・ UC-222〜UC-229 | [UC-240](UC-240.md#UC-240) |
| FR13 プライバシー・データ管理 | UC-156〜UC-163 ・ UC-173〜UC-180 ・ UC-196〜UC-198 | [UC-232](UC-232.md#UC-232) |
| FR14 セキュリティ | UC-001〜UC-006 | [UC-242](UC-242.md#UC-242) ・ [UC-243](UC-243.md#UC-243) ・ [UC-244](UC-244.md#UC-244) |
| FR15 お知らせ | UC-133〜UC-150 ・ UC-196〜UC-198 | [UC-234](UC-234.md#UC-234) ・ [UC-246](UC-246.md#UC-246) |
| FR16 検索エンジン・全文検索 | UC-046〜UC-053 ・ UC-062〜UC-075 | — |
| FR17 インポート・エクスポート | UC-062〜UC-075 ・ UC-090〜UC-095 | [UC-230](UC-230.md#UC-230) |
| FR18 UX 細部・データ運用 | UC-062〜UC-089 | — |
| FR19 アクセス制御細部 | UC-096〜UC-106 ・ UC-123〜UC-132 ・ UC-199〜UC-201 | [UC-244](UC-244.md#UC-244) |
| FR20 AI 推論動作 | UC-222〜UC-229 | [UC-245](UC-245.md#UC-245) |
| FR21 画面・機能要件一覧 | 全 30 画面の UC 群(本 §2 ・ UC-001〜UC-229) | — |

> [!NOTE]
> **監査・整合性** 監査ログの整合性検証(NFR 監査要件)は [UC-247](UC-247.md#UC-247)(旧 UC-SYSTEM-018)が担います。各操作の監査記録は対応する画面起点・システム起点 UC の事後条件に記載します。

## <span id="req-origin"></span>5. 要件起点ユースケース(第2段新設)

P7 後続(第2段)で、画面・システム起点ユースケースに未連結だった機能要件(FR)を起点に、業務ユースケース UC-248〜UC-304 を新設しました。各 UC は1 FR(および関連 BR)を起点とする操作粒度の業務ユースケースで、機械支援による生成のため要レビューです。下表は機能グループ別に対応 FR と新設 UC を索引します。

| 機能グループ | 対応FR | UC |
|---|---|---|
| ユーザー管理(オーナー + メンバー) | [FR-015](../01_specifications/FR-015.md#FR-015) ・ [FR-020](../01_specifications/FR-020.md#FR-020) ・ [FR-028](../01_specifications/FR-028.md#FR-028) ・ [FR-033](../01_specifications/FR-033.md#FR-033) ・ [FR-034](../01_specifications/FR-034.md#FR-034) | [UC-248](UC-248.md#UC-248) ・ [UC-249](UC-249.md#UC-249) ・ [UC-250](UC-250.md#UC-250) ・ [UC-251](UC-251.md#UC-251) ・ [UC-252](UC-252.md#UC-252) |
| プロジェクト管理 | [FR-038](../01_specifications/FR-038.md#FR-038) ・ [FR-039](../01_specifications/FR-039.md#FR-039) ・ [FR-041](../01_specifications/FR-041.md#FR-041) ・ [FR-042](../01_specifications/FR-042.md#FR-042) ・ [FR-045](../01_specifications/FR-045.md#FR-045) ・ [FR-046](../01_specifications/FR-046.md#FR-046) | [UC-253](UC-253.md#UC-253) ・ [UC-254](UC-254.md#UC-254) ・ [UC-255](UC-255.md#UC-255) ・ [UC-256](UC-256.md#UC-256) ・ [UC-257](UC-257.md#UC-257) ・ [UC-258](UC-258.md#UC-258) |
| AI 回答 | [FR-060](../01_specifications/FR-060.md#FR-060) ・ [FR-062](../01_specifications/FR-062.md#FR-062) ・ [FR-063](../01_specifications/FR-063.md#FR-063) ・ [FR-064](../01_specifications/FR-064.md#FR-064) | [UC-259](UC-259.md#UC-259) ・ [UC-260](UC-260.md#UC-260) ・ [UC-261](UC-261.md#UC-261) ・ [UC-262](UC-262.md#UC-262) |
| 未解決質問登録 | [FR-070](../01_specifications/FR-070.md#FR-070) | [UC-263](UC-263.md#UC-263) |
| 未解決質問から FAQ 登録 | [FR-076](../01_specifications/FR-076.md#FR-076) ・ [FR-077](../01_specifications/FR-077.md#FR-077) ・ [FR-078](../01_specifications/FR-078.md#FR-078) ・ [FR-079](../01_specifications/FR-079.md#FR-079) ・ [FR-080](../01_specifications/FR-080.md#FR-080) ・ [FR-081](../01_specifications/FR-081.md#FR-081) | [UC-264](UC-264.md#UC-264) ・ [UC-265](UC-265.md#UC-265) ・ [UC-266](UC-266.md#UC-266) ・ [UC-267](UC-267.md#UC-267) ・ [UC-268](UC-268.md#UC-268) ・ [UC-269](UC-269.md#UC-269) |
| 利用量 | [FR-095](../01_specifications/FR-095.md#FR-095) ・ [FR-099](../01_specifications/FR-099.md#FR-099) | [UC-270](UC-270.md#UC-270) ・ [UC-271](UC-271.md#UC-271) |
| 管理ダッシュボード | [FR-101](../01_specifications/FR-101.md#FR-101) ・ [FR-102](../01_specifications/FR-102.md#FR-102) ・ [FR-103](../01_specifications/FR-103.md#FR-103) ・ [FR-104](../01_specifications/FR-104.md#FR-104) ・ [FR-105](../01_specifications/FR-105.md#FR-105) ・ [FR-106](../01_specifications/FR-106.md#FR-106) ・ [FR-107](../01_specifications/FR-107.md#FR-107) ・ [FR-108](../01_specifications/FR-108.md#FR-108) ・ [FR-110](../01_specifications/FR-110.md#FR-110) ・ [FR-111](../01_specifications/FR-111.md#FR-111) ・ [FR-112](../01_specifications/FR-112.md#FR-112) | [UC-272](UC-272.md#UC-272) ・ [UC-273](UC-273.md#UC-273) ・ [UC-274](UC-274.md#UC-274) ・ [UC-275](UC-275.md#UC-275) ・ [UC-276](UC-276.md#UC-276) ・ [UC-277](UC-277.md#UC-277) ・ [UC-278](UC-278.md#UC-278) ・ [UC-279](UC-279.md#UC-279) ・ [UC-280](UC-280.md#UC-280) ・ [UC-281](UC-281.md#UC-281) ・ [UC-282](UC-282.md#UC-282) |
| 通知 | [FR-116](../01_specifications/FR-116.md#FR-116) ・ [FR-117](../01_specifications/FR-117.md#FR-117) ・ [FR-118](../01_specifications/FR-118.md#FR-118) ・ [FR-119](../01_specifications/FR-119.md#FR-119) | [UC-283](UC-283.md#UC-283) ・ [UC-284](UC-284.md#UC-284) ・ [UC-285](UC-285.md#UC-285) ・ [UC-286](UC-286.md#UC-286) |
| ウィジェット | [FR-126](../01_specifications/FR-126.md#FR-126) ・ [FR-127](../01_specifications/FR-127.md#FR-127) ・ [FR-128](../01_specifications/FR-128.md#FR-128) ・ [FR-129](../01_specifications/FR-129.md#FR-129) ・ [FR-130](../01_specifications/FR-130.md#FR-130) ・ [FR-131](../01_specifications/FR-131.md#FR-131) ・ [FR-132](../01_specifications/FR-132.md#FR-132) ・ [FR-133](../01_specifications/FR-133.md#FR-133) ・ [FR-134](../01_specifications/FR-134.md#FR-134) ・ [FR-135](../01_specifications/FR-135.md#FR-135) ・ [FR-136](../01_specifications/FR-136.md#FR-136) | [UC-287](UC-287.md#UC-287) ・ [UC-288](UC-288.md#UC-288) ・ [UC-289](UC-289.md#UC-289) ・ [UC-290](UC-290.md#UC-290) ・ [UC-291](UC-291.md#UC-291) ・ [UC-292](UC-292.md#UC-292) ・ [UC-293](UC-293.md#UC-293) ・ [UC-294](UC-294.md#UC-294) ・ [UC-295](UC-295.md#UC-295) ・ [UC-296](UC-296.md#UC-296) ・ [UC-297](UC-297.md#UC-297) |
| お知らせ | [FR-159](../01_specifications/FR-159.md#FR-159) ・ [FR-160](../01_specifications/FR-160.md#FR-160) ・ [FR-161](../01_specifications/FR-161.md#FR-161) ・ [FR-165](../01_specifications/FR-165.md#FR-165) ・ [FR-166](../01_specifications/FR-166.md#FR-166) ・ [FR-167](../01_specifications/FR-167.md#FR-167) | [UC-298](UC-298.md#UC-298) ・ [UC-299](UC-299.md#UC-299) ・ [UC-300](UC-300.md#UC-300) ・ [UC-301](UC-301.md#UC-301) ・ [UC-302](UC-302.md#UC-302) ・ [UC-303](UC-303.md#UC-303) |
| 検索 | [FR-168](../01_specifications/FR-168.md#FR-168) | [UC-304](UC-304.md#UC-304) |

---

<!-- portal-bottom -->
[要件定義](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
