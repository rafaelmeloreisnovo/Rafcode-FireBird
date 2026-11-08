# Separate licenses / ownership boundary

| Path | Work | License or authority |
| --- | --- | --- |
| `NUCLEOS/include`, `NUCLEOS/src`, `NUCLEOS/tests` | Original and explicitly imported RAFAELIA C code | MIT: [NUCLEOS/LICENSE](../NUCLEOS/LICENSE) |
| `audit/`, `scripts/` | Original hosted verification tooling | MIT: [audit/LICENSE](../audit/LICENSE) |
| `README.md`, `AGENTS.md`, `CURRENT_STATE.md`, `001_PONTEIRO/`, `docs/`, `controls/` | Original documentation and informative mapping | CC BY 4.0: [docs/LICENSE.md](../docs/LICENSE.md) |
| Firebird engine in **another repo**, including IPL/IDPL source and dependencies | Third party upstream | **Not relicensed by this repository** |
| NIST standards / original publication texts | External government/public sources | External publisher terms; linked, **not copied** |
| Brands, trade names, logos, private telemetry or customer datasets | Separate rights | Not licensed here |

License statements cover only the original material where the respective authors/contributors possess rights. Preserve attribution, original notices, and exact source commit. Any future copy of third-party code must be reviewed before a license assertion. MIT is permissive but does not certify originality, security, patent status, compliance or suitability.

For specific legal and provenance falsifiers, see [AUTHORIAL_FIREBIRD_BOUNDARY.md](AUTHORIAL_FIREBIRD_BOUNDARY.md). The existence of more than one license scope does not put upstream Firebird code under MIT or make the entire repository dual-licensed.

## Additive G0c scope

NUCLEOS/ports/linux/*.c and scripts/check-*.sh contain original MIT implementation code where authors hold rights; NUCLEOS/LICENSE and audit/LICENSE govern as applicable. docs/PROCEDURAL_ASSURANCE_V1.md and NUCLEOS/ports/linux/README.md are authored prose under CC BY 4.0, excluding third-party normative terms. This does not alter upstream Firebird IPL/IDPL or replace original notices.
