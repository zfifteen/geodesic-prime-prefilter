# F18-004 Threshold Analysis (Issue #45)

**Date:** 2026-07-25  
**Status:** analysis / measured support (not a theorem promotion)  
**Claim ID:** F18-004 · corpus row RH-103  
**Issue:** [#45](https://github.com/zfifteen/prime-gap-structure/issues/45)

---

## What F18-004 asserts

For consecutive primes `p < q` with nonempty interior, GWR witness `w`, and

```text
C(q) = max(64, ceil(0.5 * (log q)^2))
ratio = (w - p) / C(q)
```

when

```text
ratio >= 0.65  and  q > 10^7  and  w is not a prime square,
```

the prediction is

```text
tau(w) >= max(6, floor(0.75 * log q)).
```

**Logical status today:** tested prediction on a finite exhaustive surface (40M in the pinned campaign). Not in `PROOF.md` as a universal theorem.

---

## Acceptance criteria map (issue #45)

| Criterion | This document / branch |
|-----------|------------------------|
| Proof in `PROOF.md` **or** explicit falsifier | **Neither complete.** No promotion. No falsifier on extended audit surface. |
| Derive or refute conservative floor `0.75 log q` | **Partial derivation:** shows the floor is **not** forced by the Short Divisor-Average `H`-packaging alone; gives a correct **upper** bound on `d` from that packaging; floor remains conservative empirical. |
| FINDINGS RH-103 status | **Stays `measured`** |
| Reproducible audit with LIMIT and thresholds | Hardened script + pinned multi-threshold matrix outputs |

---

## What the proved chain actually forces

Authority: `PROOF.md` (Witness Threshold Lemma, Short Divisor-Average Lemma, Large-Divisor Adjacent Closure).

For non-square `w` with `d = tau(w) >= 4` in the large-divisor regime, the proof packages an interval length

```text
H = floor( w * L / (4*(d-1)) ) ,   L = log w
```

and obtains the offset control

```text
w - p  <=  H.
```

For large `q`, `C(q) ~ (1/2) L_q^2` with `L_q = log q`. If a gap realizes

```text
w - p  >=  r * C(q)  ~  r * (1/2) L_q^2,
```

then necessarily

```text
r * (1/2) L_q^2  <=  H  <=  w * L / (4*(d-1)).
```

Using `w ~ q` and `L ~ L_q` at leading order,

```text
d - 1  <=  w / (2 * r * L_q)   (order-of-magnitude form).
```

### Critical reading

That inequality is an **upper bound on `d`** compatible with a large offset under the `H`-packaging. It does **not** force

```text
d  >=  c * log q.
```

So the F18-004 **lower** floor `max(6, floor(0.75 log q))` is **not** a corollary of the same half-scale packaging that yields `C(q)`. Rough-witness is a **separate** claim about which divisor counts can actually realize near-maximal GWR offsets.

### Why a lower floor is still plausible (heuristic only)

1. **Low-`d` density.** Integers with small `tau` are denser than very rough integers. The leftmost gap minimum tends to appear earlier when low-`d` carriers are available, keeping ratio modest.
2. **Square lane separation.** The only high-ratio case in the 40M surface is a prime square (`tau=3`), governed by Prime-Square Proximity, not by the divisor-average half-coefficient lane.
3. **Champion-above-average intuition.** Late non-square champions must keep the trailing short interval free of smaller `tau`, which is harder unless `d` sits above the short-interval average scale `~ log q`. This is motivation, not a closed estimate with the constant `0.75`.

None of (1)–(3) is promoted to theorem language here.

---

## What would constitute a theorem promotion

A `PROOF.md`-grade statement must do at least one of the following:

1. **Fixed low-`d` theorem (weaker, more realistic first target):**

   ```text
   For non-square w with tau(w) <= 5 and q large enough,
   (w-p)/C(q) < 0.65.
   ```

   This matches the original falsification search (`d <= 5`) and avoids the free constant `0.75`.

2. **Derived `c(r)` curve:** an explicit function `c(r)` such that

   ```text
   ratio >= r  and non-square  =>  tau(w) >= c(r) * log q
   ```

   with a proof from PGS lemmas (or a refutation by counterexample).

3. **Falsifier artifact:** one gap with

   ```text
   ratio >= 0.65, q > 10^7, non-square w, tau(w) < max(6, floor(0.75 log q)).
   ```

Until one of these lands, RH-103 stays **`measured`**.

---

## Empirical matrix (how to read)

The hardened auditor emits a `threshold_matrix` over ratio levels. For each level `r`:

| Field | Meaning |
|-------|---------|
| `non_square_high_ratio` | Non-square cases with ratio `>= r` and `q > q_min` |
| `f18_004_falsifiers` | Non-square cases below the rough floor at that `r` |
| `min_d_non_square_high_ratio` | Smallest `d` among non-square high-ratio cases |
| `legacy_non_square_d_le_5` | Original d`<=5` search class |

**Interpretation rules:**

- `f18_004_falsifiers > 0` at `r = 0.65` **invalidates** the stated F18-004 floors on that regime.
- Empty falsifiers only support **measured survival**, never verified/validated program language without an executed `10^18` surface under AGENTS policy (this claim class is intermediate; keep `measured`).
- If `min_d_non_square_high_ratio` stays large while ratio climbs, the rough-witness shape is consistent; if it drops toward 4–6 at high `r`, the log-floor is too aggressive.

---

## Conservative floor `0.75`: status after this analysis

| Statement | Status |
|-----------|--------|
| `0.75` is forced by Short Divisor-Average packaging | **Refuted as a derivation claim** (packaging gives an upper bound on `d`, not this lower floor) |
| `0.75` is a deliberate loose empirical constant for falsifiability | **Retained** (FINDING_STATEMENT intent) |
| Exact `c(r)` | **Open** |
| Universal rough-witness theorem | **Open** |

---

## Repro commands

Smoke (local, fast):

```bash
python3 research/18-derived-half-coefficient/scripts/near_maximal_witness_audit.py \
  --limit 1000000 \
  --output research/18-derived-half-coefficient/output/near_maximal_audit_results_1M.json
```

Pinned campaign parameters (expensive):

```bash
python3 research/18-derived-half-coefficient/scripts/near_maximal_witness_audit.py \
  --limit 40000000 \
  --ratio-threshold 0.65 \
  --q-min 10000000 \
  --d-log-coeff 0.75 \
  --output research/18-derived-half-coefficient/output/near_maximal_audit_results_40M.json
```

---

## Boundary

- Not RH, not pole placement, not half-scale correspondence (RH-040 remains quarantined).
- Not a downgrade of F18-001 / RH-006 (derived `1/2` in `C(q)` stays proved).
- Square high-ratio cases remain on the Prime-Square Proximity lane.
