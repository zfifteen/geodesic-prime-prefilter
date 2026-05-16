# Mutual Certificate Closure False Positive Analysis

**Step 1 Analysis** — Comparative study of the 50-bit false positive vs the 64-bit true positive under the uniform transported certificate-chain traversal.

**Date of analysis:** Current committed ladder state after the OECC uniform refactor.

---

## 1. Executive Summary

After the uniform certificate-chain refactor, the committed RSA v2 ladder shows three resolutions at the level of public structural endpoint classes:

- **40-bit**: Resolved via reciprocal deadline-signature correction after 0 chain steps → audit `factor_found = true`
- **50-bit**: Resolved via mutual certificate closure after **350** chain steps → audit `factor_found = false`
- **64-bit**: Resolved via mutual certificate closure after **1162** chain steps → audit `factor_found = true`

The 50-bit case is a **clean false positive** under the current mutual certificate closure predicate. The rule walked 350 previous public endpoints, derived certificates, performed reciprocal transport, and eventually found a lower/upper certificate pair whose:

- reset endpoints satisfied mutual floor images under `N`
- reset signatures were identical (`carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail`)

Yet the emitted pair `(32047651, 32059633)` is **not** the actual factor pair `(30729371, 33434981)`.

This is more informative than an unresolved case. It demonstrates that the current mutual closure conditions (mutual floor transport + signature string equality) can be satisfied by a structurally coherent but incorrect endpoint class deep in the lower previous-endpoint chain.

---

## 2. Resolution Context for Both Mutual-Closure Cases

| Property                        | 50-bit (False Positive)     | 64-bit (True Positive)      |
|--------------------------------|-----------------------------|-----------------------------|
| bits                           | 50                          | 64                          |
| N                              | 1027435935526951            | 10376454699372036973        |
| public_closure_status          | mutual certificate closure  | mutual certificate closure  |
| endpoint_chain_steps           | **350**                     | **1162**                    |
| chain position at resolution   | Deep walk                   | Much deeper walk            |
| carrier_d (lower + upper)      | 4 + 4                       | 4 + 4                       |
| lock_carrier_d (lower + upper) | 4 + 4                       | 4 + 4                       |
| threat (both sides)            | False                       | False                       |
| deadline source (signature)    | tail                        | tail                        |
| resolved via                   | corrected pair (deadline-signature path inside chain) | corrected pair |

Both cases required substantial chain walking before mutual certificate closure succeeded. The 64-bit case walked more than 3× as far as the 50-bit case before locking.

---

## 3. Certificate Profile Comparison (Lower Side)

Both lower certificates are d=4 carriers (semiprime squares or products of two close primes inside the gap).

**Lower Certificate Fields**

| Field                              | 50-bit False             | 64-bit True              | Observation |
|------------------------------------|--------------------------|--------------------------|-----------|
| lower_anchor                       | 32047627                 | 3221225461               | — |
| lower_gap_offset                   | **24**                   | **12**                   | 50-bit lower gap is twice as wide |
| lower_lock_carrier_offset          | **6**                    | **10**                   | Lock sits earlier in 50-bit gap |
| lower_carrier_w                    | 32047633                 | 3221225471               | Both extremely close to anchor |
| lower_reset_endpoint               | 32047651                 | 3221225473               | — |
| lower_reset_deadline_margin        | **12**                   | **6**                    | 50-bit margin = 2× 64-bit |
| lower_transported_deadline_width   | **12**                   | **7**                    | After transport, 50-bit has larger effective width |
| lower_tail_after_reset_offsets     | [36,40,54,94,100,112]    | [18,72,88,90,100,102]    | Different structure |
| lower_unresolved_count             | 6                        | 6                        | Identical |
| lower_resolved_count               | 1                        | 1                        | Identical |
| lower_closed_offsets_before_q len  | 27                       | 26                       | Very similar |

**Key PGS-native observations on lower side:**

- The 50-bit lower gap is materially wider (gap_offset 24 vs 12). This means the selected d=4 carrier sits farther from its left prime than in the 64-bit case.
- The lock_carrier_offset is earlier in the 50-bit case (6 vs 10). The "locked" d=4 carrier is relatively closer to the left of its local gap.
- The deadline margin is twice as large on the 50-bit lower certificate (12 vs 6). After transport, this asymmetry becomes even more pronounced (upper margin 46 vs 30).

---

## 4. Certificate Profile Comparison (Upper Side)

| Field                              | 50-bit False             | 64-bit True              | Observation |
|------------------------------------|--------------------------|--------------------------|-----------|
| upper_anchor                       | 32059619                 | 3221275487               | — |
| upper_gap_offset                   | 14                       | 14                       | Identical |
| upper_lock_carrier_offset          | 2                        | 2                        | Identical (very early lock) |
| upper_reset_deadline_margin        | **46**                   | **30**                   | 50-bit upper margin significantly larger |
| upper_transported_deadline_width   | **46**                   | **30**                   | Matches the margin (no correction on upper) |
| upper_tail_after_reset_offsets     | [60,74,98,102,114,128]   | [44,72,86,92,104,110]    | Different distribution |
| upper_unresolved_count             | 6                        | 6                        | Identical |

The upper-side gaps are structurally similar in width, but the **deadline margin asymmetry** between lower and upper is more extreme in the 50-bit false positive (12 vs 46) than in the 64-bit true positive (6 vs 30).

---

## 5. What the Current Mutual Closure Predicate Actually Verified

From the uniform implementation in `certificate_chain_state_closure`:

For a pair (L, U) to be accepted as mutual certificate closure, the code requires:

1. `transported_upper == upper.reset_endpoint`
2. `transported_lower == lower.reset_endpoint`
3. `lower.reset_signature == upper.reset_signature`

The signature in both the 50-bit and 64-bit cases was exactly:

```
carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail
```

Because both sides were d=4 carriers with no active threat and the deadline taken from the first tail offset, the signatures matched. Combined with the mutual floor condition on the (eventually corrected) endpoints, the pair was emitted.

**No other certificate-internal property was consulted.**

---

## 6. Most Salient PGS-Native Differences

The following differences stand out as potentially exploitable for a tighter predicate:

1. **Deadline margin asymmetry (lower vs upper after transport)**
   - 50-bit: lower margin 12, upper margin 46 (ratio ~1:3.83)
   - 64-bit: lower margin 6, upper margin 30 (ratio 1:5)
   - The false positive has a less extreme ratio. This may be noise, or it may indicate something about how "tight" the reciprocal deadline relationship is.

2. **Lower gap_offset relative to lock position**
   - 50-bit lower: gap_offset 24, lock at offset 6 (lock is 25% into the gap)
   - 64-bit lower: gap_offset 12, lock at offset 10 (lock is ~83% into the gap)
   - In the true positive, the locked d=4 carrier sits much closer to the right end of its local gap.

3. **Lower transported deadline width vs upper**
   - In the false positive, the lower transported deadline width (12) is much smaller than the upper (46).
   - In the true positive, the ratio is 7 vs 30 — still asymmetric, but the absolute values and the chain depth at which closure occurred may matter.

4. **Chain depth at closure (350 vs 1162 steps)**
   - The true positive required walking more than three times as many previous endpoints. This is consistent with the idea that deeper in the chain, the reciprocal structure becomes more constrained.

5. **Tail structure after the chosen deadline**
   - Both tails have 6 entries, but the spacing after the first tail offset (the chosen deadline) differs noticeably.

---

## 7. Implications for Refinement

The current mutual certificate closure predicate is too permissive because it only checks:

- Mutual floor transport of the reset endpoints (or corrected endpoints)
- Exact string equality of the reset signatures

It does **not** yet look at:
- The relationship between lower and upper deadline margins after transport
- The position of the locked carrier inside its local gap (lock_carrier_offset relative to gap_offset)
- Any property of how the tail intervals themselves transport under `floor(N / ·)`
- The number of steps required to reach closure (depth in the previous-endpoint chain)

The 50-bit false positive demonstrates that a d=4 carrier on the lower side, when transported, can find a matching d=4 carrier on the upper side with an identical signature string, even when the pair is not the true factor pair.

Any next refinement must add at least one additional PGS-native condition that the 50-bit pair fails while the 64-bit pair passes, without introducing scale-specific logic.

---

## 8. Recommended Next Analytical Steps (Step 2)

Before proposing a concrete new predicate, the following targeted extractions would be high value:

- Full tail transport comparison: compute `floor(N / t)` for every tail offset on the lower certificate and compare the resulting structure on the upper side for both cases.
- Lock carrier transport behavior: examine where `carrier_w` (the actual locked d=4 integer) lands after transport in both the false and true cases.
- Deadline margin ratio as a function of chain depth across more rungs (if additional ladder cases become available).
- Whether the "unresolved_count = 6" on both sides of the false positive is coincidental or diagnostic.

Once those are mapped, candidate predicates can be written as pure relational tests on the already-computed certificate fields (no new divisor counting required inside the closure check).

---

**Document status:** This is Step 1 comparative analysis only. It does not yet propose a new closure rule. It is intended to ground any subsequent refinement in the actual certificate data of the current false positive.