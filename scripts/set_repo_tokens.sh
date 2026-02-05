#!/usr/bin/env bash
# Usage: GITHUB_TOKEN_VALUE=xxx GITHUB_TOKEN_ORG_VALUE=yyy ./scripts/set_repo_tokens.sh sbattywolf/GAIA
set -euo pipefail
repo=${1:-sbattywolf/GAIA}

if [ -n "${GITHUB_TOKEN_VALUE:-}" ]; then
  echo "Setting GITHUB_TOKEN for $repo"
  gh secret set GITHUB_TOKEN --repo "$repo" --body "$GITHUB_TOKEN_VALUE"
else
  echo "GITHUB_TOKEN_VALUE not set. Skipping GITHUB_TOKEN"
fi

if [ -n "${GITHUB_TOKEN_ORG_VALUE:-}" ]; then
  echo "Setting GITHUB_TOKEN_ORG for $repo"
  gh secret set GITHUB_TOKEN_ORG --repo "$repo" --body "$GITHUB_TOKEN_ORG_VALUE"
else
  echo "GITHUB_TOKEN_ORG_VALUE not set. Skipping GITHUB_TOKEN_ORG"
fi

echo "Done."
