# FINDINGS_LWM_PROP_01: Deterministic Local Propagation (Carry Analog)

**Experiment ID:** LWM-PROP-01  
**Path:** literal multiplicative-web / thread-triangulation (under rewind contract)  
**Location:** `docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/japanese-thread-mapping-plan/LWM-PROP-01/`  
**Baseline:** literal hole-trace flat primary support (from `literal_web_hole_trace.py`)  
**Status:** COMPLETE: all artifacts frozen

---

## Outcome (Leads All Interpretation)

**Propagation improved nomination of the true held-out distances in the ladder regime without introducing any leakage or false positives into the maximum-evidence tier.**

- On the 4 toy cases (baseline sqrt-radius): no regression. The unique max-support hole remained the same true direct offset in all 4/4 cases. Emitted max-set size and purity unchanged (1/1 true).
- On 6 ladder rungs (6×p radius, up to 131×167): strict improvement in 5/6 cases for the key nomination metric (count of true held-out direct p/q-thread offsets that reach the global maximum support tier). In 0 cases did the count of trues in the max tier decrease.
- In all 10 cases (100%), every offset that reached the augmented maximum support tier after propagation was a true held-out distance. **Zero non-true offsets were promoted into the emitted max set.**
- Full provenance logs confirm every +1 bonus was applied using only post-holdout public small-prime kernels on already-positive primary support positions.
- The rule is fully reversible and produced no new candidate offsets.

**Comparison vs baseline (flat primary support only):**
- Baseline already nominates true offsets at the max tier (4/4 toys; 1 to 5 trues per ladder rung in the max tier).
- After deterministic propagation the max tier captured 3 to 9 trues per ladder rung (increases of +2 to +6 in five cases; 0 change in one).
- Best rank of any true remained 1 (already optimal in baseline). Multiple individual true offsets improved their position in the full descending-support ordering.
- Emitted max-set size increased only by addition of additional true offsets (purity stayed 100% true).
- No degradation on any case.

---

## Exact Propagation Rule (Public, Auditable, Implemented)

Applied **after** primary flat support computation and holdout, using **only** public data:

1. From the primary support map (built exclusively from factors of heldout rows), extract the sorted list of all distinct public small primes that contributed any thread.
2. Kernels K = the smallest 6 of those public primes (fixed public constant `PROP_MAX_KERNELS=6` for this experiment; data-driven from the web itself).
3. Strong sources = all offsets t where primary_support[t] >= 2 (fixed public constant `PROP_THRESHOLD=2`).
4. For each strong t, each k ∈ K, each sign ∈ {+1, −1}:
   - tp = t + sign × k
   - If |tp| ≤ radius, tp ≠ 0, **and** primary_support[tp] ≥ 1 (explicit guard: only reinforce existing positive-support holes):
     - Add +1 (fixed public `PROP_BONUS`) to augmented score of tp.
     - Record provenance entry {"from_offset": t, "k": k} for reversibility.
5. Single synchronous (one-pass) application. No iteration, no fixed-point, no multi-hop chains, no search.
6. Augmented support at t = primary_support[t] + bonus[t].
7. Nomination: offsets achieving the new global max(augmented) are emitted (tie-break identical to baseline: by |t| then t). Full sorted list also retained for rank analysis.

**Reversibility & audit:** Every augmented hole carries its complete list of contributing (source, k) pairs. Re-running the identical public rule on the frozen primary_support + public_primes list reproduces the bonuses exactly.

**Leakage controls (enforced in code):**
- p and q used **only** to simulate holdout of direct rows (identical to baseline contract) and for final scoring/audit labels.
- Kernel selection, threshold, bonus, target acceptance, and all decisions use **zero** information from direct_offsets, audit_kind, or the values of p/q.
- No candidate generation: propagation never adds support to a position that had primary_support = 0.
- No classical methods, no ratios, no pruning, no residue arithmetic in the propagation step.

---

## Detailed Metrics (from frozen artifacts)

| case              | scale          | radius | prim_max | aug_max | prim emitted (trues) | aug emitted (trues) | trues total | non-trues in aug max |
|-------------------|----------------|-------:|---------:|--------:|----------------------|---------------------|------------:|----------------------|
| toy_23x31        | baseline_sqrt |     26 |        3 |       3 | 1 (1)               | 1 (1)              |           2 | 0                    |
| toy_43x59        | baseline_sqrt |     50 |        3 |       3 | 1 (1)               | 1 (1)              |           2 | 0                    |
| toy_61x83        | baseline_sqrt |     71 |        3 |       3 | 1 (1)               | 1 (1)              |           2 | 0                    |
| toy_89x113       | baseline_sqrt |    100 |        3 |       3 | 1 (1)               | 1 (1)              |           2 | 0                    |
| ladder_00_23x31  | ladder_6p     |    138 |        3 |       3 | 1 (1)               | 3 (3)              |          20 | 0                    |
| ladder_01_43x59  | ladder_6p     |    258 |        3 |       3 | 2 (2)               | 8 (8)              |          20 | 0                    |
| ladder_02_61x83  | ladder_6p     |    366 |        3 |       3 | 3 (3)               | 3 (3)              |          20 | 0                    |
| ladder_03_89x113 | ladder_6p     |    534 |        3 |       3 | 3 (3)               | 7 (7)              |          20 | 0                    |
| ladder_04_101x137| ladder_6p     |    606 |        3 |       3 | 5 (5)               | 9 (9)              |          20 | 0                    |
| ladder_05_131x167| ladder_6p     |    786 |        3 |       3 | 5 (5)               | 7 (7)              |          20 | 0                    |

**Aggregate:** 5/6 ladder rungs showed increased true coverage in the max tier. 0/10 cases showed any non-true promoted to max tier. 0/10 cases showed regression in true coverage at the max tier.

**Example provenance (ladder_01_43x59, N=2537):**
- 118 (true): primary=2 → aug=3, +1 from 129 (k=11)
- 129 (true): primary=2 → aug=3, +1 from 118 (k=11)
- −172 (true): primary=2 → aug=3, +1 from −177 (k=5)
- 172 (true): primary=2 → aug=3, +1 from 177 (k=5)
- −177 (true): primary=2 → aug=3, +1 from −172 (k=5)
- 177 (true): primary=2 → aug=3, +1 from 172 (k=5)
(The two primary=3 trues at 43 and −59 received 0 bonus in this case.)

Mutual reinforcement occurs precisely when two true direct offsets are separated by a small public prime that appears in the web.

---

## Guardrail & Contract Compliance

- **PGS / rewind contract:** Fully inside literal web. No return to parked ratio/candidate machinery. Public web evidence → primary support → public propagation → emitted offsets → audit labels read last.
- **No hidden search paths:** Rule is a fixed, local, one-pass function of public data only. No optimization, no iteration, no residue search, no trial division.
- **No leakage:** All propagation decisions independent of p/q values.
- **Reversible & auditable:** Complete provenance + manifest + public_nomination.json per case + full results.json.
- **No candidate expansion:** PROP_ONLY_TO_POSITIVE guard enforced; zero positions with primary=0 ever received support.
- **Deterministic:** Same inputs (N, radius, public factors after holdout) always produce identical bonuses and nominations.
- **No violations** recorded in manifest.json (`"no_violations": true`).

---

## Artifact Inventory (All Paths Absolute)

All outputs under:
`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/japanese-thread-mapping-plan/LWM-PROP-01/`

- `lwm_prop_01_runner.py`, self-contained implementation (exact rule + baseline replica)
- `output/manifest.json`, run metadata + rule constants
- `output/LWM_PROP_01_summary.md`, machine-generated aggregate table
- `output/results.json`, complete per-case data including provenance for every hole
- `output/augmented_top_holes.jsonl`, every offset that reached max augmented tier across cases
- Per-case directories (e.g. `output/ladder_01_43x59/`):
  - `public_nomination.json`, public freeze (kernels, rule description, emitted offsets chosen by augmented, no audit labels in decision fields)
  - `audit_comparison.json`, true ranks + emitted trues (audit sidecar)
  - `holes_augmented.jsonl`, sample of holes with full propagation_sources

SHA256 / reproducibility: re-run the runner.py with identical CASES list and constants reproduces the outputs exactly (sympy factorint is deterministic for these inputs).

---

## Interpretation (After Outcome)

The Japanese carry analog maps cleanly onto the literal web: small public primes observed in the thread web act as natural "place-value" steps. When multiple true factor-distance offsets (and their low-multiple relatives visible in the direct rows) lie a small public prime apart, their mutual thread support reinforces under the rule, lifting an entire local cluster to the highest evidence tier together.

This is pure post-processing of the existing public thread object. It requires no new information, creates no search, and demonstrably concentrates the true held-out distances at the peak without polluting that peak with non-trues.

The effect is scale-sensitive: negligible on tiny sqrt-radius toys (already maximal signal), material on 6×p ladder windows where more structural intervals align with the small public primes.

**No theorem is claimed.** This is a measured, contract-compliant refinement of the literal web nomination surface. Future secondary experiments (banded, cross-family, witness) remain independent.

---

**End of FINDINGS_LWM_PROP_01**  
All claims are directly supported by the frozen artifacts listed above. The propagation rule is reproduced verbatim in the public_nomination.json files and the runner source.