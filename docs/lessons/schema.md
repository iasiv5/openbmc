# Lesson Frontmatter Schema (MVP)

All lesson entries must start with YAML frontmatter.

## Required fields

- `id`: `LL-YYYY-NNN` (example: `LL-2026-001`)
- `title`: concise title, <= 80 chars recommended
- `date`: ISO date (`YYYY-MM-DD`)
- `component`: target area (example: `meta-iasi/u-boot`)
- `tags`: array of 3-8 keywords
- `topic`: one of:
  - `build`, `boot`, `kernel`, `device-tree`, `packaging`, `security`, `ci`, `tooling`
- `failure_mode`: one of:
  - `config-drift`, `size-overflow`, `dependency-missing`, `provider-conflict`, `regression`, `flaky`
- `impact`: one of `low`, `medium`, `high`, `critical`
- `confidence`: one of `hypothesis`, `validated`
- `sensitivity`: one of `public`, `internal`, `confidential`
- `status`: one of `draft`, `active`, `superseded`, `archived`
- `owner`: person or team name
- `applicability`: short scope statement (machine/layer/distro)
- `symptoms`: array
- `root_cause`: array
- `fix`: array
- `prevention`: array
- `links`: array of URLs or repo-relative references

## Optional fields

- `lifecycle`: subset of `detect`, `diagnose`, `fix`, `verify`, `prevent`
- `reviewed_on`: `YYYY-MM-DD`
- `supersedes`: lesson id list

## Minimal example

```yaml
---
id: LL-2026-001
title: U-Boot partition overflow due to wrong include resolution
date: 2026-02-22
component: meta-iasi/machine-config
tags: [ast2700, flash-layout, u-boot, include-collision]
topic: build
failure_mode: size-overflow
impact: high
confidence: validated
sensitivity: internal
status: active
owner: iasi-bsp-team
applicability: machine=iasi-2700, layer=meta-iasi
symptoms:
  - do_generate_static reports u-boot.bin too large
root_cause:
  - machine include resolved to wrong ast2700.inc by BBPATH order
fix:
  - switch to unique include filename and override flash layout there
prevention:
  - avoid colliding include names across layers
links:
  - meta-iasi/conf/machine/iasi-2700.conf
---
```
