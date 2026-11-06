#!/usr/bin/env python3
"""RAFCODE G1 independent Firebird SQL compatibility gate; disposable DB ONLY.

This checks a real Firebird embedded engine, not the Python MON adapter or
upstream #9269 Windows/NTFS hang. No network, no production DB input, no daemon,
no engine source mutation, no external packages. The database is created in a
private ephemeral directory and erased by TemporaryDirectory after the test.

Result is machine-readable and self-hashed (NOT a signed/authenticated receipt).
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
import pathlib
import platform
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

ISQL = shutil.which('isql-fb')
SQL_PROBE = (
    'SELECT d.MON$PAGE_SIZE, i.MON$PAGE_READS, i.MON$PAGE_WRITES '
    'FROM MON$DATABASE d LEFT JOIN MON$IO_STATS i '
    'ON i.MON$STAT_ID = d.MON$STAT_ID AND i.MON$STAT_GROUP = 0'
)

def command(cmd: list[str], query: str, env: dict[str, str], deadline: int = 12):
    return subprocess.run(cmd, input=query, capture_output=True, text=True,
                          env=env, timeout=deadline, check=False)

def metric(data: str, field: str):
    match = re.search(r'^' + re.escape(field) + r'\s+([0-9]+)\s*$', data, re.M)
    return int(match.group(1)) if match else None

def main():
    receipt = {
        'schema': 'raf-firebird-real-disposable-sql-gate-v1',
        'at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'scope': 'REAL_FIREBIRD_EMBEDDED_DISPOSABLE_SQL_ONLY',
        'os': platform.system(),
        'machine': platform.machine(),
        'engine_version': None,
        'github_mon_adapter_exact_code_executed': False,
        'python_firebird_driver_installed_for_test': False,
        'firebird_5_disk_full_issue_9269_reproduced': False,
        'database_source': 'NEW_PRIVATE_TEMPORARY_DATABASE',
        'probe_sql_sha256': hashlib.sha256(SQL_PROBE.encode()).hexdigest(),
        'read_only_dml_falsifier_expected_to_fail': True,
        'read_only_dml_rejected': False,
        'result_row_count_zero': False,
        'page_size': None,
        'page_reads': None,
        'page_writes': None,
        'create_database_success': False,
        'mon_probe_query_success': False,
        'status': 'NOT_RUN',
        'claim_allowed': False,
    }
    if not ISQL:
        print(json.dumps(receipt, sort_keys=True))
        return 2
    ver = command([ISQL, '-z'], 'QUIT;\n', dict(os.environ), deadline=5)
    versions = re.findall(r'V(?:ersion)?[^\n]{0,100}4\.0[^\n]*', ver.stdout + ver.stderr, re.I)
    receipt['engine_version'] = versions[0] if versions else 'FIREBIRD_VERSION_UNVERIFIED'
    if not versions:
        receipt['status'] = 'BLOCKED_VERSION'
        print(json.dumps(receipt, sort_keys=True))
        return 2
    with tempfile.TemporaryDirectory(prefix='raf_fb_g1_real_') as tmp:
        os.chmod(tmp, 0o700)
        db = pathlib.Path(tmp, 'gate.fdb')
        # Temporary path is generated internally. No option to target user DB.
        pwd = secrets.token_hex(20)
        baseenv = dict(os.environ, ISC_USER='SYSDBA', ISC_PASSWORD=pwd)
        ddl = (f"CREATE DATABASE '{db}' USER 'SYSDBA' PASSWORD '{pwd}' "
               'DEFAULT CHARACTER SET UTF8;\n'
               'CREATE TABLE RAF_G1_TESTONLY (VAL INTEGER NOT NULL);\n'
               'COMMIT;\nQUIT;\n')
        created = command([ISQL, '-q'], ddl, baseenv)
        # No raw output is logged: Firebird can echo DSN and auth data in errors.
        receipt['create_database_success'] = bool(
            created.returncode == 0 and db.is_file() and not created.stderr.strip())
        if not receipt['create_database_success']:
            receipt['status'] = 'BLOCKED_CREATE'
        else:
            negative = (
                'SET LIST ON;\nCOMMIT;\n'
                'SET TRANSACTION READ ONLY READ COMMITTED RECORD_VERSION;\n'
                f'{SQL_PROBE};\n'
                'INSERT INTO RAF_G1_TESTONLY (VAL) VALUES (123);\n'
                'ROLLBACK;\n'
                'SET TRANSACTION READ ONLY READ COMMITTED RECORD_VERSION;\n'
                'SELECT COUNT(*) AS N FROM RAF_G1_TESTONLY;\n'
                'ROLLBACK;\nQUIT;\n'
            )
            ran = command([ISQL, '-q', str(db)], negative, baseenv)
            receipt['page_size'] = metric(ran.stdout, 'MON$PAGE_SIZE')
            receipt['page_reads'] = metric(ran.stdout, 'MON$PAGE_READS')
            receipt['page_writes'] = metric(ran.stdout, 'MON$PAGE_WRITES')
            receipt['result_row_count_zero'] = metric(ran.stdout, 'N') == 0
            receipt['read_only_dml_rejected'] = (
                ran.returncode != 0 and
                'attempted update during read-only transaction' in ran.stderr)
            receipt['mon_probe_query_success'] = (
                isinstance(receipt['page_size'], int) and
                1024 <= receipt['page_size'] <= 65536 and
                isinstance(receipt['page_reads'], int) and
                isinstance(receipt['page_writes'], int) and
                not any(k in ran.stderr for k in ('unknown column', 'Token unknown',
                                                  'Dynamic SQL Error')))
            receipt['status'] = ('PASS_SCOPED_FIREBIRD4_SQL'
                                 if receipt['mon_probe_query_success'] and
                                    receipt['read_only_dml_rejected'] and
                                    receipt['result_row_count_zero']
                                 else 'FAILED_SCOPED')
    unsigned = json.dumps(receipt, sort_keys=True, ensure_ascii=False,
                          separators=(',', ':')).encode('utf8')
    receipt['self_sha256_not_signature'] = hashlib.sha256(unsigned).hexdigest()
    out = pathlib.Path('/mnt/data/rafcode_firebird4_mon_g1_receipt.json')
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf8')
    print(json.dumps({'status': receipt['status'], 'engine': receipt['engine_version'],
                      'page_size': receipt['page_size'],
                      'reads': receipt['page_reads'], 'writes': receipt['page_writes'],
                      'denied_dml': receipt['read_only_dml_rejected'],
                      'rows_after': 0 if receipt['result_row_count_zero'] else 'UNKNOWN',
                      'receipt_sha256': receipt['self_sha256_not_signature']}, sort_keys=True))
    return 0 if receipt['status'] == 'PASS_SCOPED_FIREBIRD4_SQL' else 1

if __name__ == '__main__':
    raise SystemExit(main())
