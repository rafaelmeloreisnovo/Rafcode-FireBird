/* SPDX-License-Identifier: MIT */
#include "../include/raf_gate.h"
raf_gate_result raf_gate_evaluate(const raf_gate_input* in)
{
    raf_gate_result r = { 0u, 0u, 0u, RAF_GATE_INVALID };
    if (!in || !in->required || (in->required & ~RAF_CTRL_ALL) ||
        (in->known & ~RAF_CTRL_ALL) || (in->passed & ~in->known) ||
        (in->failed & ~in->known) || (in->passed & in->failed) ||
        in->anchor_verified > 1u) return r;
    r.unknown = in->required & ~in->known;
    r.failing = in->required & in->failed;
    r.pending = in->required & in->known & ~(in->passed | in->failed);
    r.state = (r.unknown || r.failing || r.pending || !in->anchor_verified)
        ? RAF_GATE_BLOCKED : RAF_GATE_REVIEW_REQUIRED;
    return r;
}
