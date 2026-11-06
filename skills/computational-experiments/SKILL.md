---
name: computational-experiments
description: Run mathematical computations so their results can be trusted, reproduced and cited. Covers one fresh run directory and manifest per experiment, evidence tiers from floating-point screen to certified result, exact or interval re-verification, honest accounting of the work done, and correct recording of outcomes in the project's results register. Use this whenever the agent is about to launch or has just run a computer search, numerical experiment, symbolic computation, enumeration, parameter sweep, optimisation or verification in a research project (including quick probes whose output might later be quoted), and whenever a computed number, count, bound, root, certificate or "no counterexample found" is about to be reported or used as evidence for a mathematical claim.
---

# Computational experiments

Computation produces two kinds of output: evidence that can be cited, and
numbers that only look like evidence. This skill keeps them apart. Every run
leaves a directory that explains itself, every reported number carries its
evidence tier, and nothing already recorded is silently altered. The aim is
that a colleague, or the agent itself in three weeks' time after the context
has been lost, can say exactly what was computed, with which code, and how
much it proves.

Status labels (PROVED, CERTIFIED, NUMERICAL, UNRESOLVED, …) and the review
field are defined in the `math-research-core` skill; the workspace layout is
defined in the `research-workspace` skill. For searches aimed at
counterexamples or extremal objects, also use the `construction-search`
skill.

## When to use

- Before launching any computation whose result might be quoted: a search,
  sweep, enumeration, numerical solve, symbolic simplification, optimisation
  or certification.
- When an exploratory probe gives an interesting result and is about to be
  relied on.
- When reporting a computed result anywhere: in conversation, in the Results
  register, in `HANDOFF.md`, or in a paper.
- When resuming, auditing or re-interpreting earlier runs.

## What this skill reads and writes

| Workspace item | Read | Write |
|---|---|---|
| `runs/<YYYY-MM-DD>_<slug>/manifest.json` | when resuming or auditing | one per run; status and summary at the end |
| `runs/<…>/` (other files) | | every output of that run, and nothing from other runs |
| `code/` | | maintained, version-controlled code that runs call |
| `probes/` | | throwaway exploratory scripts, one README line each |
| `PROJECT_SUMMARY.md` (Results register) | before reporting | rows for claims the run bears on |
| `STRATEGIES.md` | the strategy and kill criterion being tested | the outcome of the test |
| `LOG.md` | | one line when a run starts and when it ends |
| `HANDOFF.md` | | reproduction commands, the work-accounting ledger, corrections |

## Procedure

### 1. Before running: decide what the run can show

1. **State the question in one sentence**, and the strategy (`S`-id) and claims
   (`R`-ids) it bears on. If the question cannot be stated, the computation is a
   probe: put the script in `probes/` and treat anything it says as a hint at
   most.
2. **Decide in advance what each outcome will mean**: what counts as a hit, what
   counts as an exclusion, what counts as inconclusive. Write this in the
   manifest's `question` and `notes`. Deciding after seeing the data invites
   reading the output in whichever way is most encouraging.
3. **Choose the evidence tier the run is aiming for.** A screen gives NUMERICAL
   evidence; a certified computation gives CERTIFIED evidence. If you will
   want a certificate, choose the certification method now (see
   `references/certification.md`). Certification bolted on afterwards often
   fails because the exact data it needs was never stored.
4. **Choose tools** (see `references/tools.md`), preferring ones that can give
   exact or validated answers for the step that matters.
5. **Run a positive control**: a small instance with a known answer. A pipeline
   that cannot reproduce a known case is not evidence about unknown ones.

### 2. Create the run

Use the bundled script, from the project root:

```bash
python3 <skill-dir>/scripts/new_run.py create deg6-pencil-sweep \
    --purpose "Screen degree-6 pencils for configurations above the record" \
    --question "Does any pencil in family F reach N+1? Hit = certified N+1; exclusion = certified upper bound <= N" \
    --strategy S3 --claims R4 R7 \
    --hash code/sweep.py code/certify.py --packages numpy sympy \
    --command "python3 code/sweep.py --config runs/<run>/config.json"
```

This creates `runs/<today>_deg6-pencil-sweep/manifest.json`, records the git
commit and whether the working tree is dirty, the Python version and machine,
SHA-256 hashes of the named files and versions of the named packages. It
refuses to reuse an existing directory. Then fill in `parameters` and `seeds`
(or save a config file in the run directory and list it in `outputs`).

Why one fresh directory per experiment: old outputs are the evidence for
whatever was concluded from them. Overwriting destroys the audit trail and
mixes outputs from different code versions. Re-running "the same
experiment" with changed code or parameters is a new run.

Commit the code before a run you might cite. If the tree is dirty, the
manifest says so, and the file hashes are what tie the result to the code.

### 3. While it runs

- **Long runs** (more than a few minutes) go in the background, logging to a
  file inside the run directory, writing checkpoints to the run directory at
  regular intervals. Mark the run as running with
  `new_run.py start <run-dir>`.
- **Make resumption idempotent.** Record which work units are complete (for
  example a file of completed chunk indices), so a restart neither counts a
  unit twice nor skips one. Write down how to resume in the manifest `notes`.
- **Never let two processes write one run directory.** If it happens by
  accident, record it in `notes` with the affected counts; do not tidy it up
  silently.

### 4. After it runs

1. Close the run: `new_run.py finish <run-dir> --status completed --summary "…"`
   (or `failed` / `interrupted`). This sets the finish time and status only.
2. Write the `result_summary` at the tier actually reached ("screen: 3
   candidates at float precision", not "found 3 examples").
3. Fill `accounting` with units and scope (see the rules below).
4. Record implementation failures separately from mathematical outcomes (see
   below), rerun them as new runs, and never count a crashed unit as a negative
   result.
5. Update the Results register, the strategy card in `STRATEGIES.md`, and add a
   line to `LOG.md`.

### 5. Promotion: from screen to certificate

Evidence comes in three tiers:

| Tier | What it is | Status it supports |
|---|---|---|
| 1. Screen | floating point, sampling, heuristic solvers, plots | NUMERICAL |
| 2. Validated re-verification | the recorded exact object re-checked with exact arithmetic, interval/ball arithmetic or a certified algorithm | CERTIFIED (`review: self`) |
| 3. Independent check | a second implementation, other software, or an independent checker program verifying a certificate, run by a fresh agent session with no access to the working notes (a subagent, if the agent supports them) or a human colleague | CERTIFIED (`review: independent` or `human:<name>`) |

When promoting:

- **Certify the object you will report**, stored exactly in the run directory
  (integers, rationals, algebraic numbers, combinatorial data), not a nearby
  float. If you round or simplify it for presentation, the simplified object is
  a different object and needs its own certificate.
- **Check the whole acceptance criterion**, including side conditions such as
  smoothness, nondegeneracy, genericity and membership of the required family.
  A partial lower bound without a matching upper bound and the side conditions
  is not a certificate.
- **Keep the checker independent of the search code.** A checker that reuses
  the code path that produced the candidate inherits its bugs.
- **Record the trusted base**: which software, solver or checker, and any
  hypotheses the computation relies on (for example a result conditional on
  the generalised Riemann hypothesis).

A certification is itself a run, with its own directory and manifest.

## Rules, and why they matter

**A screen result is NUMERICAL until certified.** Floating point and sampling
fail quietly in exactly the delicate situations research targets:
near-degenerate configurations, tangencies, features at several scales. More
digits or a finer grid make an error less likely, but they prove nothing.

**Timeouts, weak bounds and non-convergence are UNRESOLVED, not exclusions.** A
case is excluded only by a supported bound at or below the target, or by an
exact decision. Report how many units ended unresolved, alongside the hits and
the exclusions.

**Never modify finished evidence.** Once a run is finished its outputs are
read-only. If it later turns out to be wrong, append a note to its manifest
("superseded by `runs/…`: reason"), add a row to the Corrections table in
`HANDOFF.md`, and make a new run. Deleting or rewriting the old outputs makes
it impossible to tell later what an earlier conclusion was based on.

**"Exhaustive" needs a finite, precisely defined set in which every case was
decided.** Otherwise say "no hit within scope …" and give the family, parameter
ranges, sizes, resolution and the number of units actually completed. "We
searched extensively" is not a scope.

**Results on samples are about the samples.** An exact algorithm on sampled
data (exact connectivity of a sampled grid, exact rank of a sampled matrix)
gives an exact answer about the sample, not about the underlying object.

**Conserved quantities check consistency; they do not show completeness.** A
matching Euler characteristic, degree, index sum or Morse count is consistent
with a missing pair of features that cancel. Use such checks to catch errors,
never as proof that nothing was missed.

**Fix normalisation before optimising.** An objective that can improve by
scaling, shrinking or letting the object degenerate will do so. Fix a scale and
recheck the strict target condition, not only the surrogate score.

**Coordinate changes must preserve the property under study.** A
transformation that does not commute with the construction (for example a
projective change of coordinates applied to an affine construction) can create
or destroy features. Check this before using a change of coordinates to
simplify a computation.

**Account for work with units and scope, and never add up counts that measure
different things.** "Random samples evaluated", "distinct exact objects
certified", "intervals of a parameter pencil" and "optimiser restarts" are
different units. Overlapping campaigns, pilots and reruns cannot be added
together. Keep a ledger table in `HANDOFF.md`:

| Ledger | Count | Unit | Scope | Overlaps with |
|---|---:|---|---|---|

Do not turn search volume into a probability ("the chance a counterexample
exists is below …") unless the sampling model and independence genuinely
support it, which they rarely do. A large amount of computation without a hit
is evidence about the search's reach as much as about the conjecture.

**Keep implementation failures apart from mathematical results.** Crashes,
serialisation errors, a file pattern that matched log files, a resumed job that
skipped a chunk: record each in the manifest `notes` and in `HANDOFF.md`, rerun
as a new run, and make sure none was counted as a decided case.

**Probes are for intuition; code is for evidence.** `probes/` holds quick,
untested scripts, each with one line in `probes/README.md` saying what it was
for and on what date. Anything a probe found can be quoted as HEURISTIC at
most. To rely on it, reimplement or move the code into `code/`, test it on
known cases, and run it as a proper run.

**Record the environment.** Library versions change floating-point results,
default orderings and the internal random choices of some algorithms. Two runs
that differ only in environment can disagree.

**Do not draw conclusions from single replicates of stochastic methods.**
Comparing two randomised methods on one run each tells you little. Use several
seeds and report the spread, or report the comparison as anecdotal.

## Reporting computed results

In prose, attach the status, the run and the scope:

> No configuration in family F with parameters in [0, 1]^3 at grid spacing
> 10^-3 exceeds N components [NUMERICAL] (run `runs/2026-11-02_f-sweep`,
> 1.2 × 10^6 grid points, 312 points unresolved).

In the Results register (`PROJECT_SUMMARY.md`):

| ID | Claim | Status | Review | Evidence | Updated |
|---|---|---|---|---|---|
| R7 | Object X has exactly 11 components | CERTIFIED | self | `runs/2026-11-03_x-certify` (interval topology, exact rational input) | 2026-11-03 |

A claim that a computation supports can only be as strong as the weakest tier
in its chain: if the input object was taken from a screen and never fixed
exactly, a certified computation on its float approximation certifies the
approximation, not the object.

## Common failure modes

- Re-rounding coefficients to "clean" values after a screen, which destroys a
  small or multi-scale feature, and then reporting the cleaned version.
- Calling a component count from a sampled grid "exact" because the
  connectivity algorithm was exact.
- Treating a solver timeout or a failed convergence as "no solution".
- Reporting a partial lower bound ("at least k found") as the count, without a
  matching upper bound and nondegeneracy checks.
- Reading the verifier's one-line summary instead of the checks it actually
  performed.
- An optimisation "improving" by driving the object towards degeneracy.
- Double counting after a restart, or silently dropping the overlap.
- Changing code mid-campaign without starting a new run, so that outputs from
  two versions are mixed.
- Counting work units from different campaigns as if they were comparable.
- Promoting a probe's output to a claim without rerunning it through
  maintained code.

## Bundled files

- `scripts/new_run.py`: creates run directories and manifests and closes runs
  (`create`, `start`, `finish`). Run it with `--help` for options. Use it for
  every run you might cite.
- `templates/manifest.json`: the manifest format with every field explained.
  Read it when filling a manifest by hand, or when adding fields the script
  does not prefill (parameters, seeds, certificate, accounting).
- `references/tools.md`: what the main mathematical software is good and bad
  at, and how to get exact or validated answers from each. Read it when
  choosing tools for a run.
- `references/certification.md`: certification techniques by problem type,
  with what each certifies and its typical pitfalls. Read it before planning a
  CERTIFIED run or promoting a NUMERICAL result.
