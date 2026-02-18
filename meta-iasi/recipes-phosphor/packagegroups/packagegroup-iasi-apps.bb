SUMMARY = "OpenBMC for IASI - Applications"
PR = "r1"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES = " \
        ${PN}-chassis \
        ${PN}-flash \
        ${PN}-system \
        ${PN}-user \
        "

PROVIDES += "virtual/obmc-chassis-mgmt"
PROVIDES += "virtual/obmc-flash-mgmt"
PROVIDES += "virtual/obmc-system-mgmt"
PROVIDES += "virtual/obmc-user-mgmt"

RPROVIDES:${PN}-chassis += "virtual-obmc-chassis-mgmt"
RPROVIDES:${PN}-flash += "virtual-obmc-flash-mgmt"
RPROVIDES:${PN}-system += "virtual-obmc-system-mgmt"
RPROVIDES:${PN}-user += "virtual-obmc-user-mgmt"

SUMMARY:${PN}-chassis = "IASI Chassis"
RDEPENDS:${PN}-chassis = " \
        phosphor-ipmi-ipmb \
        "

SUMMARY:${PN}-user = "IASI User"
RDEPENDS:${PN}-user = " \
        phosphor-ipmi-net \
        "

SUMMARY:${PN}-flash = "IASI Flash"
RDEPENDS:${PN}-flash = " \
        phosphor-software-manager \
        "

SUMMARY:${PN}-system = "IASI System"
RDEPENDS:${PN}-system = " \
        bmcweb \
        webui-vue \
        phosphor-ipmi-host \
        phosphor-host-postd \
        phosphor-post-code-manager \
        phosphor-sel-logger \
        phosphor-logging \
        phosphor-led-manager \
        phosphor-health-monitor \
        "
