# Active Goal: 50-bit residual honesty (Phase-1 complete)

**Updated:** 2026-07-13  
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
| 50-bit still unresolved | **measured** first-tail residual |

**Package:** `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/phase1_residual_honesty/`  
**Result note:** `.../phase1_residual_honesty/RESULT.md`  
**Classification:** **(C)** honest unresolved obstruction with joint diagnostics

### 50-bit pin (measured)

```text
decision residual: unresolved_by_first_tail_misalignment
dual-gap D: holds (delta=30 boundD=45 g_lo=24 g_up=14)
first-tail: fails (delta=-22)
lock dominance: fails (lock=6 gap=24)  [visible in ledger]
```

## Status labels

| Layer | Label |
| --- | --- |
| Dual-gap D / residual laws | **hypothesis** |
| This fixture package | **measured** |
| 50-bit residual | **unresolved** |
| UBC / PSP / GWR / next-prime | **theorem** (untouched) |
| Historical mutual-closure false class | **invalidated** as factor solve; anti-admitted |

## Code homes

```text
rsa-v3/gwr_carrier_closure.py  :: evaluate (full diagnostics), anti-admission, ledger
rsa-v3/resolver.py             :: residual_component_ledger + emit reject
tests/test_a1_endpoint_resolver_unit.py :: phase1 joint + anti-admission tests
```

Do **not** edit `PROOF.md` for this work. No verified/validated residual language
without residual-family `10^18`.
