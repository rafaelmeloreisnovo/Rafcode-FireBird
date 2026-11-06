# NUCLEOS — contracts / evidence states

| Component | Role | Implementation |
| --- | --- | --- |
| `include/raf_guard.h` + `src/raf_guard.c` | Deterministic progress/IO observer + bounded cadence | Implemented; separately sourced (see PROVENANCE) |
| `include/raf_gate.h` + `src/raf_gate.c` | Typed evidence gate that **cannot** authorize claims | Implemented; locally tested; remote CI unverified |
| `tests/test_guard.c` + `tests/test_gate.c` | Synthetic adversarial falsifiers | Provided; local execution has separate verification context |
| `tests/run.sh` | Offline test runner; GCC/Clang selectable | Implemented |
| `LICENSE` | Original C components under MIT | License scoped |
| [AGENTS.md](AGENTS.md) | Strict agent and manual contributor rules | Authored |

**NOT IMPLEMENTED:** Firebird client/server adapter, log collection, OS privilege, actual CPU monitoring, data recovery, automatic remediation, cryptographic signature, independent external anchor. The test results are scoped, not an operational guarantee.

[Audit receipt verifier](../audit/README.md) is a hosted separate boundary; [NIST control crosswalk](../controls/NIST_CROSSWALK.csv) is informative, not NIST certification.
