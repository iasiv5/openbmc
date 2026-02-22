# Lesson Learned Hub (MVP)

This directory stores reusable engineering lessons for `meta-iasi` with
progressive disclosure:

- L0: index and summary (`index.yaml`)
- L1: process guidance (`checklist.md`, `schema.md`)
- L2: lesson entries (Markdown with YAML frontmatter)
- L3: deep analysis sections inside each lesson (optional)

## Scope

- Current MVP scope: `meta-iasi`
- Submission flow: GitHub PR first, direct git push allowed for maintainers
- This system does not change BitBake build flow

## Directory layout

- `checklist.md`: author/reviewer checklist
- `schema.md`: metadata contract and enums
- `templates/quick-lesson.md`: lightweight template
- `templates/deep-lesson.md`: detailed template
- `index.yaml`: generated lesson index (do not hand edit)

## Create a lesson

1. Copy a template from `templates/`
2. Fill YAML frontmatter per `schema.md`
3. Put file under `docs/lessons/entries/` (create if absent)
4. Run validation:
   - `python3 scripts/lessons/validate_lessons.py`
5. Rebuild index:
   - `python3 scripts/lessons/build_index.py`

## Metadata search examples

- By component: `grep -R "component: meta-iasi/u-boot" docs/lessons/entries`
- By tag: `grep -R "- provider-conflict" docs/lessons/entries`
- By sensitivity: `grep -R "sensitivity: confidential" docs/lessons/entries`

## Sensitive content policy

- `public`: full details allowed
- `internal`: redact sensitive values and topology
- `confidential`: keep only summary, impact, decision, and safe remediation steps

Do not commit secrets, tokens, private keys, customer identifiers, or internal
infrastructure credentials to lesson files.
