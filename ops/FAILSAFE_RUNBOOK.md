# SOP-001 — Opt-in observer and fail-safe runbook

**Scope:** reviewed standalone observer policy, *not* Firebird failover. Current runtime adapter is `NOT_IMPLEMENTED`; so commands below propose or test only, cannot toggle a live Firebird service.

## Before any action (PRE)
- Confirm repository exact SHA, [CURRENT_STATE](../CURRENT_STATE.md), pinned sources and owner/role.
- Use a synthetic test environment, no service credentials or client dataset. Explicit operator consent is required for future runtime binding.
- Confirm default policy `enabled=false`; no syslog transport, no database connection.
- If missing source, owner, test or data protection rule: `ROUTE_STATE=BLOCKED`; `TOKEN_VAZIO`.

## Offline quick commands
```sh
python3 -m federation.control status
python3 -m federation.control plan-enable
python3 -m federation.control plan-disable
sh scripts/check.sh
```
Output is **proposal-only**, no files modified, no system activity started. The C API `raf_fed_stage` prepares a revision, `raf_fed_commit(ctx,1)` requires caller acknowledgment, `raf_fed_disable` stops observer output, and `raf_fed_failback(ctx,1)` restores one previous policy in memory. They do **not** implement a persistent switch or concurrency-safe hot swap.

## Safety/fallback matrix
| Condition | Allowed behavior | Forbidden |
| --- | --- | --- |
| No adapter / disabled | no output | infer service is running |
| New revision valid | stage only | activate without acknowledgment |
| UNKNOWN clock/progress/IO | no autonomous action | panic recovery or claim deadlock |
| STALLED/IO_ERROR verified | ALERT preview | restart/kick transaction |
| Syslog formatting overflow | return zero/no transmission | truncate identifying data |
| Audit storage full | preserve gap / bounded telemetry loss | block Firebird write path |
| Operator disable | observer NONE immediately | mutate DB state |
| Repeated revision or bad schema | reject, preserve active | downgrade/rollback silently |

## Reversal and failback
- **Observer local:** `raf_fed_disable` (synchronous local object) / `plan-disable` (preview CLI). To failback config, operator acknowledges previously staged policy; cannot roll back source code or a DB transaction this way.
- **Git:** revert dedicated feature commits or close DRAFT PR; readback base/main unchanged. Do not destroy original history.
- **Firebird:** follow vendor-specific recovery procedure in a separately approved environment; this SOP is NOT authority to restart, restore, switch primary, drop data, or alter network configuration.

## Acceptance, exit and receipt
Exit only after exact-head build + adversarial checks, privacy review, independent evidence and rollback test. Otherwise `IMPLEMENTED_UNTESTED` or `PASS_SCOPED` and `claim_allowed=false`. Receipt: base, head, actor role, action, data classification, test commands, exit codes, result, gaps, reversal.

## G1 observer extension (one-shot only)

Default command `python3 -m federation.mon_probe status` is offline. `once` cannot run without an independently prepared enabled-preview policy, `--ack`, `RAF_FB_DISPOSABLE=1`, a disposable DB connection and an installed exact-version optional Firebird driver. This is an **operator-run** snapshot, not a persistent switch. In a hung engine, snapshot timeout is plausible and must be recorded as UNKNOWN rather than a false diagnosis.

To stop: do not issue further one-shot commands; keep committed policy disabled. No Firebird data, server config, users or service touched by our implementation.
