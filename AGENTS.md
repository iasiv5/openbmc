# AGENTS

This repository supports a structured Lesson Learned workflow. Agents should use
progressive disclosure to reduce context usage.

## Scope

- MVP focus: `meta-iasi`
- Lesson source: `docs/lessons/`

## Retrieval strategy (progressive disclosure)

1. Read summary first:
   - `docs/lessons/README.md`
   - `docs/lessons/index.yaml`
2. Filter by metadata:
   - `component`, `tags`, `topic`, `failure_mode`, `sensitivity`
3. Read full lesson body only when matched
4. Prefer lessons in this order:
   - `confidence=validated`
   - newest `date`
   - exact component match

## Sensitive handling

- `public`: full details allowed
- `internal`: redact values if possible
- `confidential`: only provide summary, impact, decision, and safe remediation

Never output secrets, private keys, credentials, or internal identifiers.

## Authoring policy

When adding or updating lessons:
- Follow `docs/lessons/schema.md`
- Run `python3 scripts/lessons/validate_lessons.py`
- Run `python3 scripts/lessons/build_index.py`
- Follow `docs/lessons/checklist.md`
