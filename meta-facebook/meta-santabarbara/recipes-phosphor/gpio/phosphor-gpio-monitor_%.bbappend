FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

inherit obmc-phosphor-systemd systemd

SERVICE_LIST = "assert-post-end.service \
                assert-power-good-drop.service \
                assert-reset-button.service \
                deassert-post-end.service \
                deassert-power-good-drop.service \
                deassert-reset-button.service \
                platform-host-ready.target \
                power-rail-assert-log@.service \
                power-rail-deassert-log@.service \
                thermal-assert-log@.service \
                thermal-deassert-log@.service \
                multi-gpios-sys-init.service \
                vr-fault-assert-log@.service \
                vr-fault-deassert-log@.service \
                "

SERVICE_FILE_FMT = "file://{0}"

SRC_URI += " \
    file://assert-post-end \
    file://assert-power-good-drop \
    file://assert-reset-button \
    file://deassert-post-end \
    file://deassert-power-good-drop \
    file://deassert-reset-button \
    file://multi-gpios-sys-init \
    file://plat-phosphor-multi-gpio-monitor.json \
    file://power-rail-event-logger \
    file://thermal-event-logger \
    file://vr-fault-event-logger \
    ${@compose_list(d, 'SERVICE_FILE_FMT', 'SERVICE_LIST')} \
    "

RDEPENDS:${PN}:append = " bash"

FILES:${PN} += "${systemd_system_unitdir}/*"

SYSTEMD_SERVICE:${PN} += "${SERVICE_LIST}"

do_install:append() {
    install -d ${D}${datadir}/phosphor-gpio-monitor
    install -m 0644 ${UNPACKDIR}/plat-phosphor-multi-gpio-monitor.json \
                    ${D}${datadir}/phosphor-gpio-monitor/phosphor-multi-gpio-monitor.json

    for s in ${SERVICE_LIST}
    do
        install -m 0644 ${UNPACKDIR}/${s} ${D}${systemd_system_unitdir}/${s}
    done

    install -d ${D}${libexecdir}/${PN}
    install -m 0755 ${UNPACKDIR}/assert-post-end ${D}${libexecdir}/${PN}/
    install -m 0755 ${UNPACKDIR}/assert-power-good-drop ${D}${libexecdir}/${PN}/
    install -m 0755 ${UNPACKDIR}/assert-reset-button ${D}${libexecdir}/${PN}/
    install -m 0755 ${UNPACKDIR}/deassert-post-end ${D}${libexecdir}/${PN}/
    install -m 0755 ${UNPACKDIR}/deassert-power-good-drop ${D}${libexecdir}/${PN}/
    install -m 0755 ${UNPACKDIR}/deassert-reset-button ${D}${libexecdir}/${PN}/
    install -m 0755 ${UNPACKDIR}/multi-gpios-sys-init ${D}${libexecdir}/${PN}/
    install -m 0755 ${UNPACKDIR}/power-rail-event-logger ${D}${libexecdir}/${PN}/
    install -m 0755 ${UNPACKDIR}/thermal-event-logger ${D}${libexecdir}/${PN}/
    install -m 0755 ${UNPACKDIR}/vr-fault-event-logger ${D}${libexecdir}/${PN}/
}

SYSTEMD_OVERRIDE:${PN}-monitor += "phosphor-multi-gpio-monitor.conf:phosphor-multi-gpio-monitor.service.d/phosphor-multi-gpio-monitor.conf"
