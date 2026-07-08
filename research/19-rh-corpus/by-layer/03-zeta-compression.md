# Layer 3 — Zeta compression

**Status mix:** `exact`, `measured`  
**Proves RH?** No — exact identities only; pole placement remains L5

This layer is the **arithmetic-to-analytic lift**: the same divisor-count field
that governs gap interiors compresses into classical zeta language without
approximation on `Re(s) > 1`.

---

## Source order (fixed)

```text
τ(n) on integers  →  E(n), H(n) load  →  D(s), K(s) series  →  ζ², −ζ'/ζ
```

Authority: [docs/rh/dni-to-zeta-compression.md](../../../docs/rh/dni-to-zeta-compression.md)  
Do not duplicate proof bodies here — link only.

---

## Core mappings

### Divisor-count series → ζ²

Ordered factor pairs $(a,b)$ with $ab=n$ count $\tau(n)$:

$$
D(s)=\sum_{n\ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2,
\qquad \operatorname{Re}(s)>1.
$$

**RH-020** — exact identity, not asymptotic.

### Bridge load → logarithmic derivative

Integer load (same information as excess):

$$
H(n)=\log n + E(n)=\frac{\tau(n)\log n}{2},
\qquad
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

Normalization series $K(s)=-\frac{1}{e^2}D'(s)$ gives the **function-level** ratio:

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}
=\sum_{n\ge 1}\frac{\Lambda(n)}{n^s}.
$$

**RH-021** — quotient is taken after summation, not coefficientwise.

### Pole–zero dictionary

After continuation, poles of $R(s)$ track zeros of $\zeta(s)$:

| ζ zero/pole | R(s) record |
|-------------|-------------|
| Pole at $s=1$ | PNT main term |
| Trivial zeros | Trivial poles |
| Nontrivial zeros | Nontrivial poles |

**RH-022** — dictionary only; does not place zeros on $\operatorname{Re}(s)=\tfrac12$.

---

## What L1 supplies to L3

The proved local theorems ([PROOF.md](../../../PROOF.md)) fix **which integers**
enter the coefficient field before compression:

| L1 object | Role in compression |
|-----------|---------------------|
| Next prime $q=\min\{n>p:\tau(n)=2\}$ | Endpoint where $\Lambda$ "resets" to prime power |
| GWR witness $w$ | Leftmost interior $\arg\min E(n)$; shapes local load |
| Bounded offset $w-p\le C(q)$ | Cramér-scale chamber width before spectral read |
| Derived $\tfrac12$ in $C(q)$ | Arithmetic closure ([RH-006](../FINDINGS_INDEX.md), F18-001) |
| F18-004 rough-witness split | Non-square vs square branch discipline ([RH-103](../FINDINGS_INDEX.md)) |

The compression identities are **global**; GWR selection is **local**. The open
L4–L5 work is to show how local chamber geometry constrains global pole placement.

---

## Branch discipline (F18-004 → compression)

Near-maximal witness offsets $(w-p)/C(q)\ge 0.65$ split into two lanes:

| Branch | $\tau(w)$ | Compression relevance |
|--------|-----------|------------------------|
| Non-square | Must be rough ($\tau(w)\gtrsim 0.75\log q$) | Drives divisor-average contradiction → factor $\tfrac12$ |
| Prime square | $\tau(w)=3$; ceiling ratio $\approx 0.715$ | Closed by Prime-Square Proximity; **does not** set $\tfrac12$ |

40M exhaustive replay: **zero** non-square low-$d$ falsifiers.  
Artifact: [research/18-derived-half-coefficient/output/near_maximal_audit_results_40M.json](../../18-derived-half-coefficient/output/near_maximal_audit_results_40M.json)

This separates **arithmetic forcing** of the half-coefficient from **square tiling**
geometry — critical for honest RH-facing exposition (compare [RH-040](../FINDINGS_INDEX.md) hypothesis only).

---

## Worked micro-example (gap 23–29)

From [integer-order demo](../../../experiments/integer-order-before-zeta-whitepaper-2026-07/integer_order_demo.py):

| $n$ | $\tau(n)$ | $E(n)$ |
|-----|-----------|--------|
| 23 | 2 | 0 |
| 25 (GWR $w$) | 3 | $\log 25$ |
| 29 ($q$) | 2 | 0 |

The interior load profile is fixed **before** any Dirichlet sum. Summing
$\tau(n)n^{-s}$ over all $n$ still yields $\zeta(s)^2$; the gap example shows
**where** local minima sit in the source field.

---

## Measured validation (RH-105)

Reproducible partial-sum probe at multiple $s$:

```bash
python3 research/19-rh-corpus/empirics/zeta_compression_probe.py
```

Output: [empirics/output/compression_probe_results.json](../empirics/output/compression_probe_results.json)

Status: `measured` — confirms convergence of truncated sums; not a certificate of
analytic continuation or critical-line placement.

---

## Indexed findings (this layer)

| ID | Status | Title | Path |
|----|--------|-------|------|
| [RH-020](../FINDINGS_INDEX.md) | exact | $D(s)=\zeta(s)^2$ | [dni-to-zeta-compression.md](../../../docs/rh/dni-to-zeta-compression.md) |
| [RH-021](../FINDINGS_INDEX.md) | exact | $R(s)=-\zeta'/\zeta$ | [dni-to-zeta-compression.md](../../../docs/rh/dni-to-zeta-compression.md) |
| [RH-022](../FINDINGS_INDEX.md) | exact | Pole–zero dictionary | [pole-placement.md](../../../docs/rh/pole-placement.md) |
| [RH-091](../FINDINGS_INDEX.md) | exact | DNI–RH bridge workbench | [12-rh-bridge](../../12-rh-bridge/README.md) |
| [RH-103](../FINDINGS_INDEX.md) | measured | F18-004 rough-witness | [FINDING_STATEMENT.md](../../18-derived-half-coefficient/docs/FINDING_STATEMENT.md) |
| [RH-105](../FINDINGS_INDEX.md) | measured | Multi-s compression probe | [zeta_compression_probe.py](../empirics/zeta_compression_probe.py) |

---

## Category errors (read before citing)

| Wrong | Right |
|-------|-------|
| $\zeta(s)^2$ identity proves RH | Exact compression; L5 placement open |
| $E(n)=0$ on integers = $\operatorname{Re}(s)=\tfrac12$ | Analogy only unless [RH-040](../FINDINGS_INDEX.md) proved |
| Partial sums at $N=10^4$ certify all poles | Measured convergence regime only |
| F18-004 is a theorem | Tested prediction; falsifier search documented |

---

## Downstream

- **L4:** [04-placement-geometry.md](./04-placement-geometry.md) — chamber invariants from GWR geometry  
- **L5:** [05-pole-placement-rh.md](./05-pole-placement-rh.md) — RH sentence on pole locus  
- **L6:** [06-explicit-formula-bridge.md](./06-explicit-formula-bridge.md) — $R\to\Lambda\to\psi$ translation  

[Stack overview](../SOURCE_STACK.md) · [Full index](../FINDINGS_INDEX.md) · [Gap analysis](../GAP_ANALYSIS.md)