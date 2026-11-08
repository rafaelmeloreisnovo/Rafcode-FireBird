#!/bin/sh
# SPDX-License-Identifier: MIT. Separate freestanding objects, no hosted libraries.
set -eu
cd "$(dirname "$0")/.."
command -v clang >/dev/null 2>&1 || { echo 'FREESTANDING_ABI=BLOCKED clang missing' >&2; exit 2; }
w=$(mktemp -d /tmp/raf-abi.XXXXXXXX) || exit 2
trap 'rm -rf "$w"' 0
trap 'exit 2' 1 2 3 15
flags='-std=c11 -O2 -ffreestanding -fno-builtin -fno-stack-protector -fno-unwind-tables -fno-asynchronous-unwind-tables -ffunction-sections -fdata-sections -Wall -Wextra -Werror -pedantic'
for arch in x86_64 armv7 aarch64; do
 case "$arch" in
  x86_64) triple=x86_64-unknown-linux-gnu ;;
  armv7) triple=armv7a-none-eabi ;;
  aarch64) triple=aarch64-none-elf ;;
 esac
 for unit in raf_guard raf_gate; do
  clang --target="$triple" $flags -I NUCLEOS/include -c "NUCLEOS/src/$unit.c" -o "$w/$arch-$unit.o"
  sh scripts/check-core-object.sh "$arch" "$w/$arch-$unit.o"
 done
 echo "FREESTANDING_ABI=PASS_OBJECTS arch=$arch"
done
sh scripts/check-abi-falsifiers.sh
echo 'FREESTANDING_ABI=PASS_SCOPED_OBJECTS_AND_FALSIFIERS ARM_runtime=NOT_RUN'
