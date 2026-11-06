# Independent review protocol

## Why

The author of a proof, agent or human, reads it with the reasoning that produced
it still in mind, and that reasoning silently fills whatever the text leaves out.
An independent reviewer has only the text, so missing steps show up as missing.
The protocol is built to keep the reviewer independent and to point them at
finding faults, not at confirming the proof.

## Who reviews

Any of the following:

- A fresh agent session with no access to the working notes, the conversation
  history or earlier drafts. A subagent qualifies if the agent supports them.
- A human colleague.

For a headline result, use two independent reviewers: two fresh sessions, or one
session and one human. A session that has already seen the proof, or its
development, does not count as independent.

## What to hand over, and what to withhold

**Hand over:**

1. The statement, exactly as in `PROOF_PROGRESS.md`.
2. The notation table and the standing assumptions.
3. The proof, as numbered steps.
4. The exact statements of every cited result, with references and theorem
   numbers.
5. Optionally, a few examples where the conclusion is known. These give the
   reviewer test cases; they are not reassurance.

**Withhold:**

- The history of how the proof was found, including dead ends and intuitions.
- The claimed status, and any statement that the result "is proved" or "has been
  checked". These anchor the reviewer towards agreeing.
- The author's confidence, and anything suggesting which steps are thought safe.

## Reviewer instructions (hand over verbatim)

```text
You are reviewing a mathematical argument. Your job is to find what is wrong or
missing, not to confirm that it is right.

You are given a statement, its notation and standing assumptions, a proof split
into numbered steps, and the exact statements of the results it cites.

1. Restate the claim in your own words, including all hypotheses. If the
   statement can be read in more than one way, list the readings, then review
   the most natural one and say which you chose.

2. Before reading the proof, try to break the statement. Test it on the
   smallest and most degenerate cases you can think of and on standard
   examples in this area. Report what you tried and what happened.

3. Go through the proof step by step. Give each step exactly one verdict:
   - correct: it follows from earlier steps, cited results or definitions.
     Say which.
   - gap: plausibly true but not justified as written. State precisely what
     is missing.
   - error: false as written, or does not follow. Give the reason and, if
     possible, a counterexample.
   - unclear: you cannot tell what is being claimed. Say what is ambiguous.
   "Probably fine" is a gap, not "correct".

4. For each cited result, check that every one of its hypotheses holds where
   it is applied, that its definitions match the ones used here, and that it
   is used in the direction and at the strength stated.

5. For each standing assumption, say where it is used. Flag any assumption
   that is never used, and any step that silently needs an assumption that is
   not listed.

6. Check whether the argument proves too much: would the same steps prove
   something false in another dimension, degree or field, or in a degenerate
   case? If so, say where the steps fail to break.

7. Name the single weakest step and explain why.

Do not repair the proof unless asked; describe each problem precisely. Do not
soften findings. If you could not check something, say so explicitly. Use the
report format below.
```

## Reviewer report format

```markdown
## Review of <item> — <YYYY-MM-DD>

**Reviewer:** fresh agent session | human:<name>
**Reading of the statement:** …
**Attempts to break the statement:** <cases tried, outcomes>

### Step verdicts
| Step | Verdict (correct / gap / error / unclear) | Reason |
|---|---|---|
| 1 | | |

### Cited results
| Result | Hypotheses checked where applied | Problems |
|---|---|---|

### Assumptions
- Never used:
- Needed but not listed:

**Proves too much?** …
**Weakest step:** …
**Overall:** no problems found | gaps found | errors found
**Could not check:** …
```

The "Overall" line never says "proved" or "correct". The reviewer reports
findings; the status is decided by the argument and the register's rules.

## How the author responds

Every finding gets exactly one of these responses, recorded in the review history
table of `PROOF_PROGRESS.md`:

- **Fix.** Repair the step. The changed steps then need checking again: either a
  new fresh reviewer for those steps, or at least the verification checklist
  re-run on them, with a note saying which was done.
- **Downgrade.** If the finding can't be fixed now:
  - mark the step with a `GAP-<n>`;
  - set the result to PROVED-MODULO, or REFUTED if an error kills it;
  - update the Results register;
  - follow the dependency graph forwards and downgrade everything that depends on
    the result.
- **Rebut.** Write the argument that answers the finding *into the proof text*.
  "The reviewer misunderstood" is never enough: if a careful reader misunderstood,
  the text was unclear, and the clarification belongs in the proof.

## Rules

- **A review never raises a status on its own.** A review that finds nothing
  changes only the review field (`review: independent`, plus the date). The status
  comes from the argument and the propagation rule in `math-research-core`.
- **Set `review: independent` only if this protocol was followed:** fresh
  reviewer, history withheld, report in the format above.
- **Never set `review: human:<name>` yourself.** Only the named person records a
  human review. An agent must never describe its own work, or another agent's
  review, as human-checked.
- **Keep every review report.** Append it to the review history, or store it in
  `archive/` and link to it, even when it found nothing. A clean review of an
  earlier version does not carry over to a revised proof.
- **Record disagreements.** If reviewers disagree and the issue is not settled,
  treat the step as a GAP until it is.
