# Linux ABI port (MIT code; independently scoped)

The source files in this directory are opt-in OS entry adapters, **not part of the pure freestanding core** in NUCLEOS/src or NUCLEOS/include. Each exit_*.c contains exactly one Linux syscall, never a Firebird or Android API call. entry.c exercises positive and negative gate states without files, SQL, network or production data.

The check-linux-standalone.sh test links **static -nostdlib** x86_64, ARMv7 and AArch64 ELFs; runs the x86_64 binary on Linux and leaves ARM runtimes NOT_RUN. No APK is built. Compiler/LLD/readelf/OS are still required for building/executing this test. This is a verified ABI boundary only in its tested Linux-host scope.

An initial local x86_64 entry without a stack-alignment adjustment segfaulted; the guarded force_align_arg_pointer attribute corrected that specific local counterexample. The portable producer core was not changed. No on-device Android execution or Firebird recovery is claimed.

Source-code license: MIT. Human-authored README: CC BY 4.0 where author rights are held. Firebird upstream retains IPL/IDPL.
