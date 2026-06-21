# FAQ AI ウィジェット SaaS / メインシステム 設計ポータル(Markdown 版)

本リポジトリは設計ドキュメントを **Markdown** で管理する。Markdown を正本とし、本書がポータルのトップ(全文書索引)である。

- 図は ` ```mermaid ` で保持。相互参照は `<span id="…">` アンカー。各ページにパンくず・戻り導線を付与。
- 読み順: 要件定義 ＞ 業務ユースケース ＞ 画面設計 ＞ 画面イベント ＞ API設計 ＞ DB設計 ＞ シーケンス ＞ 権限/エラー/メッセージ。

## 要件定義

- [概要・一覧](01_requirements/index.md)
- [FR01: アカウント管理](01_requirements/FR01.md)
- [FR02: ユーザー管理(オーナー + メンバー)](01_requirements/FR02.md)
- [FR03: プロジェクト管理](01_requirements/FR03.md)
- [FR04: FAQ 管理](01_requirements/FR04.md)
- [FR05: AI 回答](01_requirements/FR05.md)
- [FR06: 未解決質問登録](01_requirements/FR06.md)
- [FR07: 未解決質問から FAQ 登録](01_requirements/FR07.md)
- [FR08: 処理エラー](01_requirements/FR08.md)
- [FR09: 利用量・課金](01_requirements/FR09.md)
- [FR10: 管理ダッシュボード](01_requirements/FR10.md)
- [FR11: 通知](01_requirements/FR11.md)
- [FR12: ウィジェット](01_requirements/FR12.md)
- [FR13: プライバシー・データ管理](01_requirements/FR13.md)
- [FR14: セキュリティ](01_requirements/FR14.md)
- [FR15: お知らせ](01_requirements/FR15.md)
- [FR16: 検索・全文検索](01_requirements/FR16.md)
- [FR17: インポート・エクスポート](01_requirements/FR17.md)
- [FR18: UX 細部・データ運用](01_requirements/FR18.md)
- [FR19: アクセス制御細部](01_requirements/FR19.md)
- [FR20: AI 推論動作](01_requirements/FR20.md)
- [FR21: 画面・機能要件一覧](01_requirements/FR21.md)

### 要件仕様

- [一覧](01_requirements/01_specifications/index.md)

### 業務ユースケース

- [一覧](01_requirements/02_business_usecases/index.md)
- [UC-BIZ-001: サービスにアクセスする(ログイン・規約同意)](01_requirements/02_business_usecases/UC-BIZ-001.md)
- [UC-BIZ-002: アカウント設定と通知を管理する](01_requirements/02_business_usecases/UC-BIZ-002.md)
- [UC-BIZ-003: サービス利用を開始する(契約開設・本人確認)](01_requirements/02_business_usecases/UC-BIZ-003.md)
- [UC-BIZ-004: FAQ 提供基盤を構築する(プロジェクト・ウィジェット設置)](01_requirements/02_business_usecases/UC-BIZ-004.md)
- [UC-BIZ-005: チームを編成して共同運用する(メンバー招待・権限)](01_requirements/02_business_usecases/UC-BIZ-005.md)
- [UC-BIZ-006: 利用量と費用を管理する(利用状況・上限・請求)](01_requirements/02_business_usecases/UC-BIZ-006.md)
- [UC-BIZ-007: サービス利用を終了する(退会・データ消去)](01_requirements/02_business_usecases/UC-BIZ-007.md)
- [UC-BIZ-008: FAQ を整備して公開する(作成・編集・一括・CSV)](01_requirements/02_business_usecases/UC-BIZ-008.md)
- [UC-BIZ-009: 問い合わせから FAQ を改善する(未解決→FAQ化)](01_requirements/02_business_usecases/UC-BIZ-009.md)
- [UC-BIZ-010: ウィジェットの応答を最適化する(設定・しきい値・許可ドメイン)](01_requirements/02_business_usecases/UC-BIZ-010.md)
- [UC-BIZ-011: 疑問をその場で自己解決する](01_requirements/02_business_usecases/UC-BIZ-011.md)
- [UC-BIZ-012: 利用者へ重要連絡を届ける(お知らせ配信・通知・再送)](01_requirements/02_business_usecases/UC-BIZ-012.md)
- [UC-BIZ-013: データ保護と健全性を維持する(削除・監査・アクセス制御)](01_requirements/02_business_usecases/UC-BIZ-013.md)
- [UC-SCR-001: ログイン ユースケース](01_requirements/02_business_usecases/UC-SCR-001.md)
- [UC-SCR-002: アカウント登録 ユースケース](01_requirements/02_business_usecases/UC-SCR-002.md)
- [UC-SCR-003: パスワード再設定 ユースケース](01_requirements/02_business_usecases/UC-SCR-003.md)
- [UC-SCR-004: プロジェクト ユースケース](01_requirements/02_business_usecases/UC-SCR-004.md)
- [UC-SCR-004-001: プロジェクト作成・編集モーダル ユースケース](01_requirements/02_business_usecases/UC-SCR-004-001.md)
- [UC-SCR-005: 要対応の質問一覧 ユースケース](01_requirements/02_business_usecases/UC-SCR-005.md)
- [UC-SCR-005-001: 要対応の質問詳細 ユースケース](01_requirements/02_business_usecases/UC-SCR-005-001.md)
- [UC-SCR-006: FAQ 一覧 ユースケース](01_requirements/02_business_usecases/UC-SCR-006.md)
- [UC-SCR-006-001: FAQ 編集 ユースケース](01_requirements/02_business_usecases/UC-SCR-006-001.md)
- [UC-SCR-006-002: FAQ CSV インポートモーダル ユースケース](01_requirements/02_business_usecases/UC-SCR-006-002.md)
- [UC-SCR-007: ウィジェット設定 ユースケース](01_requirements/02_business_usecases/UC-SCR-007.md)
- [UC-SCR-008: 概要(プロジェクト) ユースケース](01_requirements/02_business_usecases/UC-SCR-008.md)
- [UC-SCR-009: メンバー(プロジェクト) ユースケース](01_requirements/02_business_usecases/UC-SCR-009.md)
- [UC-SCR-009-001: メンバー招待 / 編集モーダル ユースケース](01_requirements/02_business_usecases/UC-SCR-009-001.md)
- [UC-SCR-010: 利用規約閲覧 ユースケース](01_requirements/02_business_usecases/UC-SCR-010.md)
- [UC-SCR-011: お知らせ一覧 ユースケース](01_requirements/02_business_usecases/UC-SCR-011.md)
- [UC-SCR-012: お知らせ詳細 ユースケース](01_requirements/02_business_usecases/UC-SCR-012.md)
- [UC-SCR-013: メール確認 ユースケース](01_requirements/02_business_usecases/UC-SCR-013.md)
- [UC-SCR-014: 退会申請 ユースケース](01_requirements/02_business_usecases/UC-SCR-014.md)
- [UC-SCR-015: 規約再同意割込み ユースケース](01_requirements/02_business_usecases/UC-SCR-015.md)
- [UC-SCR-016: 利用状況 ユースケース](01_requirements/02_business_usecases/UC-SCR-016.md)
- [UC-SCR-017: 個人設定 ユースケース](01_requirements/02_business_usecases/UC-SCR-017.md)
- [UC-SCR-018: メンバーアカウント有効化 ユースケース](01_requirements/02_business_usecases/UC-SCR-018.md)
- [UC-SCR-019: プロジェクト連絡先メール確認完了 ユースケース](01_requirements/02_business_usecases/UC-SCR-019.md)
- [UC-SCR-020: プライバシーポリシー閲覧 ユースケース](01_requirements/02_business_usecases/UC-SCR-020.md)
- [UC-SCR-021: 利用量と上限(プロジェクト単位) ユースケース](01_requirements/02_business_usecases/UC-SCR-021.md)
- [UC-SCR-021-001: 質問数上限設定モーダル ユースケース](01_requirements/02_business_usecases/UC-SCR-021-001.md)
- [UC-SCR-022: 請求 ユースケース](01_requirements/02_business_usecases/UC-SCR-022.md)
- [UC-SCR-023: 設定 ユースケース](01_requirements/02_business_usecases/UC-SCR-023.md)
- [UC-SCR-WIDGET: エンドユーザー向け FAQ ウィジェット ユースケース](01_requirements/02_business_usecases/UC-SCR-WIDGET.md)
- [UC-SYSTEM-001: 非同期 CSV インポートジョブ](01_requirements/02_business_usecases/UC-SYSTEM-001.md)
- [UC-SYSTEM-002: Resend Webhook 受信(配信状態更新)](01_requirements/02_business_usecases/UC-SYSTEM-002.md)
- [UC-SYSTEM-003: 90 日物理削除バッチ](01_requirements/02_business_usecases/UC-SYSTEM-003.md)
- [UC-SYSTEM-004: 月次請求確定バッチ](01_requirements/02_business_usecases/UC-SYSTEM-004.md)
- [UC-SYSTEM-005: 運営お知らせ配信](01_requirements/02_business_usecases/UC-SYSTEM-005.md)
- [UC-SYSTEM-006: 運用イベントのシステム通知自動生成](01_requirements/02_business_usecases/UC-SYSTEM-006.md)
- [UC-SYSTEM-007: メンバー割当変更通知](01_requirements/02_business_usecases/UC-SYSTEM-007.md)
- [UC-SYSTEM-008: 質問数上限アラート通知](01_requirements/02_business_usecases/UC-SYSTEM-008.md)
- [UC-SYSTEM-009: 通知再送](01_requirements/02_business_usecases/UC-SYSTEM-009.md)
- [UC-SYSTEM-010: 利用量リアルタイム集計・UI 反映](01_requirements/02_business_usecases/UC-SYSTEM-010.md)
- [UC-SYSTEM-011: 上限到達ウィジェット受付停止](01_requirements/02_business_usecases/UC-SYSTEM-011.md)
- [UC-SYSTEM-012: 決済失敗→猶予→サスペンション](01_requirements/02_business_usecases/UC-SYSTEM-012.md)
- [UC-SYSTEM-013: セッション失効・再認証](01_requirements/02_business_usecases/UC-SYSTEM-013.md)
- [UC-SYSTEM-014: ログイン失敗ロックアウト・解除](01_requirements/02_business_usecases/UC-SYSTEM-014.md)
- [UC-SYSTEM-015: 契約停止時セッション一斉無効化](01_requirements/02_business_usecases/UC-SYSTEM-015.md)
- [UC-SYSTEM-016: AI しきい値変更の伝播・フォールバック](01_requirements/02_business_usecases/UC-SYSTEM-016.md)
- [UC-SYSTEM-017: 受信箱の重複集約](01_requirements/02_business_usecases/UC-SYSTEM-017.md)
- [UC-SYSTEM-018: 監査ログ整合性検証(日次)](01_requirements/02_business_usecases/UC-SYSTEM-018.md)

## 基本設計

- [概要・一覧](02_basic_design/index.md)
- [課金・請求設計書](02_basic_design/05_billing-design.md)
- [メール設計書](02_basic_design/06_mail-design.md)
- [認証・認可設計書](02_basic_design/07_auth-design.md)

### 画面設計

- [一覧](02_basic_design/01_screens/index.md)
- [SCR-001 ログイン](02_basic_design/01_screens/SCR-001.md)
- [SCR-002 アカウント登録](02_basic_design/01_screens/SCR-002.md)
- [SCR-003 パスワード再設定](02_basic_design/01_screens/SCR-003.md)
- [SCR-004 プロジェクト](02_basic_design/01_screens/SCR-004.md)
- [SCR-004-001 プロジェクト作成・編集モーダル](02_basic_design/01_screens/SCR-004-001.md)
- [SCR-005 要対応の質問一覧](02_basic_design/01_screens/SCR-005.md)
- [SCR-005-001 要対応の質問詳細](02_basic_design/01_screens/SCR-005-001.md)
- [SCR-006 FAQ 一覧](02_basic_design/01_screens/SCR-006.md)
- [SCR-006-001 FAQ 編集](02_basic_design/01_screens/SCR-006-001.md)
- [SCR-006-002 FAQ CSV インポートモーダル](02_basic_design/01_screens/SCR-006-002.md)
- [SCR-007 ウィジェット設定](02_basic_design/01_screens/SCR-007.md)
- [SCR-008 概要(プロジェクト)](02_basic_design/01_screens/SCR-008.md)
- [SCR-009 メンバー(プロジェクト)](02_basic_design/01_screens/SCR-009.md)
- [SCR-009-001 メンバー招待 / 編集モーダル(プロジェクト単位)](02_basic_design/01_screens/SCR-009-001.md)
- [SCR-010 利用規約閲覧](02_basic_design/01_screens/SCR-010.md)
- [SCR-011 お知らせ一覧](02_basic_design/01_screens/SCR-011.md)
- [SCR-012 お知らせ詳細](02_basic_design/01_screens/SCR-012.md)
- [SCR-013 メール確認](02_basic_design/01_screens/SCR-013.md)
- [SCR-014 退会申請](02_basic_design/01_screens/SCR-014.md)
- [SCR-015 規約再同意割込み](02_basic_design/01_screens/SCR-015.md)
- [SCR-016 利用状況](02_basic_design/01_screens/SCR-016.md)
- [SCR-017 個人設定](02_basic_design/01_screens/SCR-017.md)
- [SCR-018 メンバーアカウント有効化](02_basic_design/01_screens/SCR-018.md)
- [SCR-019 プロジェクト連絡先メール確認完了](02_basic_design/01_screens/SCR-019.md)
- [SCR-020 プライバシーポリシー閲覧](02_basic_design/01_screens/SCR-020.md)
- [SCR-021 利用量と上限(プロジェクト単位)](02_basic_design/01_screens/SCR-021.md)
- [SCR-021-001 質問数上限設定モーダル](02_basic_design/01_screens/SCR-021-001.md)
- [SCR-022 請求](02_basic_design/01_screens/SCR-022.md)
- [SCR-023 設定](02_basic_design/01_screens/SCR-023.md)
- [WIDGET エンドユーザー向け FAQ ウィジェット](02_basic_design/01_screens/SCR-WIDGET.md)

### 画面イベント設計

- [一覧](02_basic_design/02_screen_events/index.md)

### API設計

- [一覧](02_basic_design/03_apis/index.md)
- [AI 推論 IF](02_basic_design/03_apis/API-ai.md)
- [認証 API](02_basic_design/03_apis/API-auth.md)
- [利用量・課金 API](02_basic_design/03_apis/API-billing.md)
- [API 共通仕様](02_basic_design/03_apis/API-common.md)
- [ダッシュボード API](02_basic_design/03_apis/API-dashboard.md)
- [FAQ 管理 API](02_basic_design/03_apis/API-faq.md)
- [お知らせ受信箱 API](02_basic_design/03_apis/API-inbox.md)
- [未解決質問 API](02_basic_design/03_apis/API-inquiry.md)
- [メール配信 IF](02_basic_design/03_apis/API-mail.md)
- [利用者(メンバー)API](02_basic_design/03_apis/API-member.md)
- [プロジェクト管理 API](02_basic_design/03_apis/API-project.md)
- [規約・退会 API](02_basic_design/03_apis/API-terms.md)
- [外部 Webhook](02_basic_design/03_apis/API-webhook.md)
- [ウィジェット API](02_basic_design/03_apis/API-widget.md)

### DB設計

- [一覧](02_basic_design/04_database/index.md)
- [TBL-H-001 H_QUESTION_LOGS](02_basic_design/04_database/TBL-H-001.md)
- [TBL-H-002 H_NOTIF_LOGS](02_basic_design/04_database/TBL-H-002.md)
- [TBL-H-003 H_AUDIT_LOGS](02_basic_design/04_database/TBL-H-003.md)
- [TBL-H-004 H_ERROR_LOGS](02_basic_design/04_database/TBL-H-004.md)
- [TBL-H-005 H_INQUIRY_FAQ](02_basic_design/04_database/TBL-H-005.md)
- [M_USER](02_basic_design/04_database/TBL-M-001.md)
- [M_CONTRACT](02_basic_design/04_database/TBL-M-002.md)
- [M_PRJ_USERS](02_basic_design/04_database/TBL-M-003.md)
- [M_PROJECTS](02_basic_design/04_database/TBL-M-004.md)
- [TBL-M-005 M_ALLOWED_DOMAINS](02_basic_design/04_database/TBL-M-005.md)
- [TBL-M-006 M_FAQS](02_basic_design/04_database/TBL-M-006.md)
- [TBL-M-007 M_EMAIL_SUPPRESS](02_basic_design/04_database/TBL-M-007.md)
- [TBL-M-008 M_OWNER_QUOTA_OVR](02_basic_design/04_database/TBL-M-008.md)
- [TBL-M-009 M_PRJ_QUOTA_LIMITS](02_basic_design/04_database/TBL-M-009.md)
- [TBL-M-010 M_SERVICE_ANNOUNCE](02_basic_design/04_database/TBL-M-010.md)
- [TBL-M-011 M_ANNOUNCE_AUD](02_basic_design/04_database/TBL-M-011.md)
- [TBL-M-012 M_TERMS_VER](02_basic_design/04_database/TBL-M-012.md)
- [TBL-T-001 T_SESSIONS](02_basic_design/04_database/TBL-T-001.md)
- [TBL-T-002 T_ACCESS_TOKENS](02_basic_design/04_database/TBL-T-002.md)
- [TBL-T-003 T_PRJ_LEGACY_KEYS](02_basic_design/04_database/TBL-T-003.md)
- [TBL-T-004 T_QLOG_FAQ_REFS](02_basic_design/04_database/TBL-T-004.md)
- [TBL-T-005 T_INQUIRIES](02_basic_design/04_database/TBL-T-005.md)
- [TBL-T-006 T_BILL_SUBS](02_basic_design/04_database/TBL-T-006.md)
- [TBL-T-007 T_BILL_INVOICES](02_basic_design/04_database/TBL-T-007.md)
- [TBL-T-008 T_USAGE_METER](02_basic_design/04_database/TBL-T-008.md)
- [TBL-T-009 T_ANNOUNCE_RCPT](02_basic_design/04_database/TBL-T-009.md)
- [TBL-T-010 T_INBOX_MSG](02_basic_design/04_database/TBL-T-010.md)
- [TBL-T-011 T_WITHDRAW_REQ](02_basic_design/04_database/TBL-T-011.md)
- [TBL-T-012 T_TERMS_AGREE](02_basic_design/04_database/TBL-T-012.md)
- [TBL-TP-001 TP_FAQ_FTS](02_basic_design/04_database/TBL-TP-001.md)
- [TBL-TP-002 TP_AI_THRESH_CACHE](02_basic_design/04_database/TBL-TP-002.md)

### シーケンス設計

- [一覧](02_basic_design/05_sequences/index.md)

### 権限設計

- [一覧](02_basic_design/06_permissions/index.md)

### エラー設計

- [一覧](02_basic_design/07_errors/index.md)

### メッセージ設計

- [一覧](02_basic_design/08_messages/index.md)

## 将来対応

- [概要・一覧](03_future/index.md)
- [FUT01: 認証・セキュリティ強化](03_future/FUT01.md)
- [FUT02: 検索・AI 強化](03_future/FUT02.md)
- [FUT03: 国際化・リージョン](03_future/FUT03.md)
- [FUT04: プラン・課金・ブランド](03_future/FUT04.md)
- [FUT05: 通知・FAQ 運用・連携](03_future/FUT05.md)
- [FUT06: 個別チャット](03_future/FUT06.md)
- [FUT06: 個別チャット詳細設計](03_future/FUT06-detail.md)
- [FUT06: 個別チャット要件](03_future/FUT06-req.md)

---

保守・編集のルールは [CLAUDE.md](CLAUDE.md) を参照。
