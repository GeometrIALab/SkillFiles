# Certification techniques by problem type

A computation is CERTIFIED when there is a recorded run that rigorously
establishes the claim for an exactly specified object, and the run can be
reproduced. This file lists the main techniques: what each one certifies, how
it is used, and how it typically goes wrong. Choose the technique before the
search, so that the data the certificate needs is stored.

## Contents

0. Principles common to all techniques
1. Exact rational and algebraic arithmetic
2. Interval and ball arithmetic
3. Certified real root isolation (one variable)
4. Gröbner bases, resultants and discriminants
5. Polynomial systems: alpha theory, Krawczyk and interval Newton
6. Topology of real algebraic sets: counting components, isotopy type
7. Sums of squares and semidefinite programming
8. Linear and mixed-integer programming
9. SAT and SMT with proof logs
10. Exhaustive combinatorial enumeration
11. Verified ODE solving and integration
12. Validated numerics for PDE and computer-assisted proofs (outline)
13. Recording a certificate

---

## 0. Principles common to all techniques

- **Certify the stored object exactly.** Integers, rationals, algebraic
  numbers given by a minimal polynomial and isolating interval, or
  combinatorial data, kept in the run directory with a hash. A certificate
  about a float approximation is a certificate about the approximation.
- **Rounding or rationalising changes the object.** Converting a floating-point
  candidate to rationals, or "cleaning" its coefficients, can destroy small or
  multi-scale features. Certify the rationalised object you actually store; if
  you later simplify it, the simplified object needs its own certificate.
- **The checker should be cheap, simple and independent of the search.** The
  best certificates can be verified by a short program, in other software, that
  did not produce them: a dual solution, a proof log, an exact identity.
- **Check the whole claim.** Side conditions (smoothness, nondegeneracy,
  genericity, being in the right family, degree, sign conventions) are part of
  the claim. A lower bound without its matching upper bound is not a count.
- **Know your trusted base.** Write down which software you trust, which
  conjectures the result is conditional on (if any), and which encodings you
  wrote yourself.
- **Consistency checks are not certificates.** A matching Euler
  characteristic, degree, index sum or Morse count is consistent with a missing
  pair of features that cancel. Use these to catch errors, never to prove that
  nothing was missed.

## 1. Exact rational and algebraic arithmetic

- **Certifies:** any identity, sign, rank or equality decided by computing
  exactly in ℤ, ℚ, a number field, the real algebraic numbers, or a finite
  field.
- **How:** use exact types throughout (see `tools.md`). Represent a real
  algebraic number by its minimal polynomial and an isolating interval.
- **Pitfalls:** coefficient growth makes exact computation slow, which tempts
  people to drop to floats midway, and the result is then no longer exact. A
  result over a finite field certifies only the finite-field statement; lifting
  it to ℚ needs an argument (for example about good primes, or a bound plus the
  Chinese remainder theorem plus a final exact check).

## 2. Interval and ball arithmetic

- **Certifies:** enclosures of values. Typical uses: a function has a strict
  sign on a box (so it has no zero there); a quantity lies in a given interval;
  two quantities are different.
- **How:** evaluate in interval or ball arithmetic. Subdivide boxes where the
  enclosure is too wide. Record the boxes and the results.
- **Pitfalls:** one floating-point constant or input breaks the guarantee
  (0.1 is not exactly representable in binary; pi typed as a float is not pi).
  Overestimation can make enclosures useless: subdivide or use better forms
  (centred, mean-value, Taylor models). An enclosure that contains zero decides
  nothing, so "could not certify" is UNRESOLVED, not a negative result.
  Exact zeros, such as the multiple root of a non-squarefree polynomial or a
  point where a curve is singular, cannot be detected by interval evaluation
  alone and need algebraic arguments.

## 3. Certified real root isolation (one variable)

- **Certifies:** disjoint intervals each containing exactly one real root of a
  polynomial, together with the exact number of real roots.
- **How:** Descartes' rule of signs with bisection (Vincent–Collins–Akritas-type
  algorithms) or Sturm sequences, on exact coefficients. Bit-stream variants
  accept coefficients given to arbitrary precision.
- **Pitfalls:** work with the squarefree part, or handle multiplicities
  explicitly. Isolating the roots of a float approximation of the polynomial
  isolates the roots of a different polynomial.

## 4. Gröbner bases, resultants and discriminants

- **Certifies:** exact elimination; emptiness of the *complex* solution set
  (1 lies in the ideal); dimension and degree; radical membership; the exact
  discriminant locus of a family.
- **Checkable certificates:** for emptiness, cofactors g_i with
  1 = Σ g_i f_i, which anyone can verify by multiplying out. For an
  elimination, check that the claimed polynomial lies in the ideal.
- **Pitfalls:** modular (mod p) or probabilistic algorithms used for speed
  need a final exact verification. Emptiness over ℂ implies emptiness over ℝ,
  but not conversely: real emptiness needs a Positivstellensatz certificate
  (see §7) or CAD (see §6). Generic-coordinate arguments must be checked for the
  coordinates actually used.

## 5. Polynomial systems: alpha theory, Krawczyk and interval Newton

- **Certifies:** a given box (or approximate point) corresponds to exactly one
  true solution of a square system; two approximate solutions correspond to
  different true solutions; a solution is real (unique solution in a box
  invariant under complex conjugation).
- **How:** Smale's alpha theory (for example in alphaCertified) or the
  Krawczyk / interval Newton test (for example HomotopyContinuation.jl's
  certification), applied to each numerical solution.
- **Completeness:** these tests certify the solutions you have, not that you
  have them all. If the number of certified distinct isolated solutions equals
  a proven upper bound (Bézout number, a mixed-volume bound, or a known generic
  root count for the family), then the list is complete. Positive-dimensional
  solution components need separate treatment.
- **Pitfalls:** singular solutions (where the Jacobian is not invertible)
  cannot be certified this way without deflation or other extra work.

## 6. Topology of real algebraic sets: counting components, isotopy type

- **Certifies:** the number of connected components, their arrangement
  (nesting of ovals), or a complete isotopy type, for an exactly given
  polynomial.
- **How:**
  - *Cylindrical algebraic decomposition (CAD):* complete and exact, but
    practical only in few variables or for low degree.
  - *Certified curve topology for plane curves:* compute the critical points
    (with respect to a projection) exactly, isolate them with certified root
    isolation, then connect the sections between consecutive critical values.
    Requires checking that the coordinate system is generic (or handling the
    non-generic case).
  - *Certified subdivision:* subdivide the plane into boxes with interval
    tests that certify the curve's behaviour in each box (for example: the
    function has no zero in the box, or the gradient is bounded away from zero so
    the curve is a single smooth arc). These give certified results for smooth
    curves in a bounded region, under conditions stated by each method.
- **Pitfalls:**
  - A sampled grid (marching squares, a pixel picture, a mesh) can miss small
    components and can connect or separate branches wrongly near close
    approaches. An exact union-find on the grid is exact about the grid only.
  - Components at or through infinity, and unbounded components in an affine
    chart, must be handled; decide whether you count in affine or projective
    space and treat the line at infinity explicitly.
  - Singular points (nodes, cusps, isolated real points) need separate algebraic
    treatment; interval tests cannot certify them.
  - Euler characteristic and Morse-count checks cannot detect a missing pair
    of critical points that cancel.
  - A partial result ("at least k components certified") must be reported as a
    lower bound; the count needs a matching certified upper bound and the
    smoothness check.

## 7. Sums of squares and semidefinite programming

- **Certifies:** a polynomial is non-negative (an SOS decomposition); a
  semialgebraic set is empty (a Positivstellensatz certificate); a bound on an
  optimisation problem.
- **How:** solve the SDP numerically, then turn the numerical Gram matrix into an
  exact one: rationalise it, project it exactly onto the affine constraints, and
  verify that the result is positive semidefinite in exact arithmetic (an exact
  LDLᵀ decomposition, or an interval lower bound on the smallest eigenvalue).
- **Pitfalls:** this works only if the numerical solution is strictly inside the
  cone with some margin. If the true certificate lies on the boundary (the Gram
  matrix must be singular), rounding fails and the problem has to be reduced
  first (facial reduction). A solver reporting "optimal" with small residuals is
  not a certificate.

## 8. Linear and mixed-integer programming

- **Certifies:** a feasible point (check it exactly); an upper or lower bound
  on the optimum (an exact dual certificate); optimality of an integer
  solution (needs the whole branch-and-bound argument).
- **How:**
  - Feasibility: check the rational solution against every constraint in exact
    arithmetic.
  - Bounds for an LP: by weak duality, *any* dual-feasible vector gives a valid
    bound. Rationalise the dual solution, repair feasibility exactly if needed,
    and compute the bound exactly. "Safe bounds" can also be obtained from
    floating-point duals with rigorous error correction, given bounds on the
    variables.
  - MILP: use an exact solver mode where available, or a solver that emits a
    checkable certificate (for example in the VIPR format) and an independent
    checker.
- **Pitfalls:** integrality and feasibility tolerances accept slightly wrong
  answers. Big-M formulations are numerically fragile. Pre-solve reductions
  happen inside the solver and are part of what you trust unless a certificate
  covers them.

## 9. SAT and SMT with proof logs

- **Certifies:** satisfiable instances by a model; unsatisfiable instances by a
  proof of unsatisfiability.
- **How:** check a model by evaluating every clause. For UNSAT, have the solver
  write a DRAT or LRAT proof and check it with an independent checker
  (drat-trim, or a formally verified checker).
- **Pitfalls:** the proof certifies the formula, not the mathematics. The
  encoding of the problem, and any symmetry-breaking constraints, are part of
  the trusted base:
  - Test the encoding on small cases with known answers (both satisfiable and
    unsatisfiable).
  - Prove, on paper, that the symmetry breaking keeps at least one
    representative of every solution orbit. Unsound symmetry breaking turns a
    satisfiable problem into an "UNSAT" one.
  - Cube-and-conquer splits must be shown to cover all cases.

## 10. Exhaustive combinatorial enumeration

- **Certifies:** a complete list of objects up to isomorphism in a finite class,
  or that none of them has a property.
- **How:** orderly generation or canonical augmentation with canonical
  labelling (see `construction-search` references), plus an exact decision for
  each object.
- **Independent checks:**
  - Compare counts with known values for small sizes (OEIS, published tables).
  - Enumerate a second time by a different method.
  - Check the orbit-counting identity: the sum of |G|/|Aut(X)| over the
    representatives X must equal the number of labelled objects, when that
    number can be computed independently.
- **Pitfalls:** unsound pruning, encodings whose isomorphism is not the
  intended one, and integer overflow in counts.

## 11. Verified ODE solving and integration

- **Certifies:** enclosures of solutions of ODEs over a time interval; values
  of definite integrals.
- **How:** rigorous integrators based on interval Taylor methods or Taylor
  models (for example the CAPD library, or COSY Infinity); rigorous quadrature
  in ball arithmetic (Arb/FLINT has a certified numerical integration routine).
- **Pitfalls:** ordinary adaptive solvers give error *estimates*, not bounds.
  Enclosures can blow up over long times (the wrapping effect). Singularities of
  the integrand must be handled analytically.

## 12. Validated numerics for PDE and computer-assisted proofs (outline)

- **Certifies:** existence (and often local uniqueness) of a true solution near
  a numerically computed one, with an explicit error bound.
- **How (in outline):** compute an approximate solution; bound its residual
  rigorously; bound the inverse of the linearised operator; show that a
  Newton-like map is a contraction on a ball of explicit radius (the
  Newton–Kantorovich theorem, or the "radii polynomial" approach). Every
  constant in the argument must be computed rigorously.
- **Pitfalls:** truncation of infinite-dimensional problems needs analytic tail
  estimates; one non-rigorous constant invalidates the result. This needs
  expertise in the specific equation. Treat as a project in itself, and record
  each constant with its method of bounding.

## 13. Recording a certificate

In the run's `manifest.json`:

```json
"evidence_tier": "CERTIFIED",
"certificate": {
  "method": "interval subdivision + exact critical points; exact rational input",
  "checker": "independent script code/check_topology.py (not the search code), FLINT 3.x ball arithmetic",
  "location": "certificate/boxes.json, certificate/check_output.txt"
}
```

In the Results register, point to the run directory. Say who did the
independent check: `self`, `independent` (a fresh agent session with no access
to the working notes, or a subagent), or `human:<name>` (set only by that
human).
