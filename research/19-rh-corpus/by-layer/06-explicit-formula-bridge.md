# Layer 6: Explicit formula bridge

**Status mix:** `narrative`  
**Proves RH?** No: downstream translation for reviewers

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

### Formal identities (classical; status narrative in this hub)

On $\operatorname{Re}(s)>1$:

$$
R(s)=-\frac{\zeta'(s)}{\zeta(s)}=\sum_{n\ge 1}\frac{\Lambda(n)}{n^s}.
$$

Chebyshev function and schematic explicit formula:

$$
\psi(x)=\sum_{n\le x}\Lambda(n),
\qquad
\psi(x)=x-\sum_{\rho}\frac{x^{\rho}}{\rho}+\text{elementary terms},
$$

with $\rho$ ranging over nontrivial zeros of $\zeta(s)$ (equivalently, nontrivial
poles of $R(s)$ after continuation; [RH-022](../FINDINGS_INDEX.md)).

**PGS reading:** $\Lambda(n)$ is the packaged prime-power detector recovered from
the same divisor field that selects GWR $w$. The oscillatory sum over $\rho$ is
how classical analysis writes the residual after the main term $x$. Closing L5
([RH-051](../FINDINGS_INDEX.md)) would force every such $\rho$ onto
$\operatorname{Re}(s)=\tfrac12$; that step is **not** proved here.

---

## Source-side vs spectral-side

| Object | Layer | Role |
|--------|-------|------|
| $E(n)$, GWR $w$ | L1 to L2 | Integer gap mechanism |
| $D(s)$, $R(s)$ | L3 | Exact compression |
| Chamber $frac\_pos$ | L4 | Local placement geometry |
| Zero sum over $\rho$ | L6 | Classical oscillatory correction |

Layer 6 is how reviewers **already** talk about primes. PGS adds the upstream
integer read, it does not replace the explicit formula proof machinery.

---

## Super-signal hook (labeled, invalidated)

The former Super-Signal claim was: when GWR witness $w$ has high primorial
resonance ($w\equiv 0\pmod{30}$, 4+ remainder zeros), the gap terminates
immediately ($q=w+1$). That universal twin-gap lock is **invalidated**
([RH-005](../FINDINGS_INDEX.md); CEs $p=17666309$, $p=22284029$). Resonance
remains a **measured pattern** in small regimes only, not a proved local
termination of the oscillatory correction.

Status: **invalidated** at L1 for the twin-gap implication; modular
$z\ge 4\Leftrightarrow 30\mid w$ still proved; any L6 interpretive link is
`narrative` only.

---

## Open placement target (L6 restatement)

The remaining program step is to show that **source-side chamber constraints**
([RH-035](../FINDINGS_INDEX.md)) force the zero sum in the explicit formula to
align with critical-line poles only. That is equivalent to [RH-051](../FINDINGS_INDEX.md).

---

## Indexed findings

| ID | Status | Title | Path |
|----|--------|-------|------|
| [RH-022](../FINDINGS_INDEX.md) | exact | Pole to zero dictionary (upstream of L6) | [pole-placement.md](../../../docs/rh/pole-placement.md) |
| [RH-060](../FINDINGS_INDEX.md) | narrative | Explicit formula bridge | [explicit-formula-bridge.md](../../../docs/rh/explicit-formula-bridge.md) |
| [RH-051](../FINDINGS_INDEX.md) | unresolved | RH sentence restated via zero sum | [status-ledger.md](../../../docs/rh/status-ledger.md) |

**Do not cite L6 as the PGS proof path.** Use it to translate unresolved L5
targets into familiar notation.

[Stack overview](../SOURCE_STACK.md) · [Full index](../FINDINGS_INDEX.md) · [L5 pole placement](./05-pole-placement-rh.md)