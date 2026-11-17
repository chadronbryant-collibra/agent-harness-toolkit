import contextlib
import http.server
from unittest.mock import patch
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
import uuid

import kit
import toolkit
from memory_semantic import EmbeddingError, Ollama


ROOT = Path(__file__).resolve().parents[1]
MODEL = 'local-model:latest'
DIGEST = 'a' * 64


class FakeOllama(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def reply(self, result, code=200):
        payload = json.dumps(result).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path != '/api/tags':
            return self.reply({}, 404)
        self.reply({'models': [{'name': MODEL, 'digest': self.server.digest,
                                'details': {'format': 'gguf'}}]})

    def do_POST(self):
        if self.path != '/api/embed':
            return self.reply({}, 404)
        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        inputs = request['input']
        self.server.received.extend(inputs)
        vectors = [[1.0, 0.0] if 'registration' in text.lower() or 'sign up' in text else [0.0, 1.0]
                   for text in inputs]
        self.reply({'model': MODEL, 'embeddings': vectors})


@contextlib.contextmanager
def fake_ollama():
    server = http.server.HTTPServer(('127.0.0.1', 0), FakeOllama)
    server.digest = DIGEST
    server.received = []
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=10)


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

    def test_semantic_uses_selected_current_records_and_falls_back(self):
        self.install()
        (self.root / 'project.md').write_text('Registration plan', encoding='utf-8')
        key = self.memory('save', data=self.record())['id']
        other = self.root / 'Other workspace'
        other.mkdir()
        self.install(other)
        self.assertEqual(self.memory('recall', data='registration', root=other)['results'], [])
        with fake_ollama() as service:
            self.assertEqual(self.memory('recall', data='When can people sign up?')['results'], [])
            cfg = ['semantic-configure', '--port', str(service.server_port), '--model', MODEL, '--digest', DIGEST]
            self.memory(*cfg)
            self.memory('semantic-build', expect=2)
            self.assertEqual(service.received, [])
            self.memory('semantic-build', '--id', key)
            found = self.memory('recall', '--semantic', data='When can people sign up?')
            self.assertEqual(found['results'][0]['id'], key)
            self.assertEqual(found['results'][0]['matched_by'], ['semantic'])
            service.digest = 'f' * 64
            previous = list(service.received)
            fallback = self.memory('recall', '--semantic', data='registration')
            self.assertEqual(fallback['semantic_status'], 'unavailable')
            self.assertEqual(fallback['results'][0]['id'], key)
            self.assertEqual(service.received, previous)
            service.digest = DIGEST
            self.memory('forget', key, '--version', '1')
            self.assertEqual(self.memory('recall', '--semantic', data='sign up')['results'], [])
            self.assertEqual(self.memory('status')['semantic_indexed'], 0)
            self.memory('semantic-off')
            self.assertEqual(self.memory('status')['semantic'], 'disabled')

    def test_guided_meaning_setup_discovers_model_and_remembers_choice(self):
        self.assertEqual(self.call('memory_harness.py', 'semantic-check')['status'], 'memory-not-set-up-here')
        self.install()
        (self.root / 'project.md').write_text('Registration plan', encoding='utf-8')
        key = self.memory('save', data=self.record())['id']
        with fake_ollama() as service:
            port = str(service.server_port)
            before = self.memory('semantic-check', '--port', port, '--model', MODEL)
            self.assertEqual(before['status'], 'model-ready-to-configure')
            self.assertEqual(service.received, [])
            result = self.memory('semantic-configure', '--port', port, '--model', MODEL, '--use-by-default')
            self.assertEqual(result['digest'], DIGEST)
            self.assertEqual(self.memory('semantic-check')['status'], 'choose-notes')
            self.assertEqual(service.received, [])
            self.memory('semantic-build', '--id', key)
            ready = self.memory('semantic-check')
            self.assertEqual(ready['indexed'], 1)
            self.assertTrue(ready['use_by_default'])
            self.assertEqual(self.memory('recall', data='When can people sign up?')['results'][0]['id'], key)
            previous = list(service.received)
            self.assertEqual(self.memory('recall', '--keyword-only', data='When can people sign up?')['results'], [])
            self.assertEqual(service.received, previous)
            service.digest = 'e' * 64
            self.assertEqual(self.memory('semantic-check')['status'], 'local-model-changed')
            service.digest = DIGEST
            self.memory('semantic-configure', '--port', port, '--model', MODEL, '--manual')
            self.assertFalse(self.memory('semantic-check')['use_by_default'])
            self.assertEqual(self.memory('semantic-check')['indexed'], 1)
            self.assertEqual(self.memory('recall', data='When can people sign up?')['mode'], 'keyword')

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

    def test_unsafe_sources_and_cloud_model_are_refused(self):
        self.install()
        self.memory('save', data=self.record(ref='../project.md'), expect=2)
        with self.assertRaises(EmbeddingError):
            Ollama(11434, 'remote:cloud', DIGEST)


if __name__ == '__main__':
    unittest.main()
