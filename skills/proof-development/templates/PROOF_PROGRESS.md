# Proof progress: {{TITLE}}

_Last updated: {{DATE}}_

<!--
Working file for arguments: statements, notation, assumptions, lemmas, gaps and
failed attempts. Statuses here must agree with the Results register in
PROJECT_SUMMARY.md; if they differ, the register is right and this file is
updated. Status labels and the review field are defined in the
`math-research-core` skill. Delete these guidance comments once they are no
longer useful.
-->

## 0. Target statement

**Theorem (target).** <!-- Precise statement: every quantifier in order, every hypothesis, the setting (field and characteristic, real or complex, smoothness, compactness, dimension range), and what "generic" means if used. -->

- Register ID: <!-- R<n> -->
- Status: <!-- CONJECTURE | PROVED-MODULO (GAP-…) | PROVED | REFUTED | UNRESOLVED -->
- Review: <!-- none | self | independent (YYYY-MM-DD) | human:<name> (set only by that person) -->
- Serves strategy: <!-- S<n> in STRATEGIES.md -->
- Acceptance criterion delivered: <!-- quote from PROJECT_SUMMARY.md, or explain the mismatch -->

### Examples checked against the statement

<!-- Test the statement before proving it: smallest cases, degenerate cases, one standard example. -->

| Example | Expected | Checked how (by hand / run ID / reference) | Outcome |
|---|---|---|---|
| | | | |

## 1. Notation and conventions

| Symbol | Meaning | Convention notes (signs, normalisations, sources that differ) |
|---|---|---|
| | | |

## 2. Standing assumptions

<!-- Number them so steps can refer to them. Note where each is used; an assumption that is never used is a warning sign. -->

- (A1) … — used in:
- (A2) … — used in:

## 3. Dependency graph

<!-- Plain text tree, or a mermaid graph. Mark the crux. Check that there are no cycles. -->

```text
Theorem (target)            [status]
├── L1                      [status, review]
├── L2                      [status, review]
│   └── [Ref, Thm x.y]      [CITED]
└── L3  ← crux              [status, review]
    └── run 2026-01-01_slug [CERTIFIED]
```

**Crux:** <!-- which lemma, and why it is where the difficulty lies -->

## 4. Lemmas

### L1. <!-- short name -->

**Statement.** <!-- self-contained; all hypotheses explicit -->

- Status:
- Review:
- Depends on: <!-- lemmas, cited results with theorem numbers, run IDs -->
- Used by:
- Cited results and hypothesis checks:
  - <!-- [Ref, Thm x.y]: hypothesis (i) holds because …; (ii) holds because … -->

**Proof.**

1. <!-- one inference per step, each with its justification -->
2.

**Checks done.**

- [ ] Verification checklist (date, items that applied):
- [ ] Conclusion tested on examples:
- [ ] Does not prove too much (case where the conclusion is false, and the step that breaks there):
- [ ] Every hypothesis used:
- [ ] Independent review (date, reviewer type, outcome):

<!-- Copy the L1 block for each further lemma. -->

## 5. Proof of the target from the lemmas

<!-- Numbered steps citing L1, L2, … Unjustified steps carry GAP markers. -->

1.

## 6. Open gaps

| Gap | Precise missing claim | Where used | Current status of the claim | Ideas / blockers |
|---|---|---|---|---|
| GAP-1 | | | | |

## 7. Failed approaches

<!-- Keep these. Each records an obstacle so later sessions do not repeat it. If one closes a strategy, also add it to the Closed directions table in STRATEGIES.md, with scope. -->

### F1. <!-- approach name --> (<!-- YYYY-MM-DD -->)

- Idea:
- Step that failed:
- Why it fails: <!-- error found / counterexample to an intermediate claim / missing tool -->
- Specific to this method, or a genuine obstruction?:
- Recorded as a closed direction in STRATEGIES.md?: <!-- yes (row) / no -->

## 8. Review history

| Date | Item | Reviewer (fresh agent session / human:<name>) | Findings | Response (fixed / downgraded / rebutted, where) |
|---|---|---|---|---|
| | | | | |
