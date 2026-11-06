/* SPDX-License-Identifier: MIT
 * SAFE SWITCH: on boot disabled; staged config never activates by itself.
 * This is synchronous, caller-owned in-memory logic, NOT concurrent hot swap.
 */
#include "../include/raf_federation.h"

int raf_fed_valid(const raf_fed_config* c)
{
    if (!c || c->abi_version != RAF_FED_ABI || c->revision == 0 ||
        c->enabled > 1u || c->reserved ||
        c->sink > RAF_FED_SINK_OPERATOR) return 0;
    if (!c->enabled) return c->sink == RAF_FED_SINK_NONE;
    return c->sink == RAF_FED_SINK_PREVIEW || c->sink == RAF_FED_SINK_OPERATOR;
}

void raf_fed_init(raf_fed* c)
{
    if (!c) return;
    c->active.abi_version = RAF_FED_ABI;
    c->active.revision = 0;
    c->active.enabled = 0;
    c->active.sink = RAF_FED_SINK_NONE;
    c->active.reserved = 0;
    c->previous = c->active;
    c->staged = c->active;
    c->revision_highwater = 0;
    c->has_previous = 0;
    c->has_staged = 0;
    c->initialized = 1;
}

int raf_fed_stage(raf_fed* c, const raf_fed_config* next)
{
    if (!c || !c->initialized) return 0;
    /* Revoke a previously staged candidate on any attempted new stage. */
    c->has_staged = 0;
    if (!raf_fed_valid(next) || next->revision <= c->revision_highwater)
        return 0;
    c->staged = *next;
    c->has_staged = 1;
    return 1;
}

int raf_fed_commit(raf_fed* c, uint8_t ack)
{
    if (!c || !c->initialized || ack != 1u || !c->has_staged ||
        !raf_fed_valid(&c->staged) || c->staged.revision <= c->revision_highwater)
        return 0;
    c->previous = c->active;  /* exactly one failback slot */
    c->has_previous = 1;
    c->active = c->staged;
    c->revision_highwater = c->active.revision;
    c->has_staged = 0;
    return 1;
}

void raf_fed_disable(raf_fed* c)
{
    if (!c || !c->initialized) return;
    /* Emergency kill switch: never changes the database or any external sink. */
    c->active.enabled = 0;
    c->active.sink = RAF_FED_SINK_NONE;
    c->has_staged = 0;
}

int raf_fed_failback(raf_fed* c, uint8_t ack)
{
    if (!c || !c->initialized || ack != 1u || !c->has_previous ||
        c->has_staged) return 0;
    /* Explicit operator approved revert of observer configuration ONLY. */
    c->active = c->previous;
    c->has_previous = 0;
    /* Do not decrease revision_highwater: old epochs cannot be replayed. */
    return 1;
}

raf_action raf_fed_observe(const raf_fed* c, const raf_result* r)
{
    if (!c || !c->initialized || !c->active.enabled || !r ||
        r->state > RAF_IO_ERROR || r->action > RAF_ALERT)
        return RAF_NONE;
    if (r->state == RAF_UNKNOWN)
        return RAF_NONE;
    if (r->state == RAF_IO_ERROR || r->state == RAF_STALLED)
        return RAF_ALERT;
    return RAF_OBSERVE;
}
