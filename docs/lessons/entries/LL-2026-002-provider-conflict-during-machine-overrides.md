---
id: LL-2026-002
title: Provider conflicts from broad machine override blocks
date: 2026-02-22
component: meta-iasi/machine-config
tags: [provider, virtual-runtime, machine-features, override-scope]
topic: build
failure_mode: provider-conflict
impact: medium
confidence: validated
sensitivity: internal
status: active
owner: iasi-bsp-team
applicability: machine=iasi-2700, distro=openbmc-phosphor
lifecycle: [detect, diagnose, fix, verify, prevent]
symptoms:
  - image parse fails with virtual provider not buildable
  - changes intended for one feature affect unrelated dependency resolution
root_cause:
  - machine include carried broad provider and feature overrides copied from another context
  - those overrides conflicted with layer-specific packagegroups in current distro setup
fix:
  - reduced machine include content to minimal responsibilities
  - kept platform-independent provider choices in their original layer defaults
prevention:
  - keep machine include focused on hardware layout and boot-critical settings
  - add checklist review item for provider or runtime override side effects
links:
  - docs/lessons/checklist.md
  - docs/lessons/schema.md
---

## Context

During flash layout corrections, legacy machine-level override blocks were
activated and started conflicting with current distro provider expectations.

## Detection and impact

- First observed in image task dependency resolution
- Build blocked early; no runtime image generated
- Impact limited to configurations using the affected machine include

## Investigation timeline

1. Confirmed parse-time provider conflict error messages
2. Compared effective variables against minimal machine include baseline
3. Isolated broad override block as the conflict source

## Final fix

Retained only flash-layout overrides in machine include and delegated provider
selection back to layer defaults.

## Validation

- Re-ran image task dependency resolution
- Confirmed unrelated provider chain is buildable again

## Prevention plan

- Update review checklist for machine-level provider changes
- Require rationale line for any new virtual runtime override
