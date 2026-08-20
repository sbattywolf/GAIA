#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${GAIA_CONFIG_DIR:-$HOME/.config/gaia}"
PUBLIC_ENV="${CONFIG_DIR}/home_assistant.env"
SECRETS_ENV="${CONFIG_DIR}/.secrets.env"
STATE_DIR="${GAIA_PM002_STATE_DIR:-${TMPDIR:-/tmp}/gaia-pm002}"
DISABLED="${STATE_DIR}/disabled"
READY="${STATE_DIR}/ready"

if [[ -f "${DISABLED}" ]]; then
  echo "PM-002 disabled; no external read performed" >&2
  exit 3
fi

[[ -f "${PUBLIC_ENV}" ]] || { echo "Missing ${PUBLIC_ENV}" >&2; exit 1; }
[[ -f "${SECRETS_ENV}" ]] || { echo "Missing ${SECRETS_ENV}" >&2; exit 1; }

set -a
# shellcheck disable=SC1090
source "${PUBLIC_ENV}"
# shellcheck disable=SC1090
source "${SECRETS_ENV}"
set +a

: "${HOME_ASSISTANT_BASE_URL:?Missing HOME_ASSISTANT_BASE_URL}"
: "${HOME_ASSISTANT_TOKEN:?Missing HOME_ASSISTANT_TOKEN}"
ENTITY_ID="${GAIA_PM002_ENTITY_ID:-light.living_room}"
MAX_AGE="${GAIA_PM002_MAX_AGE_SECONDS:-}"

mkdir -p "${STATE_DIR}"
rm -f "${DISABLED}"

export GAIA_PM002_BASE_URL="${HOME_ASSISTANT_BASE_URL}"
export GAIA_PM002_TOKEN="${HOME_ASSISTANT_TOKEN}"
export GAIA_PM002_ENTITY_ID="${ENTITY_ID}"
export GAIA_PM002_MAX_AGE_SECONDS="${MAX_AGE}"

PYTHONPATH="$(cd "$(dirname "$0")/../src" && pwd)" python3 - <<'PY'
import os
from datetime import timedelta
from gaia.adapters.home_assistant_http_transport import HomeAssistantHTTPTransport
from gaia.adapters.home_assistant_light_adapter import HomeAssistantLightAdapter
from gaia.core.request_router import Request, RequestRouter
from gaia.home.models import ResourceId
from gaia.w3 import LIVING_ROOM_LIGHT

entity_id = os.environ["GAIA_PM002_ENTITY_ID"]
if entity_id != LIVING_ROOM_LIGHT.external_reference.value:
    raise SystemExit("PM-002 only permits light.living_room")
max_age_raw = os.environ.get("GAIA_PM002_MAX_AGE_SECONDS", "")
max_age = timedelta(seconds=int(max_age_raw)) if max_age_raw else None
transport = HomeAssistantHTTPTransport(os.environ["GAIA_PM002_BASE_URL"], os.environ["GAIA_PM002_TOKEN"], timeout=5.0)
provider = HomeAssistantLightAdapter(transport, ResourceId("home.light.living_room"), max_age=max_age)
router = RequestRouter(home_collaborator=__import__("gaia.home.collaborator", fromlist=["HomeCollaborator"]).HomeCollaborator(__import__("gaia.home.read_current_resource_state", fromlist=["ReadCurrentResourceStateCapability"]).ReadCurrentResourceStateCapability(__import__("gaia.home.resource_resolver", fromlist=["HomeResourceResolver"]).HomeResourceResolver({"living-room light": (LIVING_ROOM_LIGHT,)}), provider)))
outcome = router.handle(Request(operation=RequestRouter.READ_CURRENT_RESOURCE_STATE, resource_label="living-room light"))
name = type(outcome).__name__
if name == "CurrentStateSuccess":
    name = outcome.observation.state.value
elif name == "InformationStale":
    name = "STALE"
elif name == "SourceUnavailable":
    name = "UNAVAILABLE"
elif name == "ExecutionFailure":
    name = "ERROR"
print(f"PM-002 READY outcome={name} resource=home.light.living_room")
PY

printf 'ready\n' > "${READY}"
printf '%s\n' "PM-002 started and validated with one read-only Light observation." 
