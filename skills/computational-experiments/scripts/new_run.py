#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 GeometrIA Lab, CBG
# SPDX-License-Identifier: MIT
r"""Create, start and finish run directories for reproducible mathematical computations.

Each run lives in <root>/<YYYY-MM-DD>_<slug>/ and is described by manifest.json.

Subcommands
  create SLUG      make <root>/<today>_<slug>/ with a prefilled manifest.json
                   (refuses to reuse an existing directory)
  start RUN_DIR    mark a planned run as running and record the start time
  finish RUN_DIR   record the finish time and final status of a run

Only manifest.json is ever written; no other file in the run directory is
touched. Standard library only (Python 3.8+).

Examples
  python3 new_run.py create deg6-sweep --purpose "Screen family F" \
      --strategy S3 --claims R4 R7 --hash code/sweep.py --packages numpy
  python3 new_run.py start runs/2026-11-06_deg6-sweep
  python3 new_run.py finish runs/2026-11-06_deg6-sweep --status completed \
      --summary "Screen: 0 hits, 312 units unresolved"
"""

import argparse
import datetime
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

STATUSES = ("planned", "running", "completed", "failed", "interrupted")
FINAL_STATUSES = ("completed", "failed", "interrupted")
TIERS = ("NUMERICAL", "CERTIFIED")
MANIFEST = "manifest.json"


def now_iso():
    """Local time with UTC offset, to the second (ISO 8601)."""
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")


def slugify(text):
    slug = re.sub(r"[^a-z0-9._-]+", "-", text.strip().lower()).strip("-.")
    if not slug:
        raise SystemExit("error: the slug is empty after normalisation; use letters, digits, '-', '_' or '.'")
    return slug


def run_git(args, cwd):
    try:
        res = subprocess.run(["git", "-C", str(cwd)] + args, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    return res if res.returncode == 0 else None


def git_info(path):
    """Commit and dirty flag of the repository containing `path`, or None outside a repository."""
    top = run_git(["rev-parse", "--show-toplevel"], path)
    if top is None:
        return None
    head = run_git(["rev-parse", "HEAD"], path)  # fails in a repository with no commits yet
    status = run_git(["status", "--porcelain", "--untracked-files=no"], path)
    return {
        "repository": top.stdout.strip(),
        "git_commit": head.stdout.strip() if head else None,
        "dirty": bool(status.stdout.strip()) if status else None,
    }


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def package_versions(names):
    try:
        from importlib import metadata
    except ImportError:  # Python < 3.8
        return {n: "unknown (importlib.metadata unavailable)" for n in names}
    out = {}
    for name in names:
        try:
            out[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            out[name] = "not installed in this interpreter"
    return out


def parse_param(item):
    if "=" not in item:
        raise SystemExit(f"error: --param expects KEY=VALUE, got {item!r}")
    key, value = item.split("=", 1)
    try:
        return key, json.loads(value)
    except json.JSONDecodeError:
        return key, value


def write_json_atomic(path, data, exclusive=False):
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if exclusive:
        with open(path, "x", encoding="utf-8") as fh:
            fh.write(text)
        return
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


def load_manifest(run_dir):
    path = Path(run_dir) / MANIFEST
    if not path.is_file():
        raise SystemExit(f"error: no {MANIFEST} in {run_dir}")
    with open(path, encoding="utf-8") as fh:
        return path, json.load(fh)


def append_note(manifest, note):
    stamped = f"[{now_iso()}] {note}"
    existing = manifest.get("notes") or ""
    manifest["notes"] = (existing + "\n" + stamped).strip() if existing else stamped


def cmd_create(args):
    root = Path(args.root)
    date = datetime.date.today().isoformat()
    run_id = f"{date}_{slugify(args.slug)}"
    run_dir = root / run_id
    if run_dir.exists():
        raise SystemExit(
            f"error: {run_dir} already exists. Finished runs are evidence and are never reused; "
            "choose a different slug (for example add -v2 or a short description of what changed)."
        )
    for f in args.hash:
        if not Path(f).is_file():
            raise SystemExit(f"error: --hash file not found: {f}")
    if args.status not in ("planned", "running"):
        raise SystemExit("error: a new run starts as 'planned' or 'running'")

    git = git_info(Path(args.repo) if args.repo else Path.cwd())
    created = now_iso()
    manifest = {
        "run_id": run_id,
        "created": created,
        "purpose": args.purpose,
        "question": args.question,
        "strategy": args.strategy,
        "claim_ids": args.claims,
        "command": args.command,
        "code_version": {
            "repository": git["repository"] if git else None,
            "git_commit": git["git_commit"] if git else None,
            "dirty": git["dirty"] if git else None,
            "file_sha256": {f: sha256(f) for f in args.hash},
        },
        "environment": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "packages": package_versions(args.packages),
            "external_software": {},
            "machine": {
                "platform": platform.platform(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "cpu_count": os.cpu_count(),
                "hostname": platform.node() if args.record_hostname else None,
            },
        },
        "parameters": dict(parse_param(p) for p in args.param),
        "seeds": args.seed,
        "started": created if args.status == "running" else None,
        "finished": None,
        "status": args.status,
        "evidence_tier": args.tier,
        "certificate": {"method": None, "checker": None, "location": None},
        "outputs": [],
        "result_summary": "",
        "accounting": [],
        "notes": "",
    }
    if git is None:
        append_note(manifest, "Not inside a git repository: record code versions with --hash.")
    elif git["git_commit"] is None:
        append_note(manifest, "Repository has no commits yet: code version is identified by file hashes only.")
    elif git["dirty"]:
        append_note(manifest, "Working tree had uncommitted changes to tracked files when the run was created.")

    run_dir.mkdir(parents=True, exist_ok=False)
    write_json_atomic(run_dir / MANIFEST, manifest, exclusive=True)
    print(run_dir)


def cmd_start(args):
    path, manifest = load_manifest(args.run_dir)
    if manifest.get("status") != "planned" and not args.force:
        raise SystemExit(f"error: run status is {manifest.get('status')!r}, not 'planned' (use --force to override)")
    manifest["status"] = "running"
    manifest["started"] = now_iso()
    if args.note:
        append_note(manifest, args.note)
    write_json_atomic(path, manifest)
    print(f"{args.run_dir}: running")


def cmd_finish(args):
    path, manifest = load_manifest(args.run_dir)
    if manifest.get("status") in FINAL_STATUSES and not args.force:
        raise SystemExit(
            f"error: run already finished with status {manifest.get('status')!r}. Finished runs are evidence; "
            "to record a later problem use --note with --force, and make a new run."
        )
    if args.summary and manifest.get("result_summary") and not args.force:
        raise SystemExit("error: result_summary is already set (use --force to replace it)")
    manifest["status"] = args.status
    manifest["finished"] = now_iso()
    if manifest.get("started") is None:
        append_note(manifest, "Start time was not recorded (run was never marked as running).")
    if args.summary:
        manifest["result_summary"] = args.summary
    if args.tier:
        manifest["evidence_tier"] = args.tier
    if args.note:
        append_note(manifest, args.note)
    write_json_atomic(path, manifest)
    print(f"{args.run_dir}: {args.status}")


def build_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        epilog="Run '<subcommand> --help' for the options of each subcommand.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create", help="create a new run directory with manifest.json")
    c.add_argument("slug", help="short name for the run, e.g. deg6-pencil-sweep")
    c.add_argument("--root", default="runs", help="directory holding all runs (default: ./runs)")
    c.add_argument("--purpose", default="", help="why this run exists, one sentence")
    c.add_argument("--question", default="", help="the question it answers and what each outcome will mean")
    c.add_argument("--strategy", default="", help="strategy id from STRATEGIES.md, e.g. S3")
    c.add_argument("--claims", nargs="*", default=[], metavar="RID", help="Results-register ids, e.g. R4 R7")
    c.add_argument("--command", default="", help="the exact command that performs the run")
    c.add_argument("--hash", nargs="*", default=[], metavar="FILE", help="code or data files to fingerprint with SHA-256")
    c.add_argument("--packages", nargs="*", default=[], metavar="NAME", help="Python packages whose versions to record")
    c.add_argument("--param", action="append", default=[], metavar="KEY=VALUE", help="parameter (VALUE parsed as JSON if possible); repeatable")
    c.add_argument("--seed", action="append", default=[], type=int, metavar="N", help="random seed; repeatable")
    c.add_argument("--tier", choices=TIERS, default="NUMERICAL", help="evidence tier the run aims for (default NUMERICAL)")
    c.add_argument("--status", choices=("planned", "running"), default="planned", help="initial status (default planned)")
    c.add_argument("--repo", default=None, help="path inside the git repository to describe (default: current directory)")
    c.add_argument("--record-hostname", action="store_true", help="also record the machine's hostname")
    c.set_defaults(func=cmd_create)

    s = sub.add_parser("start", help="mark a planned run as running")
    s.add_argument("run_dir")
    s.add_argument("--note", default="", help="note to append, e.g. how to resume")
    s.add_argument("--force", action="store_true", help="allow when status is not 'planned'")
    s.set_defaults(func=cmd_start)

    f = sub.add_parser("finish", help="record finish time and final status")
    f.add_argument("run_dir")
    f.add_argument("--status", choices=FINAL_STATUSES, required=True)
    f.add_argument("--summary", default="", help="result summary, stated at the evidence tier actually reached")
    f.add_argument("--tier", choices=TIERS, default=None, help="evidence tier actually reached, if different")
    f.add_argument("--note", default="", help="note to append (failures, overlaps, how to resume)")
    f.add_argument("--force", action="store_true", help="allow changing an already finished run (leave a --note saying why)")
    f.set_defaults(func=cmd_finish)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
