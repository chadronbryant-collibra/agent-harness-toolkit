import contextlib
from unittest.mock import patch
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import uuid

import kit
import toolkit


ROOT = Path(__file__).resolve().parents[1]
class WorkspaceMemory(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='memory workspace ')
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name).resolve()

    def call(self, entry, *args, data=None, expect=0, root=None):
        base = root or self.root
        command = [sys.executable, '-B', str(ROOT / entry), '--workspace', str(base), *args]
        result = subprocess.run(command, input=data, text=True, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, expect, result.stderr or result.stdout)
        return json.loads(result.stdout if expect == 0 else result.stderr)

    def install(self, root=None):
        plan = self.call('kit.py', 'add', 'memory-harness', root=root)
        return self.call('kit.py', 'add', 'memory-harness', '--apply-plan', plan['plan_sha256'], root=root)

    def memory(self, *args, data=None, expect=0, root=None):
        base = root or self.root
        return self.call(base / '.harness/memory-tools/memory_harness.py',
                         *args, data=data, expect=expect, root=base)

    def record(self, *, body='Registration opens after venue confirmation.', ref='project.md'):
        return json.dumps({'kind': 'decision', 'title': 'Registration timing', 'note': body,
                           'source': {'type': 'file', 'ref': ref}, 'aliases': ['enrolment']})

    def test_install_preserves_instructions_and_starts_without_a_database(self):
        (self.root / 'AGENTS.md').write_text('Owner instructions.', encoding='utf-8')
        self.install()
        status = self.memory('status')
        self.assertTrue(status['enabled'])
        self.assertFalse((self.root / status['storage']).exists())
        self.assertEqual((self.root / 'AGENTS.md').read_text(encoding='utf-8'), 'Owner instructions.')
        self.assertEqual((self.root / '.harness/.gitignore').read_text(encoding='utf-8').strip(), '*')
        self.assertEqual(self.memory('recall', data='anything')['results'], [])

    def test_lifecycle_prefers_current_and_rechecks_original(self):
        self.install()
        source = self.root / 'project.md'
        source.write_text('Registration opens after venue confirmation.', encoding='utf-8')
        receipt = self.memory('save', data=self.record())
        key = receipt['id']
        self.assertEqual(self.memory('recall', data='enrolment')['results'][0]['source_status'], 'unchanged')
        source.write_text('Registration opens today.', encoding='utf-8')
        self.assertEqual(self.memory('show', key)['source_status'], 'changed')
        self.memory('correct', key, '--version', '0', expect=2, data=self.record())
        self.memory('correct', key, '--version', '1', data=self.record(body='Registration opens today.'))
        self.assertEqual(self.memory('show', key)['note'], 'Registration opens today.')
        history = self.memory('history', key)
        self.assertEqual([r['action'] for r in history], ['correct', 'save'])
        self.assertIn('venue confirmation', history[1]['note'])
        source.unlink()
        self.assertEqual(self.memory('show', key)['source_status'], 'missing')
        self.assertEqual(self.memory('rebuild')['records'], 1)
        self.memory('export', 'before.json')
        snapshot = json.loads((self.root / 'before.json').read_text(encoding='utf-8'))
        self.assertEqual(len(snapshot['records']), 2)
        self.memory('forget', key, '--version', '2')
        self.assertEqual(self.memory('recall', data='registration')['results'], [])
        self.assertIsNone(self.memory('show', key))
        self.assertNotIn('note', self.memory('history', key)[-1])
        self.assertEqual(self.memory('export', 'after.json')['revisions'], 0)
        self.assertEqual(self.memory('rebuild')['records'], 0)

    def test_legacy_import_replays_safely_and_keeps_the_original(self):
        self.install()
        path = self.root / '.harness/memory.sqlite3'
        with contextlib.closing(sqlite3.connect(path)) as db, db:
            db.execute('CREATE TABLE records (id TEXT PRIMARY KEY, body TEXT, source TEXT, created TEXT)')
            db.execute('INSERT INTO records VALUES (?, ?, ?, ?)',
                       (str(uuid.uuid4()), '  Earlier meeting note\n', 'Local label\nunchanged ', toolkit.now()))
        original = path.read_bytes()
        plan = self.memory('import-legacy')
        self.assertNotIn('Earlier', json.dumps(plan))
        imported = self.memory('import-legacy', '--apply-plan', plan['plan_sha256'])
        self.assertEqual(imported['imported'], 1)
        self.assertEqual(self.memory('import-legacy', '--apply-plan', plan['plan_sha256'])['skipped'], 1)
        key = self.memory('recall', data='earlier')['results'][0]['id']
        result = self.memory('show', key)
        self.assertEqual(result['note'], '  Earlier meeting note\n')
        self.assertEqual(result['source']['ref'], 'Local label\nunchanged ')
        self.assertEqual(path.read_bytes(), original)

    def test_upgrade_keeps_saved_records_and_rejects_an_edited_helper(self):
        self.install()
        (self.root / 'project.md').write_text('Registration plan', encoding='utf-8')
        key = self.memory('save', data=self.record())['id']
        relative = '.harness/memory-tools/memory_harness.py'
        target = self.root / relative
        original = b'Previous release sample'
        target.write_bytes(original)
        with patch.dict(kit.MEMORY_120, {relative: toolkit.digest(original)}):
            plan = kit.add(self.root, 'memory-harness')
            self.assertEqual(next(row for row in plan['files'] if row['path'] == relative)['status'], 'update')
            target.write_bytes(b'User edit after preview')
            with self.assertRaisesRegex(toolkit.HarnessError, 'setup-plan-changed'):
                kit.add(self.root, 'memory-harness', plan['plan_sha256'])
            self.assertEqual(target.read_bytes(), b'User edit after preview')
            target.write_bytes(original)
            result = kit.add(self.root, 'memory-harness', plan['plan_sha256'])
        self.assertEqual(result['files_updated'], [relative])
        self.assertEqual(self.memory('show', key)['note'], 'Registration opens after venue confirmation.')
        self.assertTrue((self.root / '.claude/rules/toolkit-memory.md').is_file())

    def test_upgrade_removes_only_the_shipped_retired_helper(self):
        self.install()
        retired = self.root / kit.RETIRED_MEMORY_FILE
        original = b'Shipped older helper'
        retired.write_bytes(original)
        with patch.dict(kit.MEMORY_121, {kit.RETIRED_MEMORY_FILE: toolkit.digest(original)}):
            plan = kit.add(self.root, 'memory-harness')
            self.assertEqual(plan['files'][-1]['status'], 'remove')
            self.assertEqual(kit.add(self.root, 'memory-harness', plan['plan_sha256'])['files_removed'],
                             [kit.RETIRED_MEMORY_FILE])
            self.assertFalse(retired.exists())
            retired.write_bytes(b'User edit')
            plan = kit.add(self.root, 'memory-harness')
            self.assertEqual(plan['files'][-1]['status'], 'keep-edited')
            kit.add(self.root, 'memory-harness', plan['plan_sha256'])
            self.assertEqual(retired.read_bytes(), b'User edit')

    def test_rebuild_removes_old_index_tables_without_changing_saved_records(self):
        self.install()
        (self.root / 'project.md').write_text('Registration plan', encoding='utf-8')
        key = self.memory('save', data=self.record())['id']
        store = self.root / '.harness/memory-harness.sqlite3'
        with contextlib.closing(sqlite3.connect(store)) as db, db:
            db.execute('CREATE TABLE vectors (id TEXT PRIMARY KEY)')
            db.execute('CREATE TABLE semantic_settings (id INTEGER PRIMARY KEY)')
        self.memory('rebuild')
        self.assertEqual(self.memory('recall', data='registration')['results'][0]['id'], key)
        with contextlib.closing(sqlite3.connect(store)) as db:
            rows = db.execute("SELECT name FROM sqlite_master WHERE name IN ('vectors', 'semantic_settings')").fetchall()
        self.assertEqual(rows, [])

    def test_unsafe_file_source_is_refused(self):
        self.install()
        self.memory('save', data=self.record(ref='../project.md'), expect=2)


if __name__ == '__main__':
    unittest.main()
