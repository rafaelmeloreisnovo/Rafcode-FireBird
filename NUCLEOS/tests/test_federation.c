/* SPDX-License-Identifier: MIT */
#include "../include/raf_federation.h"
#include <stdio.h>
static unsigned checks;
#define CHECK(x) do { ++checks; if (!(x)) { fprintf(stderr,"FED_FAIL:%d: %s\n",__LINE__,#x); return 1; } } while(0)
int main(void)
{
    raf_fed f;
    raf_fed_config on = { RAF_FED_ABI, 1u, 1u, RAF_FED_SINK_PREVIEW, 0u };
    raf_fed_config off = { RAF_FED_ABI, 2u, 0u, RAF_FED_SINK_NONE, 0u };
    raf_result healthy = { 1u, 1u, RAF_HEALTHY, RAF_OBSERVE, RAF_REASON_PROGRESS };
    raf_result stalled = { 2u, 1u, RAF_STALLED, RAF_ALERT, RAF_REASON_STALL };
    raf_result unknown = { 3u, 1u, RAF_UNKNOWN, RAF_NONE, RAF_REASON_NO_DATA };
    unsigned i;
    raf_fed_init(&f);
    CHECK(f.initialized && !f.active.enabled && !f.has_staged);
    CHECK(raf_fed_observe(&f,&stalled)==RAF_NONE);
    CHECK(!raf_fed_commit(&f,1u));
    CHECK(raf_fed_valid(&on) && raf_fed_stage(&f,&on));
    CHECK(!raf_fed_commit(&f,0u));
    CHECK(!f.active.enabled);
    CHECK(raf_fed_commit(&f,1u));
    CHECK(f.active.enabled && f.active.revision == 1u);
    CHECK(raf_fed_observe(&f,&healthy)==RAF_OBSERVE);
    CHECK(raf_fed_observe(&f,&stalled)==RAF_ALERT);
    CHECK(raf_fed_observe(&f,&unknown)==RAF_NONE);
    CHECK(!raf_fed_stage(&f,&on)); /* replay prevented */
    on.revision = 3u; on.sink = 9u;
    CHECK(!raf_fed_stage(&f,&on)); /* invalid sink revokes stage */
    CHECK(!raf_fed_commit(&f,1u));
    CHECK(raf_fed_stage(&f,&off));
    CHECK(!raf_fed_failback(&f,1u)); /* cannot failback during stage */
    CHECK(raf_fed_commit(&f,1u));
    CHECK(!f.active.enabled && f.active.revision==2u);
    CHECK(raf_fed_failback(&f,1u)); /* explicit in-memory failback */
    CHECK(f.active.enabled && f.active.revision==1u && f.revision_highwater==2u);
    CHECK(!raf_fed_failback(&f,1u));
    CHECK(!raf_fed_stage(&f,&off));
    raf_fed_disable(&f);
    CHECK(raf_fed_observe(&f,&stalled)==RAF_NONE);
    CHECK(!raf_fed_observe(&f,0));
    CHECK(!raf_fed_stage(0,&on));
    CHECK(!raf_fed_valid(0));
    for(i=3u;i<10003u;++i) {
        raf_fed_config p={RAF_FED_ABI,i,1u,RAF_FED_SINK_PREVIEW,0u};
        CHECK(raf_fed_stage(&f,&p));
        CHECK(!raf_fed_commit(&f,2u));
        CHECK(raf_fed_commit(&f,1u));
        CHECK(raf_fed_observe(&f,&unknown)==RAF_NONE);
        raf_fed_disable(&f);
        CHECK(raf_fed_observe(&f,&stalled)==RAF_NONE);
    }
    printf("RAF_FED_PASS checks=%u cycles=10000; database_mutations=0; live_hotswap=NOT_RUN\n",checks);
    return 0;
}
