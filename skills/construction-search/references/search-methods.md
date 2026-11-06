# Search methods for constructions and counterexamples

For each method: when it fits, how to use it well, and how it typically fails.
The quick table helps pick a starting rung; the sections give details.

## Quick choice

| Situation | Start with |
|---|---|
| Finite combinatorial objects, small sizes | §1 exhaustive enumeration with symmetry reduction |
| Finite objects, the property is a set of constraints, sizes too big to enumerate | §2 SAT / SMT / ILP |
| Continuous parameters, cheap evaluation, no idea where to look | §3 random sampling for calibration, then §4 local search |
| A good seed and a smooth-ish objective | §4 local search |
| Several distinct good regions, rugged landscape | §5 evolutionary and quality-diversity search |
| Cheaper methods plateau; good examples share learnable structure | §6 learned or model-guided search |
| Objects naturally built step by step | §7 reinforcement learning (after trying §4–§6) |
| Known special or degenerate objects nearby | §8 continuation, perturbation and gluing |
| A symmetry or product structure is plausible | §9 structured ansätze |

## Contents

1. Exhaustive enumeration with symmetry reduction
2. SAT, SMT and integer linear programming
3. Random sampling
4. Local search
5. Evolutionary and quality-diversity search
6. Learned or model-guided search
7. Reinforcement learning
8. Continuation, homotopy, perturbation and gluing
9. Structured ansätze: symmetry, products, reduction

---

## 1. Exhaustive enumeration with symmetry reduction

**When it fits:** finite objects (graphs, designs, matrices with bounded
entries, sign patterns, triangulations, small codes) at sizes where the number
of objects up to isomorphism is manageable.

**How:**
- Generate one representative per isomorphism class: orderly generation
  (only extend canonical objects), or canonical augmentation (accept an
  extension only if it is the canonical way to build the larger object), using
  canonical labelling software such as nauty, Traces or bliss.
- Prune with properties that are inherited by sub-objects (hereditary
  properties): if a sub-object fails, every extension fails.
- Decide the property for each representative exactly.

**Checks:** compare counts for small sizes with known values (OEIS, published
tables). Where possible, check the orbit-counting identity (the sum of
|G|/|Aut(X)| over representatives equals the number of labelled objects).

**Failure modes:**
- Pruning on a property that is not actually hereditary, which silently
  removes valid objects.
- An encoding whose notion of isomorphism is not the intended one (too coarse
  merges distinct objects; too fine wastes time but is safe).
- The count grows faster than expected; estimate it in advance (from known
  sequences or by sampling the search tree).

## 2. SAT, SMT and integer linear programming

**When it fits:** the property is a finite set of constraints on discrete
variables (Ramsey-type colourings, designs, codes, tilings, combinatorial
configurations), and the space is too large to enumerate directly.

**How:**
- Encode carefully, with standard encodings for cardinality and
  at-most-one constraints.
- Add symmetry-breaking constraints (for example lexicographic-leader
  constraints) to cut the search, but only ones you can *prove* keep at least
  one member of every solution orbit.
- For hard instances, split the problem into cubes and solve them separately
  (cube-and-conquer), recording a proof that the cubes cover everything.
- Ask for proof logs (DRAT/LRAT) so UNSAT answers can be checked
  independently.

**Failure modes:**
- Encoding bugs. Test the encoding on small instances with known answers,
  both satisfiable and unsatisfiable.
- Unsound symmetry breaking turns a satisfiable problem into a false "UNSAT".
- ILP tolerances accept nearly-integral or nearly-feasible solutions; check
  solutions exactly.
- An UNSAT result without a checked proof is UNRESOLVED as a certificate (it
  is still useful as a screen).

## 3. Random sampling

**When it fits:** calibration ("how often does a random object reach the
record?"), generating diverse seeds for local search, and estimating typical
behaviour.

**How:** choose the distribution deliberately and record it: for example
Gaussian or invariant ensembles for polynomial coefficients, Erdős–Rényi or
random regular models for graphs, uniform distributions over a normalised
parameter box.

**Failure modes:**
- Random objects are typically far from extremal. For many questions about
  maximal counts (components, cycles, independent sets) the typical random
  object is nowhere near the maximum, so pure sampling almost never finds
  records.
- Results depend strongly on the distribution; a different ensemble can change
  the picture completely.
- Volume is not evidence of absence: a billion samples from a distribution
  that rarely produces extremal objects say little about whether one exists.

## 4. Local search

**When it fits:** you have a reasonable starting point and a way to make small
changes and score them.

**Methods:**
- Discrete: hill climbing, simulated annealing, tabu search, large
  neighbourhood search (destroy part of the object and rebuild it).
- Continuous: gradient-free methods (Nelder–Mead, CMA-ES, pattern search), or
  gradient methods on a differentiable surrogate.

**How:** fix the normalisation first. Use many restarts from diverse seeds.
Track the true property next to any surrogate. Tune the move set to the
structure of the problem; it matters more than the choice of algorithm.

**Failure modes:**
- Getting stuck in local optima, which makes restart diversity essential.
- Drifting towards degenerate objects that score well (shrinking features,
  scaling, coalescing points).
- The surrogate improves while the true property does not.
- Comparing methods on a single run each.

## 5. Evolutionary and quality-diversity search

**When it fits:** rugged landscapes with several distinct good regions;
problems where crossing over parts of good solutions makes sense.

**Methods:** genetic algorithms; quality-diversity methods such as MAP-Elites,
which keep the best object in each cell of a grid of features, so the archive
stays diverse by construction.

**Failure modes:**
- Premature convergence to one family when diversity is not enforced.
- Expensive evaluation multiplied by large populations.
- Crossover that produces invalid objects most of the time; design operators
  that respect the structure.

## 6. Learned or model-guided search

**When it fits:** cheaper methods have plateaued, and the good examples found
so far seem to share structure a model could learn and extrapolate.

**Patterns:**
- *Local search plus a learned generator:* run local search, keep the best
  objects, train a generative model (for example a small transformer on a
  sequence encoding of the objects) on them, sample new starting points from
  the model, improve them with local search, and repeat.
- *Program search:* instead of searching for objects, search for short programs
  that generate objects. A language model proposes new or modified programs,
  an evaluator scores the objects they produce, and a population of the best
  programs is kept and evolved. The programs found are often readable, which
  can suggest a general construction.
- *Surrogate models:* train a cheap predictor of the score to filter
  candidates before expensive evaluation.

**Failure modes:**
- The generator exploits bugs or loopholes in the evaluator. Use an
  independent evaluator for top candidates early.
- High cost, with gains on small problems that well-tuned local search often
  matches. Run a strong simple baseline with the same budget.
- Hard to reproduce. Record the model, its version or weights, the prompts or
  training data, the sampling settings and the seeds.
- Every output still needs the full candidate protocol; a learned method gives
  no extra trust.

## 7. Reinforcement learning

**When it fits:** objects are naturally built step by step (add an edge, place
a point, choose the next coefficient), and the final property can be scored.

**Failure modes:**
- Sparse rewards (only the finished object is scored) make learning slow.
- Reward shaping invites gaming.
- Often outperformed by simpler local search at equal compute; compare against
  a baseline before investing.

## 8. Continuation, homotopy, perturbation and gluing

**When it fits:** known special, singular or degenerate objects are close to
what you want, and there is theory describing how features appear under
perturbation.

**Patterns:**
- *Small perturbation of a singular object:* smooth the nodes of a singular
  curve or surface in a controlled way to create components; perturb a
  degenerate configuration in chosen directions.
- *Gluing and patchworking:* build objects from local pieces with a
  combinatorial gluing rule (for example Viro-type patchworking of real
  algebraic curves). These come with theorems saying when the glued object has
  the predicted topology.
- *Parameter continuation:* follow a family through a parameter and track
  events (births and deaths of components, bifurcations, collisions).

**Failure modes:**
- The perturbation regime is not controlled. Higher-order terms can change the
  outcome, so the "small enough" parameter must be certified, not assumed.
- Events between steps are missed. Locate the events exactly (for example as
  roots of a discriminant) instead of stepping blindly.
- Gluing theorems have nondegeneracy hypotheses. Check every one for the
  actual pieces, especially along edges and boundaries, where they most often
  fail.

## 9. Structured ansätze: symmetry, products, reduction

**When it fits:** extremal examples often have symmetry or product structure,
and imposing it shrinks the search space dramatically.

**Patterns:**
- Impose invariance under a group (cyclic, dihedral, permutation) and search
  only the invariant subfamily.
- Products, tensor constructions, and lifts of small examples to larger ones.
- Reduction modulo a prime or to a combinatorial skeleton to find candidate
  structure, then lift and verify.

**Failure modes:**
- The symmetric subfamily may be provably bounded below the target. Check the
  literature for bounds on symmetric examples before searching.
- A structure found in a reduction may not lift. Treat it as a candidate and
  certify the lifted object itself.
