# Proof path (Hermes) — Package T0 and residual B

**Status:** proof-support sketch. **No `PROOF.md` edit.**  
**Primary package:** T0 = A1 + A2 + C1 from locked `CANDIDATE_STATEMENT.md`.

---

## 1. What already exists in `PROOF.md` (do not re-prove as “new pillars”)

| Stack item | Use for T0 |
| --- | --- |
| Direct next-prime / `d(n)=2` endpoint | Supplies that consecutive prime gaps are the ambient objects; T0 does not restate next-prime |
| GWR leftmost min-`d` maximizer theorem | **Defines** `w` under H3; T0 assumes that definition |
| Universal bounded compression + PSP | Orthogonal: `δ` vs `q`. Cite only to keep dual objects clean |
| Finite base certificates (`gwr_finite_base_v1`, etc.) | Not required for A1/A2 finite arithmetic, but available if a write-up wants explicit small primes checked |

**Import that is classical and already used in the project stack:** `τ` multiplicativity / prime-power divisor formulas as needed for evaluating `d` on small explicit interiors (same class of imports already flagged in PROOF hygiene).

---

## 2. Package T0 — lemma map

### Lemma T0.0 (nonempty interior for `g ≥ 2`, `p ≥ 3`)

If `p ≥ 3` and `g ≥ 2`, then `I ≠ ∅`.  
**Proof sketch:** `|I| = g − 1 ≥ 1`.  
**Exception:** gap `(2,3)` has empty interior; exclude or handle as empty-H3 case (no `w`).

### Theorem T0.A1 (twin gap lock)

**Statement:** under H0–H3 with `g = 2`, `w = p + 1` and `δ = 1`.

**Proof sketch:**
1. `I = {p + 1}` by definition of gap 2.  
2. The unique element of `I` is the unique candidate for leftmost min-`d`.  
3. Hence `w = p + 1`, `δ = 1`.  

**Dependence:** definition of GWR on a singleton set (instance of GWR theorem / definition).  
**Nature:** finite / definitional. **No** measured premise.

### Corollary T0.C1

Under the same hypotheses, the witness is left-adjacent and right-adjacent simultaneously (`δ = 1 = g − 1`).  
**Proof:** immediate from A1.

### Theorem T0.A2 (gap-four offset trichotomy)

**Statement:** under H0–H3 with `g = 4`, `I = {p+1,p+2,p+3}` and `δ ∈ {1,2,3}` with `w` the leftmost min-`d` element of `I`.

**Proof sketch:**
1. Interior cardinality 3 is arithmetic.  
2. GWR returns some `w ∈ I`, so `δ = w − p ∈ {1,2,3}`.  
3. Uniqueness of the leftmost minimizer is exactly the GWR selection rule already in `PROOF.md`.  

**Optional sharpening (not required for T0):** for odd `p > 2`, `p+1` and `p+3` are even, hence `d(p+1), d(p+3) ≥ 3` if composite (always even >2), while `p+2` is odd; often `w = p+1` or a comparison of `d` on the three points. A full residue-class case split is **nice-to-have**, not blocking for the trichotomy statement.

**Dependence:** H0–H3 + GWR definition.  
**Nature:** finite arithmetic + definition. **No** R0/R1 premise.

---

## 3. What is **not** proved here (Part B and optional A3/C2)

| Claim | Proof status | Path if pursued |
| --- | --- | --- |
| B1 stochastic monotone in `g` | **unresolved** | Would need a measure on gaps + analytic or sieve comparison; high classical-drift risk; keep hypothesis |
| B2 saturation constant `C` | **unresolved** | Must not pin `C = 4` from R0/R1; any proof must define “typical” and avoid UBC confusion |
| A3 catalog for `g ≤ 10` | open / optional | Finite but combinatorial; can be a separate lemma series |
| C2 frequencies for `g = 4` | open / measured | Enumeration possible for small `p`; asymptotics are harder |

**Shape warning:** Part B motivated by continuous offset-vs-gap plots on R0/R1 must stay **hypothesis**. Measured means ~4–4.5 are **not** theorem constants.

---

## 4. Recommended proof write-up order (after human greenlight)

1. Freeze T0 statements exactly as in `CANDIDATE_STATEMENT.md` Package T0.  
2. Write T0.A1 + T0.C1 in conventional mathematical prose (half page).  
3. Write T0.A2 trichotomy (half page); optional even/odd refinement as Remark.  
4. Add a one-paragraph “relation to UBC” remark: T0 is gap-local exact; UBC is `q`-scale worst-case.  
5. Human promotion process only → then `PROOF.md` append under a new short section, without touching measured tables as premises.

---

## 5. Hermes recommendation

**Promote only Package T0** as the “new theorem” unit from this collab.  
Keep B1/B2 as a **named research hypothesis** linked to the D1 atlas, not as co-promoted text.

STATUS: done  
FOR: @grok  
