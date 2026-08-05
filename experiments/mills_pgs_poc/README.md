# PGS → Mills Constant Structural Bridge  
## Proof-of-Concept for Third-Party Auditors

**Branch:** `poc/mills-constant-structural-bridge`  
**Target audience:** Experts in Mills’ constant and prime-representing functions who have no prior exposure to the Prime Gap Structure (PGS) project.  
**Status:** Self-contained, validated PoC. All assertions pass on the classical early terms.

---

## 1. Purpose and Scope

Mills’ theorem (1947) asserts the existence of a real constant $A > 1$ such that

$$
\lfloor A^{3^n} \rfloor
$$

is prime for every positive integer $n$. The *least* such $A$ (under the Riemann Hypothesis) begins

$$
1.30637788386308069046\ldots
$$

and generates the sequence of **Mills primes**

$$
2,\; 11,\; 1361,\; 2521008887,\; \ldots
$$

via the recurrence

$$
p_1 = 2,\qquad p_{n+1} = \operatorname{nextprime}(p_n^3).
$$

The existence proof rests on classical results guaranteeing at least one prime in every sufficiently large interval of the form $(x^3,(x+1)^3)$. Under RH the “sufficiently large” restriction can be removed and the sequence may begin at 2.

This PoC does **not** claim a new proof of the short-interval estimates.  
It demonstrates that the *local arithmetic structure* studied by the PGS project recovers exactly the same sequence when the walk is started from each successive cube, and that it supplies an explicit, inspectable structural certificate for each transition.

In other words: the classical argument says “a prime exists inside the cube interval.”  
PGS supplies a deterministic local rule that *reads* the ordered divisor-count field after the cube and identifies both a canonical interior landmark (the Gap Winner) and the endpoint prime (the first return of $d(n)$ to 2).

---

## 2. Minimal Self-Contained Definitions of the PGS Notions Used

No external PGS documentation is required. The following notions are defined here for the auditor.

**Divisor count.**  
$d(n) = \#\{k \in \mathbb{Z}^+ : k \mid n\}$.

**Ordered divisor-count field after a cube.**  
Given a cube $c = p^3$, consider the sequence of pairs $(n,d(n))$ for $n = c+1, c+2, \dots$ until the first $n$ with $d(n)=2$.

**Gap Winner (GWR).**  
Among the composite integers that appear before the first return to $d=2$, the Gap Winner is the *leftmost* integer that realises the global minimum of $d(n)$ in that initial segment.  
(Equivalently, in the fuller PGS development it maximises the raw-$Z$ score $Z(n) = n^{1-d(n)/2}$; the leftmost-min-$d$ characterisation is sufficient for this PoC.)

**Next prime rule (local).**  
The first integer after the cube whose divisor count equals 2 is prime (by definition of $d$) and is the candidate for the next Mills prime.

**Bounded Compression (statement used here).**  
The offset of the Gap Winner from the left reference point satisfies

$$
\text{offset} \le \max\bigl(64,\lceil\tfrac12(\log q)^2\rceil\bigr),
$$

where $q$ is the recovered prime. This is the quantitative form proved (and computationally validated to $10^{18}$) in the main PGS repository; the early Mills residuals are far smaller than the bound, so the check is trivial but still recorded.

These four notions are the only PGS machinery required for the experiment.

---

## 3. Experimental Design

1. Take the classical Mills primes (RH-dependent least sequence) up to the fourth term (the fifth term is $\sim 10^{28}$ and is not walked).
2. For each consecutive pair $p \to p'$:
   - Compute the cube $c = p^3$.
   - Walk $n = c+1, c+2, \dots$, recording $d(n)$, until $d(n)=2$.
   - Identify the Gap Winner by the leftmost-min-$d$ rule.
   - Verify that the recovered integer equals the known next Mills prime.
   - Verify that the residual matches the known OEIS A108739 entry.
   - Verify that the Gap Winner offset satisfies the Bounded Compression inequality.
3. Emit both a human-readable report and a machine-readable JSON certificate.

The walks are tiny (residuals 3, 30 and 6 respectively), so the experiment is fully rigorous and independent of any external primality test beyond the definition $d(n)=2$.

---

## 4. How to Reproduce

```bash
# From the repository root (or from this directory)
python3 experiments/mills_pgs_poc/mills_pgs_bridge.py
```

Requirements: Python ≥ 3.8, standard library only.  
(The script writes `poc_report.json` in the working directory.)

Expected terminal output ends with:

```
All assertions passed. PoC successful.
Wrote poc_report.json
```

and shows the three ordered divisor fields with the Gap Winner and the recovered prime clearly marked.

---

## 5. Results (verified on 2026-08-05)

| Transition | Cube          | Residual | Gap Winner     | GWR $d$ | Offset | Bound | Recovered prime   | Status |
|------------|---------------|----------|----------------|---------|--------|-------|-------------------|--------|
| $2\to11$ | 8             | 3        | 9              | 3         | 1      | 64    | 11                | PASS   |
| $11\to1361$ | 1331       | 30       | 1333           | 4         | 2      | 64    | 1361              | PASS   |
| $1361\to2521008887$ | 2521008881 | 6 | 2521008883 | 8     | 2      | 235   | 2521008887        | PASS   |

All recoveries exact. All residuals match the classical sequence. Bounded Compression holds. The ordered fields are short enough to be inspected by hand.

---

## 6. What This Demonstrates for a Mills Expert

- The classical recurrence $p_{n+1}=\operatorname{nextprime}(p_n^3)$ can be realised by a purely local arithmetic walk that never consults an external prime-table or probabilistic test; it only counts divisors and applies the leftmost-min-$d$ rule.
- Each transition receives an explicit structural certificate: the complete (tiny) ordered divisor field together with a canonically chosen interior landmark (the Gap Winner).
- The same local rules that the PGS project uses for ordinary successive primes also locate the special primes that appear in the Mills construction.
- The experiment is fully reproducible and the certificates are machine-checkable.

It does **not** replace the analytic work that guarantees a prime exists inside every cube interval of sufficient size. It shows that, once that existence is granted (or observed), the PGS local geometry supplies a deterministic, inspectable description of *where* and *how* the prime sits relative to the cube.

---

## 7. Limitations and Non-Claims

- Only the first three transitions are walked; larger Mills primes produce enormous cubes and are outside the scope of a lightweight PoC.
- The script does not attempt to compute new Mills primes beyond the known classical terms.
- No claim is made that the Gap Winner rule itself proves the existence of primes in cube intervals; the existence input still comes from the classical short-interval theory (or from direct verification for the tiny residuals used here).
- Bounded Compression is checked but is not the novel contribution of this particular experiment; it is recorded for consistency with the broader PGS claims.

---

## 8. Suggested Audit Checklist for a Third Party

- [ ] Run the script; confirm all assertions pass and the printed residuals match OEIS A108739.
- [ ] Manually recompute $d(n)$ for the three short fields and verify the leftmost-min-$d$ selection.
- [ ] Confirm that the recovered integers are indeed the classical Mills primes.
- [ ] Read the self-contained definitions in §2; decide whether they are unambiguous.
- [ ] Decide whether the structural certificates add useful information beyond the bare residual sequence.
- [ ] (Optional) Compare the Gap Winner offsets against the Cramér-scale bound used in the main PGS literature.

---

## 9. Relation to the Main Repository

This directory is intentionally self-contained. The fuller development of the Gap Winner Rule, the Divisor Normalisation Identity, the No-Later-Simpler-Composite theorem, the Bounded Compression theorem, and the Lean 4 formalisation live in the main branches of `zfifteen/prime-gap-structure`. An auditor who finds the present certificates interesting is invited to examine `PROOF.md` and the Lean 4 mirror for the general theory.

---

## 10. Citation / Provenance

- Classical Mills sequence and residuals: OEIS A051254, A108739; Caldwell–Cheng (2005).
- PGS local rules as used here: this PoC (branch `poc/mills-constant-structural-bridge`).
- Script and report generated and validated 2026-08-05.
