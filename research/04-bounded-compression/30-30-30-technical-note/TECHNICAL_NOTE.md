# Prime-Square Proximity Theorem Technical Note

**Date:** 2026-07-11  
**Finding / Theorem:** Prime-Square Proximity Theorem (PSP; square-branch bounded compression)  
**Status:** proved (prose analytic; universal under stated hypotheses)  
**Formalization:** Lean 4 mirror in progress (`near_root_exclusion_bound` proved in Lean; `prime_square_proximity_theorem` still a stub / lean-partial and does not yet emit `C(q)`; formalization status only, not a demotion of the theorem)  
**Authority:** `PROOF.md` (Headline pillar 3; §Prime-Square Proximity Theorem) · `docs/proof-enhancements/psp-closure/README.md` · `docs/RESULTS.md` (Bounded Compression) · `docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md` (GWR context) · `research/04-bounded-compression/README.md`

---

## Part I: Plain-Language Summary

Take two consecutive primes, for example $23$ and $29$. Between them sit the
interior integers $24,25,26,27,28$. Each integer has a **divisor count**: how
many positive integers divide it evenly. Primes have count $2$. Composites have
count $3$ or higher. An integer with count exactly $3$ is always a **prime
square** (the square of a prime).

The Prime Gap Structure (PGS) rule called GWR picks one special interior point:
the **leftmost** integer with the **smallest** divisor count in the gap. Call
that point $w$. In the gap from $23$ to $29$, the counts are $8,3,4,4,6$. The
minimum is $3$ at $n=25$, so $w=25=5^2$. The distance from the left prime to
that square is $25-23=2$.

The **square branch** is the case where that selected point has divisor count
$3$, so $w=r^2$ for some prime $r$. The **Prime-Square Proximity Theorem**
bounds how far that square can sit past the left prime $p$. It does **not**
bound the full gap length $q-p$. On this branch it proves

$$
r^2 - p \;\le\; \max\bigl(64,\; \lceil 0.5\,(\log(r^2))^2 \rceil\bigr).
$$

Because $r^2 < q$, the cutoff
$C(q)=\max\bigl(64,\; \lceil 0.5\,(\log q)^2 \rceil\bigr)$
covers $w-p$ when $w$ is a prime square. PSP is only the **square-branch
component** of **universal bounded compression** (every gap has
$w-p\le C(q)$, proved 2026-07-05 in `PROOF.md`). The other components are the
finite base, residual $K=128$ first-$d_4$ elimination, and large-divisor /
half-coefficient closure for $\tau(w)\ge 4$.

If the square sits too far past $p$, each even step below the square needs a
smallest prime factor less than $r$. Counting those factors against a fixed
budget yields a contradiction once the offset exceeds $C(q)$.

**Status.** The Prime-Square Proximity Theorem is **proved** in analytic prose.
Finite audits **corroborate** it; they do not replace it. Lean formalization is
**in progress** (not a demotion). This does **not** prove the Riemann
Hypothesis, the Prime Number Theorem, or that the raw gap $q-p$ is always small.

---

## Part II: Visual Summary

![Prime-Square Proximity Theorem: square-branch bound on r squared minus p](infographic.svg)

*PNG export:* [infographic.png](infographic.png)

The diagram shows the square-branch chain:

1. Consecutive primes $p,q$; GWR selects leftmost minimum $\tau$ in the interior.
2. Square branch: $\tau(w)=3$ forces $w=r^2$ (prime square); bound target is $r^2-p$, not $q-p$.
3. Active rows $x_m=r^2-2m$ for $m\le M=\lfloor C(q)/2\rfloor$ need least factors $\ell_m=r-h_m$.
4. Near-root exclusion: nonsymmetric $M$-rough placements force $h_m>\sqrt{r}$ (factors barred near $r$).
5. Capacity contradiction if $r^2-p>C(q)$: too many active rows for small-$\ell$ absorption plus zero rough slots on small $m$.
6. Conclusion: on the square branch, $r^2-p\le C(q)$. **PROVED** (PSP only). With the finite base, residual $K=128$, and $\tau\ge 4$ closures, universal bounded compression holds on every branch (`PROOF.md` pillar 3). Boundary: not gap $q-p$, not RH.

---

## Part III: Technical Treatment

### 1. Setting and notation

Let $p<q$ be consecutive primes with **nonempty interior**

$$
I(p,q)=\{p+1,p+2,\ldots,q-1\},\qquad |I|=q-p-1\ge 1.
$$

Let $\tau(n)$ (also written $d(n)$ in some project docs) denote the positive
divisor-count function. The **Gap Winner Rule (GWR)** / leftmost
minimum-divisor rule selects

$$
w=w(p,q)=\min_{\prec}\arg\min_{n\in I(p,q)}\tau(n),
$$

where $\prec$ is left-to-right order on $\mathbb{Z}$. Authority for the selection
rule and maximizer theorem: `PROOF.md` (Interior maximizer); context prose in
`docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md`.

The **dynamic cutoff** for universal bounded compression is

$$
C(q)=\max\Bigl(64,\;\bigl\lceil \tfrac12\,(\log q)^2\bigr\rceil\Bigr).
$$

**Square branch.** The square branch is the residual case

$$
\tau(w)=3.
$$

The positive integers with $\tau(n)=3$ are exactly the squares of primes. Hence
there exists a prime $r$ with

$$
w=r^2.
$$

Leftmost minimality forces $\tau(n)\ge 4$ for every $n$ with $p<n<r^2$: every
earlier interior integer is composite and is not a prime square.

Set

$$
M=\bigl\lfloor C(q)/2\bigr\rfloor.
$$

For integers $m\ge 1$ with $2m\le r^2-p$, define the **row**

$$
x_m:=r^2-2m.
$$

Each such $x_m$ is composite and not a prime square, so it has a least prime
factor $\ell_m<r$. Writing $\ell_m=r-h_m$ with $h_m\ge 0$ yields the
**root-straddling factorization**

$$
x_m=(r-h_m)\,(r+h_m+d_m),\qquad d_m\ge 0.
$$

- **Symmetric row:** $d_m=0$, equivalent to $2m=h_m^2$.
- **Nonsymmetric row:** $d_m\ge 1$, with quotient equation
  $d_m\,\ell_m=h_m^2-2m$.
- **$M$-rough row:** every prime divisor of $x_m$ is strictly greater than $M$
  (equivalently $\ell_m>M$).
- **Modulus-link collision:** distinct rows $m_1\neq m_2$ **collide** if
  $\ell_{m_1}=\ell_{m_2}$.

Canonical definitions: `docs/proof-enhancements/psp-closure/README.md`.

---

### 2. Formal statement

**Theorem (Prime-Square Proximity; square-branch bounded compression).**  
Let $p<q$ be consecutive primes with nonempty interior, and let $w$ be the GWR
witness. Assume the square branch $\tau(w)=3$, so $w=r^2$ for a prime $r$. Then

$$
r^2-p\;\le\;\max\Bigl(64,\;\bigl\lceil \tfrac12\,(\log(r^2))^2\bigr\rceil\Bigr).
$$

Since $r^2<q$ and $C$ is nondecreasing in its argument for the relevant range,
this implies

$$
w-p=r^2-p\;\le\;C(q).
$$

**Relation to universal $C(q)$ compression.**  
Headline pillar 3 of `PROOF.md` states: for every consecutive prime gap with
nonempty interior,

$$
w-p\;\le\;C(q)=\max\Bigl(64,\;\bigl\lceil \tfrac12\,(\log q)^2\bigr\rceil\Bigr).
$$

Closure components (`docs/RESULTS.md`, Bounded Compression):

| Component | Role |
|-----------|------|
| Finite base ($q<\lceil e^{16}\rceil$) | Max selected-witness offset $60$ |
| Residual $K=128$ first-$d_4$ elimination | Odd-adjacent high-$\tau$ residual branches |
| **Prime-Square Proximity** | Square branch $\tau(w)=3$ only |

PSP is therefore the **square-branch component** of universal bounded
compression, not a bound on raw gap size and not a replacement for the
half-coefficient / large-divisor adjacent-closure arguments used on
$\tau(w)\ge 4$ branches.

**Status.** Logical: **proved** (analytic prose in `PROOF.md`, 2026-07-05).  
Scope: **universal** under the square-branch hypotheses above.  
Formalization: **in progress** (Lean); see §6. Do not demote the prose theorem
because the machine-checked mirror is incomplete.

---

### 3. Lemma architecture

The proof is a reductio: assume $r^2-p>C(q)$ and derive a capacity
contradiction on the active rows $\{1,\ldots,M\}$. Authority stack:
`PROOF.md` §Prime-Square Proximity Theorem; lemma inventory and sub-lemmas
canonicalized in `docs/proof-enhancements/psp-closure/README.md`.

#### Lemma 0: Square-branch setup

From $\tau(w)=3$ and GWR leftmost minimality:

- $w=r^2$ for a prime $r$;
- $\tau(n)\ge 4$ for all $p<n<r^2$;
- each $x_m=r^2-2m$ with $1\le 2m\le r^2-p$ admits a least prime factor
  $\ell_m<r$.

#### Lemma 1: Row to Factor Assignment

Each active $m\in\{1,\ldots,M\}$ admits a unique admissible placement
$(\ell_m,h_m,d_m)$ with $\ell_m$ prime, $\ell_m=r-h_m$, $\ell_m<r$, and
$x_m=\ell_m\cdot(r+h_m+d_m)$. Existence follows from compositeness and the
root-straddling form; uniqueness takes $\ell_m$ as the least prime factor.

#### Lemma 2: Symmetric-row cardinality

If $d_m=0$ then $2m=h_m^2$, hence

$$
\#\{m\in\{1,\ldots,M\}:d_m=0\}\;\le\;\bigl\lfloor\sqrt{M/2}\bigr\rfloor.
$$

#### Lemma 3: Near-root exclusion

For nonsymmetric $M$-rough rows, the quotient equation and
$\ell_m=r-h_m$ force

$$
h_m\;\ge\;\Bigl\lceil\frac{\sqrt{1+4(r+2m)}-1}{2}\Bigr\rceil\;>\;\sqrt{r},
$$

so $\ell_m=r-h_m<r-\sqrt{r}$. Named Lean lemma:
`near_root_exclusion_bound` in `lean-4/PGS/ChamberReset.lean`.

#### Lemma 4a: Injectivity on $M$-rough rows

The map $m\mapsto\ell_m$ is injective on $M$-rough rows in $\{1,\ldots,M\}$.
Mechanism: rows $x_m$ lie in $[r^2-2M,r^2-2]$; if a common odd prime $\ell$
divides two distinct rows, minimum separation is at least $2\ell$, forcing
$\ell<M$, which contradicts $M$-roughness.

#### Lemma 4b: Pigeonhole upper bound

Let $R$ (resp. $R_{\mathrm{ns}}$) be the set of $M$-rough (resp. nonsymmetric
$M$-rough) rows. Near-root exclusion plus injectivity give

$$
|R_{\mathrm{ns}}|\;\le\;\pi\bigl(\lfloor r-\sqrt{r}\rfloor\bigr)-\pi(M),
$$

where $\pi$ is the prime-counting function (used only as a finite interval
count of available primes, not as a density model for inference).

#### Lemma 4c / Corollary 4c.3: Capacity contradiction

Assume $r^2-p>C(q)$. Then every $m\in\{1,\ldots,M\}$ is active (Step A: full
row activation, using $2M\le C(q)$). Partition into small-$\ell$ and $M$-rough
rows (Step B). With $s=\lfloor\sqrt{M/2}\rfloor$ and $T=\#\{m:\ell_m\le M\}$:

$$
L_{\mathrm{lower}}\;=\;M-\pi(M)-2s
$$

is a lower bound on excess nonsymmetric rough demand after small-$\ell$
absorption (Sub-lemma 4c.1: $T\le\pi(M)+s$). Algebraic block 4c.2b: admissible
nonsymmetric $M$-rough placements require $h_m>\sqrt{r}$ and force
$m>\sqrt{r}/2$, so **no** such placement exists for $m\le\lfloor\sqrt{r}/2\rfloor$.
Boundary $m$-range and small-$M$ comparisons are discharged by finite audit of
`audit_square_branches.py` where the pure inequality is not yet free of a finite
check (4c.2b′, 4c.2d). Analytic discharge of $L_{\mathrm{lower}}>0$ for large $M$
uses an explicit prime-count upper bound
$\pi(x)\le 1.25506\,x/\ln x$ (4c.2c).

**Corollary.** Under the reductio, required rough placements are positive while
realizable rough capacity on the active small-$m$ regime is zero (boundary by
finite). Contradiction. Hence $r^2-p\le C(q)$.

---

### 4. Finite premises and audit surfaces

These complete or corroborate the analytic stack; they are not substitutes for
the universal square-branch statement.

| Surface | Role | Status label |
|---------|------|--------------|
| `bounded_compression_base_v1` | Exhaustive base for universal $C(q)$ at $q<\lceil e^{16}\rceil$; max offset $60$ | finite-certified premise |
| `residual_k128_v1` | Residual odd-adjacent $d=4$ elimination before square/large-$d$ closure | finite-certified premise |
| Square-branch falsification sweeps | e.g. prime roots $300\mathrm{M}$ to $400\mathrm{M}$, $5{,}084{,}001$ tested; no counterexample; max utilization $0.70$ | audit corroboration (`docs/RESULTS.md`) |
| `audit_square_branches.py` | PSP capacity / bound-violation probe (psp-closure Phase 2) | audit corroboration |

Invalidated legacy rule (not to be revived): fixed cutoffs $\{2{:}44,\,4{:}60,\,6{:}60\}$ fail at $q=24{,}098{,}209$ with square-branch $E(q)=72>60$.

---

### 5. Micro-example (observable row)

Gap $p=23$, $q=29$:

```text
n:             24  25  26  27  28
tau(n):         8   3   4   4   6
```

- GWR witness $w=25=5^2$, so $\tau(w)=3$ (square branch), $r=5$.
- Offset $r^2-p=2$.
- $C(29)=64$, so $2\le C(29)$ holds with large margin.
- Full gap length $q-p=6$ is **not** the quantity bounded by PSP.

Source for the row: `docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md`.

---

### 6. Formalization status (separate from theorem status)

| Lean object | Role | Status |
|-------------|------|--------|
| `near_root_exclusion_bound` | Lemma 3 geometric exclusion | proved in `lean-4/PGS/ChamberReset.lean` |
| `prime_square_proximity_theorem` | Target: full chain to emit $r^2-p\le C(q)$ | in progress / lean-partial until upgraded |
| Row assignment / injectivity / 4c capacity | Structural lemmas | targets listed in `docs/proof-enhancements/psp-closure/README.md` |

**Explicit separation:** incomplete Lean coverage does **not** demote the
analytic theorem in `PROOF.md`. Formalization is a machine-checked mirror
track.

---

### 7. Boundary statement

The Prime-Square Proximity Theorem is a **proved bound on the square-branch
selected-witness offset** $r^2-p$ (equivalently $w-p$ when $\tau(w)=3$). It does
**not**:

- bound the raw consecutive-prime gap $q-p$;
- prove the Riemann Hypothesis;
- prove the Prime Number Theorem;
- prove every classical formulation of Cramér's conjecture for gap size;
- assert that the $(log)^2$ envelope is a probabilistic Cramér model (the scale
  matches Cramér's envelope but the object is witness placement, derived from
  divisor-count structure).

Universal bounded compression inherits the same boundary for $w-p$ on all
branches (`PROOF.md` Headline pillar 3 boundary language; `docs/RESULTS.md`).

---

### 8. Authority paths

- `PROOF.md`: Headline pillar 3; §Prime-Square Proximity Theorem (Square-Branch Bounded Compression); theorem stack row for PSP
- `docs/proof-enhancements/psp-closure/README.md`: lemma inventory (0 to 5), definitions, Sub-lemma 4c.2 / Corollary 4c.3 canonical chain
- `docs/RESULTS.md`: Bounded Compression (Proved); audit corroboration regimes
- `docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md`: GWR / leftmost minimum-divisor context and $23$ to $29$ row
- `research/04-bounded-compression/README.md`: chapter home, dynamic cutoff, invalidated fixed cutoffs
- `lean-4/PGS/ChamberReset.lean`: `near_root_exclusion_bound` and PSP formalization targets
- `docs/square_branch_theorem_plan.md`: historical execution plan (Phases 1 to 4)

---

*30/30/30 Technical Note · skill `30-30-30-technical-note` · chapter `research/04-bounded-compression`*
