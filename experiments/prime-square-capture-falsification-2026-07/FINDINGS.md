# Prime-Square Hierarchical Capture — Falsification Report

**Date:** 2026-07-06  
**Regime:** `p < 2·10^6` full gap scan (148,931 interiors) + three square-branch extremal rows at `~10^16–10^17`

## Executive Summary

**The Core Insight is not falsified on mechanism, bypass, or boundary-utilization frontier. It is partially falsified on one loose reading of “worst-case class,” and it remains untested at record-gap scale for the decoupling claim.**

On every gap where an interior prime square is the unique `τ=3` integer, GWR selects that square and ignores earlier `τ=4` composites. At the measured utilization frontier through `2·10^6`, the top 20 rows are all square-branch captures. At extremal square-branch rows (offsets 462–540), prefixes contain 52–63 semiprimes (`τ=4`) before the square, confirming that long offsets are not explained by local absence of small-factor composites.

The insight survives as a **proved local selection consequence** of the Interior Maximizer Theorem whenever `τ=3` is gap-minimal. What remains open is whether **global** worst-case cutoff pressure is *exclusively* square-branch at scales where wide non-square gaps exist.

---

## PGS Frame

| Object | Role in test |
| --- | --- |
| Gap interior `I = {p+1,…,q−1}` | Chamber under test |
| Divisor-count field `τ(n)` | Selection input |
| GWR witness `w` | Leftmost interior argmin `τ(n)` |
| Prefix offset `w − p` | “Depth” into gap |
| Dynamic cutoff `C(q) = max(64, ⌈0.5·log(q)²⌉)` | Boundary ruler |
| Interior prime square `r²` | Proposed capture carrier |

---

## Falsification Matrix

| Claim | Test | Result | Status |
| --- | --- | --- | --- |
| **C1** Unique interior `τ=3` forces GWR = prime square | 223 gaps with interior square at `p < 2·10^6`; 3 extremal rows | 0 failures | **Not falsified** |
| **C2** Long square offsets bypass early `τ=4` tiling | Extremal rows + square gaps with offset ≥ 24 | First `τ=4` at offsets 2–10; GWR at 462–540; 52–63 `τ=4` before `w` | **Not falsified** |
| **C3** Worst-case *utilization* belongs to square class | Top 20 by `offset/C(q)` at `2·10^6` | 20/20 square-branch | **Not falsified** (utilization sense) |
| **C3′** Worst-case *raw offset ranks* are square-dominated | Top 100 by raw offset at `2·10^6` | 37 square, 62 `τ=4`, 1 other | **Partially falsified** (ranking sense) |
| **C4** Non-square gaps cannot match square extremes | Max offset 60 (square) vs 24 (`τ=4`); max utilization 0.615 vs 0.261 | No `τ=4` gap exceeds square frontier | **Not falsified** (`p < 2·10^6`) |
| **C5** Decoupled from “compositeness-only” wide gaps | 80 widest record gaps (`10^12+`, width 1284–1442) | All lack interior prime square; GWR offset unreadable here | **Unresolved** |
| **C6** Adjacent-square trivial break | `p=3`, square at `p+1` | Single row; offset 1 | **Consistent** with stated exception |

---

## Measured Evidence

### Standard `τ=4` regime (`p < 2·10^6`)

- `110,947` gaps: GWR is first interior `τ=4`.
- Mean first-`τ=4` offset = **3.75** (= GWR offset): selection is immediate.
- Only **223** gaps contain an interior prime square; each has **unique** `τ=3`.

### Square-capture regime (`p < 2·10^6`)

- All **223** square gaps: `w = r²`, `τ(w)=3`, `capture_mechanism_holds = true`.
- Mean GWR offset **9.85** (vs 3.75 for `τ=4` branch).
- Max offset **60** (square) vs **24** (`τ=4`).
- Max utilization **0.615** (square) vs **0.261** (`τ=4`).

### Extremal square-branch rows (bounded-compression frontier)

| `r` | Offset | Utilization | First `τ=4` | `τ=4` count before `w` |
| ---: | ---: | ---: | ---: | ---: |
| `82,357,433` | 540 | 0.812 | 10 | 63 |
| `102,017,779` | 462 | 0.678 | 2 | 52 |
| `251,066,071` | 540 | 0.721 | 6 | 60 |

Capture and bypass both hold on all three rows.

---

## Interpretation by Claim

### Mechanism (hierarchy, not starvation)

**Supported.** When a prime square sits in the interior and is the unique `τ=3` integer, GWR must select it. This is not a statistical effect; it follows from the proved leftmost minimum-divisor rule.

The extremal rows show dense `τ=4` prefixes (52–63 semiprimes) while GWR remains at the late square. Long offset is therefore **not** caused by local absence of small-factor composites in those cases.

### Prefix distance reframing

**Supported on tested data.** Prefix distance to GWR measures placement of the sparse `τ=3` square, not distance to the nearest dense `τ=4` layer.

### Worst-case boundary pressure

**Supported in utilization sense; weak in raw-rank sense.**

- Utilization frontier (pressure against `C(q)`): top 20 at `2·10^6` are 100% square-branch; global maxima are square-branch.
- Raw offset leaderboard: many `τ=4` gaps appear because offset ≈ first-`τ=4` offset in short gaps — a different quantity than cutoff utilization.

The Core Insight’s phrase “push hardest against theoretical boundary limits” aligns with **utilization**, not raw offset rank. Under that reading, the claim stands on the tested regime.

### Decoupling from extreme compositeness

**Supported to `2·10^6`; unresolved at record-gap scale.**

No `τ=4` gap in the scan matches square-branch offset or utilization extremes. However, the 80 widest known gaps (`10^12+`, no interior square) are natural adversarial targets once interior `τ` data is available. Falsification of decoupling at that scale is still open.

### Universal / adjacency exception

**Supported.** Unique-`τ=3` capture holds in all 226 tested cases (223 + 3 extremal). The only adjacent-square case in the `2·10^6` scan is `p=3`, `4=p+1`, offset 1 — consistent with the stated trivial break.

---

## Theorem vs Measured vs Hypothesis

| Statement | Label |
| --- | --- |
| GWR = leftmost argmin `τ` in interior | **proved** (`PROOF.md`) |
| `τ=3` iff `n=r²` for prime `r` (for `n>8`) | **classical fact** |
| Square present ⇒ unique interior `τ=3` | **proved arithmetic** |
| Capture selects square over earlier `τ=4` | **proved consequence** of GWR when `min τ = 3` |
| Max utilization frontier is square-only through `2·10^6` | **measured** |
| Max utilization frontier is square-only at all scales | **hypothesis** (open) |
| Wide non-square gaps cannot approach square utilization | **unresolved** at `10^12+` |
| Prime-square proximity / bounded compression | **proved** (`PROOF.md`, 2026-07-05) |

---

## Verdict

| Overall | Detail |
| --- | --- |
| **Core mechanism** | **Survives falsification** |
| **Bypass / not starvation** | **Survives falsification** |
| **Boundary-limit worst cases** | **Survives** (utilization); **weakened** (raw offset rank) |
| **Global decoupling at record-gap scale** | **Unresolved** |

The hierarchical capture picture is the correct local description of GWR behavior when an interior prime square exists. It should not be overstated as “all large offsets are square-branch” without specifying utilization vs raw rank and tested scale.

---

## Reproduction

```bash
python3 experiments/prime-square-capture-falsification-2026-07/prime_square_capture_falsification_probe.py --limit 2000000
python3 experiments/prime-square-capture-falsification-2026-07/square_branch_extremal_capture_probe.py
python3 experiments/prime-square-capture-falsification-2026-07/non_square_large_gap_probe.py
```

**Artifacts:**

- `falsification_summary.json`
- `gap_scan_details.csv`
- `square_branch_extremal_probe.json`
- `non_square_large_gap_probe.json`