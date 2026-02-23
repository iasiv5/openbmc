---
name: lesson-archiver
description: Generate and archive compliant Lesson Learned entries for bug fixes in this repository. Use when users ask to create lesson learned, archive a fix, write postmortem-style lessons, summarize bug fixes into reusable knowledge, or update lesson index/checklist. After fix verification, ask once: "要不要归档？" and support one-click flow: create entry -> validate -> build index.
---

# Lesson Archiver

Use this skill to create or update lesson entries under `docs/lessons/entries/`.

## Workflow

1. Read summary and policy first:
   - `docs/lessons/README.md`
   - `docs/lessons/index.yaml`
   - `AGENTS.md`
2. Load detailed constraints only when needed:
   - `references/lessons-workflow.md`
3. Collect fix context:
   - symptom, root cause, changed files, validation evidence, links
4. Decide template:
   - quick lesson for normal single-issue fixes
   - deep lesson for high-impact/cross-component/recurrent issues
5. Ask once after fix is verified:
   - `要不要归档？`
6. If confirmed, archive in one flow:
   - create lesson entry
   - run `scripts/archive-after-fix.sh <entry-file>`

## Required behavior

- Follow `docs/lessons/schema.md` and `docs/lessons/checklist.md`.
- Use progressive disclosure; avoid loading all lessons unless needed.
- Respect sensitivity policy:
  - `public`: full details allowed
  - `internal`: redact sensitive values
  - `confidential`: keep summary, impact, decision, safe remediation only
- Never include secrets, credentials, private keys, or internal identifiers.

## Script usage

- Create a lesson entry:
   - `.github/skills/lesson-archiver/scripts/create_lesson.py --type quick --title "<title>" --component "<component>" --owner "<owner>" --applicability "<scope>"`
- Validate only:
  - `.github/skills/lesson-archiver/scripts/validate.sh`
- Build index only:
  - `.github/skills/lesson-archiver/scripts/build-index.sh`
- Full archive flow:
  - `.github/skills/lesson-archiver/scripts/archive-after-fix.sh docs/lessons/entries/<file>.md`

## Integration note

When fix completion is detected by sentinel, bridge helper runs one-click archival by default and returns execution result:

- `.github/skills/fix-complete-sentinel/scripts/next_action_after_detect.py`
