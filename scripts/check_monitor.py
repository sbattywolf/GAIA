#!/usr/bin/env python3
import sys, subprocess, socket, json
out = {}
# try psutil
try:
    import psutil
    procs = []
    for p in psutil.process_iter(['pid','name','create_time','cmdline']):
        info = p.info
        procs.append(info)
    out['psutil']=True
    out['processes']=procs
except Exception as e:
    out['psutil']=False
    # fallback wmic
    try:
        p = subprocess.run(['wmic','process','get','ProcessId,CommandLine','/format:list'], capture_output=True, text=True, timeout=30)
        lines = p.stdout.splitlines()
        procs=[]
        cur = {}
        for line in lines:
            if not line.strip():
                if cur:
                    procs.append(cur)
                    cur={}
            else:
                if '=' in line:
                    k,v = line.split('=',1)
                    cur[k]=v
        if cur:
            procs.append(cur)
        out['processes_wmic']=procs
    except Exception as e2:
        out['wmic_error']=str(e2)

# filter processes with monitor/app.py or 'monitor' and 'app.py'
matches=[]
if out.get('psutil'):
    for p in out.get('processes',[]):
        cmd = ' '.join(p.get('cmdline') or [])
        pid = p.get('pid')
        if cmd and ('monitor' in cmd and 'app.py' in cmd):
            matches.append({'pid':pid,'cmdline':cmd})
else:
    for p in out.get('processes_wmic',[]):
        cmd = p.get('CommandLine','')
        pid = p.get('ProcessId')
        if cmd and ('monitor' in cmd and 'app.py' in cmd):
            matches.append({'pid':pid,'cmdline':cmd})
out['monitor_matches']=matches

# netstat
try:
    p = subprocess.run(['netstat','-ano'], capture_output=True, text=True)
    lines = [l for l in p.stdout.splitlines() if ':5000' in l]
    out['netstat_port5000']=lines
except Exception as e:
    out['netstat_error']=str(e)

# try TCP connect
sres = {}
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(('127.0.0.1',5000))
        sres['connect']=True
    except Exception as e:
        sres['connect']=False
        sres['error']=str(e)
    s.close()
except Exception as e:
    sres['socket_error']=str(e)
out['socket_test']=sres

print(json.dumps(out, indent=2, default=str))
