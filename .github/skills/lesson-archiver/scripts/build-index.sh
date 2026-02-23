#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

if [[ -f "$repo_root/scripts/lessons/build_index.py" ]]; then
  python3 "$repo_root/scripts/lessons/build_index.py"
elif [[ -f "$repo_root/poky/scripts/lessons/build_index.py" ]]; then
  python3 "$repo_root/poky/scripts/lessons/build_index.py"
else
  echo "ERROR: build_index.py not found under scripts/lessons or poky/scripts/lessons" >&2
  exit 2
fi
