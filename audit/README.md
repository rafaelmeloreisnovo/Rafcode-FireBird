# Hosted audit tool — offline, read-only, no Firebird dependency

`python3 -m audit.receipt_chain path/to/synthetic.jsonl`

Strict JSONL verifier: schema and labels allowlist, canonical byte encoding for SHA-256, sequence and parent hash chain, duplicate-key rejection, false PASS rejection and truncation detection. No third-party dependencies. No network calls, file writes, collection of SQL/data or database access.

Run falsifiers: `python3 -m unittest discover -v -s audit/tests`.

**Limitations:** A valid SHA-256-linked file can be completely rewritten by an attacker who controls the file; the verifier cannot prove a signed independent checkpoint or authentic source. It is not a ledger server, a cryptographic-signature implementation or NIST attestation. Do not ingest production SQL/credentials/identifiers. Use an external approved signing/key custody architecture and independently anchored timestamps in a future separate module.

Receipt schema v1 (exact keys): `v,seq,prev,id,ts_utc,kind,source,artifact,execution,evidence,state,gap,claim_allowed,sha256`. Labels are opaque uppercase ASCII, no free-text event payload. `claim_allowed` is forced to `false` in this verifier to prevent mislabelled global claims.
