import os
from pathlib import Path

def load_file(path):
 if not Path(path).exists(): return
 for raw in Path(path).read_text(encoding='utf-8').splitlines():
  s=raw.strip()
  if s and not s.startswith('#') and '=' in s:
   k,v=s.split('=',1);os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
def load(base):
 load_file(Path(base)/'.env');load_file(Path(base)/'.secrets.env')
def require(name):
 v=os.getenv(name,'').strip()
 if not v or v.upper().startswith(('REPLACE_','TODO_')): raise RuntimeError(f'Missing {name}')
 return v
