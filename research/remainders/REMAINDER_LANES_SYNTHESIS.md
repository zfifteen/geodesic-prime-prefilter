# Remainder Lanes Synthesis — Multi-Lane Investigation Report

**Date:** 2026-07-07  
**Investigation runner:** `research/remainders/run_investigation.py`  
**Python:** 3.13.0 (see `correlations/investigation/RUN_LOG.json`)

PGS framing: all statistics below are **measured on named regimes**. They do not establish theorems, redefine GWR, or choose the next prime `q`.

---

## Executive summary

Remainders appear in PGS under **six distinct lanes** that are not yet unified epistemically. This report inventories each lane, pins reproducible artifacts, and quantifies associations (or null results) between remainder features and gap-length / prime-placement proxies.

| Lane | Role in PGS | Data status | Strongest measured signal |
|------|-------------|-------------|---------------------------|
| Interior `R(n,M)` | Coordinate on gap interiors | **Scaled** (78,498 gaps, 921,503 records at `p≤10⁶`) | Low MI between `num_zeros` and termination distance (0.058); GWR-last rate 14.2% |
| GWR Super-Signal | Claimed termination invariant at GWR | **Epistemic open** (theorem vs measured split) | On `p≤10⁶`, every GWR with 4+ zeros occurs in `g=2` gaps (2,697 cases); proof hardening pending G2 |
| Endpoint `q mod` masks | Search acceleration | **Pinned** (hourly frontier doc) | 100% next-prime resolution inside 96-open mask at `10¹³`; 99.98% small-prime mod reduction |
| Left-prime `p mod 30` ridge | Ridge orientation modulation | **Scaled** (JSON through `10¹⁸`) | `p≡13 (mod 30)` right-edge lift 1.58× at `10⁶` |
| State-budget residue cells | Matched-pair transition tests | **Pinned** (powers 12–18) | `mod30` match: 230 decisive pairs, +40 square-ruler advantage (unresolved) |
| RSA backward modulus/remainder | Semiprime closure search | **Pinned** (toy `N≤5000`) | Zero factor-reach recall on all invariant laws tested |

**Gap-echo hypothesis:** Falsified — see `research/remainders/correlations/CORRELATION_REPORT.md` (no late repeats for `g<210`; large-gap echoes correlate with GWR *earlier*, not terminal).

---

## Lane 1 — Interior remainder vectors `R(n, M_v1)`

**Objects:** For each interior composite `n` in gap `(p,q)`, vector `(n mod 2, 3, 5, 7, 30, 210, 2310)`.

**Status:** Collection complete at `p ≤ 10⁶`. Validated tiny set at `p ≤ 600` (108 gaps).

**Repro:**
```bash
python research/remainders/collect_remainder_stats.py \
  --max-p 1000000 \
  --output-dir research/remainders/output/1e6/
python research/remainders/enrich_remainder_records.py \
  --input research/remainders/output/1e6/raw_records.jsonl \
  --output research/remainders/correlations/enriched/1e6_enriched.jsonl
```

**Pinned counts** (`research/remainders/output/1e6/summary.json`):
- Gaps processed: **78,498**
- Interior records: **921,503**
- Max observed `g`: **114** (repeats impossible on `vec[:6]` state in this regime)

**Placement correlations** (measured on full 1e6 JSONL stream):

| Proxy | Metric | Value |
|-------|--------|-------|
| Prime placement | GWR-last rate (`dist_to_next==1` at GWR) | **0.1416** (11,115 / 78,497 gaps) |
| Termination | MI(`num_zeros`, `dist_to_next` binned) | **0.0584** (normalized 0.0507) — near-null |
| Gap length | Spearman(entropy of `vec[:6]`, `g`) | **1.0000** (expected: almost-unique states for small `g`) |
| GWR signature | Avg zeros at GWR minus gap average | **−0.664** (GWR tends to have fewer zeros) |
| Modular density | Fraction with `n ≡ 0 (mod 2)` | **0.543** |

Artifact: `research/remainders/correlations/investigation/interior_1e6_placement_stats.json`

**Open questions:**
- Does any remainder scalar predict GWR-last above baseline 14% on disjoint `p` ranges?
- Extend collector to `p ≤ 10⁷` for `g` large enough to test echo regime (`g ≥ 210`).

---

## Lane 2 — GWR Super-Signal (epistemic status only)

**Claim:** If GWR winner `w` has 4+ zeros in `R(w)`, then `g=2` and `q=w+1`.

**Status:** Written as theorem in `PROOF.md` but theorem-stack row says **measured · corollary**. Proof-enhancements **G2** lists open hardening items (`docs/proof-enhancements/goals.md`). **No Lean mirror.**

**Empirical check on interior 1e6 surface (measurement, not proof):**
- GWR records with 4+ zeros: **2,697** (3.44% of gaps)
- All **2,697** occur in **`g=2`** gaps (consistent with claim on this finite surface)
- GWR-last rate overall: 14.2% — super-signal cases are a subset of twin gaps, not a general placement predictor

Artifact: `research/remainders/correlations/investigation/super_signal_status.json`

**Open questions (G2):** Exhaustive `4+ zeros ⟺ w ≡ 0 (mod 30)` case analysis; replace informal Step 3 language; harden or reclassify.

---

## Lane 3 — Endpoint residue state (`q mod 30`, `q mod p`)

**Role:** Compress next-prime search — carry endpoint residues, OR certification masks, skip wheel-open composites.

**Status:** Strong operational results documented in hourly frontier; mask prototype not committed as repo script.

**Pinned surface** (`research/00-index/docs/algorithmic_frontier_hourly.md`, 2026-04-11):

| Metric | Value |
|--------|-------|
| Regime | 100,000 consecutive gaps, `q ≥ 10¹³` |
| Mask width | 96 wheel-open positions |
| Carried residues | `q mod p` for primes `≤ 37` |
| Chain mismatches | **0** |
| Resolved inside mask | **100%** |
| Small-prime mod checks | 5,145,085 → **0** (99.98% reduction) |
| Miller-Rabin calls | unchanged (444,678) |
| Wall-time speedup | **1.0345×** |

Artifact: `research/remainders/correlations/investigation/endpoint_lane_summary.json`

**Repro note:** Hourly cites `gwr_dni_boundary_state_mask_search.py` (not in tree). Related probes: `research/02-gwr-dni/scripts/gwr_dni_transition_probe.py`.

**Open questions:** Commit mask search script; thread mask into production next-prime path; measure at `10¹⁸`.

---

## Lane 4 — Left-prime `p mod 30` ridge orientation

**Role:** Modulates where within-gap raw-Z peak occurs (left vs right edge).

**Status:** Committed JSON through sampled `10¹⁸`.

**Pinned at `10⁶`** (`research/11-gap-ridge/output/insight_probes/residue_mod30_right_edge_share.json`):

| `p mod 30` | Gaps | Right-edge share | Lift vs global |
|------------|------|------------------|----------------|
| Global | 70,327 | 0.160 | 1.00× |
| 13 | 9,824 | 0.252 | **1.58×** |
| 23 | 9,839 | 0.209 | **1.30×** |
| 11 | 7,074 | 0.093 | 0.58× |
| 17 | 7,075 | 0.087 | 0.54× |

Artifact: `research/remainders/correlations/investigation/mod30_ridge_lane_summary.json`  
Findings doc: `research/11-gap-ridge/docs/findings/residue_mod30_ridge_orientation.md`

**Repro:**
```bash
python research/11-gap-ridge/scripts/insight_probes.py
# see residue_mod30_right_edge_share output under research/11-gap-ridge/output/insight_probes/
```

**Open questions:** Link ridge orientation to interior `R(n,M)` marginals conditioned on `p mod 30`.

---

## Lane 5 — State-budget residue-matched cells

**Role:** Test whether adding `p_n mod 30` (and prev gap width) to matched transition cells changes square-vs-tail decisiveness.

**Status:** Pinned summary for powers 12–18.

**Pinned results** (`research/05-state-budget/output/state_budget_residue_matched_pair_summary.json`):

| Match mode | Decisive pairs | Signed advantage (square_ruler) | Advantage share | Verdict |
|------------|----------------|-----------------------------------|-----------------|---------|
| base | 589 | +73 | 0.124 | unresolved |
| **mod30** | **230** | **+40** | **0.174** | unresolved |
| mod30_prev_gap | 35 | +15 | 0.429 | unresolved |

Artifact: `research/remainders/correlations/investigation/state_budget_lane_summary.json`

**Repro:**
```bash
python research/05-state-budget/scripts/state_budget_residue_matched_pair_test.py
```

**Open questions:** Whether residue matching is signal or cell fragmentation; extend decisive-pair count.

---

## Lane 6 — RSA backward modulus/remainder search

**Role:** After backward lane entry, search closure laws as `(modulus_value, target_remainder)` pairs over gap-width and offset invariants.

**Status:** Toy corpus `N ≤ 5000`, 980 cases.

**Pinned results** (`research/06-cryptology-rsa/output/semiprime_branch/pgs_semiprime_backward_invariant_closure_search_summary.json`):
- Invariant laws tested: 8 (`containing_gap_mod_n`, `left_offset_mod_entry`, …)
- **Factor-reach recall: 0.0** on all laws
- Primary failures: `entry_not_lane` (733), `no_entry_candidate` (158)

Super-Signal moduli `(2,3,5,7,30,210,2310)` used in cryptology docs as search geometry — inherits Lane 2 epistemic ambiguity.

Artifact: `research/remainders/correlations/investigation/rsa_lane_summary.json`

**Repro:**
```bash
python research/06-cryptology-rsa/scripts/pgs_semiprime_backward_invariant_closure_search.py \
  --max-n 5000 \
  --output-dir research/06-cryptology-rsa/output/semiprime_branch
```

---

## Placement-correlation synthesis (interior lane)

**Gap-length proxy (`g`):** Remainder entropy of `vec[:6]` is essentially deterministic in `g` for `g ≤ 114` (Spearman ≈ 1.0). Not a useful predictor beyond trivial uniqueness.

**Prime-placement proxies:**
- `distance_to_next_prime` at interior points: MI with `num_zeros` ≈ **0.06** — quantified null.
- GWR-last flag: **14.2%** baseline at `p≤10⁶`; echo hypothesis does not sharpen this (falsified in `CORRELATION_REPORT.md`).
- Super-Signal at GWR: **100%** co-occur with `g=2` on measured 1e6 surface (2,697 cases).

---

## Gap-echo hypothesis (falsified)

Source: `research/remainders/correlations/CORRELATION_REPORT.md`

- Tiny + 1e6 (`g ≤ 114`): **0** gaps with late `vec[:6]` repeats.
- 50 large real gaps (`g ≈ 480–1442`): **100%** have echoes, **0%** GWR-last.
- Conclusion: echoes, when possible, associate with GWR *earlier*, opposite of "memory selects winner."

---

## Downstream index (pattern / correlation mining)

### Entry commands

```bash
# Full multi-lane pull (interior stream + cross-lane JSON extract)
python research/remainders/run_investigation.py \
  --output-dir research/remainders/correlations/investigation

# Descriptive correlation on any JSONL
python research/remainders/correlation_analysis.py \
  --records research/remainders/output/tiny_val/raw_records.jsonl \
  --out research/remainders/correlations/tiny_verify

# Interior collection (scale)
python research/remainders/collect_remainder_stats.py \
  --max-p 1000000 \
  --output-dir research/remainders/output/1e6/
```

**Python version:** 3.13.0 (pinned in investigation `RUN_LOG.json`)

### Artifact paths

| Path | Contents |
|------|----------|
| `research/remainders/REMAINDER_LANES_SYNTHESIS.md` | This document |
| `research/remainders/run_investigation.py` | Multi-lane orchestrator |
| `research/remainders/correlation_analysis.py` | MI, Spearman, marginals, repeat stats |
| `research/remainders/output/1e6/raw_records.jsonl` | Interior records (921,503 lines) |
| `research/remainders/output/1e6/summary.json` | Marginals + gap counts |
| `research/remainders/output/1e6/RUN_LOG.md` | Collection repro log |
| `research/remainders/output/tiny_val/raw_records.jsonl` | Validation set (490 records) |
| `research/remainders/correlations/investigation/interior_1e6_placement_stats.json` | Placement stats at scale |
| `research/remainders/correlations/investigation/placement_correlation_table.md` | Summary table |
| `research/remainders/correlations/investigation/endpoint_lane_summary.json` | Endpoint mask rates |
| `research/remainders/correlations/investigation/mod30_ridge_lane_summary.json` | Ridge orientation rates |
| `research/remainders/correlations/investigation/state_budget_lane_summary.json` | Residue-matched cells |
| `research/remainders/correlations/investigation/rsa_lane_summary.json` | Backward invariant search |
| `research/remainders/correlations/investigation/super_signal_status.json` | Epistemic status pointer |
| `research/remainders/correlations/investigation/RUN_LOG.json` | Investigation metadata |
| `research/remainders/correlations/CORRELATION_REPORT.md` | Echo falsification + tiny analysis |
| `research/remainders/correlations/tiny_verify/descriptive_stats.json` | Tiny-set correlation run |
| `research/11-gap-ridge/output/insight_probes/residue_mod30_right_edge_share.json` | Full ridge scales |
| `research/05-state-budget/output/state_budget_residue_matched_pair_summary.json` | State-budget cells |
| `research/06-cryptology-rsa/output/semiprime_branch/pgs_semiprime_backward_invariant_closure_search_summary.json` | RSA invariants |

### Tests

```bash
python -m pytest research/remainders/test_remainder_utils.py -q
python -m pytest research/remainders/test_run_investigation.py -q
```

---

## Suggested downstream mining targets

1. **Conditioned marginals:** `R(n,M)` histograms split by `p mod 30` and `g` bin on 1e6 JSONL.
2. **GWR-last uplift:** Test whether `coprime_to_210` or `dist_nearest_zero_mod30` shifts GWR-last rate above 14.2%.
3. **Cross-lane join:** Merge ridge orientation labels (`p mod 30`) onto interior records via left endpoint `p`.
4. **Super-Signal audit:** Independent recount of `g=2` ⟺ 4+ zeros at GWR on disjoint `p` range.
5. **Large-gap echo regime:** Collector run targeting gaps with `g ≥ 210` only.

---

**End of synthesis.**