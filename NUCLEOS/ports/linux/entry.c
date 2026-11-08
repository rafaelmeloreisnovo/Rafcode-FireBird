/* SPDX-License-Identifier: MIT -- Linux test entry, not producer core. */
#include "../../include/raf_gate.h"
extern void raf_linux_exit(unsigned long code) __attribute__((noreturn));
#if defined(__x86_64__)
__attribute__((force_align_arg_pointer))
#endif
void _start(void)
{
    raf_gate_input in = { RAF_CTRL_ALL, RAF_CTRL_ALL, RAF_CTRL_ALL, 0u, 0u };
    raf_gate_result r = raf_gate_evaluate(&in);
    if (r.state != RAF_GATE_BLOCKED || r.unknown || r.failing || r.pending)
        raf_linux_exit(11u);
    in.anchor_verified = 1u;
    r = raf_gate_evaluate(&in);
    if (r.state != RAF_GATE_REVIEW_REQUIRED || r.unknown || r.failing || r.pending)
        raf_linux_exit(12u);
    in.known &= ~RAF_CTRL_PRIVACY;
    in.passed &= ~RAF_CTRL_PRIVACY;
    r = raf_gate_evaluate(&in);
    if (r.state != RAF_GATE_BLOCKED || r.unknown != RAF_CTRL_PRIVACY)
        raf_linux_exit(13u);
    raf_linux_exit(0u);
}
