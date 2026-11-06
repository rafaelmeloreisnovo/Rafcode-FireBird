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
