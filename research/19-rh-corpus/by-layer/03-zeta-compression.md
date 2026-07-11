# Layer 3: Zeta compression

**Status mix:** `exact`, `measured`  
**Proves RH?** No: exact identities only. L5 is a downstream catalog, not a driver.
See [FRAME_CONTRACT.md](../FRAME_CONTRACT.md).

This layer is the **arithmetic-to-analytic lift**: the same divisor-count field
that governs gap interiors compresses into classical zeta language without
approximation on `Re(s) > 1`.

---

## Source order (fixed)

```text
τ(n) on integers  →  E(n), H(n) load  →  D(s), K(s) series  →  ζ², −ζ'/ζ
```

Authority: [docs/rh/dni-to-zeta-compression.md](../../../docs/rh/dni-to-zeta-compression.md)  
Do not duplicate proof bodies here, link only.

---

## Core mappings

### Divisor-count series → ζ²

Ordered factor pairs $(a,b)$ with $ab=n$ count $\tau(n)$:

$$
D(s)=\sum_{n\ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2,
\qquad \operatorname{Re}(s)>1.
$$

**RH-020**: exact identity, not asymptotic.

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

**RH-021**: quotient is taken after summation, not coefficientwise.

### Pole to zero dictionary

After continuation, poles of $R(s)$ track zeros of $\zeta(s)$:

| ζ zero/pole | R(s) record |
|-------------|-------------|
| Pole at $s=1$ | PNT main term |
| Trivial zeros | Trivial poles |
| Nontrivial zeros | Nontrivial poles |

**RH-022**: dictionary only; does not place zeros on $\operatorname{Re}(s)=\tfrac12$.

---

## Formal mapping: GWR chamber → zeta increments

Fix consecutive primes $p<q$, interior $I(p,q)=\{p+1,\ldots,q-1\}$, and GWR
witness $w(p,q)=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}$ ([PROOF.md](../../../PROOF.md)).

### Integer invariants (proved / measured)

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n,\qquad
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2},
$$

$$
B(p,q)=\sum_{n\in I} E(n),\qquad
C(q)=\max\!\left(64,\left\lceil\tfrac12(\log q)^2\right\rceil\right),\qquad
w-p\le C(q).
$$

Fractional placement: $\mathrm{frac\_pos}(p,q)=\dfrac{w-p}{q-p-1}$ when $|I|\ge1$.

### Chamber Dirichlet increments (exact at $\operatorname{Re}(s)>1$)

$$
\Delta D(s;p,q)=\sum_{n\in I}\frac{\tau(n)}{n^s},\qquad
\Delta B(s;p,q)=\sum_{n\in I}\frac{H(n)}{n^s}.
$$

Local chamber compression ratio (diagnostic, **not** additive across gaps):

$$
\rho_{\mathrm{ch}}(s;p,q)=\frac{\Delta B(s;p,q)}{\Delta D(s;p,q)}.
$$

Global continuation ([RH-021](../FINDINGS_INDEX.md)):

$$
R(s)=\frac{B(s)}{D(s)}=-\frac{\zeta'(s)}{\zeta(s)},
\quad
B(s)=\sum_{n\ge1}\frac{H(n)}{n^s}=-\tfrac12 D'(s).
$$

**Boundary:** $R(s)$ is a single meromorphic function; $\rho_{\mathrm{ch}}$ is a
per-gap slice. Placement target [RH-035](../FINDINGS_INDEX.md) bounds smoothed
kernel mass $\mathcal{K}(p,q;\Phi)$ from $B(p,q)$ and $\mathrm{frac\_pos}$, not
from summing $\rho_{\mathrm{ch}}$.

### F18 branch partition (compression relevance)

Let $r=(w-p)/C(q)$.

| Branch | Condition | Zeta-side role |
|--------|-----------|----------------|
| Prime square | $\tau(w)=3$, $w=r_0^2$ | Square tiling lane; **does not** derive $\tfrac12$ in $C(q)$ |
| Non-square, $r\ge 0.65$ | F18-004 measured | $\tau(w)\gtrsim 0.75\log q$ (rough witness) |
| Non-square, $r<0.65$ | Typical | Sub-threshold; divisor-average closure inactive |

Implemented in [chamber_compression.py](../empirics/chamber_compression.py);
validated by [zeta_compression_probe.py](../empirics/zeta_compression_probe.py) ([RH-105](../FINDINGS_INDEX.md)).

### Worked chamber numbers (gap 23 to 29, $s=2.5$)

| Quantity | Value |
|----------|-------|
| $w$ | 25 |
| $B(p,q)$ | $\sum_{n=24}^{28} E(n)$ |
| $\Delta D(2.5)$ | chamber divisor-series increment |
| $\rho_{\mathrm{ch}}(2.5)$ | $\Delta B/\Delta D$ (local) |
| $R(2.5)$ | global $-\zeta'/\zeta$ via `evaluate_partial_sum_bridge` |

Reproduce: `PYTHONPATH=src/python:research/19-rh-corpus/empirics python3 research/19-rh-corpus/empirics/zeta_compression_probe.py`

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
geometry: critical for honest RH-facing exposition (compare [RH-040](../FINDINGS_INDEX.md) hypothesis only).

---

## Worked micro-example (gap 23 to 29)

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

Reproducible partial-sum probe at five $s$-values:

```bash
PYTHONPATH=src/python:research/19-rh-corpus/empirics \
  python3 research/19-rh-corpus/empirics/zeta_compression_probe.py
```

| Pin | Value |
|-----|-------|
| $s$ grid | $\{2.0, 2.5, 3.0, 3.5, 4.0\}$ |
| Term count $N$ | $10^4$ |
| Example chambers | $23\to 29$, $89\to 97$ |
| F18 max case | integer branch only at $q\approx 1.5\times 10^7$ ($\Delta D/\Delta B$ deferred) |

Output: [empirics/output/compression_probe_results.json](../empirics/output/compression_probe_results.json)
fields `global_bridge_by_s` and `example_increments_multi_s`.

Status: `measured`, confirms convergence of truncated sums toward $-\zeta'/\zeta$;
not a certificate of analytic continuation or critical-line placement.

---

## Indexed findings (this layer)

| ID | Status | Title | Path |
|----|--------|-------|------|
| [RH-020](../FINDINGS_INDEX.md) | exact | $D(s)=\zeta(s)^2$ | [dni-to-zeta-compression.md](../../../docs/rh/dni-to-zeta-compression.md) |
| [RH-021](../FINDINGS_INDEX.md) | exact | $R(s)=-\zeta'/\zeta$ | [dni-to-zeta-compression.md](../../../docs/rh/dni-to-zeta-compression.md) |
| [RH-022](../FINDINGS_INDEX.md) | exact | Pole to zero dictionary | [pole-placement.md](../../../docs/rh/pole-placement.md) |
| [RH-091](../FINDINGS_INDEX.md) | exact | DNI to RH bridge workbench | [12-rh-bridge](../../12-rh-bridge/README.md) |
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

- **L4:** [04-placement-geometry.md](./04-placement-geometry.md): chamber invariants from GWR geometry  
- **L5:** [05-pole-placement-rh.md](./05-pole-placement-rh.md): RH sentence on pole locus  
- **L6:** [06-explicit-formula-bridge.md](./06-explicit-formula-bridge.md): $R\to\Lambda\to\psi$ translation  

[Stack overview](../SOURCE_STACK.md) · [Full index](../FINDINGS_INDEX.md) · [Gap analysis](../GAP_ANALYSIS.md)