# PGS to RH

Exact divisor-count structure is the source; RH is the downstream
pole-placement sentence after that structure is compressed into zeta language.

**Hard rule (not optional):** RH must never drive research design. PGS laws are
upstream. Binding contract for the indexed corpus:
[research/19-rh-corpus/FRAME_CONTRACT.md](../../research/19-rh-corpus/FRAME_CONTRACT.md).

The required reading order is:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> (optional) further source laws still free of zeros
-> only then source-to-spectral transfer, if forced by source
-> only then pole placement/RH sentence, if transfer closes
```

## What This Folder Does

`docs/rh` is the affirmative narrative spine for the PGS-to-RH documentation
bundle. It starts from arithmetic objects the reader can inspect directly:
divisor counts, consecutive prime-gap interiors, and the selected integer
inside each nonempty gap. It then moves through the local theorem authority
and the exact DNI-to-zeta compression. Pole-placement and explicit-formula
pages are **downstream catalog and translation**, not experiment drivers.

This folder is the bundle index and source-order guide. The FAQ remains the
objection-handling surface. **Note (post-archival):** The detailed `research/12-rh-bridge` workbench material (classical completion strategy, loop infrastructure, etc.) has been moved outside the repository to `/Users/velocityworks/prime-gap-structure-archives/2026-05-classical-rh-bridge-completion-route/` due to classical drift and prompt injection concerns. See the pointer at `research/12-rh-bridge/README.md` and the ARCHIVAL_HANDOFF.md there.

The public narrative spine in `docs/rh/` remains, but deep technical workbench content is no longer on the live surface.

For Zero-Excess DNI Phase 1, zero-excess is an exact coordinate
reformulation. The zero-excess floor is integer-side; the critical line is
zeta-side.

## Table Of Contents

| Page | Role | Status |
| --- | --- | --- |
| [Source Order](source-order.md) | Establishes the direction from integer objects to RH language. | explanatory consequence |
| [DNI-to-Zeta Compression](dni-to-zeta-compression.md) | Shows the coefficient bridge from divisor counts to $R(s)=-\zeta'(s)/\zeta(s)$. | exact zeta compression |
| [Pole Placement](pole-placement.md) | Records how zeros of $\zeta$ become poles of the continued DNI ratio. | exact zeta compression |
| [Off-Critical Pole Exclusion](off-critical-pole-exclusion.md) | Records the residual-closure route and the current obstruction to using it as a proof of pole placement. | unresolved proof target |
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
| Zero-Excess DNI | The zero-excess floor is the integer-side coordinate $E(n)=0$ under the $n>1$ prime guard. | exact coordinate reformulation |
| PGS local theorems | `PROOF.md` controls the next-prime theorem and the interior maximizer theorem. | proved theorem |
| DNI-to-zeta compression | The native DNI series gives `(e^2/2)K(s)/D(s) = -zeta'(s)/zeta(s)`; in zero-excess notation the bridge load is $H(n)=\log n+E(n)$, not $E(n)$ alone. | exact zeta compression |
| Source-to-spectral placement | The residual test closes failed identities and coefficient-bookkeeping errors, but the no-extra-carrier argument does not yet rule out zeros carried by the same global zeta object. | unresolved proof target |
| Pole placement/RH sentence | Zeros of `zeta` become poles of the continued DNI ratio. Placing every nontrivial pole on the critical line still requires a source-to-spectral placement theorem. | unresolved proof target |
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
5. Apply the source-side residual test and its current obstruction for
   off-critical poles.
6. Translate the continued ratio into pole-placement/RH language.
7. Use the explicit-formula bridge only as downstream translation into
   `Lambda`, `psi`, zero-term, and error-term language.

`PROOF.md` controls local PGS theorem status. It does not itself prove RH.
The remaining bridge is source-to-spectral placement: chamber geometry and
the $Z=1$ / $E=0$ return law must still be shown to force the nontrivial poles
of the continued DNI ratio onto the critical line.
