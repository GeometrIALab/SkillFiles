# Mathematical software: what each tool is for

Use this to choose tools for a run. For each tool: what it is good at, what it
is not good at, and how to get exact or validated answers from it. Versions and
interfaces change, so check the current documentation before relying on a
specific function name. Record versions in the run manifest.

General rule: use whatever is fastest to *find* things, and a tool that gives
exact or validated answers to *confirm* them. These are often different tools.

## Contents

1. General-purpose computer algebra
2. Commutative algebra and algebraic geometry
3. Number theory
4. Group theory and combinatorics
5. Numerical algebraic geometry
6. Exact, multiprecision, interval and ball arithmetic
7. Floating-point numerics
8. Optimisation: LP, MILP, SDP
9. SAT and SMT
10. Polyhedral geometry and triangulations
11. Real algebraic geometry and quantifier elimination
12. Data sources for checking small cases
13. Plotting

---

## 1. General-purpose computer algebra

**SageMath** (open source, Python-based). Combines many specialised systems
(PARI, GAP, Singular, FLINT, Maxima and others) behind one interface.
- Good for: glue code that needs several areas at once; exact rings (integers,
  rationals, number fields, finite fields, the field of real algebraic numbers
  `AA` and algebraic numbers `QQbar`); polynomial rings and ideals (Gröbner bases
  through Singular); graph theory and combinatorics; interfaces to LP/MILP
  solvers.
- Not good for: the very largest specialised computations, where the
  underlying system called directly may be faster or more configurable.
- Exactness: work in `ZZ`, `QQ`, number fields, `AA`/`QQbar`. The real ball and
  interval fields (`RealBallField`/`RBF`, `RealIntervalField`/`RIF`, and complex
  versions) give rigorous enclosures. `RR` and `RDF` are floating point and are
  not rigorous.

**Commercial systems (Mathematica, Maple, Magma).** Powerful, but the
algorithms behind some high-level functions are not fully documented. For
certification, prefer methods whose output you can check independently (for
example a returned certificate, or a result you re-verify in exact arithmetic).
A licence is required, which also limits who can reproduce the run.

**SymPy** (Python). Symbolic manipulation, exact rationals and algebraic
numbers, polynomial tools including real root isolation for univariate
polynomials with exact coefficients, and (slow) Gröbner bases.
- Good for: small exact computations inside a Python pipeline; generating
  exact expressions for other tools.
- Not good for: large polynomial systems or heavy linear algebra.
- Pitfalls: `simplify` is heuristic and may fail to recognise zero; `==` tests
  structural equality, not mathematical equality; `nsimplify` and similar
  "guess a closed form" functions produce conjectures, not proofs.

## 2. Commutative algebra and algebraic geometry

**Macaulay2.** Gröbner bases, free resolutions, Betti numbers, Hilbert series
and polynomials, sheaf cohomology on projective varieties, primary
decomposition, many packages (including numerical algebraic geometry).
- Exactness: computations over `QQ` and finite fields are exact. Computations
  over a finite field are a fast probe for the rational case, but a result mod p
  only transfers to the rationals for "good" primes; without an argument that p
  is good, treat it as HEURISTIC evidence about the rational case.

**Singular.** Polynomial computations with global and local orderings
(standard bases), singularity theory (Milnor and Tjurina numbers,
classification of singularities), primary decomposition, many libraries.
- Same mod-p caveat as Macaulay2.

**OSCAR** (Julia). Brings together GAP, Singular, polymake and number theory
libraries in one system. Broad coverage; the interface is newer and changes
more between versions, so pin the version.

**Magma** (commercial). Strong in number theory, arithmetic geometry, group
theory, coding theory and algebraic geometry over finite fields.

## 3. Number theory

**PARI/GP.** Fast arithmetic in number fields, class groups and units,
elliptic curves, L-functions, modular forms, factorisation.
- Pitfalls: some class group and unit computations are conditional on the
  generalised Riemann hypothesis unless explicitly certified (PARI provides a
  certification routine for this); real numbers are multiprecision floating
  point, not intervals. Record which results are conditional.

**FLINT** (C library; Python bindings exist). Fast exact arithmetic over the
integers, rationals, finite fields and number fields: polynomials, matrices,
factorisation. Since version 3 it also contains the former Arb library for ball
arithmetic (see §6).

**LMFDB** (online database of L-functions, modular forms, number fields,
elliptic curves and related objects). Good for cross-checking small cases;
each entry's own page states how complete and how certified its data is.

## 4. Group theory and combinatorics

**GAP.** Permutation groups, finitely presented groups, character tables,
representation theory, and libraries of small groups, transitive groups and
primitive groups.
- Pitfalls: some methods are randomised. For any result you will cite, check
  in the documentation of that specific function whether the answer is verified
  or probabilistic, and how to request a verified computation.

**nauty and Traces** (also **bliss**). Canonical labelling and automorphism
groups of graphs; nauty's `geng` generates graphs up to isomorphism.
- Use for: removing isomorphic duplicates, computing symmetry groups, generating
  all small graphs in a class.
- Pitfall: when encoding another structure (a design, a matrix, a coloured
  configuration) as a graph, make sure graph isomorphism of the encoding is
  exactly isomorphism of the structure. Test the encoding on cases where the
  answer is known.

## 5. Numerical algebraic geometry

**HomotopyContinuation.jl** (Julia), **Bertini**, and similar. Find the
isolated complex solutions of polynomial systems by path tracking; monodromy
methods; parameter homotopies for families.
- Good for: systems far too large for Gröbner bases; finding many solutions
  quickly; families of systems.
- Not good for: proving that *all* solutions were found. Path tracking can fail
  or jump between paths.
- Validation: HomotopyContinuation.jl can certify individual solutions with
  interval methods (that a box contains a unique true solution, and whether it
  is real). Standalone certifiers based on Smale's alpha theory (for example
  alphaCertified) do the same. Completeness needs a separate argument: if the
  number of certified distinct solutions equals a proven upper bound on the
  number of isolated solutions (Bézout, a mixed-volume bound, or a known
  generic count), then all isolated solutions have been found.

## 6. Exact, multiprecision, interval and ball arithmetic

**Arb, now part of FLINT** (C; available through SageMath, python-flint and
other bindings). Ball arithmetic: every number is a midpoint with a rigorous
error radius. Covers elementary and many special functions, polynomial roots,
linear algebra and rigorous numerical integration.

**MPFR and MPFI.** MPFR is correctly rounded multiprecision floating point;
MPFI builds interval arithmetic on top of it.

**mpmath** (Python). Arbitrary-precision floating point plus an interval
arithmetic context (`mpmath.iv`).
- Pitfall: the default `mp` context is not rigorous. Raising the precision
  makes errors less likely; it does not bound them.

**Interval libraries in other languages** (for example Julia's
IntervalArithmetic.jl; C++ libraries such as those in the CAPD project).

Pitfalls common to all interval and ball arithmetic:
- Every operation must be done in the interval/ball type. One float constant
  (a decimal such as 0.1 typed as a float, or pi as a float) silently breaks
  the guarantee.
- Overestimation (the dependency problem) can make enclosures too wide to
  decide anything. Subdivide, use centred forms or Taylor models, or raise
  precision; never narrow an enclosure by hand.

## 7. Floating-point numerics

**NumPy and SciPy** (Python), and the equivalents in Julia and MATLAB. Linear
algebra through LAPACK, optimisation, ODE solvers, FFTs, sparse matrices.
- Good for: screens, exploration, generating candidates and starting points.
- Not good for: decisions that depend on exact zeros, ranks, signs or
  topology. For example, `numpy.linalg.matrix_rank` decides rank with a
  singular-value threshold, which is a heuristic.

## 8. Optimisation: LP, MILP, SDP

- **Modelling layers:** CVXPY (Python), JuMP (Julia), PuLP and Pyomo (Python).
- **LP and MILP solvers:** HiGHS, SCIP, GLPK (open source); Gurobi, CPLEX
  (commercial). SoPlex has an exact rational LP mode; QSopt_ex is an exact
  rational LP solver.
- **SDP solvers:** SCS, Clarabel, CSDP, SDPA (with multiprecision variants),
  MOSEK (commercial).
- Pitfalls: solvers work with feasibility and integrality tolerances (a value
  of 0.9999997 may be accepted as 1); "optimal" means optimal within tolerance.
  Big-M constraints are numerically fragile. To certify, see
  `certification.md` §7–8. Certificate formats for MILP exist (for example
  VIPR) but are not supported by every solver.

## 9. SAT and SMT

- **SAT solvers:** CaDiCaL, Kissat, CryptoMiniSat, among others. Modern solvers
  can emit proofs of unsatisfiability in DRAT or LRAT format.
- **Proof checkers:** drat-trim; formally verified checkers for DRAT/LRAT-style
  proofs (for example cake_lpr).
- **SMT solvers:** Z3, cvc5 (arithmetic, bit-vectors, quantifiers).
- Pitfalls: a satisfying assignment is easy to check directly; an UNSAT answer
  is only as good as its checked proof *and* the correctness of the encoding and
  any symmetry-breaking constraints, which are part of what you trust.

## 10. Polyhedral geometry and triangulations

- **polymake:** convex hulls, face lattices, lattice polytopes, triangulations,
  tropical geometry, matroids; exact rational arithmetic.
- **TOPCOM:** enumeration of triangulations of point configurations. It
  distinguishes regular triangulations from all triangulations. Many
  constructions (for example Viro-type patchworking) need regular ones, so check
  which set you enumerated.
- **Normaliz:** lattice points, Hilbert bases, Ehrhart series.
- Exactness: these work in exact rational arithmetic by default. Keep it that
  way.

## 11. Real algebraic geometry and quantifier elimination

- **Cylindrical algebraic decomposition (CAD) and quantifier elimination:**
  available in QEPCAD B, Redlog, Maple's RegularChains, and Mathematica.
  Complete but doubly exponential in the number of variables, so practical only
  in low dimension.
- **Certified topology of plane real algebraic curves:** CAD-based algorithms
  and subdivision algorithms with certified tests exist in several systems and
  research codes. Check what the specific implementation guarantees (isotopy?
  only the number of components? only for smooth curves?) before citing it.
- Pitfall: emptiness or dimension over the complex numbers (from Gröbner bases)
  says nothing direct about the real points.

## 12. Data sources for checking small cases

- **OEIS:** compare counts from your enumeration with known sequences.
- **LMFDB:** number-theoretic objects (see §3).
- **House of Graphs, and graph and design catalogues:** known extremal graphs
  and combinatorial designs.
- Published tables in papers: cite the table, and say whether you reproduced
  it.

Reproducing known values is a positive control, not just a curiosity. Do it
before trusting new values from the same code.

## 13. Plotting

matplotlib, Makie, gnuplot and the plotting in the computer algebra systems
are for intuition and presentation. A plot is not evidence about topology or
counts: rendering resolution hides small components, merges nearby branches and
invents crossings. If a figure appears in a paper, generate it from a script
stored in `code/` and say what it was computed from.
