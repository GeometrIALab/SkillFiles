---
name: construction-search
description: Plan, run and report computer searches for counterexamples, extremal examples and explicit constructions in mathematics (graphs, polynomials, real curves, codes, designs, configurations, matrices, functions). Covers climbing from exhaustive small-case enumeration to local and learned search, objectives that cannot be gamed by degenerate solutions, a strict protocol for certifying a candidate before announcing it, and honest, scoped reporting when nothing is found. Use this whenever the agent is asked to find a counterexample, disprove or stress-test a conjecture, beat a known record or bound, construct an object with prescribed properties, or judge whether a search "found nothing", and whenever a candidate counterexample has turned up and is about to be reported.
---

# Construction search

Many research questions come down to "does an object with these properties
exist?" A search can answer *yes* decisively, by producing a certified example.
It can only answer *no* within a stated scope. This skill designs searches so
that a hit means something and a miss is informative, and it stops candidates
from being announced before they are certified.

Run directories, manifests, evidence tiers and certification methods come from
the `computational-experiments` skill; status labels (CERTIFIED, REFUTED,
UNRESOLVED, …) from the `math-research-core` skill. Each search campaign is
a strategy with a kill criterion, managed with the `strategy-planning` skill.

## When to use

- Looking for a counterexample to a conjecture, or stress-testing one before
  trying to prove it.
- Trying to beat a known record (more components, larger code, denser graph,
  better constant) or to construct an object with prescribed properties.
- Deciding what a search that found nothing actually shows.
- A candidate has turned up and you are about to tell someone.

## What this skill reads and writes

| Workspace item | Read | Write |
|---|---|---|
| `LITERATURE_REVIEW.md` | known records, known constructions, known obstructions | gaps found while searching |
| `STRATEGIES.md` | open strategies; the Closed directions table (do not repeat a closed search as such) | a strategy card per campaign, with kill criterion and scope; Closed directions row when it closes |
| `runs/<…>/` | | one run per campaign stage; candidate records in `runs/<…>/candidates/` |
| `PROJECT_SUMMARY.md` (Results register) | | candidates (NUMERICAL), certified hits (CERTIFIED, and REFUTED for the conjecture), scoped negative results |
| `HANDOFF.md` | | everything tried and why it failed; work-accounting ledger |

## Procedure

### 1. Pin down the target

- **State the property as a precise, checkable predicate**, and the
  **acceptance criterion**: which certified check will confirm a hit. For
  example: "a real plane curve of degree d with more than N connected
  components, certified by exact critical-point topology on rational
  coefficients".
- **Collect the known records and obstructions** from the literature. Do not
  search a region that a theorem already rules out: some construction methods
  carry proven upper bounds below the target, and searching inside them can only
  rediscover the record. Write down why the target could exist at all.
- **Identify the symmetries** acting on the search space (coordinate changes,
  scalings, relabellings, sign changes, dualities). Fix a normal form or
  canonical representative. This avoids searching the same object many times,
  and avoids objectives that can drift along orbits without changing anything.
- **Run positive controls before the campaign**: rediscover the known records,
  or find planted solutions. A search that cannot find known examples is not
  evidence that unknown ones don't exist.

### 2. Climb the search ladder

Start at the cheapest rung that could be decisive, and climb only when the
current rung's kill criterion fires. Record the reason each time.

1. **Small cases, exhaustively, with symmetry reduction.** Small cases often
   contain the counterexample, or reveal the structure of extremal examples, and
   they validate the code against known values.
2. **Structured families.** Constructions from the literature with parameters,
   symmetric ansätze (impose a group action), products, gluing and patchworking
   constructions, perturbations of special or degenerate objects. Cheap, and the
   results can be understood.
3. **Random sampling** from a deliberately chosen distribution. Mostly useful
   for calibration (how often do random objects reach the record?) and as seeds:
   random objects are typically far from extremal.
4. **Local search and optimisation** from good seeds, with the normalisation
   fixed.
5. **Exact solvers** (SAT, SMT, ILP) when the property is finite and
   combinatorial. These can also prove that no example exists, within their
   encoding.
6. **Learned or model-guided search** (a generative model trained on good
   examples, program search, reinforcement learning). Expensive; worth trying
   when cheaper rungs plateau and there is structure a model could learn.

`references/search-methods.md` describes each method: when it fits, and how it
fails.

### 3. Design the objective

- **Prefer scores that are** invariant under the symmetries (or computed on the
  normal form), scale-free and bounded, correlated with the true property near
  the threshold, and cheap.
- **Rule out degenerate improvement.** Check whether the score can improve by
  moving towards degenerate objects: scaling to zero, coalescing points,
  shrinking features below the evaluation resolution, letting coefficients blow
  up. Unless degeneration is what you want, fix the normalisation (unit norm,
  bounded box, fixed leading coefficient) and recheck the strict target
  condition, not only the surrogate.
- **Treat surrogates with suspicion.** A continuous surrogate for a discrete
  property (a margin, an eigenvalue, a signed distance) is useful for guiding
  search, but improving it is progress only if the true property improves. Log
  the true property next to the surrogate.
- **Watch the resolution.** If evaluation samples a grid or mesh, a "hit" may
  be an artefact. Re-evaluate top candidates at a finer resolution, and treat
  disagreement as a signal.
- **Expect the search to exploit bugs in the evaluator,** especially learned
  search. Spot-check the best candidates with an independent evaluator early,
  not only at the end.

### 4. Keep diversity and archives

- Keep an archive of the best and of diverse candidates (binned by invariants
  or features), not just the single best. Searches collapse into one basin.
- Remove duplicates using the canonical form.
- Restart from diverse seeds, and record every seed.
- Store what is needed to reproduce each archived candidate: its exact
  representation, the seed and the code version.

### 5. Candidate protocol: when something looks like a hit

Until step 3 below is complete, call it a *candidate* everywhere, including in
conversation. A premature announcement is hard to retract, and a wrong one
costs credibility for every later result.

1. **Freeze.** Store the exact representation (integers, rationals, algebraic
   numbers, combinatorial data) in the run directory, with a SHA-256 hash, and
   create a candidate record from `templates/candidate-record.md`. Do not
   round or simplify after this point; a simplified object is a new candidate.
2. **Re-screen** at higher precision or resolution. Status: NUMERICAL.
3. **Certify** the frozen object against the *whole* acceptance criterion,
   side conditions included (smoothness, nondegeneracy, genericity, degree,
   membership of the family), using a method from the `computational-experiments`
   skill's `references/certification.md`. A partial lower bound without the
   matching upper bound and side conditions is not a hit.
4. **Check it against theory.** If the hit contradicts a published theorem,
   suspect a bug first: re-read the theorem's hypotheses and check them against
   the object. A real contradiction would mean the theorem's hypotheses do not
   apply to your object, or that a published result is wrong. Both need careful
   checking before anything else.
5. **Re-check independently.** Give only the object and the acceptance
   criterion to a fresh agent session with no access to the working notes (a
   subagent, if the agent supports them) or to a human colleague, and have them
   verify it with different code or software.
6. **Then record and report.** Register the object as CERTIFIED and the
   conjecture as REFUTED, with the run directory as evidence and the review
   field matching who did step 5.

### 6. Report negative results with scope and budget

A search that finds nothing must report:

- **scope:** the family, parameter ranges, degrees or sizes, and resolution;
- **budget:** units with counts, following the accounting rules in the
  `computational-experiments` skill (units differ between campaigns and must
  not be added up);
- **what was decided exactly** and what was only screened;
- **how many units ended unresolved** (timeouts, inconclusive enclosures);
- **positive controls:** which known records were reproduced.

Status:

- An exhaustive search of a finite, precisely defined set, with a certified
  decision for every member, supports a CERTIFIED claim of non-existence
  *within that set*.
- Anything less leaves the conjecture's status unchanged. The search result
  goes into the register as NUMERICAL or HEURISTIC evidence with its scope, and
  the strategy is CLOSED with a row in the Closed directions table saying what
  was ruled out and in what scope.
- Do not convert search volume into a probability that a counterexample
  exists, unless the sampling model really supports it.

### 7. When to stop

- The kill criterion on the strategy card fires. Set it in advance: for
  example "no improvement in the true objective after 10^6 evaluations from 50
  diverse seeds", or "the exhaustive enumeration for n ≤ 9 finds nothing".
- The true objective has plateaued over a pre-set budget, and diversity has
  collapsed.
- The search keeps rediscovering the same structures. This is often a sign of
  a theorem. Hand the pattern over to the `strategy-planning` and
  `proof-development` skills: a plateau that can be explained becomes either an
  obstruction to prove or a hint about where else to look.

## Rules, and why they matter

- **No announcement before certification.** Floating-point screens and sampled
  evaluations are least reliable exactly where counterexamples hide: near
  degenerate configurations and at multiple scales.
- **REFUTED needs a CERTIFIED counterexample** (or a proof). A NUMERICAL
  candidate leaves the conjecture as it was, with a note in the register.
- **Never repeat a closed direction as such.** Read the Closed directions table
  first. Revisit a closed direction only with a stated reason why the new
  attempt differs (a larger scope, a different encoding, a new idea).
- **Fix normalisations before optimising.** An objective with a degenerate
  direction will find it.
- **Keep implementation failures apart from search outcomes.** A crash or a
  timeout is not a negative result.
- **Compare stochastic methods only across several seeds.** One run per method
  shows little; report the spread or call the comparison anecdotal.

## Common failure modes

- Announcing a candidate after a floating-point screen.
- Simplifying coefficients after certification and reporting the simplified
  version.
- An objective "improving" through degeneration or rescaling.
- Searching inside a family that a known theorem bounds below the target.
- A "hit" that is an artefact of the sampling resolution.
- A change of coordinates that does not preserve the property, applied for
  convenience.
- No positive controls, so a failed search says nothing.
- Treating improvements in a surrogate score as progress on the true property.
- Restarts that double count units, or overlap with earlier runs without saying
  so.
- Learned search exploiting a bug in the evaluator.

## Bundled files

- `references/search-methods.md`: each search method, when it fits, and how it
  fails. Read it when choosing the first rung or switching rungs.
- `templates/candidate-record.md`: fill one for every candidate that survives
  the first screen, and keep it in the run directory under `candidates/`.
