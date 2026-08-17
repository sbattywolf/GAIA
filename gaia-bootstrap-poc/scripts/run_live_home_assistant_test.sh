#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${GAIA_CONFIG_DIR:-$HOME/.config/gaia}"
PUBLIC_ENV="${CONFIG_DIR}/home_assistant.env"
SECRETS_ENV="${CONFIG_DIR}/.secrets.env"

if [[ ! -f "${PUBLIC_ENV}" ]]; then
  echo "Missing ${PUBLIC_ENV}" >&2
  exit 1
fi

if [[ ! -f "${SECRETS_ENV}" ]]; then
  echo "Missing ${SECRETS_ENV}" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "${PUBLIC_ENV}"
# shellcheck disable=SC1090
source "${SECRETS_ENV}"
set +a

required_vars=(
  HOME_ASSISTANT_BASE_URL
  HOME_ASSISTANT_TOKEN
  GAIA_HA_ENTITY_ID
)

for name in "${required_vars[@]}"; do
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required runtime variable: ${name}" >&2
    exit 1
  fi
done

exec env \
  GAIA_HA_URL="${HOME_ASSISTANT_BASE_URL}" \
  GAIA_HA_TOKEN="${HOME_ASSISTANT_TOKEN}" \
  GAIA_HA_ENTITY_ID="${GAIA_HA_ENTITY_ID}" \
  python -m pytest -m integration \
    gaia-bootstrap-poc/tests/test_real_home_assistant_integration.py
