# Artifact Note

This file is the original technical essay draft. It is preserved in
`reviews/` for provenance, but it is not an independent review. The later
review files pressure-test this draft and identify framing changes adopted in
the current Collatz bundle.

Absolutely. Here’s a technical essay draft in conventional vocabulary.

**Prime-Gap Divisor Structure and Collatz First-Descent Behavior**

Consider the accelerated odd Collatz map

$$C(n)=\frac{3n+1}{2^{\nu_2(3n+1)}}$$

where `n` is odd and `ν₂(m)` is the exponent of `2` dividing `m`.

For an odd seed `s`, follow the odd orbit until the first odd value below `s`. This gives a finite first-descent block. The final source in that block is the last odd value before the descent below the seed.

Now take a separate object from prime-gap arithmetic. For consecutive primes `p < q`, look at the integers strictly between them and compute the divisor-count function `τ(n)`. Define the prime-gap divisor minimizer `w` to be the leftmost integer in `(p, q)` where `τ(n)` is minimal.

The experiment asks whether Collatz first-descent blocks interact nontrivially with these prime-gap divisor minimizers.

They do.

Across odd seeds below `1,000,000`, Collatz source states hit the odd cells nearest these prime-gap divisor minimizers at about `1.76x` the same-prime-gap background rate. That enrichment remains above background in every measured `ν₂(3n+1)` stratum.

A second result appears at the terminal source of the first-descent block.

When the terminal source lies immediately below the divisor minimizer,

```text
n = w - 1
```

then the final Collatz step has the form

$$C(w-1)=\frac{3w-2}{2^k}$$

where `k = ν₂(3(w-1)+1)`.

This forces the divisor minimizer itself into the residue class

$$w \equiv 2\cdot 3^{-1}\pmod {2^k}$$

with the corresponding exactness condition modulo `2^{k+1}`.

So the object is not merely “near a prime gap feature.” The divisor minimizer inside a prime gap is occupying the exact `2`-adic residue class that makes the adjacent odd integer a terminal Collatz descent source.

That is the bridge:

```text
prime-gap divisor minimizer
+
Collatz terminal residue class modulo 2^k
```

The reset behavior changes in this regime. Terminal sources immediately below the divisor minimizer show a stronger median first-descent reset than matched no-contact blocks. The effect is not uniform across all blocks; it localizes most clearly in short first-descent families, especially blocks with exactly three odd steps and final exponents such as `k=4` and `k=8`.

This gives a concrete next problem:

Can one prove a reset inequality for short Collatz first-descent blocks whose terminal source is `w - 1`, where `w` is the leftmost divisor-count minimizer in its prime gap and

$$w \equiv 2\cdot 3^{-1}\pmod {2^k}?$$

If such an inequality closes, then prime-gap divisor structure is not just correlated with Collatz descent. It becomes part of a deterministic mechanism for a class of first-descent resets.

The empirical result is already sharp enough to be independently checked: compute first-descent blocks, locate the containing prime gaps of their source states, identify the leftmost minimum of `τ(n)` inside each gap, and compare terminal-adjacent cases against same-gap background controls.
