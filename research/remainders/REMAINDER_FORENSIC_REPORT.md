# Remainder Research: Super Sleuth Forensic Report

**Date:** 2026-07-07  
**Team:** Super Sleuth Scientific Detective Agent Team (`DETECTIVE_TEAM_MANIFEST.md`)  
**Subject:** Independent forensic examination of Remainder Research Super Team findings  
**Super Team run:** `correlations/investigation/SUPER_TEAM_RUN.json` (all lane collectors `returncode: 0`)  
**Run log:** `correlations/investigation/RUN_LOG.json` (`gaps_with_interiors: 114154`, `records_analyzed: 1385850`)

This report cross-examines pinned artifacts only. It does not re-collect data, edit `PROOF.md`, or upgrade measured statistics to theorem language.

---

## Executive Forensic Summary

| Lane | Agent ID | Integrity verdict | Strongest defensible claim |
|------|----------|-------------------|----------------------------|
| Interior `R(n,M)` | `interior_rnm` | **Confirmed** (scaled surface) | 114,154 gaps; GWR-last 13.86%; MI 0.057; echo repeats 0 |
| Modular remainder zeros | `modular_remainder_status` | **Modular lemma proved** | Measured: 3,842 GWR 4+ zero cases on 1.5e6; modular $z\ge4\Leftrightarrow 30\mid w$ proved |
| Endpoint `q mod` | `endpoint_mask` | **Confirmed** (two regimes, do not merge) | Fresh simple cert: 23.73%; hourly propagated mask ref: 100% |
| `p mod 30` ridge | `mod30_ridge` | **Confirmed** (regime-specific) | Fresh 200k: global right-share 0.193; pinned 1e6 `p≡13` lift 1.576× |
| State-budget cells | `state_budget` | **Inconclusive** | mod30: 230 decisive pairs, +40 advantage, verdict unresolved |
| RSA backward | `rsa_backward` | **Falsified** (toy closure) | 980 cases, 0% factor-reach; searched family falsified |

**Cross-lane finding:** Gap-echo hypothesis is **falsified** (`correlations/CORRELATION_REPORT.md`). Large gaps show universal echoes but **0%** GWR-last when echoes present: opposite of the hypothesized sharpening mechanism.

---

## Methodology

1. **Lane detectives** (six IDs in `DETECTIVE_TEAM_MANIFEST.md`) each audited one Super Team lane.
2. **Evidence chain:** Super Team manifest → `SUPER_TEAM_RUN.json` / `RUN_LOG.json` → lane summary JSON → primary collector output.
3. **Numeric spot-checks:** Seven claims verified by `forensic_verify.py` against primary JSON (see Verification section).
4. **Epistemic audit:** Reconciled modular zero lemma status in `PROOF.md` with measured remainder-lane counts.

### Gap-count semantics (canonical: not a contradiction)

| Field | Meaning | 1.5e6 value | Source |
|-------|---------|-------------|--------|
| `gaps_with_interiors` | Left primes with ≥1 interior record | **114,154** | `output/1.5e6/summary.json`, `interior_placement_stats.json` |
| `prime_walk_steps` | Walk steps including empty-interior gaps | **114,155** | `output/1.5e6/summary.json` |
| `gaps_empty_interiors` | Twin at `p=2` (0 records) | **1** | `output/1.5e6/summary.json` |

The +1 delta is **expected** (one empty twin gap), not a data integrity failure. Legacy alias `gaps_processed` equals `prime_walk_steps` per `collect_remainder_stats.py`.

---

## Lane 1: Interior `R(n,M)` (`interior_rnm`)

**Detective:** `detective_interior`  
**Super Team status:** `streamed`, `gaps_with_interiors: 114154`  
**Primary artifacts:**
- `research/remainders/output/1.5e6/raw_records.jsonl`
- `research/remainders/output/1.5e6/summary.json`
- `research/remainders/correlations/investigation/interior_placement_stats.json`

**Repro:**
```bash
python research/remainders/collect_remainder_stats.py \
  --max-p 1500000 --output-dir research/remainders/output/1.5e6/
```

### Forensic evidence table

| Claim | Value | Source field | Verdict |
|-------|-------|--------------|---------|
| Scaled gap count | 114,154 | `gaps_with_interiors` | **Confirmed** |
| Records emitted | 1,385,850 | `records_analyzed` / `records_emitted` | **Confirmed** |
| GWR-last rate | 0.1386 (15,824 / 114,154) | `gwr_last_rate`, `gwr_last_count` | **Confirmed** |
| MI(num_zeros, dist_bin) | 0.0568 (norm 0.0498) | `mi_num_zeros_vs_dist_bin` | **Confirmed**: weak signal |
| Spearman(entropy, g) | 1.0000 | `spearman_entropy_vs_g` | **Confirmed**: definitional (entropy bins track g) |
| GWR zero − gap avg | −0.670 | `avg_gwr_zero_minus_gap_avg` | **Confirmed** |
| z4 residual @ GWR (4+ zeros) | 3,842 cases | `z4_at_gwr_count` | **Confirmed** |
| GWR with 4+ zeros in g=2 (1.5e6) | 3,842 / 3,842 | `g2_with_z4_gwr` | **Confirmed**: measured conditional only |
| Late echo repeats (vec[:6]) | 0 gaps | `repeat_stats.gaps_with_late_repeats` | **Confirmed** |
| mod-2 even fraction | 0.541 | `mod2_even_fraction` | **Confirmed** |

### Integrity notes

- Surface meets ≥10⁵ gap threshold (114,154 > 100,000). Legacy 1e6 surface (78,497 gaps) remains valid for cross-regime comparison.
- GWR-last rate varies by regime: ~31% (tiny_val 108 gaps), ~14.2% (1e6), **13.86%** (1.5e6). Range is **measured**, not inconsistent counting.
- z4 residual count (3,842) is a **subset** of GWR-last cases (15,824): rate `z4_at_gwr_rate` = 0.0337 among all gaps.

### Lane verdict: **Confirmed** measured interior coordinate system; correlations are descriptive, not predictive theorems.

---

## Lane 2: Modular remainder zeros (`modular_remainder_status`)

**Detective:** `detective_modular_remainder`  
**Super Team status:** `inline` (no subprocess)  
**Primary artifacts:**
- `research/remainders/correlations/investigation/modular_remainder_status.json`
- `PROOF.md` § Modular zero lemma on remainder vector $M_{v1}$

### Forensic evidence table

| Claim | Stated status | Source | Verdict |
|-------|---------------|--------|---------|
| Theorem-stack classification | `proved · modular lemma only` | `modular_remainder_status.json`, `PROOF.md` | **Aligned** |
| Modular lemma $z\ge 4 \Leftrightarrow 30\mid w$ | proved case analysis | `PROOF.md` | **Confirmed** |
| Measured: 4+ zeros @ GWR on 1.5e6 | 3,842 cases | `interior_placement_stats.json` | **Confirmed** (empirical surface only) |
| Gap-size lock from remainder zeros | not in theorem stack | `PROOF.md` | **Confirmed absent** |

**Reconciled classification:**
- **Proved:** modular zero lemma on fixed $M_{v1}$ only.
- **Measured:** finite-surface counts of high-zero GWR witnesses.
- **Not claimed:** any twin-gap or gap-size implication from remainder zeros.

### Lane verdict: **Modular lemma proved**; finite placement counts measured only.

---

## Lane 3: Endpoint `q mod` mask (`endpoint_mask`)

**Detective:** `detective_endpoint`  
**Super Team status:** `ok`, `returncode: 0`  
**Primary artifacts:**
- `correlations/investigation/endpoint_residue_probe_fresh.json`
- `correlations/investigation/endpoint_lane_summary.json`
- Reference: `research/00-index/docs/algorithmic_frontier_hourly.md` (via lane summary)

**Repro:**
```bash
python research/remainders/lane_collectors/endpoint_residue_probe.py \
  --start-p 10000000000037 --max-gaps 10000 \
  --output research/remainders/correlations/investigation/endpoint_residue_probe_fresh.json
```

### Forensic evidence table: Regime A (fresh simple certification)

| Claim | Value | Source | Verdict |
|-------|-------|--------|---------|
| Gaps measured | 10,000 | `gaps_measured` | **Confirmed** |
| Start regime | `p = 10^13 + 37` | `start_p` | **Confirmed** |
| `resolved_in_mask_fraction` | **0.2373** (2,373/10,000) | fresh probe | **Confirmed** |
| Mask width | 96 | `mask_width` | **Confirmed** |
| Max wheel-open index for q | 8 | `max_q_wheel_open_index` | **Confirmed** |
| Mean certified opening prefix | 0.9127 | `mean_certified_opening_prefix_len` | **Confirmed** |
| Certification primes | ≤ 47 | `small_primes_for_certification` | **Confirmed** |

### Forensic evidence table: Regime B (hourly propagated reference)

| Claim | Value | Source | Verdict |
|-------|-------|--------|---------|
| `resolved_in_mask_fraction` | **1.0** | `endpoint_lane_summary.reference_artifact` | **Confirmed** (reference only) |
| Regime | 10^13, 100k consecutive gaps | `reference_artifact.regime` | **Confirmed** |
| Small-prime mod reduction | 99.98% | `small_prime_mod_reduction_fraction` | **Confirmed** |
| Chain mismatches | 0 | `chain_mismatches` | **Confirmed** |

### Contradiction flagged (must not conflate)

**23.73% ≠ 100%** is not a data error. Regime A measures per-gap simple wheel-open certification (candidates composite by primes ≤47). Regime B uses a **96-open propagated state mask** across a GWR chain with full frontier propagation. Merging these into one headline rate would be a forensic fail.

### Lane verdict: **Confirmed** in both regimes separately; operational accelerator potential in Regime B only.

---

## Lane 4: Left-prime `p mod 30` ridge (`mod30_ridge`)

**Detective:** `detective_mod30`  
**Super Team status:** `ok`, `returncode: 0`  
**Primary artifacts:**
- `correlations/investigation/mod30_ridge_probe_fresh.json`
- `correlations/investigation/mod30_ridge_lane_summary.json`
- Pinned: `research/11-gap-ridge/output/insight_probes/residue_mod30_right_edge_share.json`

**Repro:**
```bash
python research/remainders/lane_collectors/mod30_ridge_probe.py \
  --max-p 200000 \
  --output research/remainders/correlations/investigation/mod30_ridge_probe_fresh.json
```

### Forensic evidence table: Fresh probe (`max_p = 200,000`)

| Residue | Gaps | Right share | Right lift | Verdict |
|---------|------|-------------|------------|---------|
| Global | 17,983 | 0.1926 | 1.00 (baseline) | **Confirmed** |
| p≡1 | 2,224 | 0.2932 | 1.522× | **Confirmed** |
| p≡7 | 2,256 | 0.3440 | 1.786× | **Confirmed** |
| p≡11 | 2,254 | 0.0905 | 0.470× | **Confirmed** |
| p≡13 | 2,268 | 0.2134 | 1.108× | **Confirmed** |
| p≡17 | 2,247 | 0.0966 | 0.501× | **Confirmed** |
| p≡19 | 2,240 | 0.1875 | 0.973× | **Confirmed** |
| p≡23 | 2,248 | 0.2260 | 1.173× | **Confirmed** |
| p≡29 | 2,244 | 0.0905 | 0.470× | **Confirmed** |

### Forensic evidence table: Pinned 1e6 scale

| Residue | Gaps @ 1e6 | Right lift | Verdict |
|---------|------------|------------|---------|
| p≡13 | 9,824 | **1.576×** | **Confirmed** |
| p≡1 | 9,807 | 1.052× | **Confirmed** |
| p≡11 | 7,074 | 0.580× (left-heavy) | **Confirmed** |

### Integrity notes

- Fresh 200k probe shows **stronger** lifts at p≡1 and p≡7 than pinned 1e6 p≡13: scale and `max_p` matter. Do not extrapolate 200k ranking to 1e6+ without re-measurement.
- Ridge signal is **measured peak-side modulation** of GWR placement; it does not select `q`.

### Lane verdict: **Confirmed** residue-conditioned asymmetry; regime labels mandatory.

---

## Lane 5: State-budget residue cells (`state_budget`)

**Detective:** `detective_state_budget`  
**Super Team status:** `ok`, `returncode: 0`  
**Primary artifacts:**
- `correlations/investigation/state_budget_lane_summary.json`
- `research/05-state-budget/output/state_budget_residue_matched_pair_summary.json`

**Repro:**
```bash
python research/05-state-budget/scripts/state_budget_residue_matched_pair_test.py
```

### Forensic evidence table

| Claim | Value | Source | Verdict |
|-------|-------|--------|---------|
| mod30 decisive pairs | 230 | `mod30_decisive_pairs` | **Confirmed** |
| Signed advantage | +40 | `mod30_signed_advantage` | **Confirmed** |
| Advantage share | 17.39% | `mod30_advantage_share` | **Confirmed** |
| Verdict | unresolved | `mod30_verdict` | **Inconclusive** |

### Integrity notes

+40 wins on 230 decisive pairs is a **modest** directional signal. Without pre-registered significance thresholds, multiplicity across residue cells, or held-out validation, the detective classifies this as **inconclusive**: not falsified, not confirmed as a budget law.

### Lane verdict: **Inconclusive**: probe completed cleanly; evidentiary standard not met for promotion.

---

## Lane 6: RSA backward modulus/remainder (`rsa_backward`)

**Detective:** `detective_rsa`  
**Super Team status:** `ok`, `returncode: 0`  
**Primary artifacts:**
- `correlations/investigation/rsa_lane_summary.json`
- `research/06-cryptology-rsa/output/semiprime_branch/pgs_semiprime_backward_invariant_closure_search_summary.json`

**Repro:**
```bash
python research/06-cryptology-rsa/scripts/pgs_semiprime_backward_invariant_closure_search.py \
  --max-n 5000 --output-dir research/06-cryptology-rsa/output/semiprime_branch
```

### Forensic evidence table

| Claim | Value | Source | Verdict |
|-------|-------|--------|---------|
| Toy case count | 980 | `case_count` | **Confirmed** |
| Best factor-reach recall | **0.0** | `best_factor_reach_recall` | **Confirmed** |
| Best law | `containing_gap_mod_n` | closure summary | **Confirmed** |
| Searched family falsified | true | `searched_family_falsified` | **Falsified** |
| Dominant failure | `entry_not_lane` (733) | stdout in `RUN_LOG.json` | **Confirmed** |

### Integrity notes

This lane tests **backward** remainder/modulus invariants on semiprimes `N ≤ 5000`. Zero recall falsifies the searched invariant **family** on this toy surface: not RSA security, not live-solver v2 certificates. Scope is intentionally narrow.

### Lane verdict: **Falsified** for toy backward closure family; live RSA engine track is separate.

---

## Cross-Lane Hypothesis: Gap-Echo (`CORRELATION_REPORT.md`)

**Detective cross-reference:** All interior detectives + `detective_interior`

| Regime | Gaps | has_echo | GWR_last \| echo | Verdict |
|--------|------|----------|------------------|---------|
| tiny_val | 108 | 0 | untestable | No support |
| 1e6 full | 78,497 | 0 | baseline 14.16% | Echo impossible (g≤114) |
| 1.5e6 | 114,154 | 0 | baseline 13.86% | **Confirmed** repeat_stats |
| Large gaps (50, g≈480 to 1442) | 50 | 100% | **0%** | **Falsified** |
| Synthetic positive control | 500 | forced | ~100% vs ~27% | Analysis code valid |

**Ruling:** Hypothesis that late remainder echoes **sharpen** GWR terminal placement is **falsified**. When echoes exist (large g), GWR is **never** last (0/50). Echo mechanism is a **dead end** for placement prediction.

Sources: `research/remainders/correlations/CORRELATION_REPORT.md`, `interior_placement_stats.json` `repeat_stats`, `gap_echo_hypothesis_validation_plan.md`.

---

## Cross-Lane Epistemic Audit

| Source | What it claims | Stack truth | Detective ruling |
|--------|----------------|-------------|------------------|
| `PROOF.md` modular zero lemma | $z\ge 4 \Leftrightarrow 30\mid w$ on $M_{v1}$ | proved, modular only | **Aligned** |
| `modular_remainder_status.json` | `proved · modular lemma only` | matches `PROOF.md` | **Aligned** |
| `REMAINDER_LANES_SYNTHESIS.md` | Six-lane measured inventory | Aligned | **Confirmed** honest framing |
| Finite 1.5e6 z4@GWR counts | 3,842 cases | measured surface only | **Confirmed** empirical |

**Reconciled rule:** Cite the modular zero lemma as proved. Cite finite high-zero GWR counts as measured on the named surface. Do not promote finite empty false-positive counts into a gap-size theorem.

---

## Super Team Run Integrity (`SUPER_TEAM_RUN.json` / `RUN_LOG.json`)

| Agent | Collector | Status | Returncode |
|-------|-----------|--------|------------|
| `interior_rnm` | `collect_remainder_stats.py` | streamed | n/a |
| `modular_remainder_status` | inline orchestrator | inline | n/a |
| `endpoint_mask` | `endpoint_residue_probe.py` | ok | **0** |
| `mod30_ridge` | `mod30_ridge_probe.py` | ok | **0** |
| `state_budget` | `state_budget_residue_matched_pair_test.py` | ok | **0** |
| `rsa_backward` | `pgs_semiprime_backward_invariant_closure_search.py` | ok | **0** |

Fresh probes executed 2026-07-07T23:06Z (endpoint, mod30). Interior streamed from on-disk 1.5e6 JSONL. Pinned references used where noted (endpoint hourly, mod30 1e6 insight probe).

**Checkout note:** `output/1.5e6/` and `output/1e6/` may be gitignored; forensic citations assume on-disk paths in the investigating environment. Reproduce via collector commands above.

---

## Synthesis: What Role Do Remainders Play in PGS?

### Proved (independent of this investigation)

- **GWR interior maximizer** and **next-prime rule**: formal spine (`PROOF.md`); remainder vectors are **coordinates** on gap interiors, not replacements for GWR.
- **Finite bases** certify GWR/compression up to stated bounds.

### Measured correlations (confirmed on named regimes)

1. **Interior coordinate:** `R(n,M_v1)` is a reproducible attachment to each interior record; weak MI(zeros, termination) ≈ 0.057 at 1.5e6.
2. **GWR-last baseline:** ~14% of gaps (regime-dependent); not driven by late echo repeats at scale ≤1.5e6.
3. **z4 residual counts:** 4+ zeros at GWR on the 1.5e6 surface: 3,842 cases (measured only; modular lemma is separate and proved).
4. **Mod-30 ridge:** Left-prime residue modulates right-edge share (e.g. p≡13 lift 1.576× @ 1e6).
5. **Endpoint acceleration:** Propagated 96-open mask achieves 100% in-window resolution at 10^13 (reference); simple per-candidate cert ~24%.

### Operational (engineering, not proved closure)

- Endpoint propagated mask + small-prime mod reduction for search acceleration.
- Ridge orientation as a **prior** on witness placement side: not a selector for `q`.

### Dead ends / falsified

- **Gap-echo sharpening** of GWR terminal placement: falsified on large-gap sample.
- **Toy RSA backward invariant family** (`N≤5000`): 0% factor-reach; family falsified.

### Honest limits

- Scales: 1.5e6 interior, 200k ridge fresh, 10k endpoint @ 10^13, 980 RSA toys.
- No predictive ML or held-out validation in this Super Team pass.
- Finite high-zero GWR counts are not a gap-size theorem.

---

## Downstream Research Index (prioritized)

| Priority | Probe | Open question | Artifacts / command |
|----------|-------|---------------|---------------------|
| **P1** | Modular lemma Lean mirror | Optional formalization of $z\ge4\Leftrightarrow 30\mid w$ on $M_{v1}$ | `PROOF.md`, `modular_remainder_status.json` |
| **P2** | z4 residual converse | Does g=2 twin gap always show 4+ zeros at GWR? (not measured here) | `interior_placement_stats.json`, extend collector |
| **P3** | Endpoint regime bridge | Quantify gap between 23.7% simple cert vs 100% propagated mask | `endpoint_lane_summary.json`, hourly doc |
| **P4** | Ridge scale stability | Does p≡13 lift 1.576× persist at 1.5e6? | `mod30_ridge_probe.py --max-p 1500000` |
| **P5** | State-budget resolution | Pre-register decisive-pair threshold; hold-out cells | `state_budget_lane_summary.json` |
| **P6** | MI termination | Permutation null for MI=0.057 at 1.5e6 | `interior_placement_stats.json`, new test script |
| **P7** | Echo mechanism post-mortem | Why 0% GWR-last when echoes present? | `CORRELATION_REPORT.md`, large-gap JSONL |
| **P8** | RSA backward v2 | Map toy falsification to live-solver certificate gaps | `research/06-cryptology-rsa/output/semiprime_branch/` |

---

## Verification

```bash
python research/remainders/forensic_verify.py
python -m pytest research/remainders/test_forensic_report.py -q
```

Spot-checked numerics (primary JSON): `gaps_with_interiors=114154`, `gwr_last_rate≈0.1386`, `z4_at_gwr_count=3842`, `resolved_in_mask_fraction=0.2373`, `p≡13 right_lift=1.576×`, `mod30_decisive_pairs=230`, `best_factor_reach_recall=0.0`.

---

**End of forensic report.**