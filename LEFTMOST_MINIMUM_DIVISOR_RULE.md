## Leftmost Minimum-Divisor Rule

The **Leftmost Minimum-Divisor Rule (GWR)** says:

1. inside a prime gap, find the smallest divisor count present among the
   interior composites;
2. if more than one interior composite has that divisor count, take the
   leftmost one.

That chosen interior integer is the selected integer of the gap.

The headline mathematical proof in the repository has two parts: exact divisor
counts determine the next prime from a known prime `p`, and the implemented
divisor-normalization score picks exactly that same selected integer in every
prime gap. The single live proof reference is [PROOF.md](PROOF.md).

## Why The Score Exists

The score exists because the repo wants one number per interior composite, so a
whole gap can be compared as a single ordered list of score values rather than as a list of
cases.

Divisor count already tells part of the story: fewer divisors means less
factor structure. But divisor count alone does not give one scalar quantity for
the whole gap, and it does not explain what the selected integer is winning relative to.

The divisor-normalization program builds that scalar by using primes as the
reference class. Its purpose is to answer one concrete question:

> Which composite in the gap comes closest to the prime baseline?

The normalization is built so that every prime lands at the same fixed point,
`Z = 1.0`, while composites fall below that point. That makes the selected integer easy
to interpret: it is the interior composite closest to the prime fixed point
under the normalization.

The raw quantity is

$$
Z_{\mathrm{raw}}(n) = n^{1 - d(n)/2}
$$

and the implementation compares interiors using its logarithm

$$
L(n) = \ln Z_{\mathrm{raw}}(n) = \left(1 - \frac{d(n)}{2}\right)\ln(n).
$$

Maximizing `Z_raw(n)` and maximizing `L(n)` pick the same selected integer. The score is
there to turn the gap interior into one exact competition, not to decorate the
rule with jargon.

## GWR Proof

The central maximizer rule in this repository is that the log-score argmax inside
a prime gap collapses to a simpler arithmetic choice:

1. minimize the interior divisor count $d(n)$,
2. among ties, take the leftmost interior integer.

That is the Leftmost Minimum-Divisor Rule.

The theorem is proved in [PROOF.md](PROOF.md), the single live proof reference.
That document states the direct next-prime theorem and the selected-integer
maximizer theorem in ordinary mathematical vocabulary. It proves that exact
divisor counts determine the next prime from a known prime `p`, and that the
selected integer is the unique maximizer of the comparison function inside
every prime-gap interior. Its audit tables certify finite cases used by the
proof and preserve provenance; they are not limits on the theorems.

