/* SPDX-License-Identifier: MIT: hosted test harness, not core. */
#include "../include/raf_gate.h"
#include <stdio.h>
static unsigned checks;
#define T(x) do { ++checks; if (!(x)) { fprintf(stderr, "GATE_FAIL:%d: %s\n", __LINE__, #x); return 1; } } while (0)
int main(void)
{
    raf_gate_input in = { RAF_CTRL_ALL, RAF_CTRL_ALL, RAF_CTRL_ALL, 0u, 1u };
    raf_gate_result r = raf_gate_evaluate(&in);
    unsigned i;
    T(r.state == RAF_GATE_REVIEW_REQUIRED && !r.unknown && !r.failing && !r.pending);
    in.anchor_verified = 0u;
    T(raf_gate_evaluate(&in).state == RAF_GATE_BLOCKED);
    in.anchor_verified = 1u;
    for (i = 0; i < 7u; ++i) {
        const uint32_t bit = UINT32_C(1) << i;
        in.known = RAF_CTRL_ALL & ~bit;
        in.passed = in.known;
        in.failed = 0u;
        r = raf_gate_evaluate(&in);
        T(r.state == RAF_GATE_BLOCKED && r.unknown == bit);
        in.known = RAF_CTRL_ALL;
        in.passed = RAF_CTRL_ALL & ~bit;
        in.failed = bit;
        r = raf_gate_evaluate(&in);
        T(r.state == RAF_GATE_BLOCKED && r.failing == bit);
        in.failed = 0u;
        r = raf_gate_evaluate(&in);
        T(r.state == RAF_GATE_BLOCKED && r.pending == bit);
    }
    in.required = 0u;
    T(raf_gate_evaluate(&in).state == RAF_GATE_INVALID);
    in.required = RAF_CTRL_ALL;
    in.known = 0u; in.passed = 1u; in.failed = 0u;
    T(raf_gate_evaluate(&in).state == RAF_GATE_INVALID);
    in.known = RAF_CTRL_ALL; in.passed = RAF_CTRL_ALL; in.failed = 1u;
    T(raf_gate_evaluate(&in).state == RAF_GATE_INVALID);
    in.failed = 0u; in.anchor_verified = 2u;
    T(raf_gate_evaluate(&in).state == RAF_GATE_INVALID);
    T(raf_gate_evaluate(0).state == RAF_GATE_INVALID);
    in.anchor_verified = 1u;
    for (i = 0; i < 10000u; ++i) {
        const uint32_t bit = UINT32_C(1) << (i % 7u);
        in.known = RAF_CTRL_ALL & ~bit; in.passed = in.known; in.failed = 0u;
        r = raf_gate_evaluate(&in);
        T(r.state == RAF_GATE_BLOCKED && r.unknown == bit);
    }
    printf("RAF_GATE_PASS checks=%u; samples=10000; Firebird_E2E=NOT_RUN\n", checks);
    return 0;
}
