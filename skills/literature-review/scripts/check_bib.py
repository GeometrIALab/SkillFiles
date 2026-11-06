#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 GeometrIA Lab, CBG
# SPDX-License-Identifier: MIT
"""Check that the DOIs and arXiv identifiers in a BibTeX file resolve to the
papers the entries claim to be.

For each entry with a DOI (doi field, or a doi.org URL) the Crossref REST API
is queried; for each entry with an arXiv identifier (eprint with
archiveprefix/eprinttype arXiv, an arxiv field, or an arxiv.org URL) the arXiv
API is queried. The record's title (normalised fuzzy match), first-author
surname and year are compared with the entry.

Statuses
  OK         every identifier resolved and the metadata matched
  MISMATCH   an identifier resolved but the title, first author or year differ
  NOT_FOUND  an identifier does not exist (or is malformed)
  UNCHECKED  no identifier, or the service could not be reached; check by hand

A network failure is always UNCHECKED, never OK. OK means only that the
identifier and the metadata agree: it does not check that a cited theorem
exists or says what is claimed. That needs the full text.

Exit codes: 0 if no entry is MISMATCH or NOT_FOUND (and, with --strict, none
is UNCHECKED); 1 otherwise; 2 on usage or parse errors.

Only the Python 3 standard library is used.
"""

import argparse
import difflib
import json
import re
import socket
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

USER_AGENT = "check_bib/1.0 (bibliography metadata checker; python-urllib)"
CROSSREF_URL = "https://api.crossref.org/works/{}"
ARXIV_URL = "https://export.arxiv.org/api/query?id_list={}"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

NEW_ARXIV_RE = re.compile(r"^(\d{4}\.\d{4,5})(v\d+)?$")
OLD_ARXIV_RE = re.compile(r"^([a-z\-]+)(\.[A-Z]{2})?/(\d{7})(v\d+)?$")
ARXIV_IN_TEXT_RE = re.compile(
    r"(?:arxiv\.org/(?:abs|pdf)/|arxiv:\s*)"
    r"([a-z\-]+(?:\.[A-Z]{2})?/\d{7}(?:v\d+)?|\d{4}\.\d{4,5}(?:v\d+)?)",
    re.IGNORECASE,
)
DOI_IN_TEXT_RE = re.compile(r"(?:doi\.org/|doi:\s*)(10\.\d{4,9}/\S+)", re.IGNORECASE)

SEVERITY = {"NOT_FOUND": 3, "MISMATCH": 2, "OK": 1, "UNCHECKED": 0}


# --------------------------------------------------------------------------
# BibTeX parsing (enough for real-world .bib files; not a full implementation)
# --------------------------------------------------------------------------

def _match_brace(s, i):
    """s[i] == '{'; return index of the matching '}' (or len(s)-1)."""
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2  # skip escaped character such as \{ or \}
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return len(s) - 1


def _parse_fields(body):
    fields = {}
    i, n = 0, len(body)
    while i < n:
        while i < n and body[i] in " \t\r\n,":
            i += 1
        if i >= n:
            break
        m = re.match(r"([A-Za-z0-9_\-:.+]+)\s*=\s*", body[i:])
        if not m:
            j = body.find(",", i)
            if j == -1:
                break
            i = j + 1
            continue
        name = m.group(1).lower()
        i += m.end()
        parts = []
        while i < n:
            c = body[i]
            if c == "{":
                j = _match_brace(body, i)
                parts.append(body[i + 1:j])
                i = j + 1
            elif c == '"':
                j, depth = i + 1, 0
                while j < n:
                    if body[j] == "{":
                        depth += 1
                    elif body[j] == "}":
                        depth -= 1
                    elif body[j] == '"' and depth == 0:
                        break
                    j += 1
                parts.append(body[i + 1:j])
                i = j + 1
            else:
                m2 = re.match(r"[^,#\s}]+", body[i:])
                if not m2:
                    i += 1
                    break
                parts.append(m2.group(0))
                i += m2.end()
            while i < n and body[i] in " \t\r\n":
                i += 1
            if i < n and body[i] == "#":
                i += 1
                while i < n and body[i] in " \t\r\n":
                    i += 1
                continue
            break
        fields[name] = "".join(parts).strip()
    return fields


def parse_bib(text):
    entries = []
    i = 0
    while True:
        at = text.find("@", i)
        if at == -1:
            break
        m = re.match(r"@\s*([A-Za-z]+)\s*([{(])", text[at:])
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        start = at + m.end()
        if m.group(2) == "{":
            end = _match_brace(text, at + m.end() - 1)
        else:
            depth, end = 0, len(text) - 1
            for j in range(start, len(text)):
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                elif text[j] == ")" and depth == 0:
                    end = j
                    break
        body = text[start:end]
        i = end + 1
        if etype in ("comment", "preamble", "string"):
            continue
        comma = body.find(",")
        if comma == -1:
            continue
        key = body[:comma].strip()
        fields = _parse_fields(body[comma + 1:])
        entries.append({"type": etype, "key": key, "fields": fields})
    return entries


# --------------------------------------------------------------------------
# Normalisation
# --------------------------------------------------------------------------

SPECIAL_LETTERS = {
    r"\ss": "ss", r"\o": "o", r"\O": "O", r"\ae": "ae", r"\AE": "AE",
    r"\oe": "oe", r"\OE": "OE", r"\aa": "a", r"\AA": "A", r"\l": "l",
    r"\L": "L", r"\i": "i", r"\j": "j",
}


def delatex(s):
    s = re.sub(r"\\([`'^\"~=.])\s*\{?\\?([A-Za-z])\}?", r"\2", s)
    s = re.sub(r"\\([uvHtcdbrk])(?:\s*\{\\?([A-Za-z])\}|\s+([A-Za-z]))",
               lambda m: m.group(2) or m.group(3), s)
    for cmd, rep in SPECIAL_LETTERS.items():
        s = re.sub(re.escape(cmd) + r"(?![A-Za-z])", rep, s)
    s = re.sub(r"\\[A-Za-z]+\*?", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)  # HTML/MathML tags in Crossref titles
    s = s.replace("{", "").replace("}", "").replace("$", " ").replace("~", " ")
    return s


def norm(s):
    s = unicodedata.normalize("NFKD", delatex(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^0-9a-zA-Z]+", " ", s).lower()
    return " ".join(s.split())


def title_score(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    ta, tb = set(a.split()), set(b.split())
    jaccard = len(ta & tb) / len(ta | tb)
    return max(ratio, jaccard)


def first_author(author_field):
    """Return (surname, full name) of the first author of a BibTeX author field."""
    if not author_field:
        return "", ""
    first = re.split(r"\s+and\s+", author_field.strip(), maxsplit=1)[0].strip()
    if "," in first:
        surname = first.split(",", 1)[0]
    else:
        braced = re.findall(r"\{([^{}]*)\}\s*$", first)
        surname = braced[0] if braced else first.split()[-1]
    return norm(surname), norm(first)


def author_matches(bib_author_field, remote_family, remote_full):
    surname, full = first_author(bib_author_field)
    if not surname:
        return None  # nothing to compare
    rf, rfull = norm(remote_family), norm(remote_full)
    padded = " " + (rfull or rf) + " "
    if (" " + surname + " ") in padded:
        return True
    if rf and (" " + rf + " ") in (" " + full + " "):
        return True
    # tolerate transliteration differences in a single surname
    return bool(rf) and difflib.SequenceMatcher(None, surname, rf).ratio() >= 0.85


def bib_year(fields):
    for k in ("year", "date"):
        m = re.search(r"\d{4}", fields.get(k, ""))
        if m:
            return int(m.group(0))
    return None


# --------------------------------------------------------------------------
# Identifier extraction
# --------------------------------------------------------------------------

def clean_doi(d):
    d = d.strip()
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", d, flags=re.IGNORECASE)
    return d.rstrip(".,;")


def normalise_arxiv(raw):
    """Return (base_id, version or None), or (None, None) if malformed."""
    s = raw.strip()
    s = re.sub(r"^(arxiv:\s*|https?://arxiv\.org/(abs|pdf)/)", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\.pdf$", "", s)
    m = NEW_ARXIV_RE.match(s)
    if m:
        return m.group(1), (int(m.group(2)[1:]) if m.group(2) else None)
    m = OLD_ARXIV_RE.match(s)
    if m:
        return "{}/{}".format(m.group(1), m.group(3)), (int(m.group(4)[1:]) if m.group(4) else None)
    return None, None


def identifiers(fields):
    dois, arxivs = [], []
    if fields.get("doi"):
        dois.append(clean_doi(fields["doi"]))
    prefix = (fields.get("archiveprefix") or fields.get("eprinttype") or "").lower()
    eprint = fields.get("eprint", "")
    if eprint and (prefix == "arxiv" or normalise_arxiv(eprint)[0]):
        arxivs.append(eprint)
    if fields.get("arxiv"):
        arxivs.append(fields["arxiv"])
    for k in ("url", "note", "howpublished", "journal"):
        v = fields.get(k, "")
        for m in ARXIV_IN_TEXT_RE.finditer(v):
            arxivs.append(m.group(1))
        for m in DOI_IN_TEXT_RE.finditer(v):
            dois.append(clean_doi(m.group(1)))
    # de-duplicate, keep order
    seen, d2, a2 = set(), [], []
    for d in dois:
        if d.lower() not in seen:
            seen.add(d.lower())
            d2.append(d)
    seen = set()
    for a in arxivs:
        if a not in seen:
            seen.add(a)
            a2.append(a)
    return d2, a2


# --------------------------------------------------------------------------
# Network
# --------------------------------------------------------------------------

class Fetcher:
    def __init__(self, delay, timeout, mailto=None):
        self.delay = delay
        self.timeout = timeout
        self.mailto = mailto
        self.last = 0.0

    def get(self, url):
        """Return (status, body). status: int HTTP code, or None on network failure."""
        attempts = 0
        while True:
            wait = self.delay - (time.monotonic() - self.last)
            if wait > 0:
                time.sleep(wait)
            ua = USER_AGENT + ("; mailto:" + self.mailto if self.mailto else "")
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            attempts += 1
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    body = r.read()
                    self.last = time.monotonic()
                    return r.status, body
            except urllib.error.HTTPError as e:
                self.last = time.monotonic()
                if e.code in (429, 500, 502, 503, 504) and attempts < 2:
                    time.sleep(max(self.delay, 1.0) * 3)
                    continue
                return e.code, b""
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as e:
                self.last = time.monotonic()
                if attempts < 2:
                    time.sleep(max(self.delay, 1.0))
                    continue
                return None, str(getattr(e, "reason", e)).encode()


def check_doi(doi, fields, fetcher, threshold):
    status, body = fetcher.get(CROSSREF_URL.format(urllib.parse.quote(doi, safe="/")))
    src = "doi " + doi
    if status is None:
        return "UNCHECKED", src, "network error: " + body.decode(errors="replace")
    if status == 404:
        return "NOT_FOUND", src, "Crossref has no record of this DOI"
    if status != 200:
        return "UNCHECKED", src, "Crossref returned HTTP {}".format(status)
    try:
        msg = json.loads(body.decode("utf-8"))["message"]
    except (ValueError, KeyError):
        return "UNCHECKED", src, "could not parse Crossref response"
    rtitle = " ".join((msg.get("title") or [""])[:1] + (msg.get("subtitle") or [])[:1])
    authors = msg.get("author") or []
    rfam = authors[0].get("family", authors[0].get("name", "")) if authors else ""
    rfull = (authors[0].get("given", "") + " " + rfam).strip() if authors else ""
    years = set()
    for k in ("issued", "published-print", "published-online", "published"):
        try:
            years.add(int(msg[k]["date-parts"][0][0]))
        except (KeyError, IndexError, TypeError, ValueError):
            pass
    return compare(fields, src, rtitle, rfam, rfull, years, threshold, year_tolerance=1)


def check_arxiv(raw, fields, fetcher, threshold):
    base, version = normalise_arxiv(raw)
    src = "arXiv " + raw.strip()
    if base is None:
        return "NOT_FOUND", src, "does not look like an arXiv identifier"
    status, body = fetcher.get(ARXIV_URL.format(urllib.parse.quote(base, safe="/")))
    if status is None:
        return "UNCHECKED", src, "network error: " + body.decode(errors="replace")
    if status != 200:
        return "UNCHECKED", src, "arXiv API returned HTTP {}".format(status)
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return "UNCHECKED", src, "could not parse arXiv response"
    entries = root.findall(ATOM + "entry")
    if not entries:
        return "NOT_FOUND", src, "arXiv returned no record"
    e = entries[0]
    eid = (e.findtext(ATOM + "id") or "").strip()
    rtitle = " ".join((e.findtext(ATOM + "title") or "").split())
    if "api/errors" in eid or not rtitle or rtitle.lower() == "error":
        summary = " ".join((e.findtext(ATOM + "summary") or "").split())
        return "NOT_FOUND", src, "arXiv API error: " + (summary or "no record")
    names = [a.findtext(ATOM + "name") or "" for a in e.findall(ATOM + "author")]
    rfull = names[0] if names else ""
    rfam = rfull.split()[-1] if rfull.split() else ""
    published = e.findtext(ATOM + "published") or ""
    v1_year = int(published[:4]) if published[:4].isdigit() else None
    st, src, detail = compare(fields, src, rtitle, rfam, rfull, set(), threshold, year_tolerance=None)
    notes = []
    m = re.search(r"v(\d+)$", eid)
    latest = int(m.group(1)) if m else None
    if version and latest and version < latest:
        notes.append("cites v{}, latest is v{}: check whether statements or numbering changed".format(version, latest))
    elif not version and latest and latest > 1:
        notes.append("no version cited; latest is v{}".format(latest))
    by = bib_year(fields)
    if by and v1_year and by < v1_year:
        notes.append("bib year {} is before arXiv v1 ({}); fine only if published before posting".format(by, v1_year))
    rdoi = (e.findtext(ARXIV_NS + "doi") or "").strip()
    if rdoi and not fields.get("doi"):
        notes.append("arXiv lists published DOI " + rdoi + ", which is not in the entry")
    jref = " ".join((e.findtext(ARXIV_NS + "journal_ref") or "").split())
    if jref and not fields.get("journal"):
        notes.append("journal-ref: " + jref)
    if notes:
        detail = detail + "; " + "; ".join(notes)
    return st, src, detail


def compare(fields, src, rtitle, rfam, rfull, ryears, threshold, year_tolerance):
    problems = []
    btitle = fields.get("title", "")
    if btitle:
        sc = title_score(btitle, rtitle)
        if sc < threshold:
            problems.append('title similarity {:.2f}: entry "{}" vs record "{}"'.format(
                sc, " ".join(delatex(btitle).split()), rtitle))
    else:
        problems.append("entry has no title to compare")
    am = author_matches(fields.get("author", "") or fields.get("editor", ""), rfam, rfull)
    if am is False:
        problems.append('first author: entry "{}" vs record "{}"'.format(
            first_author(fields.get("author", "") or fields.get("editor", ""))[1], rfull or rfam))
    by = bib_year(fields)
    if year_tolerance is not None and by and ryears:
        if not any(abs(by - y) <= year_tolerance for y in ryears):
            problems.append("year: entry {} vs record {}".format(by, sorted(ryears)))
    if problems:
        return "MISMATCH", src, "; ".join(problems)
    return "OK", src, "title/author/year match" if year_tolerance is not None else "title/author match"


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def overall(results):
    if not results:
        return "UNCHECKED"
    statuses = [r[0] for r in results]
    for s in ("NOT_FOUND", "MISMATCH"):
        if s in statuses:
            return s
    if "OK" in statuses:
        return "OK"
    return "UNCHECKED"


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Check DOIs and arXiv identifiers in a BibTeX file against Crossref and arXiv.",
        epilog="OK means the identifier resolves and metadata match; it does not check that a cited "
               "theorem exists or says what is claimed. Network failures are reported as UNCHECKED.")
    p.add_argument("bibfile", help="path to the .bib file")
    p.add_argument("--offline", action="store_true",
                   help="no network: list which entries have identifiers")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--strict", action="store_true", help="also fail (exit 1) if any entry is UNCHECKED")
    p.add_argument("--delay", type=float, default=3.0,
                   help="seconds between requests (default 3; the arXiv API asks for at least 3)")
    p.add_argument("--timeout", type=float, default=20.0, help="per-request timeout in seconds")
    p.add_argument("--title-threshold", type=float, default=0.8,
                   help="minimum normalised title similarity for a match (default 0.8)")
    p.add_argument("--mailto", default=None,
                   help="optional contact address sent to Crossref (only if you choose to; none by default)")
    p.add_argument("--key", action="append", help="check only this entry key (repeatable)")
    a = p.parse_args(argv)

    try:
        with open(a.bibfile, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as e:
        print("error: cannot read {}: {}".format(a.bibfile, e), file=sys.stderr)
        return 2
    entries = parse_bib(text)
    if a.key:
        entries = [e for e in entries if e["key"] in set(a.key)]
    if not entries:
        print("error: no BibTeX entries found", file=sys.stderr)
        return 2

    fetcher = Fetcher(a.delay, a.timeout, a.mailto)
    report = []
    for ent in entries:
        f = ent["fields"]
        dois, arxivs = identifiers(f)
        results = []
        if a.offline:
            ids = ["doi " + d for d in dois] + ["arXiv " + x for x in arxivs]
            detail = ("offline; identifiers: " + ", ".join(ids)) if ids else \
                "no DOI or arXiv identifier: verify by hand (MR/zbMATH number, publisher page)"
            report.append({"key": ent["key"], "status": "UNCHECKED", "checks": [], "detail": detail})
            continue
        for d in dois:
            results.append(check_doi(d, f, fetcher, a.title_threshold))
        for x in arxivs:
            results.append(check_arxiv(x, f, fetcher, a.title_threshold))
        if not results:
            detail = "no DOI or arXiv identifier: verify by hand (MR/zbMATH number, publisher page)"
        else:
            detail = " | ".join("{} [{}]: {}".format(s, src, d) for s, src, d in results)
        report.append({"key": ent["key"], "status": overall(results),
                       "checks": [{"status": s, "source": src, "detail": d} for s, src, d in results],
                       "detail": detail})
        if not a.json:
            r = report[-1]
            print("{:<10} {}  {}".format(r["status"], r["key"], r["detail"]), flush=True)

    counts = {}
    for r in report:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    if a.json:
        print(json.dumps({"entries": report, "counts": counts}, indent=2, ensure_ascii=False))
    else:
        if a.offline:
            for r in report:
                print("{:<10} {}  {}".format(r["status"], r["key"], r["detail"]))
        print()
        print("Summary: " + ", ".join("{} {}".format(k, counts[k]) for k in
                                     sorted(counts, key=lambda s: -SEVERITY[s])))
        print("Note: OK means identifier and metadata agree. Whether the cited result exists and says "
              "what is claimed must be checked in the full text.")
    bad = counts.get("MISMATCH", 0) + counts.get("NOT_FOUND", 0)
    if a.strict and not a.offline:
        bad += counts.get("UNCHECKED", 0)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
