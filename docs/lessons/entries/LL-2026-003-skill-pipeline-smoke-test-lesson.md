---
id: LL-2026-003
title: Skill pipeline smoke test lesson
date: 2026-02-23
component: meta-iasi/skill
tags: [skill, automation, lesson]
topic: build
failure_mode: config-drift
impact: medium
confidence: validated
sensitivity: internal
status: draft
owner: iasi-bsp-team
applicability: machine=iasi-2700, layer=meta-iasi
symptoms:
  - manual archiving is repetitive
root_cause:
  - lack of one-click generation flow
fix:
  - added create_lesson.py plus wrappers
prevention:
  - standardize skill-based archival flow
links:
  - .github/skills/lesson-archiver/SKILL.md
---
## Summary

One-paragraph summary of what happened and why this lesson matters.

## Verification

- Evidence 1:
- Evidence 2:

## Reuse notes

- When to apply:
- When not to apply:
