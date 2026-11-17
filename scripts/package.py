#!/usr/bin/env python3
"""Build/verify an explicit-file, deterministic toolkit ZIP."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'docs/reference/memory.md',
    'memory_harness.py',
    'skills/workspace-memory/SKILL.md',
    'templates/memory/settings.json',
    'templates/memory/ignore',
    'templates/memory/remember-in-this-folder.md',
    'examples/memory/project.md',
    'examples/memory/decision.json',
    'tests/test_memory_harness.py',
    'docs/index.html',
    'docs/learn/advanced.md',
    'docs/learn/connections.md',
    'docs/learn/context.md',
    'docs/learn/skills.md',
    'docs/walkthrough.css',
    'docs/walkthrough.js',
    'examples/advanced/clasp-project.json',
    'examples/advanced/gcloud-project.ini',
    'kit.py',
    'skills/build-a-skill/SKILL.md',
    'skills/find-a-source/SKILL.md',
    'skills/review-a-plan/SKILL.md',
    'skills/write-a-brief/SKILL.md',
    'templates/context/PREFERENCES.md',
    'templates/context/PROJECT.md',
    'templates/reference-library/SOURCES.md',
    'templates/skill-starter/SKILL.md',
    '.github/workflows/test.yml',
    '.gitignore',
    'AGENTS.md',
    'CHANGELOG.md',
    'README.md',
    'START-HERE.md',
    'bootstrap.ps1',
    'bootstrap.sh',
    'config/defaults.json',
    'config/model-catalog.example.json',
    'docs/README.md',
    'docs/acceptance.md',
    'docs/architecture.md',
    'docs/distribution.md',
    'docs/everyday-use.md',
    'docs/extensions.md',
    'docs/hooks.md',
    'docs/maintenance.md',
    'docs/memory-and-references.md',
    'docs/models-and-cost.md',
    'docs/reference/commands.md',
    'docs/reference/configuration.md',
    'docs/reference/setup-for-claude.md',
    'docs/security.md',
    'docs/validation-2026-10-30.md',
    'examples/notes.md',
    'examples/task.json',
    'examples/workshop/AGENTS.md',
    'examples/workshop/CLAUDE.md',
    'examples/workshop/README.md',
    'examples/workshop/notes.md',
    'knowledge/starter-lessons.md',
    'manifest.json',
    'references/catalog.json',
    'scripts/package.py',
    'skills/harness/SKILL.md',
    'templates/CLAUDE.md',
    'templates/WORKSPACE.md',
    'templates/agents/implementer.md',
    'templates/agents/reviewer.md',
    'templates/agents/scout.md',
    'tests/test_core.py',
    'toolkit.py',
)


def source_files():
    paths = [ROOT / name for name in FILES]
    license_path = ROOT / 'LICENSE'
    if license_path.exists() or license_path.is_symlink():
        paths.append(license_path)
    for path in paths:
        relative_parents = [parent for parent in path.parents if parent != ROOT and parent.is_relative_to(ROOT)]
        if not path.is_file() or path.is_symlink() or any(parent.is_symlink() for parent in relative_parents):
            raise ValueError('unsafe-source')
    return sorted(paths)


def verify(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(set(names)) != len(names) or len(names) > 500:
            raise ValueError('duplicate-or-excessive-members')
        if sum(i.file_size for i in z.infolist()) > 5_000_000:
            raise ValueError('archive-too-large')
        for info in z.infolist():
            parts = PurePosixPath(info.filename).parts
            if not parts or info.filename.startswith('/') or '\\' in info.filename or ':' in info.filename or any(p in ('.', '..') or (p.startswith('.') and info.filename not in ('.gitignore', '.github/workflows/test.yml')) for p in parts):
                raise ValueError('unsafe-member')
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('linked-member')
        hashes = json.loads(z.read('SHA256SUMS.json'))
        if set(hashes) != set(names) - {'SHA256SUMS.json'}:
            raise ValueError('manifest-membership-mismatch')
        for name, expected in hashes.items():
            if hashlib.sha256(z.read(name)).hexdigest() != expected:
                raise ValueError('digest-mismatch')
    return {'status': 'verified', 'files': len(hashes), 'sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'authenticity': 'compare-out-of-band-digest'}


def build(output):
    output = Path(output).resolve()
    if output.is_relative_to(ROOT) or output.exists():
        raise ValueError('output-must-be-new-and-outside-source')
    data = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in source_files()}
    data['SHA256SUMS.json'] = (json.dumps({n: hashlib.sha256(b).hexdigest() for n, b in data.items()}, sort_keys=True, indent=2) + '\n').encode()
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        for name, body in sorted(data.items()):
            item = zipfile.ZipInfo(name, (2026, 10, 30, 0, 0, 0))
            item.external_attr = 0o100644 << 16
            item.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(item, body)
    return verify(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output'); group.add_argument('--verify')
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.verify) if args.verify else build(args.output), indent=2))
    except (OSError, ValueError, KeyError, zipfile.BadZipFile):
        print('Archive validation refused. Preserve the original and inspect selected inputs.', file=sys.stderr)
        raise SystemExit(2)
