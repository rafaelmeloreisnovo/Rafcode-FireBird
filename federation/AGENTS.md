# AGENTS — federation scoped governance

1. Read `../AGENTS.md`, `../CURRENT_STATE.md`, this `README.md`, the exact manifest and tests before change.
2. Source registry must keep `PIN_ONLY` commits; do not accept mutable branches, network URLs or user-supplied arbitrary providers without new reviewed trust policy.
3. Only synthetic / metadata-only data. No Firebird connection string, user, SQL, client ID, IP, hostname, private secret, raw log or unredacted trace here.
4. Static policy `enabled=false` by default; preview is a proposal, not a running service; no automatic auth, DB writes, failover, restart, garbage-collect, backup or reconfiguration.
5. A C policy commit always requires explicit operator acknowledgment; disable cannot fail; failback needs known prior state. Adaptation is limited to bounded sampling and alert cadence; never modifies database state.
6. Change contracts and tests together. Every new switch needs a negative test and docs/spec reference; insist exact base/head SHA and CI readback.
7. No compliance/certification, uptime SLA, world-first, ISO 8000 conformity or cryptographic authenticity claim without independent evidence. See `../docs/ISO8000_QUALITY.md`.
8. End with F_ok / F_gap / F_next; commit on feature branch only, DRAFT/HOLD until integrated evidence.
