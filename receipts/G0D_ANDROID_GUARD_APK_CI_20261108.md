# G0d Android Guard APK CI receipt — 2026-11-08

SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM.

## Authoritative source and execution
- PRODUCER: `rafaelmeloreisnovo/Rafcode-FireBird` PR #4 DRAFT/HOLD, base main `d761a29949c6bba921e6c408c8d5f088d9c5664a`.
- EXACT_TESTED_SOURCE_SHA: `4e3c3b94183f244005713755d16cbdfc1224a687`.
- WORKFLOW: `https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42512384275` completed SUCCESS.
- JOBS: `core-freestanding` 128828040714 SUCCESS; `apk-armv7` 128828091098 SUCCESS; `apk-arm64` 128828091133 SUCCESS.
- CORE: C11 freestanding compiler/ELF/falsification gate PASS_OBJECT x86_64, ARMv7, AArch64; negative symbol/syscall/legacy int0x80/wrong-machine/absent-tool gates PASS. No SDK/NDK/Java required in this stage.
- ANDROID ADAPTER: NativeActivity shared library and APK packaging depend on Android NDK, SDK aapt2, zipalign, apksigner, keytool, system libandroid/libdl/libc. No Gradle or authored Java/JNI implementations. They are not wholly freestanding Android APKs.

## Exact produced APK file hashes — distinct from ZIP artifact digests

| ABI | APK size bytes | SHA256 of APK bytes | GitHub workflow artifact |
| --- | ---: | --- | --- |
| armeabi-v7a | 29108 | `296c74fee9fe7df18dc6296528bf1ae6255ce608b71cf396a20f81a9849caab5` | [artifact 13630216268](https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42512384275/artifacts/13630216268) |
| arm64-v8a | 33202 | `1f923d03e1682f6cd2ad463ade03bad8ccaca9677cdedf406dfdb3fbb80ba8ad` | [artifact 13630251040](https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42512384275/artifacts/13630251040) |

ZIP artifact digest reported by provider (NOT APK checksum): ARMv7 `sha256:74b2364d64ca84146a3aecf84b4adf65d37ee40a886700112d0b61d9d3c49233`, ARM64 `sha256:31298988bba04a7a2f0af311747dee944fa662ce7b056106e283e688c852b972`. Archive downloaded and opened: each contained exactly one APK, one SHA256 receipt and one text status receipt. APK SHA256 matches the archived SHA256 text. ELF ARM32 and AArch64 verified on extracted librafguard.so with exported `ANativeActivity_onCreate`, normal libandroid/bionic platform imports and no Firebird engine. APK signatures v1/v2/v3 verified in CI; x86_64/ARM actual device install NOT_RUN.

## Critical scope and safety
- **Guard probe APKs, NOT Firebird engine/server APKs**; `firebird_rafcodephi/android/embedded` currently emits an AAR library, not an executable server APK.
- No database, network, recovery, SQL, privileged operation, secrets or production licensing changes. APK uses ephemeral test-only signing identity regenerated per run; production installation/updates require an owner-managed stable signing process.
- Source readback != actual Motorola E7 Power installation. `Android_E2E=NOT_RUN`; `Firebird_engine_E2E=NOT_RUN`; `CLAIM_ALLOWED=false`.
- APK artifacts stored by GitHub Actions with 7-day retention at time of execution, with expiry 2026-11-15. No release or public permanent APK distribution created. Privacy risk: limited diagnostic app without network/data access.
- ROLLBACK: close PR#4 or revert G0d additions; current main remains unchanged; installed test APK removable by package manager.
- R3: F_ok=three CI jobs success, two separate APKs signed and hashes independently inspected; F_gap=on-device runtime, production signing, Firebird engine; F_next=physical Motorola readback, engine build separately in its source repo after a proven Android integration.

Receipt is informational evidence, not independent external attestation, ISO certification or Firebird performance benchmark.
