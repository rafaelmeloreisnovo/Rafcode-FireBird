# SPDX-License-Identifier: MIT
"""Only synthetic fixtures: never a real Firebird or Android runtime claim."""
import importlib.util
import io
import pathlib
import tempfile
import unittest
import zipfile

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "firebird_consumer_scope_gate.py"
spec = importlib.util.spec_from_file_location("firebird_consumer_scope_gate", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def zip_bytes(items):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in items:
            zf.writestr(name, data)
    return buf.getvalue()


def elf(abi, machine=None):
    data = bytearray(20)
    data[:4] = b"\x7fELF"
    data[4] = 2 if abi == "arm64-v8a" else 1
    data[5] = 1
    data[18:20] = (machine if machine is not None else gate.ELF_MACHINE[abi]).to_bytes(2, "little")
    return bytes(data)


class ScopedArtifactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.aar = pathlib.Path(self.tmp.name) / "lib.aar"
        self.apk = pathlib.Path(self.tmp.name) / "app.apk"
        jar = zip_bytes([(gate.FIREBIRD_CLASS, b"\xca\xfe\xba\xbe")])
        self.aar.write_bytes(zip_bytes([("classes.jar", jar)]))
        self.apk.write_bytes(zip_bytes([("classes.dex", b"dex\n039\x00")]))
        self.sha = "a" * 40

    def check(self):
        return gate.validate(self.aar, self.apk, self.sha)

    def test_scoped_no_engine_is_not_pass_engine(self):
        result = self.check()
        self.assertEqual(result["gate"], "PASS_SCOPED_ARTIFACT_STRUCTURE")
        self.assertEqual(result["firebird_engine"], "BLOCKED_NO_NATIVE_FIREBIRD_ENGINE_IN_APK")
        self.assertFalse(result["claim_allowed"])

    def test_native_presence_never_means_runtime_pass(self):
        self.apk.write_bytes(zip_bytes([
            ("classes.dex", b"dex\n039\x00"),
            ("lib/arm64-v8a/libfbclient.so", elf("arm64-v8a")),
        ]))
        result = self.check()
        self.assertEqual(result["firebird_engine"], "NATIVE_PRESENT_NOT_FUNCTIONAL_PROOF")
        self.assertEqual(result["firebird_runtime"], "NOT_RUN")

    def test_wrong_elf_abi_fails_closed(self):
        self.apk.write_bytes(zip_bytes([
            ("classes.dex", b"dex\n039\x00"),
            ("lib/arm64-v8a/libfbclient.so", elf("arm64-v8a", 40)),
        ]))
        with self.assertRaisesRegex(gate.GateFailure, "MISMATCH"):
            self.check()

    def test_missing_dex_fails(self):
        self.apk.write_bytes(zip_bytes([("assets/empty.txt", b"a")]))
        with self.assertRaisesRegex(gate.GateFailure, "DEX_MISSING"):
            self.check()

    def test_wrong_dex_header_fails(self):
        self.apk.write_bytes(zip_bytes([("classes.dex", b"bad-header")]))
        with self.assertRaisesRegex(gate.GateFailure, "DEX_MAGIC_INVALID"):
            self.check()

    def test_zip_traversal_fails(self):
        self.apk.write_bytes(zip_bytes([
            ("classes.dex", b"dex\n039\x00"), ("../escape", b"escape"),
        ]))
        with self.assertRaisesRegex(gate.GateFailure, "UNSAFE_ZIP_PATH"):
            self.check()

    def test_duplicate_zip_name_fails(self):
        self.apk.write_bytes(zip_bytes([
            ("classes.dex", b"dex\n039\x00"),
            ("classes.dex", b"dex\n039\x00"),
        ]))
        with self.assertRaisesRegex(gate.GateFailure, "DUPLICATE_ZIP_PATH"):
            self.check()

    def test_wrong_class_magic_fails(self):
        jar = zip_bytes([(gate.FIREBIRD_CLASS, b"bad!")])
        self.aar.write_bytes(zip_bytes([("classes.jar", jar)]))
        with self.assertRaisesRegex(gate.GateFailure, "CLASS_MAGIC_INVALID"):
            self.check()


if __name__ == "__main__":
    unittest.main()
