# Separate Android smoke APKs — RAFAELIA Guard, NOT Firebird DB

Source: this repo's original MIT C11 evidence-gate and independent Android UI adapter. The two output APKs have different package IDs and architectures:

- ARMv7 (Motorola E7 Power candidate): `rafaelia-firebird-guard-probe-armeabi-v7a.apk`.
- AArch64: `rafaelia-firebird-guard-probe-arm64-v8a.apk`.

Core CI uses Clang -ffreestanding without Android/Java tools. APK CI uses preinstalled NDK Clang, Android SDK aapt2, zipalign and apksigner; an APK **cannot be considered SDK-free packaging**. No application Java code, JNI implementation or Gradle. Android's system NativeActivity and libandroid/bionic are platform dependencies of this UI adapter, never the original pure core.

The display is a minimal color bar probe, green if the guard semantics self-test passes, red otherwise. This is not a user-ready diagnostics interface, Firebird client, Firebird server, actual SQL engine or monitoring connection. No Firebird engine files, credentials, SQL, network calls, storage or service restart.

CI uses an ephemeral key regenerated every run; install/upgrade identity is not stable across runs. Artifact verification checks signatures, ELF architectures, launcher, package IDs, single ABI native library and SHA256. A successful APK static check != installation/launch proof on Motorola; physical runtime NOT_RUN.

The upstream engine is separately licensed IPL/IDPL and resides in rafaelmeloreisnovo/firebird_rafcodephi. Its current Android project declares com.android.library and emits an AAR, NOT an installable Firebird APK. No upstream engine has been repackaged here. claim_allowed=false; merge_allowed=false.
