---
name: strategy-planning
description: Plans and manages lines of attack on a mathematical research problem. Writes a strategy card for each approach, with its mechanism, the cheapest decisive test and a kill criterion fixed in advance; ranks the approaches; records every outcome, including failures; and keeps a closed-directions table so that dead ends are not repeated under new names. Use this whenever starting on an open problem, conjecture or construction, when the current approach has stalled or just failed, when deciding what to try next, before launching a large computation or a long proof attempt, when tempted to weaken the target, or when the user asks "how should we attack this?", "what else could we try?", "is this worth continuing?" or "why are we stuck?". Read STRATEGIES.md before proposing any new idea in an existing project.
---

# Strategy planning

Most research effort goes into approaches that do not work. The aim of this
skill is to make those failures cheap, informative and one-off:

- every approach states up front what would show it has failed;
- the cheapest test that could show it is run first;
- the outcome is recorded with its exact scope, so that neither the agent nor
  anyone after it re-runs a closed direction under a new name.

Use the claim-status labels from `math-research-core` for any result a
strategy produces, and the workspace layout from `research-workspace`.
Strategy statuses are `PROPOSED`, `ACTIVE`, `PAUSED`, `CLOSED` (its kill
criterion fired; the scope is recorded) and `SUCCEEDED`.

## When to use

- At the start of a project, after the problem is pinned down and an initial
  literature review exists.
- Whenever choosing the next piece of work: a new proof attempt, a search, a
  large computation.
- When a test has just finished, successfully or not, to record the outcome
  and re-rank.
- When progress has stalled: no strategy has advanced in the last session or
  two.
- Before any change to the target (weakening it, specialising it, changing
  the acceptance criterion). Such changes are decisions for the user.

## Reads and writes

| File | Use |
|---|---|
| `PROJECT_SUMMARY.md` | Read the target, the acceptance criterion and the Results register. Register any result a strategy produces. |
| `STRATEGIES.md` | Main output, started from `templates/STRATEGIES.md`. Strategy cards S1, S2, …, the ranking, the closed-directions table and the decisions log. |
| `LITERATURE_REVIEW.md` | Read the known obstructions, barrier results and techniques before proposing. |
| `HANDOFF.md` | Read the Corrections table: earlier misreadings are often the root of tempting but closed ideas. |
| `LOG.md` | Add a dated line whenever a strategy changes status. |
| `archive/` | Before a substantial rewrite, move the old version to `archive/STRATEGIES_<YYYY-MM-DD>_<slug>.md`. |

## Procedure

### 1. Pin the target

Copy the target and the acceptance criterion from `PROJECT_SUMMARY.md` into
§0 of `STRATEGIES.md`. The acceptance criterion says what counts as success:
a written proof (`PROVED`), a certified example (`CERTIFIED`), or a disproof
(`REFUTED`).

Also list **fallback targets**: weaker results that would still be worth
having, such as a special case, a weaker bound, a conditional result, or a
classification of what cannot work. Writing them down at the start keeps the
main target from drifting later, because the weaker versions already have a
named place to go.

### 2. Read what is already closed

Before generating anything, read:

- the closed-directions table;
- the known obstructions in `LITERATURE_REVIEW.md`;
- the Corrections table in `HANDOFF.md`.

For each new idea, check whether it is a closed direction under another name.
If it overlaps one, the card must say what is different and why the closure's
recorded scope does not cover it. If you cannot say that, the idea is not
new.

### 3. Generate candidates widely

Produce several genuinely different candidates before committing to one.
Include:

- both directions: attempts to prove *and* attempts to disprove;
- theoretical and computational approaches;
- at least one approach suggested by a known obstruction (what would have to
  be true to get round it?).

`references/heuristics.md` lists exploration moves (specialise, generalise,
find an invariant, change representation, minimal counterexample, analogy, …)
with examples. Go through it when the list of candidates is thin or when
stuck.

### 4. Write a strategy card for each serious candidate

Use `templates/strategy-card.md`. The fields that matter most:

- **Mechanism:** *why* this could work, in one paragraph. A strategy without
  a mechanism ("try harder at X") cannot be tested or closed.
- **Key ingredient:** the lemma, construction or computation it depends on,
  stated precisely, with its current status label.
- **Known obstructions it must avoid:** taken from the literature review and
  the closed directions.
- **Pre-mortem:** the most likely way it fails. Write it before investing
  anything. If the answer is "it collides with a known barrier", stop here.
- **Cheapest decisive test:** the smallest piece of work whose outcome would
  substantially change our belief in the strategy. Small cases, a single
  example, a degree-one version, a computer check of the key lemma on
  examples.
- **Kill criterion and its scope**, fixed before the test is run (see below).
- **Budget:** how much time or compute before the next review.

### 5. Rank, then work on one thing

Rank by roughly *value × chance of success ÷ cost*, and record the reasons in
the ranking table. In practice:

- Cheap tests that settle something come first, even for strategies with
  modest value. They shrink the space quickly.
- Prefer tests that discriminate between strategies: one outcome that helps
  rank several of them is worth more than one that only concerns a single
  strategy.
- Keep at most one or two strategies `ACTIVE`. Parallel half-finished
  attempts leave nothing closed and nothing proved.

### 6. Run the test through the right skill

- `proof-development` for arguments;
- `computational-experiments` for computations (fresh run directory,
  manifest);
- `construction-search` for searches for examples or counterexamples;
- `literature-review` when the test is "is this already known?".

### 7. Record the outcome immediately

On the card, add a dated line to the outcome log: what was run, where the
evidence is (a `runs/…` directory or a section of `PROOF_PROGRESS.md`), what
it showed, and the status change.

- **Kill criterion fired:** set the status to `CLOSED` and add a row to the
  closed-directions table (direction, outcome, scope, where recorded).
- **Partial results** (a lemma proved, an example certified, a bound shown)
  go into the Results register with their status labels. Negative results
  are results.
- **Budget exhausted without a decisive outcome:** the strategy is `PAUSED`,
  not `CLOSED`. Say what remains unknown.

### 8. Review and re-rank

Review after each decisive test and at the end of each session.

When every active strategy has closed, step back before inventing more:

- Look for an assumption shared by all the failed strategies. A common
  failure mechanism is often an obstruction worth stating and proving: it is
  a result in its own right and the best guide to what might work.
- Re-examine the target. Is there evidence that it is false? Is a fallback
  target the right next step? Changing the target is the user's decision:
  propose it, with reasons, in the decisions log.

### 9. Keep the file honest over time

Do not rewrite history in place. When `STRATEGIES.md` needs a substantial
reorganisation, archive the old version first. Outcomes and closures stay
visible.

## Kill criteria

A kill criterion is a statement, written before the test, of an observable
outcome that would close the strategy, together with the scope in which it
would then count as ruled out. Good kill criteria are:

- **Specific and observable:**
  - "If the exhaustive search over family F in degree 6 finds no example
    exceeding the bound, close S3 (scope: family F, degree 6)."
  - "If Lemma 2 fails for n = 5 (checked by exact computation), close S1."
- **Scoped:** a finite search rules out a *method within its scope*, not the
  target. Write the scope so that the closure cannot later be read as an
  impossibility theorem.
- **Budgeted:** "If, after two sessions, the key inequality cannot be reduced
  to a known one, pause and review."

Why fix them in advance? After a long effort, every outcome looks like
"nearly there": the goalposts move, a failed test gets reinterpreted as
partial success, and effort keeps flowing into a dead end. A criterion
written beforehand is the only reliable defence.

**Ruled out versus impossible.** `CLOSED` records that a method failed within
a stated scope. It becomes a mathematical statement ("no example exists in
family F") only if that statement is actually proved or certified. In that
case, also enter it in the Results register with its own status label.

## Rules, and why

- **Never weaken the target silently.** If a weaker target becomes the
  working goal, record it as a separate target, with the date and the reason,
  in the decisions log. The original stays open and stays stated. Silent
  weakening is how a project ends up "proving" something other than what was
  asked.
- **Negative outcomes are recorded as carefully as positive ones.** For the
  next session and for other researchers, knowing exactly what failed, why,
  and within which scope is often the most valuable output of the work.
- **Closed directions are not re-proposed without an argument.** If an old
  idea is reopened, cite its closure and explain why the new variant escapes
  its scope.
- **Separate implementation failures from mathematical failures.** A crash,
  a timeout, a numerical blow-up or a bug does not fire a kill criterion: the
  strategy's question is still unanswered. Inconclusive computations leave
  claims `UNRESOLVED`, never refuted.
- **Be wary of proxy progress.** Improving a numerical score, a margin or a
  relaxed objective is progress only if the link to the target is proved.
  Check that the improvement cannot come from a degeneracy such as rescaling,
  shrinking, collapsing to a boundary case, or exploiting a gauge freedom.
- **Counting arguments are heuristics.** "The parameter count says this
  should be possible" is `HEURISTIC` until the actual equations, the
  transversality and the reachability are established.
- **Local mechanisms are not global theorems.** A sign condition or
  inequality verified at one kind of point, or in one chart, is not evidence
  that it holds everywhere.
- **Decisions belong to the user.** Pivots, abandoning the main target, large
  compute budgets and changes to the acceptance criterion are proposed in the
  decisions log and confirmed by the user.

## Common failure modes

- **Goalpost drift:** the success criterion is reinterpreted after the
  result is in.
- **Renamed repeats:** a closed direction comes back with new terminology
  and the same mechanism.
- **Finite search read as impossibility:** "no example in the searched
  family" turns into "no example exists" in a summary.
- **Timeout read as exclusion:** an unresolved case is counted as ruled out.
- **Degenerate proxy gains:** the objective improves because the object is
  shrinking or degenerating, not because it is approaching the target.
- **Borrowed technique outside its hypotheses:** a gluing, perturbation or
  deformation theorem is applied where one of its non-degeneracy hypotheses
  fails on part of the configuration.
- **Unexamined analogy:** a mechanism that works in a neighbouring setting is
  assumed to work here.
- **Sunk cost:** a strategy continues because effort has been spent, not
  because the evidence supports it.
- **Too many active strategies:** many half-attempts, none closed and none
  finished.
- **Strategies without tests:** "think more about X" has no cheapest test and
  no kill criterion, so it never ends.
- **Ignored barrier results:** a strategy is pursued that the literature
  already shows cannot reach the target.

## Bundled files

- `templates/STRATEGIES.md`: copy to the project root when strategy planning
  starts. It contains the target, the shared framework, the ranking, the
  cards, what "ruled out" means, the closed-directions table and the
  decisions log.
- `templates/strategy-card.md`: copy once per strategy into §3 of
  `STRATEGIES.md`.
- `references/heuristics.md`: read when generating candidates, when the list
  of strategies is thin, or when everything has closed and a new angle is
  needed.
