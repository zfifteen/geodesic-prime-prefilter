# What Counts As A Proof Of GWR

This note records the exact standard being applied when deciding whether it is
technically correct to say that the `Gap Winner Rule` (`GWR`) is **proven**.

The purpose is not to dismiss the current evidence surface.
The purpose is to separate three different things clearly:

- a theorem,
- an evidence-backed prime-gap law on a tested surface,
- and a universal proof for all prime gaps.

## The Statement At Issue

The `Gap Winner Rule` says:

for every prime gap $(p, q)$ with at least one composite interior, the score

$$
L(n)=\left(1-\frac{d(n)}{2}\right)\ln(n)
$$

is maximized exactly at the leftmost interior composite with minimal divisor
count.

Equivalently, if

$$
w = \min \{\, n : p < n < q,\ d(n)=\delta_{\min}(p, q) \,\},
$$

where

$$
\delta_{\min}(p, q)=\min_{p<n<q} d(n),
$$

then `GWR` is the claim that

$$
L(w) > L(n)
\qquad
\text{for every other interior composite } n \neq w.
$$

That is the infinite statement whose proof status is being discussed.

## What Is Not Required

To call `GWR` proven, it is **not** necessary to test all prime gaps one by
one.

That would be impossible.

A proof of an infinite statement normally works by one of these routes:

1. a direct universal argument that covers every gap at once,
2. or a reduction showing that any counterexample must lie in a finite range,
   followed by an exhaustive exact verification of that finite remainder.

So the issue is not "did we test infinitely many gaps?"

The issue is "do we now have a finite deductive argument that eliminates the
infinite tail?"

## The Narrow Current Gap

The present issue is narrower than "how can one ever prove an infinite
prime-gap statement?"

The current exact ordered-dominance theorem already proves one half of the
winner claim:

- if `w` is the leftmost interior carrier of the minimal divisor class,
- then `w` beats every later interior composite.

That is not under dispute.

The only missing universal step is the earlier-spoiler direction:

- can some earlier interior composite `a < w` with larger divisor count
  `d(a) > d(w)` nevertheless satisfy `L(a) > L(w)` inside a prime gap?

That is the exact point at issue.

So the current standard is not demanding:

- an impossible check of infinitely many gaps,
- or a brand-new theorem replacing the existing dominance theorem.

It is demanding only one of these:

- a direct gap-specific argument ruling out every earlier spoiler,
- or a finite-remainder reduction that confines every possible earlier spoiler
  to a bounded range.

## What Does Count As A Proof

Any one of the following would justify saying `GWR` is proven.

### Route A: Direct Universal Proof

Produce a theorem that, for an arbitrary prime gap $(p, q)$, lets

$$
w = \min \{\, n : p < n < q,\ d(n)=\delta_{\min}(p, q) \,\}
$$

and then proves

$$
L(w) > L(n)
\qquad
\text{for every } n \in (p, q),\ n \neq w.
$$

This route needs no computation beyond ordinary lemma verification.

If such a direct proof exists and is written cleanly, `GWR` is proven.

### Route B: Counterexample Reduction Plus Finite Exhaustion

This is the standard computer-assisted proof route.

It requires all of the following pieces.

#### B1. Exact Elimination Of Later Candidates

One exact theorem must show that the `GWR` candidate beats every later interior
candidate.

The current ordered-dominance theorem already supplies this backbone:

if $a < b$ and $d(a) \le d(b)$, then $L(a) > L(b)$.

That handles every later interior point once the leftmost minimum-divisor
carrier is fixed.

#### B2. Exact Reduction Of Earlier Spoilers

One exact theorem must show that any earlier interior composite that could beat
the `GWR` candidate must satisfy an explicit severe restriction.

One plausible reduction path is this.

Let $w$ be the leftmost interior carrier of the minimal divisor class
$\delta = d(w)$, and let $a < w$ be an earlier interior composite with larger
divisor count $D = d(a) > \delta$.

If $a$ were to beat $w$, then necessarily

$$
L(a) > L(w),
$$

which is equivalent to

$$
(D-2)\ln a < (\delta-2)\ln w.
$$

So one must have

$$
w > a^{(D-2)/(\delta-2)}.
$$

In an odd prime gap, Bertrand gives

$$
q < 2p,
$$

and since

$$
p < a < w < q,
$$

one gets

$$
w < 2a.
$$

Combining the two inequalities gives the necessary spoiler condition

$$
a^{(D-\delta)/(\delta-2)} < 2,
$$

or equivalently

$$
a < 2^{(\delta-2)/(D-\delta)}.
$$

That kind of class-pair bound is exactly the sort of reduction needed here.

To count as a proof route, the reduction must be written rigorously and applied
to every possible earlier spoiler class.

#### B3. Explicit Finite Remainder Bound

After the spoiler reduction is complete, there must be an explicit bound $B$
such that:

- every possible counterexample to `GWR` lies below $B`,
- or equivalently, every gap above $B$ is eliminated by theorem.

This is the step that closes the infinite tail.

Without an explicit finite remainder, the argument is still only partial.

#### B4. Exhaustive Exact Verification Up To The Bound

Once the theorem reduces all possible failures to gaps below $B$, one may
exhaustively verify every prime gap up to $B$.

For this to count as part of the proof, the computation must use one of:

- exact score comparison,
- exact sign determination of winner margins,
- or a separately proved comparison method that is mathematically equivalent.

Simple floating-point argmax agreement by itself is not the strongest possible
foundation for a proof artifact unless accompanied by a proof that rounding
cannot change the winner.

#### B5. Reproducible Proof Artifact

The finite verification must be:

- deterministic,
- fully reproducible,
- and narrow enough that another person can rerun it and inspect the logic.

If `B1` through `B5` are all present, then `GWR` is proven by a
computer-assisted finite-remainder argument.

### Route C: Reduction To An Already Proved External Theorem

If `GWR` can be shown to follow as a corollary of an already established theorem
about divisor profiles in prime gaps, then that also counts as a proof.

In practice, this still requires:

- a precise reduction theorem in this repo,
- and a correct appeal to the external theorem.

At present, no such external reduction is documented here.

## What Does Not Count As A Proof

The following do **not** by themselves justify saying `GWR` is proven.

### 1. Finite Validation Surface Alone

Even a very large zero-counterexample surface is still finite evidence unless
it is attached to a reduction that eliminates all larger cases.

### 2. Sampled High-Scale Windows Alone

Broad scale coverage is valuable, but sampling is not the same thing as a proof
for all gaps.

### 3. Endorsements Or External Reviews Alone

A deep-dive report, AI review, or positive expert reaction can strengthen
confidence. It does not replace a universal argument.

### 4. "For All Practical Purposes" Language

This may be fair rhetoric for overwhelming evidence.
It is not the same as the mathematical word `proven`.

### 5. The Ordered-Dominance Theorem By Itself

The current exact ordered-dominance theorem is real and important.
But by itself it only handles later candidates once the `GWR` candidate is
fixed.

To prove `GWR` for all gaps, one still needs either:

- a direct theorem eliminating every earlier higher-divisor spoiler,
- or a reduction that confines every possible earlier higher-divisor spoiler to a finite
  remainder that can be checked exactly.

## What The Current Repo Already Has

The repo already has:

- an exact ordered-dominance theorem,
- a current `GWR` winner law on the tested surface,
- theorem-candidate refinements such as `No-Later-Simpler-Composite`,
- and a dominant `d=4` reduction with a very strong tested surface.

That is already substantial.

It means the current project is not missing mathematics.
It means the remaining issue is one specific universal step for the whole
prime-gap statement: the elimination of earlier higher-divisor spoilers.

## Exact Public Wording Standard

This is the wording standard being applied.

### Safe To Say Now

- `GWR is the current prime-gap winner law on the tested surface.`
- `The repo reports zero counterexamples on its current exact and sampled validation surfaces.`
- `An exact ordered-dominance theorem supplies the current theorem backbone and proves the later-candidate half of the winner comparison.`
- `The dominant d=4 regime reduces to square exclusion plus first-d=4 arrival on the tested surface.`

### Not Yet Safe Unless The Above Proof Routes Are Closed

- `GWR is proven for all prime gaps.`
- `The full prime-gap winner law is now a theorem.`

### Safe Once Route A, B, Or C Is Completed

- `GWR is proven.`
- `The Gap Winner Rule is a theorem for all prime gaps.`
- `The full prime-gap winner law has been proved, with [direct proof / computer-assisted finite reduction / reduction to known theorem].`

## Practical Decision Rule

The decision rule is simple.

It is technically correct to say `GWR` is proven if and only if at least one of
these is true:

1. a direct universal proof is written,
2. a finite-remainder reduction theorem is written and the finite remainder is
   exhaustively verified exactly,
3. or a correct reduction to an already proved external theorem is written.

If none of those is yet in hand, then the right description is:

`very strong evidence`, `zero-counterexample validated on the current surface`,
or similar language of that kind.

## Safe Summary

To call `GWR` proven, it is not necessary to test all prime gaps.

It is necessary to do something stronger and more finite:

- either prove the full statement directly,
- or prove that any failure would have to occur in a finite explicit range and
  then check that range exactly.

That is the standard being applied here.
