# The Remainder Futility Tautology: A Mathematical Verification

## Executive Summary
This document formalizes a structural insight discovered and mathematically verified by the Adversarial Auditor on 2026-07-18. The insight formally proves that the statistical correlation tracking performed in `research/remainders` (e.g., `pattern_hunt.py`, `collect_remainder_stats.py`) is mathematically futile. The perceived statistical variance in the `num_zeros` metric for the GWR winner is a computational illusion caused by the intersection of sample selection bias and a fundamental algebraic tautology. All statistical correlation hunting on these specific remainder features is formally abandoned.

## Context: The `num_zeros` Metric
The current remainder probes attempt to find statistical correlations by evaluating the GWR winner against fixed macroscopic moduli: 2, 3, 5, 7, 30, 210, 2310. The scripts sum the number of moduli that divide the winner without a remainder (`num_zeros`) and search for information-theoretic relationships (e.g., Mutual Information).

## The Selection Bias Illusion
The empirical datasets currently under analysis (e.g., $p \le 400,000$) only sample astronomically small integers. For numbers of this scale, the density of semiprimes is high enough that every observed prime gap contains at least one integer with $\tau \in \{3,4\}$ (a semiprime, prime square, or prime cube). As a result, the GWR algorithm exclusively selects winners with $\tau \le 4$.

This created the false impression that GWR winners are *always* semiprimes or prime squares. However, by the Chinese Remainder Theorem (CRT), there exist arbitrarily long sequences of consecutive integers where every integer possesses at least $k$ distinct prime factors. For $k=3$, every integer in the gap has $\tau \ge 8$. The assumption that the GWR winner always has $\tau \le 4$ is a textbook example of selection bias.

## The Algebraic Tautology
For the entirety of the computable dataset, the GWR winner is strictly limited to $\tau \le 4$. This means the winner has, at most, two prime factors ($p_1 p_2$ or $p^3$ or $p^2$).

If a number $w$ has at most 2 prime factors, its evaluation against the fixed primorial moduli becomes a strict algebraic tautology:
- To be divisible by 30 ($2 \times 3 \times 5$), the number must possess at least 3 distinct prime factors.
- To be divisible by 210 ($2 \times 3 \times 5 \times 7$), the number must possess at least 4 distinct prime factors.
- To be divisible by 2310 ($2 \times 3 \times 5 \times 7 \times 11$), the number must possess at least 5 distinct prime factors.

Mathematically, a semiprime or prime square can **never** be divisible by 30, 210, or 2310. 

Furthermore, since $w > 2310$ for macroscopic gaps, $w$ cannot contain two distinct prime factors from the set $\{2, 3, 5, 7\}$ because their maximum possible product is $7 \times 7 = 49$, which is strictly less than 2310.

### Conclusion
Therefore, $w$ can be divisible by **at most ONE** prime in the set $\{2, 3, 5, 7\}$. 

Consequently, the `num_zeros` metric evaluated across these moduli can only ever equal exactly 0 or exactly 1. It is a pure algebraic tautology that measures absolutely nothing about prime gap structure; it merely indicates whether $w$'s smallest prime factor happens to be $\le 7$.

## Adversarial Auditor Verification
This finding was rigorously tested and verified by the Adversarial Auditor:

1. **Null Hypothesis:** Verified that the universal claim "GWR winners always have $\tau \le 4$" fails at scale due to the Chinese Remainder Theorem, exposing the selection bias.
2. **Tautologies:** Verified that for the observable dataset (where $\tau \le 4$), the `num_zeros` metric is a pure algebraic tautology because semiprimes structurally cannot contain enough factors to trigger the macroscopic moduli.
3. **Selection Bias:** Exposed that the apparent invariant structure is purely the result of evaluating small prime gaps where semiprimes dominate the interior.

## Final Directive
The `num_zeros` statistical correlation is a computational illusion representing the spurious intersection of selection bias and a mathematical tautology. All correlation hunting using this metric must be abandoned.
