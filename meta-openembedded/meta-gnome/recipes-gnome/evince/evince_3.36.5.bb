SUMMARY = "Evince is a document viewer for document formats like pdf, ps, djvu"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=96f2f8d5ee576a2163977938ea36fa7b"
SECTION = "x11/office"
DEPENDS = " \
    gnome-common-native \
    yelp-tools-native \
    appstream-glib \
    gtk+3 \
    gspell \
    libsecret \
    poppler \
    gstreamer1.0-plugins-base \
    orc \
    adwaita-icon-theme \
    ${@bb.utils.contains('DISTRO_FEATURES','x11','gnome-desktop3','',d)} \
"

GNOMEBASEBUILDCLASS = "meson"

inherit gnomebase itstool gnome-help pkgconfig gsettings gobject-introspection upstream-version-is-even gettext mime-xdg gtk-doc

SRC_URI[archive.md5sum] = "5d68c81a3d4c5d27754b97405451f04e"
SRC_URI[archive.sha256sum] = "6f0dd6e30639eb620f201a6ae40f21c4b78c030f0d6437f9e309f7240195e97c"
SRC_URI += " \
    file://0001-Add-format-attribute-to-_synctex_malloc.patch \
    file://0002-add-a-formatting-attribute-check.patch \
"

GTKDOC_MESON_OPTION = "gtk_doc"

EXTRA_OEMESON = " \
    -Dsystemduserunitdir=no \
"

do_compile_prepend() {
    export GIR_EXTRA_LIBS_PATH="${B}/libdocument/.libs"
}

PACKAGECONFIG ??= ""
PACKAGECONFIG[nautilus] = "-Dnautilus=true,-Dnautilus=false,nautilus"
PACKAGECONFIG[browser-plugin] = "-Dbrowser_plugin=true,-Dbrowser_plugin=false"

RDEPENDS_${PN} += "glib-2.0-utils"
RRECOMMMENDS_${PN} = "adwaita-icon-theme"

PACKAGES =+ "${PN}-nautilus-extension"
PACKAGES =+ "${PN}-browser-plugin"

FILES_${PN} += "${datadir}/dbus-1 \
                ${datadir}/metainfo \
                ${datadir}/thumbnailers \
"
FILES_${PN}-nautilus-extension = "${libdir}/nautilus/*/*so"
FILES_${PN}-browser-plugin = "${libdir}/mozilla/*/*so"
