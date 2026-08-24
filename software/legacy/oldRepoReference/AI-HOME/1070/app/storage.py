import json,uuid,re
from datetime import datetime,timezone
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
LOG=BASE/'logs';BACKLOG=BASE/'artifacts'/'backlog_candidates'
def rid():return str(uuid.uuid4())
def now():return datetime.now(timezone.utc).isoformat()
def log(record):
 LOG.mkdir(parents=True,exist_ok=True)
 with (LOG/'request_log.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
def backlog(record):
 BACKLOG.mkdir(parents=True,exist_ok=True);slug=re.sub(r'[^A-Za-z0-9_-]+','_',record['action'])[:40]
 p=BACKLOG/f"{record['timestamp'][:10]}_{slug}_{record['request_id'][:8]}.md"
 p.write_text(f"# Zeus Candidate\n\n{record['message']}\n\nStatus: not executed\n",encoding='utf-8')
