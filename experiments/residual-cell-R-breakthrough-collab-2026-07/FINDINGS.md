# Findings: residual cell R breakthrough collab

**Updated:** 2026-07-14  
**Collab status:** **done** (lead declared; peer Claude returns failed empty, slices absorbed)

## Status labels

| Layer | Label |
| --- | --- |
| Next-prime / GWR / UBC / PSP | **theorem** (`PROOF.md`, untouched) |
| Residual cell R, pinch S, joint C1T2L1 | **hypothesis** residual map |
| 50-bit vs 64-bit unit pin separation | **measured** on those pins |
| Constant-gaming H2′ (boundD grid) | **measured** on unit pin (boundD retune cannot clear first-tail) |
| E2e resolver residual emission | **measured** on regression fixtures (40 + 50 bit) |
| RSA solve / twin primes | **non-claim** |

## Object

Public residual ranks and pinch (rsa-v3 `gwr_carrier_closure.py`):

- `R = (r_carrier, r_tail, r_lock)` → cell `C*T*L*`
- `pinch_S = |T_c - upper.anchor| + |delta_t|`
- Decision residual subclass: `unresolved_by_joint_cell_C1T2L1` when stack hits first-tail fail and cell is C1T2L1

## Measured pins

| Pin | Cell | pinch_S | Stack / residual |
| --- | --- | --- | --- |
| 50-bit false | C1T2L1 | 54 | unresolved joint cell |
| 64-bit true | C0T0L0 | 21 | holds (close) |

## E2e resolver (lead, this round)

Command:

```bash
python3 research/06-cryptology-rsa/experiments/live-solver/rsa-v3/run_resolver.py \
  --cases research/06-cryptology-rsa/experiments/live-solver/rsa-v3/fixtures/regression_cases.jsonl \
  --output-dir experiments/residual-cell-R-breakthrough-collab-2026-07/output/resolver_run
```

| Case | bits | residual_code | endpoint_class_emitted |
| --- | --- | --- | --- |
| rsa_v2_40bit_static_001 | 40 | null | true |
| rsa_v2_50bit_static_001 | 50 | `unresolved_by_joint_cell_C1T2L1` | false |

Histogram (measured only): `unresolved_by_joint_cell_C1T2L1: 1`.  
50-bit residual vector on disk: `cell=C1T2L1;r=(1,2,1);pinch_S=54;delta_c=30;delta_t=-22`.  
Artifacts: `output/resolver_run/{summary,residuals,inference_rows,...}`.

## Lead checks

```bash
python3 -m pytest research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_unit.py -q
# 12 passed
python3 -m pytest research/06-cryptology-rsa/experiments/live-solver/rsa-v3/test_h2_constant_sweep.py -q
# 38 passed (boundD grid anti-gaming; real assertions)
```

## Charter bar (1–5)

| # | Requirement | Status |
| --- | --- | --- |
| 1 | Named geometry joint cell + pinch | met (code + continuity) |
| 2 | Separation true close vs false pin | met (64 vs 50 unit; 40 resolve vs 50 residual e2e) |
| 3 | Anti-gaming H2′ | met (38 green) |
| 4 | Taxonomy/ledger residual on resolver path | met (e2e residual_code) |
| 5 | No theorem / RSA-solve inflation | held |

Kill shapes: `KILL_SHAPES.md` (lead absorbed Claude slice). No kill landed on checked pins.

## Peer delivery summary

| Peer | Delivery |
| --- | --- |
| hermes | ACTIVE_GOAL joint-cell pin; taxonomy string match (RESIDUAL_TAXONOMY / residual.py / inventory); FINDINGS continuity polish; unit recheck 12 green (python3.13) |
| agy | Unit re-confirm 12 green; prediction checklist residual boxes + scope lock (`experiments/pgs-prediction-inventory-2026-07/CHECKLIST.md`); decade ladder isolated from this track. Lead e2e still in collab `output/resolver_run/` |
| claude | empty returns (rc=1); kill shapes absorbed by lead |

Note: checklist “expand fixtures” stays optional follow-on, outside the closed collab done-bar.

## Continuity pin

`research/00-index/continuity/notes/ACTIVE_GOAL_50bit_residual_discriminator.md`  
records decision residual `unresolved_by_joint_cell_C1T2L1` with first-tail as underlying fail.

## What this is (plain)

A **genuine residual-map advance**: the 50-bit obstruction is no longer a vague  
“first-tail fail.” It is a named joint cell with public ranks, a pinch score, a  
decision residual code on the live resolver path, and measured separation from a  
true close. That is progress on residual honesty geometry.

## What remains outside this collab

- Broader true-close corpus for K1 strength (optional next research).  
- Residual-family `10^18` surface before any verified/validated program language.  
- Optional pinch threshold law (hypothesis only).  
- RSA-scale solve: still **unresolved** and out of scope here.
