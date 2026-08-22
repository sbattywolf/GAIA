#!/usr/bin/env bash
set -u
set -o pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$ROOT" ]]; then
  echo "ERROR: must run inside the GAIA repository." >&2
  exit 10
fi
cd "$ROOT"

source "$(dirname "$0")/../config/defaults.env"

REMOTE="${REMOTE:-origin}"
BRANCH="${BRANCH:-ING_3090}"
VALIDATION_TARGET="${VALIDATION_TARGET:-1070}"
RUNNER="${RUNNER:-gaia_1070_physical_validation/run_1070_validation.sh}"
EVIDENCE_FILE="${EVIDENCE_FILE:-validation_evidence.json}"
PUSH_EVIDENCE="${PUSH_EVIDENCE:-0}"
EXPECTED_COMMIT="${EXPECTED_COMMIT:-}"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="gaia_1070_evidence/runs/${TS}"
mkdir -p "$RUN_DIR"

fail() {
  echo "ERROR: $*" | tee "$RUN_DIR/framework_error.txt" >&2
  exit 10
}

echo "GAIA 1070 OPERATOR EVIDENCE RUNNER"
echo "=================================="

git branch --show-current > "$RUN_DIR/branch.txt"
git rev-parse HEAD > "$RUN_DIR/head_before.txt"
git status --short > "$RUN_DIR/status_before.txt"
git remote -v > "$RUN_DIR/remotes.txt"

CURRENT_BRANCH="$(cat "$RUN_DIR/branch.txt")"
if [[ "$CURRENT_BRANCH" != "$BRANCH" ]]; then
  fail "current branch is '$CURRENT_BRANCH', expected '$BRANCH'."
fi

if grep -qE '^[ MADRCU?]{1,2} ' "$RUN_DIR/status_before.txt"; then
  echo "Working tree is not clean; untracked runtime artifacts are allowed."
  if git status --short | grep -E '^[ MARCUD?]{1,2} ' | grep -vE '^\?\? '; then
    fail "tracked modifications detected; refusing automatic pull/push."
  fi
fi

echo "== FETCH =="
git fetch "$REMOTE" "$BRANCH" --prune 2>&1 | tee "$RUN_DIR/fetch.log" || fail "fetch failed"

REMOTE_SHA="$(git rev-parse "refs/remotes/${REMOTE}/${BRANCH}")"
echo "$REMOTE_SHA" > "$RUN_DIR/remote_sha.txt"

if [[ -n "$EXPECTED_COMMIT" && "$REMOTE_SHA" != "$EXPECTED_COMMIT" ]]; then
  fail "remote branch SHA $REMOTE_SHA does not match EXPECTED_COMMIT $EXPECTED_COMMIT"
fi

LOCAL_SHA="$(git rev-parse HEAD)"
if [[ "$LOCAL_SHA" != "$REMOTE_SHA" ]]; then
  echo "== FAST-FORWARD =="
  git pull --ff-only "$REMOTE" "$BRANCH" 2>&1 | tee "$RUN_DIR/pull.log" || \
    fail "fast-forward pull failed"
fi

FINAL_SHA="$(git rev-parse HEAD)"
echo "$FINAL_SHA" > "$RUN_DIR/head_after_pull.txt"

if [[ -n "$EXPECTED_COMMIT" && "$FINAL_SHA" != "$EXPECTED_COMMIT" ]]; then
  fail "checked-out SHA $FINAL_SHA does not match EXPECTED_COMMIT $EXPECTED_COMMIT"
fi

test -x "$RUNNER" || fail "runner not executable: $RUNNER"

echo "== RUNTIME SNAPSHOT =="
{
  echo "timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "commit=$FINAL_SHA"
  echo "hostname=$(hostname)"
  echo "kernel=$(uname -sr)"
  echo
  echo "[nvidia-smi]"
  nvidia-smi --query-gpu=name,memory.total --format=csv 2>&1 || true
  echo
  echo "[docker]"
  docker version --format '{{.Server.Version}}' 2>&1 || true
  echo
  echo "[ollama]"
  curl -sS --max-time 10 http://127.0.0.1:11434/api/tags 2>&1 || true
} | tee "$RUN_DIR/runtime_snapshot.txt"

echo "== VALIDATION =="
set +e
VALIDATION_TARGET="$VALIDATION_TARGET" \
  "$RUNNER" 2>&1 | tee "$RUN_DIR/validation.log"
RUN_EXIT="${PIPESTATUS[0]}"
set -e
echo "$RUN_EXIT" > "$RUN_DIR/validation_exit.txt"

if [[ -f "$EVIDENCE_FILE" ]]; then
  cp "$EVIDENCE_FILE" "$RUN_DIR/validation_evidence.json"
  if command -v jq >/dev/null 2>&1; then
    jq empty "$RUN_DIR/validation_evidence.json" >/dev/null 2>&1 || \
      echo "WARNING: validation_evidence.json is not valid JSON" > "$RUN_DIR/evidence_warning.txt"
  fi
else
  echo "validation_evidence.json NOT GENERATED" > "$RUN_DIR/evidence_missing.txt"
fi

# Ensure validation.log is properly referenced in the final report
if [[ -f "$RUN_DIR/validation.log" ]]; then
  echo "validation.log PERSISTED" > "$RUN_DIR/validation_log_status.txt"
else
  echo "validation.log NOT PERSISTED" > "$RUN_DIR/validation_log_status.txt"
fi

OVERALL="UNKNOWN"
if [[ -f "$RUN_DIR/validation_evidence.json" ]] && command -v jq >/dev/null 2>&1; then
  OVERALL="$(jq -r '.overall_status // .status // "UNKNOWN"' "$RUN_DIR/validation_evidence.json" 2>/dev/null || echo UNKNOWN)"
fi

cat > "$RUN_DIR/GAIA_1070_EVIDENCE_HANDOFF.md" <<EOF
# GAIA 1070 Evidence Handoff

## Checkpoint
- branch: $BRANCH
- commit: $FINAL_SHA
- target: $VALIDATION_TARGET

## Runtime
- hostname: $(hostname)
- validation exit code: $RUN_EXIT
- evidence file generated: $([[ -f "$RUN_DIR/validation_evidence.json" ]] && echo YES || echo NO)
- evidence status: $OVERALL

## Evidence Classification
The report records runtime observations only. Missing evidence is not
converted into PASS.

## Artifacts
- validation.log (persisted: $([[ -f "$RUN_DIR/validation_log_status.txt" ]] && grep -q "PERSISTED" "$RUN_DIR/validation_log_status.txt" && echo YES || echo NO))
- runtime_snapshot.txt
- validation_exit.txt
- validation_evidence.json (when generated)

## Source
This run was performed by the 1070 operator-side evidence handoff framework.
EOF

echo "== RESULT =="
cat "$RUN_DIR/GAIA_1070_EVIDENCE_HANDOFF.md"

if [[ "$PUSH_EVIDENCE" == "1" ]]; then
  echo "== EVIDENCE PUSH =="
  git status --short > "$RUN_DIR/status_before_push.txt"

  # Stage only this run's report/evidence.
  git add "$RUN_DIR"

  if git diff --cached --name-only | grep -v "^${RUN_DIR}/" >/dev/null; then
    git reset
    fail "unexpected files staged; refusing evidence push"
  fi

  git diff --cached --check || {
    git reset
    fail "staged evidence has whitespace errors"
  }

  git commit -m "GAIA: record 1070 validation evidence" || {
    git reset
    fail "evidence commit failed"
  }

  git push "$REMOTE" "$BRANCH" || fail "evidence push failed"

  LOCAL_PUSH_SHA="$(git rev-parse HEAD)"
  REMOTE_PUSH_SHA="$(git ls-remote "$REMOTE" "refs/heads/$BRANCH" | awk '{print $1}')"

  echo "local_push_sha=$LOCAL_PUSH_SHA" > "$RUN_DIR/push_verification.txt"
  echo "remote_push_sha=$REMOTE_PUSH_SHA" >> "$RUN_DIR/push_verification.txt"

  [[ "$LOCAL_PUSH_SHA" == "$REMOTE_PUSH_SHA" ]] || \
    fail "remote SHA does not match local pushed SHA"
fi

echo
echo "RUN_DIR=$RUN_DIR"
echo "VALIDATION_EXIT=$RUN_EXIT"

# The validation result is the runner's result. Evidence absence is never
# silently mapped to PASS.
exit "$RUN_EXIT"