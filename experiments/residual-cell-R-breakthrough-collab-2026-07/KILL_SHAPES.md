# Kill shapes: residual cell R / joint C1T2L1

**Author:** lead (`grok`) — absorbs Claude falsify slice after empty collab returns (rc=1).  
**Status labels:** hypothesis residual map; measured on named pins only.  
**Not theorem.** No RSA-solve claim.

## Target claim under pressure

Joint residual cell **C1T2L1** plus decision residual  
`unresolved_by_joint_cell_C1T2L1` is an **honest public residual marker** for the  
50-bit false structure (first-tail fail + loose carrier + weak lock), and it must  
**not** fire as a false-positive residual on a true public close.

## Kill shapes (if any land, the residual map dies or must be redesigned)

| ID | Shape | Evidence checked this collab | Result |
| --- | --- | --- | --- |
| K1 | **C1T2L1 on a true public close** | 64-bit unit pin: cell **C0T0L0**, `pinch_S=21`, stack holds (unit suite) | **Not observed** on known true close pin |
| K2 | **Constant-only / boundD gaming** turns 50-bit into silent endpoint emit | `test_h2_constant_sweep.py` boundD grid: first-tail stays fail; joint cell retained; **38 passed** | **Blocked** (anti-gaming holds on pin) |
| K3 | **Window widen** admits `delta_t=-22` as success | Process rule: forbidden by charter / residual honesty | **Not used** (would be process failure, not breakthrough) |
| K4 | **Residual honesty fail**: constant-only endpoint emit without residual path | Resolver e2e + residual ledger: 50-bit emits decision residual, not endpoint class | **Not observed** |
| K5 | **Ledger / taxonomy miss**: joint cell fails to surface as residual code | e2e `summary.json` + `residuals.jsonl`: `residual_code=unresolved_by_joint_cell_C1T2L1` | **Surfaces correctly** |

## Positive separation (not a kill — supporting measured geometry)

| Pin | Path | Cell / residual | Note |
| --- | --- | --- | --- |
| 40-bit golden resolve | e2e resolver | residual `null`, endpoint class emitted | Clean resolve path |
| 50-bit golden false | e2e resolver | `C1T2L1`, residual `unresolved_by_joint_cell_C1T2L1`, `pinch_S=54`, `delta_t=-22` | Decision residual subclass |
| 64-bit true close | unit pin | `C0T0L0`, `pinch_S=21` | Distinct from C1T2L1 |

E2e package:  
`experiments/residual-cell-R-breakthrough-collab-2026-07/output/resolver_run/`  
(`summary.json`, `residuals.jsonl`, `inference_rows.jsonl`)

## Residual risk (explicit, open after collab)

- True-close **cell geometry** is still thin: one strong unit pin (64-bit).  
  Broader true-close corpus would strengthen K1, not currently a kill.  
- 40-bit resolves without hitting residual ranks; it supports separation of  
  “resolve vs residual” paths, not K1 coverage.  
- Residual map remains **hypothesis** until a residual-family `10^18` surface  
  exists (program rule for verified/validated language).

## Verdict for this collab

No kill shape landed on the checked pins. Joint cell C1T2L1 stands as a  
**measured residual-map object** on the 50-bit obstruction, separated from the  
64-bit true close cell, with H2′ anti-gaming and e2e residual emission green.
