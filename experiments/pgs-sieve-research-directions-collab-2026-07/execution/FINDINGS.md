# FINDINGS — PGS × sieve execution collab (R0)

**Date:** 2026-07-15  
**Epoch:** pgs-sieve-execution-2026-07  
**Collab status:** **done**  
**Claim language:** measured on R0 only. Not verified. Not theorem. PROOF.md untouched.

## Done bar

| # | Requirement | Result |
| --- | --- | --- |
| 1 | D1 R0 measured | **met** — 78,498 pairs, p≤10⁶, 100% resolved; `d1_atlas/` |
| 2 | D1 analysis | **met** — continuous gap bins (hermes + lead ANALYSIS) |
| 3 | Kill adjudication | **met** — `KILL_ADJUDICATION_R0.md` (claude) |
| 4 | D4 measured link | **met** — `D4_MEASURED_LINK.md` (agy) |
| 5 | D2 pilot or hard defer | **met** — deferred with K2-b / gap-match blocker until R1 |
| 6 | D3 / D5 | **met** — both deferred (K3-d; D1 redesign wait) |
| 7 | FINDINGS + next residual | **this file** |

## What was measured (R0)

- Interior via `gwr_next_gap_profile` (divisor field, leftmost min-d). Primes catalog = input only.
- Max consecutive gap at p≤10⁶: **114**. Fixed H∈{246,600,1000} tags **all** rows; `gap>1000` control **empty**.
- Within-log-bin quartile reclass: small-gap offset mean **~2.0** vs large-gap **~4.0**; compression means **~0.024** vs **~0.048**.
- Continuous gap bands (hermes): mean offset climbs ~1→4 as gap goes 2→20+, then plateaus near ~4.
- Empty interior: **1** / 78,498 (p=2).
- UBC floor **64** dominates compression ratios at this magnitude.

## Kill adjudication (claude, accepted)

| Shape | Verdict | Note |
| --- | --- | --- |
| K1-a | **PASS** | Gradient exists; not null atlas |
| K1-b | **REDESIGN** | Drop H-primary; continuous gap-width + log-bin quartiles |
| K1-c | **REDESIGN** | Compression claim needs larger p where log² term competes with floor 64 |
| K1-d | **PASS** | Empty interior not dominant |
| K1-e | **REDESIGN (partial)** | Small-gap endpoint concentration is real; add left/right/genuine-interior subclass |

**No kill.** Three recoverable redesigns. Live D1 success criterion becomes: continuous gap-width stratification with within-log-bin controls; H labels historical only; endpoint subclass on small gaps.

## Dual bounds (D4)

Zhang–Maynard gap-size i.o. and PGS witness compression remain **non-implying** duals. R0 measures local offset/compression geometry only; it does not prove infinitude of small gaps and does not promote Super-Signal.

## Deferred (with owners for later)

- **D2:** blocked until R1 gap-percentile controls exist (constellation anchors confounded by small gaps). Written defer: `d2_pilot/DEFER.md`.
- **D3:** K3-d — sieve weight object not stably defined.
- **D5:** wait until D1 redesign is stable at a higher rung.

## Residual next step (outside this closed collab)

**D1 R1 (or decade sample)** with default control mode **quartile** (`run_d1_atlas.py --control-mode quartile`), optional p around 10⁷–10⁹ as cost allows, to (1) retest continuous offset story, (2) reduce UBC-floor dominance on compression ratios, (3) unlock D2 gap-matched controls.

## Peer map

| Peer | Delivery |
| --- | --- |
| hermes | `HERMES_D1_QA.md` |
| agy | `D4_MEASURED_LINK.md` + DIRECTIONS/D1 status |
| claude | `KILL_ADJUDICATION_R0.md` + D2/D3/D5 deferrals |
| lead | R0 run, ANALYSIS, harness, FINDINGS |

## Non-claims

No verified/validated language. No RSA/RH. No Super-Signal. No theorem promotion.
