**The proposed replacement direction is only partially methodologically correct for the next runner.**

The strongest objection is the scale-derived `THREAD_SET` rule. Deriving the thread alphabet cardinality (or selection) from `N.bit_length()` or public radius makes the core definition of triangulation depth itself vary with N. Depth then ceases to be a uniform, comparable measure of public modulus-link closures across the measurement surface; the evidence budget changes per N rather than the data (residues of that N) and the fixed public rule operating on it. This breaks direct comparison of depth histograms, pre_cap densities, and recovery surfaces between cases, mixes mechanism change into the measured reduction, and risks non-auditable computational scaling in the CRT extension tree. The other two controls can (and should) be ratio-adjusted while the alphabet remains a single explicit fixed public constant for the contract version. That preserves the original triangulation mechanism exactly.

### Final ratio-based proposal (public-state-only, triangulation preserved)

All three values are computed from N alone using only the locked public `public_radius` / `original_space_size` formulas already in the v01 contract plus three new locked public ratio constants. The CRT construction, left/right side handling, base (modulus 2, residue 1), depth counting, shared-thread scoring, deterministic sort key, and explanatory-field collection remain byte-for-bit identical in structure to the v01.1 runner.

- **THREAD_SET**: Explicit fixed public constant for this contract version.  
  `THREAD_SET = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)` (first 12 odd primes).  
  No derivation from N. The alphabet is declared once in the contract and used identically for every N. (Future contract versions may adopt a larger fixed tuple under the same ratio rules below.)

- **MIN_DEPTH**: Scale-aware only through the fixed alphabet size (future-proofs later alphabet enlargements without ad-hoc constants).  
  ```
  DEPTH_RATIO = 5 / 12          # locked public rational
  min_depth = max(3, ceil(DEPTH_RATIO * len(THREAD_SET)))
  ```  
  On the current 12-thread set this yields exactly 5, reproducing v01 behavior on the toy corpus. The ratio is the single contract constant; the integer threshold follows deterministically.

- **MAX_CANDIDATES**: Pure public-space retention ratio (directly attacks the documented cap-saturation regime while bounding output size).  
  ```
  RETENTION_DIVISOR = 1024      # locked public integer (~10-bit nominal reduction target)
  ABS_FLOOR = 256
  ABS_CEIL  = 16384
  space = original_space_size(N)
  k = space // RETENTION_DIVISOR
  max_candidates = max(ABS_FLOOR, min(ABS_CEIL, k))
  ```  
  The runner still collects the full qualified set at the computed min_depth, sorts by the public score, then truncates to the per-N `max_candidates`. Actual emitted count is always `min(qualified, max_candidates)`. The reduction metrics continue to use the exact v01 original_space definition.

These formulas are fully deterministic, auditable from the manifest (which must still emit the actual thread_set used, the computed min_depth, the computed max_candidates, N_bits, original_space_size, and all seven explanatory fields), and require zero private information at any point in inference or control selection. On the existing 10-53 bit corpus the new cap grows from 256 (small cases, where it never binds) to 16384 (largest cases), while the depth rule stays at 5.

**One concrete deliverable for this meeting:** A single self-contained decision record (minimal HTML, same visual style as the existing design_contract.html) written under `research-meetings/ratio-replacement-constants-review/decision_record_v02_ratios.html` that states the strongest objection verbatim, the three exact formulas with the four numeric constants above, the required manifest deltas, the one-line public Python reference implementations of the two derived functions, and the precise delta to the pre-implementation certification checklist from v01/v01.1. This record becomes the direct reference for any v02 runner contract.

What single numeric value for RETENTION_DIVISOR (or equivalent RETENTION_FRACTION expressed as a power of two) should the decision record lock so that the v02 surface on a fresh public corpus still targets lists in the low thousands at 40-60 bits while guaranteeing at least 9-10 bits nominal reduction against the locked original_space formula?
