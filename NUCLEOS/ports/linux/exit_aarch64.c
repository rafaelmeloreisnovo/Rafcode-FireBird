/* SPDX-License-Identifier: MIT -- Linux AArch64 exit syscall port. */
void raf_linux_exit(unsigned long code) __attribute__((noreturn));
void raf_linux_exit(unsigned long code)
{
    register unsigned long x0 __asm__("x0") = code;
    register unsigned long x8 __asm__("x8") = 93u;
    __asm__ __volatile__("svc #0" : "+r"(x0) : "r"(x8) : "memory");
    for (;;) { }
}
