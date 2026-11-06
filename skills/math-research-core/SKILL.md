---
name: math-research-core
description: Ground rules for agent-assisted mathematical research. Provides one vocabulary for the status of every claim (PROVED, PROVED-MODULO, CITED, CERTIFIED, NUMERICAL, HEURISTIC, CONJECTURE, REFUTED, UNRESOLVED), the evidence each status needs, how to mark gaps, how to report negative results within their scope, and how to correct earlier claims. Use it whenever you state, record, summarise or report a mathematical result, lemma, computation, counterexample or literature fact, whether in notes, project files, reports, papers or conversation. Also use it whenever you work on a research-level problem, even if nobody asks about rigour. The other skills in this pack (research-workspace, literature-review, strategy-planning, proof-development, computational-experiments, construction-search, lean-formalisation, paper-writing) all build on these rules.
---

# Mathematical research: core rules

In research mathematics, wrong ideas are normal and cheap. The expensive failure
is a wrong idea **recorded as a fact**: once "we showed X" is in the notes, every
later session builds on it, and the error surfaces weeks later, far from its cause.
These rules keep the status of every statement visible. The mathematician and every
later session can then tell at a glance what is known, what is believed, and what
was only observed.

## The research pipeline

This skill is the hub. The other skills cover the stages of a project:

| Stage | Skill | Main files |
|---|---|---|
| Set up, resume or hand over a project | `research-workspace` | `PROJECT_SUMMARY.md`, `HANDOFF.md`, `LOG.md` |
| Find out what is known | `literature-review` | `LITERATURE_REVIEW.md`, `refs.bib` |
| Plan and prioritise lines of attack | `strategy-planning` | `STRATEGIES.md` |
| Develop and check proofs | `proof-development` | `PROOF_PROGRESS.md` |
| Run reproducible computations, certify results | `computational-experiments` | `runs/` |
| Search for counterexamples and extremal objects | `construction-search` | `runs/`, candidate records |
| Formalise in a proof assistant (optional) | `lean-formalisation` | `formal/` |
| Write the paper | `paper-writing` | `paper/` |

The stages are not sequential: real projects loop between them. What ties them
together is the vocabulary below and the **Results register** in
`PROJECT_SUMMARY.md`, the single place where the current status of every claim
lives (see `research-workspace`).

## Claim status labels

Give every mathematical statement that is recorded or reported exactly one of these
labels. Use the uppercase strings as written: they are meant to be searchable.

| Label | Meaning | Minimum evidence |
|---|---|---|
| `PROVED` | A complete argument exists in the project files and every step has been checked. | Written proof, every step justified, hypotheses of every cited result checked, no open `GAP` markers. |
| `PROVED-MODULO` | Complete except for explicitly named gaps. | As for `PROVED`, plus a list of `GAP-n` markers, each a precise mathematical statement. |
| `CITED` | Established in the literature. | Exact statement and theorem number read in the source itself; its hypotheses checked against our setting. |
| `CERTIFIED` | A computation with a rigorous certificate. | Exact or validated arithmetic, or a checked proof log. Reproducible from a recorded run, ideally rechecked by an independent checker. |
| `NUMERICAL` | Computational evidence without a certificate. | A recorded run: floating point, sampling, a finite or heuristic search, solver output. |
| `HEURISTIC` | A plausibility argument. | Parameter or dimension count, analogy, partial argument, pattern in data. |
| `CONJECTURE` | A precise statement believed true, without proof. | The statement and the reasons for believing it. |
| `REFUTED` | Shown to be false. | A `PROVED` disproof or a `CERTIFIED` counterexample. |
| `UNRESOLVED` | Attempted, inconclusive. | A record of what was tried and why it did not settle the question. |

### Review is a separate field

Status measures the strength of the evidence. Review records who has checked it.
Record both:

```
review: none | self | independent | human:<name>
```

- `self`: the author (agent or person) re-checked their own work. This is useful but weak, because
  authors tend to see what they intended to write.
- `independent`: checked by a reviewer who saw only the statement and the
  proof or certificate, not the working notes. This means a fresh agent session with no access to
  the notes (a subagent, if the agent supports them) or a human colleague. The
  protocol is in the `proof-development` skill.
- `human:<name>`: record this only when that person, or the user speaking for
  them, says they have checked it. Never infer it.

Do not describe AI-produced work as checked, validated or verified by a human unless
this field says so. "AI-generated, not yet independently reviewed" is an honest and
respectable status. Overstating review damages the trust that makes the work usable.

## Moving between statuses

- **Upgrades need new evidence, not new confidence.** Re-reading your own proof and
  feeling better about it does not turn `PROVED-MODULO` into `PROVED`. Closing the
  gap does.
- `NUMERICAL` becomes `CERTIFIED` only when the *exact object recorded* is
  certified. Certifying a nearby rounded or rationalised object does not count, because
  rounding can change the very property being certified.
- No amount of numerical evidence turns `HEURISTIC` or `CONJECTURE` into `PROVED`.
  Report the evidence and keep the label.
- **Downgrade immediately.** As soon as a step is in doubt, insert a `GAP` marker and
  downgrade, then restore the status when the step is fixed. A cautious label costs little. A wrong
  `PROVED` costs everything built on top of it.
- A status belongs to a *precise* statement. If the argument only covers a special
  case (small degree, generic parameters, characteristic zero, a finite range), say so
  in the statement, or split it into the special case you proved and the general case that is still open.
- When a status changes, update the Results register. If the claim was previously
  stated more strongly, add an entry to the Corrections table (see below).

## Negative results and scope

Keep three kinds of negative statement apart:

1. **"X is false."** This is `REFUTED`. It needs a disproof or a certified counterexample.
2. **"Method M cannot establish X."** This is a theorem about the method and needs its own proof.
3. **"Method M did not find X within scope S."** This is a fact about a search or an attempt, not
   about X.

Most negative results are of the third kind. Record the scope precisely: parameter
ranges, degrees, sample sizes, time budgets, and which parts were exhaustive and which were
sampled. Timeouts, solver failures and bounds that are too weak to decide anything are
`UNRESOLVED`, not exclusions. A strategy marked `CLOSED` (see `strategy-planning`)
means its pre-agreed kill criterion fired within the stated scope. It does not
mean the idea is impossible.

## Gaps

- Mark a gap where it occurs: `GAP-<n>: <precise statement of the missing claim>`.
  Number gaps through the whole project and never reuse a number. Keep the list of
  open gaps current, so that "what is left?" always has a short answer.
- A gap is a precise mathematical claim, not "details to be filled in". If you
  cannot say exactly what is missing, the argument is `HEURISTIC`, not
  `PROVED-MODULO`.
- Some phrases often hide gaps: "clearly", "it is easy to see", "standard arguments
  show", "by compactness", "generically", "without loss of generality",
  "similarly". Use them only where you could write the step out in full if asked.
  Otherwise write it out, or mark a gap.

## Reporting

- Put the status word into the prose: "we proved", "we checked numerically for
  d ≤ 9", "we conjecture". Do not write "we showed" for numerical evidence.
- Report what was done, not what was hoped. Write "an exhaustive search of all 1,686,015
  classes found none", not "there are none".
- Do not round up. "Verified for d ≤ 11" must not become "verified".
- Report failures as prominently as successes. A clearly recorded failure saves
  the next session from repeating it.
- When summarising for the user, start with the strongest *established* result,
  then give the evidence, then the caveats and open gaps.

## Corrections

When an earlier statement turns out to be wrong or too strong:

1. Fix it where it appears, and leave a short dated note at the original location,
   for example `[Corrected 2026-03-14 — see HANDOFF.md, Corrections]`.
2. Add a row to the Corrections table in `HANDOFF.md`:
   `| Date | Earlier statement | Correct statement | Reason | Where fixed |`.
3. Trace what depended on it, using the Evidence column of the Results register and the
   lemma dependency graph in `PROOF_PROGRESS.md`, and re-check or downgrade those claims.

Do not silently overwrite. Later sessions, collaborators and readers may have relied on
the old version, and the record of *why* a tempting claim fails is often worth as
much as a new result. Treat corrections as progress, not as embarrassment.

## Working habits that prevent most errors

- Test a claim on examples before trying to prove it, and test the proof on examples
  after writing it. Many wrong lemmas fail on the first non-trivial example.
- Look for the simplest counterexample first, especially before a long proof
  attempt.
- Check the hypotheses of every cited theorem against the actual situation, including
  conventions (signs, normalisations, which version of a definition).
- Keep exploration apart from the record. Scratch work and probes are fine.
  The project files contain only labelled statements.
- Get independent review for anything that other work will build on.
- Leave decisions that belong to the mathematician to them: changing the target
  statement, accepting a weaker result, leaving a gap open for now, and anything
  that involves contacting people outside the project.

## Bundled reference

- `references/failure-modes.md` is a catalogue of tempting inferences that have
  produced false claims in agent-assisted research, with what to do instead. Read it
  before upgrading a status, when reviewing evidence from a computation or a search,
  and whenever a result seems too good.
