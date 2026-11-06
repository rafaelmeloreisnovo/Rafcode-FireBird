# CURRENT_STATE — Rafcode-FireBird producer

- **Producer**: `rafaelmeloreisnovo/Rafcode-FireBird`; default branch `main` remains untouched while this implementation is on a feature branch.
- **Initial source**: `main` commit `b4f7d8601203dbc2426a6db49db92bee40fc3077` (README-only bootstrap).
- **Active implementation route**: `feat/nist-governance-audit-kernels-v1`.
- **Status**: `IMPLEMENTED_SCOPED` / `TESTS_LOCAL`; remote CI and vendor runtime require independent observation.
- **Included**: watch-only kernel, gate policy kernel, test harnesses, Python read-only digest verifier, crosswalk, licensed docs and narrow CI.
- **Known gaps**: no Firebird runtime adapter; no #9269 disk-full reproduction; no external signatures/anchors; no NIST conformity assessment; no production privacy audit.
- **Denied claims**: `claim_allowed=false`; `merge_allowed=false`; no automatic recovery, deployment or data access.
- **Rollback**: discard or revert feature branch commits; no production service or database was modified.
- **Next**: exact-head readback + source tests + review of CI (if any); then a read-only adapter spec over disposable Firebird DB.
- **Prior technology**: C11 guard from `firebird_rafcodephi` recorded in [PROVENANCE.md](PROVENANCE.md). This is an explicit import, not an independently re-invented source.
- **Evidence ledger**: absent external independent attestation => `TOKEN_VAZIO`; no signed checkpoint should be assumed.
