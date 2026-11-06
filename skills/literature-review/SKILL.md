---
name: literature-review
description: Systematic literature search and citation verification for mathematical research. Finds prior work, records exact statements with their hypotheses and theorem numbers, checks that every reference exists and says what is claimed, compares preprint and published versions, and maintains LITERATURE_REVIEW.md and refs.bib. Use this whenever starting work on a new problem, before claiming that a result is new, whenever a theorem is cited or quoted from memory, when an argument depends on a known result whose hypotheses need checking, when building or cleaning a bibliography, or when the user asks "what is known about…", "has anyone proved…", "find references for…" or "is this new?". Use it even for a single citation, because unverified or misremembered references are one of the commonest sources of error in agent-assisted mathematics.
---

# Literature review

Find out what is already known, record it precisely enough that an argument can
safely rest on it, and make every citation checkable. In mathematics a
reference is only useful if the exact statement, its hypotheses and its
conventions are right: a theorem quoted without its hypotheses, from the wrong
version, or from memory, silently turns a proof into a conjecture.

Follow the claim-status labels of the `math-research-core` skill (a literature
result is `CITED` only once it has been checked against the source) and the
workspace layout of the `research-workspace` skill.

## When to use

- At the start of a project, before any strategy is chosen: the literature
  decides what is already known, what is known to be impossible, and which
  techniques exist.
- Before writing "new", "first", "to our knowledge" or "open" about anything.
- Whenever a proof step cites a result. Check that the result exists, that the
  numbering matches the version read, and that its hypotheses hold in our
  setting.
- When a strategy borrows a technique from another setting (the "limits of
  analogy" check).
- When preparing a bibliography for a paper (`paper-writing` relies on the
  entries produced here).
- When a citation came from memory, from a survey, from a talk, or from an
  agent's own recall. Treat all of these as leads to check, not as facts.

## Reads and writes

| File | Use |
|---|---|
| `PROJECT_SUMMARY.md` | Read the problem statement and acceptance criterion to fix the scope. Add `CITED` claims to the Results register once they are checked. |
| `LITERATURE_REVIEW.md` | Main output. Start from `templates/LITERATURE_REVIEW.md`. |
| `refs.bib` | One BibTeX entry per source, with identifiers (`doi`, `eprint` + `archiveprefix`). Checked with `scripts/check_bib.py`. |
| `STRATEGIES.md` | Read it so the search covers each strategy's key ingredients. Report known obstructions back to it. |
| `HANDOFF.md` | Add a row to the Corrections table whenever an earlier citation turns out to be wrong. |
| `LOG.md` | Add a dated line per search session: what was searched and what changed. |

## Procedure

### 1. Fix the question and its vocabulary

Write the question as a precise mathematical statement. Then list:

- **synonyms and variant names** for the main objects. Different communities
  often name the same object differently, and older literature uses older
  names.
- **notation variants**, for example a quantity normalised differently or a
  dual formulation.
- **MSC codes**, taken from two or three key papers.
- **neighbouring settings** where the same question has been asked (over
  another field, in another dimension, for a discrete analogue).

This list drives the search. A search that uses one name only is the most
common reason for missing directly relevant work.

### 2. Search in rounds and log every round

Run the search in rounds and record each in the search log of
`LITERATURE_REVIEW.md` (date, source, query, number of hits scanned, new
relevant items). A logged search can be extended, repeated by someone else,
and cited when making a novelty claim. An unlogged search can only be redone.

1. **Seed:** surveys, books, lecture notes and the most recent papers on the
   topic. Recent papers give the current state and cite the important older
   work.
2. **Databases:** run each vocabulary variant through at least two general
   databases (for example zbMATH Open and arXiv, plus MathSciNet if the user
   has access).
3. **Citation chasing:** go backwards through the reference lists of the core
   papers and forwards through "cited by". Forward chasing is how you find
   improvements, corrections, counterexamples and errata. Never skip it for a
   result the project depends on.
4. **Specialist sources:** MathOverflow for folklore and known
   counterexamples, OEIS for integer sequences produced by small cases, and
   field databases (LMFDB, the Stacks Project, graph and knot databases and so
   on) for data and canonical statements.

See `references/sources.md` for what each source is good for, and for the
stopping rule.

### 3. Triage

For each candidate, read the title, abstract and the statements of the main
results, then decide: core (read in full), relevant (record the main
statement), background (citation only) or irrelevant (log only). Keep the
core set small enough to actually read.

### 4. Record each relevant result precisely

Use `templates/entry.md` for every core or relevant source:

- **Full citation and identifiers:** arXiv id with the version read, DOI of
  the published version, and MR/zbMATH numbers if available.
- **The statement, quoted exactly**, with the theorem number *in the version
  you read*. Paraphrases drop hypotheses. Quote first, then paraphrase if
  needed.
- **Every hypothesis made explicit**, including the ones stated once at the
  start of a section ("throughout, X is smooth and projective over ℂ").
  Standing assumptions are where most misapplications come from.
- **Conventions** that differ from ours: normalisations, sign conventions,
  what "degree" or "genus" means, affine or projective, real or complex.
- **How it was verified** (see step 5).
- **Applicability:** take each hypothesis in turn and say whether it holds in
  our setting, and why.

### 5. Verify, and label honestly

Record a verification level for each entry:

| Level | Meaning | Allowed status if used in an argument |
|---|---|---|
| full text | Statement and hypotheses read in the source itself, version recorded | `CITED` |
| abstract only | Only the abstract or summary was read | lead only |
| secondary source | Taken from a survey, review, talk, MathOverflow answer or another paper's citation | lead only |
| not verified | From memory or unsourced | lead only |

A lead is not a result. If an argument needs a result that is only a lead, the
argument is at most `PROVED-MODULO` with a gap such as:

`GAP-3: check that [Key20, Thm 4.2] holds for singular X; only the abstract has been read.`

Then either verify the lead (read the full text) or ask the user to obtain it.
Do not get round a paywall by unofficial means; if no legitimate copy is
available, say so and leave the gap open.

### 6. Compare versions and look for corrections

For every result the project depends on:

- Check the arXiv version history. The statement, the hypotheses or the
  numbering may differ between versions and the published paper. Record which
  version was read, and any differences found.
- Look for errata, corrigenda, retractions and later papers that correct or
  refute the result: forward citations, the MathSciNet/zbMATH review, the
  author's homepage, and a search for the title together with "erratum" or
  "corrigendum".
- If the preprint and the published version state different results, cite the
  one you read and checked, and say so in the entry. The stronger statement is
  not automatically the right one.

### 7. Synthesise

Fill in the sections of `LITERATURE_REVIEW.md`:

- what is known to exist or hold
- known restrictions and obstructions
- techniques
- limits of analogies
- gaps
- open questions

Write the synthesis around the project's question, not paper by paper. The two
sections that save the most effort later are:

- **Known restrictions and obstructions:** results showing that something is
  impossible or that a technique cannot go beyond a certain point. Pass these
  to `STRATEGIES.md` so that no strategy collides with them unawares.
- **Limits of analogies:** for each technique borrowed from a neighbouring
  setting, which hypotheses of the original theorem fail or are unchecked
  here. Until those are checked, an analogy is `HEURISTIC` evidence.

### 8. Maintain `refs.bib` and run the checker

Give every entry its identifiers: `doi`, `eprint` with
`archiveprefix = {arXiv}`, and the arXiv version in `note` or `eprint` if a
specific version is cited. Then run:

```
python3 scripts/check_bib.py refs.bib
```

The script checks that each DOI or arXiv identifier resolves to a record whose
title, first author and year match the entry. It reports `OK`, `MISMATCH`,
`NOT_FOUND` or `UNCHECKED`, and it reports a newer arXiv version than the one
cited. Fix every `MISMATCH` and `NOT_FOUND` entry. Resolve each `UNCHECKED`
entry by hand (books and older papers often have no DOI; use the MR or zbMATH
number instead).

`OK` only means that the identifier and metadata agree. It says nothing about
whether the cited theorem exists or says what we claim; only step 5 checks
that. Use `--offline` to see which entries have identifiers when there is no
network.

### 9. Novelty claims

Never write "this is new". Write what the search supports: "we could not find
this in the literature; searches are logged in LITERATURE_REVIEW.md §1".
Record the search in the log so the claim can be audited, and flag it to the
user, because only an expert in the field can really confirm novelty.

## Rules, and why

- **No citation from memory goes into an argument or a paper unverified.**
  Recalled references are often a mix of two papers, have the wrong theorem
  number, or do not exist. The cost of checking is minutes; the cost of an
  invented reference is the credibility of the whole document.
- **Quote before paraphrasing.** The hypotheses are in the exact wording. A
  paraphrase made early tends to lose them, and everything built on it inherits
  the loss.
- **Record the version.** Numbering and even statements change between arXiv
  versions and the published paper. "Theorem 3.1" means nothing without a
  version.
- **Separate what a paper proves from what it says.** Introductions,
  remarks, "it is well known that…" and announced results are not proved
  theorems. Note which is which. Folklore without a reference is labelled as
  folklore, not as `CITED`.
- **Trace secondary sources to the primary one.** Surveys simplify statements
  and sometimes drop hypotheses or mix several results.
- **Applicability is a separate check from correctness.** A correct theorem
  applied outside its hypotheses proves nothing. Check each hypothesis
  against the project's setting explicitly, in writing.
- **Corrections are recorded, not overwritten.** When a citation turns out to
  be wrong, fix the entry, keep a note of the earlier version, and add a row to
  the Corrections table in `HANDOFF.md`, so that anything built on the earlier
  version can be found and re-checked.

## Common failure modes

- **Stronger preprint statement.** An unrevised preprint states a stronger
  result than the published version (or the other way round), and the project
  quotes the version that suits it. Compare the versions; cite what was
  checked.
- **Dropped standing assumptions.** A result proved over ℂ, for smooth
  objects, for generic parameters or in characteristic zero is applied over ℝ,
  to singular objects, to all parameters or in positive characteristic.
- **Convention mismatch.** A bound or formula is off by a normalisation, a
  sign or an index shift because "degree", "genus", "dimension" or a constant
  is defined differently.
- **Conflated references.** Two papers by the same authors, or with similar
  titles, are merged into one citation.
- **Missed corrections.** A result was later corrected, weakened or refuted,
  and only forward citation chasing would have shown it.
- **Single-vocabulary search.** The problem is studied under another name in
  another community, or in older literature, and was missed.
- **Analogy treated as a theorem.** A technique that works in a neighbouring
  setting is assumed to work here, although one of its key hypotheses (for
  example a non-degeneracy condition) fails on part of our configuration.
- **"Known" without a source.** A step relies on a "standard fact" that nobody
  can locate. Either find it, prove it, or mark it with a GAP.
- **Endless search.** No stopping rule, so the search never finishes; or the
  search stops after one database. Use the stopping rule in
  `references/sources.md`.

## Bundled files

- `references/sources.md`: read when planning or extending a search. It covers
  what each database and specialist resource is good for, search tactics, the
  stopping rule, and how to check a reference and find errata.
- `templates/LITERATURE_REVIEW.md`: copy to the project root at the first
  search session.
- `templates/entry.md`: copy for each core or relevant source.
- `scripts/check_bib.py`: run on `refs.bib` after adding entries and before
  circulating anything. `python3 scripts/check_bib.py --help` lists the
  options: `--offline`, `--json`, `--strict`, `--delay`, `--mailto`.
