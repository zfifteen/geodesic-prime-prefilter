# Symmetric Trivial-Zero Capacity Requirements

Date: 2026-05-24

Status: requirements note for the post-one-sided completion-capacity route.

The one-sided trivial-zero regularization cannot be closed from the existing
GWR lower-production data. The completion side must therefore use a symmetric
or sign-regularized capacity decomposition in which the trivial-zero reservoir
contributes positive odd transport capacity as well as negative odd transport
capacity.

The raw trivial-zero atoms do not do this by themselves. A positive odd
capacity from the trivial-zero side requires a signed decomposition of the
same completion atoms.

## Raw Trivial-Zero Atom

In the completed coordinate

$$
u=s-\frac12,
$$

the `m`th trivial-zero transport atom sits at

$$
y_m=-2m-\frac12,
\qquad m\ge0.
$$

Its raw coefficient is `+1`, so its odd capacity is

$$
J_z(y_m)<0.
$$

Thus the raw atom contributes only negative odd capacity.

## Minimal Sign-Regularized Split

A symmetric capacity representation must preserve the same analytic atom while
allowing a signed transport budget. The minimal local split has the form

$$
\delta_{y_m}
=
(1+\alpha_m(z))\delta_{y_m}
-
\alpha_m(z)\delta_{y_m},
\qquad
\alpha_m(z)\ge0.
$$

This changes no completion term atom by atom. It introduces a positive
transport capacity from the negative share at the same nonzero radius:

$$
T_{+,m}^{\mathrm{triv,sym}}(z)
=
\alpha_m(z)|J_z(y_m)|.
$$

The negative side receives

$$
T_{-,m}^{\mathrm{triv,sym}}(z)
=
(1+\alpha_m(z))|J_z(y_m)|.
$$

The packetwise negative folded cost created by the positive-capacity share is

$$
C_{-,m}^{\mathrm{triv,sym}}(z)
=
\alpha_m(z)K_z(y_m).
$$

Since

$$
|y_m|\ge\frac12
$$

for every trivial-zero atom, any negative folded-cost mass assigned from this
split remains outside every packet excursion `M_{p,q}<1/2`.

Moreover,

$$
\frac{T_{+,m}^{\mathrm{triv,sym}}(z)}
{C_{-,m}^{\mathrm{triv,sym}}(z)}
=
|y_m|.
$$

For any nonzero finite combination of such splits,

$$
\frac{T_+^{\mathrm{triv,sym}}(z)}
{C_-^{\mathrm{triv,sym}}(z)}
$$

is a `K_z`-weighted average of the radii `|y_m|`, hence at least `1/2`.

## Required Conditions

A usable symmetric trivial-zero capacity decomposition must satisfy five
conditions.

1. **Exact assembly.**
   The signed split must sum back to the original gamma/trivial-zero
   transport atoms:
   $$
   \sum_{m\ge0}
   \left((1+\alpha_m)\delta_{y_m}-\alpha_m\delta_{y_m}\right)
   =
   \sum_{m\ge0}\delta_{y_m}.
   $$

2. **Positive trivial-zero capacity.**
   The positive capacity side must be available from the trivial-zero
   reservoir:
   $$
   T_+^{\mathrm{triv,sym}}(z)
   =
   \sum_{m\ge0}\alpha_m(z)|J_z(y_m)|.
   $$

3. **Sidewise balance.**
   The pole plus sign-regularized trivial-zero capacities must match packet
   drift demands:
   $$
   T_+^{\mathrm{pole}}(z)+T_+^{\mathrm{triv,sym}}(z)=D_-(z),
   $$
   $$
   T_-^{\mathrm{pole}}(z)+T_-^{\mathrm{triv,sym}}(z)=D_+(z).
   $$

4. **Controlled summation.**
   The positive-capacity split must have finite folded negative cost:
   $$
   \sum_{m\ge0}\alpha_m(z)K_z(y_m)<\infty,
   $$
   and the remaining negative-capacity side must be regularized in a way
   compatible with the completed gamma factor.

5. **No negative zero-radius leakage.**
   All negative folded-cost mass introduced by the split is supported at
   `|y_m| >= 1/2`. Zero-radius constants remain outside the negative
   packetwise folded-cost measure.

## Principal Analytic Obstacles

The construction above identifies the shape of a symmetric decomposition, but
it does not yet prove the bridge. Four analytic obstacles remain.

**Canonical normalization.**
The split

$$
\delta_{y_m}=(1+\alpha_m)\delta_{y_m}-\alpha_m\delta_{y_m}
$$

preserves exact assembly for any nonnegative `alpha_m`. Without a deterministic
normalization, the positive capacity is a gauge choice rather than a theorem.
The proof must specify an intrinsic rule for `alpha_m(z)`.

**Regularized negative side.**
The raw negative trivial-zero capacity already diverges logarithmically. Adding
`alpha_m` increases that side. The proof must define the finite part or
renormalized sidewise capacity without changing the completed quotient.

**Compatibility in `z`.**
The allocation may be formulated at the folded-kernel level, but it must remain
compatible with a single completed analytic correction. Arbitrary `z`-wise
choices do not automatically define an analytic completion representation.

**Exchange of global sums.**
Packet drift demands, trivial-zero capacities, and allocation weights must be
summable strongly enough to justify sign splitting and packetwise transport.
Net cancellation is not sufficient.

## Resulting Target

The next completion-side target is the following lemma.

> **Canonical Symmetric Trivial-Zero Transport Lemma.**
> For each `z > 0` in the folded-kernel domain, the gamma/trivial-zero
> completion correction admits a deterministic sign-regularized atom split
> at the existing trivial-zero radii `|y_m| >= 1/2` such that exact assembly,
> positive trivial-zero transport capacity, sidewise drift balance, controlled
> summation, and no negative zero-radius leakage all hold.

This lemma replaces the failed one-sided regularization as the live
completion-side bridge into the Chamber-Deconvolved Reciprocal Balance Lemma.
