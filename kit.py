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
}


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
        if target.exists():
            status = 'same' if target.is_file() and target.stat().st_size == len(body) and target.read_bytes() == body else 'conflict'
        plan['files'].append({'path': destination, 'status': status, 'sha256': toolkit.digest(body)})
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
        children = []
        for row in plan['files']:
            if row['status'] == 'same':
                continue
            target = toolkit.safe_path(root, row['path'])
            body = preset_bytes(preset, PRESETS[preset][row['path']])
            if toolkit.digest(body) != row['sha256']:
                raise toolkit.HarnessError('preset-source-changed')
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(body)
            children.append(row['path'])
    return {'status': 'copied', 'files_added': children, 'client_loaded': 'not-checked'}


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
