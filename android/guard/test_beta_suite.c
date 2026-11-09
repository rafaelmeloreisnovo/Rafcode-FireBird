/* SPDX-License-Identifier: MIT. Hosted falsifiers for the C11 pure test runner. */
#include "beta_suite.h"
#include <stdio.h>
#include <stdint.h>
int main(void) {
    static const uint32_t seeds[] = {
        0u, 1u, UINT32_C(0x12345678), UINT32_C(0xffffffff), UINT32_C(0x80000000)
    };
    uint32_t i, j;
    raf_beta_report r;
    raf_beta_run((raf_beta_report*)0, 1u);
    for(i=0u;i<5u;i++) {
        raf_beta_run(&r,seeds[i]);
        if(r.seed!=seeds[i] || r.count!=RAF_BETA_MAX_CASES ||
           r.passed!=RAF_BETA_MAX_CASES || r.failed!=0u) {
            (void)fprintf(stderr,"BETA_FAIL seed=%u pass=%u fail=%u\n",
                          seeds[i],r.passed,r.failed);
            return 1;
        }
        for(j=0u;j<r.count;j++) {
            if(r.cases[j].route!=j || r.cases[j].pass!=1u) return 2;
        }
    }
    (void)puts("BETA_SUITE=PASS_SCOPED seeds=5 cases=120 physical=NOT_RUN engine=NOT_RUN");
    return 0;
}
