# SPDX-License-Identifier: MIT
import copy
import json
import unittest
from pathlib import Path
from federation.manifest import (ManifestError, read_bounded, validate_sources, validate_policy, plan)
ROOT=Path(__file__).resolve().parents[1]
class FederationTests(unittest.TestCase):
    def setUp(self):
        self.src=read_bounded(ROOT/"sources.v1.json")
        self.p=read_bounded(ROOT/"policy.v1.json")
    def test_baseline_off(self):
        self.assertTrue(validate_sources(self.src))
        self.assertTrue(validate_policy(self.p))
        self.assertFalse(self.p["enabled"])
    def test_plan_no_mutation(self):
        proposal=plan(self.p,"enable")
        self.assertTrue(proposal["enabled"])
        self.assertEqual(proposal["sink"],"PREVIEW")
        self.assertFalse(self.p["enabled"])
        self.assertFalse(plan(proposal,"disable")["enabled"])
    def test_unknown_repositories(self):
        x=copy.deepcopy(self.src)
        x["sources"][0]["repo"]="example.com/attacker"
        with self.assertRaises(ManifestError): validate_sources(x)
    def test_unpinned(self):
        x=copy.deepcopy(self.src)
        x["sources"][0]["commit"]="master"
        with self.assertRaises(ManifestError): validate_sources(x)
    def test_duplicate_role(self):
        x=copy.deepcopy(self.src)
        x["sources"][0]["role"]="engine_fork"
        with self.assertRaises(ManifestError): validate_sources(x)
    def test_network_flag_denied(self):
        x=copy.deepcopy(self.src)
        x["automatic_network_access"]=True
        with self.assertRaises(ManifestError): validate_sources(x)
    def test_unknown_field_denied(self):
        x=copy.deepcopy(self.p)
        x["credentials"]="secret"
        with self.assertRaises(ManifestError): validate_policy(x)
    def test_sneaky_write_denied(self):
        for field in ("auto_recovery","auto_failover","auto_backup_restore","auto_firebird_config_change"):
            x=copy.deepcopy(self.p);x[field]=True
            with self.subTest(field=field), self.assertRaises(ManifestError):validate_policy(x)
    def test_sink_mismatch_denied(self):
        x=copy.deepcopy(self.p);x["enabled"]=True
        with self.assertRaises(ManifestError):validate_policy(x)
    def test_unknown_transport_denied(self):
        x=copy.deepcopy(self.p);x["syslog_transport"]="UDP"
        with self.assertRaises(ManifestError):validate_policy(x)
    def test_revision_bool_denied(self):
        x=copy.deepcopy(self.p);x["revision"]=True
        with self.assertRaises(ManifestError):validate_policy(x)
    def test_exhausted(self):
        x=copy.deepcopy(self.p);x["revision"]=2**32-1
        with self.assertRaises(ManifestError):plan(x,"enable")
    def test_duplicate_json_key(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"invalid.json"
            p.write_text('{"enabled":false,"enabled":true}',encoding="utf8")
            with self.assertRaises(ManifestError):read_bounded(p)
    def test_too_large(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"invalid.json";p.write_bytes(b"x"*17000)
            with self.assertRaises(ManifestError):read_bounded(p)
if __name__=="__main__":
    unittest.main()
