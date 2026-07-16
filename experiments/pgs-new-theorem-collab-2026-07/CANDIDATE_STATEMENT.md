# Candidate statement (Hermes freeze — locked A/B/C)

**Status of this file:** **hypothesis / candidate**. Not in `PROOF.md`. Not theorem.  
**Working title (whole package):** Gap-Width GWR Offset Law (split by claim strength)  
**Promote-ready fragment (Hermes preference):** **Package T0 = A1 + A2 + C1** only.  
**Revision:** 2026-07-15 Hermes lock (quantifiers + hypotheses explicit)

---

## Common objects and hypotheses

**Standing hypotheses H0–H3** for all parts below unless a part weakens them:

- **H0 (consecutive primes).** Let `p, q` be primes with `p < q` and no prime strictly between them. Write `g := q − p` and assume `g ≥ 2`.  
- **H1 (interior).** Let `I := { n ∈ ℤ : p < n < q }`. If `g = 2` then `|I| = 1`; if `g ≥ 3` then `|I| = g − 1 ≥ 2`.  
- **H2 (divisor field).** Let `d(n) = τ(n)` be the number of positive divisors of `n`.  
- **H3 (GWR selection, nonempty interior).** If `I ≠ ∅`, define  
  `d_* := min_{n ∈ I} d(n)`,  
  `W := { n ∈ I : d(n) = d_* }`,  
  `w := min W` (leftmost minimizer),  
  `δ := w − p`.  
  Then `1 ≤ δ ≤ g − 1`.

**Notation.** Call `w` the **GWR witness** and `δ` the **selected-witness offset**. Empty interior occurs only for the gap `(2,3)` among consecutive primes with `g ≥ 1` in the usual ordering starting at 2; handle it as a trivial exception outside H3.

**Relation to existing theorems (not restated as new).**  
GWR existence/uniqueness of the leftmost min-`d` maximizer for the project’s objective is already universal under `PROOF.md` hypotheses. Parts A/C below are **gap-local arithmetic consequences** of that definition for fixed small `g`, complementary to UBC (which bounds `δ` against a function of `q`, not primarily against `g`).

---

## Part A — Finite-gap determinacy

**Claim strength target:** **theorem-ready** under H0–H3 (finite case analysis).  
**Status now:** **candidate / hypothesis** until human-approved promotion.

### A1 (twin gap lock)

**Statement.** Assume H0–H3 and `g = 2`.  
Then `I = {p + 1}`, `w = p + 1`, and `δ = 1`.

**Quantifiers.** For every consecutive prime pair with gap exactly 2.

### A2 (gap-four trichotomy of offsets)

**Statement.** Assume H0–H3 and `g = 4`.  
Then `I = {p + 1, p + 2, p + 3}` and  
`w ∈ I`, `δ ∈ {1, 2, 3}`,  
where `w` is uniquely the leftmost among those elements of `I` attaining minimal `d` on `I`.

**Quantifiers.** For every consecutive prime pair with gap exactly 4.  
**Non-claim.** A2 does not assert which of `{1,2,3}` occurs for which residue classes of `p`; that is optional A3/C2 work.

### A3 (optional finite catalog — not in T0)

**Statement (candidate).** For each fixed `g ∈ {2, 4, 6, 8, 10}`, the set of admissible pairs `(δ, d(w))` under H0–H3 is finite and classifiable by elementary divisibility constraints on the arithmetic progression of length `g − 1` starting at `p + 1`.

**Status.** Optional expansion; **out of Package T0** unless a peer delivers a complete classification with proof.

---

## Part B — Gap-width offset topography

**Claim strength target:** default **hypothesis / measured-motivated**. Do **not** promote from R0/R1 alone.

### B0 (trivial envelope — definitional)

**Statement.** Under H0–H3 with `I ≠ ∅`, `δ ≤ g − 1`.  

**Status.** True by definition of `I`; not a new theorem (may be mentioned as a lemma only).

### B1 (ordering / stochastic monotone — unresolved)

**Statement (candidate, not locked for promotion).**  
There exists an absolute integer `G_* ≥ 2` such that for every magnitude window `M` of the form `{p : X ≤ p < 2X}` with `X` large enough (to be quantified in a proof), the conditional law of `δ` given `g = k` is stochastically nondecreasing in `k` for all even `k` with `2 ≤ k ≤ G_*` that occur as prime gaps in that window.

**Status:** **unresolved hypothesis**. Measured R0/R1 are compatible but **do not prove** B1.

### B2 (saturation of typical offset — unresolved)

**Statement (candidate, not locked for promotion).**  
There exist absolute constants `C ≥ 1` and `G0 ≥ 2` such that for all consecutive prime pairs with `g ≥ G0` and `p` larger than an explicit `P0`, a **typical** functional of `δ` (e.g. median, or mean under a named measure on gaps) satisfies  
`typical(δ | g) ≤ C`  
or grows strictly slower than any positive power of `g` (exact functional form to be fixed before proof).

**Explicit non-claims (locked):**
- B2 does **not** assert `δ ≤ 4` for all gaps.  
- B2 does **not** assert that the measured plateau mean `≈ 4`–`4.5` on R0/R1 is a universal constant.  
- B2 does **not** replace UBC / PSP (those bound worst-case `δ` on the `q`-scale).

**Status:** **unresolved hypothesis**. Measured plateau is **support only**.

### B3 (anti-smuggle clause)

Any prose that rewrites B1/B2 as “proved that mean offset is about 4 for large gaps” is **out of contract** for this collab.

---

## Part C — Endpoint adjacency subclass

### C1 (twin adjacency — in Package T0)

**Statement.** Assume H0–H3 and `g = 2`.  
Then the witness is **left-adjacent** (`δ = 1`). The same point is also right-adjacent in the sense `δ = g − 1 = 1`.

**Quantifiers.** For every twin prime pair (consecutive primes at distance 2).  
**Status:** candidate; reduces immediately to A1.

### C2 (gap-four adjacency partition — optional)

**Statement (candidate).** Assume H0–H3 and `g = 4`.  
Then exactly one of the following holds: left-adjacent (`δ = 1`), center (`δ = 2`), or right-adjacent (`δ = 3`).

**Status:** definitional partition of A2’s `{1,2,3}`; frequency bounds remain **measured or open**, not in T0 unless proved.

### C3 (definitions only)

- **Left-adjacent:** `δ = 1`.  
- **Right-adjacent:** `δ = g − 1`.  
- **Genuine interior:** `1 < δ < g − 1`.

---

## Package T0 (single promote-able theorem bundle)

**Name (proposed for promotion process):**  
**Finite-Gap GWR Offset Determinacy for `g ∈ {2, 4}`** (or split into two lemmas under one theorem header).

**Contents:**
1. A1  
2. A2  
3. C1 (corollary of A1)

**Excluded from T0:** B1, B2, A3, C2 frequency claims, any R0/R1 numerical constant.

**Ordinary-language form of T0:**  
For consecutive primes at distance 2, the GWR witness is forced at the single interior integer `p+1`. For distance 4, the witness is one of the three interior integers, chosen as the leftmost minimum-divisor carrier among them, so the offset is only 1, 2, or 3.

---

## Dual objects (keep clean)

| Object | Bounds / describes | Status in PROOF.md |
| --- | --- | --- |
| UBC / PSP | worst-case `δ` vs `q` (Cramér-scale cutoff) | theorem under stated hypotheses |
| T0 (this package) | exact `δ` options for fixed small `g` | **candidate** until promotion |
| B1/B2 | typical `δ` vs `g` | **hypothesis only** |

---

## Promotion gate (pointer)

No part of this file enters `PROOF.md` until the human-approved process in `PROMOTION_GATE.md` (agy) is green, with proof text complete for T0 only unless human expands scope.

STATUS labels in force: **hypothesis / candidate** throughout.
