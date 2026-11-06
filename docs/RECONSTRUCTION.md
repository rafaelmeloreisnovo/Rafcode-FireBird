# Reconstructible operating memory: humans and AI, minimal friction

Read order:
1. [START_HERE](../001_PONTEIRO/START_HERE.md) → [CURRENT_STATE](../CURRENT_STATE.md).
2. [AGENTS](../AGENTS.md) → [federation/README](../federation/README.md) → [SOP](../ops/PROCEDURES.md).
3. Select exactly one producer source SHA; separate issue, code, test command, receipt, and claim.
4. Execute offline `sh scripts/check.sh`; if unavailable, record NOT_RUN rather than inference.
5. Compare HEAD with its parent, check licence and C ABI; use `ops/FAILSAFE_RUNBOOK.md` for reversal.
6. Append small evidence delta, link parent and superseded state, and re-index CURRENT_STATE if material.

Typed graph nodes: source, policy, adapter, signal, decision, test, receipt, claim, risk; edges: derived_from, validated_by, supersedes, blocked_by, observed_at. An edge does not become true by an AI-generated analogy. Evidence is bounded by trust domain: synthetic/local CI ≠ live Firebird.

No customer datasets, raw SQL/Trace or secrets belong in public knowledge. Historic experiences and institutional memory are hypotheses/provenance until independently verified. Comments are close to code and part of maintainability; tests and runtime traces remain the falsifiers.

For releases: record `release_id | exact_sha | parent | files | ABI/schema | backward compatibility | command | environment | elapsed | test_result | privacy | rollback | known_gap | independent_review`. If any critical field is missing, promotion BLOCKED. No fixed deadline is evidence of completion.
