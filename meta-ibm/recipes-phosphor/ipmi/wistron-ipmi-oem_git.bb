SUMMARY = "Wistron OEM commands"
DESCRIPTION = "Wistron OEM commands"
HOMEPAGE = "https://github.com/openbmc/wistron-ipmi-oem"
PR = "r1"
PV = "0.1+git${SRCPV}"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=fa818a259cbed7ce8bc2a22d35a464fc"

inherit autotools pkgconfig
inherit obmc-phosphor-ipmiprovider-symlink

DEPENDS += "phosphor-ipmi-host"
DEPENDS += "autoconf-archive-native"

S = "${WORKDIR}/git"
SRC_URI = "git://github.com/openbmc/wistron-ipmi-oem"
SRCREV = "572a22ad0a72142db434b5b78ec28182e27a57fd"

FILES:${PN}:append = " ${libdir}/ipmid-providers/lib*${SOLIBS}"
FILES:${PN}:append = " ${libdir}/host-ipmid/lib*${SOLIBS}"
FILES:${PN}-dev:append = " ${libdir}/ipmid-providers/lib*${SOLIBSDEV} ${libdir}/ipmid-providers/*.la"

HOSTIPMI_PROVIDER_LIBRARY += "libwistronoem.so"
