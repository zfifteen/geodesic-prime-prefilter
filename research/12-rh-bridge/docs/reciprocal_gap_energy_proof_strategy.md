# Reciprocal Gap-Energy Proof Strategy

Date: 2026-05-24

Status: candidate proof strategy and obstruction note for the Reciprocal
Gap-Energy Theorem.

The Reciprocal Gap-Energy Theorem asks for

$$
\sum_q\frac{g(q)^2\log q}{q^2}<\infty.
$$

The dyadic form is

$$
\sum_{X<q\le2X}g(q)^2
\le
C X(\log X)^B.
$$

This is a global endpoint-chain second-moment theorem. It is equivalent to a
large-gap tail law for zero-excess returns.

## Tail Formulation

For a dyadic block, define

$$
N_X(H)=\#\{q:X<q\le2X,\ g(q)\ge H\}.
$$

Using the layer-cake identity for nonnegative integers,

$$
\sum_{X<q\le2X}g(q)^2
\asymp
\sum_{H\ge1}H\,N_X(H).
$$

A sufficient large-gap tail bound is

$$
\boxed{
N_X(H)\le
C\frac{X(\log X)^B}{H^2}
}
$$

uniformly for `1 <= H <= X`.

Then

$$
\sum_{H\le X}H\,N_X(H)
\le
C X(\log X)^B\sum_{H\le X}\frac1H
\le
C'X(\log X)^{B+1}.
$$

This gives the dyadic second-moment bound with one additional logarithm.

Thus the reciprocal gap-energy theorem can be proved by a PGS-native
large-gap tail theorem.

## PGS-Native Reading

A large prime gap is a long positive-excess excursion:

```text
zero-excess endpoint -> positive-excess chamber -> next zero-excess endpoint
```

The required tail theorem says that long positive-excess excursions have
sufficiently small frequency in the endpoint chain.

In PGS terms, the missing law is:

> **Zero-Excess Return-Time Tail Theorem.**
> In each dyadic endpoint block, chambers of width at least `H` occur with
> frequency at most `C X(log X)^B / H^2`.

This is stronger than local GWR ordering. It is a global law about return
times to the zero-excess floor.

## Possible Proof Inputs

A proof would need at least one of the following structural inputs.

1. **Endpoint-chain occupancy.**
   A direct theorem bounding how often the endpoint chain can leave gaps of
   length `H` inside `[X,2X]`.

2. **Divisor-field recurrence.**
   A theorem showing that the divisor-count field forces zero-excess returns
   with a second-moment return-time bound.

3. **Chamber grammar tail law.**
   A proved finite-state or finite-memory grammar with quantitative tail
   control for chamber widths, not merely measured transition concentration.

4. **Gap-energy bootstrap.**
   A direct weighted estimate on
   $$
   \sum_{X<q\le2X}g(q)^2
   $$
   derived from exact endpoint-chain partition identities.

## What Existing Machinery Supplies

Current PGS results supply exact local facts:

- every prime endpoint is a zero-excess return;
- every chamber interior is positive-excess;
- the GWR selector is the leftmost minimum-excess interior point;
- finite-base and residual records control specific branches or finite
  surfaces.

These facts do not currently imply a tail bound for `N_X(H)`.

A chamber can be long while still having a perfectly valid selected interior
minimum. The selector theorem does not count how often such long chambers
occur.

## Existing Global Results

The repo's grammar and motif surfaces show measured compression of chamber
state transitions. They are not all-scale tail theorems. They do not prove

$$
N_X(H)\le C X(\log X)^B/H^2.
$$

The zero-excess DNI work gives the correct return-time language, but it does
not prove return-time frequency bounds.

Thus the reciprocal gap-energy theorem cannot currently be reduced to an
existing PGS global result.

## Required New Argument

The needed argument is fundamentally global:

```text
positive-excess chamber lengths have a square-summable reciprocal tail.
```

The minimal new theorem is the Zero-Excess Return-Time Tail Theorem above. It
would immediately imply the dyadic reciprocal gap-energy estimate, then the
Reciprocal Endpoint Occupancy Theorem, then the endpoint drift counterterm for
the Chamber-Centered Von Mangoldt Finite-Part Principle.

This is the current endpoint-chain obstruction.
