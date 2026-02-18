# Copyright (c) 2025 IASI Inc.
# SPDX-License-Identifier: Apache-2.0

FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

# Add AST2700 device tree support
SRC_URI:append:aspeed-g7 = " \
    file://aspeed-g7/defconfig \
    file://aspeed-g7/aspeed-g7.dtsi \
    file://aspeed-g7/aspeed-g7-pinctrl.dtsi \
    file://aspeed-g7/aspeed-bmc-iasi-2700.dts \
    file://aspeed-g7/openbmc-flash-layout-128.dtsi \
    file://aspeed-g7/dt-bindings/clock/ast2700-clock.h \
    file://aspeed-g7/dt-bindings/pinctrl/aspeed-pinctrl.h \
"

# Copy defconfig to kernel source before kernel_metadata task
do_ast2700_copy_defconfig[dirs] = "${S}"
do_ast2700_copy_defconfig() {
    bbnote "Copying defconfig to arch/arm64/configs/aspeed_g7_defconfig"
    bbnote "UNPACKDIR: ${UNPACKDIR}"
    bbnote "S: ${S}"
    # Copy defconfig to arch/arm64/configs
    install -d ${S}/arch/arm64/configs
    install -v -m 0644 ${UNPACKDIR}/aspeed-g7/defconfig ${S}/arch/arm64/configs/aspeed_g7_defconfig
    ls -la ${S}/arch/arm64/configs/
}
addtask do_ast2700_copy_defconfig before do_kernel_metadata after do_kernel_checkout

# Copy device tree files to kernel source directory
do_configure:prepend:aspeed-g7() {
    # Create AST2700 device tree directory in arm64
    install -d ${S}/arch/arm64/boot/dts/aspeed

    # Copy device tree files
    install -m 0644 ${UNPACKDIR}/aspeed-g7/aspeed-g7.dtsi ${S}/arch/arm64/boot/dts/aspeed/
    install -m 0644 ${UNPACKDIR}/aspeed-g7/aspeed-g7-pinctrl.dtsi ${S}/arch/arm64/boot/dts/aspeed/
    install -m 0644 ${UNPACKDIR}/aspeed-g7/aspeed-bmc-iasi-2700.dts ${S}/arch/arm64/boot/dts/aspeed/
    install -m 0644 ${UNPACKDIR}/aspeed-g7/openbmc-flash-layout-128.dtsi ${S}/arch/arm64/boot/dts/aspeed/

    # Copy dt-bindings header files
    install -d ${S}/include/dt-bindings/clock
    install -m 0644 ${UNPACKDIR}/aspeed-g7/dt-bindings/clock/ast2700-clock.h ${S}/include/dt-bindings/clock/
    install -d ${S}/include/dt-bindings/pinctrl
    install -m 0644 ${UNPACKDIR}/aspeed-g7/dt-bindings/pinctrl/aspeed-pinctrl.h ${S}/include/dt-bindings/pinctrl/
}

# Use the defconfig for AST2700
KBUILD_DEFCONFIG:aspeed-g7 = "aspeed_g7_defconfig"

# Add AST2700 device tree to build
KERNEL_DEVICETREE:append:aspeed-g7 = " aspeed/aspeed-bmc-iasi-2700.dtb"
