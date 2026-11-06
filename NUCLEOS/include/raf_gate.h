/* SPDX-License-Identifier: MIT
 * RAFAELIA: freestanding evidence-gate core. Never authorizes a claim/recovery.
 */
#ifndef RAF_GATE_H
#define RAF_GATE_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
#define RAF_CTRL_SOURCE       UINT32_C(0x01)
#define RAF_CTRL_ARTIFACT     UINT32_C(0x02)
#define RAF_CTRL_EXECUTION    UINT32_C(0x04)
#define RAF_CTRL_EVIDENCE     UINT32_C(0x08)
#define RAF_CTRL_INTEGRITY    UINT32_C(0x10)
#define RAF_CTRL_PRIVACY      UINT32_C(0x20)
#define RAF_CTRL_INDEPENDENT  UINT32_C(0x40)
#define RAF_CTRL_ALL          UINT32_C(0x7f)
typedef struct raf_gate_input {
    uint32_t required;  /* Required gate bit set, nonempty */
    uint32_t known;     /* Controls with actual observed evidence */
    uint32_t passed;    /* Subset of known, must exclude failed */
    uint32_t failed;    /* Subset of known, must exclude passed */
    uint8_t anchor_verified; /* External anchor verified by trusted caller */
} raf_gate_input;
typedef enum raf_gate_state {
    RAF_GATE_INVALID = 0,
    RAF_GATE_BLOCKED = 1,
    RAF_GATE_REVIEW_REQUIRED = 2 /* NOT approved: human/provider review still required */
} raf_gate_state;
typedef struct raf_gate_result {
    uint32_t unknown;
    uint32_t failing;
    uint32_t pending;
    raf_gate_state state;
} raf_gate_result;
raf_gate_result raf_gate_evaluate(const raf_gate_input* input);
#ifdef __cplusplus
}
#endif
#endif
