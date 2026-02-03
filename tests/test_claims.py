import os
import time
from scripts import claims


def setup_module():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    claims_dir = os.path.join(root, ".tmp", "claims")
    if os.path.exists(claims_dir):
        for f in os.listdir(claims_dir):
            try:
                os.remove(os.path.join(claims_dir, f))
            except Exception:
                pass
    else:
        os.makedirs(claims_dir)


def test_claim_and_conflict():
    s = "StoryA"
    t = "Todo1"
    ok, data = claims.claim(s, t, "ownerA", "agentA", "fpA", ttl_seconds=60)
    assert ok
    ok2, reason = claims.claim(s, t, "ownerB", "agentB", "fpB", ttl_seconds=60)
    assert not ok2
    assert "already claimed" in reason
    info = claims.inspect_claim(s, t)
    assert info["owner"] == "ownerA"


def test_release_and_reclaim():
    s = "StoryB"
    t = "Todo2"
    ok, data = claims.claim(s, t, "ownerX", "agentX", "fpX", ttl_seconds=60)
    assert ok
    okr, msg = claims.release(s, t, agent_id="agentX")
    assert okr
    ok2, data2 = claims.claim(s, t, "ownerY", "agentY", "fpY", ttl_seconds=60)
    assert ok2


def test_ttl_expiry():
    s = "StoryTTL"
    t = "TodoTTL"
    ok, data = claims.claim(s, t, "owner1", "agent1", "fp1", ttl_seconds=1)
    assert ok
    time.sleep(1.1)
    ok2, data2 = claims.claim(s, t, "owner2", "agent2", "fp2", ttl_seconds=60)
    assert ok2
