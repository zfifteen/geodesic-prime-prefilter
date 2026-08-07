# Plan: Add the 128-bit Rung under the Resolved Residual Ladder

**Date:** 2026-08-07  
**Status:** Planning document (adversarial review applied)  
**Location:** research/06-cryptology-rsa/docs/

---

The current resolved ladder covers the 40-bit, 50-bit, and 64-bit rungs under one reciprocal rule (V3 carrier reciprocal closure for the 50-bit case). The 128-bit case already exists in `ladder_spec.json` as `rsa_v2_128bit_static_001`. It returns `unresolved_by_missing_lower_certificate`. The runner already carries coordinates as `gmpy2.mpz`. The exact divisor-count interval backend remains small-regime.

The work has two linked goals:

1. Make the arithmetic layer support anchors and chambers at 128-bit scale.
2. Bring the 128-bit rung under the same measured V3 framing used for the lower rungs.

---

## 1. Current Arithmetic Boundary

- Public coordinates (`N`, `isqrt(N)`, endpoints, floors, deadlines) use `gmpy2.mpz`.
- The interval-measurement helper converts those values to Python `int`.
- The helper itself is limited to the small-regime range.
- The C high-scale path (`src/c/high-scale-pgs`) exists but does not yet return complete lower certificates for anchors near 2^64 and above.
- `ARITHMETIC.md` states the required future surface: lower PGSPG certificate → reciprocal transport → upper PGSPG certificate → reciprocal certificate closure.

Any change must keep this surface. Do not introduce per-rung branches.

---

## 2. Required Capabilities for 128-bit

- Exact integer arithmetic on numbers up to at least 2^128 (and temporary intermediates larger than that).
- Integer square-root of a 128-bit modulus.
- Floor division `N // x` for 64-bit to 128-bit values.
- Contiguous divisor-count segments around anchors near 2^64.
- Chamber-reset state extraction (carrier, lock, threat, deadline, tail offsets) at those anchors.
- Batch-friendly measurement of previous-endpoint chunks.
- Stable conversion between `gmpy2.mpz` and any backend representation.
- Memory use that stays practical on a single machine for chain lengths observed on the 64-bit rung.

---

## 3. Arithmetic Library Options and Boundary Contract

**Option A – Full gmpy2 path**  
Keep all coordinates and interval work inside `gmpy2.mpz`.  
Risk: pure-Python loops over large segments become slow.

**Option B – Hybrid with C GMP (recommended)**  
Use the existing high-scale C library for all chamber and divisor-count work.  
Python receives only the final certificate or an unresolved status.  
Dense phase-space traversal stays inside C memory.

**Option C – Pure Python arbitrary integers**  
Use built-in Python `int` for everything.  
Risk: too slow for dense segment scans at 64-bit scale.

**Strict boundary contract**  
- The entire phase-space traversal loop runs in C.  
- Intermediate chamber states never cross the language boundary.  
- Python acts only as orchestrator.  
- Only the finalized certificate (or an unresolved code) returns to Python.

---

## 4. Technical Considerations (Adversarial Constraints)

**Correctness**
- Every nontrivial arithmetic step must keep a plain-language comment (see `ARITHMETIC.md`).
- Preserve the exact certificate-pair surface.
- Do not introduce `gcd`, `%`, primality tests, or product checks inside the inference path.
- Regression tests on the three resolved rungs must stay green.

**Performance and serialization**
- Dense evaluation stays inside C.  
- The ctypes bridge is used only for the final result.  
- Measure cost per chamber certificate at anchors near 2^64.  
- Record time and memory for previous-endpoint discovery by contiguous chunks.

**Memory and tail offsets**
- Derive a fixed upper bound on tail-offset capacity from the measured V3 surface on the 40/50/64-bit rungs.  
- Allocate the tail array once inside the C certificate struct.  
- Copy only the used portion when the final certificate returns to Python.  
- If the measured bound is exceeded, emit an explicit unresolved status. Do not truncate or stream.

**Intermediate overflow near 2^64**
- All internal C calculations that can produce values larger than 2^64 must use `mpz_t`.  
- Native 64-bit registers are forbidden for intermediate values near the anchor boundary.  
- Add explicit overflow tests in the C test suite for anchors in the range [2^63, 2^65].

**Theoretical purity versus computational budget**
- Classical pre-filters remain forbidden.  
- The pure reciprocal rules must constrain the candidate set.  
- If the projected candidate set exceeds a documented computational budget, the status is `unresolved_by_computational_budget`.  
- Do not mask the failure with classical filters.

**API stability**
- The backend selection (`get_backend_for_anchor`) already routes on size. Extend it without adding bit-length special cases in the solver logic.  
- Keep public inference free of audit factors.

**Integration points**
- `pgs_inference_backend.py`
- `run_experiment.py`
- `src/c/high-scale-pgs` (certificate population, especially `tail_after_reset_offsets` and lower-threat fields)
- Fixture builders in `data-ladder/rsa-v2`
- Diagnostic scripts (`diagnose_transport_metrics.py`)

**Documentation and continuity**
- Update `ARITHMETIC.md` with the new boundary.  
- Update `SESSION_BOOTSTRAP.md` and the resolved-ladder note after the first measured 128-bit result.  
- Keep the public-versus-audit separation strict.  
- Record any new unresolved predicate in the same style as the existing ones.

---

## 5. Phased Work Plan

**Phase 0 – Inventory (no logic change)**  
- Confirm the C high-scale library builds and loads.  
- Run existing cost probes on a 64-bit and a 128-bit anchor.  
- Document current missing fields in the high-scale certificate dict.  
- List every call site that converts `mpz` to Python `int`.

**Phase 1 – Scaffolding**  
- Add comments that describe the 128-bit path and the required certificate fields.  
- Extend tests with placeholder cases that assert “not yet ready”.  
- Update the ladder fixtures only if provenance is already clean.  
- No change to inference results.

**Phase 2 – Harden the C arithmetic core**  
- Build the `mpz_t` overflow test suite for anchors in [2^63, 2^65].  
- Enforce `mpz_t` for all intermediate calculations near the 64-bit boundary.  
- Complete population of the final certificate struct (carrier, lock, threat, deadline, bounded tail).  
- Keep the dense traversal loop entirely inside C.  
- Return only the final certificate or an unresolved code to Python.  
- Add instrumentation (call count, time, anchor size).

**Phase 3 – Interval backend maturity**  
- Route 128-bit anchors through the completed high-scale path.  
- Keep the small-regime path for the lower rungs.  
- Add batch previous-endpoint measurement that stays inside C.  
- Run the 128-bit case end-to-end and capture the public status.

**Phase 4 – Measurement and documentation**  
- Compare transport metrics against the 40/50/64-bit resolved cases.  
- Record the exact public closure status (resolved under V3 framing or a new unresolved predicate).  
- Update continuity documents and the resolved-ladder note.  
- Confirm all focused tests remain green.

---

## 6. Risks and Guards

- Do not declare the 128-bit rung resolved until audit confirms the endpoint class.  
- Do not weaken the public-inference contract.  
- Do not optimize only for the curated 128-bit case and break the lower rungs.  
- If the chamber cost is too high, emit an explicit unresolved status rather than a silent timeout.  
- Keep classical factorization methods out of the inference path.  
- Never return intermediate chamber states across the C-to-Python boundary.  
- Never truncate tail data; exceed the measured bound and report unresolved.

---

## 7. Immediate Next Actions

1. Inventory the high-scale certificate fields and the mpz-to-int conversion sites.  
2. Confirm the C library builds cleanly on the current machine.  
3. Build the `mpz_t` overflow test suite for the 2^64 boundary (first concrete task of Phase 2).  
4. Produce a short cost-probe report for one 128-bit-scale anchor.

This sequence keeps the existing resolved ladder intact while the arithmetic layer grows to support the next rung under a strict C-side evaluation contract.
