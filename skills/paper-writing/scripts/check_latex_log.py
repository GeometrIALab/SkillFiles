#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 GeometrIA Lab, CBG
# SPDX-License-Identifier: MIT
"""Check a LaTeX .log file for problems that should block circulation.

Errors (cause a non-zero exit status):
  * TeX errors (lines beginning with "! ")
  * undefined references and undefined citations
  * multiply-defined labels
  * missing files (packages, \\input files, graphics)
  * cleveref reference formats that are undefined (these print "??")

Warnings (reported; cause a non-zero exit only with --strict):
  * overfull boxes wider than the threshold (default 1pt)
  * requests to rerun LaTeX or BibTeX (cross-references may be stale)
  * missing .bbl file (BibTeX has not been run)

The log is only read; nothing is modified. Python 3 standard library only.

Exit status: 0 = no blocking problems; 1 = problems found; 2 = log unreadable.

Examples:
  python3 check_latex_log.py paper/main.log
  python3 check_latex_log.py main.log --overfull-threshold 5 --strict
  python3 check_latex_log.py main.log --json > log_report.json
"""

import argparse
import json
import re
import sys
from collections import OrderedDict

RE_UNDEF_REF = re.compile(
    r"Reference [`'](?P<key>[^`']+)' on page \S+ undefined(?: on input line (?P<line>\d+))?")
RE_UNDEF_CITE = re.compile(
    r"Citation [`'](?P<key>[^`']+)' on page \S+ undefined(?: on input line (?P<line>\d+))?")
RE_MULTI_LABEL = re.compile(r"Label [`'](?P<key>[^`']+)' multiply defined")
RE_MISSING_FILE = re.compile(r"File [`'](?P<key>[^`']+)' not found")
RE_CREF_FORMAT = re.compile(
    r"cref reference format for label type [`'](?P<key>[^`']*)' undefined"
    r"(?: on input line (?P<line>\d+))?")
RE_OVERFULL = re.compile(
    r"Overfull \\(?P<box>[hv]box) \((?P<amount>[0-9.]+)pt too (?:wide|high)\)(?P<rest>.*)")
RE_LINES = re.compile(r"lines? (\d+)(?:--(\d+))?")
RE_TEX_LINE = re.compile(r"^l\.(\d+)")
RE_NO_BBL = re.compile(r"^No file (?P<key>\S+\.bbl)\.")
# Phrases LaTeX and common packages use to ask for another run. Package
# identification lines ("Package: rerunfilecheck ... Rerun checks ...") are
# excluded separately.
RE_RERUN = re.compile(r"Rerun to get|Rerun LaTeX|Please \(re\)run|rerun LaTeX")
SUMMARY_UNDEF_REFS = "There were undefined references"
SUMMARY_UNDEF_CITES = "There were undefined citations"
SUMMARY_MULTI = "There were multiply-defined labels"


def unwrap(lines, width):
    """Rejoin log lines that TeX broke at max_print_line characters."""
    if width <= 0:
        return lines
    out, buf = [], ""
    for line in lines:
        buf += line
        if len(line) == width:
            continue  # TeX wrapped this line; the next one continues it
        out.append(buf)
        buf = ""
    if buf:
        out.append(buf)
    return out


class Report:
    def __init__(self):
        # (category, key) -> list of line numbers (as strings, may be empty)
        self.errors = OrderedDict()
        self.warnings = OrderedDict()

    def add(self, bucket, category, key, line=None):
        entry = bucket.setdefault((category, key), [])
        if line and line not in entry:
            entry.append(line)

    def error(self, category, key, line=None):
        self.add(self.errors, category, key, line)

    def warn(self, category, key, line=None):
        self.add(self.warnings, category, key, line)


def parse(text, overfull_threshold, width):
    lines = unwrap(text.splitlines(), width)
    rep = Report()
    saw_summary = {"ref": False, "cite": False, "multi": False}

    for i, line in enumerate(lines):
        stripped = line.strip()

        # TeX errors and missing files.
        if line.startswith("! "):
            tex_line = None
            for look in lines[i + 1:i + 12]:
                m = RE_TEX_LINE.match(look)
                if m:
                    tex_line = m.group(1)
                    break
            m = RE_MISSING_FILE.search(line)
            if m:
                rep.error("missing file", m.group("key"), tex_line)
            else:
                rep.error("TeX error", line[2:].strip(), tex_line)
            continue

        m = RE_UNDEF_REF.search(line)
        if m:
            rep.error("undefined reference", m.group("key"), m.group("line"))
            continue
        m = RE_UNDEF_CITE.search(line)
        if m:
            rep.error("undefined citation", m.group("key"), m.group("line"))
            continue
        m = RE_MULTI_LABEL.search(line)
        if m:
            rep.error("multiply-defined label", m.group("key"))
            continue
        m = RE_CREF_FORMAT.search(line)
        if m:
            rep.error("cleveref format undefined (prints ??; add \\crefname)",
                      m.group("key") or "(empty type)", m.group("line"))
            continue
        m = RE_MISSING_FILE.search(line)
        if m and "Warning" in line:
            rep.error("missing file", m.group("key"))
            continue

        m = RE_OVERFULL.search(line)
        if m:
            amount = float(m.group("amount"))
            if amount > overfull_threshold:
                lm = RE_LINES.search(m.group("rest"))
                where = None
                if lm:
                    where = lm.group(1) + ("--" + lm.group(2) if lm.group(2) else "")
                rep.warn("overfull " + m.group("box"),
                         "%.1fpt too %s" % (amount, "wide" if m.group("box") == "hbox" else "high"),
                         where)
            continue

        m = RE_NO_BBL.match(stripped)
        if m:
            rep.warn("missing bibliography", m.group("key") + " (run BibTeX, then LaTeX twice)")
            continue

        if SUMMARY_UNDEF_REFS in line:
            saw_summary["ref"] = True
        if SUMMARY_UNDEF_CITES in line:
            saw_summary["cite"] = True
        if SUMMARY_MULTI in line:
            saw_summary["multi"] = True

        if RE_RERUN.search(line) and not stripped.startswith("Package:"):
            msg = re.sub(r"^\([A-Za-z]+\)\s*", "", stripped)  # "(pkg)   ..." continuation
            msg = re.sub(r"^(LaTeX|Package \S+) Warning:\s*", "", msg)
            rep.warn("rerun requested", msg)

    # Fall back on LaTeX's end-of-run summaries if the details were not parsed
    # (for example because of unusual line wrapping).
    cats = {c for (c, _) in rep.errors}
    if saw_summary["ref"] and "undefined reference" not in cats:
        rep.error("undefined reference", "(reported by LaTeX; details not parsed)")
    if saw_summary["cite"] and "undefined citation" not in cats:
        rep.error("undefined citation", "(reported by LaTeX; details not parsed)")
    if saw_summary["multi"] and "multiply-defined label" not in cats:
        rep.error("multiply-defined label", "(reported by LaTeX; details not parsed)")
    return rep


def fmt_lines(lines):
    if not lines:
        return ""
    label = "line" if len(lines) == 1 and "--" not in lines[0] else "lines"
    return "%s %s" % (label, ", ".join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Check a LaTeX .log for undefined references/citations, "
                    "multiply-defined labels, missing files, TeX errors, overfull "
                    "boxes and rerun requests.",
        epilog="Exit status: 0 = no blocking problems, 1 = problems found, "
               "2 = log unreadable.")
    ap.add_argument("log", help="path to the .log file produced by LaTeX")
    ap.add_argument("--overfull-threshold", type=float, default=1.0, metavar="PT",
                    help="report overfull boxes wider than PT points (default 1.0)")
    ap.add_argument("--strict", action="store_true",
                    help="also exit non-zero on warnings (overfull boxes, rerun "
                         "requests, missing .bbl)")
    ap.add_argument("--json", action="store_true", help="print a JSON report")
    ap.add_argument("--max-print-line", type=int, default=79, metavar="N",
                    help="TeX's log line width, used to rejoin wrapped lines "
                         "(default 79; 0 disables rejoining)")
    args = ap.parse_args(argv)

    try:
        with open(args.log, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        print("check_latex_log: cannot read %s: %s" % (args.log, exc), file=sys.stderr)
        return 2

    rep = parse(text, args.overfull_threshold, args.max_print_line)
    rerun = any(c == "rerun requested" for (c, _) in rep.warnings)
    failed = bool(rep.errors) or (args.strict and bool(rep.warnings))

    if args.json:
        out = {
            "log": args.log,
            "ok": not failed,
            "errors": [{"kind": c, "detail": k, "lines": v} for (c, k), v in rep.errors.items()],
            "warnings": [{"kind": c, "detail": k, "lines": v} for (c, k), v in rep.warnings.items()],
            "rerun_requested": rerun,
        }
        print(json.dumps(out, indent=2))
        return 1 if failed else 0

    print("check_latex_log: %s" % args.log)
    print("ERRORS (%d)" % len(rep.errors))
    for (cat, key), lines in rep.errors.items():
        print("  %-28s %s  %s" % (cat, key, fmt_lines(lines)))
    print("WARNINGS (%d)" % len(rep.warnings))
    for (cat, key), lines in rep.warnings.items():
        print("  %-28s %s  %s" % (cat, key, fmt_lines(lines)))
    if rerun:
        print("Note: LaTeX asked for a rerun; undefined references may be stale. "
              "Recompile (and rerun BibTeX if citations changed) before trusting this report.")
    print("Result: %s (%d errors, %d warnings%s)" % (
        "FAIL" if failed else "OK", len(rep.errors), len(rep.warnings),
        ", strict" if args.strict else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
