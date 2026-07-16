# FALSIFIERS.md

**Author:** claude  
**Date:** 2026-07-15  
**Collab epoch:** pgs-new-theorem-collab-2026-07  
**Status:** adversarial review — parts labeled per candidate strength

---

## Purpose

This document lists what would kill each candidate part (A / B / C) of the Gap-Width GWR Offset Monotone Saturation Law candidate. Two kill types are distinguished throughout:

- **Proof kill (P-kill):** A mathematical counterexample or a valid proof that the statement is false. This kills the candidate dead regardless of measured data.
- **Measured kill (M-kill):** A measured counterexample that provides empirical pressure against the claim, which would push the candidate to "refuted by measurement" if confirmed under broader coverage. Not a logical kill, but fatal to promotion.

---

## Part A — Finite gap determinacy

### A1: If `g = 2`, then `I = {p+1}`, `w = p+1`, `δ = 1`.

**Status: nearly definitional. Low falsifier risk.**

- **P-kill:** A consecutive prime pair `p < q` with `q − p = 2` and no interior integer. Impossible by definition of the gap interval `I = {n : p < n < q}`. For `g = 2`, `I = {p+1}` contains exactly one element. `w` is forced to `p+1`, `δ = 1`. This is a pure set-cardinality argument.  
- **M-kill:** None possible. A1 is not an empirical claim; it follows from the definition of the gap objects alone. The only "falsifier" would be a logic error in those definitions, which is agy's territory.
- **Verdict:** A1 is essentially a lemma, not a conjecture. If hermes locks the formal statement cleanly, A1 should be first into the promotion pipeline.

### A2: If `g = 4`, then `I = {p+1, p+2, p+3}`, `δ ∈ {1, 2, 3}`.

**Status: definitional + arithmetic. Low risk.**

- **P-kill:** Same set argument as A1. `I` has exactly 3 elements; `δ = w − p ∈ {1, 2, 3}` by set membership. Unfalsifiable as stated.
- **The interesting sub-claim:** which of the three offset values actually minimizes `d`? Divisibility constraints on `p+1`, `p+2`, `p+3` (at least one of which is divisible by 3, at least one even) produce concrete tau lower-bounds. A claim that *a specific δ* dominates for g=4 would need proof; the bare "δ ∈ {1,2,3}" does not.
- **P-kill risk for any frequency claim:** if A2 is extended to claim "δ=1 dominates for g=4", a single prime pair `p < q = p+4` where `p+2` (or `p+3`) has lower tau than `p+1` would P-kill that extension. Such pairs exist: e.g., if `p+1 ≡ 0 (mod 4)` then `d(p+1) ≥ 3` while `p+2` might be `2 × odd-semiprime` with `d=4`, but `p+3` might be a prime square with `d=3`. Depends on the specific prime. No universal frequency claim for A2 sub-cases is safe without proof.
- **Verdict:** A2 bare is fine. Frequency extensions need explicit arithmetic proof for each fixed pair of divisibility classes.

### A3 (optional): Classify `(δ, d(w))` for small fixed `g ∈ {2,4,6,8,10}`.

- **P-kill risk (moderate):** For `g = 6`: interior `{p+1, …, p+5}`. Among these, `p+3` is always divisible by 3 if `p ≡ 0 (mod 3)` — but `p` itself is prime, so `p ≠ 3` implies `p ≡ 1` or `2 (mod 3)`. This restricts the residue classes but doesn't immediately force `δ`. For `g = 10`, the interior has 9 elements and the divisibility landscape grows complex. Classification without explicit modular arithmetic for each residue class is at P-kill risk from overlooked cases.
- **M-kill risk (low):** R0/R1 measured data covers `g ≤ 154` for R1. For the small finite cases `g ∈ {2,4,6,8,10}`, exhaustive verification from measured data is easy and would confirm or kill specific classification claims. Grok's note that R1 max gap is 154 means we have rich coverage for all of A3.
- **Verdict:** A3 classification claims should be verified exhaustively against R0/R1 before any promotion claim is locked by hermes. High chance of surviving, but only if every modular case is spelled out.

---

## Part B — Gap-width offset topography

**Default:** stays hypothesis. I treat Part B with maximum adversarial pressure.

### B1 (weak ordering): Distribution of `δ | g` is stochastically nondecreasing in `g` for `2 ≤ g ≤ G*`.

- **P-kill:** Find a gap width `g2 > g1` (both within claimed range) where the δ distribution for `g2` first-order stochastically dominates **neither** the g1 distribution, nor is it shifted right. A specific example: if `g = 6` gaps systematically yield lower median δ than `g = 4` gaps (perhaps because g=6 gaps happen in regimes where composite structure forces small δ), B1 is P-killed.
  - **Measured signal:** the measured R1 plateau near ~4–4.5 for *large* gaps, with mean ~2.0 for "small" gaps, is consistent with B1 for `g ≤ 20` roughly. But "stochastically nondecreasing" is a stronger claim than "mean increases".
  - **Risk:** the stochastic dominance condition can fail even when means are ordered. Two distributions can have the same mean but different shapes such that CDF crossing violates stochastic dominance. B1 is at serious P-kill risk from distribution-shape analysis.
- **M-kill:** Cross-gap-width distribution comparison in R0/R1 data at g=4, g=6, g=8, g=10, g=12 separately. If the empirical CDFs cross, B1 is measured-killed even if means are ordered. **We have not done this comparison explicitly.** Flag for MEASURED_PRESSURE.md.
- **Verdict:** B1 as stated ("stochastically nondecreasing") is too strong without explicit CDF analysis. Weaker form (mean ordering) is more defensible.

### B2 (saturation): Mean δ remains `O(1)` in `g` for large gaps, or high quantile plateaus.

**This is the main smuggling risk Grok warned about. I treat it accordingly.**

- **The smuggling version being killed:** "Mean δ ≈ 4 for all gaps above some threshold" as a *universal theorem*. Kill reasons:
  1. **R0/R1 measured mean ≈ 4.5 for large gaps** is a measured mean in `p ≤ 10^7`. This does not bound the mean universally over all primes. As gaps grow to Cramér scale `O((log p)^2)`, the interior grows as well, and the min-τ element could shift further from the left endpoint.
  2. **UBC already controls worst-case δ** at `O((log q)^2)` scale. The measured "plateau at 4–4.5" is consistent with UBC but is not a replacement or improvement on it at large scale.
  3. A theorem "mean δ is bounded by an absolute constant C for all sufficiently large consecutive prime gaps" would require a proof that the distribution of the leftmost min-τ element in gaps of growing width converges. That's a much deeper result.
- **P-kill for the universal constant version:** A sequence of prime gaps of growing width `g_n → ∞` where the mean offset `δ` over the corresponding R2/R3 bands grows (even slowly) would kill the "absolute constant" version. No such sequence is known but none is ruled out either.
- **M-kill for any version:** compute mean δ separately for large-gap bands (g ≥ 50, g ≥ 100) in R1. If the mean still sits ≈ 4–4.5 there too, that's consistent; if it rises to 5–6 in higher bands, the plateau story weakens even as a measured description. **This band analysis is not yet in MEASURED_GROUNDING.md.**
- **Verdict:** Kill the "mean ≈ 4 universal" version. Keep only: "In R0/R1, mean δ plateaus near ~4–4.5 for gaps above ~g=20. This is measured motivation only. It says nothing about the universal bound or about regimes beyond R1." If hermes wants a provable fragment from B2, the best candidate is the weak form: "δ = O((log p)^2)" — which is already implied by UBC and adds nothing new. A genuinely new proved result would need to tighten the multiplicative constant, which requires new analytic input.
- **B3 (non-claim) is safe by construction.** No falsification needed; it's a scope disclaimer.

---

## Part C — Endpoint subclass

### C1: For `g = 2`, every case is left-adjacent (`δ = 1`).

- **P-kill:** Impossible — same as A1. C1 = A1 restated in endpoint language.
- **Verdict:** Safe. Definitional.

### C2: For `g = 4`, left-adjacent / right-adjacent / center are the only options; frequency bounds only if clean.

- **P-kill of the tripartite classification:** None possible. The three offset values for `g=4` are `{1, 2, 3}`, which map exactly to left-adjacent / center / right-adjacent. This is just naming, not a claim.
- **P-kill of any frequency bound:** If a claim like "center (δ=2) is never the minimum for `g=4`" is asserted, that is P-killable. Example: if `p+2` is a prime square (τ=3) while `p+1 ≡ 0 (mod 4)` gives τ(p+1) ≥ 3, and `p+3` is divisible by at least 2 primes so τ(p+3) ≥ 4, then `p+2` has the minimum τ and `δ = 2` (center). This happens. So any claim that center is impossible for `g=4` is P-killed.
- **M-kill for proposed frequency claims:** For `g=4` specifically, the R1 dataset has thousands of such pairs. Any frequency claim should be checked against that. If the claim passes R1, it survives M-kill for now.
- **Verdict:** C2 classification is safe. Frequency claims need explicit R0/R1 verification before entering a promotion-candidate statement.

---

## Overall verdict table

| Part | Bare form | P-kill risk | M-kill risk | Recommendation |
|------|-----------|-------------|-------------|----------------|
| A1 | δ=1 for g=2 | None (definitional) | None | Theorem-ready |
| A2 | δ∈{1,2,3} for g=4 | None (definitional) | None | Theorem-ready |
| A2 ext. | frequency claim for g=4 | Moderate | Low (R1 covers it) | Verify first |
| A3 | classify g∈{2,4,6,8,10} | Moderate (modular cases) | Low | Check vs R0/R1 before locking |
| B1 | stochastic ordering in g | High (CDF crossing) | Moderate | Downgrade to mean ordering or CDF verify |
| B2 | mean δ = O(1) universal | Very high (universal bound) | Moderate | Kill universal form; keep as measured observation only |
| B3 | δ≤4 not claimed universally | N/A (disclaimer) | N/A | Retain as scope guard |
| C1 | left-adjacent for g=2 | None (=A1) | None | Theorem-ready |
| C2 | tripartite classification | None (naming) | None | Safe |
| C2 ext. | frequency claims | Moderate | Low (R1 covers) | Verify before promoting |

---

## Best theorem-shaped fragment if Part B fails

If Part B cannot be proved in any interesting form (likely for B2, at risk for B1), the residual theorem worth promoting is:

**Finite Gap Classification Corollary (FGC):**

> Let `g ∈ {2, 4}`. For any consecutive prime pair `(p, q)` with `q − p = g`, the GWR-selected witness offset `δ` is completely determined by the divisor-count minimizer among the `g − 1` interior integers. For `g = 2`, `δ = 1` always. For `g = 4`, `δ ∈ {1, 2, 3}` with exact divisibility constraints on each case derivable from the residue classes of `p (mod 6)`.

This is genuinely new as a named theorem (it's not stated anywhere in PROOF.md), is immediately proved, and makes no empirical overclaim. It also extends cleanly to `g ∈ {4, 6}` via finite modular case-work, giving a real classification theorem that anchors the A/C parts into a provable package without depending on Part B at all.

That is my recommendation for the single best theorem-shaped fragment.

---

**Paths written:** `experiments/pgs-new-theorem-collab-2026-07/FALSIFIERS.md`  
**What remains for lead:** MEASURED_PRESSURE.md is the companion file (see next artifact).
