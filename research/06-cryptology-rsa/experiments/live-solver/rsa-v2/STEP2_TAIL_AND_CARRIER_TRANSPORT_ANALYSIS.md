# Step 2: Tail and Carrier Transport Analysis

**Focus:** Reciprocal transport behavior of lower certificate internal points (carrier_w and tail offsets) compared against the actual upper certificate structure.

This analysis uses only the already-computed fields from the PGSPG certificates + pure `floor(N / ·)` transport. No new divisor counting is performed.

---

## 1. Summary of Transport Observations

When we take points that exist inside the lower certificate (the locked carrier `carrier_w` and the tail points after the reset endpoint) and transport them through `floor(N / x)`, we observe consistent differences between the false positive and the true positive.

### 1.1 Transported Lower `carrier_w` relative to Upper Structure

| Case              | lower_carrier_w | Transported lower_carrier_w | upper_anchor | upper_carrier_w | Overshoot above upper_anchor | Overshoot above upper_carrier_w |
|-------------------|-----------------|-------------------------------|--------------|-----------------|-------------------------------|---------------------------------|
| **50-bit False**  | 32047633        | 32059651                      | 32059619     | 32059621        | **+32**                       | **+30**                         |
| **64-bit True**   | 3221225471      | 3221275503                    | 3221275487   | 3221275489      | **+16**                       | **+14**                         |

**Observation:** In the true positive, the transported position of the lower locked carrier lands only 16 above the upper_anchor and 14 above the actual upper_carrier_w. In the false positive, it overshoots by exactly twice as much (+32 / +30).

---

### 1.2 First Transported Lower Tail Point relative to Upper Anchor

| Case              | First lower tail offset | First lower tail point | Transported position | Delta from upper_anchor |
|-------------------|---------------------------|------------------------|----------------------|---------------------------|
| **50-bit False**  | +36                       | 32047687               | 32059597             | **-22**                   |
| **64-bit True**   | +18                       | 3221225491             | 3221275482           | **-5**                    |

**Observation:** The first transported point from the lower tail lands dramatically closer to the upper_anchor in the true positive (-5) than in the false positive (-22). This is one of the sharpest single-number differences found so far.

---

### 1.3 Transported Lower Deadline Value

| Case              | lower_reset_deadline_value | Transported lower deadline | upper_reset_deadline_value | Delta (trans - upper) |
|-------------------|----------------------------|------------------------------|------------------------------|-----------------------|
| **50-bit False**  | 32047663                   | 32059621                     | 32059679                     | **-58**               |
| **64-bit True**   | 3221225479                 | 3221275494                   | 3221275531                   | **-37**               |

Both cases undershoot the actual upper deadline when the lower deadline is transported. The false positive undershoots by a larger absolute amount.

---

## 2. Full Lower Tail Transport vs Upper Tail Structure

When every point in the lower `tail_after_reset_offsets` is transported, none of them land inside the upper gap or on the upper reset endpoint in either case. However, the *pattern* of their landing positions relative to the upper structure differs.

### 50-bit False Positive — Transported Lower Tails

Upper gap on this modulus: `[32059619 ... 32059633]`

| Lower tail offset | Lower tail point | Transported | Distance to nearest upper structure | Position relative to upper gap |
|-------------------|------------------|-------------|-------------------------------------|--------------------------------|
| +36               | 32047687         | 32059597    | -22 from upper_anchor               | 22 before gap                  |
| +40               | 32047691         | 32059593    | -26 from upper_anchor               | 26 before gap                  |
| +54               | 32047705         | 32059579    | -40 from upper_anchor               | 40 before gap                  |
| +94               | 32047745         | 32059539    | -80 from upper_anchor               | Deep before gap                |
| +100              | 32047751         | 32059533    | -86 from upper_anchor               | Deep before gap                |
| +112              | 32047763         | 32059521    | -98 from upper_anchor               | Deep before gap                |

### 64-bit True Positive — Transported Lower Tails

Upper gap on this modulus: `[3221275487 ... 3221275501]`

| Lower tail offset | Lower tail point | Transported | Distance to nearest upper structure | Position relative to upper gap |
|-------------------|------------------|-------------|-------------------------------------|--------------------------------|
| +18               | 3221225491       | 3221275482  | **-5** from upper_anchor            | 5 before gap                   |
| +72               | 3221225545       | 3221275428  | -59 from upper_anchor               | 59 before gap                  |
| +88               | 3221225561       | 3221275412  | -75 from upper_anchor               | 75 before gap                  |
| +90               | 3221225563       | 3221275410  | -77 from upper_anchor               | 77 before gap                  |
| +100              | 3221225573       | 3221275400  | -87 from upper_anchor               | 87 before gap                  |
| +102              | 3221225575       | 3221275398  | -89 from upper_anchor               | 89 before gap                  |

**Strong signal:** In the true positive, the *very first* transported lower tail point lands only 5 before the upper_anchor. In the false positive, the closest any transported lower tail gets is 22 before the upper_anchor.

---

## 3. Interpretation in PGS Terms

These transport results suggest that the true positive exhibits a tighter **reciprocal alignment** between the internal structure of the lower gap (particularly the position of the locked d=4 carrier and the beginning of its tail) and the upper gap structure.

In the 64-bit true positive:

- The lower locked carrier (`carrier_w`), when transported, lands only 16 past the upper_anchor (and 14 past the actual upper locked carrier).
- The first point in the lower tail, when transported, lands only 5 before the upper_anchor — extremely close to the start of the upper gap.

In the 50-bit false positive, these alignments are roughly twice as loose (32/30 overshoot on the carrier, 22 undershoot on the first tail point).

This is consistent with the idea that when two d=4 carriers are genuine reciprocal images of each other under the semiprime (i.e., they are the actual factor endpoints or very close to them), their internal gap structures (lock position + tail) will exhibit a tighter "mirror" relationship under floor transport than when the pair is a spurious structural match.

---

## 4. Candidate Directions for a Tighter Predicate

Based on this transport analysis, the following PGS-native conditions appear worth testing on the next set of rungs:

**A. Carrier transport tightness**
- Require that the transported lower `carrier_w` lands within a bounded distance of the upper `carrier_w` (or upper_anchor), e.g. `|transported_lower_carrier_w - upper_carrier_w| <= 20` (or some function of local gap size).
- The 64-bit case satisfies a bound of ~14–16. The 50-bit case violates it at 30.

**B. First tail point proximity to upper_anchor**
- Require that the transported position of the *first* lower tail offset lands within a small distance of the upper_anchor (e.g. within 10 on the lower side).
- The 64-bit case lands at -5. The 50-bit case lands at -22.

**C. Combined carrier + first-tail alignment**
- A compound condition: the transported lower carrier overshoots the upper_anchor by roughly the same magnitude that the first transported tail undershoots it, and both deltas are small.
- This would capture the "pinching" behavior visible in the true positive around the upper_anchor.

**D. Deadline value transport error**
- Bound the absolute error when transporting the lower `reset_deadline_value` against the actual upper `reset_deadline_value`.
- Both cases undershoot, but the true positive undershoots by less (-37 vs -58).

Any of these can be evaluated using only values already present in the two certificates plus `floor(N / ·)` — they require no additional divisor counting inside the closure check.

---

## 5. Next Recommended Actions

Before codifying any of the above into a new predicate, the following would strengthen the analysis:

1. Apply the same transport measurements to the **40-bit** case (which resolved via deadline-signature correction at step 0) to ensure any new condition does not break the already-committed correct resolution.
2. Check whether the "first transported tail close to upper_anchor" property holds on additional known true-positive rungs (if any exist beyond the current three).
3. Examine whether the *ratio* of lower_gap_offset to the lock_carrier_offset (24:6 vs 12:10) survives transport in a meaningful way.

These measurements are cheap and stay entirely within the existing PGSPG certificate data.

---

**Document status:** Step 2 transport analysis. Purely observational. No new rule is proposed yet. All calculations use only existing certificate fields + reciprocal floor. This document is intended to make the next predicate proposal evidence-based rather than speculative.