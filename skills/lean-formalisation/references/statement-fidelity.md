# Statement fidelity: does the formal statement say what the mathematics says?

The kernel guarantees that a proof proves its formal statement. Nothing
guarantees that the formal statement is the theorem you meant. This protocol
checks that, before effort goes into the proof and again whenever the
statement changes.

## Protocol

1. **Fix the informal statement.** Copy it from `PROOF_PROGRESS.md` (or the
   paper) with all hypotheses and conventions written out: the ground field or
   ring, the ranges of indices, what "smooth", "generic" or "positive" mean, and
   the normalisations.
2. **Write the formal statement** and the definitions it depends on, with the
   proof as `sorry`.
3. **Self-check** against the checklist below. Fix what it finds.
4. **Independent back-translation.** Give a fresh agent session with no access
   to the working notes (a subagent, if the agent supports them), or a human
   colleague:
   - the Lean statement;
   - every project-specific definition it uses;
   - access to the Mathlib documentation;
   - but *not* the informal statement or the paper.

   Ask them to write a precise prose statement of what the Lean statement
   says: all hypotheses, the types of all variables, the quantifier order, and
   every operation whose value depends on a junk-value convention. The reviewer
   should also say anything that looks odd: unused hypotheses, unusually strong
   typeclass assumptions, edge cases (n = 0, empty sets).
5. **Compare** the back-translation with the informal statement, and classify
   the result:
   - **equivalent**: the same statement, possibly rephrased;
   - **formal stronger**: the formal statement implies the informal one (fewer
     hypotheses, more general types). Fine; note it.
   - **formal weaker**: extra hypotheses, a special case, a weaker conclusion.
     Record the difference; the formal proof will not establish the informal
     claim in full (see "Recording results" in `SKILL.md`).
   - **different**: neither implies the other. Fix the statement and repeat from
     step 3.
6. **Non-vacuity test.** Write an `example` (or a lemma) that builds a concrete
   object satisfying all the hypotheses. If you cannot, the hypotheses may be
   contradictory and the theorem vacuous.
7. **Sanity tests where cheap:**
   - For new definitions, `example`s that compute known values on small cases.
   - For classifications or equivalences, check known small cases.
   - Where a hypothesis is believed necessary, check that dropping it makes the
     statement false (a formal or informal counterexample). If the statement
     stays provable without it, either the hypothesis is unnecessary or the
     statement does not express what you think.
8. **Record** the check (format below) in `HANDOFF.md` and point to it from the
   Results register.

Repeat steps 3 to 8 whenever the formal statement changes, including changes
made "just to get the proof through".

## Checklist

**Types and domains**
- [ ] Each variable has the intended type (ℕ, ℤ, ℚ, ℝ, ℂ; positive or
      non-negative; finite or arbitrary).
- [ ] The case n = 0 (or the empty set, or `Fin 0`) is treated as the paper
      treats it.
- [ ] `Finset` or `Set` is used deliberately; finiteness is not assumed by accident.
- [ ] Index ranges match (`Finset.range n` is `{0, …, n - 1}`; interval
      endpoints are as intended).

**Quantifiers and logic**
- [ ] The quantifier order matches (uniform versus pointwise statements).
- [ ] `∃` versus `∃!`, `∀` versus `∃`, `→` versus `↔` are as intended.
- [ ] The inequalities are strict or non-strict as intended.

**Junk values**
- [ ] Every division, subtraction in ℕ, square root, logarithm, real power,
      infinite sum, derivative, integral, supremum or cardinality is either
      guarded by a hypothesis or harmless at its junk inputs.

**Definitions and conventions**
- [ ] Each Mathlib definition used has the same meaning as the paper's (read
      its docstring): normalisations, sign conventions, branch cuts, degree of
      zero, primality, regularity classes.
- [ ] Each project-specific definition has sanity `example`s.

**Hypotheses**
- [ ] Every hypothesis of the informal statement appears.
- [ ] No extra hypothesis appears unless recorded as a weakening.
- [ ] Typeclass assumptions are not stronger than the paper's (field versus
      ring, characteristic, algebraic closure, finite dimension, completeness).
- [ ] No hypothesis is unused (or, if one is, that is understood).
- [ ] A non-vacuity `example` exists.

**Conclusion**
- [ ] The conclusion is not weaker than the informal one.
- [ ] Casts are where intended (for example `((a - b : ℕ) : ℝ)` versus
      `(a : ℝ) - b`).

## Record format

```markdown
### Fidelity check: <Lean declaration name> ↔ <R-id / lemma label>

- Lean file and commit: formal/<path>.lean @ <commit>
- Lean / Mathlib versions: <toolchain> / <Mathlib commit>
- Informal statement (source): PROOF_PROGRESS.md §<n>, Lemma <label>
- Back-translation by: independent (fresh session or subagent) | human:<name>  — date
- Back-translation text: <prose, or a link to where it is stored>
- Classification: equivalent | formal stronger | formal weaker (<what is lost>) | different (fixed in <commit>)
- Non-vacuity example: <Lean name>
- Sanity tests: <names, or "none needed: …">
- Notes: <unused hypotheses, edge cases, conventions documented>
```
