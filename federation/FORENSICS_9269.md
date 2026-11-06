# Firebird #9269 — source-anchored fault model (hypotheses, not fixes)

## SOURCE AND BOUNDARY

Primary report: https://github.com/FirebirdSQL/firebird/issues/9269 (Windows 11, NTFS, Firebird 5.0.3/5.0.4, 1 GB VHDX, 4 insert writers, full disk; intermittent persistent 100% CPU after space was freed). The reporter observes 2 get_buffer() loops. No complete independent reproduction by this repo.

Engine source inspected at immutable fork commit `f78dbc4e500e8896a4004dd2fb7d7a94785e54df`:
`src/jrd/cch.cpp` blob `b52272e6286c1df06d7bd8eb9483fb370204477d`.
No source patch or inferred branch merges.

## Two competing mechanism hypotheses (both may apply)

**H1 — dirty cache exhaustion / suspended background writer:**
- `get_buffer()` waits for a free/old buffer, `get_oldest_buffer()` marks dirty candidates and wakes writer; in absence of a candidate, it yields and tries again.
- `write_page()` sets `BDB_io_error` + `DBB_suspend_bgio` after an I/O error. `cache_writer()` skips work while `DBB_suspend_bgio` is set.
- Cross-check: release of the suspension is tied to successful write of an error buffer or `CCH_forget_page()`. Candidate starvation and lack of retry may form a persistent liveness failure; **not proven**.

**H2 — mismatched cache descriptor identity after page removal:**
- `get_buffer()` can see `bdb2->bdb_page != page` and retry `emplace()`.
- CDS `BCBHashTable::remove(BufferDesc*)` uses `list.erase(bdb->bdb_page)` by key; a key-only erase deserves scrutiny if a newer occupant can exist after a concurrent reassign.
- A static callsite does **not** prove ABA, stale ownership, invalid erase, or the user report. Need ordering, list primitive guarantees, hazard-pointer semantics and concurrency schedule.

**H3 — unrelated lock/contention path:** high CPU and stalled inserts can arise from distinct paths; until stack samples with symbols + thread states are reproduced, assume independent hypotheses.

## Adversarial falsifiers / expected evidence

| Model | Falsifier | Required test |
| --- | --- | --- |
| H1 | Background writer is active and dirty queue drains despite permanent hang | same Windows build, cache writer flags and dirty counts sampled externally |
| H2 | CDS hash for page always returns descriptor with matching `bdb_page` | deterministic adversarial replacement schedule + bounds/TSAN if supported |
| H3 | Hang persists with no writer suspension and no hash identity mismatch | repeatable minimal repro with call stacks and lock ownership |

A one-time `MON$` query does **not** prove writer availability or completion: system monitoring views are transaction-scoped snapshots and may itself fail to respond during #9269. Even an increasing page-write counter is **not** an end-to-end committed transaction receipt. The read-only opt-in probe in `mon_probe.py` only reports `MON_SNAPSHOT / UNKNOWN / DEADLINE_EXCEEDED`.

## Gates and recovery

G1 = independently fetched Firebird MON$ snapshot on disposable DB with bounded wall-clock, **not yet run**. G2 = genuine #9269 Windows disk-full crash/hang witness with DBA-authorized disposable environment, **not run**. G3 = narrow tested engine fix, **not implemented**.

Never recreate disk exhaustion on a production volume, restart the engine autonomously, discard or rewrite page cache, pretend that freeing disk is a repair, or accept a `TIMEOUT` as proof of the engine defect.

**Root hypothesis state: UNRESOLVED.** Distinguish `source evidence`, `hypothesis`, `execution` and `actual causal proof`. All engine mutation/promotion claims remain blocked.

### References

- Firebird monitor semantics: https://github.com/FirebirdSQL/firebird/blob/master/doc/README.monitoring_tables
- Official Firebird Python driver transaction guide: https://firebird-driver.readthedocs.io/usage-guide/transactions/
- Engine source at SHA: https://github.com/rafaelmeloreisnovo/firebird_rafcodephi/blob/f78dbc4e500e8896a4004dd2fb7d7a94785e54df/src/jrd/cch.cpp

**Additional observability confounder:** Firebird database event triggers (ON CONNECT/ON DISCONNECT) run in their own transactions, so even an explicitly read-only monitoring transaction cannot certify the entire *attachment lifecycle* had no DB effects. Source: https://www.firebirdsql.org/file/documentation/html/en/refdocs/fblangref50/firebird-50-language-reference.html . Gate requires disposable test DB and trigger audit.

## H2 negative design gate — exact vendored libcds contract review (2026-11-06)

Before suggesting a cache-hash hotfix, inspect upstream Firebird's bundled `extern/libcds/cds/container/impl/michael_kvlist.h` at source SHA `f78dbc4e500e8896a4004dd2fb7d7a94785e54df`, Git blob `c7252d8e4b7cd6410fab7f011aa82137af065bf1` (Boost Software License 1.0, **read only**):
https://github.com/FirebirdSQL/firebird/blob/f78dbc4e500e8896a4004dd2fb7d7a94785e54df/extern/libcds/cds/container/impl/michael_kvlist.h

**Observed API constraints** (read exact vendor code, not invented capabilities):
- `MichaelKVList::erase(key)` delegates to `erase_at(head(),key,intrusive_key_comparator())`. It is keyed deletion; it does not check `mapped_type` (here `BufferDesc*`) as a precondition.
- `erase_with(key,Less)` changes the **key-order search comparator**. Its documentation requires `Less` to preserve the same ordering used to construct the list. Replacing that comparator with a pointer-identity predicate would break the ordered-list contract and may introduce harder concurrency defects.
- `erase(key, Func)` calls a callback for the found element **as it deletes it**; this is not a documented conditional veto. Printing/asserting the descriptor in the callback does not prevent deleting the wrong key association.
- `extract(key)` also unlinks the key before yielding a guarded pointer; post-extraction equality checking is not an atomic compare-before-erase.

**Negative gate:** do not merge any proposed `erase_with`/callback-based key+descriptor hotfix absent a verified, atomic, value-conditional removal primitive or independently proven synchronization mechanism for DHP/hazard pointers. This is a **constraint on proposed fixes**, not proof that the existing key-only erase caused #9269. The exact concurrency interleaving and version-specific behavior remain `TOKEN_VAZIO`.

### Minimal evidence demanded for future H2 engine patch

Instrument only a disposable TEST build, disabled by default: `page-key`, `BufferDesc` identity, generation if available, hash slot transition, writer suspension state and thread/synchronization order. Avoid collecting page contents or user data. Show a deterministic interleaving that violates `hash_entry(page).descriptor.page==page`, then an independently checked non-regression trace under concurrent read/insert/eviction and memory-reclamation tests. Run both CDS and non-CDS code paths, Windows and a second platform, with sanitizers where supported. Without that: `IMPLEMENTED_UNTESTED` at most, `claim_allowed=false`.

Source-level finding `PASS_SOURCE_REVIEW_SCOPED`; integrated Firebird build, libcds concurrency test, Windows #9269 fault replay all `NOT_RUN`.
