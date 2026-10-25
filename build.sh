#!/usr/bin/env bash
# Builds the .skill files to upload in Claude (Settings → Capabilities → Skills): a zip of each skill folder.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf dist && mkdir -p dist
for s in job-prospecting job; do
  (cd skills && python3 -c "
import sys, zipfile, pathlib
nom = sys.argv[1]
with zipfile.ZipFile(f'../dist/{nom}.skill', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(pathlib.Path(nom).rglob('*')):
        if f.is_file():
            z.write(f, f.as_posix())
" "$s")
  echo "dist/$s.skill"
done
