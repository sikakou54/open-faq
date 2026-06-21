# FAQ AI ウィジェット SaaS / メインシステム 設計ポータル(Markdown 版)

本リポジトリは「FAQ AI ウィジェット SaaS / メインシステム」の設計ドキュメントを **Markdown** で管理する。
かつての静的 HTML ポータルを Markdown へ全面変換し、Markdown を正本とした。本書がポータルのトップ(旧サイドバー相当の全文書索引)である。

- 図は ` ```mermaid ` コードブロックで保持(GitHub 等でそのまま描画)。
- 画面モック(ワイヤーフレーム)は PNG 画像で表示(元の HTML は `<details>` 内に保持)。
- 相互参照は `<span id="…">` アンカーで保持(例 `FR-005` / `BR-028` / `API-AUTH-001` / `TBL-M-001`)。
- 各ページ上部にパンくず、下部に戻り導線を付与。

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

## 基本設計

- [概要](02_basic-design/index.md)

### 画面設計

- [画面設計書](02_basic-design/01_screen-design.md)
- [SCR-001 ログイン](02_basic-design/SCR-001.md)
- [SCR-002 アカウント登録](02_basic-design/SCR-002.md)
- [SCR-003 パスワード再設定](02_basic-design/SCR-003.md)
- [SCR-004 プロジェクト](02_basic-design/SCR-004.md)
- [SCR-004-001 プロジェクト作成・編集モーダル](02_basic-design/SCR-004-001.md)
- [SCR-005 要対応の質問一覧](02_basic-design/SCR-005.md)
- [SCR-005-001 要対応の質問詳細](02_basic-design/SCR-005-001.md)
- [SCR-006 FAQ 一覧](02_basic-design/SCR-006.md)
- [SCR-006-001 FAQ 編集](02_basic-design/SCR-006-001.md)
- [SCR-006-002 FAQ CSV インポートモーダル](02_basic-design/SCR-006-002.md)
- [SCR-007 ウィジェット設定](02_basic-design/SCR-007.md)
- [SCR-008 概要(プロジェクト)](02_basic-design/SCR-008.md)
- [SCR-009 メンバー(プロジェクト)](02_basic-design/SCR-009.md)
- [SCR-009-001 メンバー招待 / 編集モーダル(プロジェクト単位)](02_basic-design/SCR-009-001.md)
- [SCR-010 利用規約閲覧](02_basic-design/SCR-010.md)
- [SCR-011 お知らせ一覧](02_basic-design/SCR-011.md)
- [SCR-012 お知らせ詳細](02_basic-design/SCR-012.md)
- [SCR-013 メール確認](02_basic-design/SCR-013.md)
- [SCR-014 退会申請](02_basic-design/SCR-014.md)
- [SCR-015 規約再同意割込み](02_basic-design/SCR-015.md)
- [SCR-016 利用状況](02_basic-design/SCR-016.md)
- [SCR-017 個人設定](02_basic-design/SCR-017.md)
- [SCR-018 メンバーアカウント有効化](02_basic-design/SCR-018.md)
- [SCR-019 プロジェクト連絡先メール確認完了](02_basic-design/SCR-019.md)
- [SCR-020 プライバシーポリシー閲覧](02_basic-design/SCR-020.md)
- [SCR-021 利用量と上限(プロジェクト単位)](02_basic-design/SCR-021.md)
- [SCR-021-001 質問数上限設定モーダル](02_basic-design/SCR-021-001.md)
- [SCR-022 請求](02_basic-design/SCR-022.md)
- [SCR-023 設定](02_basic-design/SCR-023.md)
- [WIDGET エンドユーザー向け FAQ ウィジェット](02_basic-design/SCR-WIDGET.md)

### API設計

- [API 設計書](02_basic-design/02_api-design.md)
- [API 共通仕様](02_basic-design/API-common.md)
- [認証 API](02_basic-design/API-auth.md)
- [プロジェクト管理 API](02_basic-design/API-project.md)
- [利用者(メンバー)API](02_basic-design/API-member.md)
- [FAQ 管理 API](02_basic-design/API-faq.md)
- [未解決質問 API](02_basic-design/API-inquiry.md)
- [ウィジェット API](02_basic-design/API-widget.md)
- [ダッシュボード API](02_basic-design/API-dashboard.md)
- [利用量・課金 API](02_basic-design/API-billing.md)
- [お知らせ受信箱 API](02_basic-design/API-inbox.md)
- [規約・退会 API](02_basic-design/API-terms.md)
- [AI 推論 IF](02_basic-design/API-ai.md)
- [メール配信 IF](02_basic-design/API-mail.md)
- [外部 Webhook](02_basic-design/API-webhook.md)

### データベース設計

- [データベース設計書](02_basic-design/03_database-design.md)
- [M_USER](02_basic-design/TBL-M-001.md)
- [M_CONTRACT](02_basic-design/TBL-M-002.md)
- [M_PRJ_USERS](02_basic-design/TBL-M-003.md)
- [M_PROJECTS](02_basic-design/TBL-M-004.md)
- [TBL-M-005 M_ALLOWED_DOMAINS](02_basic-design/TBL-M-005.md)
- [TBL-M-006 M_FAQS](02_basic-design/TBL-M-006.md)
- [TBL-M-007 M_EMAIL_SUPPRESS](02_basic-design/TBL-M-007.md)
- [TBL-M-008 M_OWNER_QUOTA_OVR](02_basic-design/TBL-M-008.md)
- [TBL-M-009 M_PRJ_QUOTA_LIMITS](02_basic-design/TBL-M-009.md)
- [TBL-M-010 M_SERVICE_ANNOUNCE](02_basic-design/TBL-M-010.md)
- [TBL-M-011 M_ANNOUNCE_AUD](02_basic-design/TBL-M-011.md)
- [TBL-M-012 M_TERMS_VER](02_basic-design/TBL-M-012.md)
- [TBL-T-001 T_SESSIONS](02_basic-design/TBL-T-001.md)
- [TBL-T-002 T_ACCESS_TOKENS](02_basic-design/TBL-T-002.md)
- [TBL-T-003 T_PRJ_LEGACY_KEYS](02_basic-design/TBL-T-003.md)
- [TBL-T-004 T_QLOG_FAQ_REFS](02_basic-design/TBL-T-004.md)
- [TBL-T-005 T_INQUIRIES](02_basic-design/TBL-T-005.md)
- [TBL-T-006 T_BILL_SUBS](02_basic-design/TBL-T-006.md)
- [TBL-T-007 T_BILL_INVOICES](02_basic-design/TBL-T-007.md)
- [TBL-T-008 T_USAGE_METER](02_basic-design/TBL-T-008.md)
- [TBL-T-009 T_ANNOUNCE_RCPT](02_basic-design/TBL-T-009.md)
- [TBL-T-010 T_INBOX_MSG](02_basic-design/TBL-T-010.md)
- [TBL-T-011 T_WITHDRAW_REQ](02_basic-design/TBL-T-011.md)
- [TBL-T-012 T_TERMS_AGREE](02_basic-design/TBL-T-012.md)
- [TBL-H-001 H_QUESTION_LOGS](02_basic-design/TBL-H-001.md)
- [TBL-H-002 H_NOTIF_LOGS](02_basic-design/TBL-H-002.md)
- [TBL-H-003 H_AUDIT_LOGS](02_basic-design/TBL-H-003.md)
- [TBL-H-004 H_ERROR_LOGS](02_basic-design/TBL-H-004.md)
- [TBL-H-005 H_INQUIRY_FAQ](02_basic-design/TBL-H-005.md)
- [TBL-TP-001 TP_FAQ_FTS](02_basic-design/TBL-TP-001.md)
- [TBL-TP-002 TP_AI_THRESH_CACHE](02_basic-design/TBL-TP-002.md)

### 横断設計

- [ユースケース・シーケンス設計書](02_basic-design/04_usecase-design.md)
- [課金・請求設計書](02_basic-design/05_billing-design.md)
- [メール設計書](02_basic-design/06_mail-design.md)
- [認証・認可設計書](02_basic-design/07_auth-design.md)

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
