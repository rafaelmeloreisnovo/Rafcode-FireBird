/* SPDX-License-Identifier: MIT -- Linux x86-64 exit syscall port. */
void raf_linux_exit(unsigned long code) __attribute__((noreturn));
void raf_linux_exit(unsigned long code)
{
    __asm__ __volatile__("mov $60, %%rax\n\tsyscall" : : "D"(code) : "rax", "rcx", "r11", "memory");
    for (;;) { }
}
