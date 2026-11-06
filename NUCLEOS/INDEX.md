# NUCLEOS — contracts / evidence states

| Component | Role | Implementation |
| --- | --- | --- |
| `include/raf_guard.h` + `src/raf_guard.c` | Deterministic progress/IO observer + bounded cadence | Implemented; separately sourced (see PROVENANCE) |
| `include/raf_gate.h` + `src/raf_gate.c` | Typed evidence gate that **cannot** authorize claims | Implemented; locally tested; remote CI unverified |
| `tests/test_guard.c` + `tests/test_gate.c` | Synthetic adversarial falsifiers | Provided; local execution has separate verification context |
| `include/raf_federation.h` + `src/raf_federation.c` | Opt-in in-memory stage / switch / disable / failback | PASS_SCOPED_CI at source commit a708a0add36b46cd38defff01a64d510039159d5 |
| `include/raf_syslog.h` + `src/raf_syslog.c` | Sanitized RFC5424-shaped **preview**, no transport | PASS_SCOPED_CI at source commit a708a0add36b46cd38defff01a64d510039159d5 |
| `tests/test_federation.c` + `tests/test_syslog.c` | Switch replay and syslog overflow falsifiers | PROVIDED; CI result separate |
| `tests/run.sh` | Offline test runner; GCC/Clang selectable | Implemented |
| `LICENSE` | Original C components under MIT | License scoped |
| [AGENTS.md](AGENTS.md) | Strict agent and manual contributor rules | Authored |

**NOT IMPLEMENTED:** Firebird client/server adapter, log collection, OS privilege, actual CPU monitoring, data recovery, automatic remediation, cryptographic signature, independent external anchor. The test results are scoped, not an operational guarantee.

[Audit receipt verifier](../audit/README.md) is a hosted separate boundary; [NIST control crosswalk](../controls/NIST_CROSSWALK.csv) is informative, not NIST certification.
