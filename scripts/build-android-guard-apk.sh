#!/bin/sh
# SPDX-License-Identifier: MIT. Android test APK packaging is platform-dependent.
set -eu
cd "$(dirname "$0")/.."
if [ "$#" -ne 1 ]; then echo 'APK_GUARD=BLOCKED ABI argument' >&2; exit 2; fi
abi=$1
case "$abi" in
 armeabi-v7a) cc=armv7a-linux-androideabi23-clang; pkg=org.rafaelia.firebird.guard.armv7; title='Firebird Guard ARMv7'; machine='Machine:.*ARM' ;;
 arm64-v8a) cc=aarch64-linux-android23-clang; pkg=org.rafaelia.firebird.guard.arm64; title='Firebird Guard ARM64'; machine='Machine:.*AArch64' ;;
 *) echo 'APK_GUARD=BLOCKED unknown ABI' >&2; exit 2 ;;
esac
sdk=$ANDROID_HOME
ndk=$ANDROID_NDK_HOME
[ -d "$sdk" ] && [ -d "$ndk" ] || { echo 'APK_GUARD=BLOCKED Android toolchain not available' >&2; exit 2; }
bt="$sdk/build-tools/35.0.0"
androidjar="$sdk/platforms/android-35/android.jar"
toolchain="$ndk/toolchains/llvm/prebuilt/linux-x86_64/bin"
for item in "$bt/aapt2" "$bt/aapt" "$bt/apksigner" "$bt/zipalign" "$androidjar" "$toolchain/$cc"; do
 [ -f "$item" ] || { echo "APK_GUARD=BLOCKED missing $item" >&2; exit 2; }
done
for c in keytool readelf zip unzip sha256sum; do
 command -v "$c" >/dev/null 2>&1 || { echo "APK_GUARD=BLOCKED tool $c" >&2; exit 2; }
done
work=$(mktemp -d /tmp/raf-guard.XXXXXXXX) || exit 2
trap 'rm -rf "$work"' EXIT
trap 'exit 2' HUP INT TERM
mkdir -p "$work/lib/$abi" out/apk
sed -e "s/@PACKAGE@/$pkg/g" -e "s/@LABEL@/$title/g" android/guard/AndroidManifest.xml.in >"$work/AndroidManifest.xml"
flags='-std=c11 -O2 -ffreestanding -fno-builtin -fPIC -fvisibility=hidden -fstack-protector-strong -Wall -Wextra -Werror -pedantic'
"$toolchain/$cc" $flags -c NUCLEOS/src/raf_gate.c -o "$work/core.o"
"$toolchain/$cc" $flags -c android/guard/beta_suite.c -o "$work/beta_suite.o"
"$toolchain/$cc" $flags -c android/guard/native_activity.c -o "$work/adapter.o"
"$toolchain/$cc" -shared -Wl,--no-undefined -Wl,-z,relro,-z,now "$work/adapter.o" "$work/beta_suite.o" "$work/core.o" -landroid -o "$work/lib/$abi/librafguard.so"
readelf -h "$work/lib/$abi/librafguard.so" | grep -q "$machine" || { echo 'APK_GUARD=FAIL ELF architecture' >&2; exit 1; }
readelf -Ws "$work/lib/$abi/librafguard.so" | grep -q ANativeActivity_onCreate || { echo 'APK_GUARD=FAIL missing entry' >&2; exit 1; }
"$bt/aapt2" link --manifest "$work/AndroidManifest.xml" -I "$androidjar" --min-sdk-version 23 --target-sdk-version 28 -o "$work/base.apk"
(cd "$work" && zip -q -0 base.apk "lib/$abi/librafguard.so")
"$bt/zipalign" -f 4 "$work/base.apk" "$work/aligned.apk"
keytool -genkeypair -noprompt -alias g0d -keyalg RSA -keysize 2048 -validity 2 -storetype PKCS12 -keystore "$work/ephemeral.p12" -storepass ci-test-only -keypass ci-test-only -dname 'CN=Disposable CI Only, O=RAFAELIA, C=BR' >/dev/null 2>&1
out="out/apk/rafaelia-firebird-guard-probe-$abi.apk"
"$bt/apksigner" sign --ks "$work/ephemeral.p12" --ks-key-alias g0d --ks-pass pass:ci-test-only --key-pass pass:ci-test-only --out "$out" "$work/aligned.apk"
"$bt/apksigner" verify --verbose --min-sdk-version 23 "$out"
"$bt/zipalign" -c -v 4 "$out" >/dev/null
"$bt/aapt" dump badging "$out" | grep -F "package: name='$pkg'" >/dev/null || { echo 'APK_GUARD=FAIL package identity' >&2; exit 1; }
"$bt/aapt" dump badging "$out" | grep -F "launchable-activity: name='android.app.NativeActivity'" >/dev/null || { echo 'APK_GUARD=FAIL launcher missing' >&2; exit 1; }
unzip -Z1 "$out" | grep -Fx "lib/$abi/librafguard.so" >/dev/null || { echo 'APK_GUARD=FAIL ABI library absent' >&2; exit 1; }
if unzip -Z1 "$out" | grep -E 'classes[0-9]*[.]dex|lib/.*/lib(fbclient|firebird)[.]so' >/dev/null; then echo 'APK_GUARD=FAIL unreviewed engine or DEX' >&2; exit 1; fi
sha256sum "$out" >"out/apk/sha256-$abi.txt"
printf 'TYPE=ANDROID_NATIVE_GUARD_PROBE\nABI=%s\nPACKAGE=%s\nFIREBIRD_ENGINE=NOT_INCLUDED\nSTATIC_PACKAGE_GATE=PASS\nPHYSICAL_ANDROID=NOT_RUN\nSIGNING_KEY=CI_EPHEMERAL\n' "$abi" "$pkg" >"out/apk/receipt-$abi.txt"
echo "APK_GUARD=PASS_STATIC abi=$abi physical=NOT_RUN engine=NOT_INCLUDED"
