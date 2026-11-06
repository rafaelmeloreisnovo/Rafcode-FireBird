# Threat model — falsifiers before assurances

**Assets:** database integrity, source provenance, service availability, privacy, reproducible evidence, operator authority.

**Threats:** indefinite CPU spin after disk-full (#9269), GC/page-latch race (#9189), stale counter, repeated/reordered event, forged telemetry, forged entire hash chain, disk-full while writing audit record, agent-induced service restart, privacy leakage via raw SQL or logs, secret compromise, unbounded observer overhead, version drift of NIST mapping.

**Current mitigations:** freestanding no-I/O code, known-field bits separating UNKNOWN from zero, capped cadence, only alert/review-required outputs, closed JSON schema, duplicate-key/truncation/hash/sequence checks, synthetic falsifiers, branch-scoped change control and separate licenses.

**Residual:** SHA-256 without externally authenticated checkpoint is **rewritable**; CRC32 is non-cryptographic; forged input metrics may pass checks; scoped tests do not prove database durability, cryptographic authenticity or compliance.

**Counterexamples to test next:** low CPU but no progress, high CPU with progress, clock rewind, counter rollback/wrap, missing IO bit, stale/partial frame, two writers racing on a log, full disk during receipt persistence, modified parent chain with recomputed hashes, leaking host identifiers, adversarial SI/OS delays, crash/restart after partially written file.

**Fail-safe:** on unknown or degraded input return UNKNOWN/BLOCKED, preserve gap, never modify the database. Future retention/deletion policies require separate user-authorized governance; no auto deletion.
