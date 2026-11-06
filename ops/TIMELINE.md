# Timeline (append-only narrative; source vs claim separated)

| Date | Event | Evidence | State |
| --- | --- | --- | --- |
| 2026-11-06 | New independent Rafcode-FireBird producer repo initialized | Git commit `b4f7d8601203dbc2426a6db49db92bee40fc3077` | OBSERVED |
| 2026-11-06 | First scoped C watchdog/evidence gate and audit JSONL verification | PR #1 (DRAFT/HOLD) / GitHub Actions run 42166276154 | PASS_SCOPED_CI |
| 2026-11-06 | Federation observer source pin, policy switch and syslog preview added to separate feature branch | New code branch, exact HEAD to be logged after testing | IMPLEMENTED_UNTESTED |
| 2026-11-09 | Planned F0 checkpoint, conditional on tests | Date proposed, not a task executing later | PLANNED |
| 2026-11-11 | Planned F1 read-only adapter design | No adapter executed | PLANNED |
| 2026-11-13 | Planned F2 #9269 reproduction in disposable environment | Lab/fixture not established | BLOCKED |
| TBD | F3/F4 TLS syslog / actual HA | Independent review required | TOKEN_VAZIO |

Use `supersedes: event-id` for later correction; do not erase prior rows. Exact GitHub Actions run, tests and compiler labels must be appended from actual readback, never guessed.

| 2026-11-06 | Federation synthetic gate G0 exact code HEAD `a708a0add36b46cd38defff01a64d510039159d5` | [Actions 42168907060](https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42168907060); job 127731849705 | PASS_SCOPED_CI |

| 2026-11-06 | G1 candidate: optional supervised read-only MON$ one-shot implementation plus Firebird #9269 H1/H2 source model | New scoped branch source; exact-head CI pending | IMPLEMENTED_UNTESTED |

| 2026-11-06 | G1 test fixture root initially failed in run 42171784931; one-line fix in 679ea684; hardening fix to suppress false UNKNOWN promotion at `9438726c2a5a868e65957aa937e967f7e3a1967d` | [CI 42172109238](https://github.com/rafaelmeloreisnovo/Rafcode-FireBird/actions/runs/42172109238) | PASS_SCOPED_CI (37 federation Python + 17 audit, GCC/Clang) |

| 2026-11-06 06:16 UTC | Independent Firebird 4.0.5 embedded temporary DB, fixed MON$ query, read-only insert falsifier rejected and post-check COUNT=0 | `receipts/2026-11-06-FB4-disposable-mon-sql.json` Git blob `c72660bfbaa86c4ee87d8ffd8c37b9109f11d671`; executable blob `b499384ca8a4daf693386d6d4659386d05acfd8b` | PASS_SCOPED_FIREBIRD4_SQL; G1 Python adapter and #9269 still NOT_RUN |
