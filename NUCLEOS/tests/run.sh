#!/bin/sh
# SPDX-License-Identifier: MIT. Offline, creates only temporary executables.
set -eu
cd "$(dirname "$0")/.."
CC="${CC:-cc}"
OUT1="${TMPDIR:-/tmp}/raf_guard_$$"
OUT2="${TMPDIR:-/tmp}/raf_gate_$$"
trap 'rm -f "$OUT1" "$OUT2"' EXIT HUP INT TERM
"$CC" -std=c11 -O2 -ffreestanding -fno-builtin -Wall -Wextra -Werror -pedantic \
  -Iinclude src/raf_guard.c tests/test_guard.c -o "$OUT1"
"$OUT1"
"$CC" -std=c11 -O2 -ffreestanding -fno-builtin -Wall -Wextra -Werror -pedantic \
  -Iinclude src/raf_gate.c tests/test_gate.c -o "$OUT2"
"$OUT2"
