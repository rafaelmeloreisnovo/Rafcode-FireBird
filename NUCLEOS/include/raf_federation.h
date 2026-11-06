/* SPDX-License-Identifier: MIT
 * Contract RAF-FED-1.  Standalone deterministic policy switch, not Firebird failover.
 * PRE: caller owns synchronization and copies config by value, never passes secrets.
 * POST: only volatile in-memory configuration changes; never performs I/O.
 * Any OS hook, database role or live hot-swap belongs to a reviewed adapter.
 */
#ifndef RAF_FEDERATION_H
#define RAF_FEDERATION_H
#include <stdint.h>
#include "raf_guard.h"
#ifdef __cplusplus
extern "C" {
#endif
#define RAF_FED_ABI 1u
#define RAF_FED_SINK_NONE 0u
#define RAF_FED_SINK_PREVIEW 1u
#define RAF_FED_SINK_OPERATOR 2u

typedef struct raf_fed_config {
    uint32_t abi_version;
    uint32_t revision;     /* Monotonic review revision; not a DB transaction ID. */
    uint8_t enabled;       /* 0 is the safe startup value. */
    uint8_t sink;          /* PREVIEW/OPERATOR only; no transport in the kernel. */
    uint16_t reserved;     /* MUST be zero, rejects future incompatible revisions. */
} raf_fed_config;

typedef struct raf_fed {
    raf_fed_config active;
    raf_fed_config previous;
    raf_fed_config staged;
    uint32_t revision_highwater;
    uint8_t has_previous;
    uint8_t has_staged;
    uint8_t initialized;
} raf_fed;

int raf_fed_valid(const raf_fed_config* cfg);
void raf_fed_init(raf_fed* ctx);
int raf_fed_stage(raf_fed* ctx, const raf_fed_config* next);
int raf_fed_commit(raf_fed* ctx, uint8_t operator_ack);
void raf_fed_disable(raf_fed* ctx);
int raf_fed_failback(raf_fed* ctx, uint8_t operator_ack);
/* Output cannot execute Firebird actions. UNKNOWN => NONE; STALLED/IO_ERROR => ALERT. */
raf_action raf_fed_observe(const raf_fed* ctx, const raf_result* result);
#ifdef __cplusplus
}
#endif
#endif
