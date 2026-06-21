#!/usr/bin/env python3
"""P4 repo-wide reference rewrite: old API IDs -> new flat API IDs.

Handles, in order, per file:
  1. Links/paths to old group files with an endpoint anchor:
       <p>/API-<word>.md#API-<XXX>-<NNN>  ->  <p>/API-<NNN>.md#API-<NNN>
     (both ](...) and href="..." forms). New file derived from the anchor.
  2. The anchorless API-common.md link -> index.md#conv (API 共通仕様).
  3. Bare textual IDs:  API-<XXX>-<NNN>  ->  API-<NNN>.

Scope: 01_requirements, 02_basic_design, 03_future, README.md.
Excludes: 99_management, CLAUDE.md, _build, and 03_apis/ files already
emitted with new IDs (they contain only new IDs / old-ID provenance in 備考,
which we DO convert too — but those are handled by leaving 03_apis alone here
because the split script already wrote final content; we still rewrite any
stray old IDs there for safety).
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
apimap = json.load(open(os.path.join(ROOT, '99_management/crosswalk.json'), encoding='utf-8'))['apimap']

# group word -> not needed; we map via the anchor's old ID.
OLD_ID_RE = re.compile(r'API-[A-Z]+-\d+')

def new_id(old):
    return apimap[old]

def rewrite(text):
    # 1. links with group file + endpoint anchor (markdown and href)
    def repl_link(m):
        path_prefix = m.group('pre')   # e.g. ../03_apis/  or 02_basic_design/03_apis/
        old = m.group('old')
        nid = new_id(old)
        return f'{path_prefix}{nid}.md#{nid}'
    # pattern: (prefix)API-<word>.md#API-<XXX>-<NNN>
    text = re.sub(
        r'(?P<pre>(?:\.\./)*(?:[0-9A-Za-z_./]*?03_apis/))API-[a-z]+\.md#(?P<old>API-[A-Z]+-\d+)',
        repl_link, text)

    # 2. anchorless API-common.md -> index.md#conv
    text = re.sub(
        r'((?:\.\./)*(?:[0-9A-Za-z_./]*?03_apis/))API-common\.md',
        r'\1index.md#conv', text)

    # 3. bare textual old IDs -> new flat IDs
    def repl_bare(m):
        return new_id(m.group(0))
    text = OLD_ID_RE.sub(repl_bare, text)
    return text

def target_files():
    pats = [
        '01_requirements/**/*.md',
        '02_basic_design/**/*.md',
        '03_future/**/*.md',
    ]
    files = []
    for pat in pats:
        files += glob.glob(os.path.join(ROOT, pat), recursive=True)
    files.append(os.path.join(ROOT, 'README.md'))
    # NOTE: 03_apis/API-<NNN>.md are included. Their <span id> / links already
    # use new flat IDs (API-001 form, which the OLD_ID_RE does not match), so
    # only stray body-text cross-references (e.g. "API-AUTH-005 で取得") are
    # rewritten to their new flat IDs. index.md is also safe (new IDs only).
    return sorted(set(files))

def main():
    changed = 0
    for f in target_files():
        s = open(f, encoding='utf-8').read()
        n = rewrite(s)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n)
            changed += 1
    print('files changed:', changed)

if __name__ == '__main__':
    main()
