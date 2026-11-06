# Provenance and status statements

A manuscript produced with AI assistance needs a short statement that tells the
reader three things accurately:

1. **What AI tools did.** For example: literature search, computation, proof
   search, drafting, checking.
2. **Who checked what, and how.** Which results were checked by human authors,
   which only by independent AI review sessions, and which by nobody beyond the
   process that produced them.
3. **What stage the manuscript is at.** Working paper, preprint, submitted, or
   accepted after refereeing.

Everything here is keyed to the claim-status labels and the `review:` field
defined in `math-research-core`. The statement must agree with the Results
register.

## Principles

- **Be specific.** "AI tools were used in preparing this paper" tells the reader
  nothing. Say what the tools did for which parts.
- **Never describe a review that did not happen.** Self-review by the producing
  agent is not verification. An independent agent review is not a human review.
  An invitation to an expert is not that expert's approval.
- **Responsibility stays with the human authors.** Most publishers and preprint
  servers do not accept AI systems as authors and require disclosure of AI
  assistance. Check the current policy of the target venue; policies change.
- **Name the stage precisely.** Never call an unrefereed manuscript
  "peer-reviewed", and never call a manuscript the authors have not approved a
  "preprint by" them.
- **Name the AI system and version** if the venue asks for it. In templates, use
  a placeholder: `[AI system(s) and version(s)]`.

## Review states and what they allow you to say

| Register review field | What may be said |
|---|---|
| `none` | "has not been checked by anyone other than the process that produced it" |
| `self` | Same as `none` for external purposes. Self-review by the producing agent is not independent checking. |
| `independent` | "was checked by an independent AI review session, which had access only to the written argument". Say that the reviewer was an AI if it was. |
| `human:<name>` | "was checked by <name>". Only if that person recorded the review and agreed to the wording. |

## Status labels and the matching wording

| Status | Use | Avoid |
|---|---|---|
| PROVED | "we prove", "Theorem" | — |
| PROVED-MODULO | "assuming X, we prove", "conditional on Conjecture 4.1" | Unconditional phrasing anywhere, including the abstract |
| CITED | "by [Ref, Theorem 2.1]" | Paraphrases stronger than the source |
| CERTIFIED | "a computer-assisted proof, certified by [interval arithmetic / exact rational arithmetic / …], shows"; with the code location | "numerically verified" (understates it); "formally verified" (wrong unless a proof assistant checked it) |
| NUMERICAL | "numerical experiments suggest", "we observe numerically", "in all N examples computed" | "verify", "confirm", "show", "establish", "rigorously" |
| HEURISTIC | "heuristically", "a dimension count suggests", "we expect" | "it follows", "hence" |
| CONJECTURE | "we conjecture", with the evidence and its status | "it is known", "presumably true" without the evidence |
| REFUTED | "we give a counterexample to …" (the counterexample itself is PROVED or CERTIFIED) | "we disprove" on NUMERICAL evidence |
| UNRESOLVED | "we were unable to determine", "remains open" | Any implication of a result |

**"Formally verified" / "machine-checked"** is reserved for results checked in a
proof assistant. Even then, add that the formal statement was compared with the
informal one (see the `lean-formalisation` skill). Without that comparison, a
formal proof may prove something other than what the paper claims.

## Where the statement goes

- **Working paper or draft:** a short note on the title page or first page (an
  unnumbered footnote or a `\date{}` line), plus the full statement in a section
  near the end.
- **Preprint or submission:** a "Provenance" or "Use of AI tools" section before
  the acknowledgements, or wherever the venue's policy says.
- **Cover letters and messages to experts:** one or two sentences consistent with
  the manuscript statement, never stronger.

## Example statements

These are templates; edit them to the facts. Bracketed text must be replaced or
deleted.

**1. Working paper produced largely with AI assistance, not yet checked by
humans**

> This working paper was produced with substantial assistance from [AI
> system(s) and version(s)], which carried out [the literature search, the
> computations in Section 5 and the first drafts of the proofs in Sections 3–4].
> The arguments have been checked only by independent AI review sessions; they
> have not yet been checked by a human mathematician. Theorem A is proved
> conditionally on Conjecture 4.1. The results in Section 5 are numerical
> evidence, not proofs. This manuscript has not been peer-reviewed and may
> change substantially.

**2. Human-checked paper with AI assistance in specific tasks**

> [AI system(s)] assisted with [locating references, writing and running the
> code in Section 5, and drafting parts of Sections 1–2]. All proofs were
> checked line by line by the authors, who take full responsibility for the
> content. The code and data needed to reproduce Section 5 are available at
> [repository, commit or archive DOI].

**3. Computer-assisted proof**

> The proof of Proposition 5.2 is computer-assisted: the required inequalities
> were certified using [interval arithmetic in software X, version Y], and the
> code, input data and output certificates are available at [location]. The
> remaining results are proved by hand. [AI system(s)] was used to [write and
> test the certification code]; the certificate's correctness depends on [the
> interval arithmetic library and the stated code], not on the AI system.

**4. Mixed review status**

> Theorems A and B were checked by the authors. The proof of Theorem C was
> generated with AI assistance and has so far been checked only by an
> independent AI review session; we state it as a theorem because the argument is
> complete, but readers should regard it as not yet checked by a human expert.
> [Expert names] have been invited to inspect it.

Statement 4 states an unreviewed result as a theorem. It is acceptable only if
the register status is PROVED and the authors have decided to circulate at that
review level. Otherwise, demote Theorem C to a conjecture or a conditional result.

## Phrases to avoid in any provenance statement

- "fully verified", "rigorously checked", "validated": unless you also say who
  checked what, and how.
- "the AI proved": it hides who takes responsibility. Say what the tool produced
  and who checked it.
- "peer-reviewed": for anything not refereed by a journal or conference.
- "human-certified" or "approved by [name]": unless the person has done so and
  agreed to the wording.
- "minor AI assistance": if the AI produced the arguments or the code that the
  results depend on.
