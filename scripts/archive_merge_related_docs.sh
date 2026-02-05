#!/usr/bin/env bash
set -euo pipefail

# Safe archival script: copy merge/draft-related docs into doc/archive/ with timestamped names
mkdir -p doc/archive
ts=$(date -u +%Y%m%d%H%M)
patterns=("*.draft*" "*stoy_auto.draft.json" "STR_Telegram.draft")

for pat in "${patterns[@]}"; do
  while IFS= read -r -d $'\0' f; do
    name=$(basename "$f")
    dest="doc/archive/${name}.archived.${ts}"
    echo "Archiving $f -> $dest"
    cp -a "$f" "$dest"
  done < <(find doc -type f -name "$pat" -print0)
done

echo "Archival complete. Review files in doc/archive/. To remove originals, run with --delete-originals after review."
