# AST2700 SoC Configuration
# Copyright (c) 2025 IASI Inc.

SOC_FAMILY = "aspeed-g7"
include conf/machine/include/soc-family.inc

# Architecture configuration - ARM64 (Cortex-A35)
DEFAULTTUNE = "cortexa35"
require conf/machine/include/arm/arch-armv8a.inc

# Kernel configuration
PREFERRED_PROVIDER_virtual/kernel = "linux-aspeed"
KERNEL_FEATURES:remove = "cfg/fs/ext4"
KERNEL_FEATURES:append = " cfg/fs/jffs2"
KERNEL_IMAGETYPE = "Image"
KERNEL_CLASSES = "kernel-fitimage"

# Device tree configuration
KERNEL_DEVICETREE = "aspeed/aspeed-bmc-iasi-2700.dtb"

# U-Boot configuration - must be set to enable kernel build
UBOOT_MACHINE = "evb-ast2700_defconfig"
UBOOT_DEVICETREE = "ast2700-evb"
UBOOT_ENTRYPOINT = "0x80008000"
UBOOT_LOADADDRESS = "0x80008000"

# Image type
IMAGE_CLASSES:append = " image_types_phosphor_aspeed_g7"

# Serial console
SERIAL_CONSOLES = "115200;ttyS4"

# Flash layout - 128MB default
FLASH_SIZE = "131072"
FLASH_UBOOT_OFFSET = "0"
FLASH_UBOOT_ENV_OFFSET = "4096"
FLASH_KERNEL_OFFSET = "4224"
FLASH_ROFS_OFFSET = "13440"
FLASH_RWFS_OFFSET = "98304"
RWFS_SIZE = "33554432"

# Machine features
MACHINE_FEATURES += " \
    obmc-phosphor-fan-mgmt \
    obmc-phosphor-chassis-mgmt \
    obmc-phosphor-flash-mgmt \
    obmc-host-ipmi \
    obmc-host-state-mgmt \
    obmc-chassis-state-mgmt \
    obmc-bmc-state-mgmt \
    "

# Provider configuration
PREFERRED_PROVIDER_virtual/obmc-system-mgmt ?= "packagegroup-obmc-apps"
PREFERRED_PROVIDER_virtual/obmc-host-ipmi-hw ?= "phosphor-ipmi-kcs"
VIRTUAL-RUNTIME_obmc-host-state-manager ?= "x86-power-control"
VIRTUAL-RUNTIME_obmc-chassis-state-manager ?= "x86-power-control"

# MCTP support
include conf/distro/include/mctp.inc

# Secure boot disabled by default
SOCSEC_SIGN_ENABLE = "0"
