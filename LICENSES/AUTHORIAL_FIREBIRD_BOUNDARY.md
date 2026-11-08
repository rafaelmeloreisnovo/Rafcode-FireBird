# RAFAELIA / Firebird — independent authorship and official-license boundary

**Scope:** `rafaelmeloreisnovo/Rafcode-FireBird` at or after main `d761a29949c6bba921e6c408c8d5f088d9c5664a`. This document records **two distinct code licensing domains**, not a blanket dual-license or a sublicense of upstream Firebird.

| Domain / exact route | Copyright / attribution | Governing license | Can this repository change it? |
| --- | --- | --- | --- |
| `NUCLEOS/include/`, `NUCLEOS/src/`, `NUCLEOS/tests/` | Rafael Melo Reis and credited contributors, subject to file-by-file provenance | MIT (see `NUCLEOS/LICENSE`) | Only the rights holder may additionally license wholly original contributions. Prior MIT grants and contributor rights remain. |
| `audit/` and `scripts/` original code | Existing author and contributor notices | MIT (see `audit/LICENSE`) | Preserve already issued grants and notices. |
| `README.md`, `AGENTS.md`, `001_PONTEIRO/`, `CURRENT_STATE.md`, `docs/`, `controls/`, this explanatory document | Original authored text where rights are held | CC BY 4.0 (see `docs/LICENSE.md`) | This document does not relicense third-party texts. |
| `FirebirdSQL/firebird` and copied or modified upstream engine files, in the **separate fork** `firebird_rafcodephi` | Firebird/InterBase upstream contributors; precise per-file notices prevail | IPL 1.0 / IDPL 1.0, plus per-file third-party notices | **No**. Retain notices, disclose required modified sources under applicable upstream terms. |
| Future independently written ABI adapter | Ownership and code origin to be assessed per new file | **UNDECIDED** until author chooses and provenance is reviewed | **No inference** from placement or function name. |

**Authority route:** https://firebirdsql.org/en/licensing/ and https://github.com/FirebirdSQL/firebird. Firebird's published quick-start guide describes IPL/IDPL for engine files and independently licensed larger works; the binding texts and file notices control any distribution. These are reference links, not code copied from upstream.

## Gate before claiming authorial separation

1. Verify `path | original author/notice | source repository | commit | blob SHA | changes | applicable license`. Reused `raf_guard` has explicit recorded import lineage in `PROVENANCE.md`; an import is not a new invention.
2. If a file derives from Firebird, keep the applicable IPL/IDPL obligations even after an extensive rewrite. Newly written independent modules may have their own terms where legally supported.
3. For an **additional custom RAFCODE-Φ license**, provide the *actual license terms*, copyright owners and contributor authorization first. No bespoke license is silently invented, and previously granted MIT rights are not revoked.
4. No trademarks, patent, third-party contribution, customer data or rights under the Berne Convention are automatically assigned or certified by this manifest.

**Falsifiers:** discover a copied upstream source in a purported MIT-only file; find missing notices; trace a public symbol to upstream implementation; find a new contributor with incompatible rights. Any hit -> `LICENSE_SCOPE=BLOCKED` and a corrective, traceable revision.

**Claim:** authorial scope is proposed/documented; universal clean-room independence is **NOT_VERIFIED**. No license conversion or engine code modification is performed by this change.
