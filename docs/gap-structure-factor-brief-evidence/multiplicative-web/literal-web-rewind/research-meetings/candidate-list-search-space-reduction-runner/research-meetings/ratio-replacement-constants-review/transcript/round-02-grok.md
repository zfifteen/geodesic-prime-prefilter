**Yes, I agree.**

Under the user's explicit goal of replacing hard constants with ratios, both fixed absolute floors/ceilings and a permanently locked 12-thread alphabet should be rejected for v02. The safeguards you describe -- recording the exact derived `active_thread_count` and emitted `thread_set` in every manifest, freezing one ratio formula for the entire campaign, and testing only on fresh corpora -- sufficiently address comparability. They turn the scaling into a reproducible, auditable public derivation rather than hidden per-case tuning.

### Refined assessment of the two objections

1. Absolute floor and ceiling
   You are correct. `ABS_FLOOR` and `ABS_CEIL` re-introduce hard constants and recreate the precise cap-saturation failure mode the explanatory surface already diagnosed. The clean expression that matches the user's request is the pure ratio you wrote:

   ```
   max_candidates = ceil(original_space_size(N) / RETENTION_DIVISOR)
   ```

   With `RETENTION_DIVISOR = 1024` this states a single, mathematically legible rule: at most one retained public distance per 1024 odd positions in the baseline window. Small-N lists may become very short; that is observable evidence about the ratio, not a defect requiring a hidden stop. If the ratio produces too many unresolved (zero-length) cases on a fresh corpus, the remedy is to adjust the single frozen divisor in a later contract version.

2. Permanently fixed 12-thread alphabet
   The 12-element tuple is the largest remaining hard constant in the evidence model itself. The triangulation invariant is successive public modulus-link closures (CRT combinations of residues of N against an ordered public thread alphabet), not the literal integer 12. Supplying a scale-derived prefix length from a fixed, infinite, deterministic public stream (the ordered odd primes) while keeping the closure rule, left/right sides, scoring key, and depth semantics unchanged is consistent with the public-state-only discipline. Recording the derived count and the exact prefix used in every manifest, plus the fresh-corpus rule, keeps the experiment interpretable.

The one material risk that must be stated plainly in the decision record is computational: the current recursive `extend_assignments` implementation branches on every thread and will become intractable once `active_thread_count` exceeds ~18-20 on the target measurement surface. Any `THREAD_COUNT_RATIO` must therefore be set conservatively enough that the construction remains feasible up to the largest N the v02 campaign intends to run.

### Clean v02 ratio proposal (public-state-only, triangulation mechanism preserved)

All controls are derived from public quantities only (`original_space_size(N)`, `public_radius(N).bit_length()`, and locked ratio constants). No private value, no post-freeze adjustment, no absolute hard stops.

- **Retention (replaces MAX_CANDIDATES)**  
  `RETENTION_DIVISOR = 1024` (locked)  
  `max_candidates = ceil(original_space_size(N) / RETENTION_DIVISOR)`

- **Thread alphabet (replaces fixed 12-element tuple)**  
  Public thread stream rule (locked): the ordered sequence of odd primes beginning 3, 5, 7, 11, ...  
  `THREAD_COUNT_RATIO` = a single locked public rational (example conservative value below)  
  `active_thread_count = max(6, ceil(THREAD_COUNT_RATIO * public_radius(N).bit_length()))`  
  `thread_set =` first `active_thread_count` entries from the public stream  
  The manifest must emit both `active_thread_count` and the concrete `thread_set` list actually used for that N.

- **Depth threshold (replaces MIN_DEPTH)**  
  `DEPTH_RATIO = 5/12` (locked)  
  `min_depth = max(3, ceil(DEPTH_RATIO * active_thread_count))`

The CRT extension, candidate construction, scoring, explanatory field collection, PUBLIC_FREEZE_RECORD gate, and canonical membership checker remain unchanged in structure. Only the three numeric controls are now pure public ratios of public size measures.

**One concrete deliverable for this meeting:** A frozen decision record (minimal self-contained HTML in the same style as the existing contracts) at `research-meetings/ratio-replacement-constants-review/decision_record_v02_ratios.html` that records the user's choice of `RETENTION_DIVISOR = 1024`, the exact three ratio formulas above, the chosen numeric value of `THREAD_COUNT_RATIO`, the public thread stream definition, the computational feasibility guardrail, the required manifest fields, and the updated certification checklist. This single artifact becomes the direct input for any v02 runner contract.

What exact value of `THREAD_COUNT_RATIO` (as a simple fraction such as 1/4 or 3/10) should the decision record lock so that `active_thread_count` stays computationally tractable with the existing CRT implementation through at least 64-bit N on fresh corpora?
