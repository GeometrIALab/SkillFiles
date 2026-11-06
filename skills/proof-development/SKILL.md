---
name: proof-development
description: Develop, write and check mathematical proofs so that every result carries the status it actually deserves. Breaks an argument into lemmas with a dependency graph and a status for each lemma, justifies every step, checks the hypotheses of every cited theorem, tests lemmas on examples, runs an independent adversarial review and records failed attempts precisely in PROOF_PROGRESS.md. Use this whenever the agent proves or disproves a lemma or theorem, sketches, repairs or expands an argument, checks a proof (its own, a colleague's or one from a paper), decides whether a claim may be called proved, or tries to turn a heuristic or numerical observation into a theorem. Use it even when the user only says "show that…", "why is this true?", "fill in the details", "is this argument right?" or "can we prove the bound?".
---

# Proof development

An agent can write arguments that read as complete and are not. This skill makes
every proof *inspectable*. The argument is split into small claims. Each claim lists
what it depends on, is checked against a fixed list of questions, is tested on
examples and is given an honest status. The result is a `PROOF_PROGRESS.md` that a
sceptical expert could audit line by line. A polished paragraph that hides where
the difficulty went is not the goal.

The claim-status vocabulary (PROVED, PROVED-MODULO, CITED, CERTIFIED, NUMERICAL,
HEURISTIC, CONJECTURE, REFUTED, UNRESOLVED), the separate `review:` field and the
`GAP-<n>` markers are defined in the `math-research-core` skill. This skill applies
them to proofs.

## When to use

- Proving or disproving a statement, at any level from a routine lemma to the main
  theorem.
- Writing up an argument that came up in conversation, in a sketch or on a
  whiteboard photo.
- Repairing a proof after a gap or error is found.
- Reviewing an argument written by someone else, or by this agent in an earlier
  session. Use the protocol in `references/independent-review.md`.
- Deciding whether a claim in the Results register may move to PROVED.

These belong to other skills:
- Checking that a literature result says what we need: `literature-review`. Its
  output is a CITED claim.
- Rigorous computation: `computational-experiments`. Its output is a CERTIFIED
  claim, which a proof may then use.
- Formal verification in a proof assistant: `lean-formalisation`.

## Reads and writes

| File | Use |
|---|---|
| `PROJECT_SUMMARY.md` | Read the acceptance criterion and the Results register. Write status changes to the register, which is the only source of truth for statuses. |
| `STRATEGIES.md` | Read which strategy this proof serves and the closed directions. Write a closed direction when a failed proof ends a strategy. |
| `LITERATURE_REVIEW.md` | Read the exact statements of the results you cite. |
| `PROOF_PROGRESS.md` | The main working file: statements, notation, assumptions, dependency graph, lemmas, gaps and failed approaches. |
| `HANDOFF.md` | Read the Corrections table so you don't reintroduce a withdrawn claim. Add a row when you withdraw one. |
| `LOG.md` | Append a dated entry for the session. |

If no workspace exists, keep the same structure in a single file and say so. The
`research-workspace` skill sets the workspace up. `templates/PROOF_PROGRESS.md` is
the starting point for the proof file.

## Procedure

### 1. Fix the statement before proving it

Most failed proofs from an agent come from a statement that drifted while the
argument was being written. Fix the statement first.

1. Write the statement precisely. Include every quantifier in order, every
   hypothesis, and the setting: the field and its characteristic, real or complex,
   smooth or singular, compact or not, the regularity class, the dimension range.
   Say what "generic" or "general" means: which parameter space, and open dense,
   Zariski open or full measure.
2. Record the notation and conventions in the notation table, and number the
   standing assumptions (A1), (A2), …. Note any convention that differs between
   sources: the sign of the Laplacian or of curvature, normalisations, orientations.
3. **Test the statement before trying to prove it.** Check the smallest cases, the
   degenerate cases and one standard example from the literature. A false statement
   costs more time than any other error. If no case can be checked, write that down.
4. Compare the statement with the acceptance criterion in `PROJECT_SUMMARY.md`. If
   it is proved, does it deliver what the project needs? If not, find out now.

### 2. Decompose into lemmas

1. Write the proof of the main result *in terms of lemmas* before proving any of
   them. Put a `GAP-<n>` marker on every step that is not yet justified. This
   skeleton shows which lemmas are actually needed.
2. Give each lemma one idea and a statement that stands on its own, and label it
   L1, L2, …. Record what it depends on: other lemmas, cited results with exact
   theorem numbers, and certified runs by run ID. Record which results use it.
3. Draw the dependency graph and check that it has no cycles. Circular dependencies
   are easy to create when a "standard" fact is quietly derived from the main
   theorem.
4. **Identify the crux**: the lemma where the real difficulty is. Work on it first.
   Agents tend to write the easy lemmas carefully and wave at the hard one. A
   finished easy lemma is of no use while the crux is false.

### 3. Prove each lemma

Write each proof as a numbered list of steps. Each step makes one inference and
names its justification:

- *by definition*, *by L3*, *by step 4*;
- *by [Ref, Theorem 4.2]*, followed by an explicit check of each hypothesis: "(i)
  holds because M is compact by (A2); (ii) holds because…";
- *by computation*, with a run ID and its status (CERTIFIED or NUMERICAL).

Rules while writing, with the reasons:

- **Check the hypotheses of every cited theorem, in writing.** The most common
  serious error is applying a theorem whose hypotheses fail by a little. Typical
  misses are compactness, smoothness class, characteristic zero, connectedness and
  surjectivity of a derivative. Quote the statement from the source or from
  `LITERATURE_REVIEW.md`, not from memory: statements recalled from memory are
  often subtly wrong.
- **Make quantifier order and constant dependence explicit.** Write
  "C = C(n, K), independent of ε", not just "C". Hidden non-uniformity is
  invisible until written down.
- **Don't use "clearly", "obviously", "it is easy to see", "by a standard argument"
  or a bare "similarly" as a justification.** Either give the argument or mark a
  GAP. "Similarly" is acceptable only if you say what changes. These phrases are
  exactly where unchecked steps hide.
- **Mark what you cannot do.** Write `GAP-<n>: <precise statement of the missing
  claim>`. A precisely stated gap is progress and can be handed to someone else; a
  hidden gap is a liability.
- **Never change the statement silently to make the proof work.** If you need an
  extra hypothesis or a weaker conclusion, write the new statement as a separate
  result, flag the change in `LOG.md`, and leave the original with its true status.
- **Keep special cases separate.** "Proved for n = 2" is its own lemma with its own
  status, not a partial proof of the general statement.
- **Don't turn heuristics into lemmas by assertion.** Before a dimension count,
  "generically" or a transversality claim can be a step, it needs a precise
  statement: which space, which map, which theorem gives transversality, and why
  the stratum is non-empty.

### 4. Check

Do all of this before a lemma is marked PROVED.

1. **Run `references/verification-checklist.md`** on the lemma and record which
   items applied in the lemma's "Checks done" block.
2. **Test the conclusion on examples.** Evaluate it on concrete cases, symbolically
   or numerically; use `computational-experiments` for anything non-trivial. If the
   conclusion fails on an example, the lemma is false, however convincing the
   proof looks.
3. **Check that it doesn't prove too much.** Apply the same argument where the
   conclusion is known to be false: another dimension, degree or field, a
   degenerate case, a known counterexample. Find the step that breaks there. If no
   step breaks, the proof is wrong.
4. **Check that every hypothesis is used.** An unused hypothesis means either the
   statement can be strengthened, which is suspicious if that would beat known
   results, or a step silently needs it. A step that needs a hypothesis that is not
   listed is a gap.

### 5. Get an independent review

Your own re-reading is weak evidence, because the reasoning you remember fills in
whatever the text leaves out. Before the crux lemma or a main result is reported as
PROVED outside the workspace (in a paper, a summary for collaborators, or the
project summary's headline), have it reviewed independently:

- Follow `references/independent-review.md`. The reviewer is a fresh agent session
  with no access to the working notes (a subagent, if the agent supports them) or a
  human colleague. Give the reviewer only the statement, notation, assumptions,
  numbered proof and the exact statements of cited results, not the history of how
  the proof was found.
- Respond to every finding: fix the proof, downgrade the status, or rebut with an
  argument that is added to the proof text.
- Record the review in the lemma block and in the review history table. Set
  `review: independent` only if the protocol was followed. Never set
  `review: human:<name>`; only that person can record it.
- **A review never raises a status by itself.** The status comes from the argument.
  A review that finds nothing fills in the review field and nothing else.

### 6. Record the outcome

1. **Update the Results register**, applying the propagation rule:
   - A result is PROVED only if every dependency is PROVED, CITED or CERTIFIED.
   - Otherwise it is PROVED-MODULO, and each dependency that is not rigorous is
     listed as a named GAP. A NUMERICAL or HEURISTIC input is a gap, not a step.
   - The status shown in `PROOF_PROGRESS.md` must agree with the register. If they
     disagree, the register is right and the proof file is updated.
2. **Record failed attempts** under "Failed approaches". Give the idea, the exact
   step that failed, why it failed, and whether the obstacle belongs to this method
   or is a genuine obstruction (for example, a counterexample to an intermediate
   claim). Failed proofs carry information about where the difficulty lies; they
   are not clutter. If the failure closes a strategy, add a row to the Closed
   directions table in `STRATEGIES.md` and state the scope.
3. **When an earlier claim falls:**
   - Downgrade it in the register.
   - Add a row to the Corrections table in `HANDOFF.md`.
   - Follow the dependency graph *forwards*: every result that used the claim drops
     to the new status. Downgrade those as well.
4. Move superseded proof versions to `archive/` with a date stamp; don't delete
   them.
5. Append a `LOG.md` entry covering what was proved, what was downgraded and what
   gaps remain.

## Rules, and why they matter

- **Status propagates from the weakest dependency.** A chain of reasoning is only
  as strong as its weakest link, and readers of the register rely on it without
  re-reading the proofs.
- **Status words in prose must match the register.** "We have shown" next to a
  PROVED-MODULO entry misleads the next reader, who may be another agent session
  making decisions on the strength of it.
- **Checking small cases is evidence, not proof.** Checking n ≤ 10 is NUMERICAL or
  CERTIFIED evidence for the general statement. It moves a CONJECTURE nowhere
  except into a better-supported CONJECTURE.
- **Exhaustive case analyses must argue that they are exhaustive.** List the cases
  and prove the list is complete. Equality cases, boundary cases and degenerate
  configurations are the usual omissions.
- **Matching a total does not prove a list is complete.** An Euler characteristic,
  degree or index sum can match while a pair of cancelling objects is missing.
  Completeness needs its own argument or a certified computation.
- **Keep failures.** An obstruction recorded today stops the next session from
  repeating the same doomed attempt.

## Common failure modes

The full catalogue, with examples and how to detect each one, is in
`references/common-proof-errors.md`. The most frequent are:

- The statement drifts during the proof, so the argument proves something weaker or
  different.
- A cited theorem is applied outside its hypotheses, or a preprint's stronger
  statement is used where the published version is weaker.
- Uniformity is hidden: a constant or δ depends on a parameter that is later varied.
- Local information is promoted to a global conclusion without a patching or
  compactness argument.
- "Generic" information is applied to a specific object, or a dimension count is
  used as an existence proof.
- A sampled or numerical check is used as a proof step.
- Formulas are combined from sources with different sign or normalisation
  conventions.
- The proof proves too much.
- The agent reviews its own proof and agrees with it.

## Bundled files

- `templates/PROOF_PROGRESS.md`: copy into the workspace when starting a proof
  effort.
- `references/verification-checklist.md`: read before marking any lemma PROVED,
  and when reviewing anyone's proof.
- `references/independent-review.md`: read when the crux lemma or a main result
  needs review. It contains reviewer instructions that can be handed over verbatim,
  and the format for the reviewer's report.
- `references/common-proof-errors.md`: read when a proof feels finished but you
  have not found where the hard part went, when a reviewer flags a step, or when
  checking someone else's argument.
