# Direction 4: Two Bounds, One Story (Bridge)

This document clarifies the relationship between the two distinct bounding theories present in our research landscape: the Zhang–Maynard classical bound on prime gaps and the Prime Gap Structure (PGS) universal bounded compression theorem.

## 1. What Each Theory Bounds

| Theory | Object Bounded | Scope | Mode of Action |
| :--- | :--- | :--- | :--- |
| **Zhang–Maynard (Classical)** | Gap between *some* pairs of primes: $(q - p) \le C$ infinitely often. | Infinitely often (i.o.). Applies to specific tuples, not every gap. | Sieve geometry, admissibility, modular covering. |
| **PGS Compression (Theorem)** | Internal witness offset within the gap: $(w - p)$. | Universal. Applies deterministically to *every* consecutive prime gap $(p, q)$. | Divisor-field code, GWR, chamber reset logic. |

## 2. Non-Implication

These two bounds describe fundamentally different dimensions of the gap and do not imply each other.

*   **Zhang–Maynard does not imply PGS Compression:** The fact that *some* prime gaps are small (e.g., $\le 246$) provides no mechanism to explain the universal structural behavior (witness offset, residual codes) inside *every* gap, especially the large ones. 
*   **PGS Compression does not imply Zhang–Maynard (or Twin Primes):** The PGS bounded compression theorem strictly bounds the witness structure $w$ within a given gap $(p, q)$ relative to $p$. It does *not* bound the size of the overall gap $(q - p)$. As detailed in `PROOF.md`, universal bounded compression is a theorem under stated hypotheses, but it does not claim that consecutive primes will occur within a fixed distance infinitely often.

## 3. Scope of Comparison

As established in our research principles, we do not merge these categories. Classical sieve geometry and Zhang–Maynard bounds are referenced strictly for **comparison only**. 

*   **PGS** remains the primary lens for extracting the internal structural readout of a given consecutive gap.
*   **Classical bounds** operate externally to establish the infinitude of specific proximity events, without examining the gap interior via GWR or residual maps.
