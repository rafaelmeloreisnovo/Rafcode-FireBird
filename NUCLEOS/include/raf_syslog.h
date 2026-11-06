/* SPDX-License-Identifier: MIT
 * RFC5424-shaped, ASCII-only syslog preview. NO syslog transport or OS I/O.
 */
#ifndef RAF_SYSLOG_H
#define RAF_SYSLOG_H
#include <stddef.h>
#include <stdint.h>
#include "raf_guard.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Returns length excluding NUL, or 0 when invalid/insufficient capacity.
 * Uses '-' for unknown time/host, no structured data, no SQL/client payload.
 * The caller decides whether and how to transmit, subject to privacy review.
 */
size_t raf_syslog_preview(const raf_result* result, char* output, size_t capacity);
#ifdef __cplusplus
}
#endif
#endif
