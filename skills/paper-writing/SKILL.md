---
name: paper-writing
description: Turn a research workspace into a mathematics paper, preprint or working paper that claims no more than the evidence supports. Maps proofs, certified computations and literature notes into a LaTeX manuscript; keeps every theorem, remark and abstract sentence consistent with the claim statuses in the project's Results register; builds the bibliography only from checked references; writes an accurate statement of AI assistance and review status; and runs a compile check and a pre-circulation checklist. Use this whenever the agent drafts, restructures or revises a paper, preprint, working paper, thesis chapter, technical report or arXiv submission, converts notes or proofs into LaTeX, writes an abstract or introduction, answers referee reports, or prepares a manuscript to send to collaborators or experts. Use it even when the user just says "write this up", "turn this into a paper" or "draft the introduction".
---

# Paper writing

A paper is a public record of claims. This skill has two jobs. The first is to
present results clearly. The second, which matters more, is to make sure every
sentence about what is known matches the project's records: claim statuses,
evidence and review state. Rewriting a statement to read more elegantly is the
commonest way for a hypothesis to vanish. Writing "we verify" is the commonest way
for a numerical observation to turn into a theorem. This skill is built to catch
both.

The status labels (PROVED, PROVED-MODULO, CITED, CERTIFIED, NUMERICAL, HEURISTIC,
CONJECTURE, REFUTED, UNRESOLVED) and the `review:` field come from the
`math-research-core` skill. The workspace layout comes from `research-workspace`.

## When to use

- Starting a manuscript from a workspace, or from notes and proofs in conversation.
- Writing or revising an abstract, introduction, main-results statement or
  computational section.
- Preparing a working paper or preprint for circulation or submission.
- Responding to referee reports, or revising after a gap was found.
- Converting a manuscript between formats or templates while keeping its content.

## Reads and writes

| File | Use |
|---|---|
| `PROJECT_SUMMARY.md` | Read the Results register, the only source of claim status. |
| `PROOF_PROGRESS.md` | Read statements, proofs, notation table and open gaps. When writing exposes a gap, write `GAP-<n>` markers back here. |
| `LITERATURE_REVIEW.md`, `refs.bib` | Read. Cite only entries recorded as checked against the source. |
| `runs/*/manifest.json` | Read the method, certification level, code version and outputs behind each computational claim. |
| `STRATEGIES.md` | Read the closed directions, used for any honest discussion of methods that do not work. |
| `HANDOFF.md` | Read the Corrections table so no withdrawn claim comes back. |
| `paper/` | Write `main.tex`, `macros.tex`, section files, `refs.bib` (or a link to the project's), `figures/` and the scripts that generate them. |
| `LOG.md` | Append a dated entry, including the outcome of the pre-circulation checklist. |

## Procedure

### 1. Decide what the paper may claim

Start with a claim list drawn from the Results register. For each result you
intend to include, record its ID, status and review state. The status decides how
the paper may present it:

| Register status | How it may appear in the paper |
|---|---|
| PROVED | Theorem / Proposition / Lemma / Corollary. |
| PROVED-MODULO | Either close the gap first, or state a *conditional* theorem ("Assume Conjecture 4.1. Then…") with the gap stated as a hypothesis or conjecture. Never unconditionally. |
| CITED | Cite with the exact theorem number and the version checked. |
| CERTIFIED | A theorem marked as computer-assisted, with the certification method and where to find the code and data (repository, commit, run ID). |
| NUMERICAL | An observation or remark, or the experimental section ("numerical experiments suggest"). Never inside a theorem. |
| HEURISTIC | A remark or heuristic discussion, labelled as heuristic. |
| CONJECTURE | A Conjecture environment, with the supporting evidence summarised and labelled by status. |
| REFUTED | Report the counterexample; the counterexample itself needs status PROVED or CERTIFIED. |
| UNRESOLVED | Not claimed. It may be posed as an open question, with what was tried. |

Then:

- Choose the main results (usually one to three) and decide how they will be
  stated in the introduction.
- Check the review state of every headline result. If one has `review: none` or
  `review: self`, tell the user before drafting further and recommend independent
  review (the `proof-development` skill). Writing polished prose around an
  unreviewed proof makes the proof harder to doubt later.

### 2. Structure the manuscript

Start from `templates/paper-skeleton.tex`. A typical structure, with where the
material comes from:

| Paper section | Source in the workspace |
|---|---|
| Abstract | The main results, at their register status. Write it last. |
| Introduction: context, main results stated precisely, method, what is new | `PROJECT_SUMMARY.md`, `LITERATURE_REVIEW.md`, register |
| Preliminaries: notation, conventions, cited results stated exactly | Notation table and standing assumptions in `PROOF_PROGRESS.md`; checked entries in `LITERATURE_REVIEW.md` |
| Body sections: proofs | Lemmas and proofs in `PROOF_PROGRESS.md` |
| Computational section | `runs/*/manifest.json`, `code/` |
| Further directions / open questions | Open gaps, CONJECTURE and UNRESOLVED entries, closed directions worth reporting |
| Provenance and status statement | Review fields in the register; `references/provenance-statements.md` |
| References | Checked entries of `refs.bib` |

### 3. Write

- **Statements.** Copy each statement from `PROOF_PROGRESS.md`, edit it for
  readability, then compare the edited version with the original hypothesis by
  hypothesis. Put a comment `% register: R<n>` on the line after each theorem-like
  environment's `\begin`, so statuses can be checked mechanically.
- **Proofs.** Expand from the numbered proof and keep every justification,
  including the explicit hypothesis checks for cited theorems. A `GAP` marker may
  not appear in a paper. Either resolve it or make the result conditional, and
  update the register to match.
- **Notation.** Define every symbol once, in `macros.tex` or the preliminaries,
  before it is used. Keep it consistent with the notation table. State the
  conventions wherever sources differ (sign of the Laplacian or of curvature,
  normalisations). Check for collisions between sections, where one symbol is used
  with two meanings.
- **Citations.** Cite exact theorem numbers. Cite the version that was checked
  (published or preprint), and say which if they differ. Every new reference goes
  through the `literature-review` skill before it enters `refs.bib`. A reference
  that has not been checked against its source must not appear.
- **Computations.** For each computational claim, state what was computed, the
  method, its certification level, the software, and where the code, data and
  manifest are (repository and commit or archive, plus run ID). Copy numbers from
  run outputs rather than retyping them. Never write "we verified numerically" in
  support of a statement presented as a theorem.
- **Negative results.** State their scope ("no example among the N sources
  searched in the family F"), never "there is no example".
- **Wording.** Avoid "clearly" and "obviously" over steps that were not checked.
  Avoid unearned superlatives: "the first", "complete classification", "sharp",
  "optimal". "First" needs a literature search behind it, and "sharp" needs an
  example attaining the bound.
- **Figures.** Generate every figure from a script kept in the repository, and put
  the script path in a comment next to each `\includegraphics`. Hand-edited
  figures cannot be checked or regenerated.

### 4. Write the provenance and status statement

Readers need to know what AI tools did, who checked what, and what stage the
manuscript is at. Follow `references/provenance-statements.md`. Rules that cannot
be bent:

- Describe AI assistance specifically and accurately.
- Never describe a review that did not happen.
- Never call a working paper or preprint "peer-reviewed".

Most publishers and preprint servers require disclosure of AI assistance and do
not accept AI systems as authors, so check the target venue's current policy. The
human authors carry responsibility for the content, and the statement should not
blur that.

### 5. Compile and check

1. Compile fully: LaTeX, then BibTeX, then LaTeX twice; or `latexmk -pdf` if it is
   available.
2. Run `python3 scripts/check_latex_log.py paper/main.log`. Fix every error it
   reports: undefined references or citations, multiply-defined labels, missing
   files, TeX errors, missing reference formats. Review overfull boxes above the
   threshold. If it reports a rerun request, recompile and run it again.
3. Work through `references/pre-circulation-checklist.md` in full.
4. Compare the claim list with the paper: every `% register: R<n>` tag must match
   the register's current status.

### 6. Hand over for circulation

- Report the checklist outcome to the user, listing every unmet item explicitly,
  and record it in `LOG.md`.
- Leave sending, posting and submission to the human authors. The agent prepares
  the files, the checklist report and, if asked, a draft cover letter.

### Responding to referee reports

- Build a response table: each comment, the change made, and where it was made.
- Treat any comment that questions a step as a review finding under the
  `proof-development` skill. It may change a status, and the register must be
  updated before the paper is.
- Produce a marked-up diff of the revision (for example with `latexdiff`) along
  with the clean version.

## Rules, and why they matter

- **The register wins.** If the paper and the Results register disagree, the
  paper is wrong until the register is changed on the strength of new evidence.
  The register is what collaborators and later sessions trust.
- **Prose must not inflate a status.** "We show", "it follows" and "we verify"
  claim proof. A NUMERICAL or HEURISTIC result written in that language becomes a
  false claim once the paper is public.
- **The abstract and introduction may not be stronger than the body.** Readers
  often read nothing else.
- **No unchecked references.** References recalled from memory can be wrong in
  their numbering, their statement, or their existence.
- **Withdrawn claims stay withdrawn.** Check the Corrections table before reusing
  text from older drafts or archived notes.
- **Human authorship and responsibility are stated honestly.** Never imply that a
  human approved, checked or certified anything unless the register's review field
  records that the person did.

## Common failure modes

- A hypothesis is lost while rewriting a statement for elegance.
- A conditional result is stated unconditionally in the abstract.
- Numbers in the text disagree with the run outputs because they were retyped.
- The bibliography contains an unchecked or non-existent reference.
- A symbol is reused with two meanings in different sections.
- A figure cannot be regenerated.
- The provenance statement is vague ("AI tools were used") or overstated ("fully
  verified").
- cleveref is loaded before hyperref, or theorem environments are declared before
  cleveref is loaded, which breaks or misnames cross-references.
- Theorem-like environments are used for observations, so a NUMERICAL result looks
  like a theorem.

## Bundled files

- `templates/paper-skeleton.tex`: start every new manuscript from this. It covers
  package order, theorem environments, an observation environment for numerical
  results, register tags and the provenance section.
- `references/pre-circulation-checklist.md`: work through it before any manuscript
  leaves the workspace, including to co-authors.
- `references/provenance-statements.md`: read when writing the AI-assistance and
  review-status statement, a footnote on the title page, or a cover letter. It
  contains wording mapped to each status and review state.
- `scripts/check_latex_log.py`: run after every full compile. Use
  `python3 scripts/check_latex_log.py main.log [--overfull-threshold PT] [--strict] [--json]`.
  It exits with a non-zero code if blocking problems remain.
