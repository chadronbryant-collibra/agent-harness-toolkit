#!/usr/bin/env python3
"""Source-linked local memory. Use stdin for records and questions."""

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
from urllib.parse import urlsplit
import uuid

import toolkit
from memory_semantic import EmbeddingError, Ollama, bounded_vector, cosine


KINDS = ('preference', 'decision', 'progress', 'reference')
SCHEMA = 1
MAX_SOURCE_BYTES = 2_000_000
MAX_RECORDS = 2000
MAX_INDEX_ROWS = 200
SKIP_WORDS = frozenset('a an are about did do for how i in is it me of on or the to what when where which who with we you'.split())
SETUP = '.harness/memory-harness.json'
DB = '.harness/memory-harness.sqlite3'
LEGACY = '.harness/memory.sqlite3'
DDL = """
CREATE TABLE IF NOT EXISTS revisions (
    id TEXT NOT NULL, version INTEGER NOT NULL, action TEXT NOT NULL,
    record TEXT, observed_at TEXT NOT NULL, PRIMARY KEY (id, version)
);
CREATE VIEW IF NOT EXISTS current_records AS
    SELECT r.* FROM revisions r
    WHERE r.action != 'forget'
      AND NOT EXISTS (SELECT 1 FROM revisions newer
                      WHERE newer.id=r.id AND newer.version>r.version);
CREATE TABLE IF NOT EXISTS legacy_imports (legacy_id TEXT PRIMARY KEY, digest TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS semantic_settings (id INTEGER PRIMARY KEY CHECK (id=1), settings TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS vectors (id TEXT PRIMARY KEY, version INTEGER NOT NULL, vector TEXT NOT NULL);
CREATE VIRTUAL TABLE IF NOT EXISTS keywords USING fts5(id UNINDEXED, title, note, aliases);
"""


class MemoryError(toolkit.HarnessError):
    pass


def packed(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def read_input(limit):
    raw = sys.stdin.buffer.read(limit + 1)
    if len(raw) > limit:
        raise MemoryError('input-too-large')
    return raw.decode('utf-8')


def text(value, length):
    if not isinstance(value, str) or not value.strip() or len(value) > length or '\x00' in value:
        raise MemoryError('invalid-record-field')
    return value.strip()


def observe_file(root, ref):
    path = toolkit.safe_path(root, ref)
    if not path.is_file():
        return None
    with path.open('rb') as handle:
        data = handle.read(MAX_SOURCE_BYTES + 1)
    if len(data) > MAX_SOURCE_BYTES:
        raise MemoryError('source-file-too-large')
    return hashlib.sha256(data).hexdigest()


def source_record(root, source):
    if not isinstance(source, dict) or set(source) != {'type', 'ref'}:
        raise MemoryError('choose-one-source')
    kind, ref = source['type'], text(source['ref'], 1000)
    if any(char in ref for char in ('\r', '\n')):
        raise MemoryError('invalid-source-reference')
    result = {'type': kind, 'ref': ref}
    if kind == 'file':
        if (Path(ref).is_absolute() or '\\' in ref or ':' in ref
                or any(p in ('..', '.git', '.harness') for p in Path(ref).parts)):
            raise MemoryError('source-must-be-a-workspace-file')
        digest = observe_file(root, ref)
        if digest is None:
            raise MemoryError('source-file-missing')
        result['sha256'] = digest
    elif kind == 'url':
        url = urlsplit(ref)
        if url.scheme != 'https' or not url.hostname or url.username is not None or url.query:
            raise MemoryError('use-a-clean-https-source-link')
    elif kind != 'user':
        raise MemoryError('invalid-source-type')
    return result


def validate(root, value):
    fields = {'kind', 'title', 'note', 'source'}
    if not isinstance(value, dict) or set(value) - (fields | {'aliases'}) or not fields <= set(value):
        raise MemoryError('invalid-record-shape')
    if value['kind'] not in KINDS:
        raise MemoryError('invalid-record-kind')
    aliases = value.get('aliases', [])
    if not isinstance(aliases, list) or len(aliases) > 8:
        raise MemoryError('too-many-aliases')
    return {'kind': value['kind'], 'title': text(value['title'], 120),
            'note': text(value['note'], 6000),
            'source': source_record(root, value['source']),
            'aliases': [text(alias, 100) for alias in aliases]}


def setup_state(root):
    path = toolkit.safe_path(root, SETUP)
    if not path.is_file():
        return False
    if toolkit.read_json(path) != {'schema': SCHEMA, 'enabled': True}:
        raise MemoryError('unexpected-memory-configuration')
    return True


def open_read(path):
    db = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True, timeout=5)
    db.row_factory = sqlite3.Row
    return db


@contextlib.contextmanager
def database(root, *, write=False):
    if not setup_state(root):
        raise MemoryError('set-up-memory-in-this-workspace-first')
    path = toolkit.safe_path(root, DB)
    if not write:
        if not path.is_file():
            yield None
            return
        with contextlib.closing(open_read(path)) as db:
            if db.execute('PRAGMA user_version').fetchone()[0] != SCHEMA:
                raise MemoryError('unsupported-memory-database')
            # All lookups in this command see the same committed snapshot.
            db.execute('BEGIN')
            yield db
        return

    with toolkit.lock(root):
        if not path.exists():
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            os.close(fd)
        with contextlib.closing(sqlite3.connect(path, timeout=5)) as db:
            db.row_factory = sqlite3.Row
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if version == 0:
                db.executescript('BEGIN IMMEDIATE;\n' + DDL + '\nPRAGMA user_version=1; COMMIT;')
            elif version != SCHEMA:
                raise MemoryError('unsupported-memory-database')
            db.execute('BEGIN IMMEDIATE')
            with db:
                yield db


def index_record(db, key, record):
    db.execute('DELETE FROM keywords WHERE id=?', (key,))
    db.execute('DELETE FROM vectors WHERE id=?', (key,))
    if record:
        db.execute('INSERT INTO keywords VALUES (?, ?, ?, ?)',
                   (key, record['title'], record['note'], ' '.join(record['aliases'])))


def write_revision(db, key, version, action, record):
    db.execute('INSERT INTO revisions VALUES (?, ?, ?, ?, ?)',
               (key, version, action, packed(record) if record is not None else None, toolkit.now()))
    index_record(db, key, record)
    return {'id': key, 'version': version, 'action': action}


def changes(root, action, record=None, key=None, expected=None):
    with database(root, write=True) as db:
        if action == 'save':
            if db.execute('SELECT count(*) FROM current_records').fetchone()[0] >= MAX_RECORDS:
                raise MemoryError('workspace-memory-limit')
            return write_revision(db, uuid.uuid4().hex, 1, action, record)
        existing = db.execute('SELECT version FROM current_records WHERE id=?', (key,)).fetchone()
        if existing is None or existing['version'] != expected:
            raise MemoryError('record-changed-or-missing')
        return write_revision(db, key, expected + 1, action, record)


def freshness(root, source):
    if source['type'] != 'file':
        return {'user': 'user-stated', 'url': 'open-source-to-verify'}.get(source['type'], 'legacy-label')
    try:
        current = observe_file(root, source['ref'])
    except (OSError, toolkit.HarnessError):
        return 'unavailable'
    if current is None:
        return 'missing'
    return 'unchanged' if current == source['sha256'] else 'changed'


def pointer(root, row, *, include_note=False):
    record = json.loads(row['record'])
    result = {'id': row['id'], 'version': row['version'], 'kind': record['kind'],
              'title': record['title'], 'source': record['source'],
              'source_status': freshness(root, record['source'])}
    if include_note:
        result.update(note=record['note'], aliases=record['aliases'])
    return result


def keyword_rows(db, query, limit):
    terms = list(dict.fromkeys(part for part in re.findall(r'[^\W_]+', query.casefold())
                               if part not in SKIP_WORDS))[:20]
    if not terms:
        return []
    match = ' OR '.join(f'"{term}"' for term in terms)
    return db.execute("""
        SELECT c.* FROM keywords JOIN current_records c ON c.id=keywords.id
        WHERE keywords MATCH ? ORDER BY bm25(keywords, 0, 3, 1, 2), c.id LIMIT ?
    """, (match, limit)).fetchall()


def get_semantic_settings(db):
    row = db.execute('SELECT settings FROM semantic_settings WHERE id=1').fetchone() if db else None
    return json.loads(row[0]) if row else None


def semantic_rows(db, cfg, question, limit):
    if cfg is None:
        return [], 'disabled'
    rows = db.execute("""
        SELECT c.*, v.vector FROM current_records c JOIN vectors v ON v.id=c.id AND v.version=c.version
    """).fetchall()
    if not rows:
        return [], 'index-empty'
    runtime = Ollama.from_settings(cfg)
    vector = runtime.embed([question])[0]
    ranked = [(cosine(vector, bounded_vector(json.loads(row['vector']))), row) for row in rows]
    ranked.sort(key=lambda item: (-item[0], item[1]['id']))
    count = db.execute('SELECT count(*) FROM current_records').fetchone()[0]
    status = 'ready' if count == len(rows) else 'partial-index'
    return [row for score, row in ranked[:limit] if score >= 0.30], status


def recall(root, query, limit, semantic=False):
    query = text(query, 500)
    with database(root) as db:
        if db is None:
            return {'mode': 'keyword', 'results': [], 'semantic_status': 'disabled'}
        matches = keyword_rows(db, query, limit)
        related, state = [], 'not-selected'
        if semantic:
            try:
                related, state = semantic_rows(db, get_semantic_settings(db), query, limit)
            except EmbeddingError:
                state = 'unavailable'
        ranked = {}
        for method, rows in (('keyword', matches), ('semantic', related)):
            for rank, row in enumerate(rows, 1):
                entry = ranked.setdefault(row['id'], {'score': 0.0, 'row': row, 'matched_by': []})
                entry['score'] += 1 / (8 + rank)
                entry['matched_by'].append(method)
        results = sorted(ranked.values(), key=lambda entry: (-entry['score'], entry['row']['id']))[:limit]
        return {'mode': 'hybrid' if state in ('ready', 'partial-index') else 'keyword',
                'semantic_status': state,
                'results': [dict(pointer(root, entry['row']), matched_by=entry['matched_by']) for entry in results]}


def read_records(root, command, key=None, kind=None, limit=5):
    with database(root) as db:
        if db is None:
            return [] if command in ('current', 'history') else None
        if command == 'show':
            row = db.execute('SELECT * FROM current_records WHERE id=?', (key,)).fetchone()
            return pointer(root, row, include_note=True) if row else None
        if command == 'history':
            rows = db.execute('SELECT * FROM revisions WHERE id=? ORDER BY version DESC LIMIT ?',
                              (key, limit)).fetchall()
            forgotten = bool(rows and rows[0]['action'] == 'forget')
            entries = []
            for row in rows:
                item = {'id': row['id'], 'version': row['version'], 'action': row['action'],
                        'observed_at': row['observed_at']}
                if not forgotten:
                    item.update(pointer(root, row, include_note=True))
                entries.append(item)
            return entries
        rows = db.execute("""
            SELECT * FROM current_records WHERE (? IS NULL OR json_extract(record, '$.kind')=?)
            ORDER BY observed_at DESC, id LIMIT ?
        """, (kind, kind, limit)).fetchall()
        return [pointer(root, row) for row in rows]


def export(root, filename):
    path = toolkit.safe_path(root, filename)
    if path.suffix.lower() != '.json' or '.harness' in Path(filename).parts or path.exists():
        raise MemoryError('choose-a-new-json-export-file')
    with database(root) as db:
        records = [dict(row) for row in db.execute("""
            SELECT r.* FROM revisions r JOIN current_records c ON c.id=r.id ORDER BY r.id, r.version
        """)] if db else []
    for item in records:
        item['record'] = json.loads(item['record'])
    with path.open('x', encoding='utf-8') as target:
        target.write(packed({'schema': SCHEMA, 'scope': 'active-records-with-history', 'records': records}) + '\n')
    return {'export': filename, 'revisions': len(records), 'includes_forgotten': False}


def legacy_plan(root):
    path = toolkit.safe_path(root, LEGACY)
    if not path.is_file():
        return [], {'status': 'no-legacy-store', 'records': 0}
    with contextlib.closing(open_read(path)) as db:
        rows = db.execute('SELECT id, body, source, created FROM records ORDER BY id LIMIT ?', (MAX_RECORDS + 1,)).fetchall()
    if len(rows) > MAX_RECORDS:
        raise MemoryError('legacy-store-too-large')
    items = []
    for row in rows:
        body, source = row['body'], row['source']
        if not isinstance(body, str) or not isinstance(source, str) or len(body) > 12000 or len(source) > 12000:
            raise MemoryError('legacy-item-too-large-or-invalid')
        key = uuid.UUID(row['id']).hex
        title = next((line.strip() for line in body.splitlines() if line.strip()), 'Imported note')[:120]
        record = {'kind': 'reference', 'title': title, 'note': body,
                  'source': {'type': 'legacy', 'ref': source}, 'aliases': []}
        stamp = text(row['created'], 100)
        items.append((key, toolkit.digest(toolkit.encode(dict(row))), record, stamp))
    binding = toolkit.digest(toolkit.encode({'workspace': str(root), 'records': items}))
    return items, {'status': 'preview', 'records': len(items), 'plan_sha256': binding, 'legacy_preserved': True}


def migrate(root, expected):
    if not setup_state(root):
        raise MemoryError('set-up-memory-in-this-workspace-first')
    items, plan = legacy_plan(root)
    if expected is None:
        return plan
    if plan.get('plan_sha256') != expected:
        raise MemoryError('legacy-import-plan-changed')
    imported = skipped = 0
    with database(root, write=True) as db:
        if legacy_plan(root)[1] != plan:
            raise MemoryError('legacy-import-plan-changed')
        count = db.execute('SELECT count(*) FROM current_records').fetchone()[0]
        for legacy_key, digest, record, stamp in items:
            row = db.execute('SELECT digest FROM legacy_imports WHERE legacy_id=?', (legacy_key,)).fetchone()
            if row:
                if row['digest'] != digest:
                    raise MemoryError('legacy-item-changed-since-import')
                skipped += 1
                continue
            if count + imported >= MAX_RECORDS:
                raise MemoryError('workspace-memory-limit')
            key = uuid.uuid5(uuid.NAMESPACE_URL, 'agent-harness-toolkit:legacy:' + legacy_key).hex
            db.execute('INSERT INTO revisions VALUES (?, 1, ?, ?, ?)', (key, 'import', packed(record), stamp))
            index_record(db, key, record)
            db.execute('INSERT INTO legacy_imports VALUES (?, ?)', (legacy_key, digest))
            imported += 1
    return {'imported': imported, 'skipped': skipped, 'legacy_preserved': True}


def semantic_configure(root, port, model, digest):
    runtime = Ollama(port, model, digest)
    runtime.verify()
    with database(root, write=True) as db:
        previous = get_semantic_settings(db)
        if previous != runtime.settings:
            db.execute('DELETE FROM vectors')
        db.execute('INSERT OR REPLACE INTO semantic_settings VALUES(1, ?)', (packed(runtime.settings),))
    return {'semantic': 'configured', 'indexed': 'not-yet-built', 'model': model, 'digest': digest}


def semantic_build(root, selected, all_records=False):
    with database(root) as db:
        settings = get_semantic_settings(db)
        if settings is None:
            raise MemoryError('configure-local-semantic-search-first')
        if bool(selected) == all_records or len(selected) > MAX_INDEX_ROWS or len(set(selected)) != len(selected):
            raise MemoryError('choose-record-ids-or-all')
        if selected:
            marks = ','.join('?' for _ in selected)
            query = f'SELECT * FROM current_records WHERE id IN ({marks}) ORDER BY id'
            rows = db.execute(query, selected).fetchall()
            if len(rows) != len(selected):
                raise MemoryError('selected-record-missing')
        else:
            rows = db.execute('SELECT * FROM current_records ORDER BY id LIMIT ?', (MAX_INDEX_ROWS + 1,)).fetchall()
    if len(rows) > MAX_INDEX_ROWS:
        raise MemoryError('semantic-workspace-limit-use-keyword-search')
    runtime = Ollama.from_settings(settings)
    runtime.verify()
    built = []
    for start in range(0, len(rows), 16):
        group = rows[start:start + 16]
        notes = [json.loads(row['record']) for row in group]
        vectors = runtime.embed([r['title'] + '\n' + r['note'] for r in notes])
        built.extend((row['id'], row['version'], packed(v)) for row, v in zip(group, vectors, strict=True))
    with database(root, write=True) as db:
        live = [tuple(row) for row in db.execute('SELECT id, version FROM current_records ORDER BY id')
                if all_records or row['id'] in selected]
        if live != [(row['id'], row['version']) for row in rows] or get_semantic_settings(db) != settings:
            raise MemoryError('records-changed-during-index-build')
        db.execute('DELETE FROM vectors')
        db.executemany('INSERT INTO vectors VALUES (?, ?, ?)', built)
    return {'semantic': 'indexed', 'records': len(built), 'model': runtime.model}


def maintenance(root, command):
    if command == 'status':
        enabled = setup_state(root)
        report = {'enabled': enabled, 'storage': DB, 'format': 'plaintext-local',
                  'legacy_available': toolkit.safe_path(root, LEGACY).is_file(),
                  'provider_calls': 0, 'records': 0, 'semantic': 'disabled'}
        if enabled:
            with database(root) as db:
                if db:
                    report['records'] = db.execute('SELECT count(*) FROM current_records').fetchone()[0]
                    if get_semantic_settings(db):
                        report['semantic'] = 'configured'
                        report['semantic_indexed'] = db.execute('SELECT count(*) FROM vectors').fetchone()[0]
        return report
    with database(root, write=True) as db:
        db.execute('DELETE FROM vectors')
        if command == 'semantic-off':
            db.execute('DELETE FROM semantic_settings')
            return {'semantic': 'disabled', 'vectors_removed': True}
        db.execute('DELETE FROM keywords')
        rows = db.execute('SELECT * FROM current_records').fetchall()
        for row in rows:
            index_record(db, row['id'], json.loads(row['record']))
        return {'status': 'rebuilt', 'records': len(rows), 'semantic_index': 'cleared'}


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', default='.')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('status', 'save', 'rebuild', 'semantic-off'):
        sub.add_parser(name)
    for name in ('correct', 'forget'):
        item = sub.add_parser(name)
        item.add_argument('id')
        item.add_argument('--version', type=int, required=True)
    for name in ('show', 'history', 'current', 'recall'):
        item = sub.add_parser(name)
        if name in ('show', 'history'):
            item.add_argument('id')
        if name != 'show':
            item.add_argument('--limit', type=int, default=5)
        if name == 'current':
            item.add_argument('--kind', choices=KINDS)
        if name == 'recall':
            item.add_argument('--semantic', action='store_true')
    sub.add_parser('export').add_argument('file')
    sub.add_parser('import-legacy').add_argument('--apply-plan')
    build = sub.add_parser('semantic-build')
    build.add_argument('--id', action='append', default=[])
    build.add_argument('--all', action='store_true')
    item = sub.add_parser('semantic-configure')
    item.add_argument('--port', type=int, default=11434)
    item.add_argument('--model', required=True)
    item.add_argument('--digest', required=True)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        root = Path(args.workspace).absolute()
        cmd = args.command
        limit = getattr(args, 'limit', 5)
        if not 1 <= limit <= 20:
            raise MemoryError('limit-must-be-between-1-and-20')
        if cmd in ('save', 'correct', 'forget'):
            record = validate(root, json.loads(read_input(30000))) if cmd != 'forget' else None
            result = changes(root, cmd, record, getattr(args, 'id', None), getattr(args, 'version', None))
        elif cmd == 'recall':
            result = recall(root, read_input(2048), limit, args.semantic)
        elif cmd in ('current', 'show', 'history'):
            result = read_records(root, cmd, getattr(args, 'id', None), getattr(args, 'kind', None), limit)
        elif cmd == 'export':
            result = export(root, args.file)
        elif cmd == 'import-legacy':
            result = migrate(root, args.apply_plan)
        elif cmd == 'semantic-configure':
            result = semantic_configure(root, args.port, args.model, args.digest)
        elif cmd == 'semantic-build':
            result = semantic_build(root, args.id, args.all)
        else:
            result = maintenance(root, cmd)
        print(toolkit.encode(result).decode(), end='')
        return 0
    except (toolkit.HarnessError, EmbeddingError) as error:
        print(toolkit.encode({'status': 'refused', 'reason': str(error)}).decode(), end='', file=sys.stderr)
    except (OSError, ValueError, sqlite3.Error, TypeError):
        print('Memory operation failed. Check the workspace, input and SQLite FTS5 support.', file=sys.stderr)
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
