# AGENTS — federation scoped governance

Read `../CURRENT_STATE.md`, `../AGENTS.md`, `README.md`, `ADAPTER_CONTRACT.md`, `FORENSICS_9269.md` and tests.

**Producer authority:** this repo implements standalone observer contracts only. Fork/Firebird engine code is owned by its respective repository and upstream license. Do not confuse a new adapter with an upstream fix.

**Hard guard:** no mutable external Git refs, credentials in public logs/CI, raw SQL or BLOB, arbitrary sink, network or Firebird connection by default. Never self-activate. A one-shot Firebird probe may run ONLY after explicit ACK + independently prepared enabled-preview policy + disposable DB declaration + credentials in local operator environment; these are not attestation.

**Do not mutate engine:** no database writes/restart/restore/primary promotion; no syslog send, daemon, remote arbitrary source or unbounded retry. MON$ counters are not user-operation progress, and probing a hung database can itself hang; child deadline is bounded and not proof server request cleanup.

**Change gate:** every behavior change includes source SHA, falsifier, exact-head CI and scoped rollback. New field defaults to unknown. Actor verification and independently proven engine fix are still TOKEN_VAZIO. PASS_SCOPED_CI can apply only to synthetic tests until actual disposable DB runs.

Refer to [ops procedures](../ops/PROCEDURES.md), [release notes](../ops/RELEASE_NOTES.md), original MIT/LICENSE boundaries, upstream Firebird license and ISO 8000 informative quality references; never claim certification.
