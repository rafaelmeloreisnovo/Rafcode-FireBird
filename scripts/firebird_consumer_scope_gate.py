#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Hosted, fail-closed AAR/APK evidence gate. Never a freestanding runtime or SQL test."""
import argparse
import hashlib
import io
import json
import stat
import sys
import zipfile
from pathlib import Path

MAX_ENTRY = 64 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
FIREBIRD_CLASS = "org/firebirdsql/android/embedded/FirebirdConf.class"
ELF_MACHINE = {"armeabi-v7a": 40, "arm64-v8a": 183, "x86": 3, "x86_64": 62}


class GateFailure(Exception):
    pass


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as src:
        for block in iter(lambda: src.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check_archive(archive):
    infos = archive.infolist()
    if not infos:
        raise GateFailure("EMPTY_ARCHIVE")
    seen = set()
    total = 0
    for info in infos:
        name = info.filename
        if (not name or name.startswith("/") or "\\" in name
                or any(p in ("", ".", "..") for p in name.rstrip("/").split("/"))):
            raise GateFailure("UNSAFE_ZIP_PATH")
        if name in seen:
            raise GateFailure("DUPLICATE_ZIP_PATH")
        seen.add(name)
        if stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK:
            raise GateFailure("ZIP_SYMLINK")
        if info.file_size > MAX_ENTRY:
            raise GateFailure("OVERSIZED_ENTRY")
        total += info.file_size
        if total > MAX_TOTAL:
            raise GateFailure("OVERSIZED_ARCHIVE")
    return seen


def open_checked(path):
    try:
        archive = zipfile.ZipFile(path)
        names = check_archive(archive)
        return archive, names
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        raise GateFailure("UNREADABLE_ZIP") from exc


def verify_elf(data, abi):
    if abi not in ELF_MACHINE or len(data) < 20 or data[:4] != b"\x7fELF":
        raise GateFailure("ELF_HEADER_OR_ABI_MISSING")
    width, order = data[4], data[5]
    expected_width = 2 if abi in ("arm64-v8a", "x86_64") else 1
    if width != expected_width or order not in (1, 2):
        raise GateFailure("ELF_CLASS_OR_ENDIAN_MISMATCH")
    machine = int.from_bytes(data[18:20], "little" if order == 1 else "big")
    if machine != ELF_MACHINE[abi]:
        raise GateFailure("ELF_MACHINE_ABI_MISMATCH")


def native_inventory(archive, names, root):
    found = []
    for name in sorted(names):
        if not (name.startswith(root + "/") and name.endswith(".so")):
            continue
        parts = name.split("/")
        if len(parts) != 3 or parts[1] not in ELF_MACHINE:
            raise GateFailure("UNSUPPORTED_NATIVE_LAYOUT")
        with archive.open(name) as src:
            verify_elf(src.read(20), parts[1])
        found.append(name)
    return found


def validate(aar_path, apk_path, source_sha):
    with zipfile.ZipFile(aar_path) as aar:
        aar_names = check_archive(aar)
        if "classes.jar" not in aar_names:
            raise GateFailure("AAR_CLASSES_JAR_MISSING")
        with aar.open("classes.jar") as src:
            jar_bytes = src.read(MAX_ENTRY + 1)
        if len(jar_bytes) > MAX_ENTRY:
            raise GateFailure("JAR_OVERSIZED")
        with zipfile.ZipFile(io.BytesIO(jar_bytes)) as jar:
            class_names = check_archive(jar)
            if FIREBIRD_CLASS not in class_names:
                raise GateFailure("FIREBIRD_CONF_CLASS_MISSING")
            with jar.open(FIREBIRD_CLASS) as src:
                if src.read(4) != b"\xca\xfe\xba\xbe":
                    raise GateFailure("CLASS_MAGIC_INVALID")
        aar_native = native_inventory(aar, aar_names, "jni")
    with zipfile.ZipFile(apk_path) as apk:
        apk_names = check_archive(apk)
        if "classes.dex" not in apk_names:
            raise GateFailure("APK_DEX_MISSING")
        with apk.open("classes.dex") as src:
            magic = src.read(8)
        if len(magic) != 8 or magic[:4] != b"dex\n" or magic[4:7].isdigit() is False or magic[7] != 0:
            raise GateFailure("DEX_MAGIC_INVALID")
        apk_native = native_inventory(apk, apk_names, "lib")

    fb_native = [
        name for name in apk_native
        if name.rsplit("/", 1)[-1].lower() == "libfbclient.so"
        or name.rsplit("/", 1)[-1].lower().startswith("libengine")
    ]
    return {
        "schema": "rafcode-firebird-aar-apk-scope-gate-v1",
        "producer_source_sha": source_sha,
        "aar_sha256": digest(aar_path),
        "apk_sha256": digest(apk_path),
        "aar_native_paths": aar_native,
        "apk_native_paths": apk_native,
        "gate": "PASS_SCOPED_ARTIFACT_STRUCTURE",
        "firebird_engine": ("NATIVE_PRESENT_NOT_FUNCTIONAL_PROOF" if fb_native
                            else "BLOCKED_NO_NATIVE_FIREBIRD_ENGINE_IN_APK"),
        "sql": "NOT_RUN",
        "physical_android": "NOT_RUN",
        "firebird_runtime": "NOT_RUN",
        "claim_allowed": False,
        "evidence_limits": "ZIP structure, class/DEX magic, ELF ABI header only; no complete parsing, linkage, signature or runtime proof",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--aar", required=True)
    parser.add_argument("--apk", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if len(args.source_sha) != 40 or any(c not in "0123456789abcdef" for c in args.source_sha.lower()):
            raise GateFailure("SOURCE_SHA_INVALID")
        result = validate(args.aar, args.apk, args.source_sha.lower())
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print("ARTIFACT_SCOPE_GATE=PASS_SCOPED; CLAIM_ALLOWED=false")
    except (GateFailure, OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        print("ARTIFACT_SCOPE_GATE=BLOCKED; " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
