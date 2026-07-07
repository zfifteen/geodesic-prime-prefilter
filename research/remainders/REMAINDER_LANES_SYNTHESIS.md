# Remainder Lanes Synthesis — Multi-Lane Investigation Report

**Date:** 2026-07-07 (revised)  
**Investigation runner:** `research/remainders/run_investigation.py`  
**Python:** 3.13.0 (see `correlations/investigation/RUN_LOG.json`)

PGS framing: all statistics below are **measured on named regimes**. They do not establish theorems, redefine GWR, or choose the next prime `q`.

### Gap-count semantics (canonical)

The collector walks consecutive left primes `p` from 2. Two counts are reported:

| Field | Meaning |
|-------|---------|
| `gaps_with_interiors` | Left primes that emitted ≥1 interior record (canonical for analysis) |
| `prime_walk_steps` | Prime-walk steps including empty-interior gaps (e.g. `p=2` twin → 0 records) |

At `p≤10⁶`: **78,497** gaps with interiors, **78,498** prime-walk steps (one empty twin at `p=2`).  
At `p≤1.5×10⁶`: **114,154** gaps with interiors (meets ≥10⁵ threshold).

---

## Executive summary

| Lane | Role | Data status | Strongest measured signal |
|------|------|-------------|---------------------------|
| Interior `R(n,M)` | Gap-interior coordinate | **Scaled ≥10⁵** (114,154 gaps, 1,385,850 records at `p≤1.5×10⁶`) | MI(`num_zeros`, dist) **0.057**; GWR-last **13.9%** |
| GWR Super-Signal | Termination claim at GWR | **Epistemic open** (G2) | All 3,842 super-signal GWR cases are `g=2` on 1.5e6 surface |
| Endpoint `q mod` | Search acceleration | **Fresh probe** + hourly reference | 5,000-gap `q mod 30` sample from `q≥10¹³`; mask artifact 100% in-window |
| Left-prime `p mod 30` ridge | Peak-side modulation | **Fresh probe** + pinned JSON | Fresh probe at `p≤5×10⁴`; pinned `p≡13` lift 1.58× at `10⁶` |
| State-budget residue cells | Matched-pair tests | **Re-run collector** | `mod30`: 230 decisive pairs, +40 advantage (unresolved) |
| RSA backward modulus/remainder | Closure search | **Re-run collector** | 0% factor-reach on toy `N≤5000` |

**Gap-echo hypothesis:** Falsified — `research/remainders/correlations/CORRELATION_REPORT.md`.

---

## Lane 1 — Interior remainder vectors `R(n, M_v1)`

**Repro (scaled surface):**
```bash
python research/remainders/collect_remainder_stats.py \
  --max-p 1500000 \
  --output-dir research/remainders/output/1.5e6/
```

**Pinned counts** (`research/remainders/output/1.5e6/summary.json`):

| Field | Value |
|-------|-------|
| `gaps_with_interiors` | **114,154** |
| `prime_walk_steps` | 114,155 |
| `gaps_empty_interiors` | 1 |
| `records_emitted` | **1,385,850** |

**Placement correlations** (`interior_placement_stats.json`, full 1.5e6 stream):

| Proxy | Metric | Value |
|-------|--------|-------|
| Prime placement | GWR-last rate | **0.1386** (15,824 / 114,154 gaps) |
| Termination | MI(`num_zeros`, `dist_to_next` binned) | **0.0568** (normalized 0.0498) |
| Gap length | Spearman(entropy, `g`) | **1.0000** |
| GWR signature | Avg zeros (GWR − gap avg) | **−0.670** |
| Super-Signal | GWR with 4+ zeros, all `g=2` | **3,842** cases |

Legacy `p≤10⁶` surface: 78,497 gaps with interiors, 921,503 records (`output/1e6/`).

---

## Lane 2 — GWR Super-Signal (epistemic only)

Theorem-stack: **measured · corollary**. Open items: `docs/proof-enhancements/goals.md` G2.

On **1.5e6** measured surface: 3,842 GWR records with 4+ zeros; **all** in `g=2` gaps.

---

## Lane 3 — Endpoint residue state

**Fresh measurement:** `lane_collectors/endpoint_residue_probe.py` — 5,000 gaps from `p=10,000,000,000,037`, writes `endpoint_residue_probe_fresh.json`.

**Reference artifact:** hourly frontier — 96-open mask, 100% in-window at `10¹³`, 99.98% small-prime mod reduction.

```bash
python research/remainders/lane_collectors/endpoint_residue_probe.py \
  --start-p 10000000000037 --max-gaps 5000 \
  --output research/remainders/correlations/investigation/endpoint_residue_probe_fresh.json
```

---

## Lane 4 — Left-prime `p mod 30` ridge

**Fresh measurement:** `lane_collectors/mod30_ridge_probe.py`

```bash
python research/remainders/lane_collectors/mod30_ridge_probe.py \
  --max-p 50000 \
  --output research/remainders/correlations/investigation/mod30_ridge_probe_fresh.json
```

**Pinned long-scale:** `research/11-gap-ridge/output/insight_probes/residue_mod30_right_edge_share.json` — `p≡13 (mod 30)` right-edge lift **1.58×** at `10⁶`.

---

## Lane 5 — State-budget residue-matched cells

Re-run via investigation (`--run-slow-lanes`) or:

```bash
python research/05-state-budget/scripts/state_budget_residue_matched_pair_test.py
```

`mod30` decisive pairs: **230**, signed advantage **+40**, verdict **unresolved**.

---

## Lane 6 — RSA backward modulus/remainder

```bash
python research/06-cryptology-rsa/scripts/pgs_semiprime_backward_invariant_closure_search.py \
  --max-n 5000 --output-dir research/06-cryptology-rsa/output/semiprime_branch
```

980 cases; **0%** factor-reach recall on all invariant laws.

---

## Investigation orchestrator

`run_investigation.py` executes lane collectors (subprocess), streams interior JSONL, writes summaries:

```bash
python research/remainders/run_investigation.py --run-slow-lanes
# fast test path:
python research/remainders/run_investigation.py --skip-lane-execution \
  --interior-jsonl research/remainders/output/tiny_val/raw_records.jsonl
```

---

## Downstream index

| Path | Contents |
|------|----------|
| `research/remainders/REMAINDER_LANES_SYNTHESIS.md` | This document |
| `research/remainders/run_investigation.py` | Multi-lane orchestrator |
| `research/remainders/lane_collectors/endpoint_residue_probe.py` | Fresh endpoint probe |
| `research/remainders/lane_collectors/mod30_ridge_probe.py` | Fresh ridge probe |
| `research/remainders/output/1.5e6/raw_records.jsonl` | Scaled interior (≥10⁵ gaps) |
| `research/remainders/output/1.5e6/summary.json` | Collector summary |
| `research/remainders/output/1e6/` | Legacy 78,497-gap surface |
| `research/remainders/correlations/investigation/interior_placement_stats.json` | Placement stats |
| `research/remainders/correlations/investigation/endpoint_residue_probe_fresh.json` | Fresh endpoint data |
| `research/remainders/correlations/investigation/mod30_ridge_probe_fresh.json` | Fresh ridge data |
| `research/remainders/correlations/investigation/RUN_LOG.json` | Lane subprocess log |
| `research/remainders/correlations/CORRELATION_REPORT.md` | Echo falsification |

**Tests:** `python -m pytest research/remainders/test_remainder_utils.py research/remainders/test_run_investigation.py -q`

---

**End of synthesis.**