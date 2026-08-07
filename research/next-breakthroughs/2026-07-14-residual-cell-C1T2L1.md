# Residual cell C1T2L1 separates false mutual geometry from true closure geometry

**Date:** 2026-07-14 (V3 update 2026-08-07)  
**Package path:** `research/next-breakthroughs/2026-07-14-residual-cell-C1T2L1.md`  
**Related rsa-v3 run:** `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/residual_cell_C1T2L1/`  
**V3 resolve package:** `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/residual_discriminator_v2/`

**PGS frame:**  
PGS objects -> PGS invariants -> PGS rule or law -> resolved | unresolved | invalidated

**Claim class:** (B) residual subclass migration, then (A) measured resolve under V3

**Bound words:** verified/validated **absent** (no residual-family `10^18` surface).

## Objects

Start at a locked public modulus-link pair with lower/upper chamber-reset certificates.
Read GWR carrier, first-tail offset, lock offset, and gap widths from those certificates.
Floor-transport the carrier and first-tail through public `N`. Rank the three public
transport residuals. Name the joint residual cell. Emit structural certificate only
when the full GWR stack holds or when V3 carrier reciprocal closure holds; otherwise
emit a named unresolved residual.

## Mechanism (ordinary language first)

Dual-gap discriminator D already cleared the old 50-bit carrier residual
(`delta_c=30 ≤ boundD=45`). The sequential stack then stopped at first-tail fail
(`delta_t=-22`) and treated that as the whole residual story.

That was incomplete. On the same residual row, carrier is still **loose relative to
the STEP2 tight band** (`delta_c=30 > 20` while D holds), and lower lock is **weak**
(`lock=6` in `gap=24`). True mutual-closure geometry (64-bit STEP2 pin) is tight on
all three axes: `delta_c=14`, `delta_t=-5`, lock dominant, pinch sum `S=21`.

The residual vector

```text
R = (r_carrier, r_tail, r_lock)
```

and cell id `C1T2L1` make that joint geometry the V2 decision residual. Pinch sum
`S = 54` on the false class vs `S = 21` on the true class is recorded as a public
diagnostic.

**V3 (2026-08-07):** carrier reciprocal closure finds public pair `(32047633, 32059651)`
with `N//L == U` and `N//U == L`, remainder 6170868, deadline=tail signatures match,
historical false class blocked. Emitted under `resolved_by_carrier_reciprocal_closure`.
Status: measured-on-regime-only / hypothesis. Not a theorem. Not a factorisation claim.

## Formal residual map (hypothesis)

```text
r_carrier = 0 if delta_c <= 20
            1 if 20 < delta_c <= boundD
            2 if delta_c > boundD

r_tail    = 0 if delta_t in [-12, 6]
            1 if delta_t in [-21, -13]
            2 if delta_t <= -22 or delta_t >= 7
            -1 if deadline != tail / empty tail

r_lock    = 0 if 2*lock > gap
            1 if 2*lock <= gap and lock >= gap//4
            2 if lock < gap//4
            -1 if missing

cell = C{r_carrier}T{r_tail}L{r_lock}

When sequential residual would be first_tail AND cell is C1T2L1:
  decision residual = unresolved_by_joint_cell_C1T2L1

V3: when carrier reciprocal floor pair satisfies boundD + deadline=tail + anti-admission:
  resolved_by = carrier_reciprocal_closure
```

## Status separation (HARD)

| Lane | Status | Exact claim text | Evidence / bound |
| --- | --- | --- | --- |
| theorem | n/a | No PROOF.md change. No new universal claim. | PROOF.md untouched |
| implementation | implementation | rsa-v3 GWR stack implements residual_vector_R, joint residual code, and V3 carrier reciprocal probe. | `gwr_carrier_closure.py`, `residual.py`, `residual_discriminator_v2/` |
| measured | measured | On rsa-v3 regression fixtures: 40-bit public endpoint class; 50-bit V2 residual C1T2L1; 50-bit V3 measured resolve under carrier reciprocal closure. | `residual_discriminator_v2/`, DOCUMENTATION_LOCK_50BIT_V3.md |
| hypothesis | hypothesis | Residual cell R as a general residual law beyond the named fixtures remains hypothesis. | — |
| measured resolve (V3, 2026-08-07) | measured-on-regime-only | `rsa_v2_50bit_static_001` V2 residual was `unresolved_by_joint_cell_C1T2L1`; V3 emits `resolved_by_carrier_reciprocal_closure` endpoint_class=[32047633,32059651]. | residual_discriminator_v2/ |

### 10^18 evidence gate

| Field | Value |
| --- | --- |
| Executed 10^18 surface? | no |
| Claim strength used | measured on regression fixtures only |

## Explicit limits

- Regime R = rsa-v3 regression fixtures (40-bit, 50-bit) plus STEP2 arithmetic pins for 64-bit TP cell C0T0L0.
- No PROOF.md edit in this package: yes.
- No classical gates in inference: yes.
- First-tail fixed window unchanged: yes.

## Next pressure

1. Expand residual cell R to additional public mutual-closing ladder states.
2. Keep 50-bit honesty (no window widen, no classical smuggle); V3 measured resolve path is recorded under residual_discriminator_v2/; integrate into live resolver when ready.
3. Do not promote residual cell R into PROOF.md without human-approved proof process.
