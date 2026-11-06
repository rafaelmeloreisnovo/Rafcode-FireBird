/* SPDX-License-Identifier: MIT */
#include "../include/raf_syslog.h"
#include <stdio.h>
static unsigned checks;
#define CHECK(x) do { ++checks; if(!(x)){fprintf(stderr,"SYSLOG_FAIL:%d: %s\n",__LINE__,#x);return 1;} }while(0)
static int starts(const char*a,const char*b){while(*b){if(*a++!=*b++)return 0;}return 1;}
int main(void)
{
    char out[160];
    char tiny[2];
    raf_result alert={UINT64_MAX,1u,RAF_IO_ERROR,RAF_ALERT,RAF_REASON_IO_ERROR};
    raf_result info={0u,1u,RAF_HEALTHY,RAF_OBSERVE,RAF_REASON_PROGRESS};
    unsigned i;
    CHECK(raf_syslog_preview(&alert,out,sizeof(out))>0u);
    CHECK(starts(out,"<131>1 - - Rafcode - RAFSTATE - state=4 action=2 reason=5 seq=18446744073709551615"));
    CHECK(!raf_syslog_preview(&alert,tiny,sizeof(tiny)) && tiny[0]=='\0');
    CHECK(raf_syslog_preview(&info,out,sizeof(out))>0u);
    CHECK(starts(out,"<134>1 - - Rafcode - RAFSTATE - state=1 action=1 reason=2 seq=0"));
    CHECK(!raf_syslog_preview(0,out,sizeof(out)));
    CHECK(!raf_syslog_preview(&info,0,0u));
    info.state=(raf_state)99u;
    CHECK(!raf_syslog_preview(&info,out,sizeof(out)));
    info.state=RAF_HEALTHY;
    for(i=0;i<10000u;++i){
       info.sequence=i;
       CHECK(raf_syslog_preview(&info,out,sizeof(out))>0u);
       CHECK(starts(out,"<134>1 - - Rafcode - RAFSTATE - "));
    }
    printf("RAF_SYSLOG_PASS checks=%u previews=10000; sent_packets=0\n",checks);
    return 0;
}
