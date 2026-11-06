# Rafcode-FireBird | RAFAELIA Ω — Verifiable Data Governance

**Independent, experimental audit and evidence tooling for database reliability.** This repository is *not* a distribution of Firebird, not an official Firebird/NIST product, not a NIST certification, and not a claimed world-first invention.

## START HERE

- [001_PONTEIRO/START_HERE.md](001_PONTEIRO/START_HERE.md) — human/AI route to the current producer state, authority and next gates.
- [CURRENT_STATE.md](CURRENT_STATE.md) — explicit current scoped status and unknowns.
- [AGENTS.md](AGENTS.md) — contributor guardrails; [NUCLEOS/AGENTS.md](NUCLEOS/AGENTS.md) for freestanding kernels.
- [NUCLEOS/INDEX.md](NUCLEOS/INDEX.md) — standalone C11 watchdog and evidence gate.
- [federation/README.md](federation/README.md) — opt-in source pinning, safe policy staging/disable/failback, syslog preview; no live Firebird connection.
- [ops/PROCEDURES.md](ops/PROCEDURES.md) and [ops/FAILSAFE_RUNBOOK.md](ops/FAILSAFE_RUNBOOK.md) — human/AI runbooks and gated operator decisions.
- [docs/ISO8000_QUALITY.md](docs/ISO8000_QUALITY.md) — ISO 8000-61/63 **informative** data quality framework, not a certified process.
- [audit/README.md](audit/README.md) — offline read-only receipt-chain verification.
- [controls/NIST_CROSSWALK.csv](controls/NIST_CROSSWALK.csv) — **informative** mapping of intended controls to evidence, not an assessment.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — typed provenance graph, privacy model, physical/logical boundaries.
- [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md), [docs/ROADMAP.md](docs/ROADMAP.md) — falsifiers and reversible milestones.
- [LICENSES/SCOPES.md](LICENSES/SCOPES.md) — separate original code / documentation licenses and Firebird boundary.

## Repositories and authority

**This repository** is the producer for the independent RAFAELIA audit code and its contracts. The pre-existing [firebird_rafcodephi](https://github.com/rafaelmeloreisnovo/firebird_rafcodephi) is a *different* Firebird source fork, and its earlier `NUCLEOS/` experiment is recorded as provenance, not silently overwritten. The [official upstream](https://github.com/FirebirdSQL/firebird) governs Firebird engine fixes and IPL/IDPL licensing. No upstream code was copied into this repository.

## Implemented / unimplemented

**Implemented:** offline opt-in observer policy stage/disable/failback (in-memory only), RFC5424 syslog formatter (text only), strict pinned source manifest validator, deterministic freestanding C11 progress observer (no OS hooks), freestanding evidence-gate decision logic (no automatic approval), fixed-frame CRC32 for accidental corruption, a hosted Python standard-library receipt verifier with SHA-256, synthetic negative tests and path-scoped CI configuration.

**NOT_IMPLEMENTED / NOT_RUN:** Firebird adapter, live storage/CPU/network monitoring, encrypted/signature-backed receipts, independent anchoring, production data validation, automatic recovery, rollback of transactions, cross-platform ABI certification or a NIST compliance assessment. Hash linkage alone is not authentication.

Run offline tests: `sh scripts/check.sh`. The script never connects to Firebird or writes a database. Integration is opt-in, read-only and must pass independent gates. `claim_allowed=false` until external evidence and review exist.

**FIAT LUX:** SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM.
