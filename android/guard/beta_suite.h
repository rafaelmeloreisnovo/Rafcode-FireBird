/* SPDX-License-Identifier: MIT. Bounded pure C11 test battery, no I/O. */
#ifndef RAF_BETA_SUITE_H
#define RAF_BETA_SUITE_H
#include <stdint.h>
#define RAF_BETA_MAX_CASES 24u
typedef struct raf_beta_case {
    uint8_t pass;
    uint32_t route;
} raf_beta_case;
typedef struct raf_beta_report {
    uint32_t seed;
    uint32_t count;
    uint32_t passed;
    uint32_t failed;
    raf_beta_case cases[RAF_BETA_MAX_CASES];
} raf_beta_report;
void raf_beta_run(raf_beta_report *report, uint32_t seed);
#endif
