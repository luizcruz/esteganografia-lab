from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from examples.registry import EXAMPLES


def test_all_examples_run():
    failures = []
    for entry in EXAMPLES:
        try:
            mod = importlib.import_module(entry['module'])
            payload = mod.run()
            assert isinstance(payload, dict)
            assert isinstance(payload.get('steps'), list)
            assert payload['steps']
        except Exception as exc:
            failures.append((entry['id'], repr(exc)))
    assert not failures, failures


if __name__ == '__main__':
    test_all_examples_run()
    print(f'OK: {len(EXAMPLES)} exemplos executados com sucesso')
