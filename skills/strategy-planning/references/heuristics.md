# Exploration moves for generating strategies

A catalogue of Pólya-style moves for producing candidate strategies. Each entry
gives what the move is, what it is good for, a standard example, and how to
turn it into a cheapest decisive test for a strategy card. Use it when the
candidate list is thin, when every active strategy has closed, or as a
checklist at the start of a project.

Evidence produced by these moves has the status label it earns (see
`math-research-core`). Patterns in small cases are `NUMERICAL`; analogies and
counts are `HEURISTIC` until proved.

Contents
1. Specialise
2. Small cases and data
3. Extreme and equality cases
4. Generalise
5. Strengthen the induction
6. Invariants and monovariants
7. Change the representation
8. Work backwards: necessary conditions
9. Minimal counterexample
10. Look seriously for a counterexample
11. Auxiliary or relaxed problem
12. Analogy with a neighbouring field
13. Drop a hypothesis
14. Use every hypothesis
15. Decompose
16. Exploit or impose symmetry
17. Deform from a known case
18. Know the barriers

---

## 1. Specialise

**What.** Prove or test the statement in a special case: low dimension, low
degree, a specific family, extra symmetry, or a field where computation is easy.

**Good for.** Building intuition, finding the right form of the general statement, and cheap
counterexamples. A special case that resists is a warning about the general one.

**Example.** Before attacking a statement about all smooth projective varieties, settle it for
curves; before a statement about all graphs, check every graph on at most eight vertices.

**As a test.** "Verify the statement for all cases with n ≤ N by exact computation; kill if any fails."

## 2. Small cases and data

**What.** Compute the quantity of interest for the first several cases, and look for a pattern.

**Good for.** Guessing formulae, bijections and the true size of a bound; identifying the objects
via the OEIS or field databases.

**Example.** Counts 1, 2, 5, 14, 42, 132 suggest the Catalan numbers, and hence a bijection with
binary trees or Dyck paths, which suggests a proof.

**As a test.** "Compute cases 1..N; if the data contradict the conjectured formula, close."
Agreement on finitely many terms is `NUMERICAL`, not a proof.

## 3. Extreme and equality cases

**What.** Look at the boundary of the parameter range, at degenerate configurations, and at the
cases where an inequality is sharp.

**Good for.** Understanding what a proof must "see". The structure of the extremisers often
dictates the method.

**Example.** Equality in the AM–GM inequality holds exactly when all the numbers are equal, which
suggests proofs by convexity or by smoothing towards equal values. In extremal graph theory, the
balanced complete multipartite extremisers in Turán's theorem suggest symmetrisation arguments.

**As a test.** "Identify all equality cases of the conjectured bound in small cases; if they do not
fit the proposed mechanism, revise or close."

## 4. Generalise

**What.** Prove a more general statement, which may be easier because the general setting exposes
the structure, or allows induction or a parameter (the "inventor's paradox").

**Good for.** Problems where the specific instance hides the mechanism.

**Example.** To evaluate ∫₀^∞ (sin x)/x dx, introduce I(a) = ∫₀^∞ e^{−ax}(sin x)/x dx,
differentiate in a, solve the resulting simple equation, and let a → 0.

**As a test.** "Check that the generalisation holds in the small cases from move 2; if it fails
there, it is false and the strategy closes."

## 5. Strengthen the induction

**What.** When induction fails because the hypothesis is too weak to carry the step, prove a
stronger statement instead.

**Good for.** Bounds, inequalities and constructions built step by step.

**Example.** "Σ_{k≤n} 1/k² < 2" does not induct directly. "Σ_{k≤n} 1/k² ≤ 2 − 1/n" does,
because 1/(n+1)² ≤ 1/n − 1/(n+1).

**As a test.** "Find a strengthened statement that holds numerically for n ≤ N and whose inductive
step can be checked; kill if no candidate survives the data."

## 6. Invariants and monovariants

**What.** Find a quantity that is preserved (an invariant) or moves in one direction (a
monovariant) under the operations in the problem.

**Good for.** Impossibility results, upper bounds, termination proofs, and showing two objects
differ.

**Examples.**
- The colouring argument for the mutilated chessboard.
- The Euler characteristic.
- Harnack's theorem: a smooth real plane curve of degree d has at most g + 1 connected
  components, where g = (d−1)(d−2)/2.

**As a test.** "Compute the candidate invariant on known examples; if it does not separate the cases
that need separating, close."

## 7. Change the representation

**What.** Re-encode the problem: different coordinates, a transform, a dual object, a combinatorial
shadow.

**Good for.** Making hidden structure visible, and turning hard operations into easy ones.

**Examples.**
- Generating functions turn recurrences into algebraic or differential equations.
- The Fourier transform turns convolution into multiplication.
- A polynomial can be studied through its Newton polytope (toric and tropical degenerations,
  patchworking).
- A graph can be studied through its adjacency matrix (spectral bounds).
- Projective and affine charts expose different behaviour at infinity.

**As a test.** "Re-derive a known special case in the new representation; if that is no easier, the
representation is not helping."

## 8. Work backwards: necessary conditions

**What.** Assume the object or proof exists and derive what it must satisfy.

**Good for.** Ruling out cases, shrinking a search space, finding the shape of a construction.

**Example.** The Bruck–Ryser theorem: if a finite projective plane of order n exists and
n ≡ 1 or 2 (mod 4), then n is a sum of two squares. This rules out infinitely many orders without
any search.

**As a test.** "Derive necessary conditions; if they exclude the target region outright, record that
as a result (it may be a theorem) and close the existence strategy there."

## 9. Minimal counterexample

**What.** Suppose a counterexample exists, take a smallest one, and derive structure until there is
a contradiction or a very restricted family remains.

**Good for.** Structural statements about graphs, groups, and finite configurations generally.

**Example.** The classical proof of the five colour theorem: a minimal non-5-colourable planar graph
must have a vertex of degree at most five, and a recolouring argument removes it.

**As a test.** "Derive k structural properties of a minimal counterexample; if they reduce the
problem to a finite check, run it."

## 10. Look seriously for a counterexample

**What.** Try to disprove the statement: random search, structured search, extreme examples,
examples from neighbouring problems (see the `construction-search` skill).

**Good for.** Saving months on a false statement. When the search fails *in a structured way*, the
reason it fails often suggests the proof.

**Example.** Euler's conjecture on sums of like powers was refuted by a computer search that found
27⁵ + 84⁵ + 110⁵ + 133⁵ = 144⁵.

**As a test.** "Search a stated family up to a stated size; record the scope; if nothing is found,
record what blocked each near-miss."

## 11. Auxiliary or relaxed problem

**What.** Solve an easier related problem first: over ℂ instead of ℝ, the linearised or infinitesimal
version, a continuous relaxation, an averaged or probabilistic version.

**Good for.** Obtaining bounds and existence results, and isolating where the real difficulty is.

**Example.** A random graph on 2^{k/2} vertices has, with positive probability, no clique or
independent set of size k. This gives an exponential lower bound for the diagonal Ramsey numbers
without constructing any graph.

**As a test.** "Solve the relaxed problem; if even the relaxation fails to reach the target, the
original cannot, and the strategy closes (record the relaxation gap)."

## 12. Analogy with a neighbouring field

**What.** Transfer a statement, technique or conjecture from a related setting.

**Good for.** Suggesting statements and methods.

**Examples.**
- Function-field analogues of number-theoretic statements (the Riemann hypothesis for curves over
  finite fields is a theorem).
- Discrete analogues of Riemannian geometry, such as Cheeger inequalities for graphs.
- Tropical geometry as a combinatorial shadow of algebraic geometry.

**Caution.** An analogy is a source of strategies, not of results. List the hypotheses of the
original theorem and check each in the new setting, recording them under "Limits of analogies" in
the literature review. Until then the transferred statement is `HEURISTIC`.

**As a test.** "Check the hypothesis of the original theorem most likely to fail here; if it fails,
close or re-scope."

## 13. Drop a hypothesis

**What.** Remove or weaken one hypothesis and find where the statement breaks.

**Good for.** Learning which hypotheses are essential and therefore where the proof must use them.
It also produces examples that sharpen the statement.

**Example.** Without compactness, a continuous function need not attain its maximum (consider
1/x on (0, 1)). So any proof of a maximum principle–type statement must use compactness or a
replacement for it.

**As a test.** "For each hypothesis, find a counterexample to the statement without it; a hypothesis
with no such counterexample may be removable."

## 14. Use every hypothesis

**What.** Check which hypotheses a proof attempt has actually used.

**Good for.** Spotting flawed attempts. If a hypothesis was not used, either the statement holds more
generally (check that against known counterexamples) or the attempt has a gap.

**As a test.** "List where each hypothesis enters the argument; any unused hypothesis triggers a
check of the more general statement."

## 15. Decompose

**What.** Split the problem into cases, regimes, scales or local pieces, each handled by the method
that suits it. Then assemble the pieces (local to global).

**Good for.** Problems with different behaviour in different regimes (small and large parameters,
generic and special configurations).

**As a test.** "Identify the hardest piece; attack it first. If it cannot be done, the decomposition
does not help."

## 16. Exploit or impose symmetry

**What.** Use the problem's symmetry to reduce a search or a computation, or impose extra symmetry
to find structured candidates.

**Good for.** Searches and extremal constructions, and quotienting a space to make it finite or
small.

**Caution.** Extremal objects are often, but not always, symmetric. Imposing symmetry can exclude the
optimum. A negative result under imposed symmetry has exactly that scope.

**As a test.** "Search the symmetric sub-family; record its scope; compare against the best
asymmetric examples known."

## 17. Deform from a known case

**What.** Connect the problem to a solved case by a path of problems, and show the property persists
along the path. This is the method of continuity: the set of parameters where it holds is non-empty,
open and closed.

**Good for.** Existence theorems in analysis and geometry; deformation and homotopy arguments in
topology and algebraic geometry.

**Example.** The continuity method for nonlinear elliptic equations: openness comes from the
implicit function theorem, closedness from a priori estimates.

**As a test.** "Prove openness (usually the easier part); identify the a priori estimate needed for
closedness and test it numerically along the path."

## 18. Know the barriers

**What.** Find results that show certain methods cannot reach the target.

**Good for.** Pruning strategies before any work is done.

**Examples.**
- The parity problem in sieve theory: sieves alone cannot distinguish integers with an even
  number of prime factors from those with an odd number.
- The relativisation and natural-proofs barriers in complexity theory.
- In geometric and combinatorial constructions: a theorem that bounds what a given construction
  technique can achieve.

**As a test.** "Before activating a strategy, search for barrier results for its method (see
`literature-review`). If one applies, do not activate; record why in the closed-directions table."
