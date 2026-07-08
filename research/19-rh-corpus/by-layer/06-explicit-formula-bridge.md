# Layer 6 — Explicit formula bridge

**Status mix:** `narrative`  
**Proves RH?** No — downstream translation for reviewers

Layer 6 restates the compressed ratio $R(s)$ in classical prime-counting language:
von Mangoldt coefficients, Chebyshev $\psi(x)$, and zero/error terms.

**Authority:** [docs/rh/explicit-formula-bridge.md](../../../docs/rh/explicit-formula-bridge.md)

---

## Translation chain

```text
R(s) = -ζ'(s)/ζ(s)
  →  Λ(n) coefficients
  →  ψ(x) = Σ_{n≤x} Λ(n)
  →  ψ(x) = x − Σ_ρ x^ρ/ρ + elementary terms
  →  zero-term / error language
```

The schematic explicit formula:

$$
\psi(x)=x-\sum_{\rho}\frac{x^{\rho}}{\rho}+\text{elementary terms},
$$

with $\rho$ over nontrivial zeros of $\zeta(s)$.

---

## Source-side vs spectral-side

| Object | Layer | Role |
|--------|-------|------|
| $E(n)$, GWR $w$ | L1–L2 | Integer gap mechanism |
| $D(s)$, $R(s)$ | L3 | Exact compression |
| Chamber $frac\_pos$ | L4 | Local placement geometry |
| Zero sum over $\rho$ | L6 | Classical oscillatory correction |

Layer 6 is how reviewers **already** talk about primes. PGS adds the upstream
integer read — it does not replace the explicit formula proof machinery.

---

## Super-signal hook (labeled)

When GWR witness $w$ has high primorial resonance ($w\equiv 0\pmod{30}$, 4+
remainder zeros), [RH-005](../FINDINGS_INDEX.md) proves **immediate gap termination**
($q=w+1$, twin gap). In explicit-formula language, this is an **exact local
termination** of the oscillatory correction inside that chamber — not a global
zero-placement theorem.

Status: proved corollary at L1; interpretive link to L6 is `narrative` only.

---

## Open placement target (L6 restatement)

The remaining program step is to show that **source-side chamber constraints**
([RH-035](../FINDINGS_INDEX.md)) force the zero sum in the explicit formula to
align with critical-line poles only. That is equivalent to [RH-051](../FINDINGS_INDEX.md).

---

## Indexed findings

| ID | Status | Title | Path |
|----|--------|-------|------|
| [RH-060](../FINDINGS_INDEX.md) | narrative | Explicit formula bridge | [explicit-formula-bridge.md](../../../docs/rh/explicit-formula-bridge.md) |

**Do not cite L6 as the PGS proof path.** Use it to translate unresolved L5
targets into familiar notation.

[Stack overview](../SOURCE_STACK.md) · [Full index](../FINDINGS_INDEX.md) · [L5 pole placement](./05-pole-placement-rh.md)