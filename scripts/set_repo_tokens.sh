#!/usr/bin/env bash
# Usage: GITHUB_TOKEN_VALUE=xxx GITHUB_TOKEN_ORG_VALUE=yyy ./scripts/set_repo_tokens.sh sbattywolf/GAIA
set -euo pipefail

repo=${1:-sbattywolf/GAIA}

if [ -n "${AUTOMATION_GITHUB_TOKEN_VALUE:-}" ]; then
  echo "Setting AUTOMATION_GITHUB_TOKEN for $repo"
  gh secret set AUTOMATION_GITHUB_TOKEN --repo "$repo" --body "$AUTOMATION_GITHUB_TOKEN_VALUE"
else
  echo "AUTOMATION_GITHUB_TOKEN_VALUE not set. Skipping AUTOMATION_GITHUB_TOKEN"
fi

if [ -n "${AUTOMATION_GITHUB_TOKEN_ORG_VALUE:-}" ]; then
  echo "Setting AUTOMATION_GITHUB_TOKEN_ORG for $repo"
  gh secret set AUTOMATION_GITHUB_TOKEN_ORG --repo "$repo" --body "$AUTOMATION_GITHUB_TOKEN_ORG_VALUE"
else
  echo "AUTOMATION_GITHUB_TOKEN_ORG_VALUE not set. Skipping AUTOMATION_GITHUB_TOKEN_ORG"
fi

echo "Done."
