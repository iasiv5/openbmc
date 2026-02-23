#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

if [[ -f "$repo_root/scripts/lessons/validate_lessons.py" ]]; then
  python3 "$repo_root/scripts/lessons/validate_lessons.py"
elif [[ -f "$repo_root/poky/scripts/lessons/validate_lessons.py" ]]; then
  python3 "$repo_root/poky/scripts/lessons/validate_lessons.py"
else
  echo "ERROR: validate_lessons.py not found under scripts/lessons or poky/scripts/lessons" >&2
  exit 2
fi
