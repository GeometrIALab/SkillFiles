#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 GeometrIA Lab, CBG
# SPDX-License-Identifier: MIT
"""Create a mathematical research workspace with the standard layout.

Creates the standard files and folders described in the research-workspace skill:

  PROJECT_SUMMARY.md  HANDOFF.md  LOG.md  LITERATURE_REVIEW.md  refs.bib
  STRATEGIES.md  PROOF_PROGRESS.md
  runs/  probes/  code/  paper/  archive/   (and formal/ with --formal)

The templates for LITERATURE_REVIEW.md, STRATEGIES.md and PROOF_PROGRESS.md are taken
from the sibling skills (literature-review, strategy-planning, proof-development) when
they are installed in the same skills folder; otherwise a minimal stub is written.

The tokens {{TITLE}} and {{DATE}} in templates are replaced. Existing files are never
overwritten: they are reported and skipped.

Examples:
  python3 init_workspace.py ~/research/hessian-ovals --title "Hessian curves with many ovals"
  python3 init_workspace.py . --title "Bounds for X" --formal --dry-run
"""

from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PACK_DIR = SKILL_DIR.parent

# target file -> (template path, fallback heading)
TEMPLATES: dict[str, tuple[Path, str]] = {
    "PROJECT_SUMMARY.md": (SKILL_DIR / "templates" / "PROJECT_SUMMARY.md", "{{TITLE}}"),
    "HANDOFF.md": (SKILL_DIR / "templates" / "HANDOFF.md", "Handoff: {{TITLE}}"),
    "LOG.md": (SKILL_DIR / "templates" / "LOG.md", "Log: {{TITLE}}"),
    "LITERATURE_REVIEW.md": (
        PACK_DIR / "literature-review" / "templates" / "LITERATURE_REVIEW.md",
        "Literature review: {{TITLE}}",
    ),
    "STRATEGIES.md": (
        PACK_DIR / "strategy-planning" / "templates" / "STRATEGIES.md",
        "Strategies: {{TITLE}}",
    ),
    "PROOF_PROGRESS.md": (
        PACK_DIR / "proof-development" / "templates" / "PROOF_PROGRESS.md",
        "Proof progress: {{TITLE}}",
    ),
}

DIRS = ["runs", "probes", "code", "paper", "archive"]

EXTRA_FILES = {
    "refs.bib": "% Bibliography for {{TITLE}}.\n"
    "% Add only entries whose statements have been checked against the source\n"
    "% (see the literature-review skill).\n",
    "probes/README.md": "# Probes\n\n"
    "Throwaway exploratory scripts. One line per probe: date, file, question, outcome.\n"
    "Anything cited as evidence must be redone as a recorded run in runs/.\n\n"
    "| Date | File | Question | Outcome |\n|---|---|---|---|\n",
    "runs/README.md": "# Runs\n\n"
    "One directory per recorded computation, named YYYY-MM-DD_<slug>, each with a\n"
    "manifest.json (see the computational-experiments skill). Runs are write-once:\n"
    "never edit or delete an old run; make a new one.\n",
    "archive/README.md": "# Archive\n\n"
    "Superseded documents, named <NAME>_<YYYY-MM-DD>_<slug>.md. Kept for the record;\n"
    "do not edit.\n",
}


def fill(text: str, title: str, date: str) -> str:
    return text.replace("{{TITLE}}", title).replace("{{DATE}}", date)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("directory", help="project directory (created if missing)")
    parser.add_argument("--title", required=True, help="project title")
    parser.add_argument(
        "--date", default=_dt.date.today().isoformat(), help="ISO date (default: today)"
    )
    parser.add_argument(
        "--formal", action="store_true", help="also create formal/ for a proof-assistant project"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="print what would be created, change nothing"
    )
    args = parser.parse_args(argv)

    try:
        _dt.date.fromisoformat(args.date)
    except ValueError:
        parser.error(f"--date must be ISO 8601 (YYYY-MM-DD), got {args.date!r}")

    root = Path(args.directory).expanduser().resolve()
    created: list[str] = []
    skipped: list[str] = []
    stubbed: list[str] = []

    def write(rel: str, content: str) -> None:
        path = root / rel
        if path.exists():
            skipped.append(rel)
            return
        created.append(rel)
        if not args.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    if not args.dry_run:
        root.mkdir(parents=True, exist_ok=True)

    dirs = DIRS + (["formal"] if args.formal else [])
    for d in dirs:
        path = root / d
        if path.exists():
            skipped.append(d + "/")
        else:
            created.append(d + "/")
            if not args.dry_run:
                path.mkdir(parents=True)

    for name, (template, heading) in TEMPLATES.items():
        if template.is_file():
            content = template.read_text(encoding="utf-8")
        else:
            if not (root / name).exists():
                stubbed.append(name)
            content = f"# {heading}\n\n_Last updated: {{{{DATE}}}}_\n"
        write(name, fill(content, args.title, args.date))

    for rel, content in EXTRA_FILES.items():
        write(rel, fill(content, args.title, args.date))

    prefix = "Would create" if args.dry_run else "Created"
    print(f"Workspace: {root}")
    for rel in created:
        print(f"  {prefix}: {rel}")
    for rel in skipped:
        print(f"  Exists, left unchanged: {rel}")
    if stubbed:
        print(
            "  Minimal stub used (sibling skill template not found): " + ", ".join(stubbed)
        )
    if not args.dry_run:
        print("Next: fill in the problem and acceptance criterion in PROJECT_SUMMARY.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
