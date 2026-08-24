#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)";set -a;. "$BASE/.env";. "$BASE/.secrets.env";set +a
curl -fsS -H "Authorization: Bearer $OPENWEBUI_API_KEY" "$OPENWEBUI_URL/api/v1/models/export" | python3 -m json.tool > "$BASE/openwebui/exported-models.json"
