#!/usr/bin/env python3
"""Optional local setup and project checks for the Agent Harness Toolkit."""

import argparse
import configparser
from pathlib import Path
import re
import shutil
import sys

import toolkit


SKILLS = ('write-a-brief', 'find-a-source', 'review-a-plan', 'build-a-skill')
PRESETS = {
    **{name: {f'.claude/skills/{name}/SKILL.md': f'skills/{name}/SKILL.md'} for name in SKILLS},
    'context': {
        'context/PROJECT.md': 'templates/context/PROJECT.md',
        'context/PREFERENCES.md': 'templates/context/PREFERENCES.md',
    },
    'references': {'reference-library/SOURCES.md': 'templates/reference-library/SOURCES.md'},
    'memory': {'.harness/config.json': 'config/defaults.json'},
    'memory-harness': {
        '.harness/memory-harness.json': 'templates/memory/settings.json',
        '.harness/.gitignore': 'templates/memory/ignore',
        '.harness/memory-tools/memory_harness.py': 'memory_harness.py',
        '.harness/memory-tools/toolkit.py': 'toolkit.py',
        '.claude/skills/workspace-memory/SKILL.md': 'skills/workspace-memory/SKILL.md',
        '.claude/rules/toolkit-memory.md': 'templates/memory/remember-in-this-folder.md',
    },
}


# These digests identify the untouched files in the verified 1.2.0 ZIP.
MEMORY_120 = {
    '.harness/memory-tools/memory_harness.py': '7220a235181965770647bbaa978a4efd1d1ce0454cea34f6559d7f23b4c39034',
    '.harness/memory-tools/memory_semantic.py': '0f44d05fc1acc51fc39f07631661c54fe0042db8a98f26961859b4e0f548c9ce',
    '.harness/memory-tools/toolkit.py': '9d9e550e7b0bb4d59bf6b2778b0e3b523a8e2f58ca84439d5f359a35103d4c8f',
    '.claude/skills/workspace-memory/SKILL.md': '70cc98562cc0a33ab20f23cb4d2c8091755bad8b03168dd05fa4595144d4c1d4',
}


MEMORY_121 = {
    '.harness/memory-tools/memory_harness.py': 'ae57459454dd0b71181f5684df28d301afb962d03ba57cb59f928d1755233b7f',
    '.harness/memory-tools/memory_semantic.py': 'bef8bb49b931277f254137aa49d801a9881b085b76f80e91d1f2b6ed773d0f50',
    '.harness/memory-tools/toolkit.py': 'd7b0db9bd3ad17d298140b418f44ce504445aa512cbcaae375bf7cbfcb68bd19',
    '.claude/skills/workspace-memory/SKILL.md': '413ce0b971f67ca957fb184a8b5d7b6b8fe27c7c38685e3c68ff63be54db7d21',
}
MEMORY_122 = {
    '.claude/skills/workspace-memory/SKILL.md': '45a55814d46ac0fc2b585edcc4159bf7eb616ef5ee9c7c93de119f3ee8e28e87',
    '.claude/rules/toolkit-memory.md': '731584fb0ca871ab606ead6f7236ef54d928b6776ad9c6bea41010a8dd42c737',
}
RETIRED_MEMORY_FILE = '.harness/memory-tools/memory_semantic.py'


def shipped_memory_file(path, digest):
    return digest in (MEMORY_120.get(path), MEMORY_121.get(path), MEMORY_122.get(path))


def preset_bytes(preset, source):
    path = toolkit.safe_path(toolkit.ROOT, source)
    if preset == 'memory':
        config = toolkit.read_json(path)
        config['memory']['enabled'] = True
        return toolkit.encode(config)
    return path.read_bytes()


def prepare(root, preset):
    plan = {'version': toolkit.VERSION, 'workspace': str(root), 'preset': preset, 'files': []}
    for destination, source in PRESETS[preset].items():
        target = toolkit.safe_path(root, destination)
        body = preset_bytes(preset, source)
        status = 'add'
        original = None
        if target.exists():
            status = 'conflict'
            if target.is_file() and target.stat().st_size <= 1_000_000:
                original = toolkit.digest(target.read_bytes())
                if original == toolkit.digest(body):
                    status = 'same'
                elif preset == 'memory-harness' and shipped_memory_file(destination, original):
                    status = 'update'
        item = {'path': destination, 'status': status, 'sha256': toolkit.digest(body)}
        if status == 'update':
            item['previous_sha256'] = original
        plan['files'].append(item)
    if preset == 'memory-harness':
        retired = toolkit.safe_path(root, RETIRED_MEMORY_FILE)
        if retired.exists():
            digest = toolkit.digest(retired.read_bytes()) if retired.is_file() and retired.stat().st_size <= 1_000_000 else None
            status = 'remove' if digest and shipped_memory_file(RETIRED_MEMORY_FILE, digest) else 'keep-edited'
            plan['files'].append({'path': RETIRED_MEMORY_FILE, 'status': status, 'previous_sha256': digest})
    return plan


def add(root, preset, binding=None):
    if not root.is_dir():
        raise toolkit.HarnessError('choose-an-existing-workspace-folder')
    plan = prepare(root, preset)
    review = toolkit.digest(toolkit.encode(plan))
    if binding is None:
        return dict(plan, status='preview', plan_sha256=review)
    if review != binding:
        raise toolkit.HarnessError('setup-plan-changed')
    if any(row['status'] == 'conflict' for row in plan['files']):
        raise toolkit.HarnessError('existing-files: review and preserve them')
    with toolkit.lock(root):
        if prepare(root, preset) != plan:
            raise toolkit.HarnessError('setup-plan-changed')
        children, updated, removed, kept = [], [], [], []
        for row in plan['files']:
            if row['status'] == 'same':
                continue
            if row['status'] == 'keep-edited':
                kept.append(row['path'])
                continue
            target = toolkit.safe_path(root, row['path'])
            if row['status'] == 'remove':
                if toolkit.digest(target.read_bytes()) != row['previous_sha256']:
                    raise toolkit.HarnessError('setup-plan-changed')
                target.unlink()
                removed.append(row['path'])
                continue
            body = preset_bytes(preset, PRESETS[preset][row['path']])
            if toolkit.digest(body) != row['sha256']:
                raise toolkit.HarnessError('preset-source-changed')
            target.parent.mkdir(parents=True, exist_ok=True)
            if row['status'] == 'update':
                if toolkit.digest(target.read_bytes()) != row['previous_sha256']:
                    raise toolkit.HarnessError('setup-plan-changed')
                toolkit.atomic_write(target, body)
                updated.append(row['path'])
            else:
                with target.open('xb') as stream:
                    stream.write(body)
                children.append(row['path'])
    return {'status': 'copied', 'files_added': children, 'files_updated': updated,
            'files_removed': removed, 'files_kept_edited': kept, 'client_loaded': 'not-checked'}


def project_check(root, tool, relative_file, expected):
    path = toolkit.safe_path(root, relative_file)
    if not path.is_file() or path.stat().st_size > 65536:
        raise toolkit.HarnessError('choose-a-small-local-project-file')
    if tool == 'clasp':
        project = toolkit.read_json(path).get('scriptId')
    else:
        config = configparser.ConfigParser(interpolation=None)
        config.read_string(path.read_text(encoding='utf-8'))
        project = config.get('core', 'project', fallback=None)
    matched = isinstance(project, str) and project == expected
    return {'tool': tool, 'tool_on_path': shutil.which(tool) is not None,
            'project_match': matched, 'account': 'not-checked',
            'billing': 'local-only', 'network_calls': 0}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', default='.')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    add_parser = sub.add_parser('add')
    add_parser.add_argument('preset', choices=PRESETS)
    add_parser.add_argument('--apply-plan')
    sub.add_parser('memory-status')
    check = sub.add_parser('check-project')
    check.add_argument('tool', choices=('clasp', 'gcloud'))
    check.add_argument('--file', required=True)
    check.add_argument('--expected', required=True)
    args = parser.parse_args(argv)
    try:
        root = Path(args.workspace).absolute()
        if args.command == 'list':
            result = {'presets': list(PRESETS), 'billing': 'local-only'}
        elif args.command == 'add':
            result = add(root, args.preset, args.apply_plan)
        elif args.command == 'memory-status':
            result = {'enabled': toolkit.config(root)['memory']['enabled'],
                      'storage': 'workspace/.harness/memory.sqlite3 (plaintext)',
                      'store_exists': toolkit.state_path(root, 'memory.sqlite3').is_file()}
        else:
            if not re.fullmatch(r'[A-Za-z0-9_-]{1,200}', args.expected):
                raise toolkit.HarnessError('invalid-project-id')
            result = project_check(root, args.tool, args.file, args.expected)
        print(toolkit.encode(result).decode(), end='')
        return 1 if result.get('project_match') is False else 0
    except toolkit.HarnessError as error:
        print(toolkit.encode({'status': 'refused', 'reason': str(error)}).decode(), file=sys.stderr, end='')
    except (OSError, ValueError, KeyError, TypeError, AttributeError, configparser.Error):
        print('Could not read the selected workspace or project file.', file=sys.stderr)
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
