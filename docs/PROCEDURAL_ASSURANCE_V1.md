# G0c — operational quality and assurance (source-mapped, not certified)

Scope: original C11 guard/evidence gate and isolated Linux exit adapter only. No Firebird engine, Android APK or production DB. Standards are *sources of methods*, not a claim of certification or a reproduction of paid normative texts.

| Source | Procedure applied | Acceptance / remaining gap |
|---|---|---|
| ISO 8000-61:2016 (https://www.iso.org/standard/63086.html) | Specify data provenance, completeness, typed unknowns, exact commit and supersession | SHA+paths+test+status+receipt; quality capability maturity NOT_ASSESSED |
| ISO/IEC 27001:2022 and 27002:2022 (https://www.iso.org/standard/27001 and https://www.iso.org/standard/75652.html) | Asset/risk/threat boundary, least privilege, no secrets, fail-closed review | Offline, read-only CI; organizational ISMS NOT_ASSESSED |
| ISO 27500:2016 (https://www.iso.org/standard/64239.html) | Human-centered review, route navigation, operator retention of authority | DRAFT/HOLD, no automatic recovery; organizational adoption NOT_ASSESSED |
| IEEE 1012-2024 (https://standards.ieee.org/ieee/1012/7324/) | Separate artifact verification from intended-use validation; use positive and negative fixtures | Cross-link != on-device validation; physical ARM NOT_RUN |
| W3C PROV-O (https://www.w3.org/TR/prov-o/) | Typed source -> artifact -> execution -> evidence -> claim and correction relation | SHA-linked textual records; RDF/OWL serialization NOT_IMPLEMENTED |
| BCP14: RFC2119/8174 (https://www.rfc-editor.org/rfc/rfc8174) | Express project-local MUST/MUST NOT assertions unambiguously | Wrong ELF, external symbol or syscall in core MUST fail |
| RFC 8785 (https://www.rfc-editor.org/rfc/rfc8785) | Require canonical JSON before future cryptographic-signature claims | JCS and externally signed evidence NOT_IMPLEMENTED |
| NIST SP 800-53 Rev 5 + 53A Rev 5 (https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final ; https://csrc.nist.gov/pubs/sp/800/53/a/r5/final) | Map risk/control objective -> inspection -> observed evidence -> assessed outcome | G0c scoped checks; NOT a NIST audit or certification |

## 6Σ / DMAIC execution (without a statistical Six Sigma claim)

**Define** critical-to-quality properties: correct ELF machine, zero unresolved external runtime symbols, no direct syscall in core, no automatic approval, isolated Linux entry with no libc. **Measure** SHA, compiler/triple, ELF header, symbols, instruction disassembly, exit status and test counts. **Analyze** disposable adversarial fixtures: expected success object; unwanted external call; direct syscall; wrong architecture. Missing tools and a falsely accepted negative both BLOCK. **Improve** independent, reversible modules only; keep Firebird and original core untouched. **Control** reviewed PR, exact-head CI logs, no binary uploads, typed gaps, rollback and append-only receipt.

## Evidence boundary / prevention of false claims

- Local first attempt for Linux x86_64 C entry caused a segmentation fault due to kernel-entry stack alignment; a narrowly x86_64 guarded attribute corrected the local failure. That correction does not prove ARM execution.
- The Linux port intentionally invokes OS sys_exit. Core objects remain syscall-free in the measured scope. -ffreestanding and -nostdlib do NOT remove the need for compiler/linker/OS/CPU ABI.
- G0c requires new CI evidence at new HEAD, not earlier G0b PASS. Physical Motorola ARMv7 and AArch64, Android E2E, #9269, legal ownership investigation, signed external evidence remain NOT_RUN / TOKEN_VAZIO.
- claim_allowed=false; merge_allowed=false. Rollback: revert proposed additive commit or close DRAFT PR, preserve main and production data.
- Receipt contract: μID | time | source/ref | base/head SHA | paths | commands | positive/negative results | risk/privacy | gaps | next | rollback. Only readback can promote a claim.
