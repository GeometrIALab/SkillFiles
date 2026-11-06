# Mathematical research skills for AI agents

A pack of nine **skills**: instruction files that an AI agent loads as context. They
make the agent work like a careful research collaborator in mathematics. They do not
teach mathematics. They set out working discipline:

- every claim carries an explicit status, so that *proved*, *computed*, *certified* and
  *believed* never blur together;
- each project keeps a persistent file-based workspace, so that work survives across
  sessions, context resets and handovers;
- literature is checked against the source before it is cited;
- strategies are planned with kill criteria decided in advance, and failed directions
  are recorded so that they are not repeated;
- proofs get independent review, by a reviewer who sees only the proof;
- computations are reproducible, and certified before they count as rigorous;
- negative results are reported honestly, together with their scope.

The skills are plain Markdown plus a few small Python scripts that use only the standard
library. They are not tied to any particular agent or model provider.

---

## Contents

- [Why these skills](#why-these-skills)
- [The skills](#the-skills)
- [How they fit together](#how-they-fit-together)
- [Two shared conventions](#two-shared-conventions)
- [Installation](#installation)
- [Using the pack](#using-the-pack)
- [Customising and extending](#customising-and-extending)
- [Repository layout](#repository-layout)

---

## Why these skills

Agents are fast at generating ideas, code and arguments. In research mathematics the
bottlenecks are elsewhere, and three failures cause most of the wasted effort:

1. **Overclaiming.** A numerical observation becomes "we showed" two summaries later. A
   sampled count is reported as exact. A preprint's stronger statement is cited for the
   published theorem.
2. **Forgetting.** A new session has none of the previous session's context. It rebuilds
   it badly, or builds on claims that were corrected in the meantime.
3. **Repeating.** Directions that were already explored and closed get tried again under
   new names, because nobody recorded *why* they failed.

The pack addresses each of these directly. The rules are distilled from long
agent-assisted research projects, which included proof attempts, large computational
searches and literature work, and from the specific ways those projects went wrong.

## The skills

| Skill | What it does | Loads when the agent is… |
|---|---|---|
| [`math-research-core`](skills/math-research-core/SKILL.md) | **The hub.** Status labels for claims, evidence required for each, gap markers, scope of negative results, the correction procedure, a catalogue of failure modes. | stating, recording or reporting any mathematical result |
| [`research-workspace`](skills/research-workspace/SKILL.md) | Standard project files (summary with Results register, handoff, log, …), and protocols for starting, ending and handing over a session. Includes a script that creates the workspace. | starting, resuming, pausing or handing over a project |
| [`literature-review`](skills/literature-review/SKILL.md) | Search protocol, per-paper records with exact statements and hypotheses, citation checking, gap analysis. Includes a script that checks `.bib` entries against online records. | finding or citing what is known |
| [`strategy-planning`](skills/strategy-planning/SKILL.md) | Strategy cards with kill criteria fixed in advance, prioritisation, the Closed directions table, exploration heuristics. | deciding how to attack a problem, or what to try next |
| [`proof-development`](skills/proof-development/SKILL.md) | Proof structure, lemma dependencies, verification checklist, independent review protocol, catalogue of common proof errors. | writing, checking or repairing a proof |
| [`computational-experiments`](skills/computational-experiments/SKILL.md) | Run directories and manifests, levels of evidence from screening to certification, certification techniques, work accounting, tool selection. Includes a script that creates runs. | running any computation that may be cited as evidence |
| [`construction-search`](skills/construction-search/SKILL.md) | Searches for counterexamples and extremal objects: an order of methods from exhaustive to learned, objective design, a protocol for found candidates, negative-result reporting. | hunting for a counterexample or an extremal example |
| [`lean-formalisation`](skills/lean-formalisation/SKILL.md) | Lean 4 / Mathlib workflow, checking that a formal statement says what the informal one says, done criteria, pitfalls. *Optional.* | formalising a statement or proof |
| [`paper-writing`](skills/paper-writing/SKILL.md) | From workspace to manuscript: LaTeX skeleton, status-accurate wording, statements disclosing AI assistance, a pre-circulation checklist. Includes a script that checks LaTeX logs. | drafting or revising a paper |

Each skill folder has the same anatomy:

```
<skill>/
├── SKILL.md        frontmatter (name, description) + instructions; always read when the skill loads
├── references/     longer material, read only when the SKILL.md points to it
├── templates/      files the agent copies and fills
└── scripts/        small deterministic helpers (Python 3, standard library only)
```

The `description` in each `SKILL.md` frontmatter tells the agent when to load the
skill. The body is kept short. Detailed catalogues live in `references/`, so the agent
reads them only when needed.

## How they fit together

```
                 ┌──────────────────── math-research-core ────────────────────┐
                 │   status labels · review field · gaps · scope · corrections  │
                 └─────────────────────────────────────────────────────────────┘
                                             │ used by all
   research-workspace ── PROJECT_SUMMARY (Results register) · HANDOFF · LOG · runs/ · archive/
          │
          ├──► literature-review ──► strategy-planning ──┬──► proof-development ──► lean-formalisation
          │      LITERATURE_REVIEW      STRATEGIES        │      PROOF_PROGRESS          formal/
          │      refs.bib               (Closed directions)├──► computational-experiments
          │                                               │      runs/<date>_<slug>/manifest.json
          │                                               └──► construction-search
          │                                                      candidate records → certification
          └──────────────────────────────────────────────────► paper-writing ── paper/
```

Real projects loop between stages. Two things tie the stages together: the status
vocabulary, and the **Results register** in `PROJECT_SUMMARY.md`, which is the single
place where the current status of every claim is recorded.

## Two shared conventions

**Claim status labels** (defined in `math-research-core`):

| Label | Meaning |
|---|---|
| `PROVED` | Complete, checked argument in the project files |
| `PROVED-MODULO` | Complete except for named gaps `GAP-n`, each a precise statement |
| `CITED` | From the literature; statement and hypotheses checked against the source |
| `CERTIFIED` | Rigorous computation (exact or validated arithmetic, checked proof log), reproducible |
| `NUMERICAL` | Computational evidence without a certificate |
| `HEURISTIC` | Plausibility argument: parameter count, analogy, pattern |
| `CONJECTURE` | Precise statement, believed, unproved |
| `REFUTED` | Disproved, or a certified counterexample |
| `UNRESOLVED` | Attempted and inconclusive: timeouts, weak bounds, failed proofs |

A separate **review** field records who has checked a claim:
`none | self | independent | human:<name>`. Only a human can confirm `human:<name>`,
and the skills never let the agent describe its own work as human-checked.

**Project workspace** (defined in `research-workspace`):

```
<project>/
├── PROJECT_SUMMARY.md     problem · acceptance criterion · Results register · open gaps
├── HANDOFF.md             resume-from-cold document · Corrections table
├── LOG.md                 append-only session log
├── LITERATURE_REVIEW.md   refs.bib
├── STRATEGIES.md          strategy cards · Closed directions
├── PROOF_PROGRESS.md
├── runs/  probes/  code/  formal/  paper/  archive/
```

## Installation

**Install the whole pack if you can.** The skills refer to one another by name. At
minimum, install `math-research-core` and `research-workspace`: every other skill
builds on them.

### Agents that read skill folders natively

Many coding and research agents load folders in this `SKILL.md` format directly.
Copy the folders under `skills/` into the directory your agent reads skills from. Your
agent's documentation gives the location. There is usually a per-user directory and a
per-project directory.

```bash
cp -R skills/* /path/to/your/agent/skills/
```

Keep the folders side by side: `research-workspace/scripts/init_workspace.py` looks
for the templates of its sibling skills next to it.

### Agents with a single instruction file

If your agent reads one instructions or context file per project instead, keep the
pack somewhere on disk and add a short pointer to that file:

```markdown
## Mathematical research
Before doing research work in this project, read
/path/to/skill_files/skills/math-research-core/SKILL.md and
/path/to/skill_files/skills/research-workspace/SKILL.md and follow them.
For other tasks, read the SKILL.md in /path/to/skill_files/skills/ whose
description matches the task (literature, strategy, proofs, computation,
counterexample search, formalisation, paper writing).
```

### Chat interfaces with file or project uploads

Upload the `SKILL.md` files, plus the `references/` files you want, as project
knowledge, or paste `math-research-core/SKILL.md` into the custom instructions. For
interfaces that accept zipped skill folders, build the zips with:

```bash
./package.sh        # writes dist/<skill>.zip for each skill, and dist/math-research-skills.zip
```

### Scripts

The bundled scripts need Python 3.9 or later and nothing else. Each one has `--help`.

| Script | Purpose |
|---|---|
| `research-workspace/scripts/init_workspace.py` | Create a project workspace from the templates. Never overwrites existing files. |
| `literature-review/scripts/check_bib.py` | Check `.bib` entries with a DOI or arXiv identifier against Crossref and arXiv. Flags missing or mismatched records. |
| `computational-experiments/scripts/new_run.py` | Create a dated run directory with a pre-filled `manifest.json` (environment, git commit, file hashes), and mark it finished later. |
| `paper-writing/scripts/check_latex_log.py` | Report undefined references and citations, duplicate labels, missing files and bad boxes from a LaTeX log. |

## Using the pack

You do not need to name the skills. The agent loads them when the task matches. Some
typical requests:

| You say | What happens |
|---|---|
| "Let's start a project on the maximal number of real solutions of this family of polynomial systems." | `research-workspace` creates the workspace. The agent drafts the problem statement and **asks you to confirm the acceptance criterion**. `literature-review` follows. |
| "Where were we?" | The start-of-session protocol: read the summary, handoff, log and closed directions, then report the state and propose a plan. |
| "What's known about this?" | Structured search. Each source gets a record with its exact statement and hypotheses. Citations are checked before they enter `refs.bib`. |
| "Is Lemma 3 actually right?" | `proof-development` runs the verification checklist and an independent review. The status changes only on new evidence. |
| "Run the degree-7 sweep overnight." | `computational-experiments` creates a run directory and manifest, runs the job in the background with checkpoints, and records the result as `NUMERICAL` until certified. |
| "Find a counterexample." | `construction-search` goes from small exhaustive cases to larger searches, certifies any candidate before reporting it, and reports a negative result together with its scope. |
| "Write this up." | `paper-writing` builds the manuscript from the workspace, matches the wording to the register's statuses, and adds an accurate statement about AI assistance and review. |

The agent leaves to you the decisions that are yours: the acceptance criterion,
changes to the target, accepting a weaker result, leaving a gap open, and anything
involving people outside the project.

## Customising and extending

- **Field packs.** The core skills are deliberately field-independent. To add
  field-specific knowledge (conventions where sources disagree, standard results with
  exact hypotheses, standard software, classic pitfalls, test examples), copy
  [`templates/field-pack/SKILL.template.md`](templates/field-pack/SKILL.template.md)
  to `skills/field-<area>/SKILL.md` and fill it in. Have a specialist review it: errors in a field
  pack spread into every project that uses it.
- **Group-specific procedures.** Put your group's own procedures, such as release
  workflows, internal report formats or naming schemes, in a **separate** skill that
  refers to these skills, rather than editing the generic pack. You can then update the
  pack without losing local changes.
- **Changing the vocabulary.** The status labels and file names are used across all
  skills. If you change one, search the whole `skills/` tree and update every
  occurrence.
- **Testing changes.** Give an agent a few realistic research prompts with and without a
  skill installed, and compare the results. Check both that the skill loads when it
  should (its `description` is the trigger) and that the output follows its rules.

## Repository layout

```
skill_files/
├── README.md                  this file
├── LICENSE.md                 which licence covers which files
├── LICENSES/                  full texts: CC-BY-4.0, MIT, CC0-1.0
├── package.sh                 builds zip archives in dist/
├── templates/
│   └── field-pack/SKILL.template.md
└── skills/                    each skill folder also has its own LICENSE.txt
    ├── math-research-core/
    ├── research-workspace/
    ├── literature-review/
    ├── strategy-planning/
    ├── proof-development/
    ├── computational-experiments/
    ├── construction-search/
    ├── lean-formalisation/
    └── paper-writing/
```

## Licence

Copyright © 2026 GeometrIA Lab, CBG. Each kind of file has its own licence:

| Files | Licence |
|---|---|
| Instructions and documentation (`SKILL.md`, `references/`, this README) | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) |
| Scripts (`scripts/`, `package.sh`) | [MIT](LICENSES/MIT.txt) |
| Templates (`templates/` folders) | [CC0 1.0](LICENSES/CC0-1.0.txt): copy them into your own projects and papers without attribution |

Using the skills needs no attribution. Credit is only required when you share the skill
text itself or an adaptation of it. See [LICENSE.md](LICENSE.md) for details and a
suggested credit line. Each skill folder also carries its own `LICENSE.txt`, so a skill
distributed on its own keeps its terms.
