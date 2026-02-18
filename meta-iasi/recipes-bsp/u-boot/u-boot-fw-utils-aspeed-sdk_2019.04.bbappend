FILESEXTRAPATHS:prepend:iasi-2700 := "${THISDIR}/files:"

# Use AspeedTech official U-Boot v2023.10 for AST2700 ARM64 support
SRCREV:iasi-2700 = "${AUTOREV}"
SRC_URI:iasi-2700 = "git://github.com/AspeedTech-BMC/u-boot.git;branch=aspeed-master-v2023.10;protocol=https \
                     file://fw_env_flash_nor.config \
                     file://fw_env_ast2600_mmc.config \
                    "

# Update license checksum for v2023.10
LIC_FILES_CHKSUM:iasi-2700 = "file://Licenses/README;md5=2ca5f2c35c8cc335f0a19756634782f1"
