# SPDX-License-Identifier: MIT
"""Strict read-only verification of scoped, synthetic JSONL evidence receipts.

SHA-256 links accidental/rewrite differences against an externally known checkpoint;
without independent anchoring this file is NOT tamper-proof or authenticated.
"""
from __future__ import annotations
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

DOMAIN = b"RAFCODE-FIREBIRD-AUDIT-V1\x00"
ROOT = "0" * 64
MAX_LINE = 8192
KEYS = frozenset({
    "v", "seq", "prev", "id", "ts_utc", "kind", "source", "artifact",
    "execution", "evidence", "state", "gap", "claim_allowed", "sha256"})
LABEL = re.compile(r"[A-Z0-9][A-Z0-9_.:-]{0,63}\Z")
SHA = re.compile(r"[0-9a-f]{64}\Z")
TIMESTAMP = re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\Z")
KINDS = {"TEST", "INCIDENT", "CONTROL", "RISK"}
STATES = {"NOT_RUN", "PASS_SCOPED", "FAIL", "BLOCKED", "UNKNOWN"}
EXECUTIONS = {"NOT_RUN", "EXECUTED", "BLOCKED"}

class ReceiptError(ValueError):
    pass

def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ReceiptError("duplicate JSON key")
        out[key] = value
    return out

def digest(obj):
    body = {k: v for k, v in obj.items() if k != "sha256"}
    raw = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")
    return hashlib.sha256(DOMAIN + raw).hexdigest()

def validate(obj, expected_seq, parent):
    if not isinstance(obj, dict) or set(obj) != KEYS:
        raise ReceiptError("invalid schema / unexpected fields")
    if type(obj["v"]) is not int or obj["v"] != 1:
        raise ReceiptError("unsupported version")
    if type(obj["seq"]) is not int or obj["seq"] != expected_seq:
        raise ReceiptError("gap/replay/order mismatch")
    if not isinstance(obj["prev"], str) or not SHA.fullmatch(obj["prev"]) or obj["prev"] != parent:
        raise ReceiptError("broken parent chain")
    if not isinstance(obj["sha256"], str) or not SHA.fullmatch(obj["sha256"]):
        raise ReceiptError("invalid sha256")
    for field in ("id", "source", "artifact", "evidence", "gap"):
        if not isinstance(obj[field], str) or not LABEL.fullmatch(obj[field]):
            raise ReceiptError("invalid opaque label: " + field)
    if not isinstance(obj["ts_utc"], str) or not TIMESTAMP.fullmatch(obj["ts_utc"]):
        raise ReceiptError("noncanonical UTC timestamp")
    if any(not isinstance(obj[field], str) for field in ("kind", "state", "execution")):
        raise ReceiptError("nonstring enum")
    if obj["kind"] not in KINDS or obj["state"] not in STATES or obj["execution"] not in EXECUTIONS:
        raise ReceiptError("unknown enum")
    try:
        datetime.strptime(obj["ts_utc"], "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ReceiptError("invalid UTC date") from exc
    if obj["sha256"] != digest(obj):
        raise ReceiptError("digest mismatch")
    if obj["claim_allowed"] is not False:
        raise ReceiptError("unauthorized claim: requires external assessment")
    if obj["state"] == "PASS_SCOPED" and (obj["execution"] != "EXECUTED" or obj["evidence"] == "TOKEN_VAZIO"):
        raise ReceiptError("false PASS_SCOPED without execution and evidence")
    if obj["execution"] == "NOT_RUN" and obj["state"] == "PASS_SCOPED":
        raise ReceiptError("NOT_RUN != PASS")

def verify_lines(lines):
    previous = ROOT
    count = 0
    for raw in lines:
        if not isinstance(raw, bytes) or not raw.endswith(b"\n") or len(raw) > MAX_LINE:
            raise ReceiptError("oversized / truncated frame")
        try:
            record = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicates,
                                parse_constant=lambda value: (_ for _ in ()).throw(ReceiptError("nonfinite JSON constant")))
        except (ValueError, UnicodeError, TypeError, RecursionError) as exc:
            raise ReceiptError("invalid JSON") from exc
        validate(record, count + 1, previous)
        count += 1
        previous = record["sha256"]
    if not count:
        raise ReceiptError("empty chain")
    return count, previous

def verify_path(path):
    def bounded_read(handle):
        while True:
            raw = handle.readline(MAX_LINE + 1)
            if not raw:
                return
            if len(raw) > MAX_LINE or not raw.endswith(b"\n"):
                raise ReceiptError("oversized / truncated frame")
            yield raw
    with Path(path).open("rb") as handle:
        return verify_lines(bounded_read(handle))

def make_synthetic(seq, prev, *, state="NOT_RUN", execution="NOT_RUN", evidence="TOKEN_VAZIO", kind="TEST"):
    """Build an in-memory test frame; NEVER auto-write to an external audit ledger."""
    obj = dict(v=1, seq=seq, prev=prev, id="SYNTHETIC_001", ts_utc="2026-11-06T00:00:00Z",
               kind=kind, source="SYNTHETIC", artifact="SYNTHETIC",
               execution=execution, evidence=evidence, state=state,
               gap="TOKEN_VAZIO", claim_allowed=False)
    obj["sha256"] = digest(obj)
    return obj

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read-only validation of RAFAELIA scoped receipts; no authenticity claim")
    parser.add_argument("jsonl", help="local file; does not modify it")
    args = parser.parse_args()
    try:
        count, last = verify_path(args.jsonl)
    except (OSError, ReceiptError) as exc:
        parser.exit(1, "RECEIPT_FAIL: " + str(exc) + "\n")
    print("RECEIPT_PASS_SCOPED count=%d last_sha256=%s unauthenticated=true" % (count, last))
