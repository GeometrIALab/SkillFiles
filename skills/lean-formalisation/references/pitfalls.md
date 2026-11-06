# Lean and Mathlib pitfalls

Things that make a formal statement mean something other than intended, or a
proof fail in confusing ways. Lemma names below are given as examples; confirm
each with `#check` in your pinned version, since names change.

## Contents

1. Junk values
2. Coercions between ℕ, ℤ, ℚ, ℝ, ℂ
3. Definitions and conventions that differ from the literature
4. Statement-fidelity traps
5. Typeclass assumptions
6. Version drift
7. Automation that is slow or times out
8. Coverage: is the background mathematics in the library?

---

## 1. Junk values

To keep functions total, Mathlib gives "junk" values where ordinary
mathematics would say "undefined". The conventions are deliberate and
consistent, but they change the meaning of statements that forget them.

| Expression | Value in Mathlib | Typical consequence |
|---|---|---|
| `x / 0`, `x⁻¹` at 0 (fields such as ℝ, ℚ, ℂ) | `0` | `a / b * b = a` needs `b ≠ 0` |
| `a - b` in ℕ with `a < b` | `0` (truncated) | `(a - b) + b = a` needs `b ≤ a` |
| `a / b` in ℕ | floor division; `a / 0 = 0` | `(7 : ℕ) / 2 = 3` |
| `/` and `%` in ℤ for negative operands | follows a specific rounding convention | check with `#eval (-7 : ℤ) / 2` before relying on it |
| `Real.sqrt x` for `x < 0` | `0` | `Real.sqrt x ^ 2 = x` needs `0 ≤ x` |
| `Real.log 0` | `0` | |
| `Real.log x` for `x < 0` | `Real.log (-x)` | log identities hold "too often" |
| `x ^ (y : ℝ)` (`Real.rpow`) for `x < 0` | a fixed convention, not the "undefined" of textbooks | do not assume familiar rpow laws for negative bases |
| `∑'` (`tsum`) of a non-summable family | `0` | add a `Summable` hypothesis |
| `deriv f x` where `f` is not differentiable at `x` | `0` | add a `DifferentiableAt` hypothesis |
| `∫` of a non-integrable function | `0` | add an `Integrable` hypothesis |
| `sSup s` in ℝ for empty or unbounded-above `s` | `0` | add `s.Nonempty` and `BddAbove s` |
| `Set.ncard s`, `Nat.card α` for infinite `s` or `α` | `0` | add a finiteness hypothesis |
| `Polynomial.natDegree 0` | `0` (while `Polynomial.degree 0 = ⊥`) | degree statements need `p ≠ 0` |

How to use this: for every operation in a statement, ask what happens at the
junk inputs. Either the statement is still what you mean there, or you need a
hypothesis that excludes them. Conversely, a lemma that "should" need a
hypothesis may be stated without it in Mathlib because the junk value makes it
true anyway. This is fine, but don't copy such a pattern into a statement
whose meaning depends on the excluded case.

## 2. Coercions between ℕ, ℤ, ℚ, ℝ, ℂ

- `((a - b : ℕ) : ℝ)` is not `(a : ℝ) - (b : ℝ)` unless `b ≤ a`
  (`Nat.cast_sub` needs that hypothesis).
- `(2 / 3 : ℝ)` is two thirds, but `((2 / 3 : ℕ) : ℝ)` is `0`. Where the type
  annotation sits decides which division is used.
- The tactics `push_cast`, `norm_cast` and `exact_mod_cast` move casts around;
  use them instead of rewriting casts by hand.
- Numerals take the type the elaborator infers from context. If a statement
  mixes types, annotate the first numeral explicitly.
- `x ^ 2` with a natural-number exponent (`Monoid.npow`) and `x ^ (2 : ℝ)`
  (`Real.rpow`) are different functions with different lemmas. Use natural
  exponents unless you really need real ones.

## 3. Definitions and conventions that differ from the literature

Read the docstring of every Mathlib definition the statement uses, and compare
it with the paper's definition.

- `ℕ` contains 0. If the paper's "n ≥ 1" or "positive integer" is meant, say
  so with a hypothesis or use a type of positive naturals.
- `Finset.range n` is `{0, …, n - 1}`. Intervals come in `Icc`, `Ico`, `Ioc`,
  `Ioo` versions; check which endpoints are included.
- `Fin n` indexes from 0, and `Fin 0` is empty.
- `Nat.Prime p` and `Prime p` (prime element of a monoid) are different
  definitions that agree on ℕ. Use the one the lemmas you need are stated for.
- `ZMod 0` is ℤ, not the zero ring.
- Conventions for normalisation constants (Fourier transforms, measures,
  inner products linear in the first or the second argument), signs (curvature,
  Laplacians) and branch cuts (`Complex.log`, `Complex.arg`) may differ from the
  paper's.
- Bundled and unbundled structures: a ring homomorphism may be a bundled
  structure (`R →+* S`) or a function plus a property; a subgroup is a term of
  type `Subgroup G`, not a type with a group instance. Statements in the "wrong"
  style can be correct but hard to connect to library lemmas.
- Smoothness and regularity classes: the way C^n, C^∞ and analytic regularity
  are indexed has changed between Mathlib versions. Check how your pinned
  version writes "smooth".

## 4. Statement-fidelity traps

- **Vacuous hypotheses.** If the hypotheses can never all hold, the theorem is
  trivially true. Always exhibit an instance (see `statement-fidelity.md`).
- **Quantifier order.** `∀ ε > 0, ∃ δ > 0, …` and `∃ δ > 0, ∀ ε > 0, …` say very
  different things; uniformity is decided by this order. Check also `∃` versus
  `∃!`.
- **Implicit generality.** A statement about all types `α` in some class may be
  more general than the paper's (fine), or the class may be stronger than the
  paper assumes (a weaker theorem; record it).
- **`Finset` versus `Set`.** Using `Finset` silently assumes finiteness; `Set`
  with `ncard` silently gives 0 for infinite sets.
- **Edge cases of the index type.** ℕ including 0, `Fin 0` being empty, empty
  index sets making sums 0 and products 1.
- **Unused hypotheses.** The linter for unused variables can flag a hypothesis
  the proof never used. Either the hypothesis is unnecessary (a stronger theorem;
  fine, but note it), or the statement does not say what you think.
- **Conclusion weaker than intended.** `≤` instead of `<`, `∃` instead of `∀`, an
  inequality that is trivially true because of a junk value.

## 5. Typeclass assumptions

- Too strong: assuming `[Field K]`, `[CharZero K]` or `[IsAlgClosed K]` when the
  paper works over a ring or over ℝ. The result may still be fine, but it is a
  different theorem; record the difference.
- Too weak: the statement may be false (for example over the zero ring, or in
  positive characteristic). You will find out when the proof gets stuck. Check
  small counterexamples before spending effort.
- `[Nontrivial R]`, `[Fintype ι]`, `[DecidableEq ι]`: often needed for technical
  reasons and harmless for meaning, but check that a `Nontrivial` assumption is
  not excluding a case the paper includes.

## 6. Version drift

- Lemmas are renamed, generalised, moved or deprecated. A deprecation warning
  usually names the replacement.
- Names from older papers, blog posts, forum answers or memory may not exist in
  your pinned version. Confirm every name with `#check`.
- Upgrade Mathlib deliberately and separately (see `SKILL.md`). After an
  upgrade, rerun the full build and the axiom audit.

## 7. Automation that is slow or times out

- `simp` loops when its lemma set rewrites back and forth. Use `simp?` to see
  which lemmas fire, then `simp only [...]` with a controlled set.
- `nlinarith`, `polyrith`-style tools, `positivity` and `norm_num` extensions
  can be slow on large goals. Supply the key products or facts as hints, or
  split the goal with `have`.
- `decide` evaluates in the kernel and can be very slow on large finite checks.
  `native_decide` is fast but adds trust in the compiler (it shows up as
  `Lean.ofReduceBool` in `#print axioms`). Use it only with explicit agreement.
- `exact?` and `apply?` can take a long time; narrow the goal first.
- Raising `maxHeartbeats` is a diagnostic, not a fix. If it is needed, record
  why and where.
- Elaboration of large numerals or big explicit structures can be slow; build
  them from smaller definitions.

## 8. Coverage: is the background mathematics in the library?

Mathlib is broad but uneven. Some areas (for example parts of differential
geometry, PDE theory, and advanced algebraic geometry) have limited coverage,
so a short paper proof may rest on large amounts of missing foundations. Before
committing to a formalisation:

- list the background results the proof uses;
- check which ones exist in the pinned Mathlib;
- estimate the cost of the missing ones honestly, and consider formalising only
  the new, doubtful steps, stating the missing background as explicit
  hypotheses (and recording that in the register as a weaker formal result).
