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
python3 -m unittest discover -v -s audit/tests
