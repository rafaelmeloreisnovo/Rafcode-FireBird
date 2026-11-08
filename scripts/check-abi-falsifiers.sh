#!/bin/sh
# SPDX-License-Identifier: MIT. Disposable positive and adversarial ELF fixtures.
set -eu
cd "$(dirname "$0")/.."
command -v clang >/dev/null 2>&1 || { echo 'FALSIFIERS=BLOCKED clang missing' >&2; exit 2; }
w=$(mktemp -d /tmp/raf-falsify.XXXXXXXX) || exit 2
trap 'rm -rf "$w"' 0
trap 'exit 2' 1 2 3 15
cat > "$w/clean.c" <<'C'
int local_only(void) { return 7; }
C
cat > "$w/external.c" <<'C'
extern void outside(void);
void leaked_dependency(void) { outside(); }
C
cat > "$w/trap.c" <<'C'
void direct_syscall(void) {
#if defined(__x86_64__)
 __asm__ __volatile__("syscall" ::: "memory");
#elif defined(__arm__) || defined(__aarch64__)
 __asm__ __volatile__("svc #0" ::: "memory");
#else
#error Unexpected target
#endif
}
C
expect_reject() {
 if sh scripts/check-core-object.sh "$1" "$2" >"$w/check.log" 2>&1; then
   echo "FALSIFIERS=FAIL false accept arch=$1" >&2; exit 1
 fi
 grep -q 'CORE_AUDIT=FAIL' "$w/check.log" || {
   echo 'FALSIFIERS=BLOCKED tool failure is not a rejection' >&2
   cat "$w/check.log" >&2; exit 2
 }
}
for arch in x86_64 armv7 aarch64; do
 case "$arch" in
  x86_64) triple=x86_64-unknown-linux-gnu ;;
  armv7) triple=armv7a-none-eabi ;;
  aarch64) triple=aarch64-none-elf ;;
 esac
 for kind in clean external trap; do
   clang --target="$triple" -std=c11 -O2 -ffreestanding -fno-builtin \
     -fno-stack-protector -Wall -Wextra -Werror -pedantic \
     -c "$w/$kind.c" -o "$w/$arch-$kind.o"
 done
 sh scripts/check-core-object.sh "$arch" "$w/$arch-clean.o"
 expect_reject "$arch" "$w/$arch-external.o"
 expect_reject "$arch" "$w/$arch-trap.o"
 echo "FALSIFIERS=PASS target=$arch positive=1 external_reject=1 syscall_reject=1"
done
cat > "$w/legacy_x86.c" <<'C'
void legacy_os_entry(void) { __asm__ __volatile__("int $0x80" ::: "memory"); }
C
clang --target=x86_64-unknown-linux-gnu -std=c11 -O2 -ffreestanding \
 -Wall -Wextra -Werror -pedantic -c "$w/legacy_x86.c" -o "$w/legacy_x86.o"
expect_reject x86_64 "$w/legacy_x86.o"
echo 'FALSIFIERS=PASS legacy_x86_int80_rejected=1'
expect_reject aarch64 "$w/armv7-clean.o"
echo 'FALSIFIERS=PASS wrong_machine_rejected=1'
if PATH=/nonexistent /bin/sh scripts/check-core-object.sh x86_64 "$w/x86_64-clean.o" >"$w/check.log" 2>&1; then
 echo 'FALSIFIERS=FAIL tool absence falsely accepted' >&2; exit 1
fi
grep -q 'CORE_AUDIT=BLOCKED' "$w/check.log" || {
 echo 'FALSIFIERS=FAIL tool absence lacked typed BLOCKED' >&2; exit 1
}
echo 'FALSIFIERS=PASS missing_tool_blocked=1'
