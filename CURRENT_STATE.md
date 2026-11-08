## G0d CI receipt readback — 2026-11-08

**Tested code/workflow SHA:** `4e3c3b94183f244005713755d16cbdfc1224a687` (success, exact). **GitHub run:** https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42512384275, three scoped jobs PASS including two separately signed NativeActivity APKs. **Review and artifact hashes:** [receipts/G0D_ANDROID_GUARD_APK_CI_20261108.md](receipts/G0D_ANDROID_GUARD_APK_CI_20261108.md). ARMv7 APK SHA256 `296c74fee9fe7df18dc6296528bf1ae6255ce608b71cf396a20f81a9849caab5`; ARM64 APK SHA256 `1f923d03e1682f6cd2ad463ade03bad8ccaca9677cdedf406dfdb3fbb80ba8ad`.

**PASS_SCOPED:** freestanding core object audit, native-Android platform adapter build, APK signature/static inspection/architecture; **NOT_RUN:** physical Motorola E7 Power / Android launch / Firebird engine or SQL functionality. Engine fork currently AAR library, separate producer. Signing keys are ephemeral and not a production upgrade path. `claim_allowed=false; merge_allowed=false`; PR remains draft. Do not treat ZIP digest as APK digest.

---

## G0d — C11 core freestanding CI and two ABI-separated signed APK *probes* (2026-11-08)

- Predecessor HEAD 0e200aaa804d9741809f68337286d2562d640424; new APK workflow needs exact-head CI before PASS. Core previous PASS does NOT prove APK.
- GitHub Actions: independent no-SDK/NDK freestanding kernel gate, then ARMv7 and ARM64 signed NativeActivity smoke APKs (using SDK/NDK only for packaging/native adapter). No Gradle, manual JNI or Java source.
- These are **RAFAELIA Guard probes** not Firebird engine APKs; separate engine producer `firebird_rafcodephi` Android project is library AAR, currently not a standalone server APK.
- Physical Motorola E7, Android 14, Firebird database and APK install/launch remain NOT_RUN. Signing ephemeral, upgrading across CI runs not guaranteed.
- No main edits, engine code, database or credentials changed. claim_allowed=false; merge_allowed=false; rollback revert proposed commit or close PR#4.

---

## CURRENT_STATE G0c — evidence successor (2026-11-08)

- Producer: rafaelmeloreisnovo/Rafcode-FireBird; PR #4 remains DRAFT/HOLD (unmerged) when this record was created. Base main d761a29949c6bba921e6c408c8d5f088d9c5664a; exact most recently **tested source + scripts** HEAD 38c34e157d1490fab21c8a81562d1b451b9cb5c5.
- CI at that SHA: https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42510745116, job 128823038191 SUCCESS; GCC and Clang guard assertions 30041 each, evidence-gate checks 10028 each, Python 17 tests. ELF x86_64, ARMv7, AArch64 source objects PASS; negative tests rejected undefined external symbol, direct syscall, legacy x86 int0x80, wrong machine and missing tool. Linux static -nostdlib x86_64 binary executed PASS; ARMv7/AArch64 static link PASS but RUNTIME=NOT_RUN.
- This subsequent CURRENT_STATE + monitoring spec update is **documentation only**; it does not change tested C, scripts or source gate. Do not claim the new documentation commit itself was exercised by the earlier CI.
- Firebird monitoring critical observation: official Firebird 5 docs expose special DELETE behavior that can close monitored connections or cancel statements; monitoring adapter spec forbids all DML and raw SQL. See docs/FIREBIRD_MONITORING_READ_ONLY_BOUNDARY_V1.md. G1 live Firebird and #9269 fault reproduction remain NOT_IMPLEMENTED/NOT_RUN.
- Google Drive: NEXUS main ledger batchUpdate FAILED_PRECONDITION (both guarded and unguarded paths); authoritative fallback **NEXUS shard 2026-11-002** append-only μWRITE MU-FIREBIRD-G0C-DMAIC-20261108-S2 was written and read back: https://docs.google.com/document/d/1lHwoNgavaCWvG6nzHxTrAJ9UYFW3wTZkmW4rmeViOVs/edit . Do not claim the main ledger was updated.
- Supabase Rafcodephi healthy project, queried schemas public/audit/rafaelia returned no tables; no schema, SQL, privileges or migrations were changed. Not a designated Firebird receipt producer.
- ISO 8000-61, ISO/IEC 27001/27002, ISO 27500, IEEE 1012, W3C PROV-O, BCP14 and NIST SP800-53/53A are **process references**, not certification. See docs/PROCEDURAL_ASSURANCE_V1.md.
- claim_allowed=false; merge_allowed=false; ARM hardware/Android real execution, Firebird database E2E, cryptographic external anchor, independent legal and compliance assessment remain NOT_RUN/UNKNOWN.
- Rollback: close PR #4 or revert its additive commits; no Firebird engine, database or GitHub main change occurred. Follow-up requires authorized physical Motorola evidence and a disposable Firebird runtime, no autonomous remediation.

---

## CURRENT_STATE correction — 2026-11-08 (supersedes obsolete branch-only claim below)

- GitHub main HEAD **d761a29949c6bba921e6c408c8d5f088d9c5664a**, observed via repository branch API 2026-11-08; PR #1 was **merged** into main 2026-11-06. The historical statement below, "main remains untouched", is no longer current and is preserved only for historical traceability.
- New proposed producer branch: `feat/authorial-freestanding-abi-boundary-20261108`, base main `d761a299...`; no merge authorized. Scope: license boundary manifest, freestanding object-symbol audit, C11 build-script wiring, docs and route pointers; engine source and production data are unchanged.
- Tested G0 checkpoint `8abc739...` belongs to the earlier source; do not automatically transfer its PASS to the new branch. Exact new HEAD object audit, CI and physical ARM runtime = **NOT_RUN pending evidence**.
- Separate Firebird IPL/IDPL source remains in another repository; `NUCLEOS` MIT and authored documentation CC BY 4.0 retained. Clean-room status of every historical contribution is not independently certified.
- **claim_allowed=false; merge_allowed=false** for this scoped proposal. Rollback: revert this additive branch commit or close draft PR; no database rollback is relevant.
- Upstream/official producer route: `LICENSES/AUTHORIAL_FIREBIRD_BOUNDARY.md`; freestanding build gate: `docs/FREESTANDING_ABI.md`. Dynamic Firebird integration = NOT_IMPLEMENTED.

---

# CURRENT_STATE — Rafcode-FireBird producer

- **Producer**: `rafaelmeloreisnovo/Rafcode-FireBird`; default branch `main` remains untouched while this implementation is on a feature branch.
- **Initial source**: `main` commit `b4f7d8601203dbc2426a6db49db92bee40fc3077` (README-only bootstrap).
- **Active implementation route**: `feat/nist-governance-audit-kernels-v1`.
- **Status**: `PASS_SCOPED_CI` for G0 only. GitHub Actions run `42166276154` completed `success` for tested source HEAD `8abc739695b24c59e5191aecb957ecace5764f44`; Firebird runtime remains `NOT_RUN`.
- **Included**: watch-only kernel, gate policy kernel, test harnesses, Python read-only digest verifier, crosswalk, licensed docs and narrow CI.
- **Known gaps**: no Firebird runtime adapter; no #9269 disk-full reproduction; no external signatures/anchors; no NIST conformity assessment; no production privacy audit.
- **Denied claims**: `claim_allowed=false`; `merge_allowed=false`; no automatic recovery, deployment or data access.
- **Rollback**: discard or revert feature branch commits; no production service or database was modified.
- **Next**: exact-head readback + source tests + review of CI (if any); then a read-only adapter spec over disposable Firebird DB.
- **Prior technology**: C11 guard from `firebird_rafcodephi` recorded in [PROVENANCE.md](PROVENANCE.md). This is an explicit import, not an independently re-invented source.
- **Evidence ledger**: absent external independent attestation => `TOKEN_VAZIO`; no signed checkpoint should be assumed.

## Verified evidence checkpoint — 2026-11-06

- GitHub CI: https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42166276154; bounded-test job ID 127723383517: success.
- Tested source HEAD: `8abc739695b24c59e5191aecb957ecace5764f44`; subsequent append-only receipt and docs do not modify tested C/Python code.
- GNU C: guard 30041 assertions + evidence gate 10028 checks; Clang: same; Python unittest: 17 tests; 0 test failures observed in reported CI log.
- Earlier malformed-enum falsifier reproduced and surgically corrected; new negative tests included.
- G0 `PASS_SCOPED_CI`; G1 (Firebird engine integration), G2 (disk-full recovery), G3 (privacy deployment), G4 (signed anchor), G5 (independent audit) = `NOT_RUN/NOT_IMPLEMENTED`. No NIST certification.
- Evidence manifest: [receipts/2026-11-06-G0-scoped-ci.json](receipts/2026-11-06-G0-scoped-ci.json). `claim_allowed=false`, `merge_allowed=false`.
