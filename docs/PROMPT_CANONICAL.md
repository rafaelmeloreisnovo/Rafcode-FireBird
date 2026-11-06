# RAFAELIA Ω — Technical orchestration prompt for Firebird federation

**Objective**: in producer `rafaelmeloreisnovo/Rafcode-FireBird`, design and verify an opt-in, versioned, least-privilege, read-only integration boundary to the separately licensed Firebird engine. Keep database transactions, availability, privacy and operational authority intact.

**Required dispatch**: INTENT → CURRENT_STATE → μREAD (up to 3 roots) → AUTHORITY/SOURCE_MIN → BASELINE/CTQ → FALSIFIERS → MINIMAL_REVERSIBLE_PATCH → EXACT_HEAD_TEST → READBACK → RECEIPT → POINTER → R3.

**Hard constraints**:
- SOURCE ≠ ARTIFACT ≠ EXECUTION ≠ EVIDENCE ≠ CLAIM. Unknown remains typed TOKEN_VAZIO. No invented PASS.
- Pin external repo sources to immutable SHA; no network/credential/sql access by default.
- C11 freestanding state machine with no heap, libc or syscalls; OS/Firebird adapters separately reviewed.
- Observer enabled=false by default; explicitly staged/acknowledged activation; kill switch always available; bounded sampling; UNKNOWN -> no actuation.
- Syslog preview strips identifiers and raw content. Transport optional, separately reviewed; no automatic sending.
- Rollback code/config ≠ DB transaction rollback ≠ backup restore ≠ primary/replica failover. Never automate database operations without human authorization and proven consistency tests.
- Document NIST/ISO mappings as informative, not certifications. License boundaries upstream Firebird vs MIT observer vs CC BY docs.
- Keep SOP/AGENTS/roadmap/release notes/timeline close to executable contracts; changes append-only with SHA/readback and independent tests.

**Deliverables**: feature branch, compiled falsifiers, read-only source pins, source/control graph, disabled-by-default config, negative tests, exact CI receipt, SOP and rollback plan, current-state pointer. If adapter/test authority is unavailable: deliver scoped subset and explicitly BLOCK remaining gates.

**R3** = verified implementation / evidence gaps / smallest safe reversible next action.
