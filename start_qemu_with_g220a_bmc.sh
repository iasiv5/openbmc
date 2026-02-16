#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QEMU_BIN="${SCRIPT_DIR}/qemu-system-arm"
IMAGE_PATH="${SCRIPT_DIR}/build/g220a/tmp/deploy/images/g220a/obmc-phosphor-image-g220a.static.mtd"
LOG_FILE="${SCRIPT_DIR}/qemu_boot.log"

echo "=============================================="
echo "Starting QEMU with g220a BMC Image"
echo "=============================================="
echo "Script Directory: ${SCRIPT_DIR}"
echo "QEMU Binary: ${QEMU_BIN}"
echo "Image Path: ${IMAGE_PATH}"
echo "Log File: ${LOG_FILE}"
echo ""

check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "ERROR: File not found: $1"
        exit 1
    fi
}

echo "Checking required files..."
check_file_exists "${QEMU_BIN}"
check_file_exists "${IMAGE_PATH}"
echo "✓ All required files found!"
echo ""

echo "Starting QEMU..."
echo "Command:"
echo "${QEMU_BIN} -m 256 -M g220a-bmc -nographic \\"
echo "  -drive file=${IMAGE_PATH},format=raw,if=mtd \\"
echo "  -net nic \\"
echo "  -net user,hostfwd=:127.0.0.1:2222-:22,hostfwd=:127.0.0.1:2443-:443,hostfwd=:127.0.0.1:3333-:3000,hostname=g220a"
echo ""
echo "=============================================="
echo "Access Information:"
echo "  SSH: ssh -p 2222 root@localhost"
echo "  Web UI: https://localhost:2443"
echo "  D-Bus Debug: http://localhost:3333"
echo "=============================================="
echo ""

"${QEMU_BIN}" -m 256 -M g220a-bmc -nographic \
  -drive file="${IMAGE_PATH}",format=raw,if=mtd \
  -net nic \
  -net user,hostfwd=:127.0.0.1:2222-:22,hostfwd=:127.0.0.1:2443-:443,hostfwd=:127.0.0.1:3333-:3000,hostname=g220a
