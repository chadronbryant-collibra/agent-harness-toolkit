#!/usr/bin/env python3
"""Build/verify an explicit-file, deterministic private colleague ZIP."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ['.gitignore', 'AGENTS.md', 'README.md', 'START-HERE.md', 'CHANGELOG.md', 'manifest.json',
         'toolkit.py', 'bootstrap.ps1', 'bootstrap.sh']
TREES = ['config', 'templates', 'docs', 'skills', 'knowledge', 'examples', 'references', 'tests', 'scripts']


def source_files():
    paths = [ROOT / name for name in FILES]
    for tree in TREES:
        paths.extend(p for p in (ROOT / tree).rglob('*') if p.is_file() and p.suffix in ('.py', '.md', '.json'))
    for p in paths:
        if p.is_symlink() or (p.name != '.gitignore' and any(part.startswith('.') for part in p.relative_to(ROOT).parts)):
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
            if not parts or info.filename.startswith('/') or '\\' in info.filename or ':' in info.filename or any(p in ('.', '..') or (p.startswith('.') and info.filename != '.gitignore') for p in parts):
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
    output = Path(output).absolute()
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
