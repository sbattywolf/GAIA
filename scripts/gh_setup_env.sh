#!/usr/bin/env bash
set -euo pipefail

# scripts/gh_setup_env.sh
# Create a GitHub environment named `production` for the current repo
# and set environment-scoped secrets `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
# Usage: ./scripts/gh_setup_env.sh [owner/repo]

REPO_ARG=${1:-}
REVIEWERS_ARG=${2:-}
if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install from https://cli.github.com/ and authenticate (gh auth login)."
  exit 1
fi

if [ -n "$REPO_ARG" ]; then
  REPO="$REPO_ARG"
else
  REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner) || {
    echo "Failed to detect repo. Pass owner/repo as first arg.";
    exit 1
  }
fi

echo "Using repo: $REPO"

# Create environment (no-op if exists)
echo "Creating environment 'production' (if not present)..."
set +e
gh api --method POST "/repos/$REPO/environments" -f name=production >/dev/null 2>&1
RC=$?
set -e
if [ $RC -eq 0 ]; then
  echo "Environment 'production' created."
else
  echo "Environment 'production' already exists or creation returned non-OK (continuing)."
fi

# Helper to read secret value (env var preferred, otherwise prompt)
read_secret() {
  name=$1
  envval=$(printf '%s' "${!name-}")
  if [ -n "$envval" ]; then
    printf '%s' "$envval"
    return
  fi
  # prompt user
  read -rp "Enter $name (will be stored in GitHub environment 'production'): " inputval
  printf '%s' "$inputval"
}

TELEGRAM_BOT_TOKEN_VAL=$(read_secret TELEGRAM_BOT_TOKEN)
TELEGRAM_CHAT_ID_VAL=$(read_secret TELEGRAM_CHAT_ID)

if [ -z "$TELEGRAM_BOT_TOKEN_VAL" ] || [ -z "$TELEGRAM_CHAT_ID_VAL" ]; then
  echo "Both TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required to set environment secrets."
  echo "You can also set them in the environment before running this script (export TELEGRAM_BOT_TOKEN=... and export TELEGRAM_CHAT_ID=...)."
  exit 1
fi

echo "Setting environment-scoped secrets in GitHub (production)..."
# Use gh secret set with --env to store secrets scoped to the environment
printf '%s' "$TELEGRAM_BOT_TOKEN_VAL" | gh secret set TELEGRAM_BOT_TOKEN --env production --repo "$REPO" >/dev/null
printf '%s' "$TELEGRAM_CHAT_ID_VAL" | gh secret set TELEGRAM_CHAT_ID --env production --repo "$REPO" >/dev/null

echo "Secrets set for environment 'production'."

echo "Next recommended steps:"
echo "- In the GitHub repo UI: Settings → Environments → production → configure protection rules (add required reviewers and a wait timer)."
echo "  You can open the repo settings page with:"
echo "    gh repo view --web"
echo "- Alternatively, add required reviewers via the GitHub web UI (their user/team names)."

echo "Done. After adding required reviewers you can run the protected workflow 'real-send.yml' manually from Actions."

# If REVIEWERS were provided (env $REVIEWERS or 2nd arg), attempt to set protection required_reviewers
REVIEWERS_VAL=""
if [ -n "${REVIEWERS_ARG-}" ]; then
  REVIEWERS_VAL="$REVIEWERS_ARG"
elif [ -n "${REVIEWERS-}" ]; then
  REVIEWERS_VAL="$REVIEWERS"
fi

if [ -n "$REVIEWERS_VAL" ]; then
  echo "Attempting to set required reviewers for environment 'production': $REVIEWERS_VAL"
  IFS=',' read -r -a _rarr <<< "$REVIEWERS_VAL"
  reviewers_json='['
  first=true
  for r in "${_rarr[@]}"; do
    r_trimmed=$(echo "$r" | sed 's/^ *//;s/ *$//')
    if [ "$first" = true ]; then
      first=false
    else
      reviewers_json+="," 
    fi
    reviewers_json+="{\"type\":\"User\",\"login\":\"$r_trimmed\"}"
  done
  reviewers_json+=']'
  full_json="{\"reviewers\":$reviewers_json,\"dismiss_stale_reviews\":false,\"require_code_owner_reviews\":false}"

  set +e
  gh api --method PUT "/repos/$REPO/environments/production/protection/required_reviewers" -f "$full_json" -H "Accept: application/vnd.github+json" >/dev/null 2>&1
  RC=$?
  set -e
  if [ $RC -eq 0 ]; then
    echo "Protection rules updated successfully."
  else
    echo "Failed to set protection rules (exit $RC). Ensure you have repo admin rights."
  fi
fi
