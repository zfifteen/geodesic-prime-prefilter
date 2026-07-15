# Residual cell C1T2L1 separates false mutual geometry from true closure geometry

**Date:** 2026-07-14  
**Package path:** `research/next-breakthroughs/2026-07-14-residual-cell-C1T2L1.md`  
**Related rsa-v3 run:** `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/residual_cell_C1T2L1/`  

**PGS frame:**  
PGS objects -> PGS invariants -> PGS rule or law -> resolved | unresolved | invalidated

**Claim class:** (B) residual subclass migration  

**Status labels in this file:** theorem | implementation | measured | audit | hypothesis | unresolved | invalidated  

**Bound words:** verified/validated **absent** (no residual-family `10^18` surface).

## Objects

Start at a locked public modulus-link pair with lower/upper chamber-reset certificates.
Read GWR carrier, first-tail offset, lock offset, and gap widths from those certificates.
Floor-transport the carrier and first-tail through public `N`. Rank the three public
transport residuals. Name the joint residual cell. Emit structural certificate only
when the full GWR stack holds; otherwise emit a named unresolved residual.

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

and cell id `C1T2L1` make that joint geometry the decision residual. Pinch sum
`S = 54` on the false class vs `S = 21` on the true class is recorded as a public
diagnostic.

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
```

## Status separation (HARD)

| Lane | Status | Exact claim text | Evidence / bound |
| --- | --- | --- | --- |
| theorem | n/a | No PROOF.md change. No new universal claim. | PROOF.md untouched |
| implementation | implementation | rsa-v3 GWR stack implements residual_vector_R and joint residual code `unresolved_by_joint_cell_C1T2L1`. | `gwr_carrier_closure.py`, `residual.py`, `RESIDUAL_TAXONOMY.md` |
| measured | measured | On rsa-v3 regression fixtures (40-bit + 50-bit): 40-bit still public endpoint class; 50-bit residual migrates first-tail -> joint cell C1T2L1 with R=(1,2,1), pinch_S=54. | `output/residual_cell_C1T2L1/` |
| audit | n/a | No classical audit required for this residual subclass claim. | — |
| hypothesis | hypothesis | Residual cell R as a general residual law beyond the named fixtures remains hypothesis. | falsifiers in RESULT.md |
| unresolved | unresolved | `rsa_v2_50bit_static_001` remains unresolved under `unresolved_by_joint_cell_C1T2L1`. | residuals.jsonl |
| invalidated | none | — | — |

### 10^18 evidence gate

| Field | Value |
| --- | --- |
| Executed 10^18 surface? | no |
| Form / path | none |
| Claim strength used | measured on regression fixtures only |

## Why this is a residual breakthrough (and what it is not)

**It is:** a new public residual cell that separates measured false mutual geometry
from measured true mutual geometry without classical gates, without window widen,
and without reopening dual-gap D. Live residual decision name changed with tests
and a committed package.

**It is not:** a theorem; a 50-bit residual close; an RSA-scale resolver; a revival
of historical z≥4⇒g=2 claim; a Reciprocal Transport Law on continuous DNI excess.

The rejected claim packaging in `2026-07-14-grok-heavy.md` (theorem inflation,
historical z≥4⇒g=2 claim foundation, empty evidence) remains rejected.

## Repro

```bash
python3 research/06-cryptology-rsa/experiments/live-solver/rsa-v3/run_resolver.py \
  --cases research/06-cryptology-rsa/experiments/live-solver/rsa-v3/fixtures/regression_cases.jsonl \
  --output-dir research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/residual_cell_C1T2L1

python3 -m pytest \
  research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_unit.py \
  research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_adversarial.py \
  research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_regression.py \
  research/06-cryptology-rsa/tests/test_a1_certificate_verifier.py \
  research/06-cryptology-rsa/tests/test_a1_review_defects.py -q
```

## Explicit limits

- Regime R = rsa-v3 regression fixtures (40-bit, 50-bit) plus STEP2 arithmetic pins for 64-bit TP cell C0T0L0.
- No PROOF.md edit in this package: yes.
- No classical gates in inference: yes.
- First-tail fixed window unchanged: yes.

## Next pressure

1. Expand residual cell R to additional public mutual-closing ladder states (64-bit live runner, 128/256 missing-cert remains separate).
2. Keep 50-bit honest unresolved; pressure joint geometry only with public fields.
3. Do not promote residual cell R into PROOF.md without human-approved proof process.

## QA closing gate

**Review plan:**
1. Claim alignment: residual subclass, not theorem
2. Status table complete
3. historical z≥4⇒g=2 claim not used as foundation
4. 10^18 gate matches claim words
5. Repro commands match artifacts
6. 40-bit control + ADV-001 honesty
7. Diff discipline

**Outcome:**

| Criterion | Result | Fix |
| --- | --- | --- |
| Claim alignment | Pass | — |
| Status separation | Pass | — |
| Forbidden phrases | Pass | — |
| 10^18 gate | Pass | — |
| Reproducibility | Pass | package + pytest |
| PGS frame | Pass | — |
| Path discipline | Pass | — |
