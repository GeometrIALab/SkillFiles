---
name: lean-formalisation
description: Formalise mathematical statements and proofs in the Lean 4 proof assistant with the Mathlib library. Covers setting up a version-pinned project, finding existing library results before proving anything, writing a formal statement and checking independently that it says what the informal statement says, building a sorry-skeleton that mirrors the paper's lemma structure, filling it in, and confirming completeness with a clean build and an axiom audit. Use this whenever Lean, Mathlib, a proof assistant, formal verification, "formalise this lemma or theorem", `sorry` or `#print axioms` come up, whenever someone wants machine-checked certainty about a step of a proof, and whenever a formal proof is about to be cited as evidence for a claim.
---

# Lean formalisation

A Lean proof certifies exactly its formal statement, nothing more. So two
things matter:

1. The proof compiles with no gaps and no extra trust (no `sorry`, no new
   axioms, no unchecked shortcuts).
2. The formal statement is *faithful*: it says what the mathematics says.

The kernel takes care of the first. In practice most failures are in the
second: junk values, missing hypotheses, a quantifier in the wrong place, a
library definition with a different convention from the paper. This skill
puts the fidelity check before the proving effort, where it is cheap.

Status labels and the review field come from the `math-research-core` skill;
the workspace layout from the `research-workspace` skill. The informal proof
being formalised is managed with the `proof-development` skill.

## When to use

- Formalising a lemma, theorem or definition from the project in Lean 4 and
  Mathlib.
- Checking a doubtful step of an informal proof by machine.
- Reviewing or citing an existing formalisation as evidence.
- Fixing a Lean project that no longer builds after a version change.

## What this skill reads and writes

| Workspace item | Read | Write |
|---|---|---|
| `PROOF_PROGRESS.md` | informal statements, lemma labels, dependency graph | gaps and corrections the formalisation exposes (as `GAP-<n>` or corrections) |
| `formal/` | | the Lean project (a lake project): toolchain and manifest files, sources, README |
| `PROJECT_SUMMARY.md` (Results register) | | evidence for claims, including the fidelity-check record |
| `HANDOFF.md` | | build commands, Lean and Mathlib versions, list of remaining `sorry`s |
| `LOG.md` | | one line per session of formalisation work |

## Setup

- **Create the project in `formal/`** with lake, depending on Mathlib, following
  Mathlib's current instructions for a new project (at the time of writing,
  `lake new <name> math` creates a project using Mathlib's template). Download
  the prebuilt Mathlib files with `lake exe cache get` rather than compiling
  Mathlib yourself.
- **Pin versions and commit the pins.** `lean-toolchain` fixes the Lean
  version; `lake-manifest.json` fixes the Mathlib commit. Record both in
  `HANDOFF.md`. Mathlib renames and changes things often; without pins, a
  project that built last month may not build today, and nobody can reproduce
  the check.
- **Upgrade Mathlib as a deliberate, separate step**: update, rebuild
  everything, fix the breakage, commit. Never mix an upgrade with new proofs.

## Finding what already exists

Assume Mathlib has a result until a search says otherwise. Re-proving library
facts wastes time, and using the library's own definitions makes the work
usable by others.

- **Tactics that search:** `exact?` (find a term that closes the goal),
  `apply?` (find lemmas whose conclusion matches), `rw?` (find rewrites),
  `simp?` (run `simp` and report which lemmas it used, so you can replace it with
  a stable `simp only [...]`).
- **Inspection:** `#check name` shows a lemma's exact statement, including its
  hypotheses and typeclass assumptions. Read it before using the lemma.
- **Search engines and documentation:** the Mathlib API documentation (search by
  name), Loogle (search by constants, patterns and the shape of the statement),
  and LeanSearch (natural-language search).
- **Naming conventions:** Mathlib names are predictable. The conclusion
  comes first and hypotheses after `_of_` (for example `le_of_lt`), and
  operations are named after their symbols (`mul_comm`, `add_le_add`, `sub_nonneg`).
  Guessing a name and checking it with `#check` is often fastest.
- **Names recalled from memory or old sources may not exist in the pinned
  version.** Confirm every name with `#check` before building on it.
- **Human help:** the Lean community Zulip is the main forum for asking
  whether something exists or how to state it.

## Workflow

### 1. Formal statement first

Write the definitions and the main statement, with the proof left as `sorry`.

- Prefer Mathlib's definitions. If you must define something new, add small
  sanity checks right away: `example`s computing it on small cases where the
  answer is known (by `decide`, `norm_num` or `rfl`). A definition with no tests
  is the most common hiding place for a fidelity error.
- Mirror the paper's conventions explicitly in comments when Mathlib's differ
  (for example 0 ∈ ℕ, indexing from 0, the degree of the zero polynomial).

### 2. Statement-fidelity review, before any proving

Follow `references/statement-fidelity.md`. In short:

- Self-check against the checklist.
- Independent back-translation: a fresh agent session with no access to the
  working notes (a subagent, if the agent supports them) or a human colleague
  sees only the Lean statement and its definitions, and writes in prose what it
  says. Compare that with the informal statement.
- Non-vacuity: build a concrete instance satisfying the hypotheses (an
  `example`), so the theorem cannot be true merely because its hypotheses
  contradict each other.

Fix discrepancies now. Proving the wrong statement is the most expensive
mistake in formalisation.

### 3. Skeleton mirroring the paper

- One Lean declaration per lemma in `PROOF_PROGRESS.md`, with the same label in
  its name or docstring, each proved by `sorry`.
- Prove the main theorem from the lemmas first, so that the architecture
  compiles early. This often exposes a hypothesis the informal proof uses but
  never states. Record it as a `GAP-<n>` or a correction in `PROOF_PROGRESS.md`.

### 4. Fill the `sorry`s, most doubtful first

Start with the lemmas whose informal proofs are least certain. That is where
formalisation gives new information. Routine lemmas can wait.

When a lemma resists:

- It may be false as stated. Test it on small cases (`decide`, `norm_num`,
  explicit examples), or look for a counterexample, before spending more effort.
- A missing hypothesis found this way is a finding about the mathematics.
  Record it in `PROOF_PROGRESS.md`, and if the statement changes, redo the
  fidelity review for it.
- Break long goals into `have` steps. Heavy automation on a large goal is the
  usual cause of timeouts (see `references/pitfalls.md`).

### 5. Clean up

- Replace non-final `simp` calls with the `simp only [...]` that `simp?`
  suggests, so the proofs survive library changes.
- Remove `set_option maxHeartbeats` increases where possible; document any that
  remain.
- Make sure the build has no warnings you have not looked at.

## Done criteria

The formalisation of a statement is complete when all of these hold:

1. `lake build` succeeds with no errors and no "declaration uses 'sorry'"
   warnings.
2. `#print axioms <MainTheorem>` lists only the standard axioms `propext`,
   `Classical.choice` and `Quot.sound` (or a subset).
   - `sorryAx` in the list means a `sorry` remains somewhere in the dependencies.
   - `Lean.ofReduceBool` means `native_decide` was used. Newer Lean versions
     may also list a related compiler-trust axiom such as `Lean.trustCompiler`.
     Either way, the proof trusts the compiler and runtime as well as the kernel. Accept it only if the user explicitly
     agrees, and record that in the register.
   - Any other name means a custom `axiom` was introduced. Remove it.
3. A search of the project finds no `axiom`, `sorry`, `admit`, `unsafe`,
   `implemented_by` or `extern` declarations, and no options that turn off kernel
   checking.
4. The statement-fidelity check is recorded, and was redone after any change to
   the statement.
5. Lean and Mathlib versions and the commit are recorded in `HANDOFF.md`.

## Recording results in the Results register

- A complete formal proof of a statement that passed the fidelity check
  supports PROVED for the informal claim. Evidence: the path in `formal/`, the
  declaration name, the commit, the Lean and Mathlib versions, and the
  fidelity-check record. The review field reflects who did the fidelity check:
  `independent` for a fresh agent session or subagent, `human:<name>` only when
  that person did it and set it themselves.
- If the formal statement is weaker than the informal one (extra hypotheses, a
  special case), register the formal result as its own claim. Either keep the
  informal claim at its previous status, or mark it PROVED-MODULO with a
  `GAP-<n>` naming the difference.
- A partial formalisation (some `sorry`s left) supports nothing about the main
  claim. Lemmas proved completely can be registered on their own. List the
  remaining `sorry`s in `HANDOFF.md`.

## Rules, and why they matter

- **Don't change the statement to make the proof go through without recording
  it.** Quietly adding a hypothesis or weakening a conclusion produces a correct
  proof of a different theorem. Any change to the statement triggers a new
  fidelity review.
- **Use `sorry`, never `axiom`, for unfinished steps.** `sorry` produces build
  warnings and shows up in `#print axioms`; a stand-in axiom is easy to forget.
- **Pin and record versions.** A check that cannot be rerun cannot be audited.
- **Keep the skeleton aligned with the informal proof.** The labels let a reader
  match each formal lemma to its informal counterpart, and they make it clear
  which informal steps are now machine-checked.
- **Junk values are not bugs, but they change meanings.** Mathlib defines
  `x / 0 = 0` and similar conventions to keep functions total. A statement that
  ignores them can be true for unintended reasons, or say something other than
  intended (see `references/pitfalls.md`).

## Common failure modes

- Hypotheses that contradict each other, so the theorem is vacuous. Prevented
  by the non-vacuity `example`.
- A statement that holds only because of junk values (division by zero,
  truncated subtraction of natural numbers, `sSup` of an unbounded set).
- ℕ used where the paper means positive integers, so the case n = 0 changes
  the truth of the statement.
- A Mathlib definition with a different convention from the paper's.
- Lemma names copied from older sources that no longer exist in the pinned
  Mathlib.
- `simp`, `nlinarith` or `decide` timing out on a large goal, "fixed" by raising
  `maxHeartbeats` instead of splitting the goal.
- `native_decide` used for convenience without recording the extra trust.

## Bundled files

- `references/statement-fidelity.md`: the fidelity protocol, checklist and
  record format. Read it before proving anything, and again whenever a statement
  changes.
- `references/pitfalls.md`: junk values, coercions, convention mismatches,
  fidelity traps, version drift and automation timeouts. Read it when a
  statement or proof behaves unexpectedly, and during the fidelity self-check.
