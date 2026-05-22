# Reviewer Map

Check the bundle in this order:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression -> pole placement -> RH sentence
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

3. [Pole placement](pole-placement.md)

   Check that pole placement is downstream of the DNI ratio. The nontrivial
   poles of `R(s)` are the nontrivial zeros of `zeta(s)` read through the
   logarithmic derivative.

4. [Critical line and zero geometry](critical-line-and-zero-geometry.md)

   Check that the critical-line sentence is stated as the RH-side analytic
   reading:

   $$
   \mathrm{Re}(\rho)=1/2
   $$

   for every nontrivial zero `rho` of `zeta(s)`, or equivalently every
   nontrivial pole of `R(s)`.

5. [Status ledger](status-ledger.md)

   Check that proved theorem, exact zeta compression, explanatory consequence,
   measured evidence, invalidated routes, and proof targets remain separate.

## Status Discipline

- Proved local PGS theorems are controlled by `PROOF.md`.
- Exact DNI-to-zeta compression is controlled by the bridge identity.
- Pole placement is downstream analytic language.
- The RH sentence is a global proof target unless the active page supplies the
  full proof.
- Explicit-formula material is a downstream analytic bridge unless a full proof
  is written there.

## Fast Failure Checks

Reject the page for revision if it:

- starts from zero geometry before divisor counts;
- treats RH as an input to PGS local theorems;
- calls proved local PGS theorems empirical approximations;
- treats the exact DNI ratio as a full pole-placement proof without proving
  pole placement;
- uses explicit-formula terms to imply a new theorem without writing the proof.
