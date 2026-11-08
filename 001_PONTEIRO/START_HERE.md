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

## New isolated route — 2026-11-08

- [Original/official license boundary](../LICENSES/AUTHORIAL_FIREBIRD_BOUNDARY.md): independent MIT kernels vs official Firebird IPL/IDPL; original import lineage unchanged.
- [Freestanding ABI falsifier](../docs/FREESTANDING_ABI.md): compile-only ARMv7/AArch64 ELF object gate; hosted CI/runtime and Android execution are different states.
- [Pure shell executable gate](../scripts/check-freestanding-abi.sh): never an APK generator, Firebird engine build or proof of no hardware syscalls.

## G0c route

- docs/PROCEDURAL_ASSURANCE_V1.md: six-sigma DMAIC plus ISO/IEC/IEEE/W3C/IETF/NIST-inspired control objectives and evidence gates.
- NUCLEOS/ports/linux/README.md: separate syscall-aware entry adapters, no libc, no Firebird and no APK.
- scripts/check-core-object.sh and scripts/check-abi-falsifiers.sh: positive/negative source tests. Any tool absence blocks; actual ARM hardware remains NOT_RUN.
