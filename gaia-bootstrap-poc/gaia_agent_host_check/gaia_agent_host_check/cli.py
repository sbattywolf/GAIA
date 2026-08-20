import argparse,json
from pathlib import Path
from .core import *
MODULES=["host","software","runtime","containers","models","skills","scripts","security","git","monitoring","benchmark","tests","evidence","package"]

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--profile",choices=["generic","1070","3090"],default="generic")
    p.add_argument("--skill-profile",choices=list(REQ))
    p.add_argument("--runtime",choices=["auto","native","container"],default="auto")
    p.add_argument("--modules",nargs="+",choices=MODULES)
    p.add_argument("--skip",nargs="+",choices=MODULES,default=[])
    p.add_argument("--target-gaia-repo",default="UNKNOWN")
    p.add_argument("--target-legacy-repo",default="UNKNOWN")
    p.add_argument("--benchmark",action="store_true")
    p.add_argument("--skip-benchmark",action="store_true")
    p.add_argument("--json-out",type=Path)
    p.add_argument("--report-out",type=Path)
    a=p.parse_args(argv)
    selected=MODULES if a.modules is None else a.modules
    selected=[x for x in selected if x not in a.skip]
    o=[]
    if "host" in selected:o+=host_discovery()
    if "software" in selected:o+=software_discovery()
    if "runtime" in selected:
        o += [Observation("runtime","mode","PASS","INFERRED",a.runtime,"cli",[]),
              Observation("runtime","profile","PASS","OBSERVED",a.profile,"cli",[])]
    if "skills" in selected and a.skill_profile:
        available={"python" if command_exists("python3") else "",
                   "git" if command_exists("git") else "",
                   "test_runner" if command_exists("pytest") else ""}
        if command_exists("ollama"): available.add("model_runtime")
        o += skill_precheck(a.skill_profile,available)
    if "scripts" in selected:
        if a.target_gaia_repo!="UNKNOWN": o+=script_scope(a.target_gaia_repo,"GAIA")
        if a.target_legacy_repo!="UNKNOWN": o+=script_scope(a.target_legacy_repo,"LEGACY")
    if "security" in selected and a.target_gaia_repo!="UNKNOWN":
        o += security_metadata([Path(a.target_gaia_repo)/".env"])
    if "git" in selected and a.target_gaia_repo!="UNKNOWN":
        o += git_preflight(Path(a.target_gaia_repo))
    if "monitoring" in selected:
        o.append(Observation("monitoring","snapshot","PASS","OBSERVED",monitoring_snapshot(),"/proc",[]))
    if "benchmark" in selected:
        o.append(Observation("benchmark","state","PASS","RECOMMENDED",benchmark_state(a.skip_benchmark,a.benchmark),"cli",[]))
    e=envelope(o)
    report="SECRET_VALUES_COLLECTED=NO\nMUTATION_OPERATIONS=NONE\n"+"\n".join(f"{x.module}/{x.key}={x.status}" for x in o)+"\n"
    if a.json_out: a.json_out.write_text(json.dumps(e,indent=2),encoding="utf-8")
    if a.report_out: a.report_out.write_text(report,encoding="utf-8")
    print(report,end="")
if __name__=="__main__": main()
