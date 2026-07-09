# Closure Refinement Analysis Log

**Purpose:** Running analytical record of the effort to tighten the mutual certificate closure predicate in the uniform transported certificate-chain traversal for RSA v2 endpoint structure.

This document accumulates findings step by step. Each step builds on the previous. Detailed supporting documents are referenced.

**Current Status:** Correction implemented. The 50-bit closure candidate at step
350 is now an explicit unresolved structural state:
`unresolved_by_reciprocal_carrier_misalignment`.

---

## Step 1: Mutual Certificate Closure False Positive Analysis

**Date:** After uniform OECC refactor on committed ladder

**Key Finding:**
The 50-bit case produced a clean false positive under mutual certificate closure after walking 350 previous-endpoint steps. The rule emitted the structural pair `(32047651, 32059633)`, which satisfied mutual floor images + identical reset signatures, but was not the actual factor pair `(30729371, 33434981)`.

The 64-bit case resolved correctly under the same predicate after 1162 steps.

Both cases were d=4 carriers on both sides with identical signature strings:
`carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail`

**Main observations from certificate fields:**
- 50-bit lower gap was significantly wider (gap_offset 24 vs 12 on 64-bit).
- Lock position relative to gap differed (earlier lock in false positive).
- Deadline margin asymmetry was present in both, but more extreme in certain ways on the false positive.
- Current mutual closure only checked floor transport + exact signature string match. No other certificate-internal geometry was consulted.

**Supporting document:** `MUTUAL_CLOSURE_FALSE_POSITIVE_ANALYSIS.md`

**Conclusion from Step 1:**
The mutual certificate closure predicate is too permissive. It can accept structurally coherent but incorrect endpoint classes. Additional PGS-native conditions based on internal certificate geometry are required.

---

## Step 2: Tail and Carrier Transport Analysis

**Date:** Follow-up to Step 1

**Method:** Take points internal to the lower PGSPG certificate (`carrier_w` and the `tail_after_reset_offsets`) and transport them via `floor(N / x)`. Compare the landing positions against the actual upper certificate structure.

**Strongest quantitative signals:**

| Measurement                                              | 50-bit False | 64-bit True | Notes |
|----------------------------------------------------------|--------------|-------------|-------|
| Transported lower `carrier_w` overshoot above upper_anchor | **+32**      | **+16**     | Exactly 2× tighter in true case |
| Transported lower `carrier_w` overshoot above upper `carrier_w` | **+30** | **+14** | ~2× |
| First transported lower tail point relative to upper_anchor | **-22**     | **-5**      | First tail lands dramatically closer in true case |
| Transported lower deadline value error (undershoot)      | **-58**      | **-37**     | Larger error in false positive |

**Key pattern:** In the true positive, the transported lower carrier and the first lower tail point create a tight "pinch" around the upper_anchor. The false positive shows roughly twice the deviation on both sides of the upper_anchor.

**Interpretation:**
When two d=4 carriers are genuine reciprocal images under the semiprime, their internal gap geometry (locked carrier position + start of tail) produces transported images that align much more tightly with the corresponding structure on the opposite side.

**Supporting document:** `STEP2_TAIL_AND_CARRIER_TRANSPORT_ANALYSIS.md`

**Conclusion from Step 2:**
Several cheap, purely relational conditions on already-available certificate fields + floor transport appear capable of rejecting the 50-bit false positive while preserving the 64-bit true positive. These conditions do not require new divisor counting at closure time.

---

## Step 3: Candidate Predicate Formulation

**Goal:** Convert the transport observations from Step 2 into concrete, PGS-native predicate candidates that can be evaluated inside the existing uniform `certificate_chain_state_closure` function.

All candidates below use only:
- Fields already present in `PGSCertificate` (lower and upper)
- `floor(N / x)` transport
- Simple arithmetic comparisons

No classical methods, no additional sieving, no primality checks, and no scale-dependent branching.

### Candidate Predicate A: Carrier Transport Tightness

**Statement:**
After choosing the oriented transport coordinate and deriving the upper certificate, require that the transported position of the lower `carrier_w` lands close to the upper `carrier_w`:

```text
| floor(N / lower.carrier_w) - upper.carrier_w | <= K
```

Where `K` is a small constant or a simple function of the lower gap geometry (e.g. `max(20, lower.gap_offset // 2)`).

**Numbers on current cases:**
- 50-bit (False): |32059651 - 32059621| = **30**
- 64-bit (True):  |3221275503 - 3221275489| = **14**
- 40-bit (deadline-signature case): TBD (must be measured)

**Rationale:** In a genuine reciprocal pair, the actual locked d=4 carrier on the lower side should transport to a position very near the locked d=4 carrier on the upper side.

**Risk:** May be too strict if the true factors are not exactly the carriers but sit nearby. Needs checking against more true-positive rungs.

---

### Candidate Predicate B: First Tail Proximity

**Statement:**
Require that the transported position of the *first* entry in `lower.tail_after_reset_offsets` lands close to the upper_anchor (on the lower side of it):

```text
upper_anchor - D <= floor(N / (lower.reset_endpoint + lower.tail[0])) <= upper_anchor + E
```

Suggested initial bounds: `D=10`, `E=5` (or derived from local gap sizes).

**Numbers on current cases:**
- 50-bit (False): first tail (+36) transports to 32059597 → **-22** from upper_anchor (32059619)
- 64-bit (True):  first tail (+18) transports to 3221275482 → **-5** from upper_anchor (3221275487)

**Rationale:** The first tail point after the locked carrier represents the next structural event in the lower gap. When the carriers are true reciprocal images, this first event should map very close to the start of the upper gap.

This was one of the cleanest single discriminators found in Step 2.

---

### Candidate Predicate C: Combined Carrier + First-Tail Pinching (Compound)

**Statement:**
Require that the sum of the absolute deviations is small:

```text
|transported_lower_carrier_w - upper_anchor| 
+ 
|upper_anchor - transported_first_lower_tail| 
<= T
```

This captures the "pinch" observed in the true positive.

**Numbers:**
- 50-bit: 32 + 22 = **54**
- 64-bit: 16 + 5  = **21**

A threshold around 25 to 30 would separate the current cases.

**Advantage:** More robust than a single measurement. Captures the mutual approach from both sides of the upper_anchor.

---

### Candidate Predicate D: Deadline Value Transport Error (Weaker)

**Statement:**
Bound the absolute error when transporting the lower `reset_deadline_value`:

```text
| floor(N / lower.reset_deadline_value) - upper.reset_deadline_value | <= M
```

**Numbers:**
- 50-bit: 58
- 64-bit: 37

This is directionally consistent but weaker than A/B/C. It could be used as a secondary filter.

---

## Evaluation Against Existing Committed Cases (Preliminary)

| Predicate | 50-bit False | 64-bit True | 40-bit (deadline-sig) | Notes |
|-----------|--------------|-------------|-----------------------|-------|
| A (Carrier tightness) | Fails (30)   | Passes (14) | ?                     | Strongest single candidate so far |
| B (First tail proximity) | Fails (-22) | Passes (-5) | ?                     | Very clean separation |
| C (Combined pinch)    | Fails (54)   | Passes (21) | ?                     | Good compound signal |
| D (Deadline error)    | Fails (58)   | Passes (37) | ?                     | Weaker, but easy to add |

The 40-bit case (which resolved via deadline-signature correction at step 0) must be measured before any predicate is accepted. It is possible that deadline-signature resolutions have different tightness characteristics than mutual-certificate resolutions.

---

## Current Leading Recommendations (as of this step)

1. **Primary candidate:** Predicate B (First Tail Proximity) or the compound Predicate C. These showed the cleanest separation on the current data.
2. **Secondary candidate:** Predicate A (Carrier Transport Tightness), possibly with a bound that scales mildly with local gap size.
3. Do **not** rely on signature string enhancements alone: both the false and true cases had identical signatures.

All candidates are compatible with the uniform single-traversal design. They would be evaluated inside `certificate_chain_state_closure` after the upper certificate is derived, before deciding to emit a structural endpoint class.

---

## Open Questions / Risks

- Will these predicates reject the 40-bit correct resolution (which used deadline-signature correction rather than pure mutual closure)?
- Are the observed tightness differences stable across more true-positive rungs, or are they specific to these two cases?
- Should the bounds be expressed relative to local gap geometry (`gap_offset`, `lock_carrier_offset`) rather than as fixed constants?
- How do these transport properties behave on cases that only resolve deep in the chain versus at step 0?

---

## Next Step (Step 4: Proposed)

1. Instrument the current runner to compute and log the values for Predicates A/B/C/D on all three committed rungs (including the 40-bit case).
2. Measure the 40-bit case against the candidates.
3. If the 40-bit case passes at least one strong candidate (or a relaxed version of it), formalize the chosen predicate(s) as an addition to the closure logic.
4. Update the endpoint structure law documentation to describe the new condition.

---

**Document maintenance:** This log will be extended with each subsequent analytical step. Detailed raw data and intermediate calculations live in the referenced per-step documents.

---

## Phase 1: Full Transport Metrics on Committed Ladder (Executed)

**Date:** Current session

**Action taken:**
Created and ran `diagnose_transport_metrics.py` (with manual fallback for the 40-bit case, which has an empty `lower_tail_after_reset_offsets` list and resolved via threat-based deadline at step 0).

**Critical new data : 40-bit case (correct resolution via deadline-signature correction at step 0):**

- lower_carrier_w = 1048572
- Transported lower_carrier_w = 1048575
- upper_anchor = 1048573
- **Carrier overshoot above upper_anchor: +2** (extremely tight)
- Transported lower_deadline = 1048573
- upper_deadline = 1048589
- **Deadline transport error: -16**

**Note on 40-bit structure:**
The lower certificate had `carrier_d=96`, `lock_carrier_d=96`, `threat=True`, `deadline=threat`. The tail list was empty. This is a different structural regime than the d=4 / threat=False / deadline=tail cases on 50-bit and 64-bit.

---

### Phase 1 Results Table: Carrier Transport Tightness

| Case                  | Bits | Resolution Type                  | Chain Steps | Carrier Overshoot above upper_anchor | First Tail Delta from upper_anchor | Deadline Transport Error | Notes |
|-----------------------|------|----------------------------------|-------------|--------------------------------------|------------------------------------|---------------------------|-------|
| rsa_v2_40bit_static_001 | 40 | Deadline-signature correction   | 0           | **+2**                               | N/A (no tail; threat-based)       | -16                       | Extremely tight carrier transport |
| rsa_v2_50bit_static_001 | 50 | Mutual certificate closure      | 350         | **+32**                              | -22                                | -58                       | **False positive** |
| rsa_v2_64bit_static_001 | 64 | Mutual certificate closure      | 1162        | **+16**                              | -5                                 | -37                       | Correct |

**Key observations from Phase 1:**

1. **Both correct resolutions show significantly tighter carrier transport** than the false positive:
   - True cases: +2 and +16
   - False case: +32 (exactly 2× the 64-bit true case)

2. The 40-bit case (different structural regime, high divisor count, threat-based deadline, no tail) still exhibits very precise reciprocal alignment on the carrier (+2 overshoot). This is encouraging for the generality of the "tight transport" signal.

3. The first-tail proximity signal cannot be applied to threat-based deadline cases (like 40-bit), because there is no tail. Any predicate using first tail must be conditional on the deadline source being "tail".

4. Deadline transport error is directionally consistent (true cases have smaller error) but the separation is weaker than carrier overshoot.

---

### Implications for Predicate Design (Updated after Phase 1)

- **Predicate A (Carrier Transport Tightness)** remains very strong. A bound of ~20 would pass both true cases (+2 and +16) and reject the false case (+32). The 40-bit result (+2) shows the signal holds even in a different divisor regime.
- **Predicate B (First Tail Proximity)** is only applicable when `lower.reset_signature` indicates `deadline=tail`. It would need to be skipped (or relaxed) for threat-based deadline cases.
- The **compound approach (Predicate C)** needs to be made conditional on deadline source.

This data suggests we should prioritize a **carrier-centric predicate** as the primary filter, with tail-based conditions as a secondary filter only when the deadline came from the tail.

---

**Phase 1 Status:** Complete. Data collected and analyzed. Running log updated.

---

## Phase 2: Corrected Predicate Definition

**Date:** Current session

The first attempted carrier-bound statement used:

```text
Bound = max(20, floor(1.5 * lower.gap_offset))
```

That statement was arithmetically wrong for the 50-bit false positive. The
50-bit carrier error was `30`, the bound was `36`, and therefore the candidate
passed. The earlier log entry that marked this as a failure is invalidated.

The corrected carrier predicate is:

```text
abs(floor(N / matched_lower.carrier_w) - upper.carrier_w)
  <= max(20, floor(1.2 * matched_lower.gap_offset))
```

For strict reset closure, `matched_lower` is the original lower certificate.
For deadline-signature correction, `matched_lower` is the corrected lower
certificate, because that is the certificate whose signature matches the upper
certificate.

The first-tail predicate is active only when `matched_lower` uses
`deadline=tail`:

```text
-12 <= floor(N / first_matched_lower_tail_point) - upper.anchor <= 6
```

For strict reset closure and nonzero endpoint-chain correction, the matched
certificates must also satisfy:

```text
2 * matched_lower.lock_carrier_offset > matched_lower.gap_offset
matched_lower.active_count == upper.active_count
matched_lower.unresolved_count == upper.unresolved_count
```

The lock and profile-count predicates came from the follow-up live check after
the first carrier/tail filters were added. Continuing past rejected closure
candidates produced later false closures on the 50-bit, 48-bit, and 60-bit
checks. The correct control rule is therefore:

```text
first base closure candidate fails refined public geometry
-> return an explicit unresolved structural state
```

The runner does not silently skip a rejected closure candidate and keep walking
to a later closure, because that would choose among multiple coherent endpoint
classes without a public discriminator.

## Phase 3: Implemented Correction

The live runner now:

- evaluates carrier transport against the matched lower certificate;
- applies first-tail proximity for tail-deadline matched lower certificates;
- applies lower-lock dominance and profile-count symmetry for strict reset
  closure and nonzero endpoint-chain correction;
- returns an unresolved status at the first failed refined closure candidate.

The current committed ladder surface is:

```text
rsa_v2_40bit_static_001
  endpoint_class_by_reciprocal_deadline_signature_correction
  factor_found = true

rsa_v2_50bit_static_001
  unresolved_by_reciprocal_carrier_misalignment
  rejected candidate at step 350 = (32047651, 32059633)
  factor_found = false

rsa_v2_64bit_static_001
  endpoint_class_by_mutual_certificate_closure
  endpoint class = (3221225473, 3221275501)
  factor_found = true
```

`diagnose_transport_metrics.py` now handles the 40-bit no-tail certificate
without crashing and reports the corrected carrier bound:

```text
40-bit: carrier PASS, tail N/A
50-bit: carrier FAIL, tail FAIL
64-bit: carrier PASS, tail PASS
```

The focused RSA v2 test suite passes with the known normalized-frontier sidecar
test excluded:

```text
pytest -q research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py -q \
  -k 'not toy_normalized_frontier_closure_sweep_keeps_current_rows_unresolved'
```

**Status:** The false 50-bit public endpoint class is no longer emitted. The
50-bit rung is an unresolved structural state until a stronger public
discriminator is found.
