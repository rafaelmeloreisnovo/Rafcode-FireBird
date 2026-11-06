# SPDX-License-Identifier: MIT
"""Offline operator CLI. status/plan-* print only. No network or file writes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .manifest import ManifestError, plan, read_bounded, validate_policy, validate_sources

def main(argv=None):
    parser=argparse.ArgumentParser(description="Review-only federation configuration; never connects to Firebird")
    parser.add_argument("command",choices=("status","plan-enable","plan-disable","validate"))
    parser.add_argument("--dir",default=str(Path(__file__).resolve().parent),
                        help="local directory of source and policy manifests")
    args=parser.parse_args(argv)
    try:
        root=Path(args.dir)
        sources=read_bounded(root/"sources.v1.json")
        policy=read_bounded(root/"policy.v1.json")
        validate_sources(sources)
        validate_policy(policy)
        if args.command in ("plan-enable","plan-disable"):
            policy=plan(policy,args.command[len("plan-"):])
        print(json.dumps({"status":"VALIDATED_OFFLINE","command":args.command,
                          "note":"PROPOSAL_ONLY_NO_LIVE_ACTIVATION",
                          "database_access":False,"network_calls":0,
                          "policy":policy},sort_keys=True))
        return 0
    except (OSError, ManifestError) as exc:
        parser.exit(2,"FEDERATION_BLOCKED: "+str(exc)+"\n")

if __name__=="__main__":
    raise SystemExit(main())
