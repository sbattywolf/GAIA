import os
import json
from glob import glob
from scripts import claims_sqlite

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLAIMS_DIR = os.path.join(ROOT, ".tmp", "claims")


def migrate():
    files = glob(os.path.join(CLAIMS_DIR, "*.json"))
    if not files:
        print("No claim JSON files found to migrate.")
        return
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as e:
            print(f"Skipping {f}: failed to read ({e})")
            continue
        story_t = os.path.basename(f).rsplit(".json", 1)[0]
        # stored name format: story.todolist.json
        if "." in story_t:
            story, todolist = story_t.split(".", 1)
        else:
            story, todolist = story_t, "default"
        # attempt to insert as a claim if not present
        existing = claims_sqlite.inspect_claim(story, todolist)
        if existing:
            print(f"Skipping {f}: claim exists for {story}/{todolist}")
            continue
        owner = data.get("owner")
        agent_id = data.get("agent_id")
        fingerprint = data.get("fingerprint")
        ttl = data.get("ttl_seconds", 300)
        ok, res = claims_sqlite.claim(story, todolist, owner, agent_id, fingerprint, ttl_seconds=ttl)
        if ok:
            print(f"Migrated {f} -> {story}/{todolist}")
        else:
            print(f"Failed to migrate {f}: {res}")


if __name__ == "__main__":
    migrate()
