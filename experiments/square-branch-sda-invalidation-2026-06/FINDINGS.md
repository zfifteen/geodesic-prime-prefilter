# Square-Branch Advancement — June 19, 2026

## Executive Summary

The bounded dynamic cutoff theorem remains **unresolved on the square branch**.
This session extended the falsification surface to **5.17M prime roots through
`r = 299,999,977`** and found **no counterexample**. The new extremal row sits at
**72.1% cutoff utilization** (`r = 251,066,071`, offset `540`), higher than the
prior segment peak of **67.8%**.

A PGS-native structural probe **invalidates** transferring the proved d=4
Short-Divisor-Average (SDA) left-arrival route to the square branch: on all three
segment extremal rows, the prefix before the first interior prime square has
**minimum divisor count 4**, not 5, and the weaker τ≥4 SDA inequality does not
bind at the observed offsets.

The direct next-prime theorem and Interior Maximizer Theorem remain **proved**
(`PROOF.md`). Only the prime-square proximity obligation

```text
D(r) = r^2 - P(r^2) <= max(64, ceil(0.5 * log(r^2)^2))
```

on the selected-square branch is still open.

---

## 1. Context (Grok share alignment)

Shared conversation title: **PGS Next-Prime Theorem Unresolved**.

Repository reading:

- **Proved:** direct deterministic next-prime rule; Interior Maximizer Theorem.
- **Unresolved:** square-branch proximity theorem blocking all-scale bounded
  dynamic cutoff (`PROOF.md` §Square-Branch Reduction;
  `research/04-bounded-compression/docs/square_branch_blocker_acceptance.md`).

The share link did not expose full transcript (client-rendered page). This
session advanced the exact obligation named in repository handoff artifacts.

---

## 2. Measured Result — Extended Falsification Segment

**Command:**

```text
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 200000001 \
  --max-prime 300000000 \
  --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_2e8_3e8
```

**Outcome:**

| Field | Value |
| --- | --- |
| Prime roots tested | `5,173,388` |
| First counterexample | `none` |
| Max utilization | `0.7209612817089452` |
| Extremal root `r` | `251,066,071` |
| Offset `D(r)` | `540` |
| Dynamic cutoff `C(p)` | `749` |
| Elapsed | `80.8 s` |

**Cumulative utilization frontier (segment maxima):**

| Segment | Extremal `r` | Offset | Utilization |
| --- | ---: | ---: | ---: |
| `3 .. 10^8` | `82,357,433` | `540` | `0.8120` |
| `10^8 .. 2·10^8` | `102,017,779` | `462` | `0.6784` |
| `2·10^8 .. 3·10^8` | `251,066,071` | `540` | `0.7210` |

**Interpretation (measured, not theorem):** utilization is **not monotone
decreasing** in `r`; offset `540` reappears as a sharp row at multiple scales.
All observed utilizations remain **strictly below 1**.

**Artifacts:**

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_2e8_3e8/square_branch_dynamic_cutoff_search_summary.json`
- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_2e8_3e8/square_branch_dynamic_cutoff_search_frontier.csv`

---

## 3. Invalidated Route — d=4 SDA Transfer to Square Branch

**Command:**

```text
python3 experiments/square-branch-sda-invalidation-2026-06/square_branch_prefix_tau_floor_probe.py
```

**PGS frame:** chamber interior before first interior prime square `r^2`; divisor-count
field `τ(n)`; backward distance `D(r)`.

**Finding on all three segment extremal rows:**

| Quantity | Value |
| --- | --- |
| Selected-square branch (`s^2 < p < r^2`) | `true` on all rows |
| Prefix minimum `τ` | `4` (never `5`) |
| First `τ=4` offset | `2`, `6`, `10` |
| First `τ=3` offset (= observed offset) | `462`–`540` |
| τ≥5 SDA route transfers | **false** |
| τ≥4 SDA binds at observed offset | **false** |

**Why this matters (PGS-native):** In the d=4 GWR branch, the carrier is the
**first** interior `τ=4` point, so the prefix enforces `τ ≥ 5` and the proved
SDA lemma compresses left arrival. In the square branch, `τ=3` prime squares are
the carrier class, so the prefix only enforces `τ ≥ 4`; early `τ=4` semiprimes
sit between the left endpoint and the first prime square. The weaker τ≥4 SDA
inequality does not force `τ ≤ 4` (hence does not force a prime square) by the
observed offsets.

**Status:** **Invalidated proof route** (not a counterexample to the proximity
theorem itself).

**Artifact:** `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`

---

## 4. Unresolved Obligation (unchanged)

The live theorem target remains:

```text
For every selected-square branch gap with first interior prime square r^2,
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

The square-branch band bound `D(r) < (r-s)(r+s)` from GWR characterization is
**proved** but does not compress to the `2 log(r)^2` scale (measured band
bounds at extremal rows exceed `10^9` while cutoffs are `O(log(r)^2)`).

---

## 5. Next Valid Research Steps

1. **Falsification:** continue deterministic segments (`3·10^8 .. 4·10^8`, …) until
   first counterexample or a new utilization envelope stabilizes.
2. **Theorem pressure:** target `D(r)` directly on the selected-square branch —
   not via d=4 SDA porting or residue-only finite covers.
3. **Structural audit:** explain recurring offset `540` and early-`τ=4` / late-`τ=3`
   separation as a PGS chamber geometry object (hypothesis until formalized).

---

## 6. Status Separation

| Claim | Label |
| --- | --- |
| Direct next-prime theorem | **proved** (`PROOF.md`) |
| Interior Maximizer Theorem | **proved** (`PROOF.md`) |
| No counterexample through `r <= 3·10^8` | **measured** |
| Max utilization `0.721` at `2·10^8..3·10^8` | **measured** |
| d=4 τ≥5 SDA closes square branch | **invalidated** |
| Prime-square proximity theorem | **unresolved** |
| All-scale bounded dynamic cutoff | **unresolved** (square branch) |