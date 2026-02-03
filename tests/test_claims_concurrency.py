import threading
import time
from scripts import claims


def worker(results, idx):
    ok, info = claims.claim('stoybl bl bl 1', 'stoybl_list', owner=f'worker{idx}', agent_id=f'agent{idx}', fingerprint=f'fp{idx}', ttl_seconds=2)
    results.append((idx, ok, info))


def test_concurrent_claims(tmp_path):
    # Ensure clean claims dir
    path = claims._path_for('stoybl bl bl 1', 'stoybl_list')
    try:
        import os
        os.remove(path)
    except Exception:
        pass

    threads = []
    results = []
    for i in range(6):
        t = threading.Thread(target=worker, args=(results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Exactly one should have succeeded
    successes = [r for r in results if r[1] is True]
    failures = [r for r in results if r[1] is False]
    assert len(successes) == 1, f"expected 1 success, got {len(successes)}; results={results}"
