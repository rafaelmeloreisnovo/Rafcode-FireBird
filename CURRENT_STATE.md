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

## Federation delta — 2026-11-06 (new branch; append-only supersession)

- **Branch**: `feat/federation-optin-syslog-failsafe-v1` (based on the prior NIST scoped branch; `main` unchanged).
- **Tested code HEAD**: `a708a0add36b46cd38defff01a64d510039159d5`; CI run https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42168907060 => bounded-test SUCCESS.
- **F0**: `PASS_SCOPED_CI` (GCC/Clang C guard, gate, federation, syslog; 31 Python tests; validated offline CLI).
- **Default**: observer disabled; synthetic in-memory stage/ack/disable/failback only; syslog preview only, no network, no Firebird database activity.
- **F1–F4**: live read-only adapter, #9269 fault reproduction, syslog transport, genuine DB failover/hot-swap = `NOT_IMPLEMENTED/NOT_RUN`.
- **Plan target**: 2026-11-09 F0 already demonstrated in scope, next F1 2026-11-11 remains conditional (not scheduled). For exact scope and limitations see [federation receipt](receipts/2026-11-06-FEDERATION-G0-CI.json).
- **Authority**: producer owns original federation tools; Firebird upstream/fork source stays unchanged. `claim_allowed=false`, `merge_allowed=false`.
