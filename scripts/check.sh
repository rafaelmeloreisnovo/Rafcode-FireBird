#!/bin/sh
# SPDX-License-Identifier: MIT. Bounded offline tests. No artifact upload or daemon.
set -eu
cd "$(dirname "$0")/.."
for compiler in gcc clang; do
  if command -v "$compiler" >/dev/null 2>&1; then
    echo "G0 compiler=$compiler"
    CC="$compiler" sh NUCLEOS/tests/run.sh
  else
    echo "G0 compiler=$compiler NOT_RUN unavailable"
  fi
done
# Additional standalone C11 federation policy and RFC5424 syslog preview falsifiers.
TMP_EXE="${TMPDIR:-/tmp}/raf_fed_ci_$"
trap 'rm -f "$TMP_EXE"' EXIT HUP INT TERM
for compiler in gcc clang; do
  if command -v "$compiler" >/dev/null 2>&1; then
    for module in federation syslog; do
      "$compiler" -std=c11 -O2 -ffreestanding -fno-builtin -Wall -Wextra -Werror -pedantic \
        -I NUCLEOS/include "NUCLEOS/src/raf_${module}.c" "NUCLEOS/tests/test_${module}.c" -o "$TMP_EXE"
      "$TMP_EXE"
      rm -f "$TMP_EXE"
    done
  fi
done
python3 -m unittest discover -v -s audit/tests
python3 -m unittest discover -v -s federation/tests
python3 -m federation.control validate
python3 -m federation.control status
python3 -m federation.control plan-enable
python3 -m federation.control plan-disable
