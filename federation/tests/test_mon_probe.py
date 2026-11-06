# SPDX-License-Identifier: MIT
"""Falsifiers use fake clients only. Zero DB connections in GitHub CI."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from federation.manifest import read_bounded, plan
from federation.mon_probe import (SQL, SCHEMA, ProbeBlocked, _output, _preflight,
                                   _sample_with_client, _verified_worker_json, supervise)
ROOT = Path(__file__).resolve().parents[1]
class Cursor:
    def __init__(self, rows):
        self.rows = iter(rows)
        self.sql = []
    def execute(self, sql):
        self.sql.append(sql)
    def fetchone(self):
        return next(self.rows, None)
class Tr:
    def __init__(self, rows):
        self.cursor_obj = Cursor(rows)
        self.rollbacks = 0
    def cursor(self):
        return self.cursor_obj
    def rollback(self):
        self.rollbacks += 1
class Conn:
    def __init__(self, rows):
        self.tr = Tr(rows)
        self.closed = 0
        self.buffers = []
    def transaction_manager(self, tpb):
        self.buffers.append(tpb)
        return self.tr
    def close(self):
        self.closed += 1
class FirebirdMonTests(unittest.TestCase):
    def setUp(self):
        self.policy = plan(read_bounded(ROOT / "federation" / "policy.v1.json"), "enable")
        self.env = {"RAF_FB_DISPOSABLE": "1", "RAF_FB_DSN": "127.0.0.1:disposable",
                    "RAF_FB_USER": "observer", "RAF_FB_PASSWORD": "SECRET_NOT_LOGGED"}
    def fake_client(self, rows):
        con = Conn(rows)
        calls = []
        def connect(dsn, **kw):
            calls.append((dsn, kw))
            return con
        class Isolation:
            READ_COMMITTED_RECORD_VERSION = 7
        class Access:
            READ = 4
        def tpb(isolation, access_mode):
            self.assertEqual((isolation, access_mode), (7, 4))
            return b"READ_ONLY_TPB"
        return con, calls, connect, tpb, Isolation, Access
    def sample(self, rows):
        con,calls,connect,tpb,i,a=self.fake_client(rows)
        result=_sample_with_client(connect,tpb,i,a, self.env["RAF_FB_DSN"],
                                   self.env["RAF_FB_USER"], self.env["RAF_FB_PASSWORD"])
        return result,con,calls
    def test_one_snapshot_exact_query_and_rollback(self):
        result,con,calls=self.sample([(8192, 10, 5)])
        self.assertEqual(result["state"],"MON_SNAPSHOT")
        self.assertFalse(result["writer_progress_known"])
        self.assertEqual(result["database_mutations"],0)
        self.assertEqual(con.tr.cursor_obj.sql,[SQL])
        self.assertEqual(con.buffers,[b"READ_ONLY_TPB"])
        self.assertEqual((con.tr.rollbacks,con.closed),(1,1))
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0][1]["timeout"],3)
        self.assertNotIn("SECRET_NOT_LOGGED",str(result))
    def test_fresh_transaction_each_probe(self):
        r1,c1,_=self.sample([(8192,0,0)])
        r2,c2,_=self.sample([(8192,10,8)])
        self.assertNotEqual(c1,c2)
        self.assertEqual((c1.tr.rollbacks,c2.tr.rollbacks),(1,1))
        self.assertFalse(r1["writer_progress_known"] or r2["writer_progress_known"])
    def test_unknown_is_not_zero(self):
        r,c,_=self.sample([])
        self.assertEqual(r["state"],"UNKNOWN")
        self.assertIsNone(r["page_reads"])
        self.assertEqual((c.tr.rollbacks,c.closed),(1,1))
    def test_optional_missing_counters(self):
        r,_,_=self.sample([(8192,None,None)])
        self.assertEqual(r["state"],"MON_SNAPSHOT")
        self.assertIsNone(r["page_writes"])
    def test_duplicate_monitor_row_denied(self):
        con,calls,connect,tpb,i,a=self.fake_client([(8192,1,2),(8192,3,4)])
        with self.assertRaises(ProbeBlocked): _sample_with_client(connect,tpb,i,a,"db","u","p")
        self.assertEqual((con.tr.rollbacks,con.closed),(1,1))
    def test_invalid_rows_denied(self):
        for row in [(True,1,2),(8192,-1,0),(8192,True,0),(8192,1,2,3),
                    (8192,1,2**64),(0,1,1),("8192",1,1)]:
            with self.subTest(row=row),self.assertRaises(ProbeBlocked):
                self.sample([row])
    def test_failed_connect_sanitized_by_worker_boundary(self):
        con,calls,connect,tpb,i,a=self.fake_client([(8192,1,2)])
        def bad(*x,**kw): raise RuntimeError("SECRET_NOT_LOGGED: localhost:db")
        with self.assertRaises(RuntimeError):
            _sample_with_client(bad,tpb,i,a,"db","u","SECRET_NOT_LOGGED")
        self.assertEqual(len(calls),0)
    def test_reject_missing_ack(self):
        with self.assertRaises(ProbeBlocked): _preflight(self.policy,False,self.env)
    def test_reject_default_disabled(self):
        pol=read_bounded(ROOT/"federation"/"policy.v1.json")
        with self.assertRaises(ProbeBlocked): _preflight(pol,True,self.env)
    def test_reject_non_preview_sink(self):
        pol=dict(self.policy,sink="OPERATOR")
        with self.assertRaises(ProbeBlocked): _preflight(pol,True,self.env)
    def test_reject_missing_disposable_declaration(self):
        env=dict(self.env,RAF_FB_DISPOSABLE="0")
        with self.assertRaises(ProbeBlocked): _preflight(self.policy,True,env)
    def test_reject_missing_credentials(self):
        for key in ("RAF_FB_DSN","RAF_FB_USER","RAF_FB_PASSWORD"):
            env=dict(self.env);del env[key]
            with self.subTest(key=key),self.assertRaises(ProbeBlocked):
                _preflight(self.policy,True,env)
    def test_result_schema_rejects_extra_fields(self):
        x=_output("MON_SNAPSHOT",1,2);x["raw_sql"]="secrets"
        with self.assertRaises(ProbeBlocked):
            _verified_worker_json(json.dumps(x))
    def test_result_schema_rejects_forged_progress(self):
        x=_output("MON_SNAPSHOT",1,2);x["writer_progress_known"]=True
        with self.assertRaises(ProbeBlocked):_verified_worker_json(json.dumps(x))
    def test_result_schema_rejects_bogus_zero_types(self):
        x=_output("MON_SNAPSHOT",1,2);x["database_mutations"]=False
        with self.assertRaises(ProbeBlocked):_verified_worker_json(json.dumps(x))
    def test_result_schema_rejects_non_json(self):
        with self.assertRaises(ProbeBlocked):_verified_worker_json("SECRET_NOT_LOGGED")
    def test_parent_disabled_does_not_spawn(self):
        calls=[]
        def runner(*a,**kw):
            calls.append(a);raise AssertionError("must not spawn")
        state,obs=supervise(ROOT/"federation"/"policy.v1.json",True,self.env,6,runner)
        self.assertEqual((state,obs),("BLOCKED",None))
        self.assertFalse(calls)
    def test_parent_timeout_denies_success(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"policy.json";path.write_text(json.dumps(self.policy))
            def run(*args,**kw):raise subprocess.TimeoutExpired("python",6)
            status,obs=supervise(path,True,self.env,6,run)
            self.assertEqual((status,obs),("DEADLINE_EXCEEDED",None))
    def test_parent_never_carries_credentials_in_argv(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"policy.json";path.write_text(json.dumps(self.policy))
            def run(cmd,**kwargs):
                self.assertNotIn("SECRET_NOT_LOGGED", " ".join(cmd))
                self.assertEqual(kwargs["timeout"],6)
                self.assertFalse(kwargs.get("check"))
                return SimpleNamespace(returncode=0,stdout=json.dumps(_output("MON_SNAPSHOT",0,0)),stderr="")
            state,obs=supervise(path,True,self.env,6,run)
            self.assertEqual(state,"OBSERVED_SCOPED")
            self.assertFalse(obs["writer_progress_known"])
    def test_bad_child_output_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"policy.json";path.write_text(json.dumps(self.policy))
            def run(*args,**kw):return SimpleNamespace(returncode=0,stdout='{"SQL":"secret"}',stderr="")
            self.assertEqual(supervise(path,True,self.env,6,run),("OBSERVATION_FAILED",None))
    def test_extreme_deadline_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"policy.json";path.write_text(json.dumps(self.policy))
            self.assertEqual(supervise(path,True,self.env,500),("BLOCKED",None))
if __name__=="__main__":
    unittest.main()
