# Adversarial Attack & Minimal Corollary

## Attack on the Candidate Seed

1. **Classical Drift:** Part B flirts with inferring prime distribution from divisor counts. We must explicitly decouple: we are describing the *conditional* behavior of `d(n)` *given* a gap `g`. Asserting how often gap `g` occurs is classical prime number theory and outside PGS. If B asserts the distribution of `δ` unconditionally, it drifts. It must be conditioned strictly on `g`.
2. **Tautology:** "If `g=2`, `δ=1`" is trivially tautological since the interior is a singleton. Part A is mathematically sound but structurally trivial. We must not present Part A as a profound breakthrough; it's a definitional boundary condition.
3. **Super-Signal Re-entry:** The notion in Part B that mean offset "saturates" near `C ≈ 4` for large gaps risks re-introducing the invalidated Super-Signal. If we claim a universal constant `C` bounding the mean, we might be hallucinating a global signal from R0/R1 local data. B2 must not claim a global constant without proof.

## Minimal Proved Corollary (if Part B fails)

If Part B remains a hypothesis (which is highly likely as it relies on unproved saturation), the minimal theorem-grade claim is **Finite-Gap Determinacy and Left/Right-Adjacency Classification (Part A & C)**.

**Corollary Statement:**
For consecutive primes `p < q` with gap `g = q - p`:
1. If `g = 2`, the GWR witness is uniquely `w = p+1` and the offset is exactly `δ = 1` (left-adjacent).
2. If `g = 4`, the interior is `{p+1, p+2, p+3}`. The GWR witness offset `δ` must be in `{1, 2, 3}`. Determinacy can be strictly resolved by parity and divisibility by 3, yielding a finite set of outcomes for `δ` based on the residue of `p`.
3. Adjacency: The witness offset `δ` is bounded by `g-1`. For finite `g`, the frequencies of `δ=1` (left-adjacent) and `δ=g-1` (right-adjacent) are fully deterministic under local divisibility constraints.
