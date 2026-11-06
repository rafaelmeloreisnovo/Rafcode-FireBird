# 001_PONTEIRO / START HERE — audit-ready routes

**INTENT -> CURRENT_STATE -> μREAD -> ROUTE -> SOURCE_MIN -> AUTHORITY -> ACT -> EVIDENCE -> μWRITE -> R3**

1. Confirm [CURRENT_STATE](../CURRENT_STATE.md), repo `main` SHA and feature branch HEAD.
2. Work on one of three bounded roots (depth 1): [NUCLEOS](../NUCLEOS/INDEX.md) for code, [audit](../audit/README.md) for receipt validation, [controls](../controls/NIST_CROSSWALK.csv) for compliance mapping. Do not crawl unrelated corpus.
3. Check root [AGENTS.md](../AGENTS.md) plus the target directory's agent rules, license and [provenance](../PROVENANCE.md).
4. Resolve source, authority, test environment, evidence acceptance rule. On missing evidence, `ROUTE_STATE=BLOCKED`, `TOKEN_VAZIO`.
5. Execute bounded changes in feature branches; record one verified receipt; keep [ROADMAP](../docs/ROADMAP.md) and current state accurate only on material changes.
6. No production data/no background recovery/no auto-release.

## Typed routes (L9 subset)

- **L** longitudinal: baseline commit -> implementation commit -> scoped evidence.
- **O** orthogonal: fork engine vs standalone audit kernels vs independent auditor.
- **T** transversal: issue #9269 -> observer -> falsifiers -> privacy -> rollback.
- **P** provenance: source repo+commit+blob, license, derived artifact.
- **C** contextual: disposable database only; production UNKNOWN.
- **R** relational: typed `source_of`, `verified_by`, `blocked_by`, `supersedes`.
- **I** indexical: `001_PONTEIRO`, `CURRENT_STATE`, `INDEX`, receipts.
- **E** evidential: local test PASS_SCOPED is not NIST certification.
- **A** adaptive: only cadence within configured bounds; never autonomous recovery.

`SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`. Return R3 with each meaningful cycle.

## Federation dispatch (added 2026-11-06)

- Producer implementation: [federation/README.md](../federation/README.md) → exact pins [sources.v1.json](../federation/sources.v1.json) → disabled [policy.v1.json](../federation/policy.v1.json).
- Standalone policy and syslog: [NUCLEOS/INDEX.md](../NUCLEOS/INDEX.md), then C headers, tests and CI receipt.
- Operator: [ops/PROCEDURES.md](../ops/PROCEDURES.md) → [ops/FAILSAFE_RUNBOOK.md](../ops/FAILSAFE_RUNBOOK.md) → [ops/TIMELINE.md](../ops/TIMELINE.md) → [ops/RELEASE_NOTES.md](../ops/RELEASE_NOTES.md).
- Data quality and documentation rules: [docs/ISO8000_QUALITY.md](../docs/ISO8000_QUALITY.md), [docs/RECONSTRUCTION.md](../docs/RECONSTRUCTION.md), [docs/PROMPT_CANONICAL.md](../docs/PROMPT_CANONICAL.md).
- **Authority boundary:** this producer owns observer policies. [Firebird fork](https://github.com/rafaelmeloreisnovo/firebird_rafcodephi) governs engine patch branches; no automatic sync. UNKNOWN evidence -> BLOCKED, not an inferred success.
