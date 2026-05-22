# PGS to RH

Exact divisor-count structure is the source; RH is the downstream
pole-placement sentence after that structure is compressed into zeta language.

The required reading order is:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-side residual closure -> pole placement/RH sentence
```

## What This Folder Does

`docs/rh` is the affirmative narrative spine for the PGS-to-RH documentation
bundle. It starts from arithmetic objects the reader can inspect directly:
divisor counts, consecutive prime-gap interiors, and the selected integer
inside each nonempty gap. It then moves through the local theorem authority,
the exact DNI-to-zeta compression, the source-side residual closure, and the
pole-placement language that gives the RH-facing sentence.

This folder is the bundle index and source-order guide. The FAQ remains the
objection-handling surface. The `research/12-rh-bridge` tree remains the
workbench where bridge details, downstream translation notes, and draft
technical artifacts live.

## Table Of Contents

| Page | Role | Status |
| --- | --- | --- |
| [Source Order](source-order.md) | Establishes the direction from integer objects to RH language. | explanatory consequence |
| [DNI-to-Zeta Compression](dni-to-zeta-compression.md) | Shows the coefficient bridge from divisor counts to $R(s)=-\zeta'(s)/\zeta(s)$. | exact zeta compression |
| [Pole Placement](pole-placement.md) | Records how zeros of $\zeta$ become poles of the continued DNI ratio. | exact zeta compression |
| [Off-Critical Pole Exclusion](off-critical-pole-exclusion.md) | Gives the source-side residual test for excluding nontrivial off-critical poles. | source-side residual closure |
| [Critical Line And Zero Geometry](critical-line-and-zero-geometry.md) | Names the critical strip and critical line as downstream coordinate language. | explanatory consequence |
| [Explicit Formula Bridge](explicit-formula-bridge.md) | Connects $R(s)$ to $\Lambda(n)$, $\psi(x)$, and zero terms. | downstream translation bridge |
| [Status Ledger](status-ledger.md) | Separates proved theorems, exact compression, source-side closure, and downstream translation. | reviewer control |
| [Reviewer Map](reviewer-map.md) | Gives the checking order for the bundle. | reviewer control |

## Primary Sources

| Source | Role | Status |
| --- | --- | --- |
| [Root Proof Authority](../../PROOF.md) | Proves the local next-prime rule and the prime-gap interior maximizer theorem. | proved theorem |
| [DNI-to-Zeta Bridge](../../research/12-rh-bridge/docs/dni_rh_bridge.md) | Records the full bridge workbench for the DNI ratio. | exact zeta compression |
| [FAQ](../faq/README.md) | Handles recurring objections and category errors. | objection handling |
| [The Riemann Hypothesis Is Obsolete](../essays/the-riemann-hypothesis-is-obsolete.md) | States the public-facing consequence of starting from the arithmetic source. | explanatory consequence |

## Status Spine

| Source Layer | Object | Status Label |
| --- | --- | --- |
| Divisor counts | Each integer carries `tau(n)`, with primes exactly at `tau(n)=2`. | arithmetic source |
| PGS local theorems | `PROOF.md` controls the next-prime theorem and the interior maximizer theorem. | proved theorem |
| DNI-to-zeta compression | The native DNI series gives `(e^2/2)K(s)/D(s) = -zeta'(s)/zeta(s)`. | exact zeta compression |
| Source-side residual closure | The residual test closes failed identities, independent gap-length freedom, chamber log-weight remainders, and divisor-count remainders. | source-side residual closure |
| Pole placement/RH sentence | Zeros of `zeta` become poles of the continued DNI ratio, and nontrivial off-critical poles have no surviving source-side carrier. | source-side residual closure |
| Explicit-formula bridge | The `R(s) -> Lambda(n) -> psi(x)` path restates the result in classical zero-term and error-term language. | downstream translation bridge |

## Bundle Boundary

The bundle begins with ordered arithmetic and ends with RH vocabulary. Zeta
zeros enter after the divisor-count source and exact compression have been
stated. The FAQ carries objection handling; this folder carries the main claim.
The spine is constructive:

1. Count divisors on the integer line.
2. Read the finite interior between consecutive primes.
3. Apply the local PGS theorems controlled by `PROOF.md`.
4. Compress the same divisor-count source into the DNI zeta ratio.
5. Apply the source-side residual test for off-critical poles.
6. Translate the continued ratio into pole-placement/RH language.
7. Use the explicit-formula bridge only as downstream translation into
   `Lambda`, `psi`, zero-term, and error-term language.

`PROOF.md` controls local PGS theorem status. It does not itself prove RH.
PGS is not an analytical method and does not require a classical zero-estimate
or explicit-formula error-term proof before the source-side RH sentence is
closed.
