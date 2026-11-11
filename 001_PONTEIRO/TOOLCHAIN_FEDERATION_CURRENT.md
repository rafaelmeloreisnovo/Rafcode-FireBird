# 001_PONTEIRO — Firebird toolchain federation current route

Intent: AAR/APK evidence integrity without relaxing freestanding core constraints.
Producer: `rafaelmeloreisnovo/Rafcode-FireBird`, base `main@c1148850b4d3e494ad7d137e62c825283cc5dc37`.
Working branch: `rafcode/firebird-aar-apk-evidence-gate-20261110` (isolated, no merge authorization).
Status: `IMPLEMENTED_UNTESTED` until exact checkout + CI results read back.
Map: [docs/TOOLCHAIN_FEDERATION_FIREBIRD_V1.md](../docs/TOOLCHAIN_FEDERATION_FIREBIRD_V1.md).
Gate: [scripts/firebird_consumer_scope_gate.py](../scripts/firebird_consumer_scope_gate.py).
Adversarial fixtures: [audit/tests/test_firebird_consumer_scope_gate.py](../audit/tests/test_firebird_consumer_scope_gate.py).
CI producer: [.github/workflows/build-firebird-aar-consumer-apk.yml](../.github/workflows/build-firebird-aar-consumer-apk.yml).
Historical state: [CURRENT_STATE.md](../CURRENT_STATE.md), not automatically promoted.
Distinction: GitHub code = producer; Drive = ledger/index; Supabase = scoped events; alphaXiv/Undermind = scientific prior art, not CI proof.
PIRC-2: Source N0 (connector read); new CI status N5 until execution; actual Android/SQL N5; `claim_allowed=false`.
Rollback: close draft branch PR; retain receipts and predecessor; no engine fork, prod data or main direct mutation.
