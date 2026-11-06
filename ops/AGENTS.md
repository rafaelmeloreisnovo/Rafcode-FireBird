# Operations agents — boundaries

Read `../AGENTS.md`, `../CURRENT_STATE.md`, `../federation/AGENTS.md`. Only humans with explicit service authority may perform Firebird/database/network failover, backups, restart or configuration changes.

AI/automation MAY: inspect read-only repo metadata, run synthetic G0 tests, propose observer config, classify gaps and assemble a receipt. AI MUST NOT: apply a live adapter without an operator, reroute SQL traffic, edit production database, install daemon, send syslog to unknown address, flush cache, delete files or claim ISO/NIST certification.

Every procedure uses PRECONDITIONS → DRY RUN → CHECKPOINT → ACTION → TEST → RECEIPT → ROLLBACK/FAILBACK. On missing field: `TOKEN_VAZIO` and BLOCKED; emergency disable of observer is always allowed. Any recovery action changing data is outside this repo and requires a separate authorized and tested runbook.

Deadlines in `ops/TIMELINE.md` are proposal dates only. Release notes state exactly which code and CI run prove scope, not what remains aspirational.
