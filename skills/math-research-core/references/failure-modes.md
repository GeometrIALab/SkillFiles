# Failure modes: tempting inferences that produce false claims

Each entry describes a tempting inference, why it fails, and what to do instead. The
entries are generalised from real agent-assisted research projects. None of them is
exotic: each one cost real time before anyone noticed it.

Contents:
1. Computation treated as proof
2. Literature
3. Arguments
4. Process and bookkeeping

---

## 1. Computation treated as proof

| Tempting inference | Why it fails | Do instead |
|---|---|---|
| A sampled or discretised computation gives the exact answer, for example a connected-component count on a grid. | Tiny components, near-tangencies and crossings between sample points can change the true answer. A union–find count is exact *for the sampled graph* only. | Label it `NUMERICAL`. To certify, use a method that controls the whole domain, such as certified curve topology, interval subdivision with exclusion tests, or exact root isolation. |
| A conserved sum came out right, so nothing was missed. Examples are an Euler characteristic, a Morse count, a degree or a total multiplicity. | Missing objects can come in cancelling pairs that leave the sum unchanged. | Use the sum as a consistency check only. Certify completeness separately, for example with certified root isolation or counting. |
| Floating-point solving found all solutions. | Solvers miss solutions that are ill-conditioned, close together or at large scale. | Certify each solution, and certify that there are no others with an exact or interval method. |
| Rounding or rationalising the coefficients preserves the object. | Objects at several scales, such as small ovals, close roots or nearly degenerate configurations, can change or disappear. | Certify the exact object you *recorded*. Store exact coefficients (rationals or exact binary floats) alongside any decimals. |
| A partial certificate is a complete certificate. | A lower bound can come without the smoothness, nondegeneracy or matching upper bound that the claim needs. | Read what the checker actually verified, and list any missing checks as gaps. |
| A timeout, a solver failure or a weak bound excludes a candidate. | It only shows that the computation did not decide the question. | Label the candidate `UNRESOLVED`. Only a supported bound on the right side of the target excludes it. |
| A small residual or defect means the object is close to the target. | Scaling, gauge freedom or invisible constants can make relative norms meaningless. | Compare the actual objects. Remove gauge and scale directions before measuring how close they are. |
| Improving a surrogate objective is progress. | Degenerations such as shrinking, rescaling or collapsing often improve an objective without improving the mathematics. | Fix the normalisation, and re-check the actual target condition after each improvement. |
| One run with a better outcome than one control shows the method is better. | A single replicate says nothing about variance. | Run replicates, or report it as a single observation and draw no probability claims from it. |
| No counterexample in N random trials is evidence of truth. | Counterexamples in research problems are often structured and have probability zero under naive sampling. | Report the scope and the sampling distribution. Do not turn trial counts into confidence. |

## 2. Literature

| Tempting inference | Why it fails | Do instead |
|---|---|---|
| The preprint and the published paper state the same theorem. | Statements are often weakened, corrected or re-indexed during refereeing. A preprint can claim a stronger bound than the published theorem. | Read the version you cite, and record the arXiv version and the journal version. Note any differences in the literature entry. |
| The theorem applies here. | Its hypotheses may fail: characteristic, smoothness, compactness, genericity, dimension or regularity class. | Copy the hypotheses into the literature entry and check each one against your setting. |
| Source A and source B use the same conventions. | Sign conventions, normalisations, indexing, whether 0 ∈ ℕ, and affine versus projective settings all vary between sources. | Record the convention of every source you use, and convert explicitly. |
| An obstruction for one class of objects rules out a related class. | Obstructions are usually tied to a specific representation or construction. | State exactly what the obstruction covers, and check whether your objects fall inside it. |
| I remember this result from paper P. | Memory, human or machine, confuses authors, years, theorem numbers and hypotheses, and sometimes invents papers. | Never cite without opening the source. Mark unverified citations as such. |

## 3. Arguments

| Tempting inference | Why it fails | Do instead |
|---|---|---|
| A parameter or dimension count shows the object exists. | Counts are heuristics until the equations, unknowns and transversality have been specified and proved. | Label the count `HEURISTIC`. To prove existence, write the system down and prove transversality or solvability. |
| A local mechanism gives a global theorem. | Local signs, rigidity or obstructions need not hold globally. | State the local result as local. Find a separate global argument. |
| An operation commutes with the construction. | Many constructions commute only with a restricted class of transformations, for example affine but not projective changes of coordinates. | Check commutation for the exact class of transformations you use. |
| A gluing, patching or perturbation theorem applies to every piece. | Pieces at boundaries, axes or edges often violate the nondegeneracy hypotheses. | Check the hypotheses piece by piece, and treat the boundary pieces separately. |
| "Generic" means the same thing throughout. | It can mean an open dense set, a full-measure set or "outside an explicit locus", and arguments slip between these and "for all". | Say which sense you mean every time, and make sure the conclusion matches. |
| We enumerated everything. | Usually only a finite subproblem was enumerated, such as subdivisions, graphs or sign patterns up to a bound. | Name the finite set that was enumerated exactly, and say what it does not cover. |
| It held up to degree, size or dimension n, so it holds in general. | New mechanisms often appear just beyond the checked range. | State the checked range in the claim. Keep the general statement as `CONJECTURE`. |
| The proof is complete because every lemma is proved. | The lemmas may not combine into the theorem: quantifiers, constants or hypotheses may not match. | Check the final assembly step as carefully as the lemmas themselves. |

## 4. Process and bookkeeping

| Tempting inference | Why it fails | Do instead |
|---|---|---|
| The run crashed, so the approach does not work. | Crashes, serialisation bugs and wrong file globs are implementation failures, not mathematical ones. | Record implementation failures separately. Fix them and re-run before drawing conclusions. |
| Total work = the sum of every counter. | Runs overlap, restarts double-count, and counters measure different units such as evaluations, candidates or exact checks. | Give every count a unit and a scope. Never add counts of different kinds. |
| Tidy up by overwriting the old output. | It destroys the evidence that earlier claims point to. | Write each new run to a new directory. Old evidence is read-only. |
| This is a new idea. | It may be a direction already closed under another name. | Read the Closed directions table in `STRATEGIES.md` before proposing anything. |
| The target was nearly met, so call it a success. | Quietly weakening the goal misreports the outcome. | Report what was achieved against the original target. Changing the target is the mathematician's decision. |
| The summary in my notes is accurate. | Summaries drift towards stronger claims each time they are rewritten. | When summarising, copy statuses from the Results register, not from memory or from earlier summaries. |
