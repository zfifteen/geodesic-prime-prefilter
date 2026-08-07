# Active Goal: 50-bit residual honesty → V3 carrier reciprocal resolve

**Updated:** 2026-08-07  
**Status of this note:** operational continuity pin (not a theorem surface)

## Goal (Heavy correct fix)

Harden residual honesty so false public structure stays blocked and residual
names the real geometry. Do not make the 50-bit rung emit an endpoint class
by widening first-tail or classical smuggling.

## Phase-1 + V2 (done)

| Deliverable | Status |
| --- | --- |
| Full GWR component ledger on residual rows | done |
| Lock co-primary diagnostics when steps > 0 | done |
| Anti-admission of false class `(32047651, 32059633)` | done |
| First-tail window not widened | confirmed (`delta=-22` still fails) |
| 40-bit control still resolves | measured |
| V2 sharper residual code | measured: unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54 |

Underlying sequential fail remains first-tail hard miss. Residual ranks match
joint cell C1T2L1:

```text
underlying fail: first-tail (delta_t=-22; window not widened)
dual-gap D: holds (delta_c=30 boundD=45 g_lo=24 g_up=14)
lock dominance: fails (lock=6 gap=24)
residual vector R: (1, 2, 1) -> cell C1T2L1
pinch_S: 54
decision residual (V2): unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54
```

## V3 measured resolve path (2026-08-07)

Carrier reciprocal closure finds a public reciprocal floor pair:

```text
L = 32047633 (GWR carrier_w)
U = N // L = 32059651
N // U returns L exactly
remainder = 6170868
delta_c = 30 ≤ boundD = 45
both reset signatures contain deadline=tail
pair is not the historical false class (32047651, 32059633)
```

Emitted under:

```text
resolved_by = carrier_reciprocal_closure
closure_status = endpoint_class_by_reciprocal_deadline_signature_correction
endpoint_class = [32047633, 32059651]
```

Status: **measured-on-regime-only / hypothesis**.  
Not a theorem. Not a factorisation claim.  
First-tail window remains fixed at [-12, 6].  
No classical gates (no gcd, no modulus selectors, no primality APIs).

Contrast (unit true-close pin): cell C0T0L0, pinch_S=21, stack holds.

## Status labels

| Layer | Label |
| --- | --- |
| Dual-gap D / residual laws | hypothesis |
| Residual cell R / pinch / C1T2L1 | hypothesis map; measured on unit pins |
| V3 carrier reciprocal pair | measured-on-regime-only / hypothesis |
| 50-bit residual | resolved under carrier reciprocal closure (measured) |
| UBC / PSP / GWR / next-prime | theorem (untouched) |
| Historical mutual-closure false class | invalidated as factor solve; anti-admitted |

## Code homes

```text
rsa-v3/residual_discriminator_v2/probe_c1t2l1_v2.py
rsa-v3/residual_discriminator_v2/probe_c1t2l1_v3_resolve.py
rsa-v3/residual_discriminator_v2/CONTINUITY_NOTE.md
rsa-v3/residual_discriminator_v2/RESIDUAL_TAXONOMY_V2_ADDENDUM.md
rsa-v3/output/residual_discriminator_v3_resolve_report.html
rsa-v3/output/DOCUMENTATION_LOCK_50BIT_V3.md
```

Do not edit PROOF.md for this work. No verified/validated residual language
without residual-family 10^18.
