# SPDX-License-Identifier: MIT
"""Opt-in Firebird MON$ one-shot probe, isolated from freestanding observer.

SOURCE != EXECUTION != EVIDENCE != CLAIM. A readable MON$ snapshot is NOT
evidence of a healthy writer or proof against Firebird #9269. No SQL/Trace
text, identifiers, raw error details, daemon, recovery, failover or writes.

The *parent* starts one short-lived child process and enforces a wall-clock
deadline; the child uses a fresh read-only Firebird transaction. The parent
never sends the user's DSN or credentials as command-line arguments. The
optional external Python/Firebird driver is NOT part of the freestanding core.
"""
from __future__ import annotations
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
from .manifest import ManifestError, read_bounded, validate_policy, validate_sources

SCHEMA = "raf-firebird-mon-probe-v1"
EXPECTED_DRIVER_VERSION = "2.1.2"
ROOT = Path(__file__).resolve().parents[1]
# PRE: fixed SQL, no parameters, only synthetic aggregate observation.
# POST: transaction is rolled back and connection closed; no user tables.
# MON$IO_STATS counters are *not* evidence that a user statement completed.
SQL = (
    'SELECT d.MON$PAGE_SIZE, i.MON$PAGE_READS, i.MON$PAGE_WRITES '
    'FROM MON$DATABASE d LEFT JOIN MON$IO_STATS i '
    'ON i.MON$STAT_ID = d.MON$STAT_ID AND i.MON$STAT_GROUP = 0'
)
RESULT_KEYS = frozenset(("schema", "state", "page_reads", "page_writes",
                         "snapshot_known", "writer_progress_known", "database_mutations"))
MAX_U64 = (1 << 63) - 1

class ProbeBlocked(Exception):
    """Confidential details MUST NOT appear in public error output."""

def _valid_count(value, allow_missing=False):
    if value is None and allow_missing:
        return None
    if type(value) is not int or not (0 <= value <= MAX_U64):
        raise ProbeBlocked()
    return value

def _output(state, reads=None, writes=None):
    if state not in ("MON_SNAPSHOT", "UNKNOWN"):
        raise ProbeBlocked()
    reads = _valid_count(reads, allow_missing=True)
    writes = _valid_count(writes, allow_missing=True)
    return {"schema": SCHEMA, "state": state, "page_reads": reads,
            "page_writes": writes, "snapshot_known": state == "MON_SNAPSHOT",
            "writer_progress_known": False, "database_mutations": 0}

def _validated_policy(path):
    # PRE: even a valid enabled policy is never a claim of runtime authority.
    policy = read_bounded(Path(path))
    validate_policy(policy)
    return policy

def _preflight(policy, ack, environment):
    if not ack or policy["enabled"] is not True or policy["sink"] != "PREVIEW":
        raise ProbeBlocked()
    # These flags are explicit operator declarations, NOT sandbox attestation.
    if environment.get("RAF_FB_DISPOSABLE") != "1":
        raise ProbeBlocked()
    for name, limit in (("RAF_FB_DSN", 512), ("RAF_FB_USER", 128),
                        ("RAF_FB_PASSWORD", 1024)):
        value = environment.get(name)
        if not isinstance(value, str) or not (0 < len(value) <= limit) or "\x00" in value:
            raise ProbeBlocked()

def _sample_with_client(connect, tpb, isolation, access, dsn, user, password):
    """One fresh, **read-only** transaction. No implicit main transaction.

    PRE: connect/TPB are from an approved Firebird driver, caller has a
    disposable database and read-only account. Tests inject fake clients.
    POST: one SELECT; rollback even on malformed row; connection closed.
    Neither successful counter increments nor MON$ reachability imply
    application transaction progress. Any malformed/multiple result fails.
    """
    con = None
    tm = None
    try:
        con = connect(dsn, user=user, password=password, timeout=3)
        tm = con.transaction_manager(
            tpb(isolation.READ_COMMITTED_RECORD_VERSION, access_mode=access.READ))
        cur = tm.cursor()
        cur.execute(SQL)
        row = cur.fetchone()
        if row is None:
            return _output("UNKNOWN")
        if cur.fetchone() is not None or not isinstance(row, (tuple, list)) or len(row) != 3:
            raise ProbeBlocked()
        page_size = _valid_count(row[0])
        if not (1024 <= page_size <= 65536):
            raise ProbeBlocked()
        return _output("MON_SNAPSHOT", row[1], row[2])
    finally:
        # Exceptions here invalidate evidence too; never report a success.
        try:
            if tm is not None:
                tm.rollback()
        finally:
            if con is not None:
                con.close()

def _worker(policy_path, ack, environment):
    try:
        policy = _validated_policy(policy_path)
        _preflight(policy, ack, environment)
        if importlib.metadata.version("firebird-driver") != EXPECTED_DRIVER_VERSION:
            raise ProbeBlocked()
        # No package download or network setup. Module import occurs ONLY
        # after opt-in, explicit ack, disposable declaration and credentials.
        from firebird.driver import connect, tpb, Isolation, TraAccessMode
        return _sample_with_client(
            connect, tpb, Isolation, TraAccessMode,
            environment["RAF_FB_DSN"], environment["RAF_FB_USER"],
            environment["RAF_FB_PASSWORD"])
    except Exception:
        # Sanitize driver exceptions: they may contain DB path, IP or user.
        return _output("UNKNOWN")

def _verified_worker_json(raw):
    # Reject unexpected output, error text, untrusted fields or huge responses.
    if not isinstance(raw, str) or len(raw) > 512:
        raise ProbeBlocked()
    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        raise ProbeBlocked() from None
    if type(data) is not dict or set(data) != RESULT_KEYS or data["schema"] != SCHEMA:
        raise ProbeBlocked()
    if data["state"] not in ("MON_SNAPSHOT", "UNKNOWN"):
        raise ProbeBlocked()
    if type(data["snapshot_known"]) is not bool or (data["snapshot_known"] != (data["state"] == "MON_SNAPSHOT")):
        raise ProbeBlocked()
    if data["writer_progress_known"] is not False or type(data["database_mutations"]) is not int or data["database_mutations"] != 0:
        raise ProbeBlocked()
    _valid_count(data["page_reads"], allow_missing=True)
    _valid_count(data["page_writes"], allow_missing=True)
    if data["state"] == "UNKNOWN" and (data["page_reads"] is not None or data["page_writes"] is not None):
        raise ProbeBlocked()
    return data

def supervise(policy_path, ack, environment, deadline, runner=subprocess.run):
    """The only path that can spawn a child. Never writes a config file."""
    try:
        policy = _validated_policy(policy_path)
        _preflight(policy, ack, environment)
    except (ManifestError, OSError, ProbeBlocked, UnicodeError):
        return "BLOCKED", None
    if type(deadline) is not int or not (4 <= deadline <= 20):
        return "BLOCKED", None
    cmd = [sys.executable, "-m", "federation.mon_probe", "_worker",
           "--policy", str(Path(policy_path).resolve()), "--ack"]
    try:
        result = runner(cmd, env=dict(environment), cwd=str(ROOT), timeout=deadline,
                        capture_output=True, text=True, check=False)
    except subprocess.TimeoutExpired:
        # subprocess.run kills and reaps the child; DB server-level work may
        # still require DBA investigation, so never claim fully cancelled.
        return "DEADLINE_EXCEEDED", None
    except (OSError, ValueError):
        return "OBSERVATION_FAILED", None
    if result.returncode != 0:
        return "OBSERVATION_FAILED", None
    try:
        observation = _verified_worker_json(result.stdout)
    except ProbeBlocked:
        return "OBSERVATION_FAILED", None
    return "OBSERVED_SCOPED", observation

def main(argv=None):
    p = argparse.ArgumentParser(description="One-shot, opt-in, read-only Firebird MON$ probe")
    p.add_argument("action", choices=("status", "once", "_worker"))
    p.add_argument("--ack", action="store_true", help="explicit operator acknowledgment")
    p.add_argument("--policy", default=str(ROOT / "federation" / "policy.v1.json"))
    p.add_argument("--deadline", type=int, default=6, help="child wall-clock limit, 4-20 seconds")
    a = p.parse_args(argv)
    if a.action == "status":
        try:
            pol = _validated_policy(a.policy)
            state = "POLICY_OFF" if not pol["enabled"] else "POLICY_ENABLED_NOT_RUNNING"
        except (OSError, ManifestError):
            state = "BLOCKED"
        print(json.dumps({"schema": SCHEMA, "state": state, "network_calls": 0,
                          "database_mutations": 0}, sort_keys=True))
        return 0 if state != "BLOCKED" else 2
    if a.action == "_worker":
        # Even direct invocation of the private worker must be opt-in.
        print(json.dumps(_worker(a.policy, a.ack, os.environ), sort_keys=True))
        return 0
    status, observed = supervise(a.policy, a.ack, os.environ, a.deadline)
    print(json.dumps({"schema": SCHEMA, "status": status, "observation": observed,
                      "writer_hang_proven": False, "database_failover": False},
                     sort_keys=True))
    return 0 if status == "OBSERVED_SCOPED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
