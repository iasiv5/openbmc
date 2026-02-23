---
name: fix-complete-sentinel
description: Detect whether a bug fix is likely completed and prompt for knowledge archival. Use when build/test reruns succeed after failure, when logs indicate task recovery, or when users state the fix is verified. Ask exactly once: "要不要归档这次经验？" If user confirms, hand off to lesson-archiver one-click flow.
---

# Fix Complete Sentinel

Detect fix-completion signals and trigger archival prompt at the right time.

## Workflow

1. Gather signals from terminal output, test/build status, and user confirmation text.
2. Evaluate with `scripts/detect_fix_complete.py`.
3. If result is `ready=true`, run one-click archival by default.
4. If you need prompt-only behavior, use `--no-execute` and ask once:
  - `要不要归档这次经验？`

## Required behavior

- Default to one-click execution when completion signal is strong.
- Ask once per fix cycle only in prompt-only mode (`--no-execute`).
- Prefer explicit success transitions (fail -> pass) over weak heuristics.
- Never auto-write a lesson without user confirmation.
- Keep this skill focused on detection and prompting; archival is owned by `lesson-archiver`.

## Script usage

- Detect from log file:
  - `.github/skills/fix-complete-sentinel/scripts/detect_fix_complete.py --log <path>`
- Detect from inline text:
  - `.github/skills/fix-complete-sentinel/scripts/detect_fix_complete.py --text "<content>"`
- Optional previous-failure context:
  - add `--had-failure`
- Detect + execute one-click archival (default):
  - `.github/skills/fix-complete-sentinel/scripts/next_action_after_detect.py --text "<content>" --had-failure --title "<title>" --component "<component>" --owner "<owner>" --applicability "<scope>"`
- Detect + prompt-only mode:
  - `.github/skills/fix-complete-sentinel/scripts/next_action_after_detect.py --text "<content>" --had-failure --no-execute`

## Integration note

On `ready=true`, the next step should be:

1. Ask `要不要归档这次经验？`
2. If yes, run `lesson-archiver` flow (`create_lesson.py` + `archive-after-fix.sh`).
