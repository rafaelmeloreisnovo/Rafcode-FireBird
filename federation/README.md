# Federated code/data source connection V1 — explicit, pinned, read-only

**Implemented**: offline three-source pinned SHA metadata registry, fail-closed policy validator, opt-in in-memory C stage/commit/disable/failback, RFC5424 syslog text preview, offline status/plan CLI. New G1 optional **one-shot** Firebird `MON$` adapter code is supplied and synthetically testable without Firebird; no database connection has yet been executed by this project.

**Not implemented**: daemon, actual Firebird database failure repro, remote I/O root cause fix, syslog transport, automatic database failover, concurrent hot swap, persistent policy, HA, service restart, recovery or scheduler.

```sh
python3 -m federation.control status
python3 -m federation.mon_probe status
python3 -m federation.control plan-enable
python3 -m federation.control plan-disable
sh scripts/check.sh
```

These commands perform **no database or network I/O**. Never enable the committed policy. For a separately authorized disposable database see [the MON$ adapter contract](ADAPTER_CONTRACT.md).

## Federation safety contract

- Only sources pinned to reviewed SHA: producer `Rafcode-FireBird`, engine fork `firebird_rafcodephi`, upstream `FirebirdSQL/firebird`. Pin snapshots are not current HEAD claims.
- Default disabled; no secret, network or service access from baseline commands.
- C observer policy is in-memory single-threaded and never modifies DB state. `raf_fed_commit(ctx, 1)` requires explicit operator acknowledgment; `raf_fed_disable` is immediate; `raf_fed_failback(ctx,1)` changes observer configuration only.
- Monitor `MON$` counters are snapshots, **not** proof of committed inserts, writer progress or deadlock. It is unsafe to feed them to `RAF_KNOWN_PROGRESS`.
- Bounded RFC5424-shaped syslog preview has no transport or logging secrets.
- Engine failover, durable failback, rollback of transactions and HA require separate independent DBA/replication tests. No automatic promotion.

Read [federation/AGENTS.md](AGENTS.md), [issue #9269 source-model](FORENSICS_9269.md), [operator procedure](../ops/FAILSAFE_RUNBOOK.md), and the exact CI receipt before evaluating any claim.

## G1.1 disposable runtime SQL falsifier (Firebird 4 only)

[Standalone exact lab script](labs/firebird4_disposable_sql_gate.py) and [completed local receipt](../receipts/2026-11-06-FB4-disposable-mon-sql.json) are reproducible offline when `isql-fb` for Firebird 4 is installed. The script accepts **no external database path**, creates its own private ephemeral DB, attempts a forbidden INSERT under READ ONLY, verifies it failed and table remains empty, prints only safe aggregates, then cleans **only its own temporary test DB**. It is not part of default CI or a live Firebird attachment. Use this evidence only for SQL/TPB Firebird4 compatibility, not for issue #9269.

### Lab v2 recommended — no hardcoded environment paths

Use `python3 federation/labs/firebird4_disposable_sql_gate_v2.py` (requires independently installed Firebird4 `isql-fb`), optionally `RAF_G1_RECEIPT_DIR=/existing/private/directory`. The script creates only its own random temporary database and **unique 0600 receipts** in the selected directory, fails closed if missing/unwritable, and does not overwrite prior evidence. Do not place real database credentials in commands or logs. Original v1 lab source is historical and has a ChatGPT-only output location, preserved for audit. Neither version attempts a production Firebird connection or reproduces #9269.
