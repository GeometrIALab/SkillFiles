# Common errors in research-level arguments

Each entry gives what the error looks like, a short generic example, how to detect
it, and the usual repair. The examples are standard textbook situations; the
patterns recur in every field.

## Contents

1. Statement drift
2. Circularity
3. Quantifier swap
4. Hidden non-uniformity
5. "Without loss of generality" that loses generality
6. Using the converse
7. Misapplied theorem (hypotheses fail)
8. Wrong version of a cited result
9. Local-to-global leap
10. Generic versus all
11. Dimension count used as an existence proof
12. Sampled or numerical check used as a proof step
13. Matching a total taken as proof of completeness
14. Sign and convention mismatch between sources
15. Induction that does not start or does not close
16. Incomplete case analysis
17. Ignoring well-definedness
18. Unjustified interchange of limits
19. Assumed existence
20. Strict inequalities that do not survive limits
21. Approximation that changes the object
22. "Similarly" that is not similar
23. Self-review taken as verification

---

### 1. Statement drift
**Looks like:** the final step establishes something slightly different from the
statement: a weaker conclusion, an extra hypothesis, or a special case.
**Example:** the target is a bound for all degrees d ≥ 3, but the proof silently
uses d odd from step 7 onwards.
**Detect:** after finishing, re-read the target statement and compare it with the
final step. List every hypothesis actually used.
**Repair:** state what was proved as its own result with its own status, and keep
the original target at its true status.

### 2. Circularity
**Looks like:** a "standard" fact used in the proof is itself derived from the
target or from a consequence of it.
**Example:** a priori estimates for a solution on [0, T] are proved by an argument
that assumes the solution already exists on [0, T].
**Detect:** draw the dependency graph and check it has no cycles. Ask where each
"standard" fact is proved.
**Repair:** reorganise, for example with a continuity or bootstrap argument and an
explicit open-and-closed structure.

### 3. Quantifier swap
**Looks like:** "for every x there exists y" is later used as "there exists y for
every x".
**Example:** continuity at each point is used as uniform continuity on a
non-compact set.
**Detect:** write each statement in fully quantified form at the point where it is
used.
**Repair:** obtain the stronger statement (compactness, equicontinuity) or
restructure the argument.

### 4. Hidden non-uniformity
**Looks like:** a constant C or a radius δ is chosen, and later a parameter it
depends on is varied or sent to a limit.
**Example:** an elliptic estimate whose constant depends on the domain is applied
along a sequence of degenerating domains.
**Detect:** annotate every constant with what it depends on, for example
C = C(n, K, Ω).
**Repair:** prove a uniform version or track the dependence explicitly.

### 5. "Without loss of generality" that loses generality
**Looks like:** a normalisation that is incompatible with a hypothesis or with the
operation being studied.
**Example:** over ℝ, "WLOG the leading coefficient is 1" when its sign matters
(only ±1 is possible). Or "WLOG the points are in general position after a change
of coordinates" when the construction is equivariant only under a smaller group
than the coordinate change used.
**Detect:** name the group action that justifies the WLOG. Check that it preserves
every hypothesis and commutes with every construction in the proof.
**Repair:** handle the remaining cases separately, or restrict to the correct
group.

### 6. Using the converse
**Looks like:** "A implies B; B holds; hence A."
**Example:** "minimisers satisfy the Euler–Lagrange equation; u satisfies it;
hence u is a minimiser."
**Detect:** for each step, write the implication with its arrow and check the
direction.
**Repair:** find a genuine argument for the converse (convexity, uniqueness) or
weaken the conclusion.

### 7. Misapplied theorem (hypotheses fail)
**Looks like:** a theorem applied where one hypothesis fails, often only slightly.
**Examples:**
- Arzelà–Ascoli without equicontinuity.
- Sard's theorem with insufficient smoothness.
- A characteristic-zero result used in positive characteristic.
- The implicit function theorem at a point where the derivative is not
  surjective.
- A compact-case result used on a non-compact manifold or one with boundary.
**Detect:** quote the theorem and check each hypothesis explicitly, in writing.
**Repair:** verify the missing hypothesis, find a version without it, or mark a
GAP.

### 8. Wrong version of a cited result
**Looks like:** citing a statement as remembered, or as it appears in a preprint,
when the published version is weaker or has been corrected.
**Example:** a preprint states a bound with a better exponent than the published
theorem; the stronger claim was withdrawn in revision.
**Detect:** check the published version and any errata. Record which version was
checked.
**Repair:** cite the correct version and recheck what follows from it.

### 9. Local-to-global leap
**Looks like:** a property that holds near every point is asserted globally.
**Examples:**
- A closed form is locally exact, but not globally exact on a space that is not
  simply connected.
- A local diffeomorphism need not be a global diffeomorphism without properness
  and injectivity.
- Locally a graph is not globally a graph.
**Detect:** ask what mechanism turns local into global: compactness, partitions of
unity, monodromy or cohomology, properness.
**Repair:** supply that mechanism or restrict the conclusion.

### 10. Generic versus all
**Looks like:** a property true for generic objects is applied to a specific
object, or "generic" is never defined.
**Example:** "a generic polynomial has simple roots, so ours does", when ours lies
in a special family that may sit entirely inside the discriminant.
**Detect:** check whether the specific object, or the family it belongs to, lies
in the exceptional set.
**Repair:** verify the property directly for the object, or show that the family
is not contained in the exceptional set.

### 11. Dimension count used as an existence proof
**Looks like:** "the expected dimension of this stratum is non-negative, so it is
non-empty", or "the conditions are independent by a parameter count".
**Example:** counting unknowns and equations to claim that a configuration with
prescribed singularities exists, when the equations are dependent or the solution
set is empty or excess-dimensional.
**Detect:** ask which map, which spaces, and which theorem gives transversality or
surjectivity, and why the relevant set is non-empty.
**Repair:** prove transversality (for example by a surjectivity computation at an
explicit point), exhibit an explicit example, or label the claim HEURISTIC.

### 12. Sampled or numerical check used as a proof step
**Looks like:** "the function is positive on a fine grid, hence positive";
"plotting shows the curve has k components"; "the optimiser found no better point".
**Example:** a positivity check at sample points misses a tiny negative region
between them.
**Detect:** look for any step whose justification is a computation without a
certificate.
**Repair:** certify it (interval arithmetic, exact arithmetic, certified root
isolation; see `computational-experiments`) or treat the step as a GAP. A
NUMERICAL input makes the result PROVED-MODULO at best.

### 13. Matching a total taken as proof of completeness
**Looks like:** "the indices of the critical points found add up to the Euler
characteristic, so we have found all of them."
**Example:** a pair of critical points of opposite index is missing, and the sum
is unchanged.
**Detect:** ask whether objects could be missing in cancelling groups.
**Repair:** use a completeness argument (certified exhaustive root isolation, a
degree bound that is attained, a direct classification).

### 14. Sign and convention mismatch between sources
**Looks like:** formulas combined from two sources that use different conventions.
**Examples:**
- One source's Laplacian is positive and another's negative.
- Curvature sign conventions differ.
- Fourier transforms carry different 2π normalisations.
- Orientation conventions differ in a boundary formula.
- "Positive definite" in one source means semidefinite in another.
**Detect:** write each source's convention in the notation table. Test the
combined formula on the simplest example (flat space, a round sphere, a single
monomial).
**Repair:** convert everything to one convention, stated in the notation table.

### 15. Induction that does not start or does not close
**Looks like:** the base case is wrong or vacuous; the step needs more than the
inductive hypothesis provides; or the induction measure does not decrease.
**Example:** the step needs the statement for *all* smaller cases with a uniform
constant, but the hypothesis gives each case its own constant.
**Detect:** write the inductive statement P(n) explicitly and check that the step
uses only P(m) for m < n, exactly as stated.
**Repair:** strengthen the inductive statement until the step closes, then check
the stronger base case.

### 16. Incomplete case analysis
**Looks like:** cases that miss equality cases, boundary cases, degenerate
configurations, or a sign combination.
**Example:** splitting into "a > 0" and "a < 0" and forgetting a = 0; or
considering transverse intersections and forgetting tangencies.
**Detect:** prove that the list of cases is exhaustive, as its own small lemma.
**Repair:** add the missing cases, or justify excluding them in the statement.

### 17. Ignoring well-definedness
**Looks like:** a construction depends on choices (a representative, a branch of
log or square root, a basis, an ordering, a cut-off function), and the result is
treated as canonical.
**Detect:** ask what happens to the construction under each allowed change of
choice.
**Repair:** prove independence, or fix the choice in the statement.

### 18. Unjustified interchange of limits
**Looks like:** swapping a limit with an integral, sum, derivative or another
limit without justification.
**Example:** pointwise convergence used to pass a limit under an integral on an
infinite-measure space.
**Detect:** look for every interchange of limiting operations.
**Repair:** apply and check the hypotheses of dominated or monotone convergence,
uniform convergence, Fubini/Tonelli, or differentiation under the integral sign.

### 19. Assumed existence
**Looks like:** "let u be the minimiser", "let x be the limit point", "take the
solution".
**Example:** minimising a functional that is not coercive, so a minimising
sequence escapes to infinity.
**Detect:** for every definite article attached to an object, ask why it exists
(and why it is unique, if uniqueness is used).
**Repair:** prove existence (compactness, coercivity, lower semicontinuity,
completeness) or assume it explicitly and label the result accordingly.

### 20. Strict inequalities that do not survive limits
**Looks like:** f_n > 0 for all n, hence lim f_n > 0.
**Detect:** track openness and closedness, and strict versus non-strict
inequality, through every limit.
**Repair:** obtain a uniform lower bound, or weaken the conclusion to ≥.

### 21. Approximation that changes the object
**Looks like:** replacing an object by a nearby one (rounded or rational
coefficients, a truncated series, a perturbed parameter) and assuming the property
of interest is unchanged.
**Example:** rounding coefficients of a polynomial whose zero set has very small
components can change the number of components.
**Detect:** ask for a stability statement with an explicit radius.
**Repair:** certify the approximated object directly, or prove stability with
explicit bounds.

### 22. "Similarly" that is not similar
**Looks like:** "the other case is similar", when it involves a different sign, a
missing symmetry, or a boundary term that was zero in the first case.
**Detect:** write out what changes in the second case. If the change is not
trivial, write the argument.
**Repair:** give the second argument in full, or state precisely what changes.

### 23. Self-review taken as verification
**Looks like:** the author, or the same agent session, re-reads the proof and
declares it correct.
**Why it fails:** remembered reasoning fills the gaps in the text, so the gaps are
not seen.
**Repair:** use the protocol in `independent-review.md`, and record the review
level accurately (`review: self` is not `review: independent`).
