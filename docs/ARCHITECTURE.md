# System design: typed provenance across physical, logical and database layers

## Intent
Translate operator knowledge of physical ports, routed gateways, DNS, directory access, service protocols, database writes and recovery into **verifiable constraints**, not a claim of automated network inspection or vendor certification. Historical professional claims are `USER_REPORTED_UNVERIFIED`; no private customer data is collected here.

## Domains and trust boundaries

```text
Firebird engine / host / gateway (outside this repo; no permissions)
    -> [future reviewed read-only adapter] (NOT_IMPLEMENTED)
    -> counters/known-bit/progress + timestamp (no SQL/data/IP)
    -> NUCLEOS freestanding progress guard (OBSERVE/ALERT only)
    -> NUCLEOS freestanding evidence gate (BLOCKED/REVIEW_REQUIRED only)
    -> hosted audit verifier (offline JSONL; SHA-256; no writes)
    -> [future third-party authenticated anchor] (NOT_IMPLEMENTED)
    -> human auditor / operator-controlled recovery (external authority)
```

Separation of concerns:
- **Physical/network**: host/port/interface masks and routing policy remain controlled by operator; no packet interception or gateway configuration implemented.
- **Identity/access**: future read-only limited-scope Firebird roles; no LDAP/GPO/AD integration yet; no guessed identity.
- **Database**: Firebird Trace/MON$ integration would require a separate authorized adapter; no SQL statements executed by this project.
- **Evidence**: source, artifact, execution, evidence, claim remain distinct and linked by explicit references.
- **Privacy**: only known-bit counter values and opaque identifiers. Even counters and hashes can reveal operations; define consent, retention and sampling bounds.
- **Recovery**: engine rollback, backup restore and observer code rollback are different operations. No automatic actuation.

## MANIFOLD Ω / typed provenance

Nodes: `SOURCE`, `ARTIFACT`, `EXECUTION`, `EVIDENCE`, `CONTROL`, `CLAIM`, `RISK`, `DECISION`.
Edges: `DERIVED_FROM`, `EXECUTED_AT`, `VERIFIED_BY`, `ASSESSES`, `BLOCKED_BY`, `SUPERSEDES`.
No implicit semantic equivalence or relation inferred solely from identical labels. `TOKEN_VAZIO` is a typed gap, not `0`. Keep cardinality, source URI, commit SHA, time origin and trust domain explicit.

## Separately enforceable gates

C0: code provenance and license; C1: freestanding build + synthetic falsifiers; C2: real Firebird isolated fault reproduction; C3: privacy/secrets & data integrity; C4: externally authenticated checkpoint; C5: independent assessment and reviewed rollback. Fail closed when any required evidence is absent.

NIST references are **informative crosswalk entries**, not directly executable regulatory mandates and not certification.
