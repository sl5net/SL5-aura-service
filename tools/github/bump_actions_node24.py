#!/usr/bin/env python3
"""
bump_actions_node24.py

Scans GitHub Actions workflow files for `uses:` references to JavaScript
actions that still declare Node.js 20 (or older) in their action.yml, and
proposes (or applies) the *smallest* version bump that already ships with
Node.js 24 support.

Everything else is left alone:
  - actions already on node24+           -> untouched
  - composite / docker actions            -> untouched (not affected)
  - local actions (./path/to/action)      -> untouched
  - reusable workflow calls (…/.github/workflows/x.yml@ref) -> untouched
  - actions where no safe minimal bump could be determined  -> reported,
    not changed automatically (needs a human look)

For each action reference it queries GitHub directly (no local guessing):
  - `git ls-remote --tags` to get the real list of released tags
  - raw.githubusercontent.com to read the actual action.yml `runs.using`
    field for the current pin AND for candidate newer tags, ascending,
    stopping at the first one that already supports Node 24.

Usage:
    python3 bump_actions_node24.py                    # dry run, report only
    python3 bump_actions_node24.py --apply             # write the changes
    python3 bump_actions_node24.py --workflows-dir .github/workflows --apply
    python3 bump_actions_node24.py --verbose            # also show untouched actions

Requirements: Python 3.8+, git, and outbound access to
              github.com / raw.githubusercontent.com. No pip packages needed.
"""

import argparse
import re
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

USES_RE = re.compile(
    r'^(?P<prefix>\s*(?:-\s+)?uses:\s*[\'"]?)'
    r'(?P<action>[A-Za-z0-9_.-]+/[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-/]+)?)'
    r'@(?P<ref>[A-Za-z0-9._-]+)'
    r'(?P<quote>[\'"]?)'
    r'(?P<comment>\s*#.*)?'
    r'\s*$'
)
SHA_RE = re.compile(r'^[0-9a-f]{40}$')
VERSION_TAG_RE = re.compile(r'^v?(\d+)(?:\.(\d+))?(?:\.(\d+))?$')
USING_RE = re.compile(r'^\s*using:\s*[\'"]?(node\d+|composite|docker)[\'"]?', re.MULTILINE)


def find_workflow_files(workflows_dir: Path):
    return sorted(list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml')))


def parse_action_ref(action_ref: str):
    """owner/repo[/subpath] -> (owner, repo, subpath or '')"""
    parts = action_ref.split('/')
    owner, repo = parts[0], parts[1]
    subpath = '/'.join(parts[2:]) if len(parts) > 2 else ''
    return owner, repo, subpath


def is_skippable(action_ref: str, raw_uses_value: str) -> bool:
    if action_ref.startswith('.'):
        return True  # local action, e.g. ./.github/actions/foo
    if raw_uses_value.startswith('docker://'):
        return True  # direct docker image reference
    if re.search(r'\.ya?ml$', action_ref):
        return True  # reusable workflow call (owner/repo/.github/workflows/x.yml@ref)
    return False


def http_get(url: str, timeout=10):
    req = urllib.request.Request(url, headers={'User-Agent': 'bump-actions-node24-script'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except urllib.error.URLError:
        return None


def fetch_manifest(owner, repo, subpath, ref):
    base = f'https://raw.githubusercontent.com/{owner}/{repo}/{ref}/'
    if subpath:
        base += subpath.rstrip('/') + '/'
    for fname in ('action.yml', 'action.yaml'):
        text = http_get(base + fname)
        if text is not None:
            return text
    return None


def get_using(manifest_text):
    if manifest_text is None:
        return None
    m = USING_RE.search(manifest_text)
    return m.group(1) if m else None


def node_version_num(using):
    if using and using.startswith('node'):
        try:
            return int(using[4:])
        except ValueError:
            return None
    return None


def version_key(tag):
    m = VERSION_TAG_RE.match(tag)
    major = int(m.group(1))
    minor = int(m.group(2)) if m.group(2) else 0
    patch = int(m.group(3)) if m.group(3) else 0
    return (major, minor, patch)


def list_tags(owner, repo, cache={}):
    """tag_name -> commit_sha (peeled to the real commit where possible),
    plus the subset of tag names that parse as release versions, sorted."""
    key = (owner, repo)
    if key in cache:
        return cache[key]

    url = f'https://github.com/{owner}/{repo}.git'
    try:
        out = subprocess.run(
            ['git', 'ls-remote', '--tags', url],
            capture_output=True, text=True, timeout=20, check=True
        ).stdout
    except Exception:
        cache[key] = ({}, [])
        return cache[key]

    raw = {}
    for line in out.splitlines():
        if not line.strip() or '\t' not in line:
            continue
        sha, ref = line.split('\t')
        tag = ref.replace('refs/tags/', '')
        if tag.endswith('^{}'):
            raw[tag[:-3]] = sha  # peeled annotated tag -> real commit, overwrite
        else:
            raw.setdefault(tag, sha)

    def sort_key(tag):
        is_full = re.match(r'^v?\d+\.\d+\.\d+$', tag) is not None
        return version_key(tag) + (0 if is_full else 1,)  # ties: full x.y.z before bare major

    versioned = [(t, sort_key(t)) for t in raw if VERSION_TAG_RE.match(t)]
    versioned.sort(key=lambda x: x[1])
    ordered_tags = [t for t, _ in versioned]
    cache[key] = (raw, ordered_tags)
    return cache[key]


def find_anchor_version(tags_sha, current_ref):
    """Which release does the currently pinned ref correspond to?"""
    if VERSION_TAG_RE.match(current_ref):
        return current_ref
    if SHA_RE.match(current_ref.lower()):
        matches = [t for t, sha in tags_sha.items()
                   if sha.lower() == current_ref.lower() and VERSION_TAG_RE.match(t)]
        if matches:
            matches.sort(key=len, reverse=True)  # prefer the most specific tag name
            return matches[0]
    return None


def find_minimal_fix(owner, repo, subpath, current_ref):
    tags_sha, ordered_tags = list_tags(owner, repo)
    if not ordered_tags:
        return None, 'no release tags found on remote'

    anchor = find_anchor_version(tags_sha, current_ref)
    if anchor is None:
        candidates = ordered_tags  # unknown anchor: consider every tag, ascending
    else:
        akey = version_key(anchor)
        candidates = [t for t in ordered_tags if version_key(t) > akey]

    for tag in candidates[:25]:
        using = get_using(fetch_manifest(owner, repo, subpath, tag))
        nv = node_version_num(using)
        if nv is not None and nv >= 24:
            return tag, tags_sha.get(tag)
    return None, 'no released tag with node24 support found yet'


def choose_replacement(current_ref, target_tag, tags_sha):
    """Match the granularity of the original pin: SHA -> SHA, bare major -> bare major, else full tag."""
    if SHA_RE.match(current_ref.lower()):
        return tags_sha.get(target_tag, target_tag), target_tag
    if re.match(r'^v?\d+$', current_ref):
        major = version_key(target_tag)[0]
        bare = f'v{major}'
        if bare in tags_sha:
            return bare, None
    return target_tag, None


def process(workflows_dir: Path, apply: bool, verbose: bool):
    files = find_workflow_files(workflows_dir)
    if not files:
        print(f'No workflow files found under {workflows_dir}')
        return

    occurrences = []
    for f in files:
        for line in f.read_text().splitlines():
            m = USES_RE.match(line)
            if not m:
                continue
            action_ref, ref = m.group('action'), m.group('ref')
            if is_skippable(action_ref, f'{action_ref}@{ref}'):
                continue
            occurrences.append((action_ref, ref))

    unique = sorted(set(occurrences))
    decisions = {}

    for action_ref, ref in unique:
        owner, repo, subpath = parse_action_ref(action_ref)
        current_using = get_using(fetch_manifest(owner, repo, subpath, ref))

        if current_using is None:
            decisions[(action_ref, ref)] = {'status': 'skip', 'reason': 'no action.yml found at that ref/path'}
            continue
        if current_using in ('composite', 'docker'):
            decisions[(action_ref, ref)] = {'status': 'skip', 'reason': f'using: {current_using} (not affected)'}
            continue
        nv = node_version_num(current_using)
        if nv is not None and nv >= 24:
            decisions[(action_ref, ref)] = {'status': 'ok', 'reason': f'already {current_using}'}
            continue

        target_tag, tag_sha_or_err = find_minimal_fix(owner, repo, subpath, ref)
        if target_tag is None:
            decisions[(action_ref, ref)] = {
                'status': 'manual',
                'reason': f'currently {current_using}; {tag_sha_or_err}'
            }
            continue

        tags_sha, _ = list_tags(owner, repo)
        new_value, comment_tag = choose_replacement(ref, target_tag, tags_sha)
        decisions[(action_ref, ref)] = {
            'status': 'bump', 'from_using': current_using,
            'new_value': new_value, 'comment_tag': comment_tag,
        }

    print(f'\nChecked {len(unique)} unique action reference(s) across {len(files)} workflow file(s).\n')
    bumps = {k: v for k, v in decisions.items() if v['status'] == 'bump'}
    manual = {k: v for k, v in decisions.items() if v['status'] == 'manual'}
    ok = {k: v for k, v in decisions.items() if v['status'] == 'ok'}
    skip = {k: v for k, v in decisions.items() if v['status'] == 'skip'}

    if bumps:
        print('Will bump:')
        for (action_ref, ref), d in bumps.items():
            suffix = f'   # {d["comment_tag"]}' if d['comment_tag'] else ''
            print(f'  {action_ref}@{ref}  ({d["from_using"]})  ->  {action_ref}@{d["new_value"]}{suffix}')
    if manual:
        print('\nNeeds manual attention (no safe automatic fix found):')
        for (action_ref, ref), d in manual.items():
            print(f'  {action_ref}@{ref}: {d["reason"]}')
    if verbose and ok:
        print('\nAlready fine:')
        for (action_ref, ref), d in ok.items():
            print(f'  {action_ref}@{ref}: {d["reason"]}')
    if verbose and skip:
        print('\nSkipped (not a versioned JS action):')
        for (action_ref, ref), d in skip.items():
            print(f'  {action_ref}@{ref}: {d["reason"]}')

    if not bumps:
        print('\nNothing to change.')
        return

    if not apply:
        print('\nDry run only -- re-run with --apply to write these changes.')
        return

    changed_files = set()
    for f in files:
        lines = f.read_text().splitlines()
        new_lines = []
        file_changed = False
        for line in lines:
            m = USES_RE.match(line)
            if m:
                key = (m.group('action'), m.group('ref'))
                if key in bumps:
                    d = bumps[key]
                    if d['comment_tag']:
                        orig = m.group('comment')
                        leading_ws = re.match(r'\s*', orig).group(0) if orig else '  '
                        comment = f'{leading_ws}# {d["comment_tag"]}'
                    else:
                        comment = m.group('comment') or ''
                    new_line = f'{m.group("prefix")}{key[0]}@{d["new_value"]}{m.group("quote") or ""}{comment}'
                    new_lines.append(new_line)
                    file_changed = True
                    continue
            new_lines.append(line)
        if file_changed:
            f.write_text('\n'.join(new_lines) + '\n')
            changed_files.add(f)

    print(f'\nApplied changes to {len(changed_files)} file(s):')
    for f in sorted(changed_files):
        print(f'  {f}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--workflows-dir', default='.github/workflows', type=Path)
    ap.add_argument('--apply', action='store_true', help='Write changes (default: dry run / report only)')
    ap.add_argument('--verbose', action='store_true', help='Also list actions that need no change')
    args = ap.parse_args()

    if not args.workflows_dir.is_dir():
        print(f'Workflows directory not found: {args.workflows_dir}', file=sys.stderr)
        sys.exit(1)

    process(args.workflows_dir, args.apply, args.verbose)


if __name__ == '__main__':
    main()
