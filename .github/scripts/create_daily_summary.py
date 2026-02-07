import json
import datetime
import os


def main():
    path = 'doc/sprints/analysis/triage-metrics.ndjson'
    lines = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf8') as f:
            raw = f.read().strip()
            if raw:
                lines = raw.splitlines()
                last = [json.loads(l) for l in lines[-5:]]
            else:
                last = []
    else:
        last = []

    body = f"Auto-triage daily summary for {datetime.date.today().isoformat()}\n\n"
    for r in last:
        body += f"- {r.get('run_log')}: size={r.get('file_size')} empty={r.get('empty')} gist_uploaded={r.get('gist_uploaded')}\n"

    payload = {
        'title': f"Auto-triage Daily Summary {datetime.date.today().isoformat()}",
        'body': body,
        'labels': ['auto-triage']
    }

    with open('summary.json', 'w', encoding='utf8') as f:
        json.dump(payload, f)

    print('Wrote summary.json')


if __name__ == '__main__':
    main()
