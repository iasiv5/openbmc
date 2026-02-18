FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# Use AspeedTech official U-Boot v2023.10 for AST2700 ARM64 support
# Community U-Boot (openbmc/u-boot) does not have AST2700/ARM64 support yet
# v2019.04 is ARM32 only, v2023.10+ supports ARM64/AST2700
SRCREV:iasi-2700 = "${AUTOREV}"
SRC_URI:iasi-2700 = "git://github.com/AspeedTech-BMC/u-boot.git;branch=aspeed-master-v2023.10;protocol=https"

# Update license checksum for v2023.10
LIC_FILES_CHKSUM:iasi-2700 = "file://Licenses/README;md5=2ca5f2c35c8cc335f0a19756634782f1"

# AST2700 uses ARM64 Cortex-A35, not compatible with AST2600 ARMv7 config
UBOOT_MACHINE:iasi-2700 = "evb-ast2700_defconfig"
UBOOT_DEVICETREE:iasi-2700 = "ast2700-evb"
