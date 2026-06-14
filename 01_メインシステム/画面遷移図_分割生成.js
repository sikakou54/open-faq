const fs = require("fs");
const path = require("path");

const baseDir = __dirname;
const sourceName = "画面遷移図.html";
const sourcePath = path.join(baseDir, sourceName);
const source = fs.readFileSync(sourcePath, "utf8");

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function stripTags(value) {
  return value.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function findBalancedDivEnd(html, start) {
  const token = /<div\b[^>]*>|<\/div\s*>/gi;
  token.lastIndex = start;
  let depth = 0;
  let match;

  while ((match = token.exec(html))) {
    depth += match[0].startsWith("</") ? -1 : 1;
    if (depth === 0) {
      return token.lastIndex;
    }
  }

  throw new Error(`Unclosed div starting at ${start}`);
}

function extractScreenBlocks(html) {
  const blocks = new Map();
  const startPattern = /<div class="screen" id="([^"]+)"/g;
  let match;

  while ((match = startPattern.exec(html))) {
    const start = match.index;
    const end = findBalancedDivEnd(html, start);
    const block = html.slice(start, end);
    const titleMatch = block.match(/class="scr-name"[^>]*>([\s\S]*?)<\/span>/);
    const userMatch = block.match(/class="scr-user">([\s\S]*?)<\/div>/);
    blocks.set(match[1], {
      html: block,
      title: titleMatch ? stripTags(titleMatch[1]) : match[1],
      sourceUser: userMatch ? stripTags(userMatch[1]) : "",
    });
    startPattern.lastIndex = end;
  }

  return blocks;
}

function removeDivsByClassAndText(html, className, phrases) {
  const pattern = new RegExp(
    `<div\\b[^>]*class="[^"]*\\b${className}\\b[^"]*"[^>]*>`,
    "gi",
  );
  const ranges = [];
  let match;

  while ((match = pattern.exec(html))) {
    const start = match.index;
    const end = findBalancedDivEnd(html, start);
    const text = stripTags(html.slice(start, end));
    if (phrases.some((phrase) => text.includes(phrase))) {
      ranges.push([start, end]);
    }
    pattern.lastIndex = end;
  }

  return ranges
    .sort((a, b) => b[0] - a[0])
    .reduce(
      (result, [start, end]) => result.slice(0, start) + result.slice(end),
      html,
    );
}

function removeButtonsByText(html, phrases) {
  return html.replace(
    /<button\b[^>]*>([\s\S]*?)<\/button>/gi,
    (button, inner) =>
      phrases.some((phrase) => stripTags(inner).includes(phrase)) ? "" : button,
  );
}

function addScreenNote(html, note, readOnly = false) {
  let result = html.replace(
    /(<div class="screen"[^>]*>)/,
    `$1<div class="role-screen-note">${note}</div>`,
  );
  if (readOnly) {
    result = result.replace(
      /<div class="screen"/,
      '<div class="screen role-readonly"',
    );
  }
  return result;
}

function makePublicLegalView(html) {
  let result = removeDivsByClassAndText(html, "app-header", ["open-faq"]);
  result = removeDivsByClassAndText(result, "app-sidebar", ["利用規約"]);
  result = result.replace(
    '<div class="app-layout">',
    '<div class="public-legal-layout">',
  );
  return addScreenNote(
    result,
    "<strong>公開閲覧版:</strong> 認証不要URLから文書本文のみを閲覧します。管理コンソールのサイドメニューは表示しません。",
  );
}

const blocks = extractScreenBlocks(source);

const catalog = {
  "scr-001": {
    purpose: "メールアドレスとパスワードで認証し、利用可能なワークスペースへ進む。",
    condition: "有効なアカウント。ロック中・無効アカウントは遷移不可。",
  },
  "scr-002": {
    purpose: "新規契約のオーナーアカウントを登録する。",
    condition: "未登録メールアドレス、規約・プライバシーポリシーへの同意。",
  },
  "scr-003": {
    purpose: "再設定リンクを使って自分のパスワードを更新する。",
    condition: "有効期限内かつ未使用の再設定トークン。",
  },
  "scr-004": {
    purpose: "契約配下のプロジェクトを一覧し、対象プロジェクトへ移動する。",
    condition: "契約オーナーのみ。",
  },
  "scr-004-m1": {
    purpose: "プロジェクトを新規作成し、オーナーを管理者として自動割当する。",
    condition: "契約オーナーのみ。必須情報と許可ドメインの検証を通過。",
  },
  "scr-005-list": {
    purpose: "AIで解決できなかった質問を状況別に確認する。",
    condition: "対象プロジェクトへの割当とFAQまたはログ参照権限。",
  },
  "scr-005-detail": {
    purpose: "質問内容・未解決理由を確認し、対応状況を手動更新する。",
    condition: "対象プロジェクトへの有効な割当。",
  },
  "scr-006-list": {
    purpose: "FAQを検索・一覧し、新規作成、公開管理、CSV操作へ進む。",
    condition: "対象プロジェクトへの有効な割当とFAQ権限。",
  },
  "scr-006-edit": {
    purpose: "FAQの質問・回答・カテゴリ・公開状態を編集する。",
    condition: "対象プロジェクトへの有効な割当とFAQ権限。",
  },
  "scr-006-m1": {
    purpose: "UTF-8 CSVでFAQを一括登録・更新する。",
    condition: "SCR-006のCSVインポートから起動。FAQ権限が必要。",
  },
  "scr-020": {
    purpose: "最新版のプライバシーポリシーを閲覧する。",
    condition: "認証不要の公開URL、または管理画面の共通導線。",
  },
  "scr-007": {
    purpose: "公開キー、埋め込みコード、見た目、プレビューを確認・設定する。",
    condition: "対象プロジェクトへの割当。操作範囲はロールで変わる。",
  },
  "scr-008": {
    purpose: "選択中プロジェクトの状況を把握し、日常業務の各画面へ進む。",
    condition: "対象プロジェクトへの有効な割当。",
  },
  "scr-009": {
    purpose: "対象プロジェクトの参加者とロールを一覧・管理する。",
    condition: "対象プロジェクトの管理者または契約オーナー。",
  },
  "scr-009-m1": {
    purpose: "メンバー招待、ロール変更、プロジェクト割当解除を行う。",
    condition: "SCR-009から起動。対象プロジェクトの管理者以上。",
  },
  "scr-010": {
    purpose: "最新版の利用規約を閲覧する。",
    condition: "認証不要の公開URL、または管理画面の共通導線。",
  },
  "scr-011": {
    purpose: "自契約に配信されたお知らせを重要度・既読状態とともに一覧する。",
    condition: "認証済み管理コンソール利用者。",
  },
  "scr-012": {
    purpose: "選択したお知らせの本文と関連導線を確認する。",
    condition: "SCR-011または通知ベルから遷移。",
  },
  "scr-013": {
    purpose: "新規オーナー登録後のメールアドレス確認を完了する。",
    condition: "有効期限内かつ未使用のメール確認トークン。",
  },
  "scr-014": {
    purpose: "契約終了の影響を確認し、退会を申請する。",
    condition: "契約オーナーのみ。確認と再認証を伴う。",
  },
  "scr-015": {
    purpose: "改定された規約・ポリシーを確認し、契約として再同意する。",
    condition: "契約オーナーのみ。未同意時に強制割込み。",
  },
  "scr-016": {
    purpose: "契約全体のプロジェクト、利用状況、対応事項を俯瞰する。",
    condition: "契約オーナーのみ。",
  },
  "widget-enduser": {
    purpose: "導入サイト上のチャットUIでFAQ質問を行い、未解決時は問い合わせIDと連絡先を確認する。",
    condition: "許可ドメイン上の埋め込み。上限到達時は質問受付停止。",
  },
  "scr-017": {
    purpose: "自分のプロフィール、パスワード、セッション、参加プロジェクトを管理する。",
    condition: "認証済みユーザー。契約情報・退会はオーナーだけに表示。",
  },
  "scr-018": {
    purpose: "招待された本人が氏名・初回パスワード・規約同意を登録する。",
    condition: "有効期限7日以内の未使用招待トークン。",
  },
  "scr-019": {
    purpose: "プロジェクト連絡先メールの所有確認を完了する。",
    condition: "有効期限24時間以内の連絡先確認トークン。アカウント不要。",
  },
  "scr-021": {
    purpose: "対象プロジェクトの当月質問数と月次上限を確認する。",
    condition: "対象プロジェクトへの有効な割当。変更範囲はロールで変わる。",
  },
  "scr-021-m1": {
    purpose: "質問数上限のON/OFF、件数、通知閾値を設定する。",
    condition: "対象プロジェクトの管理者または契約オーナー。再認証必須。",
  },
  "scr-022": {
    purpose: "契約横断の利用量と上限接近プロジェクトを確認する。",
    condition: "契約オーナーのみ。",
  },
  "scr-023": {
    purpose: "プラン、支払方法、請求状態、請求履歴を管理する。",
    condition: "契約オーナーのみ。重要変更は再認証。",
  },
  "scr-024": {
    purpose: "契約メンバーと参加プロジェクトを横断管理する。",
    condition: "契約オーナーのみ。契約からの削除は再認証。",
  },
  "scr-025": {
    purpose: "契約内で行われた重要操作の監査履歴を確認する。",
    condition: "契約オーナーのみ。",
  },
  "scr-026": {
    purpose: "契約名、重要連絡先、契約終了導線を管理する。",
    condition: "契約オーナーのみ。",
  },
  "scr-027": {
    purpose: "プロジェクト基本情報と問い合わせ先を確認・管理する。",
    condition: "オーナーは編集・削除可。プロジェクト管理者は参照のみ。",
  },
};

const commonAuthenticatedTail = [
  "scr-011",
  "scr-012",
  "scr-017",
  "scr-010",
  "scr-020",
];
const memberProjectWork = [
  "scr-008",
  "scr-005-list",
  "scr-005-detail",
  "scr-006-list",
  "scr-006-edit",
  "scr-006-m1",
  "scr-007",
  "scr-021",
];
const adminProjectWork = [
  "scr-008",
  "scr-005-list",
  "scr-005-detail",
  "scr-006-list",
  "scr-006-edit",
  "scr-006-m1",
  "scr-007",
  "scr-009",
  "scr-009-m1",
  "scr-021",
  "scr-021-m1",
  "scr-027",
  "scr-019",
];
const ownerContractWork = [
  "scr-016",
  "scr-004",
  "scr-004-m1",
  "scr-022",
  "scr-023",
  "scr-024",
  "scr-025",
  "scr-026",
  "scr-014",
];

const roles = [
  {
    slug: "ウィジェット利用者",
    file: "画面遷移図_ウィジェット利用者.html",
    audienceKey: "widget-user",
    title: "ウィジェット利用者",
    subtitle: "導入サイトでFAQ質問と問い合わせ案内を利用するエンドユーザー",
    description:
      "管理コンソールのアカウントを持たず、導入サイトに埋め込まれたFAQウィジェットを利用します。管理画面、設定、契約情報にはアクセスしません。",
    color: "#0f766e",
    screens: [
      "widget-enduser",
      "scr-010",
      "scr-020",
    ],
    access: {
      "widget-enduser": "チャットUIで質問。上限到達時は返信で問い合わせ先を確認",
      "scr-010": "公開URLで閲覧",
      "scr-020": "公開URLで閲覧",
    },
    flows: [
      {
        name: "FAQ質問・問い合わせ",
        steps: [
          "WIDGET 質問",
          "AIで未解決",
          "問い合わせID発行",
          "連絡先メール表示",
          "別のFAQ質問を継続",
        ],
        condition:
          "質問受付中で公開済みFAQから回答できなかった場合。問い合わせIDと確認済み連絡先を表示。",
      },
      {
        name: "質問上限到達",
        steps: ["WIDGET 質問", "429 / 受付停止", "連絡先メールへ誘導"],
        condition: "プロジェクトの月次質問数が設定上限100%に到達。",
      },
    ],
    differences: [
      ["管理コンソール", "利用不可", "プロジェクト・契約のデータや設定は表示しない"],
      ["利用規約・ポリシー", "公開閲覧", "認証不要URLから本文のみ表示"],
      ["質問受付", "状態依存", "上限到達・契約停止時は新規質問を受け付けない"],
    ],
    excluded: [
      "SCR-001〜003、SCR-011〜016、SCR-017、SCR-018〜027の管理コンソール画面",
      "FAQ編集、メンバー管理、ウィジェット設定、利用量設定",
      "契約・請求・退会・操作履歴",
    ],
    notes: [
      "SCR-010 / SCR-020は既存画面の認証不要版として、管理サイドバーを除いた本文表示にしています。",
      "WIDGETは固有SCR IDを持たないiframe状態図ですが、利用者が最初に触れる画面として含めています。",
    ],
  },
  {
    slug: "プロジェクトメンバー",
    file: "画面遷移図_プロジェクトメンバー.html",
    audienceKey: "project-member",
    title: "プロジェクトメンバー",
    subtitle: "割り当てられたプロジェクトの日常運用を担当する利用者",
    description:
      "担当プロジェクトのFAQ、要対応質問、ログを扱います。メンバー招待・ロール変更、上限変更、プロジェクト設定、契約管理は行いません。",
    color: "#2563eb",
    screens: [
      "scr-018",
      "scr-001",
      "scr-003",
      ...memberProjectWork,
      ...commonAuthenticatedTail,
    ],
    access: {
      "scr-018": "招待受諾時のみ",
      "scr-001": "ログイン",
      "scr-003": "自分のパスワード再設定",
      "scr-008": "担当プロジェクトの概要",
      "scr-005-list": "閲覧・絞り込み・出力",
      "scr-005-detail": "閲覧・対応状況更新",
      "scr-006-list": "FAQ一覧・公開管理・CSV操作",
      "scr-006-edit": "FAQ編集",
      "scr-006-m1": "FAQ CSVインポート",
      "scr-007": "閲覧・埋め込みコードコピーのみ",
      "scr-021": "閲覧のみ",
      "scr-011": "自契約のお知らせ閲覧",
      "scr-012": "お知らせ詳細閲覧",
      "scr-017": "自分のプロフィール・セキュリティ",
      "scr-010": "閲覧",
      "scr-020": "閲覧",
    },
    flows: [
      {
        name: "招待から利用開始",
        steps: ["招待メール", "SCR-018 有効化", "SCR-001 ログイン", "SCR-008 概要"],
        condition: "有効な招待トークンと、氏名・パスワード・規約同意の完了。",
      },
      {
        name: "要対応質問からFAQ化",
        steps: ["SCR-008", "SCR-005 一覧", "SCR-005 詳細", "SCR-006 FAQ編集"],
        condition: "担当プロジェクトへの有効な割当。",
      },
      {
        name: "利用状況確認",
        steps: ["SCR-008", "SCR-021 閲覧", "管理者へ変更依頼"],
        condition: "メンバーは上限とアラートを変更できない。",
      },
    ],
    differences: [
      ["FAQ・要対応質問", "編集・対応可", "担当プロジェクト内に限定"],
      ["ウィジェット", "閲覧・コードコピーのみ", "公開キー再発行と設定保存は不可"],
      ["利用量と上限", "閲覧のみ", "上限・アラート変更は管理者以上"],
      ["メンバー管理", "利用不可", "招待・ロール変更・割当解除は管理者以上"],
      ["プロジェクト設定", "利用不可", "メニューと画面を表示しない"],
      ["契約管理", "利用不可", "契約WS自体を表示しない"],
    ],
    excluded: [
      "SCR-009 / SCR-009-M1 メンバー管理",
      "SCR-021-M1 上限設定、SCR-027 プロジェクト設定",
      "SCR-004 / SCR-014〜016 / SCR-022〜026の契約・オーナー専用画面",
      "SCR-002 / SCR-013の新規オーナー登録フロー",
    ],
    notes: [
      "SCR-007は既存ワイヤーフレームから設定保存・公開キー再発行を除外し、読み取り専用として掲載しています。",
      "SCR-017からオーナー専用の契約連絡先・退会パネルを除外しています。",
    ],
  },
  {
    slug: "プロジェクト管理者",
    file: "画面遷移図_プロジェクト管理者.html",
    audienceKey: "project-admin",
    title: "プロジェクト管理者",
    subtitle: "担当プロジェクトの運用・メンバー・上限設定を管理する利用者",
    description:
      "プロジェクトメンバーの全操作に加え、担当プロジェクトのメンバー招待・ロール変更、ウィジェット設定、質問数上限設定を行います。契約・請求・退会は扱いません。",
    color: "#7c3aed",
    screens: [
      "scr-018",
      "scr-001",
      "scr-003",
      ...adminProjectWork,
      ...commonAuthenticatedTail,
    ],
    access: {
      "scr-018": "招待受諾時のみ",
      "scr-001": "ログイン",
      "scr-003": "自分のパスワード再設定",
      "scr-008": "担当プロジェクトの概要",
      "scr-005-list": "閲覧・絞り込み・出力",
      "scr-005-detail": "閲覧・対応状況更新",
      "scr-006-list": "FAQ一覧・公開管理・CSV操作",
      "scr-006-edit": "FAQ編集",
      "scr-006-m1": "FAQ CSVインポート",
      "scr-007": "設定保存・公開キー再発行",
      "scr-009": "担当プロジェクトのメンバー一覧",
      "scr-009-m1": "招待・ロール変更・割当解除",
      "scr-021": "閲覧・設定画面起動",
      "scr-021-m1": "上限・通知閾値変更",
      "scr-027": "参照のみ",
      "scr-019": "連絡先メール所有者が確認",
      "scr-011": "自契約のお知らせ閲覧",
      "scr-012": "お知らせ詳細閲覧",
      "scr-017": "自分のプロフィール・セキュリティ",
      "scr-010": "閲覧",
      "scr-020": "閲覧",
    },
    flows: [
      {
        name: "招待から利用開始",
        steps: ["招待メール", "SCR-018 有効化", "SCR-001 ログイン", "SCR-008 概要"],
        condition: "招待時に当該プロジェクトのadminロールが付与されること。",
      },
      {
        name: "メンバー管理",
        steps: ["SCR-008", "SCR-009 一覧", "SCR-009-M1 招待・編集"],
        condition: "担当プロジェクト内のみ。契約からのアカウント削除は不可。",
      },
      {
        name: "上限・アラート設定",
        steps: ["SCR-008", "SCR-021", "SCR-021-M1", "再認証・保存"],
        condition: "対象プロジェクトのadminロールと再認証。",
      },
      {
        name: "連絡先メール確認",
        steps: ["SCR-027 参照", "オーナーが確認メール送信", "SCR-019 所有者確認"],
        condition: "SCR-027の編集・送信操作はオーナーが実施。",
      },
    ],
    differences: [
      ["FAQ・要対応質問", "編集・対応可", "担当プロジェクト内に限定"],
      ["メンバー管理", "招待・ロール変更・割当解除可", "契約からのアカウント削除は不可"],
      ["ウィジェット", "設定・公開キー再発行可", "再発行は再認証を伴う"],
      ["利用量と上限", "閲覧・変更可", "質問数上限と通知閾値のみ"],
      ["プロジェクト設定", "参照のみ", "編集・削除・確認メール送信はオーナー専用"],
      ["契約管理", "利用不可", "契約WS、料金、請求、退会を表示しない"],
    ],
    excluded: [
      "SCR-004 / SCR-004-M1 プロジェクト作成",
      "SCR-014〜016 / SCR-022〜026の契約・課金・退会・監査画面",
      "SCR-024の契約メンバー管理とアカウント削除",
      "SCR-002 / SCR-013の新規オーナー登録フロー",
    ],
    notes: [
      "SCR-027は権限設計の正本に合わせ、編集ボタン・確認メール送信・削除パネルを除外した参照版です。",
      "SCR-019の実操作者はプロジェクト管理者本人とは限らず、連絡先メールの所有者です。設定フローとの関係から本ページにも掲載しています。",
      "SCR-017からオーナー専用の契約連絡先・退会パネルを除外しています。",
    ],
  },
  {
    slug: "オーナー",
    file: "画面遷移図_オーナー.html",
    audienceKey: "owner",
    title: "オーナー",
    subtitle: "契約全体とすべてのプロジェクトを管理する契約オーナー",
    description:
      "契約ワークスペースと全プロジェクトワークスペースを利用し、プロジェクト作成、課金、契約メンバー、監査、契約設定、退会を含むすべての管理操作を行います。",
    color: "#b45309",
    screens: [
      "scr-002",
      "scr-013",
      "scr-001",
      "scr-003",
      "scr-015",
      ...ownerContractWork,
      ...adminProjectWork,
      ...commonAuthenticatedTail,
    ],
    access: {},
    flows: [
      {
        name: "新規契約開始",
        steps: ["SCR-002 登録", "SCR-013 メール確認", "SCR-001 ログイン", "SCR-016 契約概要"],
        condition: "メール確認と初回規約同意が完了していること。",
      },
      {
        name: "プロジェクト作成・運用",
        steps: ["SCR-016", "SCR-004", "SCR-004-M1 作成", "SCR-008 プロジェクト概要"],
        condition: "契約オーナー。作成後は自動でプロジェクト管理者となる。",
      },
      {
        name: "契約管理",
        steps: ["SCR-016", "SCR-022 利用状況", "SCR-023 料金・請求", "SCR-026 契約設定"],
        condition: "契約ワークスペース内のオーナー専有導線。",
      },
      {
        name: "退会",
        steps: ["SCR-026", "SCR-014 影響確認", "再認証", "退会申請"],
        condition: "契約オーナーのみ。全プロジェクト・全メンバーへ影響。",
      },
      {
        name: "規約再同意",
        steps: ["SCR-001", "SCR-015 強制割込み", "同意 / 退会判断", "SCR-016"],
        condition: "契約に適用される最新版への未同意がある場合。",
      },
    ],
    differences: [
      ["契約ワークスペース", "全機能", "契約概要、プロジェクト、利用状況、請求、メンバー、監査、設定"],
      ["プロジェクトワークスペース", "全機能", "全プロジェクトで暗黙の管理者権限"],
      ["プロジェクト設定", "編集・削除可", "削除はプロジェクト名確認と再認証"],
      ["契約メンバー", "横断管理・契約から削除可", "オーナー自身は削除不可"],
      ["規約再同意・退会", "契約判断可", "他ロールへ委譲不可"],
      ["料金・請求", "閲覧・変更可", "重要変更は再認証"],
    ],
    excluded: [
      "WIDGETのエンドユーザー本人向け画面",
      "SCR-018の招待メンバー有効化画面（オーナー自身は新規登録フローを利用）",
      "運営者システム主管のSCR-090〜098",
    ],
    notes: [
      "SCR-019の実操作者は連絡先メール所有者ですが、オーナーが設定・確認メール送信を管理するためフローに含めています。",
      "プロジェクト画面ではオーナーが全プロジェクトのadmin相当として操作できます。",
    ],
  },
];

const extraCss = `
<style>
body { padding-top: 54px; }
.role-nav { position: fixed; inset: 0 0 auto 0; z-index: 1000; min-height: 54px; display: flex; align-items: center; gap: 8px; padding: 8px 18px; background: rgba(255,255,255,.96); border-bottom: 1px solid var(--border); box-shadow: var(--shadow-sm); backdrop-filter: blur(8px); }
.role-nav .brand { font-weight: var(--fw-bold); color: var(--text); margin-right: auto; }
.role-nav a { color: var(--text-secondary); text-decoration: none; border: 1px solid var(--border); border-radius: var(--r-pill); padding: 5px 10px; background: var(--surface); font-size: var(--fs-sm); }
.role-nav a:hover { border-color: var(--role-accent); color: var(--role-accent); }
.role-nav a.current { background: var(--role-accent); border-color: var(--role-accent); color: #fff; font-weight: var(--fw-semibold); }
.role-document { max-width: 1440px; margin: 0 auto; padding: 28px 24px 48px; }
.role-hero { color: #fff; background: linear-gradient(135deg, var(--role-accent), color-mix(in srgb, var(--role-accent) 70%, #111827)); border-radius: 16px; padding: 30px; box-shadow: var(--shadow-lg); margin-bottom: 20px; }
.role-hero .eyebrow { font-size: var(--fs-sm); font-weight: var(--fw-bold); letter-spacing: .08em; opacity: .82; }
.role-hero h1 { margin: 6px 0 4px; font-size: 30px; }
.role-hero .lead { margin: 0 0 12px; font-size: var(--fs-lg); font-weight: var(--fw-semibold); }
.role-hero p { max-width: 900px; margin: 0; font-size: var(--fs-md); }
.role-hero .hero-links { margin-top: 18px; display: flex; gap: 8px; flex-wrap: wrap; }
.role-hero .hero-links a { color: #fff; border: 1px solid rgba(255,255,255,.45); border-radius: var(--r-pill); padding: 5px 11px; text-decoration: none; }
.doc-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.doc-section { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: var(--shadow-sm); break-inside: avoid; }
.doc-section h2 { margin: 0 0 12px; font-size: var(--fs-xl); color: var(--text); }
.doc-section h3 { margin: 14px 0 7px; font-size: var(--fs-md); }
.doc-section p { color: var(--text-secondary); }
.scope-badge { display: inline-block; color: var(--role-accent); background: color-mix(in srgb, var(--role-accent) 10%, white); border: 1px solid color-mix(in srgb, var(--role-accent) 32%, white); border-radius: var(--r-pill); padding: 3px 10px; font-weight: var(--fw-semibold); }
.role-table { width: 100%; border-collapse: collapse; font-size: var(--fs-sm); }
.role-table th, .role-table td { border: 1px solid var(--border); padding: 8px 10px; text-align: left; vertical-align: top; }
.role-table th { background: var(--gray-50); color: var(--text-secondary); }
.role-table tr:nth-child(even) td { background: var(--gray-25); }
.role-table a { color: var(--link); }
.flow-list { display: grid; gap: 12px; }
.flow-card { border: 1px solid var(--border); border-radius: var(--r-lg); padding: 12px; background: var(--gray-25); }
.flow-card strong { color: var(--role-accent); }
.flow-steps { display: flex; flex-wrap: wrap; align-items: center; gap: 7px; margin: 8px 0; }
.flow-step { border: 1px solid color-mix(in srgb, var(--role-accent) 35%, white); background: color-mix(in srgb, var(--role-accent) 7%, white); border-radius: var(--r-md); padding: 6px 9px; font-weight: var(--fw-medium); }
.flow-arrow { color: var(--role-accent); font-weight: var(--fw-bold); }
.plain-list { margin: 0; padding-left: 20px; color: var(--text-secondary); }
.plain-list li { margin: 5px 0; }
.wireframe-heading { margin: 32px 0 12px; padding: 18px 20px; border-radius: 12px; color: #fff; background: var(--role-accent); }
.wireframe-heading h2 { margin: 0; font-size: var(--fs-xl); }
.wireframe-heading p { margin: 4px 0 0; opacity: .88; }
.wireframe-stack .screen { margin-bottom: 20px; min-height: auto; page-break-after: always; }
.role-screen-note { margin: 0 0 8px; padding: 8px 12px; border: 1px solid color-mix(in srgb, var(--role-accent) 35%, white); border-left: 4px solid var(--role-accent); border-radius: var(--r-md); color: color-mix(in srgb, var(--role-accent) 80%, #111827); background: color-mix(in srgb, var(--role-accent) 7%, white); font-size: var(--fs-sm); }
.role-readonly .input, .role-readonly .select, .role-readonly .textarea { background: var(--gray-50); color: var(--text-secondary); }
.public-legal-layout { border: 1px solid var(--border); border-radius: var(--r-lg); background: var(--surface); min-height: 540px; }
.public-legal-layout .app-main { max-width: 960px; margin: 0 auto; padding: 28px; }
.source-note { font-size: var(--fs-sm); color: var(--text-secondary); text-align: center; padding: 14px; }
.index-cards { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 16px; }
.index-card { border: 1px solid var(--border); border-top: 5px solid var(--card-accent); border-radius: 12px; padding: 18px; background: var(--surface); box-shadow: var(--shadow-sm); }
.index-card h2 { margin: 0 0 6px; }
.index-card .open-link { display: inline-block; margin-top: 10px; color: #fff; background: var(--card-accent); border-radius: var(--r-md); padding: 7px 12px; text-decoration: none; font-weight: var(--fw-semibold); }
.comparison td:not(:first-child), .comparison th:not(:first-child) { text-align: center; }
.mark-full { color: var(--success); font-weight: var(--fw-bold); }
.mark-limited { color: var(--warning); font-weight: var(--fw-bold); }
.mark-none { color: var(--text-muted); }
@media (max-width: 900px) {
  body { padding-top: 94px; }
  .role-nav { flex-wrap: wrap; }
  .role-nav .brand { width: 100%; }
  .doc-grid, .index-cards { grid-template-columns: 1fr; }
  .role-document { padding: 18px 12px 36px; }
  .role-table { display: block; overflow-x: auto; }
}
@media print {
  body { padding-top: 0; }
  .role-nav { display: none; }
  .role-document { max-width: none; padding: 0; }
  .role-hero { box-shadow: none; }
  .doc-section { box-shadow: none; }
  .wireframe-stack .screen { margin-bottom: 0; }
}
</style>`;

function buildHead(title, accent) {
  const originalHead = source.match(/<head>([\s\S]*?)<\/head>/);
  if (!originalHead) {
    throw new Error("Source head not found");
  }

  return originalHead[1]
    .replace(/<title>[\s\S]*?<\/title>/, `<title>${escapeHtml(title)}</title>`)
    .concat(extraCss)
    .concat(`<style>:root { --role-accent: ${accent}; }</style>`);
}

function renderNav(currentFile) {
  const links = [
    ["画面遷移図_index.html", "全体入口"],
    ...roles.map((role) => [role.file, role.title]),
  ];
  return `<nav class="role-nav" aria-label="ユーザー種別別の画面遷移図">
  <span class="brand">open-faq 画面遷移図</span>
  ${links
    .map(
      ([file, label]) =>
        `<a href="${file}"${file === currentFile ? ' class="current" aria-current="page"' : ""}>${label}</a>`,
    )
    .join("\n  ")}
</nav>`;
}

function roleSpecificBlock(role, id) {
  const sourceBlock = blocks.get(id);
  if (!sourceBlock) {
    throw new Error(`Screen block not found: ${id}`);
  }

  let html = sourceBlock.html;

  html = removeDivsByClassAndText(html, "item", [
    "チャット",
    "自動割り当て",
  ]);

  if (role.audienceKey === "widget-user" && ["scr-010", "scr-020"].includes(id)) {
    return makePublicLegalView(html);
  }

  if (["project-member", "project-admin"].includes(role.audienceKey) && id === "scr-017") {
    html = removeDivsByClassAndText(html, "panel", [
      "連絡先 / 契約情報(オーナーのみ表示)",
      "退会(オーナーのみ表示)",
    ]);
    html = addScreenNote(
      html,
      "<strong>共通アカウント領域:</strong> このロールでは自分のプロフィール・パスワード・セッション・参加プロジェクトだけを表示します。",
    );
  }

  if (role.audienceKey === "project-member") {
    html = removeDivsByClassAndText(html, "item", [
      "自動割り当て",
      "メンバー",
      "プロジェクト設定",
    ]);
    if (id === "scr-007") {
      html = removeButtonsByText(html, ["設定を保存", "公開キーを再発行"]);
      html = addScreenNote(
        html,
        "<strong>メンバー権限:</strong> 設定値の閲覧と埋め込みコードのコピーのみ可能です。設定保存・公開キー再発行は表示しません。",
        true,
      );
    }
    if (id === "scr-021") {
      html = removeButtonsByText(html, ["アラート設定"]);
      html = addScreenNote(
        html,
        "<strong>メンバー権限:</strong> 当月利用量と上限の閲覧のみ可能です。上限・通知閾値の変更導線は表示しません。",
        true,
      );
    }
  }

  if (role.audienceKey === "project-admin" && id === "scr-027") {
    html = removeDivsByClassAndText(html, "panel", ["プロジェクトの削除"]);
    html = removeButtonsByText(html, [
      "変更を保存",
      "確認メールを送信",
      "プロジェクトを削除",
    ]);
    html = addScreenNote(
      html,
      "<strong>プロジェクト管理者権限:</strong> 基本情報と問い合わせ先は参照のみです。編集・確認メール送信・削除は契約オーナー専用です。",
      true,
    );
  }

  if (role.audienceKey === "owner" && id === "scr-019") {
    html = addScreenNote(
      html,
      "<strong>外部確認ステップ:</strong> オーナーが送信した確認メールを、連絡先メール所有者が開いて完了します。",
    );
  }

  if (role.audienceKey === "project-admin" && id === "scr-019") {
    html = addScreenNote(
      html,
      "<strong>外部確認ステップ:</strong> 実際の到達者は連絡先メール所有者です。プロジェクト管理者は完了状態を確認します。",
    );
  }

  return html;
}

function renderFlow(flow) {
  return `<div class="flow-card">
  <strong>${escapeHtml(flow.name)}</strong>
  <div class="flow-steps">${flow.steps
    .map(
      (step, index) =>
        `${index ? '<span class="flow-arrow" aria-hidden="true">→</span>' : ""}<span class="flow-step">${escapeHtml(step)}</span>`,
    )
    .join("")}</div>
  <div class="small">遷移条件: ${escapeHtml(flow.condition)}</div>
</div>`;
}

function renderRolePage(role) {
  const screenRows = role.screens
    .map((id) => {
      const block = blocks.get(id);
      const meta = catalog[id];
      if (!block || !meta) {
        throw new Error(`Missing screen metadata: ${id}`);
      }
      const access =
        role.access[id] ||
        (role.audienceKey === "owner"
          ? id === "scr-019"
            ? "確認メール送信と完了状態の管理"
            : "閲覧・操作可"
          : "利用可");
      return `<tr>
  <td><a href="#${id}">${escapeHtml(block.title)}</a><br><span class="small">${escapeHtml(id)}</span></td>
  <td>${escapeHtml(meta.purpose)}</td>
  <td>${escapeHtml(access)}</td>
  <td>${escapeHtml(meta.condition)}</td>
</tr>`;
    })
    .join("\n");

  const body = `<!DOCTYPE html>
<html lang="ja">
<head>${buildHead(`open-faq 画面遷移図 - ${role.title}`, role.color)}</head>
<body data-audience="${role.audienceKey}">
${renderNav(role.file)}
<main class="role-document">
  <section class="role-hero">
    <div class="eyebrow">USER-SPECIFIC SCREEN FLOW</div>
    <h1>${escapeHtml(role.title)}の画面遷移図</h1>
    <div class="lead">${escapeHtml(role.subtitle)}</div>
    <p>${escapeHtml(role.description)}</p>
    <div class="hero-links">
      <a href="#screen-list">利用可能な画面</a>
      <a href="#flows">主要フロー</a>
      <a href="#permissions">権限差分</a>
      <a href="#wireframes">画面ワイヤーフレーム</a>
    </div>
  </section>

  <div class="doc-grid">
    <section class="doc-section">
      <h2>対象ユーザー種別</h2>
      <p><span class="scope-badge">${escapeHtml(role.title)}</span></p>
      <p>${escapeHtml(role.description)}</p>
      <p class="small">収録画面: ${role.screens.length}画面 / 元資料: <a href="${sourceName}">${sourceName}</a></p>
    </section>
    <section class="doc-section">
      <h2>補足事項</h2>
      <ul class="plain-list">${role.notes.map((note) => `<li>${escapeHtml(note)}</li>`).join("")}</ul>
    </section>
  </div>

  <section class="doc-section" id="screen-list">
    <h2>利用可能な画面一覧・画面ごとの役割・遷移条件</h2>
    <table class="role-table">
      <thead><tr><th>画面</th><th>役割</th><th>このユーザーの操作範囲</th><th>到達・遷移条件</th></tr></thead>
      <tbody>${screenRows}</tbody>
    </table>
  </section>

  <section class="doc-section" id="flows">
    <h2>画面遷移図・主要な操作フロー</h2>
    <div class="flow-list">${role.flows.map(renderFlow).join("")}</div>
  </section>

  <div class="doc-grid">
    <section class="doc-section" id="permissions">
      <h2>他ユーザー種別との権限差分</h2>
      <table class="role-table">
        <thead><tr><th>機能領域</th><th>操作範囲</th><th>差分・制約</th></tr></thead>
        <tbody>${role.differences
          .map(
            (row) =>
              `<tr>${row.map((cell) => `<td>${escapeHtml(cell)}</td>`).join("")}</tr>`,
          )
          .join("")}</tbody>
      </table>
    </section>
    <section class="doc-section">
      <h2>このページから除外した画面・遷移</h2>
      <ul class="plain-list">${role.excluded.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    </section>
  </div>

  <section id="wireframes">
    <div class="wireframe-heading">
      <h2>${escapeHtml(role.title)}向け画面ワイヤーフレーム</h2>
      <p>既存の画面情報を保ちながら、このユーザー種別で利用する画面だけを収録しています。</p>
    </div>
    <div class="wireframe-stack">
      ${role.screens.map((id) => roleSpecificBlock(role, id)).join("\n")}
    </div>
  </section>
  <div class="source-note">全体版は <a href="${sourceName}">${sourceName}</a>、ユーザー種別の入口は <a href="画面遷移図_index.html">画面遷移図_index.html</a> を参照してください。</div>
</main>
<script>(function(){function r(){window.lucide&&lucide.createIcons({attrs:{'aria-hidden':'true',focusable:'false'}});}document.readyState==='loading'?document.addEventListener('DOMContentLoaded',r):r();})();</script>
</body>
</html>`;

  fs.writeFileSync(path.join(baseDir, role.file), body);
}

const comparisonRows = [
  ["公開ウィジェット・質問", "◎", "×", "×", "◎ 設定・プレビュー"],
  ["プロジェクト概要", "×", "◎", "◎", "◎"],
  ["FAQ・要対応質問", "×", "◎", "◎", "◎"],
  ["ウィジェット設定", "×", "△ 閲覧・コピー", "◎", "◎"],
  ["プロジェクトメンバー管理", "×", "×", "◎ 担当PJ", "◎ 全PJ"],
  ["質問数上限・アラート", "×", "△ 閲覧", "◎ 担当PJ", "◎ 全PJ"],
  ["プロジェクト設定", "×", "×", "△ 参照", "◎ 編集・削除"],
  ["契約・課金・監査・退会", "×", "×", "×", "◎"],
  ["利用規約・プライバシーポリシー", "◎ 公開閲覧", "◎ 閲覧", "◎ 閲覧", "◎ 閲覧・契約判断"],
];

function markClass(value) {
  if (value.startsWith("◎")) return "mark-full";
  if (value.startsWith("△")) return "mark-limited";
  return "mark-none";
}

function renderIndexPage() {
  const indexFile = "画面遷移図_index.html";
  const iaBlock = blocks.get("ia-v3");
  if (!iaBlock) {
    throw new Error("IA overview block not found");
  }

  const cards = roles
    .map(
      (role) => `<article class="index-card" style="--card-accent: ${role.color}">
  <h2>${escapeHtml(role.title)}</h2>
  <p><strong>${escapeHtml(role.subtitle)}</strong></p>
  <p>${escapeHtml(role.description)}</p>
  <div class="small">収録画面: ${role.screens.length}画面</div>
  <a class="open-link" href="${role.file}">この画面遷移図を開く</a>
</article>`,
    )
    .join("\n");

  const body = `<!DOCTYPE html>
<html lang="ja">
<head>${buildHead("open-faq ユーザー種別別 画面遷移図", "#2f5bd0")}</head>
<body data-audience="index">
${renderNav(indexFile)}
<main class="role-document">
  <section class="role-hero">
    <div class="eyebrow">SCREEN FLOW INDEX</div>
    <h1>ユーザー種別別 画面遷移図</h1>
    <div class="lead">open-faqの画面と遷移を、実際の利用範囲に合わせて4種類に分割</div>
    <p>全体版の情報を保持しながら、ウィジェット利用者、プロジェクトメンバー、プロジェクト管理者、オーナーごとに必要な画面・遷移・権限差分を整理しています。</p>
    <div class="hero-links">
      <a href="#roles">ユーザー種別を選ぶ</a>
      <a href="#comparison">利用範囲を比較</a>
      <a href="#common">共通・専用画面</a>
      <a href="${sourceName}">全体版を開く</a>
    </div>
  </section>

  <section class="doc-section">
    <h2>画面遷移図全体の概要</h2>
    <p>画面は「公開・エンドユーザー領域」「認証・共通領域」「プロジェクトワークスペース」「契約ワークスペース」の4範囲に整理しています。同じ画面でも操作権限が異なる場合は、ユーザー種別ごとにボタンや専用パネルを除外した版を掲載しています。</p>
    <p class="small">全画面を連続して確認する場合は <a href="${sourceName}">${sourceName}</a>、権限正本は <a href="02_基本設計/04_権限設計.md">02_基本設計/04_権限設計.md</a>、遷移正本は <a href="02_基本設計/01_画面設計.md">02_基本設計/01_画面設計.md</a> を参照してください。</p>
  </section>

  <section id="roles" class="index-cards">${cards}</section>

  <section class="doc-section" id="comparison">
    <h2>ユーザー種別ごとの利用範囲の比較</h2>
    <table class="role-table comparison">
      <thead><tr><th>機能領域</th><th>ウィジェット利用者</th><th>プロジェクトメンバー</th><th>プロジェクト管理者</th><th>オーナー</th></tr></thead>
      <tbody>${comparisonRows
        .map(
          (row) =>
            `<tr><td>${escapeHtml(row[0])}</td>${row
              .slice(1)
              .map(
                (cell) =>
                  `<td class="${markClass(cell)}">${escapeHtml(cell)}</td>`,
              )
              .join("")}</tr>`,
        )
        .join("")}</tbody>
    </table>
    <div class="small">凡例: ◎ 利用可 / △ 制限付き / × 利用不可</div>
  </section>

  <div class="doc-grid" id="common">
    <section class="doc-section">
      <h2>共通画面</h2>
      <ul class="plain-list">
        <li>全利用者共通: SCR-010 利用規約、SCR-020 プライバシーポリシー</li>
        <li>認証ユーザー共通: SCR-001 ログイン、SCR-003 パスワード再設定、SCR-011 / SCR-012 お知らせ、SCR-017 個人設定</li>
        <li>プロジェクト運用共通: SCR-008、SCR-005、SCR-006、SCR-007、SCR-021</li>
        <li>招待メンバー共通: SCR-018 アカウント有効化</li>
      </ul>
    </section>
    <section class="doc-section">
      <h2>専用・高権限画面</h2>
      <ul class="plain-list">
        <li>ウィジェット利用者専用: WIDGET</li>
        <li>プロジェクト管理者以上: SCR-009 / M1、SCR-021-M1</li>
        <li>オーナー専用: SCR-002 / SCR-013、SCR-004 / SCR-004-M1、SCR-014〜016、SCR-022〜026</li>
        <li>SCR-027: オーナーは編集・削除、プロジェクト管理者は参照のみ</li>
      </ul>
    </section>
  </div>

  <section class="doc-section">
    <h2>分類判断が必要な項目</h2>
    <table class="role-table">
      <thead><tr><th>項目</th><th>今回の分類</th><th>判断理由</th></tr></thead>
      <tbody>
        <tr><td>SCR-002 / SCR-013</td><td>オーナー</td><td>画面ヘッダは「管理者」表記ですが、画面設計の目的が「新規利用者(オーナー)」の登録と明記されているため。</td></tr>
        <tr><td>SCR-015 規約再同意</td><td>オーナー</td><td>既存ワイヤーフレームはオーナー / メンバー表記ですが、権限設計・要件・トレーサビリティでは契約判断としてオーナー専有のため。</td></tr>
        <tr><td>SCR-019 連絡先メール確認</td><td>オーナー / プロジェクト管理者の関連フロー</td><td>実操作者はアカウント不要のメール所有者ですが、設定と完了確認を行う管理ロール側にも必要なため。</td></tr>
        <tr><td>SCR-027 プロジェクト設定</td><td>管理者は参照、オーナーは編集・削除</td><td>既存ワイヤーフレームには編集操作がありますが、権限設計の正本を優先したため。</td></tr>
        <tr><td>SCR-010 / SCR-020</td><td>全4種別</td><td>認証不要URLが提供されるため、ウィジェット利用者にも公開閲覧版を含めたため。</td></tr>
      </tbody>
    </table>
  </section>

  <div class="wireframe-heading">
    <h2>既存の情報設計マップ</h2>
    <p>全体の契約・プロジェクト情報設計を確認するため、元資料のIAページを入口にも残しています。</p>
  </div>
  <div class="wireframe-stack">${iaBlock.html}</div>
</main>
<script>(function(){function r(){window.lucide&&lucide.createIcons({attrs:{'aria-hidden':'true',focusable:'false'}});}document.readyState==='loading'?document.addEventListener('DOMContentLoaded',r):r();})();</script>
</body>
</html>`;

  fs.writeFileSync(path.join(baseDir, indexFile), body);
}

for (const role of roles) {
  renderRolePage(role);
}
renderIndexPage();

const covered = new Set(roles.flatMap((role) => role.screens));
const sourceScreenIds = [...blocks.keys()].filter((id) => id !== "ia-v3");
const uncovered = sourceScreenIds.filter((id) => !covered.has(id));
if (uncovered.length) {
  throw new Error(`Unclassified source screens: ${uncovered.join(", ")}`);
}

console.log(
  [
    "Generated:",
    "  画面遷移図_index.html",
    ...roles.map((role) => `  ${role.file} (${role.screens.length} screens)`),
    `Covered source screens: ${sourceScreenIds.length}/${sourceScreenIds.length}`,
  ].join("\n"),
);
