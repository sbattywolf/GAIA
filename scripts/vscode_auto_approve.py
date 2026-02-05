#!/usr/bin/env python3
"""Auto-approve the GitHub Pull Request for the current branch using `gh`.

Usage: run this from the workspace root. Requires `gh` and `git` on PATH and
an authenticated `gh` session (e.g., `gh auth login`).
"""
import subprocess
import sys

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def main():
    try:
        # Get the current branch name
        branch = run("git rev-parse --abbrev-ref HEAD")
    except subprocess.CalledProcessError:
        print("Error: cannot determine current git branch", file=sys.stderr)
        sys.exit(2)

    try:
        # gh pr view will return the PR for the current branch when present
        pr_num = run("gh pr view --json number --jq .number")
    except subprocess.CalledProcessError:
        print(f"No open pull request found for branch: {branch}", file=sys.stderr)
        sys.exit(3)

    if not pr_num or pr_num == "null":
        print(f"No open pull request found for branch: {branch}")
        sys.exit(0)

    print(f"Found PR #{pr_num} for branch {branch}.")
    # Simple confirmation prompt to avoid accidental approvals
    try:
        resp = input(f"Approve PR #{pr_num}? [y/N]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("Aborted by user.")
        sys.exit(1)

    if resp not in ("y", "yes"):
        print("Approval cancelled.")
        sys.exit(0)

    try:
        out = run(f"gh pr review {pr_num} --approve --body \"Auto-approved via VS Code task\"")
        print(out)
        print(f"PR #{pr_num} approved.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print("Failed to approve PR:", e, file=sys.stderr)
        sys.exit(4)

if __name__ == '__main__':
    main()
