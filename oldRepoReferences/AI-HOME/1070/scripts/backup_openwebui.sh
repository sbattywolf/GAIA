#!/usr/bin/env bash
set -euo pipefail
: "${ZEUS_BACKUP_ROOT:?Set private backup root}"
VOL="${OPENWEBUI_VOLUME:-open_webui_data}";DEST="$ZEUS_BACKUP_ROOT/$(date +%Y%m%d-%H%M%S)";mkdir -p "$DEST"
docker stop open-webui;trap 'docker start open-webui >/dev/null 2>&1 || true' EXIT
docker run --rm -v "$VOL:/data:ro" -v "$DEST:/backup" alpine sh -c 'tar czf /backup/openwebui.tar.gz -C /data .'
docker start open-webui;trap - EXIT;sha256sum "$DEST/openwebui.tar.gz" > "$DEST/SHA256SUMS"
