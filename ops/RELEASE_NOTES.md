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
