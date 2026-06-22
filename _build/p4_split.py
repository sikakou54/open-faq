#!/usr/bin/env python3
"""P4 API split + flat renumber.

Splits each endpoint section of the 14 group files under
02_basic_design/03_apis/API-*.md into one file per endpoint
(API-001.md .. API-059.md) with the §8-3 skeleton, renaming the
old category ID (API-AUTH-001 ...) to the flat ID (API-001 ...)
via crosswalk.json:apimap.

Reverse-lookups (対応業務UC / 対応画面ID / 対応画面イベントID) come from
_build/p4_reverse.json (built by p4_reverse.py).

Deterministic & idempotent. Writes API-<NNN>.md files; deletion of the
old group files is done by the caller after this script succeeds.
"""
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APIDIR = os.path.join(ROOT, '02_basic_design/03_apis')

apimap = json.load(open(os.path.join(ROOT, '99_management/crosswalk.json'), encoding='utf-8'))['apimap']
rev = json.load(open(os.path.join(ROOT, '_build/p4_reverse.json'), encoding='utf-8'))

# TBL name -> file (old TBL ids still in place; do NOT rename TBL).
# Build from index links already present.
TBL_FILE = {}
idx = open(os.path.join(APIDIR, 'index.md'), encoding='utf-8').read()
for m in re.finditer(r'\[`([A-Z_]+)`\]\(\.\./04_database/(TBL-[A-Z]+-\d+)\.md\)', idx):
    TBL_FILE[m.group(1)] = m.group(2)

GROUP_FILES = sorted(glob.glob(os.path.join(APIDIR, 'API-*.md')))


def split_sections(body, level):
    """Split markdown text into (heading_text, content) by ATX heading `level`.
    Returns list of (title_without_marker, raw_block_including_heading)."""
    pat = re.compile(r'^' + '#' * level + r' (.*)$', re.M)
    out = []
    matches = list(pat.finditer(body))
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        title = re.sub(r'<span id="[^"]*"></span>', '', m.group(1)).strip()
        out.append((title, body[start:end]))
    return out


def strip_heading(block):
    """Drop the first line (the heading) and return the remaining content."""
    return block.split('\n', 1)[1] if '\n' in block else ''


def parse_basic_info(block):
    """Parse the 基本情報 table -> dict of field->value."""
    d = {}
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith('|'):
            continue
        parts = [p.strip() for p in s.strip().strip('|').split('|')]
        if len(parts) == 2 and parts[0] not in ('項目', '---', ':---', '----'):
            if set(parts[0]) <= set('-: '):
                continue
            d[parts[0]] = parts[1]
    return d


def parse_io_tables(block):
    """Return ordered unique table names from one or more I/O CRUD tables."""
    names = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith('|'):
            continue
        m = re.match(r'\|\s*`([A-Z_]+)`\s*\|', s)
        if m:
            n = m.group(1)
            if n not in names:
                names.append(n)
    return names


def crud_for(block):
    """Map table -> CRUD string from an I/O table block."""
    out = {}
    for line in block.splitlines():
        s = line.strip()
        m = re.match(r'\|\s*`([A-Z_]+)`\s*\|(.*)\|?$', s)
        if not m:
            continue
        cells = [c.strip() for c in s.strip().strip('|').split('|')]
        # cells[0] = `NAME`, next four are C R U D
        flags = cells[1:5]
        crud = ''
        for letter, val in zip('CRUD', flags):
            crud += letter if val in ('◯', '○', '◯') else '-'
        out[m.group(1)] = crud
    return out


def reverse_block(old_id):
    info = rev.get(old_id, {"evts": [], "scrs": [], "ucs": []})
    ucs = info["ucs"]
    scrs = info["scrs"]
    evts = info["evts"]
    if ucs:
        uc_links = ' ・ '.join(
            f'[{u}](../../01_requirements/02_business_usecases/{u}.md#{u})' for u in ucs)
    else:
        uc_links = '—'
    if scrs:
        scr_links = ' ・ '.join(
            f'[{s}](../01_screens/{s}.md#{s})' for s in scrs)
    else:
        scr_links = '—'
    if evts:
        evt_links = ' ・ '.join(
            f'[{e}](../02_screen_events/{e}.md#{e})' for e in evts)
    else:
        evt_links = '—'
    return uc_links, scr_links, evt_links


def build_file(old_id, new_id, section_body, name_jp):
    secs = dict((t, b) for t, b in split_sections(section_body, 3))
    basic = parse_basic_info(secs.get('基本情報', ''))
    endpoint = basic.get('エンドポイント', '—')
    method = basic.get('HTTP メソッド', basic.get('HTTPメソッド', '—'))
    auth = basic.get('認証', '—')
    authz = basic.get('権限', basic.get('認可', '—'))

    uc_links, scr_links, evt_links = reverse_block(old_id)

    # I/O tables -> 利用テーブル
    io_block = secs.get('I/O', '')
    crud = crud_for(io_block)
    tbl_lines = []
    for n in parse_io_tables(io_block):
        file = TBL_FILE.get(n)
        c = crud.get(n, '')
        # NOTE: TBL files do not yet carry `<span id="TBL-...">` anchors
        # (added in P5). Link without a fragment to keep anchors resolvable.
        if file:
            tbl_lines.append(f'| [`{n}`](../04_database/{file}.md) | `{c}` |')
        else:
            tbl_lines.append(f'| `{n}` | `{c}` |')

    # preamble = content between the H2 endpoint heading and the first H3
    first_h3 = re.search(r'^### ', section_body, re.M)
    pre = ''
    if first_h3:
        pre_raw = section_body[:first_h3.start()]
        # drop the H2 heading line itself
        pre = '\n'.join(pre_raw.split('\n')[1:]).strip()

    parts = []
    parts.append(f'# <span id="{new_id}"></span>{new_id}: {name_jp}\n')
    # summary from 処理概要 lead (first non-empty paragraph line)
    proc = secs.get('処理概要', '')
    lead = ''
    for line in strip_heading(proc).splitlines():
        t = line.strip()
        if t and not t.startswith('|'):
            lead = t
            break
    if not lead and pre:
        for line in pre.splitlines():
            t = line.strip()
            if t and not t.startswith(('|', '```', 'export', 'import')):
                lead = t
                break
    if not lead:
        lead = f'{name_jp} の処理を担う。'
    lead = lead.rstrip('。')
    parts.append(f'> **このページは {name_jp} API の契約を定義します。** {lead}。\n')
    parts.append('*版数 v2.0 ・ 更新 2026-06-21 ・ 再構成 P4*\n')

    # 項目表
    parts.append('## 項目\n')
    parts.append('| 項目 | 内容 |')
    parts.append('|---|---|')
    parts.append(f'| API ID | `{new_id}` |')
    parts.append(f'| API名 | {name_jp} |')
    parts.append(f'| 対応業務UC | {uc_links} |')
    parts.append(f'| 対応画面ID | {scr_links} |')
    parts.append(f'| 対応画面イベントID | {evt_links} |')
    parts.append(f'| エンドポイント | {endpoint} |')
    parts.append(f'| HTTPメソッド | {method} |')
    parts.append(f'| 認証 | {auth} |')
    parts.append(f'| 認可 | {authz} |')
    parts.append('')

    # 処理概要 (keep)
    if proc.strip():
        parts.append('## 処理概要\n')
        parts.append(strip_heading(proc).strip() + '\n')

    # インターフェース定義 (preamble code block for IF-style APIs: AI / メール)
    if pre and '```' in pre:
        parts.append('## インターフェース定義\n')
        parts.append(pre + '\n')

    # リクエスト (リクエストパラメータ -> ## リクエスト)
    req = secs.get('リクエストパラメータ', '')
    parts.append('## リクエスト\n')
    if req.strip():
        parts.append(strip_heading(req).strip() + '\n')
    else:
        parts.append('本 API はリクエストボディ・パラメータを持たない。\n')

    # レスポンス (any レスポンス(*) section)
    resp_blocks = [b for t, b in split_sections(section_body, 3) if t.startswith('レスポンス')]
    parts.append('## レスポンス\n')
    if resp_blocks:
        for b in resp_blocks:
            # convert ### レスポンス(200) heading into a bold status label
            lines = b.split('\n', 1)
            head = re.sub(r'^###\s*', '', lines[0]).strip()
            rest = lines[1] if len(lines) > 1 else ''
            parts.append(f'**{head}**\n')
            parts.append(rest.strip() + '\n')
    else:
        parts.append('本 API の戻り値は本文の型定義を参照する。\n')

    # バリデーション: extract from request body if a バリデーション list exists, else reference
    val_text = extract_validation(req)
    parts.append('## バリデーション\n')
    if val_text:
        parts.append(val_text + '\n')
    else:
        parts.append('入力値の検証規則は `## リクエスト` の各パラメータ説明を参照する。\n')

    # エラー
    err = secs.get('エラー', '')
    parts.append('## エラー\n')
    if err.strip():
        parts.append(strip_heading(err).strip() + '\n')
    else:
        parts.append('本 API 固有のエラーコードはない([API 共通仕様](index.md#conv) の標準エラー体系に従う)。\n')

    # 利用テーブル
    parts.append('## 利用テーブル\n')
    if tbl_lines:
        parts.append('本 API が参照・更新するテーブルと CRUD 区分。\n')
        parts.append('| テーブル | CRUD |')
        parts.append('|---|---|')
        parts.extend(tbl_lines)
        parts.append('')
    else:
        parts.append('本 API はテーブルを直接読み書きしない(外部サービス連携 IF)。\n')

    # 備考
    grp = old_id.split('-')[1]  # AUTH / PRJ / ... (former category, no numeric old ID)
    parts.append('## 備考\n')
    parts.append(f'再構成 P4 で旧グループ別 API 設計(旧カテゴリ `{grp}`)から導出し、'
                 '1 エンドポイント = 1 ファイルへフラット採番。'
                 '旧 ID との対応は [crosswalk](../../99_management/crosswalk.json) を正本とする。')
    parts.append('')

    nav_top = ('<!-- portal-top -->\n'
               f'[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [API設計](index.md) ／ **{new_id}: {name_jp}**\n'
               '<!-- /portal-top -->\n\n')
    nav_bottom = ('\n---\n\n<!-- portal-bottom -->\n'
                  '[← API設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)\n'
                  '<!-- /portal-bottom -->\n')
    return nav_top + '\n'.join(parts).rstrip() + '\n' + nav_bottom


def extract_validation(req_block):
    """Pull a 'バリデーション:' bullet list out of the request block if present."""
    lines = strip_heading(req_block).splitlines() if req_block else []
    out = []
    capture = False
    for line in lines:
        s = line.strip()
        if s.startswith('バリデーション'):
            capture = True
            continue
        if capture:
            if s.startswith('- ') or s.startswith('* '):
                out.append(line)
            elif s == '':
                if out:
                    continue
            else:
                break
    return '\n'.join(out).strip()


def main():
    written = []
    for gf in GROUP_FILES:
        if os.path.basename(gf) == 'index.md':
            continue
        text = open(gf, encoding='utf-8').read()
        # endpoint sections: ## <span id="API-XXX-NNN"></span>API-XXX-NNN <name>
        pat = re.compile(r'^## <span id="(API-[A-Z]+-\d+)"></span>(API-[A-Z]+-\d+)\s+(.*)$', re.M)
        matches = list(pat.finditer(text))
        for i, m in enumerate(matches):
            old_id = m.group(1)
            name_jp = m.group(3).strip()
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else None
            # stop at portal-bottom / trailing --- if last
            if end is None:
                pb = text.find('<!-- portal-bottom -->', start)
                tail = text.rfind('\n---\n', start, pb if pb > 0 else len(text))
                end = tail if tail > start else (pb if pb > 0 else len(text))
            section = text[start:end]
            new_id = apimap[old_id]
            content = build_file(old_id, new_id, section, name_jp)
            dest = os.path.join(APIDIR, f'{new_id}.md')
            open(dest, 'w', encoding='utf-8').write(content)
            written.append((old_id, new_id, name_jp))
    written.sort(key=lambda x: x[1])
    for o, n, nm in written:
        print(f'{o} -> {n}  {nm}')
    print('total endpoint files:', len(written))


if __name__ == '__main__':
    main()
