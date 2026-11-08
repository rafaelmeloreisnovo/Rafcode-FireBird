# Firebird MON$ — read-only monitoring boundary V1

**Status: SPEC_ONLY / NOT_IMPLEMENTED / NOT_RUN.** This is a producer-owned review contract for a future isolated adapter. No database connections, SQL commands or Firebird engine source have been executed or copied into Rafcode-FireBird.

## Primary sources (linked, never copied into executable code)

- Firebird 5 Language Reference, Monitoring Tables: https://www.firebirdsql.org/file/documentation/chunk/en/refdocs/fblangref50/fblangref50-appx05-montables.html
- Firebird 5 Language Reference, monitoring transaction/snapshot semantics: same official reference, Appendix E.
- Official Firebird source and IPL/IDPL notices: https://github.com/FirebirdSQL/firebird and https://firebirdsql.org/en/licensing/

## Priority P0: a monitoring table can have destructive semantics

The Firebird reference documents special DELETE operations on MON$ATTACHMENTS and MON$STATEMENTS that **terminate connections or cancel statements**, despite monitoring tables otherwise being described as read-only. A future adapter MUST NOT send DELETE, UPDATE, INSERT, DDL, EXECUTE BLOCK or arbitrary operator-supplied SQL.

**Fail-closed design:** compile-time immutable allowlist of exact SELECT statements selected by reviewed source version. Never construct SQL from user input, identifiers, names or metrics. An authenticated, least-privilege service context MUST establish a READ ONLY transaction, but authorization alone is not a substitute for a restricted statement set. Do not use SYSDBA. No self-healing, statement cancellation, connection close, backup restore or service restart from this adapter.

## Admissible source example for review only (NOT EXECUTED)

A candidate two-column observation from the current database, to be validated against the actual engine/version and permission context:

    SELECT MON$NEXT_TRANSACTION, MON$OLDEST_ACTIVE FROM MON$DATABASE

No path, SQL text, users, remote addresses, hostnames, statement plans, BLOB values or raw customer rows may leave the adapter. Even transaction counters may be operationally sensitive, so review visibility and retention before disclosure.

**Important:** MON$NEXT_TRANSACTION or MON$OLDEST_ACTIVE is NOT automatically evidence of real business transaction progress, I/O progress, lack of deadlock or service health. It may support diagnostics but cannot be passed as trusted raf_guard.progress without a separately validated semantic mapping.

## Snapshot and freshness

Firebird monitoring snapshots are transaction-scoped; a repeated MON$ query inside one transaction can yield unchanged data even when operations have progressed. A future adapter MUST close the observation transaction and start a new read-only observation for a new snapshot, with a bounded sampling interval and timeout. Reusing the same snapshot/failed query/clock rewind must produce typed UNKNOWN/STALE, not a zero counter and not a STALLED alert. A host-validated monotonic timebase is separate from server transaction time. Per-database observation only; no cross-database aggregation by inference.

## Required inputs / outputs

INPUT: operator-authorized disposable database connection, engine version, source of monotonic time, scope/permission, read-only transaction evidence, snapshot freshness witness, bounded counter values and privacy approval. Missing any required input -> ROUTE_STATE=BLOCKED.

OUTPUT: bounded, explicit known-bit counters only; no credentials, SQL text, user ID, raw path or unreviewed identifiers. The existing NUCLEOS guard may consume only externally validated semantic progress samples. The freestanding core MUST NOT create database connections, allocate heap, perform syscalls or network I/O.

## DMAIC / adversarial acceptance gates

- D: prohibit destructive monitoring operations, stale snapshots and privacy leaks.
- M: exact Firebird version, adapter source SHA, query allowlist SHA, isolated test database, transaction mode, privileges, elapsed time and observer result.
- A: deliberately attempt to request DELETE FROM MON$ATTACHMENTS and DELETE FROM MON$STATEMENTS through an unprivileged client API; future adapter MUST refuse **locally before DB execution**. Deliberately repeat one snapshot; must return STALE/UNKNOWN. Simulate missing timebase and insufficient permissions; must BLOCK.
- I: introduce only a read-only platform adaptor in a separate reviewed path after a disposable-DB operator authorization.
- C: require positive/negative real-DB receipts, privacy review and rollback, and keep G1=NOT_RUN until observed. No database fault injection or recovery on production.

## License / rollback

This specification is original RAFAELIA documentation under the scoped docs terms where rights are held. References are external, not relicensed. A future driver/protocol implementation needs its own copyright/license assessment. Revert this documentation-only commit or close DRAFT PR without touching Firebird server. claim_allowed=false; merge_allowed=false.
