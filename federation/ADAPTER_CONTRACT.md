
# G1 — Firebird monitoring adapter contract (implemented opt-in one-shot; no real DB test)

The G1 **optional outer adapter** is `federation/mon_probe.py`. It uses the third-party Firebird Python driver only when independently installed and exactly version `2.1.2` (PyPI 2026-10-31; see https://pypi.org/project/firebird-driver/). This is not C freestanding and is never linked into the C observer. No automatic installs, background tasks, service modification or network transport.

Actual code: one fixed SQL SELECT over `MON$DATABASE` plus `MON$IO_STATS`, fresh Firebird `TraAccessMode.READ` transaction, immediate `rollback()` and `close()`, child process supervised with deadline. No SQL text of clients, logins, DSNs, IPs, database paths, row payloads, IDs, free-form error messages or database mutations in stdout.

**Operator only, for a confirmed disposable Firebird database with independent least-privilege account** (an environment assertion cannot prove disposal):
1. Independently provision a disposable database and an observer account, inspect security policy.
2. Independently audit/install optional driver `firebird-driver==2.1.2` and system `fbclient`. Neither is installed by CI.
3. Review policy; prepare a separate copy with `enabled=true`, `sink=PREVIEW`, monotonic revision; do not edit the committed default-off policy.
4. Put `RAF_FB_DISPOSABLE=1`, `RAF_FB_DSN`, `RAF_FB_USER`, `RAF_FB_PASSWORD` in a non-public operator environment (not in a script, issue or workflow).
5. Execute a single opt-in invocation:
   ```sh
   python3 -m federation.mon_probe status
   python3 -m federation.mon_probe once --ack --policy /path/to/private-enabled-policy.json --deadline 6
   ```
6. Treat `MON_SNAPSHOT` as **only** a readable metadata snapshot. It cannot certify healthy writes. On `UNKNOWN` / `DEADLINE_EXCEEDED` / `OBSERVATION_FAILED`, stop and investigate; no automatic retries or recovery.

The parent process kills/reaps the child on timeout. This does NOT guarantee that a server-side statement has been fully cancelled immediately. The outgoing JSON has `writer_progress_known=false` and `adapter_write_statements_issued=0` as a declaration of SQL issued by adapter code, **not** proof the database was unchanged. Firebird `ON CONNECT` and `ON DISCONNECT` database-event triggers can execute their own transactions even when subsequent MON$ sampling uses a READ-only TPB. Only use a DBA-reviewed disposable database with trigger activity understood, and never claim that opening an attachment is side-effect-free.

## Non-features explicitly held

Live background monitor, syslog transport, automatic failover/failback of DB, persistent config/hot-swap, backup/restore, thread inspection, Firebird source edits and issue #9269 root-cause proof = `NOT_IMPLEMENTED/NOT_RUN`. The C observer cannot treat MON$ page counters as successful user operation progress.

## Fail-safe, rollback, falsifiers

Default policy is `enabled=false`. Invalid policy, stale source, missing ACK, missing disposable declaration, missing credentials, unrecognized driver, malformed snapshot or child timeout => **no promoted observation**; known field omission remains `null`, not zero. Rollback = stop one-shot invocation, discard private policy and stay default-off; no DB changes.

Synthetic negative tests in `federation/tests/test_mon_probe.py` inject fake clients and verify explicit read-only TPB, exactly one allowlisted SELECT, rollback/close, no credential echo, bounded child timeout, schema guards, malformed data rejection and false progress suppression. **These do not substitute Firebird live test evidence.**

Related forensic hypotheses: [FORENSICS_9269](FORENSICS_9269.md).

External authority: https://www.firebirdsql.org/file/documentation/html/en/refdocs/fblangref50/firebird-50-language-reference.html (database trigger execution semantics); source registry allowlist+40-digit SHA pins are re-validated at the parent and child gates. UNKNOWN child observation does NOT promote to OBSERVED_SCOPED.
