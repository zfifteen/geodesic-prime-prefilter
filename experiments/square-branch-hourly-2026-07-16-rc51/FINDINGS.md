# Offset-540 Structural Audit: RC51–RC53 (Proximity Slack)

**Date:** 2026-07-16  
**Job id:** `offset-540-structural-audit`  
**Status:** residual claims hold (audit only)

## Plain object

Take a selected prime square `w = r^2` and its left prime `q = P(w)`. The
chamber length is the offset `D(r) = w - q`. The square-branch dynamic cutoff
is `C_dyn(q) = max(64, ceil(0.5 · log(q)^2))`, the same budget the
falsification search uses. This package measures:

1. How hard the chamber presses that budget: `u(r) = D / C_dyn`.
2. How much integer headroom remains to the S1* breach line `u = 1`:
   `h(r) = C_dyn - D`.
3. Where high pressure sits relative to historical offset 540 and branch
   marker `o_q`.

Project terms: proximity utilization (RC51), absolute headroom (RC52),
high-pressure locus (RC53).

## Frame

PGS-native objects only:

- selected square endpoint and left prime
- offset `D(r)`
- dynamic cutoff `C_dyn(q)` from the walk helper (matches search)
- utilization `u` and headroom `h`
- Dual / Tau4 multiset retained as prior residual surface only

Not revived: fixed-band near-540 law (RC2 falsified at `D=738`), d=4 SDA.  
Not primary surface: RC48–RC50 MultisetOccupancy (retained).  
Not Dual / density renorms of RC3–RC47.

## New residual claims

| ID | Claim | Bound | Observed (7 unique chambers) | Status |
| --- | --- | --- | --- | --- |
| RC51 / P55 | Proximity utilization | `0.55 ≤ u ≤ 0.98` | range `[0.6075, 0.9342]` | holds |
| RC52 / P56 | Absolute headroom | `45 ≤ h ≤ 350` | range `[52, 314]` | holds |
| RC53 / P57 | High-pressure locus | if `u ≥ 0.85` then `o_q=6` and `\|D−540\| ≥ 150` | sole row: `r=424171123`, `D=738`, `u≈0.934` | holds |

Surface: segment utilization maxima through `4e8–5e8` plus full
`o_q ∈ {2,4,6}` branch-max panel (8 evaluation rows; 7 unique chambers).

| segment | r | D | C_dyn | u | h | o_q |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 3e7–1e8 | 82357433 | 540 | 665 | 0.812 | 125 | — |
| 1e8–2e8 | 102017779 | 462 | 681 | 0.678 | 219 | — |
| 2e8–3e8 | 251066071 | 540 | 749 | 0.721 | 209 | — |
| 3e8–4e8 | 358018553 | 546 | 776 | 0.704 | 230 | — |
| 4e8–5e8 max | 424171123 | 738 | 790 | 0.934 | 52 | 6 |
| o_q=2 | 468917503 | 542 | 798 | 0.679 | 256 | 2 |
| o_q=4 | 482342527 | 486 | 800 | 0.608 | 314 | 4 |

## Relation to prior residual surface

- RC1 / P1–P5 early-τ4 / late-τ3 chamber separation retained (holds).
- RC2 fixed near-540 band retained **falsified** (`D=738`).
- RC48–RC50 multiset occupancy retained (holds; not primary surface here).
- RC51 measures **endpoint budget pressure**, a new object class vs Tau4
  packing / Dual renorms.
- RC53 reads high util as **outside** the historical 540 cluster, consistent
  with RC2 death (not a revival of 540-as-law).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: Target S1* remains **UNRESOLVED**.

```text
S1*  ⇔  ∀ selected-square roots r:  D(r) ≤ C_dyn  ⇔  u(r) ≤ 1
     ⇔  D(r) ∉ Annulus(r)
```

Panel residual envelopes (`u ≤ 0.98` on 7 chambers) are **audit only**. They
do not empty `Annulus(r)` and do not prove universal proximity. Direct
next-prime and Interior Maximizer remain proved.

## Inputs read

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
- prior chamber table `experiments/square-branch-hourly-2026-07-10/`
- RC48 multiset package retained as prior residual surface

## Falsification commands

```text
# Residual panel RC51–RC53 (does not prove S1*)
python3 experiments/square-branch-hourly-2026-07-16-rc51/offset_540_residual_rc51_probe.py

# Target S1* primary holdout (preferred next pressure)
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 500000001 \
  --max-prime 600000000 \
  --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_5e8_6e8
```

## Next pressure

Queue falsification `5e8–6e8` (preferred holdout). Re-check RC51–RC53 and
retained RC48–RC50 on any new util maximum. Do not promote `u` or `h` to
theorem. Do not revive fixed-band 540 or d=4 SDA. Prefer new-band holdout
over further residual minting on the same 7 chambers.
