# SPDX-License-Identifier: MIT
import json
import unittest
from audit.receipt_chain import ROOT, ReceiptError, make_synthetic, verify_lines, digest

def frame(obj):
    return (json.dumps(obj, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")

class VerifyTest(unittest.TestCase):
    def setUp(self):
        self.a = make_synthetic(1, ROOT)
        self.b = make_synthetic(2, self.a["sha256"], state="PASS_SCOPED", execution="EXECUTED", evidence="SCOPED_HASH_1")

    def test_valid_chain(self):
        self.assertEqual(verify_lines([frame(self.a), frame(self.b)])[0], 2)

    def test_reordered(self):
        with self.assertRaises(ReceiptError):
            verify_lines([frame(self.b), frame(self.a)])

    def test_dropped(self):
        with self.assertRaises(ReceiptError):
            verify_lines([frame(self.b)])

    def test_tampered(self):
        x = dict(self.b, evidence="OTHER")
        with self.assertRaises(ReceiptError):
            verify_lines([frame(self.a), frame(x)])

    def test_full_rewrite_is_not_anchored(self):
        x = dict(self.b, evidence="OTHER")
        x["sha256"] = digest(x)
        # A rewritten unanchored chain can pass; independent anchoring is REQUIRED.
        self.assertEqual(verify_lines([frame(self.a), frame(x)])[0], 2)
        self.assertNotEqual(x["sha256"], self.b["sha256"])

    def test_truncated(self):
        with self.assertRaises(ReceiptError):
            verify_lines([frame(self.a)[:-1]])

    def test_duplicate_json_key(self):
        raw = frame(self.a).decode().rstrip("\n")
        raw = raw[:-1] + ',"seq":1}'
        with self.assertRaises(ReceiptError):
            verify_lines([(raw + "\n").encode()])

    def test_unknown_field(self):
        x = dict(self.a, secret="LEAK")
        x["sha256"] = digest(x)
        with self.assertRaises(ReceiptError):
            verify_lines([frame(x)])

    def test_false_pass(self):
        x = make_synthetic(1, ROOT, state="PASS_SCOPED", execution="NOT_RUN", evidence="TOKEN_VAZIO")
        with self.assertRaises(ReceiptError):
            verify_lines([frame(x)])

    def test_claim_denied(self):
        x = dict(self.a, claim_allowed=True)
        x["sha256"] = digest(x)
        with self.assertRaises(ReceiptError):
            verify_lines([frame(x)])

    def test_noncanonical_timestamp(self):
        x = dict(self.a, ts_utc="today")
        x["sha256"] = digest(x)
        with self.assertRaises(ReceiptError):
            verify_lines([frame(x)])

    def test_oversized(self):
        with self.assertRaises(ReceiptError):
            verify_lines([b"z" * 8193 + b"\n"])

    def test_empty(self):
        with self.assertRaises(ReceiptError):
            verify_lines([])

if __name__ == "__main__":
    unittest.main()
