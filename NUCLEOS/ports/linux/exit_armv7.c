/* SPDX-License-Identifier: MIT -- Linux ARM EABI exit syscall port. */
void raf_linux_exit(unsigned long code) __attribute__((noreturn));
void raf_linux_exit(unsigned long code)
{
    register unsigned long r0 __asm__("r0") = code;
    register unsigned long r7 __asm__("r7") = 1u;
    __asm__ __volatile__("svc #0" : "+r"(r0) : "r"(r7) : "memory");
    for (;;) { }
}
