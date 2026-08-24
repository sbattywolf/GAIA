import os,uuid
from pathlib import Path
import httpx
from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel
app=FastAPI(title='ZEUS Safe Tools')
def auth(a):
 if a!='Bearer '+os.environ['ZEUS_TOOLS_TOKEN']:raise HTTPException(401)
@app.get('/health')
def health():return {'status':'ok'}
@app.get('/ha/states/summary')
async def summary(domain:str|None=None,authorization:str|None=Header(None)):
 auth(authorization);h={'Authorization':'Bearer '+os.environ['HOME_ASSISTANT_TOKEN']}
 async with httpx.AsyncClient(timeout=15) as c:r=await c.get(os.environ['HOME_ASSISTANT_BASE_URL'].rstrip('/')+'/api/states',headers=h);r.raise_for_status()
 return {'states':[x for x in r.json() if not domain or x.get('entity_id','').startswith(domain+'.')][:100]}
class Candidate(BaseModel):title:str;request:str;category:str='UNKNOWN'
@app.post('/backlog/candidates')
def candidate(b:Candidate,authorization:str|None=Header(None)):
 auth(authorization);p=Path('/data/backlog_candidates');p.mkdir(parents=True,exist_ok=True);name=f'{uuid.uuid4()}.md';(p/name).write_text(f'# {b.title}\n\n{b.request}\n',encoding='utf-8');return {'status':'created','file':name}
