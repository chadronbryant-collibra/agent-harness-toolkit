import copy
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import toolkit as t


class Core(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='harness path with spaces ')
        self.root = Path(self.temp.name).resolve()
        plan = t.initialize(self.root)
        self.receipt = t.initialize(self.root, plan['plan_sha256'])

    def tearDown(self):
        self.temp.cleanup()

    def cfg(self, **changes):
        cfg = t.config(self.root)
        for key, value in changes.items(): cfg[key] = value
        t.atomic_write(t.state_path(self.root, 'config.json'), t.encode(cfg))
        return cfg

    def task(self):
        return t.read_json(ROOT / 'examples/task.json')

    def test_setup_refuses_existing(self):
        with self.assertRaises(t.HarnessError):
            t.initialize(self.root, t.initialize(self.root)['plan_sha256'])

    def test_setup_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp).resolve()
            plan = t.initialize(p)
            (p / 'CLAUDE.md').write_text('owner')
            with self.assertRaises(t.HarnessError): t.initialize(p, plan['plan_sha256'])
            self.assertEqual((p / 'CLAUDE.md').read_text(), 'owner')

    def test_uninstall_preserves_modified(self):
        (self.root / 'CLAUDE.md').write_text('owner edits')
        result = t.uninstall(self.root)
        self.assertIn('CLAUDE.md', result['retained_modified'])
        self.assertEqual((self.root / 'CLAUDE.md').read_text(), 'owner edits')

    def test_traversal(self):
        with self.assertRaises(t.HarnessError): t.safe_path(self.root, '../escape')

    def test_symlink(self):
        try: (self.root / 'linked').symlink_to(self.root, target_is_directory=True)
        except OSError: self.skipTest('Host does not grant symlink creation')
        with self.assertRaises(t.HarnessError): t.safe_path(self.root, 'linked/x')

    def test_duplicate_json(self):
        p = self.root / 'duplicate.json'; p.write_text('{"x":1,"x":2}')
        with self.assertRaises(t.HarnessError): t.read_json(p)

    def test_nonfinite_json(self):
        p = self.root / 'nan.json'; p.write_text('{"x":NaN}')
        with self.assertRaises(t.HarnessError): t.read_json(p)

    def test_route_default_unverified(self):
        self.assertEqual(t.route(t.config(self.root), self.task())['status'], 'model-verification-required')

    def test_source_cannot_authorize(self):
        task = self.task(); task['origin'] = 'retrieved-document'
        with self.assertRaises(t.HarnessError): t.route(t.config(self.root), task)

    def test_denied_effect(self):
        task = self.task(); task['effect'] = 'external-write'
        with self.assertRaises(t.HarnessError): t.route(t.config(self.root), task)

    def test_missing_acceptance(self):
        task = self.task(); task['acceptance'] = []
        with self.assertRaises(t.HarnessError): t.route(t.config(self.root), task)

    def test_evidence_rank_does_not_grant_authority(self):
        task = self.task()
        task['sources'] = [
            {'id':'old','kind':'primary','verified':True,'reviewed_at':'2020-01-01'},
            {'id':'current','kind':'primary','verified':True,'reviewed_at':'2026-10-30'},
            {'id':'unknown','kind':'unknown','verified':True,'reviewed_at':'2026-10-30'}]
        result = t.assess(t.config(self.root), task, dt.date(2026,10,30))
        self.assertEqual([r['id'] for r in result['evidence']], ['current','old','unknown'])
        self.assertFalse(result['trust_grants_permission'])
        self.assertTrue(all(not r['instruction_authority'] for r in result['evidence']))

    def test_fresh_sources_cannot_authorize_external_write(self):
        task = self.task(); task['effect'] = 'external-write'
        task['sources'] = [{'id':'primary','kind':'primary','verified':True,'reviewed_at':'2026-10-30'}]
        with self.assertRaises(t.HarnessError): t.assess(t.config(self.root), task)

    def test_reservation_unknown_retained(self):
        row = t.reserve(self.root, .5)
        done = t.reconcile(self.root, row['reservation'])
        self.assertIsNone(done['actual_usd'])
        self.assertEqual(done['charged_micro_usd'], 500000)

    def test_reservation_not_started(self):
        row = t.reserve(self.root, .5)
        self.assertEqual(t.reconcile(self.root, row['reservation'], not_started=True)['charged_micro_usd'], 0)

    def test_task_limit(self):
        with self.assertRaises(t.HarnessError): t.reserve(self.root, 1.01)

    def test_month_limit(self):
        cfg = t.config(self.root); cfg['budgets']['month_usd'] = .75
        self.cfg(budgets=cfg['budgets'])
        row = t.reserve(self.root, .5); t.reconcile(self.root, row['reservation'])
        with self.assertRaises(t.HarnessError): t.reserve(self.root, .5)

    def test_concurrent_reservation(self):
        t.reserve(self.root, .5)
        with self.assertRaises(t.HarnessError): t.reserve(self.root, .5)

    def test_stale_period(self):
        with self.assertRaises(t.HarnessError): t.reserve(self.root, .5, '2000-01')

    def test_double_reconcile(self):
        row = t.reserve(self.root, .5); t.reconcile(self.root, row['reservation'], .1)
        with self.assertRaises(t.HarnessError): t.reconcile(self.root, row['reservation'], .1)

    def test_money_invalid(self):
        for value in (float('nan'), float('inf'), -1, True, '1'):
            with self.assertRaises(t.HarnessError): t.money(value)

    def test_memory_disabled(self):
        with self.assertRaises(t.HarnessError): t.memory(self.root, 'remember', 'secret', source='test')

    def test_memory_lifecycle_and_literal_wildcards(self):
        cfg = t.config(self.root); cfg['memory']['enabled'] = True
        self.cfg(memory=cfg['memory'])
        row = t.memory(self.root, 'remember', 'Synthetic 100% example', source='synthetic')
        self.assertEqual(len(t.memory(self.root, 'search', '100%')), 1)
        self.assertEqual(t.memory(self.root, 'search', '100_'), [])
        self.assertEqual(t.memory(self.root, 'forget', record_id=row['id'])['deleted'], 1)
        self.assertEqual(t.memory(self.root, 'search', 'Synthetic'), [])

    def test_task_false_completion_refused(self):
        row = t.task_create(self.root, self.task())
        with self.assertRaises(t.HarnessError): t.task_checkpoint(self.root, row['id'], 'delivered', 'claim')
        t.task_checkpoint(self.root, row['id'], 'working', 'source pointers')
        t.task_checkpoint(self.root, row['id'], 'verified', 'declared evidence')
        t.task_checkpoint(self.root, row['id'], 'delivered', 'artifact pointer')
        self.assertEqual(t.inventory(self.root)[0]['process_state'], 'not-observed')

    def test_cycle_limit(self):
        row = t.task_create(self.root, self.task())
        for _ in range(3): t.task_checkpoint(self.root, row['id'], 'working', 'new evidence')
        with self.assertRaises(t.HarnessError): t.task_checkpoint(self.root, row['id'], 'working', 'more')

    def test_lock_contention(self):
        with t.lock(self.root):
            with self.assertRaises(t.HarnessError):
                with t.lock(self.root): pass

    def test_hook_merge_and_restore(self):
        path = self.root / '.claude/settings.json'
        before = b'{"owner": true, "hooks": {"Stop": []}}\n'
        path.write_bytes(before)
        plan = t.install_hooks(self.root)
        t.install_hooks(self.root, plan['binding'])
        self.assertTrue(t.read_json(path)['owner'])
        t.remove_hooks(self.root)
        self.assertEqual(path.read_bytes(), before)

    def test_hook_rollback_preserves_peer_change(self):
        plan = t.install_hooks(self.root); t.install_hooks(self.root, plan['binding'])
        path = self.root / '.claude/settings.json'
        path.write_text('{"peer":true}')
        with self.assertRaises(t.HarnessError): t.remove_hooks(self.root)
        self.assertTrue(t.read_json(path)['peer'])

    def test_reference_freshness(self):
        result = t.references_check(ROOT / 'references/catalog.json', dt.date(2026, 12, 1))
        self.assertTrue(all(r['status'] == 'stale' for r in result))

    def test_doctor_no_network(self):
        with patch('subprocess.run', side_effect=AssertionError('no subprocess')):
            self.assertEqual(t.doctor()['mutations'], [])

    def test_launcher_refuses_unverified(self):
        task = t.task_create(self.root, self.task())
        with self.assertRaises(t.HarnessError): t.launch(self.root, task['id'], .5)

    def test_launcher_preview_no_provider(self):
        cfg = t.config(self.root); cfg['models']['standard']['verified'] = True
        cfg['profile']['billing'] = 'metered'; self.cfg(models=cfg['models'], profile=cfg['profile'])
        task = t.task_create(self.root, self.task())
        with patch('subprocess.run', side_effect=AssertionError('no call')):
            result = t.launch(self.root, task['id'], .5, executable=sys.executable)
        self.assertIn('--restricted', result['command'])
        self.assertFalse(t.ledger(self.root)['reservations'])

    def test_unsupported_launcher_no_reservation(self):
        cfg = t.config(self.root); cfg['models']['standard']['verified'] = True
        cfg['profile']['billing'] = 'metered'; self.cfg(models=cfg['models'], profile=cfg['profile'])
        task = t.task_create(self.root, self.task())
        with patch('subprocess.run', return_value=subprocess.CompletedProcess([], 0, 'other-cli', '')):
            with self.assertRaises(t.HarnessError): t.launch(self.root, task['id'], .5, True, sys.executable)
        self.assertFalse(t.ledger(self.root)['reservations'])

    def test_hook_payload(self):
        result = subprocess.run([sys.executable, str(ROOT / 'toolkit.py'), 'hook', 'SessionStart'],
                                input='{"prompt":"do not retain"}', text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn('do not retain', result.stdout)

    def fake_launch(self, program):
        cfg = t.config(self.root)
        cfg['models']['standard']['verified'] = True
        cfg['profile']['billing'] = 'metered'
        cfg['autonomy']['timeout_seconds'] = 1
        self.cfg(models=cfg['models'], profile=cfg['profile'], autonomy=cfg['autonomy'])
        task = t.task_create(self.root, self.task())
        real_popen = subprocess.Popen
        real_run = subprocess.run
        def fake_popen(command, **kwargs):
            if '--print' in command:
                return real_popen([sys.executable, '-c', program], **kwargs)
            return real_popen(command, **kwargs)
        help_text = '--print --max-budget-usd --restricted --safe-mode --strict-mcp-config --no-session-persistence --permission-mode --allowedTools --tools --effort'
        def fake_run(command, **kwargs):
            if '--help' in command:
                return subprocess.CompletedProcess([], 0, help_text, '')
            return real_run(command, **kwargs)
        with patch('subprocess.run', side_effect=fake_run), patch('subprocess.Popen', side_effect=fake_popen):
            result = t.launch(self.root, task['id'], .5, True, sys.executable)
        return task, result

    def test_real_subprocess_success_accounting(self):
        task, result = self.fake_launch('import json; print(json.dumps({"is_error":False,"total_cost_usd":0.12}))')
        self.assertEqual(result['status'], 'executor-returned')
        self.assertEqual(result['actual_usd'], .12)
        self.assertEqual(result['artifact_acceptance'], 'pending-independent-verification')
        self.assertFalse(t.state_path(self.root, 'active-run').exists())
        with self.assertRaises(t.HarnessError): t.launch(self.root, task['id'], .5, True, sys.executable)

    def test_malformed_output_not_success(self):
        task, result = self.fake_launch('print("invalid")')
        self.assertEqual(result['status'], 'executor-failed')
        self.assertIsNone(result['actual_usd'])
        self.assertEqual(next(iter(t.ledger(self.root)['reservations'].values()))['charged_micro_usd'], 500000)

    def test_real_timeout_termination(self):
        task, result = self.fake_launch('import time; time.sleep(10)')
        self.assertEqual(result['status'], 'timeout-or-output-budget')
        self.assertIsNotNone(result['process_exit'])

    def test_malformed_budget_denied(self):
        row = t.reserve(self.root, .5)
        data = t.ledger(self.root)
        data['reservations'][row['reservation']]['charged_micro_usd'] = -1
        t.atomic_write(t.state_path(self.root, 'budget.json'), t.encode(data))
        with self.assertRaises(t.HarnessError): t.reserve(self.root, .1)

    def test_malformed_configuration_denied(self):
        cfg = t.config(self.root); cfg['autonomy']['timeout_seconds'] = -1
        t.atomic_write(t.state_path(self.root, 'config.json'), t.encode(cfg))
        with self.assertRaises(t.HarnessError): t.config(self.root)

    def test_two_process_reservations(self):
        command = [sys.executable, str(ROOT / 'toolkit.py'), '--workspace', str(self.root), 'reserve', '--usd', '0.5']
        first = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        second = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        first.communicate(timeout=10); second.communicate(timeout=10)
        self.assertEqual(sorted([first.returncode, second.returncode]), [0, 2])


class Package(unittest.TestCase):
    def test_deterministic_archive_and_roundtrip(self):
        spec = importlib.util.spec_from_file_location('package', ROOT / 'scripts/package.py')
        package = importlib.util.module_from_spec(spec); spec.loader.exec_module(package)
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / 'first.zip', Path(tmp) / 'second.zip'
            package.build(first); package.build(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            unpack = Path(tmp) / 'unpack'; unpack.mkdir()
            with zipfile.ZipFile(first) as z:
                self.assertFalse(any(n.startswith('.harness/') or n.startswith('.git/') for n in z.namelist()))
                self.assertIn('.harness/', z.read('.gitignore').decode())
                z.extractall(unpack)
            result = subprocess.run([sys.executable, str(unpack / 'toolkit.py'), 'self-check'], capture_output=True)
            self.assertEqual(result.returncode, 0)

    def test_archive_traversal_refused(self):
        spec = importlib.util.spec_from_file_location('package', ROOT / 'scripts/package.py')
        package = importlib.util.module_from_spec(spec); spec.loader.exec_module(package)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'bad.zip'
            with zipfile.ZipFile(target, 'w') as z:
                z.writestr('../escape', 'bad'); z.writestr('SHA256SUMS.json', '{}')
            with self.assertRaises(ValueError): package.verify(target)


if __name__ == '__main__': unittest.main()
