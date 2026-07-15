# Active Goal: 50-bit residual honesty (Phase-1 complete + joint cell)

**Updated:** 2026-07-14  
**Status of this note:** operational continuity pin (not a theorem surface)

## Goal (Heavy correct fix)

Harden residual honesty so false public structure stays blocked and residual
names the real geometry. **Do not** make the 50-bit rung emit an endpoint class
by widening first-tail or classical smuggling.

## Phase-1 execution (done)

| Deliverable | Status |
| --- | --- |
| Full GWR component ledger on residual rows | **done** |
| Lock co-primary diagnostics when steps > 0 | **done** |
| Anti-admission of false class `(32047651, 32059633)` | **done** |
| First-tail window not widened | **confirmed** (`delta=-22` still fails) |
| 40-bit control still resolves | **measured** |
| 50-bit still unresolved | **measured** (see joint residual below) |

**Package:** `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/phase1_residual_honesty/`  
**Result note:** `.../phase1_residual_honesty/RESULT.md`  
**Classification:** **(C)** honest unresolved obstruction with joint diagnostics

### 50-bit pin (measured)

Underlying sequential fail remains first-tail hard miss. When residual ranks match
joint cell C1T2L1, the **decision residual migrates** to the taxonomy subclass
(not an endpoint class):

```text
underlying fail: first-tail (delta_t=-22; window not widened)
dual-gap D: holds (delta_c=30 boundD=45 g_lo=24 g_up=14)  [loose under D]
lock dominance: fails (lock=6 gap=24)  [visible in ledger]
residual vector R: (r_carrier=1, r_tail=2, r_lock=1) -> cell C1T2L1
pinch_S: 54  (public floor transport only; measured on this pin)
decision residual: unresolved_by_joint_cell_C1T2L1
```

Contrast (unit true-close pin, measured): cell **C0T0L0**, `pinch_S=21`, stack holds.

Residual cell R + pinch are a **hypothesis** residual map. Fixture separation is
**measured** on named pins only. Not residual-family verified at 10^18. Not RSA solve.

Collab continuity:
`experiments/residual-cell-R-breakthrough-collab-2026-07/`
(CHARTER, FINDINGS, H2 constant-gaming sweep tests).

## Status labels

| Layer | Label |
| --- | --- |
| Dual-gap D / residual laws | **hypothesis** |
| Residual cell R / pinch / C1T2L1 | **hypothesis** map; **measured** on unit pins |
| This fixture package | **measured** |
| 50-bit residual | **unresolved** (joint cell code when ranks match) |
| UBC / PSP / GWR / next-prime | **theorem** (untouched) |
| Historical mutual-closure false class | **invalidated** as factor solve; anti-admitted |

## Code homes

```text
rsa-v3/gwr_carrier_closure.py  :: evaluate, residual_vector_R, joint cell migrate, anti-admission
rsa-v3/residual.py             :: TAXONOMY includes unresolved_by_joint_cell_C1T2L1
rsa-v3/RESIDUAL_TAXONOMY.md    :: same code
rsa-v3/resolver.py             :: residual_component_ledger + emit reject
tests/test_a1_endpoint_resolver_unit.py :: phase1 joint + anti-admission + cell R
rsa-v3/test_h2_constant_sweep.py :: boundD grid anti-gaming (fixed first-tail window)
```

Do **not** edit `PROOF.md` for this work. No verified/validated residual language
without residual-family `10^18`.
