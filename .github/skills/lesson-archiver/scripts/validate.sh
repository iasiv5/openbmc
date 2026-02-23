#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

if [[ -f "$repo_root/docs/lessons/scripts/validate_lessons.py" ]]; then
  python3 "$repo_root/docs/lessons/scripts/validate_lessons.py"
else
  echo "ERROR: validate_lessons.py not found under docs/lessons/scripts" >&2
  exit 2
fi
