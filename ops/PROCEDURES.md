# SOP index / execution map for humans and AI

| SOP | Owner / authority | Read | Action | Observable acceptance | Reversal |
| --- | --- | --- | --- | --- | --- |
| 000 discover | Human/AI read-only | CURRENT_STATE, 001_PONTEIRO | resolve source and exact HEAD | no unpinned reference | TOKEN_VAZIO / block |
| 001 observer | Human operator | FAILSAFE_RUNBOOK | status/plan/stage/disable | synthetic G0 test + explicit ack | disable/failback observer only |
| 002 syslog | Human security reviewer | federation/ADAPTER_CONTRACT | static preview | bounded ASCII/unknowns safe | stop preview; no transport |
| 003 Firebird MON$ | DB owner (future) | official Firebird monitoring spec | design read-only adapter | fresh snapshots, least privilege, no SQL text | stop adapter |
| 004 failure injection | DB test owner (future) | issue #9269 and disposal plan | disposable disk-full replay | bounded, data integrity after test | destroy test environment only with owner approval |
| 005 HA | Separate authorized DBA (future) | architecture and vendor docs | failover design only | split-brain/RPO/RTO/consistency independently proven | operator-controlled disaster recovery |
| 006 evidence | Auditor | receipts + offline verifier | verify scoped SHA linkage | anchor/genuine signature explicitly evaluated | mark BLOCKED if unanchored |
| 007 change | Repo maintainer | AGENTS and release notes | PR DRAFT → review | exact-head CI, licence, readback | revert PR commit |

**Run order:** DEFINE scope → MEASURE baseline → ANALYZE negative cases → IMPROVE reversible delta → CONTROL G0/G1 → RECEIPT → INDEX. No implicit authority transference from AI to DBA, nor GitHub repo to Firebird service.

RACI: maintainer accountable for repo merge; DBA accountable for database operations; data protection owner accountable for disclosure; auditor independent for claims. If a role not identified: `TOKEN_VAZIO`, block promotion.

## Deadlines

T0 = verified handoff+test-lab availability; if unknown, T0 is `TOKEN_VAZIO`. Initial provisional dates in `../docs/ROADMAP.md` are planning targets only. Move or supersede a date by append-only release note after a verified dependency changes; never rewrite old evidence.

## Comments as part of documentation

For each code branch, inline comments must state `PRE`, `POST`, `NO_SIDE_EFFECT`, `FAIL_SAFE`, and refer to the matching test. Documented comments reduce inference but aren't independent proof; CI and observable runtime behavior outrank prose.
