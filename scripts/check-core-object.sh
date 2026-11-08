#!/bin/sh
# SPDX-License-Identifier: MIT. Fail closed ELF symbols and direct OS/trap scan.
set -eu
if [ "$#" -ne 2 ]; then echo 'CORE_AUDIT=BLOCKED args arch obj' >&2; exit 2; fi
arch=$1 obj=$2
[ -f "$obj" ] || { echo 'CORE_AUDIT=BLOCKED obj missing' >&2; exit 2; }
command -v readelf >/dev/null 2>&1 || { echo 'CORE_AUDIT=BLOCKED readelf absent' >&2; exit 2; }
disasm=
for bin in llvm-objdump llvm-objdump-20 llvm-objdump-19 llvm-objdump-18 llvm-objdump-17 llvm-objdump-16; do
 if command -v "$bin" >/dev/null 2>&1; then disasm=$bin; break; fi
done
[ -n "$disasm" ] || { echo 'CORE_AUDIT=BLOCKED llvm-objdump absent' >&2; exit 2; }
if ! readelf -h "$obj" | grep -q 'Type:.*REL'; then
 echo 'CORE_AUDIT=FAIL not ELF relocatable' >&2; exit 1
fi
case "$arch" in
 x86_64) machine='Machine:.*X86-64' ;;
 armv7) machine='Machine:.*ARM' ;;
 aarch64) machine='Machine:.*AArch64' ;;
 *) echo 'CORE_AUDIT=BLOCKED unknown arch' >&2; exit 2 ;;
esac
if ! readelf -h "$obj" | grep -q "$machine"; then
 echo "CORE_AUDIT=FAIL wrong machine expected=$arch" >&2; exit 1
fi
symbols=$(readelf -Ws "$obj") || {
 echo 'CORE_AUDIT=BLOCKED symbol extraction failed' >&2; exit 2
}
if printf '%s\n' "$symbols" | awk '$7=="UND" && $8!="" {print $8; bad=1} END{exit bad?0:1}'; then
 echo "CORE_AUDIT=FAIL undefined external target=$arch" >&2; exit 1
fi
disassembly=$("$disasm" -d "$obj") || {
 echo 'CORE_AUDIT=BLOCKED disassembler failure' >&2; exit 2
}
if printf '%s\n' "$disassembly" | grep -E '[[:space:]](svc|swi|hvc|smc|syscall|sysenter|brk|int3|ud2)([[:space:]]|$)|[[:space:]]int[[:space:]]+[$]0x80' >/dev/null; then
 echo "CORE_AUDIT=FAIL forbidden syscall/trap target=$arch" >&2; exit 1
fi
echo "CORE_AUDIT=PASS_OBJECT target=$arch"
