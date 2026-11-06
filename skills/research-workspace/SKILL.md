---
name: research-workspace
description: Sets up and maintains a persistent, file-based workspace for a mathematical research project, so that work survives across sessions, context resets and handovers between agents and people. Defines the standard files (PROJECT_SUMMARY with its Results register, LITERATURE_REVIEW, STRATEGIES, PROOF_PROGRESS, HANDOFF, LOG, runs/, probes/, archive/), what belongs in each, and the protocols for starting, ending and handing over a session. Use it whenever you start a new research project or problem, or resume one ("where were we?", "carry on with the project"). Also use it when ending a work session, before a long task that may exhaust the context, when handing work to another agent or a colleague, or when the project's notes have become hard to navigate, even if the user does not mention files.
---

# Research workspace

An agent's memory ends with its context window. A research project lasts weeks or
months. The workspace is the project's memory: a fixed set of plain-text files that
any session, agent or person can read to find out exactly where things stand. The
names and roles are fixed on purpose. A fresh session can find what it needs without
searching, a reviewer knows where to look, and two projects can be compared at a
glance.

This skill uses the status labels and correction rules from `math-research-core`
(`PROVED`, `CERTIFIED`, `NUMERICAL`, `CONJECTURE`, …).

## Layout

```
<project>/
├── PROJECT_SUMMARY.md     problem, acceptance criterion, Results register, current state
├── HANDOFF.md             everything needed to resume from cold, including the Corrections table
├── LOG.md                 append-only dated session log
├── LITERATURE_REVIEW.md   what is known, with checked citations    (literature-review)
├── refs.bib               bibliography, checked entries only        (literature-review)
├── STRATEGIES.md          strategy cards and Closed directions      (strategy-planning)
├── PROOF_PROGRESS.md      statements, lemmas, proofs, gaps          (proof-development)
├── runs/                  one directory per recorded computation    (computational-experiments)
│   └── YYYY-MM-DD_<slug>/manifest.json
├── probes/                throwaway exploratory scripts, one line each in probes/README.md
├── code/                  maintained code that recorded runs depend on
├── formal/                proof-assistant project, if any           (lean-formalisation)
├── paper/                 manuscript sources                        (paper-writing)
└── archive/               superseded documents: <NAME>_<YYYY-MM-DD>_<slug>.md
```

`scripts/init_workspace.py` creates this layout and fills the templates (run it with
`--help`). If the script cannot be run, create the files by hand from the templates.

## What each file is for

| File | Kind | Contains | Update it when |
|---|---|---|---|
| `PROJECT_SUMMARY.md` | current state | Precise problem, acceptance criterion, conventions, the **Results register**, open gaps, a short state paragraph | A status changes; the target or the conventions change |
| `HANDOFF.md` | current state | Reading order, current state, next actions, open questions, what failed and why, recurring failure mechanisms, **Corrections**, reproduction, work accounting | At the end of every session, and before any risky long task |
| `LOG.md` | append-only | One dated entry per session: goal, what was done, status changes, next steps | During and at the end of every session |
| `LITERATURE_REVIEW.md` | current state | Checked statements from the literature, gaps | New sources are read |
| `STRATEGIES.md` | current state | Strategy cards `S1, S2, …` and the **Closed directions** table | A strategy is proposed, started, closed or succeeds |
| `PROOF_PROGRESS.md` | current state | Statements, lemma dependency graph, proofs, `GAP-n` markers, failed proof attempts | Proof work happens |
| `runs/…/` | write-once | Inputs, outputs, `manifest.json` | A computation starts or finishes. Never edit old runs. |

### One source of truth for each kind of information

- **Claim statuses** live only in the Results register in `PROJECT_SUMMARY.md`.
  Other files refer to claims by their ID (`R3`) instead of restating the status.
  When a status is copied into several places, the copies drift apart, and the
  summary ends up saying `PROVED` while the proof file says `PROVED-MODULO`.
- **Closed directions** live only in `STRATEGIES.md`.
- **Corrections** live only in `HANDOFF.md`.

### Conventions for the files

- Use ISO 8601 dates (`2026-03-14`) on every entry and on every section that can go
  stale.
- Write plain Markdown with mathematics in `$…$`, and use relative links between files,
  so the workspace reads well in any editor or repository viewer.
- Keep the current-state files short enough to read at the start of a session.
  `PROJECT_SUMMARY.md` should stay under about 200 lines; move detail into the specialist file and link to it.
  `HANDOFF.md` may be long but needs a contents list and a reading order.
- Rewrite current-state files so they stay accurate and readable. Before a substantial
  rewrite, copy the old version to `archive/<NAME>_<YYYY-MM-DD>_<slug>.md` and link
  to it from the top of the new one. `LOG.md` is only ever appended to. `runs/` is
  written once.
- Keep secrets (passwords, API keys, tokens) out of every workspace file. Workspaces
  get shared, synced and pushed to repositories. Record personal data about people only
  where the project needs it.

## Starting a session

1. Read `PROJECT_SUMMARY.md`: the problem, the acceptance criterion, the register.
2. Read `HANDOFF.md`: current state, next actions, open questions and the Corrections table.
3. Read the last two or three entries in `LOG.md`.
4. Read the Closed directions table in `STRATEGIES.md` **before** proposing any new
   line of attack.
5. Check for unfinished computations: any `runs/*/manifest.json` with status
   `running` or `interrupted`.
6. Tell the user, in a few lines, where things stand and what you propose to do in this
   session. Then go ahead unless they redirect you.

Skipping these steps causes the two most common kinds of wasted work: repeating a
direction that was already closed, and building on a claim that was later corrected.

If there is no workspace yet, initialise one (next section). If there are notes in some
other form, offer to migrate them into this layout. Keep the originals in `archive/`.

## Initialising a project

1. Create the layout, with `scripts/init_workspace.py <dir> --title "<title>"` or by hand.
2. Fill in `PROJECT_SUMMARY.md` first. Most importantly, write down the **acceptance
   criterion**: exactly what would count as solving the problem. For example, "an explicit
   example together with a `CERTIFIED` verification", or "a `PROVED` proof of the bound for all
   d ≥ 5". Confirm it with the mathematician, because it is their decision and every later
   judgement of success depends on it. Note any partial outcomes that would also be worth having.
3. Record conventions early: signs, normalisations, which variant of each definition
   is used, coordinates. Conflicting conventions are a major source of silent errors.
4. Continue with `literature-review`, then `strategy-planning`.

## During a session

- **Record as you go, not only at the end.** A session can end without warning, for example
  when the context runs out, a tool fails or the user stops it. Update the register as soon as a status
  changes, and add a line to `LOG.md` at each milestone.
- Put exploratory scripts in `probes/`, with one line each in `probes/README.md` (date,
  the question it addressed, the outcome). When a probe's result will be cited as
  evidence, redo the computation as a recorded run (see `computational-experiments`)
  and move any reusable code to `code/`.
- In long sessions, refresh the "Current state" and "Next actions" sections of
  `HANDOFF.md` from time to time, and always before starting something that may run for a long
  time or use up the context.
- Collect questions for the mathematician under "Open questions" in `HANDOFF.md`
  instead of scattering them through the files.

## Ending a session

1. Bring the Results register up to date: statuses, review, evidence links and dates.
2. Append an entry to `LOG.md` using the format in `templates/LOG.md`.
3. Update `HANDOFF.md`. "Current state" should reflect the register, "Next actions" should be
   concrete and ordered, and new open questions and corrections should be added.
4. Update strategy statuses in `STRATEGIES.md`, and add any newly closed directions.
5. Make sure every run has its final manifest status. List any jobs still running in
   `HANDOFF.md`, with how to check on them and what to do when they finish.
6. If the workspace is a version-controlled repository and the user wants commits, commit
   with a message that summarises the status changes.
7. Report to the user: what changed status, what comes next, and which decisions are theirs.

## The handoff contract

`HANDOFF.md` succeeds if a competent reader with **no other context**, such as a new
agent session or a colleague joining the project, can do all of the following from it:

- say what is established, with which status, and where the proofs and certificates are;
- avoid repeating anything that has already failed, and know why it failed;
- reproduce the key computations from the commands given;
- start on the next action straight away.

Write it for that reader. Define the notation or link to where it is defined, give exact file
paths and commands, and state results precisely instead of alluding to them. Write
"Next actions" as instructions, not intentions: "Run `code/sweep.py --deg 7` over
the pencils listed in `runs/2026-03-12_pencils/selected.json`; success means …" is
useful, while "continue the sweep" is not.

`LOG.md` is the diary and `HANDOFF.md` is the state. A handoff written as a
chronological narrative forces the reader to replay the whole history to find out where
things stand.

## Projects with several people or agents

- Where possible, only one writer edits a given file at a time. Tag each `LOG.md` entry with
  its author, either an agent session or a person's name.
- The Review column of the register records who checked what. Do not enter
  `human:<name>` unless that person has confirmed it.
- If two sessions disagree about a status, the register wins until the disagreement
  is resolved. Record the disagreement as an open question.

## Common failure modes

- **Status drift.** Different files give different statuses for the same claim. Keep
  statuses in the register only.
- **Vague next actions.** "Continue investigating" forces the next session to
  rediscover everything. Name the file, the command and the success criterion.
- **Bloated summaries.** Current-state files grow until nobody reads them at the
  start of a session. Move detail down into the specialist files and keep the top-level files short.
- **Rewriting history.** Corrections are made silently, so readers of older versions
  are misled. Follow the correction procedure in `math-research-core`.
- **Evidence overwritten.** A re-run replaces old outputs that earlier claims point to.
  Runs are write-once; make a new run instead.
- **Closed directions repeated under a new name.** Read the table first, and record
  *why* each direction closed, so that variants of it can be recognised.

## Bundled files

- `templates/PROJECT_SUMMARY.md`, `templates/HANDOFF.md`, `templates/LOG.md`: read
  these when you create or restructure those files.
- `scripts/init_workspace.py`: creates the layout. It copies the templates for
  `LITERATURE_REVIEW.md`, `STRATEGIES.md` and `PROOF_PROGRESS.md` from the sibling
  skills if they are installed alongside, and never overwrites existing files.
