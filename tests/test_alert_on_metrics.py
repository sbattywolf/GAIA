import json
from pathlib import Path


def test_evaluate_thresholds(tmp_path):
    metrics = {'telegram.retry.moved_permanent': 2, 'telegram.retry.attempt.error': 5}
    from scripts.alert_on_metrics import evaluate

    ok, details = evaluate(metrics, {'telegram.retry.moved_permanent': 1, 'telegram.retry.attempt.error': 10})
    assert ok is True
    assert 'telegram.retry.moved_permanent' in details
    assert 'telegram.retry.attempt.error' not in details


def test_read_metrics_and_no_alert(tmp_path, monkeypatch):
    # create a metrics file
    root = Path(__file__).resolve().parents[1]
    mfile = root / '.tmp' / 'metrics.json'
    mfile.parent.mkdir(parents=True, exist_ok=True)
    mfile.write_text(json.dumps({'telegram.retry.moved_permanent': 0}), encoding='utf-8')

    from scripts.alert_on_metrics import main

    # dry run should print 'No alerts' and exit 0
    rc = main(['--dry-run'])
    assert rc == 0
