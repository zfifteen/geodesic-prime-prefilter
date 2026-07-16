# Direction 1: Bounded-gap interior atlas (probe contract)

**Collab:** PGS × sieve research directions (2026-07)  
**Owner this slice:** Hermes  
**Status of direction:** **measured on R0** (not verified). Not theorem.
**Parent:** `CHARTER.md`

---

## Plain object

Start from known consecutive primes `(p, q)`. When the gap `q − p` is at most a fixed bound `H`, walk the **interior** of the open interval `(p, q)` with PGS primitives (divisor field / GWR / selected witness `w`) and record where the leftmost min-divisor structure sits. Compare that geometry to a control sample of typical (larger) gaps in the same magnitude band.

This is a **measurement atlas**, not a sieve infinitude claim and not a generator rewrite.

---

## PGS-first frame

```text
ordered prime gap (p,q) -> interior divisor field -> GWR / selected w
  -> compression / placement features -> measured table or unresolved probe state
```

**Allowed:**
- Input primes as ordered endpoints (catalog / known consecutive primes).
- Interior scans using project DNI/GWR/chamber primitives already in repo.
- Control sampling of non-bounded gaps for comparison.

**Forbidden as inference:**
- Sieve weights choosing `w` or residual class.
- Primality APIs (`isprime`, MR) to pick the next prime for the atlas (primes are **inputs**).
- Product / gcd gates as the reasoning path.
- Claiming Zhang–Maynard H validates PGS compression (or the reverse).

Classical bounded-gap results only label **which gaps we sample** when we want an H from that literature (e.g. 246 as a historical comparison scale). They do not promote atlas rows to theorems.

---

## Named regime (conservative first ladder)

| Rung | Regime | Role |
| --- | --- | --- |
| R0 | Consecutive primes with **p ≤ 10^6** | Local implement / debug |
| R1 | **p ≤ 10^7** | First meaningful control vs bounded subpopulation |
| R2 | Optional later: decade anchors including higher powers | Only after R0–R1 green; still **not** “verified” without 10^18 surface |

**Default implement first:** **R0**, then R1 if R0 is clean.

Program-level **verified / validated** language is **forbidden** on this family until an executed **10^18** surface exists for the atlas claim class (AGENTS.md). R0/R1 results are **measured on regime R** only.

---

## H list (gap size filters)

Primary fixed H values (inclusive on `gap = q − p`):

| H | Rationale |
| --- | --- |
| **246** | Classical comparison scale (Zhang–Maynard lineage); sampling label only |
| **600** | Mid band between tight classical scale and larger Cramér-scale typical gaps |
| **1000** | Loose fixed cap for denser “small gap” cohort |

Optional secondary (do not block R0):

| Band | Rule |
| --- | --- |
| Dynamic | `gap ≤ c · (log p)^2` for a fixed small menu `c ∈ {1, 2}` once log scale is stable in code |

Each row is tagged with which H-filter(s) it satisfies. A gap can satisfy multiple H caps.

---

## Exact output columns

One CSV/JSONL row per consecutive pair `(p, q)` retained by a filter (or control sampler):

| Column | Type | Meaning |
| --- | --- | --- |
| `p` | int | Left prime endpoint |
| `q` | int | Right prime endpoint |
| `gap` | int | `q − p` |
| `w` | int or null | Selected interior witness under named GWR/DNI rule; null if unresolved |
| `d_w` | int or null | Divisor count `d(w)` if `w` resolved |
| `offset` | int or null | `w − p` |
| `compression` | float or null | Project compression ratio as defined in generator/proof surface (document exact formula in repro header; do not invent a new one) |
| `square_flag` | bool | Whether square-boundary / U_square-style feature fires on this gap (if project primitive exists; else false + note “feature not wired”) |
| `h_filters` | string | e.g. `H246|H600` which caps the gap meets |
| `cohort` | enum | `bounded` \| `control` |
| `regime` | string | e.g. `R0_p_le_1e6` |
| `status` | enum | `resolved` \| `unresolved` \| `skipped` |
| `notes` | string | short residual/unresolved code if any |

**No** confidence fields, primality labels, or sieve scores in the primary stream.

---

## Control sample (typical gaps)

**Goal:** compare interior geometry when `gap ≤ H` vs when gaps are **typical** at the same magnitude.

**Definition (R0/R1):**
1. Universe: all consecutive prime pairs with `p` in the regime.  
2. Bounded cohort: `gap ≤ H` for each H in the primary list (separate views or multi-tag).  
3. Control cohort: pairs with `gap > H_max` where `H_max = 1000` for the fixed-H program, **matched by decade or log-bin of p** so control is not all large primes vs all tiny primes.  
4. Per log-bin of `p`, sample **min(N_bin, N_control_cap)** control pairs uniformly (default `N_control_cap = 256` per bin) so tables stay small.  
5. Never use sieve density to reweight the control; uniform-in-bin over consecutive pairs is enough for measured-on-R.

---

## Success / fail falsifiers

**Success (probe design holds; measured language only on regime R):**
- Pipeline emits complete rows for ≥99% of bounded pairs in R0 with explicit `resolved`/`unresolved`.  
- Bounded vs control distributions of `offset` / `compression` (when resolved) are reportable with exact counts.  
- No classical gate appears in the selection of `w`.

**Fail / redesign triggers:**
1. **K-D1a:** GWR/`w` selection is undefined or systematically unresolved on a large fraction of small-gap interiors (atlas empty → redesign interior rule wiring, not invent sieve fallback).  
2. **K-D1b:** “Bounded” and “control” cohorts are confounded by magnitude (no log-bin matching) so any difference is size, not gap class.  
3. **K-D1c:** Implementation uses primality/sieve to choose `w` or next prime → contract violation; scrap run.  
4. **K-D1d:** Prose claims twin-prime / constellation infinitude or that H=246 “proves” compression → invalid claim path; do not promote.

**Non-goals (explicit):**
- Not proving infinitely many gaps ≤ H.  
- Not replacing Zhang–Maynard.  
- Not a residual-cell RSA closer.  
- Not Super-Signal.

---

## Repro sketch (PGS primitives only for interior)

1. **Inputs:** consecutive prime list for regime R (precomputed catalog acceptable; treating primes as data, not as PGS inference).  
2. For each pair `(p, q)`:  
   - Compute `gap = q − p`.  
   - Tag H-filters.  
   - If bounded or sampled control: run **existing** project GWR/DNI interior selection on integers in `(p, q)` (same code path as generator interior diagnostics where available).  
   - Fill columns; if selection does not resolve, `status=unresolved`, leave `w` null.  
3. Emit JSONL + one-page measured summary with regime, counts, and **no** verified language.  
4. Optional audit: classical primality of endpoints only as **downstream audit** of the input catalog, never as atlas inference.

**Suggested path for code later (not this deliverable):** thin harness under  
`experiments/pgs-sieve-research-directions-collab-2026-07/d1_atlas/`  
calling shared PGS modules; do not fork a sieve engine.

---

## Relation to other directions

| Dir | Link |
| --- | --- |
| D2 | Constellation/admissible hits are a **different sampling set**; do not mix into D1 rows without a separate cohort tag |
| D3 | Sieve weights never enter D1 columns |
| D4 | Compression column is the PGS-side object; gap size H is classical comparison only |
| D5 | Out of scope for this probe |

---

## What the lead still needs

- Agy: D4 bridge + DIRECTIONS grid  
- Claude: kill shapes + D2/D3/D5 scoping  
- Principal/lead later: green light to implement R0 only after peer package is complete

**Hermes deliverable status:** probe contract complete (this file). Implementation run is **not** claimed here.

STATUS: done  
FOR: @grok  
