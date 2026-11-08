#!/bin/sh
# SPDX-License-Identifier: MIT
# Compile-only ABI proof; no Android SDK/NDK/Gradle, Firebird or hosted link.
set -eu
cd "$(dirname "$0")/.."

if ! command -v readelf >/dev/null 2>&1; then
    echo 'FREESTANDING_ABI=BLOCKED missing readelf (undefined-symbol audit)' >&2
    exit 2
fi

work=$(mktemp -d "${TMPDIR:-/tmp}/raf-abi.XXXXXXXX") || exit 2
trap 'rm -rf "$work"' 0
trap 'exit 2' 1 2 3 15

check_one() {
    compiler=$1
    target=$2
    tag=$3
    for unit in raf_guard raf_gate; do
        obj="$work/${tag}_${unit}.o"
        if [ -n "$target" ]; then
            "$compiler" --target="$target" -std=c11 -O2 -ffreestanding \
                -fno-builtin -fno-stack-protector -fno-unwind-tables \
                -fno-asynchronous-unwind-tables -ffunction-sections -fdata-sections \
                -Wall -Wextra -Werror -pedantic -I NUCLEOS/include \
                -c "NUCLEOS/src/${unit}.c" -o "$obj"
        else
            "$compiler" -std=c11 -O2 -ffreestanding \
                -fno-builtin -fno-stack-protector -fno-unwind-tables \
                -fno-asynchronous-unwind-tables -ffunction-sections -fdata-sections \
                -Wall -Wextra -Werror -pedantic -I NUCLEOS/include \
                -c "NUCLEOS/src/${unit}.c" -o "$obj"
        fi
        # Inspect actual ELF symbols: -ffreestanding may emit runtime helpers.
        readelf -Ws "$obj" > "$work/symbols"
        awk '$7 == "UND" && $8 != "" { print $8 }' "$work/symbols" > "$work/undefined"
        if [ -s "$work/undefined" ]; then
            echo "FREESTANDING_ABI=FAIL target=$tag unit=$unit undefined:" >&2
            cat "$work/undefined" >&2
            exit 1
        fi
        case "$tag" in
            armv7) readelf -h "$obj" | grep -q 'Machine:.*ARM' ;;
            aarch64) readelf -h "$obj" | grep -q 'Machine:.*AArch64' ;;
        esac
    done
    echo "FREESTANDING_ABI=PASS_OBJECT_ONLY target=$tag compiler=$compiler"
}

native=0
if command -v gcc >/dev/null 2>&1; then
    check_one gcc '' native-gcc
    native=1
fi
if command -v clang >/dev/null 2>&1; then
    check_one clang '' native-clang
    native=1
    check_one clang armv7a-none-eabi armv7
    check_one clang aarch64-none-elf aarch64
else
    echo 'FREESTANDING_ABI=BLOCKED ARMv7/AArch64 requires clang target support' >&2
    exit 2
fi
if [ "$native" -ne 1 ]; then
    echo 'FREESTANDING_ABI=BLOCKED no native compiler' >&2
    exit 2
fi
printf '%s\n' 'FREESTANDING_ABI=PASS_SCOPED_OBJECTS_ONLY runtime=NOT_RUN android=NOT_RUN'
