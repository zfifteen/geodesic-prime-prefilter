# Reviewer Map

Check the bundle in this order:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-side residual closure -> pole placement/RH sentence
```

The review question is not whether each page says something RH-adjacent. The
question is whether the page preserves the source order and assigns the right
status to each layer.

## What To Check First

1. [Source order](source-order.md)

   Confirm that the document begins from divisor counts and PGS local
   theorems, not from zeta zeros, pole language, PNT, or RH.

2. [DNI-to-zeta compression](dni-to-zeta-compression.md)

   Check the exact bridge:

   $$
   D(s)=\zeta(s)^2,
   \qquad
   K(s)=-D'(s)/e^2,
   \qquad
   R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
   =-\frac{\zeta'(s)}{\zeta(s)}.
   $$

   This is the compression layer. It must not be presented as the source of
   PGS local theorems.

3. [Off-critical pole exclusion](off-critical-pole-exclusion.md)

   Check the source-side residual test. A claimed off-critical pole must name
   a surviving source residual: a failed identity in `D,K,R`, independent
   endpoint or gap-length freedom, a chamber log-weight remainder, or an extra
   divisor-count field. A conclusion-only residual does not supply a
   mathematical carrier.

4. [Pole placement](pole-placement.md)

   Check that pole placement is downstream of the DNI ratio and source-side
   residual closure. The nontrivial poles of `R(s)` are the nontrivial zeros of
   `zeta(s)` read through the logarithmic derivative.

5. [Critical line and zero geometry](critical-line-and-zero-geometry.md)

   Check that the critical-line sentence is stated as the RH-side analytic
   reading of the source-side residual closure:

   $$
   \mathrm{Re}(\rho)=1/2
   $$

   for every nontrivial zero `rho` of `zeta(s)`, or equivalently every
   nontrivial pole of `R(s)`.

6. [Status ledger](status-ledger.md)

   Check that proved theorem, exact zeta compression, explanatory consequence,
   measured evidence, invalidated routes, source-side residual closure, and
   downstream translation bridges remain separate.

## Status Discipline

- Proved local PGS theorems are controlled by `PROOF.md`.
- Exact DNI-to-zeta compression is controlled by the bridge identity.
- Source-side off-critical-pole residual closure is controlled by
  `off-critical-pole-exclusion.md`.
- Pole placement/RH language is downstream analytic language for that closed
  source-side state.
- `PROOF.md` does not itself prove RH.
- Explicit-formula material is downstream analytic translation into
  `Lambda`, `psi`, zero-term, and error-term language. It is not a
  prerequisite for the PGS-to-RH proof path.
- PGS is not an analytical method and does not require a classical
  zero-estimate or error-term proof to close the source-side RH sentence.

## Fast Failure Checks

Reject the page for revision if it:

- starts from zero geometry before divisor counts;
- treats RH as an input to PGS local theorems;
- calls proved local PGS theorems empirical approximations;
- treats `PROOF.md` as proving RH rather than the local PGS theorems;
- treats explicit-formula terms as prerequisites for the PGS-to-RH path;
- turns downstream analytic translation into a source-side inference rule.
