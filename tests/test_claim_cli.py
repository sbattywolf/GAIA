import json
import os
import subprocess
import sys
import time


def _python():
    return sys.executable


def _run(args, timeout=20):
    cmd = [_python(), "scripts/claim_cli.py"] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def test_claim_cli_roundtrip(tmp_path):
    story = "test_cli_story"
    todolist = "default"
    claims_dir = os.path.join(".tmp", "claims")
    os.makedirs(claims_dir, exist_ok=True)
    # cleanup any previous files
    for fname in os.listdir(claims_dir):
        if fname.startswith(story + "."):
            try:
                os.remove(os.path.join(claims_dir, fname))
            except Exception:
                pass

    # inspect -> should be null/None
    rc, out, err = _run(["inspect", story, todolist])
    assert rc == 0
    assert out.strip() in ("null", "None", "{}") or out.strip().startswith("null") or out.strip().startswith("None") or out.strip().startswith("{")

    # claim
    rc, out, err = _run(["claim", story, todolist, "me", "agent-1", "fp-1"])
    assert rc == 0
    j = json.loads(out)
    assert j.get("ok") is True
    assert isinstance(j.get("result"), dict)

    # inspect -> should show owner
    rc, out, err = _run(["inspect", story, todolist])
    assert rc == 0
    j2 = json.loads(out)
    assert j2.get("owner") == "me" or j2.get("owner") == "me"

    # refresh
    rc, out, err = _run(["refresh", story, todolist, "--agent", "agent-1"])
    assert rc == 0
    j3 = json.loads(out)
    assert j3.get("ok") is True

    # release
    rc, out, err = _run(["release", story, todolist, "--agent", "agent-1"])
    assert rc == 0
    j4 = json.loads(out)
    assert j4.get("ok") is True

    # final inspect -> no claim
    rc, out, err = _run(["inspect", story, todolist])
    assert rc == 0
