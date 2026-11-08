# NUCLEOS/AGENTS.md — freestanding producer

Read root [AGENTS.md](../AGENTS.md), [INDEX.md](INDEX.md), [LICENSE](LICENSE) before changing C source or tests.

**Invariant 1 (no side effects):** `src/` and `include/` contain C11 freestanding algorithms only: no libc, heap, filesystem, sockets, OS/Firebird pointers, syscalls, signals, privilege escalation or dynamic loading. Public API uses bounded `stdint.h` values. Isolation is verified by a freestanding object build and undefined-symbol scan.

**Invariant 2 (no autonomous recovery):** watchdog outputs only NONE/OBSERVE/ALERT and a bounded cadence hint; evidence gate outputs INVALID/BLOCKED/REVIEW_REQUIRED, never permission to act, merge or claim compliance.

**Invariant 3 (typed unknown):** a valid zero differs from an absent sensor; clock rewind, counter rewind, untrusted sample, incomplete policy or missing evidence -> UNKNOWN/BLOCKED. CPU% alone cannot identify a deadlock. Never reinterpret a gap as PASS.

**Invariant 4 (privacy):** event frame accepts counters/enums only; no identifiers, SQL, rows, secrets, IP addresses, query text or raw BLOBs. Operational counters may still be sensitive; require scoped consent/retention and safe redaction.

**Invariant 5 (integrity != authenticity):** CRC32 in v1 is accidental-corruption detection, not cryptographic evidence. Hosted SHA256 linkage in `audit/` is also insufficient without an external authenticated checkpoint.

**Test discipline:** `sh tests/run.sh` (core + gate). `sh ../scripts/check.sh` also checks the hosted receipt verifier. Run both GCC and Clang where available, record exact commit+binary environment and receipts. Preserve the earlier guard source blobs in [PROVENANCE](../PROVENANCE.md) when refactoring.

**Upstream contribution:** no Firebird engine source inside this tree. #9269 disk-full fault reproduction must occur only with a disposable isolated database; no live interception or restart. Preserve the upstream's IPL/IDPL license and contributor guidance for upstream fixes.

**Finishing:** summarize `F_ok | F_gap | F_next`; cite tested execution and declared rollback, never a general security attestation from local tests.

## Platform-dependent boundary, G0c

The separate NUCLEOS/ports/linux files may use exactly the Linux exit syscall for an opt-in synthetic executable. They MUST NOT be linked into NUCLEOS/src or NUCLEOS/include objects. Cross-linked ARM is NOT physical Android E2E. Use check-abi-falsifiers.sh before a new gate can pass, and keep human review mandatory.
