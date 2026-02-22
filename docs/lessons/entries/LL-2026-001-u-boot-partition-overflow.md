---
id: LL-2026-001
title: U-Boot overflow caused by include name collision
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
  - do_generate_static reports u-boot.bin is too large
  - parsed FLASH_UBOOT_ENV_OFFSET falls back to 384
root_cause:
  - require conf/machine/include/ast2700.inc resolved to an unintended layer file
  - effective flash layout used 32MB defaults instead of 128MB settings
fix:
  - switched machine config to unique include iasi-ast2700.inc
  - removed colliding meta-iasi ast2700.inc and kept only flash overrides
prevention:
  - avoid same include filenames across layers for machine-critical settings
  - validate effective bitbake variables after machine config changes
links:
  - meta-iasi/conf/machine/iasi-2700.conf
  - meta-iasi/conf/machine/include/iasi-ast2700.inc
---

## Summary

A layer include name collision caused the machine to inherit incorrect flash
layout values. The static image assembly then allocated only 384KB to U-Boot,
while the built image required significantly more space.

## Verification

- `bitbake -e virtual/kernel` confirms `FLASH_UBOOT_ENV_OFFSET=4096`
- `bitbake obmc-phosphor-image -c do_generate_static` succeeds

## Reuse notes

- Apply when machine layout values unexpectedly revert to defaults
- Do not apply blindly if collision is not in include path resolution
