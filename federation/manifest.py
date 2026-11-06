# SPDX-License-Identifier: MIT
"""Offline, strict metadata-only federation manifest and observer policy validator.

Never imports or connects to Firebird. No transport, service actions, sockets,
auto-failover or writes. A policy's "enabled" bit is a proposed OBSERVER switch
for a future reviewed adapter, not a database privilege or live activation.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

PIN = re.compile(r"[0-9a-f]{40}\Z")
ALLOWED = {
    "producer": "rafaelmeloreisnovo/Rafcode-FireBird",
    "engine_fork": "rafaelmeloreisnovo/firebird_rafcodephi",
    "upstream_reference": "FirebirdSQL/firebird",
}
SOURCE_KEYS = {"role", "repo", "commit", "mode"}
SOURCE_ROOT = {"schema", "producer", "automatic_network_access", "database_access", "enable_by_default", "sources"}
POLICY_KEYS = {"schema", "abi_version", "revision", "enabled", "sink",
               "read_only", "auto_recovery", "auto_failover", "auto_backup_restore",
               "auto_firebird_config_change", "syslog_transport", "human_ack_required",
               "rollback", "scope"}
class ManifestError(ValueError):
    pass

def unique_pairs(pairs):
    d = {}
    for key, value in pairs:
        if key in d:
            raise ManifestError("duplicate field")
        d[key] = value
    return d

def read_bounded(path: Path):
    with path.open("rb") as handle:
        raw = handle.read(16385)
        if len(raw) > 16384:
            raise ManifestError("manifest too large")
        if not raw:
            raise ManifestError("empty manifest")
    try:
        return json.loads(raw.decode("utf8"), object_pairs_hook=unique_pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(ManifestError("nonfinite JSON constant")))
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise ManifestError("invalid JSON") from exc

def validate_sources(p):
    if not isinstance(p, dict) or set(p) != SOURCE_ROOT:
        raise ManifestError("unexpected source schema")
    if p["schema"] != "raf-federation-sources-v1" or p["producer"] != ALLOWED["producer"]:
        raise ManifestError("unknown source authority")
    for flag in ("automatic_network_access","database_access","enable_by_default"):
        if p[flag] is not False:
            raise ManifestError("source registry must remain offline/pinned by default")
    if not isinstance(p["sources"], list) or len(p["sources"]) != 3:
        raise ManifestError("source set not exactly three typed roots")
    seen = set()
    for src in p["sources"]:
        if not isinstance(src, dict) or set(src) != SOURCE_KEYS:
            raise ManifestError("invalid source entry")
        role=src["role"]
        if not isinstance(role,str) or role not in ALLOWED or role in seen or src["repo"] != ALLOWED[role]:
            raise ManifestError("unknown/duplicate/untrusted repository")
        if src["mode"] != "PIN_ONLY" or not isinstance(src["commit"],str) or not PIN.fullmatch(src["commit"]):
            raise ManifestError("unpinned or unsafe source")
        seen.add(role)
    if seen != set(ALLOWED):
        raise ManifestError("missing source role")
    return True

def validate_policy(p):
    if not isinstance(p,dict) or set(p) != POLICY_KEYS:
        raise ManifestError("unexpected policy schema")
    if p["schema"] != "raf-federation-policy-v1" or type(p["abi_version"]) is not int or p["abi_version"] != 1:
        raise ManifestError("policy ABI mismatch")
    if type(p["revision"]) is not int or not (0 < p["revision"] < 2**32):
        raise ManifestError("revision must be positive monotonic u32")
    if p["enabled"] not in (False,True) or type(p["enabled"]) is not bool:
        raise ManifestError("invalid enable switch")
    for f in ("read_only","human_ack_required"):
        if p[f] is not True:
            raise ManifestError("read-only/operator gate required")
    for f in ("auto_recovery","auto_failover","auto_backup_restore","auto_firebird_config_change"):
        if p[f] is not False:
            raise ManifestError("destructive/autonomous capability forbidden")
    if p["scope"] != "OBSERVER_ONLY" or p["rollback"] != "LAST_REVIEWED_CONFIG" or p["syslog_transport"] != "DISABLED":
        raise ManifestError("unsupported scope/rollback/transport")
    if p["sink"] not in ("NONE","PREVIEW","OPERATOR"):
        raise ManifestError("unknown preview sink")
    if bool(p["enabled"]) != (p["sink"] != "NONE"):
        raise ManifestError("disabled sink or enabled sink mismatch")
    return True

def plan(policy, action):
    """Return an in-memory *proposal*. It does not write or activate services."""
    validate_policy(policy)
    if action not in ("enable","disable"):
        raise ManifestError("unknown action")
    if policy["revision"] == 2**32 - 1:
        raise ManifestError("revision exhausted")
    proposal=dict(policy,revision=policy["revision"]+1,
                  enabled=(action == "enable"),sink="PREVIEW" if action == "enable" else "NONE")
    validate_policy(proposal)
    return proposal
