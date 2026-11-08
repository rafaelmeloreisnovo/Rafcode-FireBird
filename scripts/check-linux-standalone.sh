#!/bin/sh
# SPDX-License-Identifier: MIT -- Linux-only static ELF smoke.
set -eu
cd "$(dirname "$0")/.."
command -v clang >/dev/null 2>&1 || { echo 'STANDALONE=BLOCKED clang absent' >&2; exit 2; }
command -v readelf >/dev/null 2>&1 || { echo 'STANDALONE=BLOCKED readelf absent' >&2; exit 2; }
w=$(mktemp -d /tmp/raf-linux.XXXXXXXX) || exit 2
trap 'rm -rf "$w"' 0
trap 'exit 2' 1 2 3 15
flags='-std=c11 -O2 -ffreestanding -fno-builtin -fno-stack-protector -fno-unwind-tables -fno-asynchronous-unwind-tables -ffunction-sections -fdata-sections -Wall -Wextra -Werror -pedantic'
for arch in x86_64 armv7 aarch64; do
 case "$arch" in
  x86_64) triple=x86_64-unknown-linux-gnu; port=exit_x86_64 ;;
  armv7) triple=armv7a-none-eabi; port=exit_armv7 ;;
  aarch64) triple=aarch64-none-elf; port=exit_aarch64 ;;
 esac
 clang --target="$triple" $flags -c NUCLEOS/ports/linux/entry.c -o "$w/entry.o"
 clang --target="$triple" $flags -c "NUCLEOS/ports/linux/$port.c" -o "$w/exit.o"
 clang --target="$triple" $flags -c NUCLEOS/src/raf_gate.c -o "$w/gate.o"
 clang --target="$triple" -fuse-ld=lld -nostdlib -static -Wl,-e,_start \
   "$w/entry.o" "$w/exit.o" "$w/gate.o" -o "$w/app"
 readelf -h "$w/app" | grep -q 'Type:.*EXEC' || { echo "STANDALONE=FAIL arch=$arch non-EXEC ELF" >&2; exit 1; }
 if readelf -Ws "$w/app" | awk '$7=="UND" && $8!="" {bad=1} END{exit bad?0:1}'; then
   echo "STANDALONE=FAIL arch=$arch undefined symbols" >&2; exit 1
 fi
 if readelf -l "$w/app" | grep -q INTERP; then
   echo "STANDALONE=FAIL arch=$arch dynamic interpreter" >&2; exit 1
 fi
 if [ "$arch" = x86_64 ]; then
  "$w/app"
  echo 'STANDALONE=PASS_EXECUTED target=x86_64 host=linux'
 else
  echo "STANDALONE=PASS_LINK_ONLY target=$arch runtime=NOT_RUN"
 fi
done
