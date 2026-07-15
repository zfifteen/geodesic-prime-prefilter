# Layer 6: Explicit formula bridge (translation only)

**Status mix:** `narrative`  
**Proves RH?** No  
**May drive new work?** **No.** Downstream translation for reviewers only.
Hard rule: [FRAME_CONTRACT.md](../FRAME_CONTRACT.md).

Layer 6 restates the compressed ratio $R(s)$ in classical prime-counting language:
von Mangoldt coefficients, Chebyshev $\psi(x)$, and zero/error terms. It does
not authorize designing PGS experiments from $\Lambda$, $\psi$, or zero sums.

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

## Modular zero lemma (supporting, not a twin-gap lock)

On the fixed remainder vector $M_{v1}=\{2,3,5,7,30,210,2310\}$, four or more
zeros occur if and only if $30\mid w$ ([RH-005](../FINDINGS_INDEX.md);
`PROOF.md`). This is a modular lattice fact. It does not assert a gap-size
lock and does not terminate the L6 oscillatory correction.

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