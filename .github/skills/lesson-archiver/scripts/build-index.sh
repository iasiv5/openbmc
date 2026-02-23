#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

if [[ -f "$repo_root/docs/lessons/scripts/build_index.py" ]]; then
  python3 "$repo_root/docs/lessons/scripts/build_index.py"
else
  echo "ERROR: build_index.py not found under docs/lessons/scripts" >&2
  exit 2
fi
