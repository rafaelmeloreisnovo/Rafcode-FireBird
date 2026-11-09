/* SPDX-License-Identifier: MIT.
 * Small, deterministic, freestanding C11 gate-case sequencer.
 * This is NOT a Firebird engine, SQL test or physical device receipt.
 */
#include "beta_suite.h"
#include "../../NUCLEOS/include/raf_gate.h"

static uint32_t next_seed(uint32_t *s) {
    uint32_t x = *s;
    if (!x) x = UINT32_C(0x9e3779b9);
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    *s = x;
    return x;
}

static int verify_case(uint32_t id, uint32_t *state) {
    raf_gate_input in = { RAF_CTRL_ALL, RAF_CTRL_ALL, RAF_CTRL_ALL, 0u, 0u };
    raf_gate_result r;
    uint32_t a, b, c;
    switch (id) {
    case 0u:
        return raf_gate_evaluate((const raf_gate_input *)0).state == RAF_GATE_INVALID;
    case 1u:
        in.required = 0u;
        return raf_gate_evaluate(&in).state == RAF_GATE_INVALID;
    case 2u:
        r = raf_gate_evaluate(&in);
        return r.state == RAF_GATE_BLOCKED && !r.unknown && !r.failing && !r.pending;
    case 3u:
        in.anchor_verified = 1u;
        r = raf_gate_evaluate(&in);
        return r.state == RAF_GATE_REVIEW_REQUIRED && !r.unknown && !r.failing && !r.pending;
    case 4u:
        in.known &= ~RAF_CTRL_PRIVACY;
        in.passed &= ~RAF_CTRL_PRIVACY;
        in.anchor_verified = 1u;
        r = raf_gate_evaluate(&in);
        return r.state == RAF_GATE_BLOCKED && r.unknown == RAF_CTRL_PRIVACY;
    case 5u:
        in.passed &= ~RAF_CTRL_PRIVACY;
        in.failed = RAF_CTRL_PRIVACY;
        in.anchor_verified = 1u;
        r = raf_gate_evaluate(&in);
        return r.state == RAF_GATE_BLOCKED && r.failing == RAF_CTRL_PRIVACY;
    default:
        a = next_seed(state);
        b = next_seed(state);
        c = next_seed(state);
        in.known = a & RAF_CTRL_ALL;
        in.passed = in.known & b;
        in.failed = in.known & ~in.passed & c;
        in.anchor_verified = (uint8_t)(next_seed(state) & 1u);
        r = raf_gate_evaluate(&in);
        if (r.state == RAF_GATE_INVALID) return 0;
        if (r.unknown != (in.required & ~in.known)) return 0;
        if (r.failing != (in.required & in.failed)) return 0;
        if (r.pending != (in.required & in.known & ~(in.passed | in.failed))) return 0;
        return r.state == ((r.unknown || r.failing || r.pending || !in.anchor_verified)
            ? RAF_GATE_BLOCKED : RAF_GATE_REVIEW_REQUIRED);
    }
}
void raf_beta_run(raf_beta_report *report, uint32_t seed) {
    uint32_t i, state = seed;
    if (!report) return;
    report->seed = seed;
    report->count = RAF_BETA_MAX_CASES;
    report->passed = 0u;
    report->failed = 0u;
    for (i = 0u; i < RAF_BETA_MAX_CASES; ++i) {
        int pass = verify_case(i, &state);
        report->cases[i].pass = (uint8_t)(pass ? 1u : 0u);
        report->cases[i].route = i;
        report->passed += (uint32_t)(pass ? 1u : 0u);
        report->failed += (uint32_t)(pass ? 0u : 1u);
    }
}
