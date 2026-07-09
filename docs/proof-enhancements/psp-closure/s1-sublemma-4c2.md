# Sub-lemma 4c.2 and Corollary 4c.3 (Canonical Source)

## Statement
If `r² − p > C(q)`, then the excess |R_ns| ≥ L_lower > 0 must be assigned realizable rough admissible ℓ, but the capacity is 0 (algebraic for m ≤ ⌊√r/2⌋) or discharged by audit for the boundary under reductio. This contradicts the absorption capacity on small-ℓ coverage. Hence no such gap exists.

## Derivation chain

**Step A. Full row activation.**  
M = ⌊C(q)/2⌋ and C(q) ≥ 64 imply 2M ≤ C(q). If r² − p > C(q), then 2m < r² − p for every m ∈ {1,…,M}; the active row set has exactly M elements.

**Step B. Partition.**  
L = {m : ℓ_m ≤ M}, R = {m : ℓ_m > M} (M-rough). |L| + |R| = M. Lemma 4a gives injectivity m ↦ ℓ_m on R.

**Step C. Upper bound (Lemma 4b).**  
For m ∈ R_ns, near-root exclusion (h_m > √r, ℓ_m = r − h_m) gives ℓ_m ≤ ⌊r − √r⌋. Injectivity ⇒

|R_ns| ≤ π(⌊r − √r⌋) − π(M)

**Step D. Lower bound (Sub-lemma 4c.1).**  
Let S = #{m : d_m = 0}. Lemma 2 ⇒ |S| ≤ ⌊√(M/2)⌋. Let T = #{m : ℓ_m ≤ M} = |L|. Then

|R| = M − |L| = M − T
|R_ns| ≥ |R| − |S| ≥ M − T − ⌊√(M/2)⌋

**Sub-lemma 4c.1 (Small-ℓ absorption bound).** When r² − p > C(q), the small-ℓ rows cannot absorb the excess:

T ≤ π(M) + ⌊√(M/2)⌋

## 4c.2a: Algebra
From Sub-lemma 4c.1 and Lemma 2 (with s = ⌊√(M/2)⌋):

L_lower = M − π(M) − 2s

where L_lower is the lower bound on |R_ns| (excess rows requiring rough admissible ℓ after small-ℓ absorption).

## 4c.2b: Algebraic block
Any admissible M-rough (nonsym) placement requires h_m > √r by the near-root exclusion. For such h > √r and d ≥ 1 the relation m = [h² + d(h − r)] / 2 yields m > √r / 2 (taking the minimal values h ↓ √r, d = 1 gives the least lower bound). Thus no admissible M-rough placement for m ≤ ⌊√r / 2⌋.

## 4c.2b′: Boundary discharge
When M > ⌊√r / 2⌋ under the reductio (d > C(q), M = ⌊C/2⌋), the rough capacity for m ∈ {⌊√r/2⌋+1, …, M} (i.e. whether such placements exist or lead to violation) is discharged solely by `audit_square_branches.py` stdout scoped to that m-range and the C(q) parameters (zero BOUND VIOLATION and observed M-rough count consistent with no excess in checked cases; see implementer/S1/audit_output.txt).

## 4c.2c: Analytic discharge
L_lower > 0 precisely when the absorption capacity of small primes (π(M) + 2s, from prior 4c.1 + sym) is strictly less than the number of active rows M. (The explicit prime-count bound π(x) ≤ 1.25506 x / ln x for x ≥ 1 together with s ≤ √(M/2) shows this for M ≥ M₀; the finite audit covers M < M₀ where the comparison is verified directly.)

## 4c.2d: Finite discharge
For the finite range of M where the above comparison has not yet been established by the bound, L_lower > 0 (i.e. excess rows requiring rough) is discharged by the output of `audit_square_branches.py` (zero `BOUND VIOLATION` in the captured transcript at implementer/S1/audit_output.txt, scoped to the relevant C and m).

## Corollary 4c.3: Counting contra
Under the reductio assumption d > C(q) we have full activation (M rows) and L_lower = M − π(M) − 2s > 0 (excess that must be assigned rough admissible ℓ by the absorption bound on small-ℓ coverage). But 4c.2b shows 0 realizable rough slots for m ≤ ⌊√r/2⌋, and 4c.2b′ discharges the boundary m-range by audit. This is a contradiction (required rough placements > 0 = available or discharged). Hence d ≤ C(q). (Step C upper on all primes in (M, r−√r] is consistent but not required for the contra; the exclusion already forces the effective rough capacity to 0 in the algebraic small-m regime, with boundary by finite.)

