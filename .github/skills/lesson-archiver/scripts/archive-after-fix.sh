#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <lesson-entry-path>" >&2
  exit 2
fi

entry_path="$1"
repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

if [[ "$entry_path" = /* ]]; then
  abs_entry="$entry_path"
else
  abs_entry="$repo_root/$entry_path"
fi

if [[ ! -f "$abs_entry" ]]; then
  echo "ERROR: lesson entry not found: $entry_path" >&2
  exit 2
fi

"$repo_root/.github/skills/lesson-archiver/scripts/validate.sh"
"$repo_root/.github/skills/lesson-archiver/scripts/build-index.sh"
"$repo_root/.github/skills/lesson-archiver/scripts/validate.sh"

echo "Archive flow completed: ${abs_entry#$repo_root/}"
