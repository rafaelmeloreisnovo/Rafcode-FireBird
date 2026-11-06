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

## G1 RAFCODE MON probe delta — 2026-11-06 (exact source CI, DRAFT/HOLD)

- **Feature source HEAD tested**: `9438726c2a5a868e65957aa937e967f7e3a1967d` (parent PR#2 branch; no merge/main mutation).
- **CI**: [run 42172109238](https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42172109238) SUCCESS, job 127742099302. GCC+Clang C checks unchanged, 17 audit Python and 37 federation Python tests PASS.
- **Incident center**: Firebird [#9269](https://github.com/FirebirdSQL/firebird/issues/9269) distinguishes H1 dirty-cache/writer-suspend, H2 mismatched CDS hash key->descriptor, H3 other unknown. Evidence only from source code snapshot `f78dbc4e500e8896a4004dd2fb7d7a94785e54df`; causation unproven.
- **G1**: bounded one-shot MON$ Firebird adapter code + negative fake client tests = `PASS_SCOPED_CI`; actual Firebird DB connection, Windows disk-full repro, driver binary validation = `NOT_RUN`.
- **Safety**: default policy OFF, operator ACK + disposable env declaration; explicit read-only TPB, rollback/close, bounded child timeout, no engine writes by adapter code. Firebird ON CONNECT/DISCONNECT triggers can have side effects outside read-only transaction => **database unchanged cannot be claimed**.
- **G2/G3/G4**: OS-level hang reproducer, engine fix and independent attestations BLOCKED by missing runtime/authoritative evidence. `claim_allowed=false`, `merge_allowed=false`.
- **Receipt**: [G1 scoped CI](receipts/2026-11-06-MON-G1-scoped-ci.json); previous `F0` evidence preserved. R3 next: disposable runtime probe & exact #9269 causal witness before any engine modification.

## G1.1 REAL disposable Firebird 4.0 SQL check — 2026-11-06 (scope boundary)

- **Independent lab executable source**: `federation/labs/firebird4_disposable_sql_gate.py`, Git blob `b499384ca8a4daf693386d6d4659386d05acfd8b`, byte-identical to script executed locally. 
- **Local execution**: Linux x86_64 / Firebird LI-V4.0.5.3140 embedded against *new ephemeral private test database*, query `MON$DATABASE` LEFT JOIN `MON$IO_STATS` success; `MON$PAGE_SIZE=8192`, `MON$PAGE_READS=86`, `MON$PAGE_WRITES=3` in one snapshot. `SET TRANSACTION READ ONLY READ COMMITTED RECORD_VERSION` refused DML ("attempted update during read-only transaction"), post-rollback COUNT=0. 
- **Receipt**: `receipts/2026-11-06-FB4-disposable-mon-sql.json`, Git blob `c72660bfbaa86c4ee87d8ffd8c37b9109f11d671`, byte-identical to locally generated JSON. Self hash `f6cc410869535a136a5566ff9c100200142ece99e501b3cf6cc16915d31c5294`, NOT signed or independently anchored.
- **LIMITS**: This is a *real Firebird 4 SQL/TPB check*, NOT runtime execution of the `federation/mon_probe.py` Python driver (not installed), NOT Firebird 5.0.3/5.0.4 Windows #9269 reproduction, NOT a cause/fix/HA claim. ON CONNECT trigger risk in arbitrary DB still applies; new disposable test DB only. 
- **G1.1**: `PASS_SCOPED_FIREBIRD4_SQL`; G1.2 actual Python driver/runtime and G2 Windows fault still `NOT_RUN`. Existing GitHub synthetic G1 CI remains independent; no production connection, no engine patch, no merge, `claim_allowed=false`.

## G1.1 portability/hotfix — append-only v2 (2026-11-06)

- Discovered G1.1 original lab script hardcoded `/mnt/data` output path, not portable to operator environments (Termux included). Historic v1 script/blob/receipt are **preserved**, never overwritten.
- **New independently executed V2** `federation/labs/firebird4_disposable_sql_gate_v2.py`, Git blob `3343e65f3ac0d87a7726cd02f8191903add6c6fa` equals local executed bytes. Unique receipt name, `RAF_G1_RECEIPT_DIR` optional (defaults current working directory), atomic exclusive creation O_EXCL with permissions 0600 and fsync; never overwrites prior receipt.
- Real Firebird4.0.5 embedded two independent runs `PASS_SCOPED_FIREBIRD4_SQL`, both readonly INSERT rejected/COUNT=0; two separate receipt JSON files remained with mode 0600; nonexistent output directory produced `BLOCKED_RECEIPT_DIRECTORY` exit 2, no prior receipt modified.
- V2 example receipt `receipts/2026-11-06-FB4-LAB-PORTABLE-V2.json`, Git blob `72ec9d5b743568da94f17448df752378dff62122`, self SHA `c112434a02126ad7acbfc2d144117ba8ce11704b64e78ff8a51d61bc6accac94` (self integrity, NOT signature).
- V2 **does not** run the optional Python Firebird driver, reproduce Firebird5 Windows #9269 or prove DB failover; claims remain `false`. Rollback: use previous v1 source for historic reproduction or close draft; no engine/source/main mutation.
