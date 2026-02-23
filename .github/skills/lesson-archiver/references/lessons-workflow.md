# Lesson Workflow Reference

This file centralizes pointers to repository-owned lesson rules.

## Source of truth (do not duplicate)

- Schema: `docs/lessons/schema.md`
- Checklist: `docs/lessons/checklist.md`
- Hub guide: `docs/lessons/README.md`
- Agent retrieval and sensitivity policy: `AGENTS.md`

## Template decision tree

- Use `docs/lessons/templates/quick-lesson.md` when:
  - single bug/fix path
  - limited blast radius
  - straightforward remediation and verification
- Use `docs/lessons/templates/deep-lesson.md` when:
  - high/critical impact
  - cross-component behavior
  - recurring issue or non-obvious diagnosis

## Post-fix archive handshake

After fix verification (build/test pass or explicit user confirmation), ask:

`要不要归档？`

- If user says yes:
  1. draft lesson entry in `docs/lessons/entries/`
  - Example: `.github/skills/lesson-archiver/scripts/create_lesson.py --type quick --title "<title>" --component "<component>" --owner "<owner>" --applicability "<scope>"`
  2. run `archive-after-fix.sh <entry-file>`
  3. report file path + validation result + index update status
- If user says no:
  - skip with a one-line reason when available

## Quality baseline

- All required frontmatter fields present
- `id` format `LL-YYYY-NNN`
- No sensitive leakage
- Links are traceable to code/issue/PR/log
