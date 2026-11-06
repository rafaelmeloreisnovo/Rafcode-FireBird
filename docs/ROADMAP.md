# Reversible execution checkpoints — not a background promise

| Phase | Target | Independent evidence / gate |
| --- | --- | --- |
| P0 | Bootstrap producer repo, provenance, AGENTS, scoped C and Python tools | Exact GitHub readback and local synthetic tests |
| P1 | Validate freestanding ABIs, compiler matrices and strict CII | G0 GCC/Clang, remote CI state distinct from local |
| P2 | Design opt-in Firebird Trace/MON$ adapter with read-only grants | Privacy assessment, no DB writes, no production credentials |
| P3 | Reproduce upstream [#9269](https://github.com/FirebirdSQL/firebird/issues/9269) on disposable volume | Real disc-full fault and integrity post-check, bounded timeout |
| P4 | Separately investigate [#9189](https://github.com/FirebirdSQL/firebird/issues/9189) page-latch race | Regression against each version, no mixed patch |
| P5 | Cryptographic receipt signatures with key lifecycle and external independent anchoring | Signed checkpoint verified by external party; no keys in repo |
| P6 | Versioned NIST/OSCAL evidence mapping and independent audit | Control-by-control assessment, not self-declared certification |

No fixed delivery times; no auto actions, merges, releases, destructive cleanup or production probes. The near-term falsifier is that a synthetic proof cannot guarantee resilience during actual disk exhaustion.

## Federation v1 increments (dependency-ordered; no scheduled background work)

| Gate | Planning target | Dependency | Evidence rule |
| --- | --- | --- | --- |
| F0 | 2026-11-09 (planning only) | exact-head C/Python CI, strict default-disabled manifest | PASS_SCOPED, no runtime claims |
| F1 | 2026-11-11 (planning only) | read-only MON$ adapter design, fresh transaction, privacy review | approval + prototype sandbox only |
| F2 | 2026-11-13 (planning only) | #9269 disk-full reproduction, disposable volume, bounded timeout | actual failure/recovery receipt |
| F3 | TBD, gated | syslog over TLS adapter with redaction and backpressure | independent security review |
| F4 | TBD, gated | real HA failover/hot-swap proposals | RPO/RTO, split-brain fencing and operator review |

Target dates are coordination proposals, not commitments, release dates or evidence of completion. If dependency absent: deadline state `BLOCKED`; no invented milestone.

### F1.1 — subgate (2026-11-06 candidate, no live execution)

Implement single-process-isolated Firebird MON$ snapshot over fresh read-only transaction, mock driver error/timeout tests and no private data. **Done at source level only**; actual sandbox readback / latency / privileged signal semantics remain gates F1.2 and F2. Deadlines are targets and not promises.
