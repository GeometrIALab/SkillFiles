# Verification checklist

Run this on every lemma before it is marked PROVED, and use it when reviewing
anyone's argument. Not every item applies to every lemma. Go through all of them
anyway, and record in the lemma's "Checks done" block which ones applied and what
you found. "Not applicable" is a valid answer; skipping an item silently is not.

## Contents

- A. The statement
- B. Each step
- C. Cited results
- D. Global sanity checks
- E. Recording

---

## A. The statement

- [ ] **Quantifiers.** Every quantifier is explicit and in the intended order.
  "∀ε ∃δ" is not "∃δ ∀ε"; "for every x there is a neighbourhood" is not "there is
  a neighbourhood of every x of uniform size".
- [ ] **Setting.** Each of these is stated wherever it matters:
  - ground field and characteristic; real or complex
  - smooth or singular; compact or not; with or without boundary; connected or not
  - regularity class (C^k, smooth, analytic, Sobolev)
  - range of dimension, degree or rank
  - finite or infinite; bounded or unbounded
- [ ] **"Generic", "general", "almost all".** Say which parameter space, and
  whether it means open dense, Zariski open and non-empty, full measure, or a
  countable intersection of open dense sets. Each gives a different theorem.
- [ ] **Degenerate and boundary cases.** Is the statement true, or deliberately
  excluded, in each of these cases?
  - n = 0 and n = 1; the empty set; the trivial group
  - lowest degrees; equality cases of inequalities
  - singular members of a family; boundary of the parameter domain
  - points at infinity; zero or repeated eigenvalues
- [ ] **Examples.** The statement has been checked on at least one non-trivial
  example and one degenerate example, and the outcomes are recorded.
- [ ] **Fit with the project.** The statement is the one the acceptance criterion
  needs, or the mismatch is recorded.

## B. Each step

- [ ] **Justification named.** By definition, by an earlier step, by a lemma, by a
  cited theorem with its number, or by a run ID with its status.
- [ ] **Direction.** The implication is used in the direction it holds, not its
  converse.
- [ ] **Uniformity.** For every constant, radius, δ or N, write down what it
  depends on. Check that nothing later varies a quantity the constant was allowed
  to depend on.
- [ ] **Interchange of operations.** Swapping limits with sums, integrals,
  derivatives or each other is justified by a named result (dominated or monotone
  convergence, uniform convergence, Fubini/Tonelli, differentiation under the
  integral sign) whose hypotheses are checked.
- [ ] **Existence.** Every "let x be the minimiser / the solution / the limit" is
  backed by an existence argument: compactness, coercivity, lower semicontinuity,
  completeness.
- [ ] **Well-definedness.** If a construction involves choices (representatives,
  bases, branches of log or square root, orderings, cut-offs), the result is shown
  to be independent of them, or the choice is fixed and stated.
- [ ] **Forbidden operations.** No division by a quantity that might vanish. No
  logarithm or real square root of a quantity that might be non-positive. No
  inverse of a matrix or operator that might be singular. No normalisation of a
  vector that might be zero.
- [ ] **Signs and normalisations.** Compare the conventions of every formula
  imported from a source with ours. Common traps:
  - the sign of the Laplacian; the sign of curvature or of the Hodge star
  - Fourier transform normalisation; factors of 2π and 2
  - metric signature; orientation
  - indexing from 0 or from 1
  - "positive" meaning > 0 or ≥ 0
- [ ] **Counts.** Recompute every dimension, degree, index, rank or codimension
  count independently. For a transversality or "expected dimension" argument, name
  the map, its source and target, and the theorem that gives transversality, and
  show the relevant set is non-empty.
- [ ] **Local to global.** A global conclusion from local information has a named
  mechanism:
  - compactness and a finite subcover
  - partition of unity
  - simple connectivity or trivial monodromy
  - properness plus injectivity
  - a sheaf or cohomology argument
- [ ] **Finite to infinite, discrete to continuous, sampled to everywhere.** Each
  such passage is justified and not assumed.
- [ ] **Induction.**
  - The base case is correct and not vacuous.
  - The step uses only the inductive hypothesis as stated.
  - The induction measure strictly decreases.
  - The statement is strong enough to close the step. If not, strengthen it.
- [ ] **Case analysis.** The list of cases is shown to be exhaustive (equality,
  boundary and degenerate cases included), and overlaps do not cause double
  counting.
- [ ] **"Without loss of generality."** Name the symmetry or normalisation that
  justifies it, and check that it preserves every hypothesis and commutes with the
  construction. For example, a coordinate change may not commute with an operation
  that is only equivariant under a smaller group, and rescaling may change sign
  conditions.
- [ ] **Strict versus non-strict.** Limits and closures turn strict inequalities
  into non-strict ones. Openness and closedness are tracked.
- [ ] **Approximation.** Replacing an object by a nearby one (rounded
  coefficients, a perturbation, a truncation) comes with a stability statement with
  an explicit radius, showing that the property of interest survives.

## C. Cited results

- [ ] **Exact statement.** Quoted from the source or from `LITERATURE_REVIEW.md`,
  with the theorem number, and not paraphrased from memory.
- [ ] **Version.** The version checked is recorded (preprint version or published
  version, plus any erratum). Preprints sometimes state stronger results than the
  published version, and errata exist.
- [ ] **Hypotheses.** Every hypothesis of the cited result is checked in our
  setting and the check is written out.
- [ ] **Definitions match.** The source's definitions agree with ours: "manifold"
  with or without boundary, "variety" irreducible or not, "positive" strict or not,
  normalisations of invariants.
- [ ] **Direction and strength.** The result is used in the direction and at the
  strength stated, and not a remembered strengthening of it.

## D. Global sanity checks

- [ ] **Proves too much?** Apply the argument to a case where the conclusion is
  known to be false. Find the step that breaks there. If none does, the proof is
  wrong.
- [ ] **Every hypothesis used.** Each standing assumption is used somewhere. If
  one is never used, either the statement can be strengthened (and if that would
  beat known results, be very suspicious) or a step needs it silently.
- [ ] **Too good to be true?** If the result easily improves a well-known bound or
  settles a well-known question, look harder for the error before celebrating.
- [ ] **Circularity.** No dependency, however "standard", is derived from the
  target or from a consequence of it. The dependency graph has no cycles.
- [ ] **Numerical spot check.** The conclusion of each lemma is evaluated on at
  least one concrete example where that is feasible. Use the
  `computational-experiments` skill for anything beyond a hand calculation.
- [ ] **Statement re-read.** After finishing, re-read the target statement and
  compare it with what the final step actually established.

## E. Recording

- [ ] The lemma's "Checks done" block lists the date, the items that applied, the
  examples tested and the "proves too much" case used.
- [ ] Every unresolved item has a `GAP-<n>` marker and a row in the Open gaps
  table.
- [ ] The status set in the Results register follows the propagation rule: a
  result is no stronger than its weakest dependency.
