#!/bin/sh
# SPDX-License-Identifier: MIT. Offline producer G0 and G0c tests.
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
sh scripts/check-freestanding-abi.sh
sh scripts/check-linux-standalone.sh
python3 -m unittest discover -v -s audit/tests
