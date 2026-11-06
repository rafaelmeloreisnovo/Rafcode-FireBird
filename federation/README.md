# Federated code/data source connection V1 — explicit, pinned, read-only

**Implemented**: JSON metadata registry of exactly three source repositories pinned to immutable Git commit SHA, strict offline schema verifier, opt-in *observer* policy with disabled default, Python offline CLI to inspect or plan activation, freestanding C policy stage/commit/disable/failback, safe RFC5424 text preview.

**Not implemented**: an actual Firebird connection, OS service, live automatic integration, database/cluster failover, transport syslog, network polling, SQL/Trace capture, replication, concurrent hot swap or operational monitoring. These require distinct independently reviewed adapters.

```sh
python3 -m federation.control status
python3 -m federation.control plan-enable
python3 -m federation.control plan-disable
sh scripts/check.sh
```

These CLI commands **do not write**, connect or enable anything. For demonstration an operator can explicitly stage+commit a validated policy using the C API; without a future runtime adapter nothing is installed.

## Federation safety contract

- **Source authority**: producer `Rafcode-FireBird`, external engine fork `firebird_rafcodephi`, upstream `FirebirdSQL/firebird`. SHA pins are a snapshot, not claims of current upstream HEAD.
- **Deny by default**: policy `enabled=false`, sink `NONE`, no network, syslog transport `DISABLED`, no privileges, no secrets.
- **Switches**: `raf_fed_stage` refuses invalid/stale/unknown policy, `raf_fed_commit` requires explicit operator acknowledgment; `raf_fed_disable` is always available; `raf_fed_failback` needs a prior known configuration and acknowledgment. These are synchronous *in-memory* states, not concurrent hot deployment.
- **Fallback**: UNKNOWN telemetry -> NONE. Stalled/IO_ERROR -> ALERT. No fork/source/db mutation.
- **Failover**: database failover is **NOT_IMPLEMENTED**. Separate tests for split-brain, durable acknowledgments, replicas, consistency and recovery point are mandatory before even proposing it.
- **Syslog**: `raf_syslog_preview` emits a sanitized, bounded RFC5424-shaped frame only; no transport, hostname, timestamp, SQL, client identifiers or raw values. RFC 5424 permits '-' for absent header values; any actual TLS transport would require an independent audited adapter.
- **Rollback**: disable observer immediately; operator-reviewed failback to the previous in-memory observer policy; revert Git branch. No database restore by this software.

See [federation/AGENTS.md](AGENTS.md) and [adapter contract](ADAPTER_CONTRACT.md). Source changes from external repos are never applied automatically.
