# Release notes — version 0.2.0-alpha (unreleased / DRAFT)

## Added (on feature branch, not deployed)
- Pinned, three-source federation registry: producer / Firebird fork / upstream read-only metadata.
- Strict policy parser, dry-run-only plan-enable/plan-disable CLI with disabled default.
- Freestanding observer config stage/acknowledged commit/disable/acknowledged failback. No service hooks.
- Freestanding RFC5424-shaped sanitized syslog preview. No socket or transport.
- Synthetic falsifiers and CI targets for C11 + Python.
- SOPs, agent routes, ISO 8000-61/63 informative quality model and append-only timeline.

## Compatibility and safety
Engine: **unchanged**. No schema migration, no database connection. `main` unchanged. ABI `RAF_FED_ABI=1`. Policy `schema=raf-federation-policy-v1`. Invalid revision/sink fails closed. Rollback is observer/config-only.

## Not included / release blockers
Live monitoring adapter, background service, automatic failover, persistent hot swap, syslog TLS transport, private logs, backups, authenticating signed checkpoints, deployed rollback, or ISO/NIST certification. All are `NOT_IMPLEMENTED/NOT_RUN`.

**Version is a proposal label, not a GitHub Release/tag or independently certified package.** No publication or merge without human review.

## Test receipt appended (2026-11-06; no release/tag)

- [Scoped CI execution](https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42168907060) for `a708a0add36b46cd38defff01a64d510039159d5` succeeded: guard 30041, gate 10028, federation 50026, syslog 20008 checks per GCC/Clang build; 17 audit + 14 federation Python tests.
- Failure of hidden telemetry or unknown fields must suppress action; test environment has zero DB interactions. Still **unreleased**, unmerged, no Firebird E2E.

## G1 — opt-in monitoring probe candidate (unreleased, stacked branch)

- Added `federation/mon_probe.py` with explicit operator ACK, validated enabled-preview policy and disposable environment, a single isolated read-only `MON$` snapshot, transaction rollback/close, bounded child deadline and sanitized public output.
- Added adversarial fake-driver tests, [forensic issue #9269 model](../federation/FORENSICS_9269.md), source references and updated adapter contract.
- No Firebird engine source touched, no DB connection ever performed by CI, no dependency installed, no syslog transport or autonomous recovery.
- Exact-head CI and readback to be appended only after verified run. Until then `IMPLEMENTED_UNTESTED`, `claim_allowed=false`, `merge_allowed=false`.

## G1 test receipt — 2026-11-06 (no runtime release)

Exact tested code `9438726c2a5a868e65957aa937e967f7e3a1967d`, [CI 42172109238](https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42172109238) succeeded. 37 Python federation + 17 Python audit tests, plus GCC/Clang C G0/G1 regressions. Fixed a test fixture path, blocked false success for UNKNOWN and narrowed misleading `database_mutations=0` to `adapter_write_statements_issued=0`. Firebird's database event triggers may write on connection; no live DB was touched. Parent trial failure 42171784931 is preserved in timeline; current G1 is PASS_SCOPED_CI only. No merge, no live driver installation, no HA or disk-full recovery claim.

## G1.1 lab evidence supplement — 2026-11-06 (still unreleased)

A real embedded Firebird 4.0.5 engine on Linux x86_64 executed the same fixed MON$ aggregate SELECT used by the optional probe. A temporary-db READ ONLY TPB rejected INSERT with SQLSTATE 42000, subsequent rollback and COUNT(*) verified zero rows. Evidence JSON and exact executed script are committed as Git blobs under `receipts/` and `federation/labs/`. The self-hash detects accidental changes only; it does not authenticate observer identity or execution. Code of `mon_probe.py` was NOT exercised against real engine, Firebird 5.0 #9269 remains UNRESOLVED; no release/merge.

## #9269 H2 prevention gate — vendor libcds API reviewed

Pinned Firebird vendor `MichaelKVList` API shows `erase_with` is a key-order comparator, not atomic key+value compare-and-delete, and `erase(key, Func)` is not an action veto. Reject naive pointer-aware comparator/erase callback patches pending a value-conditional removal or proved synchronization design. Forensics doc specifies the falsifying race schedule; no engine patch or libcds runtime test claimed.
