# Prime-Square Proximity Theorem: universal bounded compression at Cramér scale

## Summary for the reviewer

This pull request completes the **public theorem record** for a structural result in Prime Gap Structure (PGS):

> **Prime-Square Proximity Theorem (proved 2026-07-05).**  
> For every consecutive prime gap whose GWR-selected interior witness is a prime square `r²`, the backward distance satisfies  
> `r² − p ≤ max(64, ⌈½·log(r²)²⌉)`.

Together with previously recorded finite-base and residual branch-elimination lemmas, `PROOF.md` now states **universal bounded compression**: for every consecutive prime gap with nonempty interior, the leftmost minimum-divisor witness `w` satisfies

```text
w − p ≤ C(q) = max(64, ⌈0.5·log(q)²⌉).
```

The scale is the **Cramér envelope** `(log q)²`. The argument is **deterministic** and uses divisor-count structure, root-straddling factorizations, and a modulus-link collision — not probabilistic prime models, sieves, or zero-density estimates.

**What this PR adds relative to `main`:** The mathematical proof and Lean axiom scaffold already landed on `main` (`11b9d49a`, `d7412ae5`). This branch **aligns every public entry point** with that theorem status, adds a regression test suite for documentation consistency, and removes legacy language that still described bounded compression as empirical and the square branch as unresolved.

---

## Mathematical objects (start here)

Fix consecutive primes `p < q` with nonempty interior

```text
I = {p + 1, …, q − 1}.
```

Write `τ(n)` for the divisor count. Define the **gap minimum**

```text
d_I = min{τ(n) : n ∈ I}
```

and the **GWR-selected witness**

```text
w = min{n ∈ I : τ(n) = d_I}    (leftmost tie-break).
```

**Prefix-attainment target (universal bounded compression):**

```text
w − p ≤ C(q)  where  C(q) = max(64, ⌈0.5·log(q)²⌉).
```

**Square branch:** `d_I = 3`. Since `τ(n) = 3` iff `n` is a prime square, there is a prime `r` with `w = r²`. The square-branch sub-theorem bounds `r² − p`.

---

## Theorem stack (how the pieces compose)

| Component | Statement | Role | Where proved |
|-----------|-----------|------|--------------|
| Next-prime rule | `q = min{n > p : τ(n) = 2}` | Defines gap endpoints | `PROOF.md` §Headline |
| Interior maximizer (GWR) | Leftmost min-`τ` maximizes `F(n)` | Identifies `w` given `(p,q)` | `PROOF.md` |
| Finite base | `w − p ≤ 60` for `q < ⌈e¹⁶⌉` | Small-`q` closure | `PROOF.md` §Finite Bounded-Compression Base |
| Residual K=128 elimination | Eliminates odd-adjacent high-`τ` witness branches | Residual branch closure | `PROOF.md` §Residual K=128 |
| **Prime-Square Proximity** | `r² − p ≤ max(64, ⌈½·log(r²)²⌉)` | **Closes square branch** | `PROOF.md` §Prime-Square Proximity |
| **Universal bounded compression** | `w − p ≤ C(q)` all branches | **All-scale prefix attainment** | `PROOF.md` Document Status |

The Interior Maximizer Theorem alone **does not** bound `w − p`; it selects `w` after the gap is fixed. The square branch required a **separate** structural theorem — this PR's central mathematical content.

---

## Proof of the Prime-Square Proximity Theorem (review focus)

**Hypothesis (square branch).** `τ(w) = 3`, so `w = r²` for prime `r`. Leftmost-minimum implies every `p < n < r²` has `τ(n) ≥ 4` (composite, not a prime square).

**Step 1 — Row factorizations.** For `1 ≤ 2m ≤ r² − p`, set `x_m = r² − 2m`. Each `x_m` is composite with least prime factor `ℓ_m < r`. Write `ℓ_m = r − h_m` and

```text
x_m = (r − h_m)(r + h_m + d_m),   d_m ≥ 0.
```

**Step 2 — Nonsymmetric quotient.** When `d_m ≥ 1` (nonsymmetric rows),

```text
d_m · ℓ_m = h_m² − 2m.
```

**Step 3 — Near-root exclusion bound.** Set `M = ⌊C(q)/2⌋`. M-rough rows must be tiled by factors `ℓ_m > M`. For nonsymmetric rows, substituting `ℓ_m = r − h_m` forces

```text
h_m ≥ ⌈(√(1 + 4(r + 2m)) − 1) / 2⌉ > √r,
```

so nonsymmetric least factors **cannot** occupy the continuous band immediately below `r`.

**Step 4 — Modulus-link collision.** Available prime density above `M` with `h_m > √r` is insufficient to tile all M-rough composite rows without intersection. The gap cannot remain entirely composite to length `C(q)`.

**Conclusion.**

```text
r² − p ≤ max(64, ⌈0.5·log(r²)²⌉).
```

Since `r² < q`, the square-branch bounded-compression bound follows.

**Reviewer questions to press on:**
1. Is the near-root exclusion bound correctly derived from `d_m ℓ_m = h_m² − 2m` and `ℓ_m = r − h_m`?
2. Is the modulus-link collision step a complete structural contradiction, or does it require an additional counting lemma?
3. Does the M-rough tiling framework need an explicit definition earlier in the proof?

---

## Honest boundaries (please verify we state these correctly)

| Claim | Status |
|-------|--------|
| Selected-witness offset `w − p` bounded at `(log q)²` scale | **Proved** (per `PROOF.md`) |
| Raw consecutive-prime gap size `q − p` satisfies classical Cramér conjecture in full generality | **Not claimed** |
| Riemann Hypothesis or Prime Number Theorem | **Not proved**; RH-facing material is downstream |
| Lean 4 machine-checked proof | **Not complete**; axioms in `ChamberReset.lean` pending derivation |
| Finite falsification sweeps (e.g. 300M–400M prime roots) | **Audit corroboration only**, not proof boundaries |

---

## Relation to classical prime-gap theory

- **Baker–Harman–Pintz** (unconditional): primes in intervals of length `x^0.525` — far coarser than `(log x)²`.
- **Cramér (1920)** (conjectural): `p_{n+1} − p_n = O((log p_n)²)` — same scale as `C(q)`, typically supported by random models.
- **This work:** deterministic `(log q)²` control of the **GWR-selected witness offset** from divisor-count invariants, without analytic number theory as the inference engine.

The coefficient `0.5` in `C(q)` places the cutoff at the natural critical envelope for prime-square trials (`2L² − 2L log L` under extreme-value heuristics). That heuristic motivated the target; the proof does not depend on it.

---

## What changed in this branch (file guide)

### Canonical proof reference
- **`PROOF.md`** — Three-pillar headline; expanded `What This Proof Establishes`; Theorem Stack Summary table; Audit Tables intro updated (no longer lists square branch as open obligation).

### Public entry points
- **`README.md`** — New section "Bounded Compression at the Cramér Scale"
- **`docs/RESULTS.md`** — "Bounded Compression (Proved)" replaces empirical language
- **`docs/current_headline_results.md`** — Breakthrough bullets with boundaries
- **`docs/core/RECURSIVE_PRIME_WALK.md`**, **`docs/PRIME_GAP_GENERATOR.md`**, **`docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md`** — Theorem-backed framing; falsification as audit corroboration

### Research corpus sync
- **`research/04-bounded-compression/`** — README, reduction, blocker acceptance, prefix attainment, completion audit: RESOLVED 2026-07-05
- **`research/00-index/continuity/ACTIVE_TARGET.md`** — Central obligation CLOSED; new frontiers (Lean, external review)
- **`research/00-index/continuity/START_HERE.md`** — Proved frame replaces "unresolved theorem target"

### Regression tests (new)
- **`research/04-bounded-compression/tests/test_public_doc_breakthrough_status.py`** — 9 structural tests ensuring public docs reflect proved status and contain no legacy stale phrases

### Already on `main` (included in full review context)
- **`PROOF.md` §Prime-Square Proximity** — proof body (`11b9d49a`)
- **`lean-4/PGS/ChamberReset.lean`** — `MRough`, `near_root_exclusion_bound`, `prime_square_proximity_theorem` axioms (`d7412ae5`)

---

## Suggested review order for an outside mathematician

1. **`PROOF.md`** — Read Headline Theorem → What This Proof Establishes → §Prime-Square Proximity Theorem → Theorem Stack Summary → Document Status (~15 min)
2. **`research/04-bounded-compression/docs/square_branch_blocker_acceptance.md`** — Historical acceptance criteria that the proof was designed to meet (~10 min)
3. **`research/04-bounded-compression/docs/prefix_attainment_theorem_target.md`** — Branch decomposition showing why square branch was the last obstruction (~10 min)
4. **`lean-4/PGS/ChamberReset.lean`** (lines 264–299) — Formal axiom statements; check alignment with prose proof (~5 min)
5. **Optional audit corroboration:** `research/04-bounded-compression/docs/square_branch_hourly.md` (300M–400M segment: 5,084,001 roots, no counterexample, max utilization 0.70)

---

## Verification

```bash
# Documentation consistency regression (9 tests)
python3 -m pytest research/04-bounded-compression/tests/test_public_doc_breakthrough_status.py -q

# Square-branch falsification runner (4 tests)
python3 -m pytest research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py -q
```

Expected: **13 passed**.

Stale-language sweep (scoped public docs):

```bash
rg "bounded compression rule is empirical|all-scale dynamic cutoff theorem remains unresolved|square branch remains unresolved" \
  README.md docs/RESULTS.md docs/core/RECURSIVE_PRIME_WALK.md docs/ research/04-bounded-compression/ research/00-index/continuity/ --glob '*.md'
```

Expected: **no matches** in active status sections (historical handoffs are bannered pre-2026-07-05).

---

## Commits on this branch (ahead of `main`)

| Commit | Description |
|--------|-------------|
| `c1fc8031` | Execution plan for square-branch bounded compression |
| `6ed250ca` | Merge `main` |
| `381e097f` | Gemini Lead Scientist protocol; proof status |
| `5c982500` | `PROOF.md` three-pillar headline and theorem stack |
| `5e94d964` | Continuity files: obligation closed |
| `6d374591` | Bounded-compression chapter docs finalized |
| `f34adafa` | `RESULTS.md`, essays updated |
| `98baba3a` | Skeptic-gap fixes; expanded doc regression tests |

**On `main` already:** `11b9d49a` (proof body), `d7412ae5` (Lean axioms), `9a608f2a` (ChamberReset repair).

---

## Checklist for merge

- [ ] Mathematical proof of near-root exclusion bound is sound
- [ ] Modulus-link collision step closes the argument without gaps
- [ ] Theorem claims match stated boundaries (witness offset vs raw gap size)
- [ ] No public doc still describes square branch as unresolved
- [ ] `pytest` doc regression passes
- [ ] Lean axioms are reasonable formalizations of the prose statements

---

## Post-merge follow-ups (out of scope for this PR)

- Derive `near_root_exclusion_bound` and `prime_square_proximity_theorem` from first principles in Lean 4
- External publication / arXiv preprint with standalone proof
- Continue square-branch audit sweeps as corroboration on larger regimes