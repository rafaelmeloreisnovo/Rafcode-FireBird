# Firebird adapter contract, design only — no runtime executable yet

**Objective**: optional connector that samples Firebird monitoring capabilities without modifying Firebird source, transactions or configuration.

## Permitted signals (future implementation)

- Snapshot of safe aggregate counters via a **fresh short read-only transaction** for each observation. Firebird monitoring tables MON$ are snapshot-bound per transaction; reusing a long-lived transaction can show stale values.
- Firebird Trace API only after explicit administrator/user authorization and privacy review. Trace can contain SQL/parameters and identifiers; **do not enable by default**, do not capture statement bodies, and validate the version-specific privileges.
- Process-level CPU/availability indicators only when separately authorized, with bounded overhead and no privileged hooks.

## Required adapter guarantees

`provider_id | pinned_adapter_version | schema_version | monotonic_tick | known_mask | progress_count | io_error | observed_at_source | trust_level`; no raw SQL, addresses, credentials, row/record content, BLOBs. Producer defines typed omissions, no fake 0.

If adapter lacks a trustworthy progress counter, return `UNKNOWN` and no alert that claims deadlock. On loss of connectivity, disable outgoing telemetry or emit bounded UNKNOWN status; **never** restart Firebird, reconnect infinitely, or alter the DB.

Integration and deactivation must be opt-in, with least privileges, quotas, health deadlines, cached last-known-good config and explicit operator acceptance. Config swaps require adapter-specific synchronization and rollback because the current freestanding policy state machine is single-threaded.

## Rollback, failback and failover boundaries

- Rollback (Git): revert adapter code/config in a separate branch.
- Failback (observer): restore last known safe observer policy after operator review.
- Fallback (telemetry): bounded local preview or stop, never change DB routing.
- Hot swap (observer): **NOT_IMPLEMENTED**; requires serialized atomic publish, safe resource handoff and concurrency tests.
- Failover (database): **NOT_IMPLEMENTED**; must test transactional safety, split-brain fencing, durable commit and RPO/RTO before an operator-run procedure can be proposed.

No inference that an observer action repairs Firebird upstream #9269. For a real reproducer use a disposable volume and strict timeout.
