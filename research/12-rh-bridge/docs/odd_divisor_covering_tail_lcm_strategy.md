# Odd Divisor-Covering Tail LCM Strategy

Date: 2026-05-24

Status: candidate proof approach for the Odd Divisor-Covering Tail Theorem.

The Odd Divisor-Covering Tail Theorem asks for

$$
\#\{2m\in[X,2X]:a(2m)\ge H\}
\ll
X(\log X)^B/H^2.
$$

Long even-channel age means every relevant odd offset before `2m` is
composite. This note outlines an LCM-growth approach to count such centers.

## Covering Certificates

Fix an even center `2m` and an odd offset interval

$$
\mathcal J_H=\{1,3,5,\ldots,H'\}.
$$

A full odd-offset divisor cover assigns to each `j in J_H` an odd proper
divisor

$$
d_j>1
$$

such that

$$
d_j\mid 2m-j.
$$

Equivalently, the center satisfies the congruence

$$
2m\equiv j\pmod{d_j}.
$$

A covering certificate is the list of congruences

$$
\{2m\equiv j\pmod{d_j}:j\in\mathcal J_H\}.
$$

## Counting A Fixed Certificate

For any compatible certificate, the center `2m` lies in one residue class
modulo

$$
L=\operatorname{lcm}_{j\in\mathcal J_H}d_j.
$$

Therefore the number of centers in `[X,2X]` satisfying that fixed certificate
is at most

$$
O(X/L+1).
$$

If every full cover forces a compatible subcertificate with

$$
L\ge cH^2/(\log X)^B,
$$

then each such subcertificate has at most

$$
O(X(\log X)^B/H^2+1)
$$

centers.

This is the desired tail scale.

## Candidate LCM-Growth Lemma

The needed combinatorial statement is:

> **Odd Cover LCM-Growth Lemma.**
> Every complete proper-divisor cover of the odd offsets
> $$
> \{1,3,\ldots,H'\}
> $$
> arising from numbers `2m-j` contains a compatible subcertificate whose
> divisor moduli have least common multiple at least
> $$
> cH^2/(\log X)^B.
> $$

This lemma would convert complete positive-excess persistence into a large
modulus constraint on the even center.

## Canonical Certificate Choice

To avoid arbitrary overcounting, the proof should use a deterministic
certificate rule, such as:

```text
d_j = least odd proper divisor of 2m-j.
```

Then every persistent even center has exactly one least-divisor covering word.
The counting problem becomes a count of possible least-divisor words whose
congruence LCM is too small.

## Required Additional Bounds

The LCM-growth strategy needs three ingredients.

1. **Least-divisor word entropy.**
   The number of possible low-LCM covering words must be small enough not to
   overwhelm the `X/L` saving.

2. **LCM growth for full covers.**
   Complete odd-offset coverage must force enough independent divisor moduli
   to make `L` at least quadratic in `H` up to logarithms.

3. **Compatibility control.**
   Congruence systems that are incompatible contribute zero centers. The proof
   must count only compatible systems without replacing them by a much larger
   unconstrained family.

## Main Obstacles

**Small-modulus covering systems.**
Odd offsets can be covered by overlapping small divisor channels. The proof
must show that such overlap cannot persist for length `H` with too many
centers.

**Certificate nonuniqueness.**
Without a canonical least-divisor rule, one center can have many certificates.
Counting all certificates would overcount badly.

**LCM is not automatically large.**
Many offsets can share divisor channels. Full coverage alone does not
immediately imply independent congruence constraints.

**No current PGS theorem supplies LCM growth.**
Current GWR and divisor-count results identify local chamber order. They do
not prove an LCM-growth law for odd-offset divisor covers.

## Result

The Odd Divisor-Covering Tail Theorem can be attacked by proving an
LCM-growth law for canonical least-divisor covering words. This is a concrete
PGS-native combinatorial target, but it is a new theorem obligation.
