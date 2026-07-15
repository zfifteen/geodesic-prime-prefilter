# Collab charter: residual cell R breakthrough

**Shared goal:** Convert the live public residual geometry into a **named, joint residual cell map** that honestly separates false structure from true close candidates without constant gaming, classical smuggling, or theorem inflation.

**Lead:** grok  
**Peers:** hermes, claude, agy  
**Status of this collab:** open until lead declares done

## What already exists (measured / hypothesis — not theorem)

Code: `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/gwr_carrier_closure.py`

- Integer residual ranks `R = (r_carrier, r_tail, r_lock)` → cell label `C*T*L*`
- Pinch sum `S = |T_c − upper.anchor| + |T_tail − upper.anchor|` (public floor transport only)
- 50-bit false pin: cell **C1T2L1**, `pinch_S = 54`, residual migrates to `unresolved_by_joint_cell_C1T2L1`
- 64-bit true close: cell **C0T0L0**, `pinch_S = 21`, stack holds
- Unit suite: 12 passed (`test_a1_endpoint_resolver_unit.py`)

This is the **candidate breakthrough object**: joint residual cells + pinch, not dual-gap retune and not first-tail window widen.

## Success bar for “genuine breakthrough” (this collab)

All required:

1. **Named geometry** of the 50-bit obstruction as joint cell + pinch (done in code; needs continuity writeup).  
2. **Separation property** on ≥ one true close vs ≥ one false pin without classical fields (done on 50 vs 64 unit pins; expand).  
3. **Anti-gaming:** constant-neighborhood / H2′ sweep does not turn C1T2L1 into a silent close.  
4. **Taxonomy + ledger** emit joint residual code on resolver path; anti-admission still holds.  
5. **No** theorem promotion, no RSA-solve claim, no verified language without residual-family 10^18.

Optional stretch (only if 1–5 green): propose **one** new public geometric law for first-tail rank that is not a free window enlarge (hypothesis only).

## Forbidden

- Widening first-tail to admit delta=-22  
- Closing 50-bit by boundD / α only  
- gcd / isprime / product as inference  
- Twin primes, RH, Rowland engines as “breakthrough” substitutes  

## Artifacts target

```text
experiments/residual-cell-R-breakthrough-collab-2026-07/
  CHARTER.md          (this file)
  FINDINGS.md         (lead+team synthesis)
  output/             (sweeps, fixture reruns)
```
