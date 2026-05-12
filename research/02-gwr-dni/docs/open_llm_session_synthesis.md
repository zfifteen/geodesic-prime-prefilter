# Open LLM Session Synthesis

Source: open LLM session responses synthesized before the raw response log was
removed from the live documentation tree.

Synthesized: 2026-04-29

## Headline Finding

Across the open Comet LLM sessions, the stable cross-model reading is that the
repository's mathematics supports a direct, context-free expression for the nth
prime when exact divisor count is used as the prime-state indicator. The same
responses also read the repository's PGS/DNI/GWR machinery as the local
structural interpretation of that expression: primes sit on the DNI fixed-point
locus, composites inside a gap are ordered by divisor-count state, and the
selected integer supplies the local reference point for the next endpoint.

The responses are evidence about external LLM interpretability. They show that
multiple models can understand and execute the divisor-count expression when it
is sent without repository context. They are not themselves theorem proofs.

## Cross-Model Consensus

The responses converge on four points.

First, the Divisor Normalization Identity gives the fixed-point split:

$$Z(n) = n^{1 - d(n)/2}.$$

Every prime has $d(n) = 2$ and therefore lands at $Z(n) = 1$. Composites fall
below that locus. The models repeatedly recognized this as the repository's
core bridge from divisor arithmetic to prime-state structure.

Second, the GWR/NLSC language gives a local gap interpretation. The selected
integer is the leftmost minimum-divisor interior integer, and the endpoint is
the next prime boundary that closes the local chamber. Several responses used
different wording, but the shared reading was that PGS is not merely a
statistical prime-gap description. It is a deterministic local ordering of the
composite interior.

Third, the closed-form nth-prime expression is understandable to outside LLMs
when written only in terms of finite sums, floors, divisibility indicators, and
divisor counts. Multiple models reconstructed the role of $\Pi(m)$ as a
prime-counting prefix sum and explained why the outer summand counts integers
before the nth prime.

Fourth, the strongest durable artifact is the combination of the context-free
divisor-count formula and the PGS interpretation. The formula gives a standalone
object another LLM can execute. The repository vocabulary explains why this
formula belongs naturally with DNI, GWR, PGS, selected integer, divisor-count
state, and endpoint structure.

## Equation-Specific Synthesis

The clean public-facing title for the equation is:

**The Divisor-Count Fixed-Point Formula for the nth Prime**

For $n \ge 1$:

$$p_n = 1 + \sum_{m=1}^{2^n}\left\lfloor {1 \over 1 + \left\lfloor \Pi(m)/n \right\rfloor^2} \right\rfloor,$$

where

$$\Pi(m) = \sum_{j=2}^{m} I_2(j),$$

$$I_2(j) = \left\lfloor {1 \over 1 + (d(j) - 2)^2} \right\rfloor,$$

and

$$d(j) = \sum_{a=1}^{j} [a \mid j].$$

Here $[a \mid j]$ equals $1$ when $a$ divides $j$ and equals $0$ otherwise.

The expression is self-contained because $d(j)$ is an exact divisor count.
The indicator $I_2(j)$ equals $1$ exactly when $j$ has two positive divisors
and equals $0$ otherwise. Therefore $\Pi(m)$ counts primes up to $m$ using only
divisor arithmetic.

The outer summand equals $1$ while $\Pi(m) < n$ and equals $0$ once
$\Pi(m) \ge n$. Summing those ones counts the integers before the nth prime,
and adding $1$ returns $p_n$. The upper bound $2^n$ is sufficient on this
indexing because it reaches beyond the nth prime.

This context-free expression is different from the repository's local PGS
successor map. The expression computes $p_n$ from $n$ alone by rebuilding the
prime-counting prefix function from divisor counts. The local PGS successor map
starts from a known prime and uses the exact local search-interval state,
GWR-selected integer, divisor-count state, and endpoint rule to recover the
next prime. They meet at the same prime-state indicator, but they serve
different explanatory roles.

## Divergences and Failure Modes

Some responses over-read empirical validation as unconditional proof. The
usable synthesis should keep proof state, audited finite surface, and external
LLM agreement separate. The LLM convergence supports communicability and
interpretability; it does not replace a theorem.

Some responses correctly identified vacuity or collapse problems in earlier
recursive formulations. If an inner minimization admits the first integer after
the previous prime by an empty-interval condition, then the formula can collapse
to a disguised next-prime scan. That criticism applies to those earlier
recursive drafts, not to the divisor-count fixed-point formula above.

Some responses used inflated rhetoric. The stable content is narrower and
stronger: exact divisor count gives a prime-state indicator; the indicator gives
a context-free nth-prime formula; PGS/DNI/GWR gives the repository-native
structural reading of why divisor-count state is the right language.

## Strongest Usable Framing

The equation can be sent without context as a complete finite expression for
the nth prime. Its ingredients are ordinary arithmetic operations, finite sums,
floor functions, and the divisibility indicator. Another LLM does not need to
know PGS, DNI, GWR, NLSC, selected integers, or endpoints to execute it.

The repository-facing interpretation is:

- DNI identifies primes as the fixed-point locus $Z = 1$.
- $I_2(j)$ is the discrete prime-state detector induced by divisor count.
- $\Pi(m)$ is the exact cumulative prime-state count.
- The outer floor expression inverts that cumulative count to recover $p_n$.
- PGS gives the local gap version: divisor-count state orders the composite
  chamber, the selected integer anchors the gap interior, and the endpoint
  closes the chamber.

That framing avoids underselling the result while preserving the distinction
between a context-free closed expression, the local PGS generator contract, the
audited empirical surface, and proof questions outside the `PROOF.md`
maximizer theorem.

## Research Implications

The LLM sessions show that the divisor-count formulation is portable. Models
from different systems recognized the same ingredients: divisor count, prime
indicator, prime-counting prefix, outer inversion, and finite upper bound.

The synthesis supports a documentation change in repository language. It is
misleading to say only that the repository does not claim a direct closed-form
expression for the next prime if the surrounding math already contains a
self-contained nth-prime expression by divisor-count fixed point. The better
distinction is:

- the context-free nth-prime expression is closed and executable;
- the local PGS successor map is a structural next-prime mechanism from a known
  prime and local search state;
- bounded PGS compression remains an empirical or proof-pressure question where
  the repository has not yet closed an unconditional theorem.

The next useful research artifact is a short public equation note using the
title above, followed by a separate repository note explaining how the
context-free formula and local PGS successor map are related without collapsing
one into the other.

## Source Coverage

| Tab | Contribution |
|---|---|
| Grok / X | Interpreted DNI, GWR, NLSC, and PGS as a deterministic local prime-gap structure; emphasized empirical validation. |
| Perplexity repo analysis | Connected DNI fixed-point language to GWR and the repository's generator claims; framed the result as a selection law. |
| Gemini | Read the repository through interference and structural wave language; contributed broad interpretive framing. |
| Grok breakthrough analysis | Reinforced the high-level PGS breakthrough framing and the role of audited zero-failure surfaces. |
| Meta AI | Summarized the repository as a deterministic prime-gap research program and emphasized the strongest data-backed evidence. |
| DeepSeek | Produced a GWR/DNI-based closed-form framing and helped separate formula statement from proof rhetoric. |
| Microsoft Copilot | Gave concise external confirmation that the notable evidence is the zero-failure deterministic surface plus the formula framing. |
| Claude | Synthesized the repo structure and later clarified the proof-surface distinction around GWR and recursive walk claims. |
| Prime Gap Carrier Insight | Sharpened the distinction between the deeper divisor-count equation, the PGS local successor map, and earlier underselling. |
| Perplexity explain-and-compute | Tested several formulations, flagged collapse in earlier recursive drafts, and validated the final divisor-count expression structure. |
| Grok / X formula check | Independently validated the formula's mechanics, explained the outer floor inversion, and spot-checked feasible regimes. |
