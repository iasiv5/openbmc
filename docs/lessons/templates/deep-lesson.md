---
id: LL-YYYY-NNN
title: <short title>
date: YYYY-MM-DD
component: <layer/component>
tags: [tag1, tag2, tag3, tag4]
topic: build
failure_mode: provider-conflict
impact: high
confidence: validated
sensitivity: internal
status: draft
owner: <team-or-name>
applicability: <machine/layer/distro scope>
lifecycle: [detect, diagnose, fix, verify, prevent]
symptoms:
  - <observable symptom>
root_cause:
  - <evidence-based root cause>
fix:
  - <what changed>
prevention:
  - <guardrail>
links:
  - <PR/issue/commit/doc>
---

## Context

Describe environment, versions, machine, and constraints.

## Detection and impact

- First observed in:
- User/business impact:
- Scope of affected systems:

## Investigation timeline

1. Hypothesis A and result
2. Hypothesis B and result
3. Confirmed root cause

## Final fix

Describe exact changes and why they are safe.

## Validation

- Build/runtime/tests performed
- Negative tests

## Prevention plan

- Process guardrails
- Tooling checks
- Ownership and follow-up date
