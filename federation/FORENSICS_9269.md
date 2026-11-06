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
