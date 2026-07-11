# d=4 GWR Fractional-Position Bound

**Date**: 2026-06-15  
**Status**: Proved lemmas (Phases 1 to 5) + measured finite-base anchor + falsification harness

This note proves the d=4 **chamber** geometry (integer gap placement). It does
not prove RH and must not be read as a spectral-transfer driver. A related
transfer draft exists but is **dormant** as a live RH path
(`source_to_spectral_transfer_lemma.md`). `PROOF.md` controls the Interior
Maximizer Theorem; this document proves corollaries on the d=4 packet class.

---

## 1. Objects

For consecutive primes `p < q`, chamber `I = {p+1,…,q−1}`, GWR carrier

```
w = min{n ∈ I : τ(n) = min_{m∈I} τ(m)}.
```

Offsets:

```
r = w − p,    g = q − p,    frac_pos = r/g.
```

Right margin `m = q − w = g − r`. Identity:

```
frac_pos = 1 − m/g.
```

---

## 2. Phase 1: Infrastructure (proved)

### Lemma 1.1 (Fractional-position identity)

For `p < w < q`:

```
frac_pos = (w−p)/(q−p) = 1 − (q−w)/(q−p).
```

*Proof.* Algebra.

### Lemma 1.2 (Left-prefix exclusion)

If `w` is the leftmost minimum-`τ` point with `δ = τ(w)`, then for every
`i` with `1 ≤ i < r = w−p`:

```
τ(p+i) > δ.
```

*Proof.* `prime_gap_exclusion_consequences.md`: equal or smaller `τ` before `w`
contradicts leftmost minimality.

### Lemma 1.3 (Right-suffix exclusion)

For every `i` with `r < i < g`:

```
τ(p+i) ≥ δ.
```

*Proof.* Same source: strict smaller `τ` after `w` contradicts minimality of `δ`.

### Lemma 1.4 (Bertrand gap bound)

For primes `p < q` with `p > 1`: `q < 2p`, hence `g < p`.

*Proof.* Bertrand postulate; used in `PROOF.md` §Witness Threshold.

### Lemma 1.5 (Witness threshold, d=4 adjacent row)

`T(4,5) = 4`. If `p > 4`, then `p > T(4,5)` and `p¹ > 2²`.

*Proof.* `PROOF.md`; formalized in `lean-4/PGS/Placement.lean`.

---

## 3. Phase 2: d=4 first-`τ=4` arrival (proved)

**Theorem 2.1 (First interior `τ=4`).** If `τ(w)=4`, then `w` is the first
interior integer with divisor count `4`.

*Proof.* Apply Lemma 1.2 with `δ=4`: every earlier interior integer has
`τ > 4`, hence `τ ≥ 5`. No earlier `τ=4` exists.

**Theorem 2.2 (No interior prime square).** If `τ(w)=4`, then no interior
integer is a prime square.

*Proof.* Prime square `n=r²` has `τ(n)=3 < 4`. Such an `n` in `I` would
violate Lemma 1.2 if `n < w`, or Lemma 1.3 if `n > w`.

**Remark.** Prime cubes (`τ=4`) are allowed; semiprime-only wording is false
(measured counterexamples exist). The correct class is `τ=4` broadly.

---

## 4. Phase 3: Closure before square threat (proved)

Let `S₊(w)` denote the least prime square strictly greater than `w`.

**Theorem 3.1 (Closure `q ≤ S₊(w)`).** If `τ(w)=4`, then `q ≤ S₊(w)`.

*Proof.* Suppose `q > S₊(w)`. Then `S₊(w) ∈ (w,q) ⊆ I`. Since `S₊(w)` is a
prime square, `τ(S₊(w))=3 < 4=τ(w)`, contradicting Lemma 1.3 on the suffix
after `w`. Therefore `q ≤ S₊(w)`.

**Corollary 3.2 (Square utilization).**

```
U_□(w,q) = (q−w)/(S₊(w)−w) ≤ 1.
```

*Proof.* `q−w ≤ S₊(w)−w` from Theorem 3.1.

**Corollary 3.3 (Right-margin bound).**

```
frac_pos = 1 − (q−w)/g ≤ 1 − (q−w)/(S₊(w)−p)   when g ≤ S₊(w)−p.
```

The tight **right-side** bound is the identity `frac_pos = 1 − m/g` with `m=q−w`.

---

## 5. Phase 4: Left-arrival bound from Short Divisor-Average

Let `r` be the first interior offset with `τ(p+r)=4` (Theorem 2.1: `r = w−p`).
Prefix `J = {p+1,…,p+r−1}` has length `H = r−1` and, by Theorem 2.1,
every `n ∈ J` has `τ(n) ≥ 5`.

**Lemma 4.1 (Short Divisor-Average, `PROOF.md`).** For `N > 1`, `1 ≤ H < N`,
`J = {N−H,…,N−1}`:

```
Σ_{n∈J} τ(n) ≤ H(log N + 2) + 2√N.
```

**Lemma 4.2 (Prefix lower bound).** If every `n ∈ J` has `τ(n) ≥ 5`, then
`Σ_{n∈J} τ(n) ≥ 5H`.

**Proposition 4.3 (No-`τ=4` prefix length).** If prefix `J` of length `H`
after `p` contains no `τ=4` and no `τ=3` integer, then

```
5H ≤ H(log(p+H)+2) + 2√(p+H).
```

*Proof.* Apply Lemma 4.1 at `N=p+H` with Lemma 4.2.

**Definition 4.4 (`R_SDA(p)`).** Let `R_SDA(p)` be the least integer `r ≥ 1`
such that the prefix of length `r−1` satisfies Proposition 4.3, or `r=1` if
the prefix is empty. Then `r ≤ R_SDA(p)` for every d=4 GWR carrier at left
prime `p`.

*Proof.* The first `τ=4` offset `r` cannot exceed the maximal prefix length
that avoids `τ≤4` while satisfying the divisor-average inequality. The
contrapositive of 4.3 forces a `τ≤4` integer no later than offset `R_SDA(p)`.

**Implementation note.** `R_SDA(p)` is computed deterministically by the
analyzer function `max_tau4_free_prefix(p)` (audit only).

---

## 6. Phase 5: Combined bound (proved synthesis)

**Theorem 5.1 (Two-sided d=4 fractional-position bound).** For GWR carrier with
`τ(w)=4` in chamber `(p,q)`:

```
frac_pos = r/g = 1 − m/g,
```

with `r = w−p`, `m = q−w`, `g = q−p`, and:

| Constraint | Bound | Source |
|------------|-------|--------|
| Left arrival | `r ≤ R_SDA(p)` | Phase 4 |
| Right margin | `m = g − r` | identity |
| Gap scale | `g < p` | Bertrand |
| Closure | `m ≤ S₊(w)−w` | Phase 3 |

Hence:

```
frac_pos ≤ min(R_SDA(p)/g, 1 − m/g).
```

**Theorem 5.2 (Explicit upper envelope).** For `m ≥ m₀`:

```
frac_pos ≤ 1 − m₀/g.
```

On the measured `10⁶` d=4 surface, `m₀ = 1` (gap `3,5` has `w=4`, `q−w=1`);
the documented closure ladder reports min margin `2` on the `11-gap-ridge`
surface, regimes differ by left-prime cutoff.

**Theorem 5.3 (No constant `θ₄ < 1` independent of `g`).** If `m = m₀` is
fixed and `g` can be arbitrarily large while `r = g − m₀`, then
`frac_pos → 1`. Such configurations occur when the first `τ=4` integer sits
near the right endpoint. Empirical max `frac_pos = 0.9375` at `10⁶` is
consistent with `m=2`, `g=32`.

*Conclusion for transfer lemma.* The usable bound is **gap-dependent**:

```
frac_pos ≤ min(R_SDA(p)/g, 1 − (q−w)/g),
```

not a single universal `θ₄ = 1/2`.

---

## 7. Finite base

All lemmas above are universal. For implementation audit, the analyzer
verifies zero violations of Theorem 5.1 on explicit regimes `p ≤ 10⁶`.

---

## 8. Lean audit (`lean-4/PGS/Placement.lean`)

| Ladder step | Theorem | Status |
|-------------|---------|--------|
| L1 | `fractionalPosition_identity` | Markdown only (Nat cast friction) |
| L2 | `gwr_d4_prefix_tau_ge_five` | **Proved** |
| L3 | `gwr_d4_first_tau_four` | **Proved** |
| L4 | `gwr_d4_closure_before_square` | **Proved** (suffix + `tau s = 3`) |
| L5 | `gwr_d4_left_arrival_Rp` | Offset form via `gwr_d4_frac_pos_left_arrival` |
| L6 | `gwr_d4_frac_pos_bound` | **Proved** (alias of combined bound) |

Smoke: `lake env lean pgs-rh-placement-invariants.lean`.

---

## 9. Status separation

| Claim | Status |
|-------|--------|
| Theorems 2.1 to 2.2, 3.1, 5.1 | **Proved corollaries of GWR + PROOF.md** |
| `R_SDA(p)` bound | **Proved** given Short Divisor-Average |
| `θ₄ = 1/2` pointwise uniform | **Invalidated** by `frac_pos` max `0.9375` |
| Min margin `m₀` | **Measured** (regime-dependent) |
| Source-to-spectral placement | **Unresolved** |