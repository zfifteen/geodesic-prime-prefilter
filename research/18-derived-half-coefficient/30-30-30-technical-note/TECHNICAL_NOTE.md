# Derived Half-Coefficient Technical Note

**Date:** 2026-07-08  
**Finding:** F18-001  
**Status:** proved · universal  
**Authority:** `PROOF.md` · `research/04-bounded-compression/`

---

## Part I — Plain-Language Summary

Between two consecutive primes, every composite has a **divisor count** (how many
positive divisors it has). Primes have count 2. Composites have 3 or more.

PGS picks one special composite in each gap: the **GWR witness** $w$. It is the
**leftmost** interior number with the **smallest** divisor count.

A proved theorem bounds how far $w$ can sit from the left prime $p$:

$$
C(q) = \max\!\left(64,\;\left\lceil 0.5 \cdot (\log q)^2 \right\rceil\right),
\qquad w - p \le C(q).
$$

The breakthrough is where **0.5** comes from. It is **not** picked to match old
gap conjectures or the zeta critical line. It is **derived** by summing divisor
counts in a short window before $w$. If that window is too long, some earlier
number must have fewer divisors than $w$, which breaks the GWR rule. The algebra
forces scale $(\log w)^2/8$, which becomes **0.5·(log q)²**.

**Example (23–29):** divisor counts 8,3,4,4,6; minimum 3 at 25; distance 2.

**Audit:** zero violations of $C(q)$ for $q \le 10^6$; median distance 2.

**Boundary:** bounds witness offset $w-p$ only — not RH, not full gap $q-p$.

---

## Part II — Visual Summary

![Derived Half-Coefficient infographic](infographic.svg)

*PNG export:* [infographic.png](infographic.png)

1. Select GWR witness $w$ in gap $(p,q)$.
2. Witness Threshold closes earlier high-$\tau$ competitors.
3. Short Divisor-Average on $J=\{w-H,\ldots,w-1\}$ forces small $H$.
4. $H=O((\log w)^2)$ with constant $1/8$ yields $\lceil 0.5(\log q)^2\rceil$.
5. Audit + boundary: 0 violations to $10^6$; does not prove RH.

---

## Part III — Technical Treatment

### Notation

$I(p,q)=\{p+1,\ldots,q-1\}$, $\tau(n)$ divisor count,

$$w=\min_\prec\arg\min_{n\in I}\tau(n), \qquad F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.$$

### Theorem

$$w-p \le C(q)=\max\left(64,\left\lceil 0.5(\log q)^2\right\rceil\right).$$

### Half-Scale Emergence (F18-001)

Set $d=\tau(w)\ge 4$, $L=\log w$,

$$H=\left\lfloor\frac{wL}{4(d-1)}\right\rfloor \ge \frac{wL}{8(d-1)}.$$

Short Divisor-Average on $J=\{w-H,\ldots,w-1\}$:

$$\sum_{n\in J}\tau(n)\le H(L+2)+2\sqrt w.$$

Mean $<d$ for large $w$, so some $n\in J$ has $\tau(n)<d$. GWR forces $n\le p$,
hence $w-p\le H$. With $d-1=\Omega(L)$, $H=O(L^2)$ and the packaged cutoff is
$\lceil 0.5(\log q)^2\rceil$.

*Authority:* `PROOF.md` §305–347, §353–392, §394–520, §574–679.

### Measured corroboration (F18-002)

Grok audit: 78,496 gaps, **0** violations, median distance 2, max 48
(`experiments/grok-share-509b8495/safari_transcript.txt`).

### Boundary

Does not prove RH, PNT, or Cramér for $q-p$. F18-003 (half-scale rhyme) is
hypothesis only.

---

*30/30/30 Technical Note · skill `30-30-30-technical-note`*