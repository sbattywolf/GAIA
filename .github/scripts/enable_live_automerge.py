from pathlib import Path


def main():
    p = Path('.github/workflows/automerge-agent-dry-run.yml')
    if not p.exists():
        print('automerge-agent-dry-run.yml not found; aborting')
        raise SystemExit(1)
    s = p.read_text(encoding='utf8')
    s = s.replace("DRY_RUN: ${{ github.event.inputs.dry_run || 'true' }}", "DRY_RUN: 'false'")
    s = s.replace("DRY_RUN: 'true'", "DRY_RUN: 'false'")
    p.write_text(s, encoding='utf8')
    print('Updated workflow to set DRY_RUN to false')


if __name__ == '__main__':
    main()
