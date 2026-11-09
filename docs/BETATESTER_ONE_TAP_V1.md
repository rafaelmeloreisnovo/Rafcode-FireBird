# Firebird Guard BetaTester — one-tap scoped gate battery v1

## What is executed

NativeActivity Android platform UI: tap the screen area labeled TAP TO RUN to execute 24 **real calls** of the freestanding raf_gate_evaluate C11 kernel (6 directed controls + 18 bounded xorshift32-seeded state cases). Pixels render PASS/FAIL per case; a separate FILE PASS/FAIL indicates whether a local receipt was actually persisted. No Java app, external memory allocator, DB credentials, database pages, SQL, connectivity, crash recovery or service restart. For audit: the Android adapter uses Android libandroid and bionic I/O, while the C11 gate kernel and scenario runner stay freestanding.

The displayed PASS has scope **gate semantics only**. It is NOT engine functionality, Firebird client/server E2E or proof of actual device launch. All 24 cases are local deterministic conditions, not a complete event graph. A hardware-time seed is recorded; repeat the same seed in host runner to reproduce state-case ordering.

## On-device receipt format

Written only after the user's tap: private internal app data path with unique betatester-[seed].csv name, fopen exclusive mode to avoid silently overwriting prior receipts. Semicolon-delimited ASCII records include a header, 24 route/status lines and count summary. Each I/O failure must visibly yield FILE FAIL. No automatic network transfer. These files are app-private; extraction requires operator-controlled device debugging or a future separately reviewed SAF export.

## Build and evidence contract

- SOURCE: android/guard/{native_activity.c,beta_suite.c,beta_suite.h,test_beta_suite.c}.
- BUILD: scripts/build-android-guard-apk.sh per ABI; SDK/NDK used for platform packaging, separate from freestanding gate compilation.
- CI: GCC+Clang host falsifier test with five seeds (5x24=120 assertions per compiler) and two separately signed one-ABI APKs after freestanding gate.
- EVIDENCE: source-run SHA, Actions jobs and per-APK SHA256; USB/physical Android runtime receipts require external observation.
- CLAiM: IMPLEMENTED_UNTESTED until exact-head CI, physical=NOT_RUN, engine=NOT_INCLUDED, claim_allowed=false.
- SIGNING: disposable CI keystore differs by run, so upgrades across CI artifact runs may fail; uninstall only with explicit awareness of app-local receipt loss.
- PRIVACY: no user database observations or private environment identifiers logged.
- ROLLBACK: close draft PR/unmerged branch; main unchanged.

This enhancement must never be described as a standalone Firebird SQL APK. The engine lives in the separately licensed producer repository and requires a distinct, explicitly authorized disposable-DB integration gate.
