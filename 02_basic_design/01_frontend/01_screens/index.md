# 画面設計書

> **このページは、メインシステムの全 33 画面(`SCR-001`〜`SCR-033`・公開ウィジェット含む)を `画面ID` / `画面名` / `URL` / `カテゴリ` で一覧する索引です。** 各画面名のリンクから個別ページ(レイアウト・画面項目・入出力・画面イベント)を開きます。

| 画面ID | 画面名 | URL | カテゴリ |
|----|----|----|----|
| [`SCR-001`](SCR-001.md) | [ログイン](SCR-001.md) | `/auth/login` | 認証フロー |
| [`SCR-002`](SCR-002.md) | [アカウント登録](SCR-002.md) | `/auth/register` | 認証フロー |
| [`SCR-003`](SCR-003.md) | [パスワード再設定](SCR-003.md) | `/auth/password-reset` | 認証フロー |
| [`SCR-018`](SCR-018.md) | [メール確認](SCR-018.md) | `/auth/email-verification` | 認証フロー |
| [`SCR-023`](SCR-023.md) | [メンバーアカウント有効化](SCR-023.md) | `/auth/activate` | 認証フロー |
| [`SCR-024`](SCR-024.md) | [連絡先メール確認完了](SCR-024.md) | `/auth/contact-verify` | 認証フロー |
| [`SCR-033`](SCR-033.md) | [ダッシュボード](SCR-033.md) | `/owner/dashboard` | 管理コンソール |
| [`SCR-021`](SCR-021.md) | [利用状況](SCR-021.md) | `/owner/usage` | 管理コンソール |
| [`SCR-004`](SCR-004.md) | [プロジェクト](SCR-004.md) | `/owner/projects` | 管理コンソール |
| [`SCR-005`](SCR-005.md) | [プロジェクト作成・編集(モーダル)](SCR-005.md) | `/owner/projects/new` | 管理コンソール |
| [`SCR-028`](SCR-028.md) | [請求管理](SCR-028.md) | `/owner/billing` | 管理コンソール |
| [`SCR-029`](SCR-029.md) | [設定](SCR-029.md) | `/owner/settings` | 管理コンソール |
| [`SCR-019`](SCR-019.md) | [退会](SCR-019.md) | `/owner/withdraw` | 管理コンソール |
| [`SCR-020`](SCR-020.md) | [規約再同意割込み](SCR-020.md) | `/owner/terms-reconsent` | 管理コンソール |
| [`SCR-012`](SCR-012.md) | [概要](SCR-012.md) | `/projects/:id/home` | プロジェクトワークスペース |
| [`SCR-006`](SCR-006.md) | [要対応の質問一覧](SCR-006.md) | `/projects/:id/inquiries` | プロジェクトワークスペース |
| [`SCR-007`](SCR-007.md) | [要対応の質問詳細](SCR-007.md) | `/projects/:id/inquiries/:iid` | プロジェクトワークスペース |
| [`SCR-008`](SCR-008.md) | [FAQ一覧](SCR-008.md) | `/projects/:id/faqs` | プロジェクトワークスペース |
| [`SCR-009`](SCR-009.md) | [FAQ編集](SCR-009.md) | `/projects/:id/faqs/:fid/edit` | プロジェクトワークスペース |
| [`SCR-010`](SCR-010.md) | [FAQ CSVインポート(モーダル)](SCR-010.md) | `/projects/:id/faqs/import` | プロジェクトワークスペース |
| [`SCR-011`](SCR-011.md) | [ウィジェット設定](SCR-011.md) | `/projects/:id/widget` | プロジェクトワークスペース |
| [`SCR-013`](SCR-013.md) | [メンバー](SCR-013.md) | `/projects/:id/members` | プロジェクトワークスペース |
| [`SCR-014`](SCR-014.md) | [メンバー招待・編集(モーダル)](SCR-014.md) | `/projects/:id/members/new` | プロジェクトワークスペース |
| [`SCR-026`](SCR-026.md) | [利用量と上限](SCR-026.md) | `/projects/:id/usage` | プロジェクトワークスペース |
| [`SCR-027`](SCR-027.md) | [質問数上限設定(モーダル)](SCR-027.md) | `/projects/:id/usage/limits/questions/edit` | プロジェクトワークスペース |
| [`SCR-031`](SCR-031.md) | [通知配信状態](SCR-031.md) | `/projects/:id/notifications/delivery-status` | プロジェクトワークスペース |
| [`SCR-032`](SCR-032.md) | [質問ログ](SCR-032.md) | `/projects/:id/question-logs` | プロジェクトワークスペース |
| [`SCR-015`](SCR-015.md) | [利用規約閲覧](SCR-015.md) | `/account/terms` | 共通領域 |
| [`SCR-016`](SCR-016.md) | [お知らせ一覧](SCR-016.md) | `/account/inbox` | 共通領域 |
| [`SCR-017`](SCR-017.md) | [お知らせ詳細](SCR-017.md) | `/account/inbox/:aid` | 共通領域 |
| [`SCR-022`](SCR-022.md) | [個人設定](SCR-022.md) | `/account/settings` | 共通領域 |
| [`SCR-025`](SCR-025.md) | [プライバシーポリシー閲覧](SCR-025.md) | `/account/policy` | 共通領域 |
| [`SCR-030`](SCR-030.md) | [FAQ ウィジェット](SCR-030.md) | `(埋め込み JS)` | エンドユーザー(公開ウィジェット) |
