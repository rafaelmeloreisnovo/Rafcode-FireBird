# Firebird / OpenSSL / Android toolchain federation — v1 (2026-11-10)

Status: **PROPOSED / IMPLEMENTED_UNTESTED until exact-head CI and readback**. This is an evidence map, not a build-success or license-compliance certificate.

## Authority and boundary (provider repository names verified; individual versions/HEADs not audited)

| Node | Producer / route | Domain | Status and test rule |
| --- | --- | --- | --- |
| Firebird audit | [Rafcode-FireBird](https://github.com/rafaelmeloreisnovo/Rafcode-FireBird) | Independent C11 gates, hosted receipt tools, probe APK | This repo owns the scoped gate, not Firebird engine |
| Firebird engine | [firebird_rafcodephi](https://github.com/rafaelmeloreisnovo/firebird_rafcodephi) | Upstream-derived Firebird and Android AAR | Engine transaction E2E = NOT_RUN |
| OpenSSL | [openssl](https://github.com/rafaelmeloreisnovo/openssl) | Crypto toolchain candidate | Exact features, license applicability, ABI, constant time and interop = N5 |
| NDK | [ndk_RafCode](https://github.com/rafaelmeloreisnovo/ndk_RafCode) | Native cross-compilation toolchain | JDK/JNI independence claims require object and packaging gates |
| JDK | [jdk_RAFCODE](https://github.com/rafaelmeloreisnovo/jdk_RAFCODE) | Hosted Java tooling | Java bytecode/ART/JDK cannot be classless by assertion |
| Gradle | [gradle](https://github.com/rafaelmeloreisnovo/gradle) | Hosted orchestration for Android AAR and APK | Gradle execution is not freestanding |
| AndroidX | [androidx_RmR](https://github.com/rafaelmeloreisnovo/androidx_RmR) | Optional UI libraries | Only if consumer declares and tests dependency |
| QEMU | [qemu_rafaelia](https://github.com/rafaelmeloreisnovo/qemu_rafaelia) | Emulation candidate | QEMU PASS != ARM hardware PASS |
| Actions | [actions](https://github.com/rafaelmeloreisnovo/actions) | Hosted CI orchestration | YAML is a recipe, not machine code |
| RafGitTools | [RafGitTools](https://github.com/rafaelmeloreisnovo/RafGitTools) | Cross-ABI kernel/tooling producer | Must use its own validated contracts |

## Typed graph (MANIFOLD Ω; no label-based equivalence)

```text
Firebird-fork@f19db285f98331192ba3887fa04d2059843623cd
  --source_of--> Android :embedded AAR
Rafcode-FireBird@exact_checkout_SHA --source_of--> consumer :app APK
AAR + APK --inspected_by--> firebird_consumer_scope_gate.py
source_SHA + inner_SHA256 + gate_result --documented_in--> CI receipt
CI receipt --evidence_for--> artifact structure ONLY
APK physical launch --blocked_by--> no device receipt
Firebird SQL transaction --blocked_by--> no disposable DB E2E
OpenSSL/NDK/JDK/Gradle/AndroidX/QEMU --related_toolchain--> named producer
```

These edges are proposals for current routing unless independently verified with a fresh exact-ref. SHA-256 is not authorship or a digital signature; ZIP hash is not inner APK hash.

## Reproducible boundaries: do not erase necessary host dependencies

1. **C11 freestanding kernel**: separate target, compile with `-std=c11 -ffreestanding -fno-builtin -Wall -Wextra -Werror -pedantic`; inspect object ELF machine, sections, symbols and unresolved references. For strict no-libc/no-syscall claims, test the exact linked object and actual architecture; flags alone do not prove it.
2. **Android platform adapter**: SDK/NDK, Java/ART and Gradle are required where the selected packaging path uses them. They belong to the host/packaging domain, not the freestanding core. Existing consumer uses Android SDK32 + JDK17/Gradle, while Firebird fork source is pinned separately.
3. **CI workflow**: YAML and GitHub Actions are hosted orchestration; action tags, runner images and packages are provider dependencies. Do not describe them as freestanding.
4. **QEMU**: optional emulator testing can prove only emulated execution. `armv7` and `aarch64` object compilation are neither device execution nor database E2E.
5. **OpenSSL**: use only behind a reviewed crypto interface and compatible license/security baseline; no automatic imports or unsupported substitution of TLS/cryptography.

Optimization goals (small flags, inline ASM, instruction counts, relocation count, stack budget and cache footprint) are **measurements**, not proof by syntax. No blind warning suppression, no unsafe `-fno-stack-protector` substitution to hide faults. Hosted tests can contain functions/variables and use standard libraries while freestanding targets remain separately audited.

## Scoped new falsifier gate

`scripts/firebird_consumer_scope_gate.py` is **hosted Python standard library**, not a C11 kernel or security/ZIP/DEX/ELF full parser. It checks archive path traversal, duplicates, size bounds, `classes.jar` FirebirdConf class magic, `classes.dex` magic, known Android ABI folders and ELF machine/class for native `.so` entries. It computes **inner AAR/APK SHA-256** and emits `scope_gate.json` with `claim_allowed=false`.

Passing asserts **only** `PASS_SCOPED_ARTIFACT_STRUCTURE`. Without `libfbclient.so` or `libEngine*` in the APK: `BLOCKED_NO_NATIVE_FIREBIRD_ENGINE_IN_APK`; if such a library exists: `NATIVE_PRESENT_NOT_FUNCTIONAL_PROOF`. Neither is a functioning engine claim. APK signature remains checked by `apksigner` separately. Full DEX, ZIP, ELF linkage/relocations and binary authenticity require independent validators.

Run scoped synthetic falsifiers: `python3 -m unittest discover -v -s audit/tests -p test_firebird_consumer_scope_gate.py`. Production workflow runs the same test after checkout, then validates built AAR/APK **before uploading artifacts**. CI artifact output includes `scope_gate.json` and the exact consumer checkout commit.

## Gates and rollback

| Gate | Acceptance criterion | Current evidential status |
| --- | --- | --- |
| G0 | Verified source SHA, fork SHA and license boundary | Source and route available; third-party license audit N5 |
| G1 | Synthetic negative falsifiers and exact-head CI | PROPOSED: inspect exact-head jobs after PR |
| G2 | ELF native libraries ABI/linker/dependencies, signed APK | Native engine/ABI full validation NOT_RUN |
| G3 | QEMU separately scoped + real Android ARM32/ARM64 launch | NOT_RUN |
| G4 | Disposable Firebird database SQL, storage faults and recovery | NOT_RUN |
| G5 | Authenticated receipt, reproducibility, privacy, human review | External anchor NOT_RUN |

Falsify by: corrupt ZIP, duplicate entry, path traversal, wrong ELF machine, wrong DEX magic, absent class; after CI, cross-check `scope_gate.json` against the provider artifact and producer commit. Reject all mismatches without weakening the workflow. Never execute live recovery, public exposure, auto-merge or production SQL in this gate.

Rollback: close draft PR (no main mutation), or revert the additive commit after review. Maintain every source/receipt historically; supersede rather than delete. The upstream Firebird repo retains its IPL/IDPL boundary; this hosted script is authored MIT under `audit/LICENSE`.

R3: F_ok=producer and route identified; F_gap=physical engine, actual OpenSSL/NDK/QEMU matrix and trusted anchor; F_next=exact-head CI plus independent disposable data/device proof.
