# Freestanding multi-ABI producer route — ABI G0b

Source boundary: `NUCLEOS/src/{raf_guard,raf_gate}.c`, separate from upstream Firebird and from hosted `audit/` tooling.

## Deterministic DAG

```text
C11 source+headers / file-level SPDX
    -> module-specific compile flags (GCC host / Clang host)
    -> compile-only object files [no linked executable]
    -> Clang armv7a-none-eabi | aarch64-none-elf
    -> readelf ELF machine + undefined-symbol table (must be empty)
    -> PASS_SCOPED_OBJECTS_ONLY or FAIL/BLOCKED
Hosted synthetic runtime + Python receipt verifier is a separate gate, never conflated with the object audit.
Firebird database / Android device / physical ABI E2E remain NOT_RUN.
```

Run at repository root with an installed C compiler, Clang with ARM targets, a POSIX shell, `mktemp`, `awk`, `grep` and `readelf`:

```sh
sh scripts/check-freestanding-abi.sh
sh scripts/check.sh
```

The compile step uses `-std=c11 -O2 -ffreestanding -fno-builtin -fno-stack-protector -fno-unwind-tables -fno-asynchronous-unwind-tables -ffunction-sections -fdata-sections -Wall -Wextra -Werror -pedantic` and `-c`. No Android SDK, NDK, JDK, JNI, Gradle, R8, Firebird library or binary app is required **to compile these particular objects**. GitHub Actions is only an optional hosted executor, not a runtime dependency of the kernel.

## What the test proves / does not prove

- **Proves when executed on exact source:** the selected compiler could emit two ELF objects for each tested target, matching ELF machines and without external undefined symbol names in their symbol tables.
- **Does not prove:** a complete linked bootable binary, a valid entry point, Android app package, no inline syscall instruction, exact ABI at a callable boundary, execution on ARM hardware, correct Firebird behavior, numerical equivalence after future inline ASM, performance improvement, formal noninterference, full third-party copyright independence, or no toolchain dependency.
- `-ffreestanding` is not `-nodefaultlibs` for arbitrary links. A compiler may still emit helper routines such as `memcpy`, `memmove`, `memset` or architecture-specific runtime helpers: the object verifier **fails** on unresolved symbols.
- `void` means no function return value (or an incomplete type), **not** syscall elimination. Comments, whitespace and source names normally do not execute; preprocessor directives, flags, symbol linkage, data representation and linker options can change outputs. Exact bytes and timing require controlled builds and measurement.
- Bare-metal and Android are different targets. Android runtime integration needs a valid OS boundary and ABI; a raw cross-compiled `.o` is not an APK. Syscalls cannot be assumed portable merely because a C compiler exists.

## Falsification protocol (6Σ / DMAIC)

**D** define self-contained object gates; **M** report compiler versions/commit, target, ELF machine and undefined symbols; **A** examine any helper or external call; **I** isolate individual modules and retain ordinary C portable baseline; **C** fail closed, preserve exact-head receipts, revert the feature commit if gate regresses.

Adversarial fixture: add `extern void outside(void); void deliberate_bad(void) { outside(); }` to one disposable test module, confirm the verifier exits nonzero and prints `outside`; restore source before re-running. This deliberately tests the scanner, not the real producer source. Reject false PASS when readelf/Clang is missing.

**Future optional inline ASM:** only for an ABI-targeted bottleneck with a verified C reference, explicit clobbers, operand widths, memory-ordering and CPU-feature guards; require bitwise differential tests on ARMv7/AArch64 real devices. Raw opcodes/hex have no automatic speed benefit and increase instruction/endianness risk. Keep such experiments out of portable core until demonstrated.

**Current status of this document:** guidance + compile-check script. Tests against the *exact repository HEAD* require a separate recorded execution receipt; local representative-fixture tests alone are not such a receipt. `claim_allowed=false`.

## G0c bounded executable and falsifiers

The scripts/check-core-object.sh ELF examiner checks the machine, unresolved symbols, and banned direct OS entry instructions in isolated core objects. scripts/check-abi-falsifiers.sh rejects an external call, a direct syscall and a wrong architecture, and rejects tool absence as BLOCKED. scripts/check-linux-standalone.sh builds static Linux-only executables without libc, runs x86_64 locally, and only links ARMv7/AArch64. See PROCEDURAL_ASSURANCE_V1.md; current new-head gate cannot be asserted before CI evidence.
