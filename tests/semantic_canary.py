"""Exercise the release with a real local embedding service and fictional notes."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
MODEL = 'all-minilm:latest'
PORT = 11434


def call(program, workspace, *args, data=None):
    command = [sys.executable, '-B', str(ROOT / program), '--workspace', str(workspace), *args]
    result = subprocess.run(command, input=data, text=True, capture_output=True, check=True, timeout=120)
    return json.loads(result.stdout)


def main():
    with urlopen(f'http://127.0.0.1:{PORT}/api/tags', timeout=15) as response:
        model = next(row for row in json.load(response)['models'] if row['name'] == MODEL)
    with tempfile.TemporaryDirectory(prefix='semantic canary ') as temp:
        workspace = Path(temp).resolve()
        plan = call('kit.py', workspace, 'add', 'memory-harness')
        call('kit.py', workspace, 'add', 'memory-harness', '--apply-plan', plan['plan_sha256'])
        rows = (
            ('Event registration', 'Registration opens after venue confirmation.',
             'When can people sign up?'),
            ('Weather contingency', 'Outdoor activities move indoors during a thunderstorm.',
             'What happens if it rains?'),
            ('Volunteer check-in', 'Volunteer badges are available at the west entrance.',
             None),
        )
        records = []
        installed = workspace / '.harness/memory-tools/memory_harness.py'
        for title, note, question in rows:
            data = json.dumps({'kind': 'decision', 'title': title, 'note': note,
                               'source': {'type': 'user', 'ref': 'fictional example'}})
            records.append((call(installed, workspace, 'save', data=data)['id'], question))
        assert call(installed, workspace, 'semantic-check')['status'] == 'model-ready-to-configure'
        setup = call(installed, workspace, 'semantic-configure', '--use-by-default')
        assert setup['digest'] == model['digest'] and setup['use_by_default']
        assert call(installed, workspace, 'semantic-check')['status'] == 'choose-notes'
        call(installed, workspace, 'semantic-build', '--all')
        assert call(installed, workspace, 'semantic-check')['indexed'] == len(records)
        for key, question in records:
            if question is None:
                continue
            keyword = call(installed, workspace, 'recall', '--keyword-only', data=question)
            hybrid = call(installed, workspace, 'recall', data=question)
            assert all(row['id'] != key for row in keyword['results']), keyword
            assert hybrid['mode'] == 'hybrid' and hybrid['results'][0]['id'] == key, hybrid
        key = records[0][0]
        call(installed, workspace, 'forget', key, '--version', '1')
        after = call(installed, workspace, 'recall', data=records[0][1])
        assert all(row['id'] != key for row in after['results']), after
        print('Real local embeddings returned both paraphrased decisions first and excluded a forgotten record.')


if __name__ == '__main__':
    main()
