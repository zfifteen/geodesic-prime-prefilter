# PSP Closure (S1) — Prime-Square Proximity Analytic Gap

**Created:** 2026-07-07  
**Parent:** [../README.md](../README.md) · **Blocker:** [../shortcomings.md](../shortcomings.md) §S1 · **Goal:** [../goals.md](../goals.md) §G1  
**Discussion:** [GitHub #23](https://github.com/zfifteen/prime-gap-structure/discussions/23)

## Objective

Close the modulus-link / tiling collision step in `PROOF.md` (Prime-Square Proximity Theorem, ~lines 604–625) so the bound

```text
r² - p ≤ max(64, ceil(0.5 · log(r²)²))
```

is established by explicit lemmas, not density metaphor. Lean `near_root_exclusion_bound` is proved; `prime_square_proximity_theorem` must consume this chain.

## Proof Spine (Target)

| Step | Lemma | Status |
|------|-------|--------|
| 0 | Square-branch setup (τ(w)=3, earlier τ≥4, r≤p) | **PROVED** — `PROOF.md` lines 587–602 |
| 1 | Row–Factor Assignment | **OPEN** |
| 2 | Symmetric-row cardinality `≤ ⌊√(M/2)⌋` | **OPEN** (sketch in prose) |
| 3 | Near-root exclusion `h_m² + h_m ≥ r + 2m` | **PROVED** — `ChamberReset.lean:280` |
| 4a | Injectivity on M-rough rows | **OPEN** — mechanism agreed in #23 |
| 4b | Explicit pigeonhole bound `\|R\| ≤ π(r−√r) − π(M)` | **OPEN** — counting corollary |
| 4c | Capacity contradiction when `r² − p > C(q)` | **OPEN** |
| 5 | PSP bound assembly | **OPEN** |

## Definitions

### Rows

For consecutive primes `p < q`, square-branch witness `w = r²`, cutoff `C(q) = max(64, ⌈0.5·log(q)²⌉)`, `M = ⌊C(q)/2⌋`, and `m ∈ {1,…,M}` with `2m ≤ r² − p`:

```text
x_m := r² − 2m
```

### Row factorization template

```text
x_m = ℓ_m · (r + h_m + d_m),   ℓ_m = r − h_m,   ℓ_m prime,   h_m ≥ 0,   d_m ≥ 0
```

### Admissible placement

`(ℓ, h, d)` is admissible for row `m` if:

1. `ℓ` prime, `ℓ < r`
2. `x_m = ℓ · (r + h + d)` with `ℓ = r − h`
3. Nonsymmetric: `d ≥ 1`; symmetric: `d = 0` and `2m = h²`

### M-rough row

Row `m` is **M-rough** if every prime divisor of `x_m` is strictly greater than `M`.

### Modulus-link collision

Rows `m₁ ≠ m₂` **collide** if `ℓ_{m₁} = ℓ_{m₂}`.

---

## Lemma 1 — Row–Factor Assignment `OPEN`

**Statement.** Under square-branch hypotheses, each `m ∈ {1,…,M}` admits a unique admissible placement `(ℓ_m, h_m, d_m)`.

**Proof obligations:**

- [ ] Existence from compositeness + root-straddling form (`PROOF.md` 596–600)
- [ ] Uniqueness of `ℓ_m` as least prime factor
- [ ] No row yields τ=3 (links to earlier-integer hypothesis)

**Lean target:** `AdmissiblePlacement` structure in `ChamberReset.lean`

---

## Lemma 2 — Symmetric Coverage `OPEN`

**Statement.** If `d_m = 0` then `2m = h_m²`, hence

```text
#{m ∈ {1,…,M} : d_m = 0} ≤ ⌊√(M/2)⌋
```

**Proof obligations:**

- [ ] From quotient equation `d_m ℓ_m = h_m² − 2m` with `d_m = 0`

---

## Lemma 3 — Near-Root Exclusion `PROVED`

**Statement.** For nonsymmetric M-rough rows: `h_m² + h_m ≥ r + 2m`, hence `h_m > √r`.

**Reference:** `lean-4/PGS/ChamberReset.lean` theorem `near_root_exclusion_bound` (lines 280–346).

**PROOF.md action:** Replace informal derivation at lines 612–616 with named cross-reference only.

---

## Lemma 4a — Injectivity on M-Rough Rows `OPEN`

**Statement.** The map `m ↦ ℓ_m` is injective on the set of M-rough rows in `{1,…,M}`.

**Proof sketch (agreed in Discussion #23):**

1. Each `x_m` is odd (`r` odd prime ⇒ `r²` odd, `2m` even).
2. Rows lie in `[r² − 2M, r² − 2]`; interval width `2M − 2`.
3. If `ℓ | x_{m₁}` and `ℓ | x_{m₂}` with `m₁ ≠ m₂`, both are odd multiples of `ℓ`; minimum separation `≥ 2ℓ`.
4. Therefore `2ℓ ≤ 2M − 2` ⇒ `ℓ < M`.
5. M-rough rows require `ℓ_m > M` — contradiction if two rows share `ℓ`.

**Proof obligations:**

- [ ] Formalize "odd multiples of ℓ" minimum gap `2ℓ`
- [ ] Connect interval width to `m₁, m₂ ∈ {1,…,M}`

**Lean target:** `m_rough_row_injectivity` lemma

---

## Lemma 4b — Explicit Pigeonhole Bound `OPEN`

**Statement.** Let `R` be the set of M-rough rows in `{1,…,M}`. Then

```text
|R| ≤ π(r − ⌈√r⌉) − π(M)
```

where `π(x)` counts primes `≤ x` (or primes in `(M, r − √r)` per near-root upper bound `ℓ_m < r − √r`).

**Proof sketch:**

- Injectivity (4a) ⇒ distinct rows map to distinct primes `ℓ_m`
- Near-root exclusion ⇒ `ℓ_m ∈ (M, r − √r)`
- Count available primes in interval

**Proof obligations:**

- [ ] Prove `ℓ_m < r − √r` from `h_m > √r` and `ℓ_m = r − h_m`
- [ ] State prime-counting bound without classical density language

---

## Lemma 4c — Capacity Contradiction `OPEN`

**Statement.** If `r² − p > C(q)`, then `|R_ns| > π(⌊r − √r⌋) − π(M)`, contradicting Lemma 4b. Hence no such gap exists.

Here `R_ns ⊆ R` is the set of **nonsymmetric M-rough** rows (`d_m ≥ 1`, `ℓ_m > M`).

### Derivation chain (draft)

**Step A — Full row activation.**  
`M = ⌊C(q)/2⌋` and `C(q) ≥ 64` imply `2M ≤ C(q)`. If `r² − p > C(q)`, then `2m < r² − p` for every `m ∈ {1,…,M}`; the active row set has exactly `M` elements.

**Step B — Partition.**  
`L = {m : ℓ_m ≤ M}`, `R = {m : ℓ_m > M}` (M-rough). `|L| + |R| = M`. Lemma 4a gives injectivity `m ↦ ℓ_m` on `R`.

**Step C — Upper bound (Lemma 4b).**  
For `m ∈ R_ns`, near-root exclusion (`h_m > √r`, `ℓ_m = r − h_m`) gives `ℓ_m ≤ ⌊r − √r⌋`. Injectivity ⇒

```text
|R_ns| ≤ π(⌊r − √r⌋) − π(M)
```

**Step D — Lower bound (Sub-lemma 4c.1, `OPEN`).**  
Let `S = #{m : d_m = 0}`. Lemma 2 ⇒ `|S| ≤ ⌊√(M/2)⌋`. Let `T = #{m : ℓ_m ≤ M} = |L|`. Then

```text
|R| = M − |L| = M − T
|R_ns| ≥ |R| − |S| ≥ M − T − ⌊√(M/2)⌋
```

**Sub-lemma 4c.1 (Small-ℓ absorption bound).** When `r² − p > C(q)`, the small-ℓ rows cannot absorb the excess:

```text
T ≤ π(M) + ⌊√(M/2)⌋
```

*Mechanism sketch:* each `ℓ ≤ M` can be the least prime factor of at most `⌈M/ℓ⌉` active rows in the progression `x_m = r² − 2m` (step 2), and symmetric rows consume at most `⌊√(M/2)⌋` additional slots. Summing over `ℓ ≤ M` is double-counting; the tight bound is the **placement saturation** inequality from Phase 2 audit.

**Step E — Contradiction.** Combine Steps C and D:

```text
M − π(M) − 2⌊√(M/2)⌋ > π(⌊r − √r⌋) − π(M)
⟺ M > π(⌊r − √r⌋) + 2⌊√(M/2)⌋
```

When `r² − p > C(q) = 2M` (or `2M+1`), this reduces to a pure counting claim in `(M, r)` with `r < q` and `C(q) = max(64, ⌈0.5·log(q)²⌉)`. **Phase 2 audit** (`audit_square_branches.py`) stress-tests the inequality on worst-case square branches; no counterexample found for `r ≤ 10⁴` (see scratch evidence).

**Proof obligations:**

- [ ] Prove Sub-lemma 4c.1 (small-ℓ absorption) without density language
- [ ] Prove Step E inequality from `r² − p > C(q)` and `r² < q`
- [ ] Replace `π` differences with explicit prime-count bounds if needed for Lean

---

## Theorem — Prime-Square Proximity (Revised) `OPEN`

**Statement.** Under square-branch hypotheses, `r² − p ≤ C(q)`.

**Assembly:** Assume `r² − p > C(q)` ⇒ all rows `m ≤ M` composite ⇒ Row–Factor Assignment ⇒ partition symmetric / M-rough ⇒ Injectivity + Pigeonhole ⇒ contradiction.

**Status after closure:** Theorem stack `proved` (analytic) · `lean-partial` until `prime_square_proximity_theorem` upgraded.

---

## Phase 2 — Empirical Stress Audit `OPEN`

**Purpose:** Falsification probe for counting bound under extreme square-branch gaps.

**Script target:** `docs/proof-enhancements/psp-closure/scripts/audit_square_branches.py`

**Outputs:**

- Worst-case `r² − p` vs `C(q)` for gaps with τ-minimum = prime square
- Least-factor sequences `(ℓ_m, h_m, d_m)` for top stress cases
- Injectivity verification on M-rough rows in sample

**Acceptance:** No counterexample to bound; stress cases document near-saturation of pigeonhole capacity.

---

## PROOF.md Patch Plan (Post-Closure)

1. Insert `### Row–Factor Assignment` after line 602
2. Insert `### Injectivity on M-Rough Rows` and `### Modulus-Link Pigeonhole Bound`
3. Replace lines 618–619 (informal density) with Lemmas 4a–4c
4. Update Document Status footer to note S1 closed
5. Theorem stack: PSP → `proved · universal · lean-partial`

---

## Cross-References

| Artifact | Role |
|----------|------|
| `PROOF.md` lines 575–627 | Live PSP proof (patch target) |
| `lean-4/PGS/ChamberReset.lean` | `MRough`, `near_root_exclusion_bound`, `prime_square_proximity_theorem` |
| `docs/square_branch_theorem_plan.md` | Prior execution plan (Phases 1–4) |
| Discussion #23 comment 17562285 | Row–Factor outline |
| Discussion #23 comment 17562295 | Injectivity + pigeonhole agreement |