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

## Status delta — 2026-11-08 G0c

P1: scoped Linux-host run + LLVM ELF object audit PASS on exact HEAD 38c34e1; ARMv7/AArch64 linked only and physical-device E2E NOT_RUN. P2: a reviewed **adapter contract** has been documented at [FIREBIRD_MONITORING_READ_ONLY_BOUNDARY_V1.md](FIREBIRD_MONITORING_READ_ONLY_BOUNDARY_V1.md). P2 implementation and disposable Firebird DB validation are NOT_IMPLEMENTED/NOT_RUN. Risk: privileged DELETE in MON$ may terminate connections or statements; this path MUST never be exposed by the proposed observer. Next step depends on an authorized disposable Firebird runtime; no production access.
