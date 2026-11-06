/* SPDX-License-Identifier: MIT
 * Operator-facing syslog frame, not a network transport or authenticated log.
 * PRIVACY: enum/sequence only. No free-form untrusted message interpolation.
 */
#include "../include/raf_syslog.h"

static int append(char* out, size_t cap, size_t* at, const char* s)
{
    while (*s) {
        if (*at + 1u >= cap) return 0;
        out[*at] = *s;
        ++*at;
        ++s;
    }
    out[*at] = '\0';
    return 1;
}
static int decimal(char* out, size_t cap, size_t* at, uint64_t n)
{
    char rev[20];
    unsigned i = 0u;
    do {
        rev[i++] = (char) ('0' + (n % UINT64_C(10)));
        n /= UINT64_C(10);
    } while (n);
    while (i) {
        if (*at + 1u >= cap) return 0;
        out[(*at)++] = rev[--i];
    }
    out[*at] = '\0';
    return 1;
}
size_t raf_syslog_preview(const raf_result* r, char* out, size_t cap)
{
    size_t at = 0;
    if (!out || !cap) return 0;
    out[0] = '\0';
    if (!r || r->state > RAF_IO_ERROR || r->action > RAF_ALERT ||
        r->reason > RAF_REASON_SEQ_EXHAUSTED) return 0;
    /* RFC 5424: local0 informational=134, local0 error=131.
     * '-' is NILVALUE for timestamp, hostname, procid, structured-data.
     * MSG is bounded ASCII derived solely from known enum/numeric fields.
     */
    if (!append(out,cap,&at,r->action == RAF_ALERT
        ? "<131>1 - - Rafcode - RAFSTATE - "
        : "<134>1 - - Rafcode - RAFSTATE - ") ||
        !append(out,cap,&at,"state=") ||
        !decimal(out,cap,&at,(uint64_t)r->state) ||
        !append(out,cap,&at," action=") ||
        !decimal(out,cap,&at,(uint64_t)r->action) ||
        !append(out,cap,&at," reason=") ||
        !decimal(out,cap,&at,(uint64_t)r->reason) ||
        !append(out,cap,&at," seq=") ||
        !decimal(out,cap,&at,r->sequence)) {
        out[0] = '\0';
        return 0;
    }
    return at;
}
