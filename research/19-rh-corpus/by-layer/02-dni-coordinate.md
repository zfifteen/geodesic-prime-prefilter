# Layer 2 — DNI coordinate

**Status mix:** `exact`  
**Proves RH?** No — integer-side reformulation only

Layer 2 rewrites the divisor field on a **single continuous scale** so that prime
returns, gap interiors, and bridge loads share one coordinate system before zeta
compression.

**Authority:** [docs/rh/dni-to-zeta-compression.md](../../../docs/rh/dni-to-zeta-compression.md) §2–3

---

## Coordinate dictionary

| Symbol | Definition | Prime value | Composite |
|--------|------------|-------------|-----------|
| $E(n)$ | $\bigl(\frac{\tau(n)}{2}-1\bigr)\log n$ | $0$ | $>0$ |
| $F(n)$ | $\bigl(1-\frac{\tau(n)}{2}\bigr)\log n$ | $0$ | $<0$ on interior minima |
| $Z(n)$ | $e^{-E(n)}=n^{1-\tau(n)/2}$ | $1$ | $<1$ |
| $H(n)$ | $\log n + E(n)=\frac{\tau(n)\log n}{2}$ | $\log n$ | load $>\log n$ |

**Key identity:** $F(n)=-E(n)$. GWR selects the leftmost interior $\arg\min E(n)$.

Core doc: [DIVISOR_NORMALIZATION_IDENTITY.md](../../../docs/core/DIVISOR_NORMALIZATION_IDENTITY.md)

---

## Worked example (gap 23–29)

| $n$ | $\tau(n)$ | $E(n)$ | $Z(n)$ |
|-----|-----------|--------|--------|
| 23 | 2 | 0 | 1 |
| 25 (GWR) | 3 | $\log 25$ | $5^{-1/2}$ |
| 29 | 2 | 0 | 1 |

- Next prime: first $n>p$ with $E(n)=0$.
- Interior: $E(n)>0$ throughout $I$.
- Witness: first $n\in I$ achieving $\min E(n)$.

Reproduce: `python3 experiments/integer-order-before-zeta-whitepaper-2026-07/integer_order_demo.py`

---

## Bridge load (compression input)

The Dirichlet bridge uses **$H(n)$**, not $E(n)$ alone:

$$
H(n)=\log n + E(n)=\frac{\tau(n)\log n}{2}.
$$

Series:

$$
K(s)=-\frac{1}{e^2}D'(s),
\qquad
D(s)=\sum_{n\ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

Normalized ratio (L3):

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}=-\frac{\zeta'(s)}{\zeta(s)}.
$$

---

## Integer half-line vs critical half-line

| Coordinate | Domain | Zero locus |
|------------|--------|------------|
| $E(n)=0$ | integers $n>1$ | primes |
| $\operatorname{Re}(s)=\tfrac12$ | complex $s$ | RH target for nontrivial zeros |

Compare by **analogy** only unless [RH-040](../FINDINGS_INDEX.md) (F18-003) is proved.
FAQ: [zero-excess-floor-vs-critical-line.md](../../../docs/faq/category-errors/zero-excess-floor-vs-critical-line.md)

---

## Indexed findings

| ID | Status | Title | Path |
|----|--------|-------|------|
| [RH-010](../FINDINGS_INDEX.md) | exact | Zero-excess $E(n)$ | [dni-to-zeta-compression.md](../../../docs/rh/dni-to-zeta-compression.md) |
| [RH-011](../FINDINGS_INDEX.md) | exact | DNI score $Z(n)$ | [DIVISOR_NORMALIZATION_IDENTITY.md](../../../docs/core/DIVISOR_NORMALIZATION_IDENTITY.md) |
| [RH-012](../FINDINGS_INDEX.md) | exact | Bridge load $H(n)$ | [dni-to-zeta-compression.md](../../../docs/rh/dni-to-zeta-compression.md) |

[Stack overview](../SOURCE_STACK.md) · [Full index](../FINDINGS_INDEX.md) · [L3 compression](./03-zeta-compression.md)