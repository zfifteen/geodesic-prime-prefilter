# Grok Findings Report: v02 Ratio Execution Review

**Meeting:** candidate-list-search-space-reduction-runner  
**Contract:** v02 (ratio-derived controls per pre-execution certification)  
**Public runner:** `thread_triangulation_v02_ratio_runner.py`  
**Certified source SHA-256:** `15be58e3d1fb9e026a76fc67b69ca6c5999ecc01351f65e90e84cc2c6211c465`  
**Harness:** `run_v02_ratio_toy_corpus.py` (SHA-256 `cd2c1eda23261f164f4360a88ad941bc8c5d3d14753a23ed3a2527a20d181d94`)  
**Corpus:** `cases/toy_corpus.jsonl` (10 toy semiprimes, 10–53 bits)  
**Output surface:** `output/toy_v02_ratio/`  
**Execution classification:** `certified_for_execution` (pre-execution)  
**Report scope:** Public manifests, public output files, public freeze logs, canonical status files (`audit/status.json`), aggregate summary files, and the v02 source certification only.

---

## Compliance Status

The execution fully complied with the v02 pre-execution certification and the certified source-separation boundary.

- Runner and harness SHAs on disk match the exact values stated in the certification.
- `py_compile` and private-token scan at certification time were clean; the same scan executed inside the runner at every runtime freeze.
- Every one of the 10 cases produced a complete `PUBLIC_FREEZE_RECORD` containing:
  - `public_source_private_token_scan: pass` (all 19 forbidden tokens false).
  - SHA-256 of the emitted `public_output.jsonl` and `public_manifest.json`.
  - Public reduction metrics (`original_space_size`, `candidate_reduction_ratio`, `candidate_reduction_bits`, `emitted_count`, `pre_cap_qualified_count`, `cap_active`, depth counts, `thread_set`, etc.).
  - `PRIVATE_AUDIT_UNLOCKED: true` printed only after the clean gate.
- The public runner accepts only `--n` (public N value) and `--out-dir`. It contains zero references to audit pairs, `p`/`q`, factor labels, or any private path. All ratio derivations (`active_thread_count`, `min_depth`, `max_candidates`) are computed from public `N` alone using the three locked constants.
- The harness strictly sequenced public runner execution + `public_freeze.log` generation before invoking the canonical membership audit.
- The public runner never imports, reads, or receives the audit pairs. The harness performs no re-ranking, re-scoring, or post-audit filtering of the public candidate list.
- All public manifests declare the exact v02 constants and derived fields:
  - `retention_divisor: 1024`
  - `thread_count_ratio: "3/8"`
  - `depth_ratio: "5/12"`
  - concrete `thread_set` (first `active_thread_count` odd primes)
  - computed `min_depth`, `max_candidates`, `cap_active`, `pre_cap_to_emitted_ratio`, etc.
- Source private-token scan inside the runner itself was clean at both certification and every execution.

No contract violations, source-separation breaches, or post-freeze private influence were detected in the delivered artifacts.

---

## Result Summary

**Aggregate (from `summary.json` and per-case `audit/status.json`):**

- policy: `thread_triangulation_v02_ratio`
- case_count: 10
- recovered_count: 0
- missed_count: 10
- hit_rate: `0/10`
- median_emitted_count: 36.0
- median_candidate_reduction_bits: 10.0

**Per-case public reduction surface (values from `public_manifest.json` and `audit/status.json`):**

| case                  | N_bits | active threads | min depth | max candidates | emitted | pre-cap | cap active | reduction bits | status  | recovered_factor |
|-----------------------|--------|---------------:|----------:|---------------:|--------:|--------:|-----------:|---------------:|---------|------------------|
| `toy_989`             | 10     | 3             | 2         | 1              | 1       | 7       | `True`     | 4.0            | missed  | null             |
| `toy_9379`            | 14     | 3             | 2         | 1              | 1       | 10      | `True`     | 6.0            | missed  | null             |
| `toy_25807`           | 15     | 4             | 2         | 1              | 1       | 28      | `True`     | 7.0            | missed  | null             |
| `toy_1242079`         | 21     | 5             | 3         | 1              | 1       | 79      | `True`     | 10.0           | missed  | null             |
| `toy_200250077`       | 28     | 6             | 3         | 8              | 8       | 226     | `True`     | 10.0           | missed  | null             |
| `toy_4295229443`      | 33     | 7             | 3         | 64             | 64      | 663     | `True`     | 10.0           | missed  | null             |
| `toy_18902665303`     | 35     | 8             | 4         | 128            | 128     | 1296    | `True`     | 10.0           | missed  | null             |
| `toy_1209476905903`   | 41     | 9             | 4         | 1024           | 1024    | 2890    | `True`     | 10.0           | missed  | null             |
| `toy_77468500194643`  | 47     | 10            | 5         | 8192           | 8192    | 10580   | `True`     | 10.0           | missed  | null             |
| `toy_4951764003343009`| 53     | 11            | 5         | 65536          | 29348   | 29348   | `False`    | 11.159...      | missed  | null             |

All 10 `public_manifest.json` files and `public_output.jsonl` files were produced under identical locked v02 ratio formulas and carry the certified runner SHA. All `audit/status.json` files report `audit_behavior: "canonical_membership_only"` and `status: "missed"`.

---

## Search-Space Reduction Interpretation

The measured reduction is the publicly observable shrinkage from the conservative baseline (`original_space_size` = count of odd positive distances d with 1 ≤ d ≤ `public_radius(N)`) to the size of the emitted list after:

1. CRT left/right residue closure construction over the ratio-derived `thread_set` (first `active_thread_count` odd primes),
2. retention only of distances that reach `min_depth` (ceil(DEPTH_RATIO × active_thread_count)),
3. deterministic score sort (triangulation_depth desc, shared_thread_count desc, total_thread_count desc, distance asc),
4. hard cap at `max_candidates = ceil(original_space_size / 1024)` when `pre_cap_qualified_count` exceeds the cap.

- For the four smallest cases the cap was extremely tight (`max_candidates = 1`); only the single highest-scoring survivor was emitted.
- For the five mid-to-large cases with `cap_active = True`, the emitted list size equals `max_candidates` (8 → 8192); the cap was the binding constraint.
- For the single largest case `cap_active = False`; every distance that reached depth ≥ 5 under the 11-thread set (29 348 of them) was emitted because the qualified set was already smaller than the 1/1024 cap.
- Median nominal reduction: 10 bits. The largest case achieved ~11.16 bits (67 M → 29 348) while still missing.

These figures are deterministic, reproducible, and fully auditable from the public manifests alone.

---

## Interpretation of 0/10

Under the locked v02 ratio formulas (`THREAD_COUNT_RATIO = 3/8`, `DEPTH_RATIO = 5/12`, `RETENTION_DIVISOR = 1024`), the public thread-triangulation nomination process placed the true factor distance inside the emitted public list for **0 of the 10** declared toy semiprimes.

This is an exact, reproducible measurement of public list membership on a fixed public corpus after the public surface was frozen under the certified contract. The `0/10` result is not a statistical claim; it is the observed containment count for this specific choice of ratios on this specific corpus.

The result does **not**:
- Prove the ratio machinery “never works.”
- Indicate that true factor distances are “usually” or “often” excluded.
- License any statement about behavior at cryptographic sizes.
- Supply per-distance diagnostics (those are excluded from the allowed surface).

It simply records that, for every N in the corpus, the distance corresponding to the hidden factor pair either never reached `min_depth` under the ratio-derived `thread_set`, or reached it but did not rank high enough under the public score key to survive the subsequent cap.

---

## Does This Invalidate the Ratio Implementation?

**No.** The ratio implementation itself (public derivation of `active_thread_count`, `min_depth`, and `max_candidates`; the unchanged CRT left/right extension engine; the deterministic scoring and cap logic; the freeze gate with embedded token scan) performed exactly as specified in the v02 certification and the runner source.

The `0/10` outcome reflects the **particular initial ratio choice** (3/8 thread ratio, 5/12 depth ratio, 1024 retention) on this corpus, not a defect in the public-only derivation or separation machinery.

The implementation remains a valid, auditable vehicle for future ratio experiments under the same public contract. Only the specific constant values are called into question by the observed result.

---

## Public Observables on the Failure Mode

From the public manifests, outputs, freeze logs, and canonical status files alone (no private data):

- **Small-N regime (active threads 3–5, min_depth 2–3):** The 1/1024 cap produced `max_candidates = 1`. The single emitted distance (highest public score) was never the true distance. Pre-cap qualified counts were already small (7–79), yet the true distance was absent from even the pre-cap set or ranked below the cutoff.
- **Mid-N regime (active threads 6–10, min_depth 3–5, cap active):** Emitted exactly the top `max_candidates` (8, 64, 128, 1024, 8192). The true distance’s public score tuple placed it outside the retained prefix. Depth histograms show that depths 6–10 are populated and preferentially retained, but the true distances did not achieve competitive (depth, shared, total) combinations.
- **Largest case (active threads 11, min_depth 5, cap inactive):** 29 348 distances reached depth ≥ 5 and were all emitted. The true distance is not among them. Therefore its maximum construction depth under the concrete 11-thread set (3,5,…,31) was strictly less than 5, or it required a thread outside the first 11 odd primes to appear at all.
- **Thread sets:** Always the leading odd primes (3,5,7,…). No private selection.
- **Score key:** Identical across all cases and identical to prior v01/v01.1 (depth primary). High-depth, high-total, low-shared candidates dominate the emitted heads when the cap permits.
- **Cap behavior:** The 1/1024 rule produced the intended “roughly 10-bit” nominal reduction on most cases; the last case shows the formula correctly becoming non-binding when the min-depth filter already prunes aggressively.

All of the above is visible in the `public_manifest.json` depth counts, `cap_active` flags, `thread_set` arrays, `pre_cap_to_emitted_ratio` values, and the ranked `public_output.jsonl` records. No hidden-factor information is required to state these observables.

---

## Recommended Next Ratio Adjustment (Strictly Public-Only, No Hard Floors or Ceilings)

A single clean, minimal adjustment that remains entirely inside the ratio framework and preserves the no-floor/no-ceiling discipline:

**Change `THREAD_COUNT_RATIO` from `3/8` to `1/2` (equivalently `4/8`), keeping `DEPTH_RATIO = 5/12` and `RETENTION_DIVISOR = 1024`.**

**Rationale (public observables only):**  
The 3/8 ratio produced `active_thread_count` values of 3–11 on the corpus. Even the largest case, which emitted every distance that reached depth ≥ 5 under 11 threads, still missed. This indicates that the true distances required either a materially larger thread alphabet or a lower relative `min_depth` to enter the qualified set. Raising the thread ratio to 1/2 directly enlarges `active_thread_count` for every N (approximately 13–14 threads for the 53-bit case, ~14–15 for the next natural 60-bit surface, etc.) while leaving the rest of the public derivation, CRT engine, scoring, and cap logic untouched. The new `active_thread_count`, `min_depth`, and concrete `thread_set` values remain purely ratio-derived from public `N` and will appear in every future manifest for independent audit.

This change yields a fresh, frozen v02.1 (or v03) contract with exactly one declared constant updated, a new runner SHA, a new pre-execution certification round, and (if desired) a new public corpus never previously audited. All other machinery and the source-separation boundary stay identical.

Alternative single-constant tweaks (e.g., `DEPTH_RATIO = 6/12` or `RETENTION_DIVISOR = 512`) are also admissible under the same public-only discipline; the thread-ratio increase is offered as one minimal, high-leverage, still-ratio example that directly addresses the observed exclusion of true distances from the qualified sets.

---

**End of report.** All statements are bounded by the declared 10-case toy corpus, the certified v02 runner and harness artifacts, the public manifests and freeze records actually produced, and the public-only review contract. No private ranks, private containment diagnostics, per-distance hidden-factor explanations, or post-freeze tuning were used or cited.

The execution was a clean, faithful run of the certified v02 ratio policy. The `0/10` result is a legitimate public measurement that now informs the next public ratio adjustment.