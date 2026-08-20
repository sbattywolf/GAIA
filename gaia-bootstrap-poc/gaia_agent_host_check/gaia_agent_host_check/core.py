from dataclasses import dataclass, asdict
from pathlib import Path
from shutil import which
import os, re, subprocess, time

CLASSES={"OBSERVED","INFERRED","HISTORICAL","RECOMMENDED","UNRESOLVED"}

@dataclass
class Observation:
    module:str
    key:str
    status:str
    evidence_class:str
    value:object
    source:str
    warnings:list
    def __post_init__(self):
        if self.evidence_class not in CLASSES: raise ValueError("invalid evidence class")

def envelope(obs,status="PASS"):
    return {"schema_version":"0.3","status":status,
            "security":{"SECRET_VALUES_COLLECTED":"NO","MUTATION_OPERATIONS":"NONE"},
            "observations":[asdict(x) for x in obs]}

def command_exists(name): return which(name) is not None

def host_discovery():
    u=os.uname(); mem={}
    p=Path("/proc/meminfo")
    if p.exists():
        for line in p.read_text(errors="replace").splitlines():
            if ":" in line: k,v=line.split(":",1); mem[k]=v.strip()
    return [Observation("host","hostname","PASS","OBSERVED",u.nodename,"os.uname",[]),
            Observation("host","kernel","PASS","OBSERVED",u.release,"os.uname",[]),
            Observation("host","architecture","PASS","OBSERVED",u.machine,"os.uname",[]),
            Observation("host","memory_total","PASS" if mem else "UNKNOWN","OBSERVED",mem.get("MemTotal","UNKNOWN"),"/proc/meminfo",[])]

def software_discovery():
    names=["python3","git","curl","jq","docker","nvidia-smi","ollama","pytest"]
    return [Observation("software","command."+n,"PASS" if command_exists(n) else "UNKNOWN","OBSERVED",command_exists(n),"PATH",[]) for n in names]

def classify_compose(plugin,legacy):
    return "DOCKER_COMPOSE_PLUGIN" if plugin else ("DOCKER_COMPOSE_LEGACY_BINARY" if legacy else "COMPOSE_CAPABILITY_UNKNOWN")

def runtime_source(native,container):
    return "NATIVE" if native and not container else ("CONTAINER" if container and not native else "UNKNOWN")

def model_inventory(text):
    rows=[]
    for line in text.splitlines()[1:]:
        parts=re.split(r"\s{2,}",line.strip())
        if len(parts)>=2: rows.append({"name":parts[0],"metadata":parts[1:]})
    return [Observation("models",f"model.{i}","PASS","OBSERVED",x,"ollama",[]) for i,x in enumerate(rows)]

REQ={"home_collaborator":["python","git","model_runtime"],
     "coding_agent":["python","git","test_runner"],
     "vision_agent":["python","model_runtime"],
     "voice_agent":["python","model_runtime"]}

def skill_precheck(skill,available):
    req=REQ.get(skill,[]); missing=[x for x in req if x not in available]
    return [Observation("skills","prerequisites","BLOCKED" if missing else "PASS","OBSERVED",
                         {"required":req,"missing":missing},"skill_precheck",[])]

def script_scope(root,scope):
    root=Path(root)
    if not root.exists(): return [Observation("scripts","scope","UNKNOWN","UNRESOLVED",str(root),"config",["path missing"])]
    files=sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())
    return [Observation("scripts",scope+".files","PASS","OBSERVED",files,"filesystem",[])]

def security_metadata(paths):
    return [Observation("security","secret."+Path(p).name,"PASS","OBSERVED",
                         {"SECRET_PRESENT":"YES" if Path(p).exists() else "NO",
                          "SOURCE":str(Path(p)),"VALUE":"REDACTED"},"metadata",[]) for p in paths]

def monitoring_snapshot():
    return {"timestamp":time.time(),"memory_source":"/proc/meminfo"}

def benchmark_state(skip,requested):
    return "BLOCKED" if skip and requested else ("READY" if requested else "SKIPPED")

def package_sanitized(root):
    bad=[]
    for p in Path(root).rglob("*"):
        if not p.is_file(): continue
        r=str(p.relative_to(root))
        if "__pycache__" in r or ".pytest_cache" in r or p.suffix in {".pyc",".pem",".key",".p12",".pfx"} or p.name in {".env",".secrets.env"}:
            bad.append(r)
        if re.search(rb"(?i)BEGIN PRIVATE KEY|bearer\s+[A-Za-z0-9._~+/=-]{12,}",p.read_bytes()):
            bad.append(r)
    return not bad, sorted(set(bad))

def git_preflight(repo):
    repo=Path(repo)
    if not (repo/".git").exists():
        return [Observation("git","repository","BLOCKED","OBSERVED",False,str(repo),["not a repository"])]
    out=[]
    for key,args in [("status",["git","status","--short"]),("branch",["git","branch","--show-current"]),("head",["git","rev-parse","HEAD"])]:
        try:
            c=subprocess.run(args,cwd=repo,capture_output=True,text=True,shell=False,timeout=10)
            out.append(Observation("git",key,"PASS" if c.returncode==0 else "BLOCKED","OBSERVED",c.stdout.strip() if c.returncode==0 else "UNKNOWN","git",[]))
        except Exception as e:
            out.append(Observation("git",key,"BLOCKED","UNRESOLVED","UNKNOWN","git",[type(e).__name__]))
    return out
