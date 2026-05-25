# Pole And Trivial-Zero Capacity Decomposition

Date: 2026-05-24

Status: decomposition note for the Transport Capacity Balance Identity.

The Transport Capacity Balance Identity is

$$
T_-(z)=D_+(z),
\qquad
T_+(z)=D_-(z).
$$

The transport reservoir has two parts:

```text
pole pair + trivial-zero transport atoms.
```

This note separates their capacity contributions.

## Decomposition

Write

$$
T_+(z)=T^{\mathrm{pole}}_+(z)+T^{\mathrm{triv}}_+(z),
$$

and

$$
T_-(z)=T^{\mathrm{pole}}_-(z)+T^{\mathrm{triv}}_-(z).
$$

Then the balance identity becomes

$$
T^{\mathrm{pole}}_-(z)+T^{\mathrm{triv}}_-(z)=D_+(z),
$$

and

$$
T^{\mathrm{pole}}_+(z)+T^{\mathrm{triv}}_+(z)=D_-(z).
$$

The pole and trivial-zero pieces do not need to match packet demand
separately. Their sum must match sidewise.

## Pole-Pair Requirement

The pole pair is finite and located at centered radius

$$
|y|=\frac12.
$$

Its analytic requirements are:

1. determine the signed odd capacities of the two pole atoms;
2. verify their contribution to `T_+` and `T_-` exactly;
3. preserve their exact contribution to
   $$
   -\frac1s-\frac1{s-1}.
   $$

The pole-pair obstruction is finite capacity. If the pole pair alone does not
match the sidewise packet drift demand, the trivial-zero reservoir must supply
the remaining capacity.

## Trivial-Zero Requirement

The trivial-zero transport reservoir is infinite, with centered radii

$$
2m+\frac12,
\qquad
m\ge0.
$$

Its analytic requirements are:

1. identify the signed odd capacities arising from the gamma/trivial-zero
   expansion;
2. prove convergence of the sign-separated capacity sums;
3. show that the remaining sidewise demand after the pole contribution is
   matched exactly:
   $$
   T^{\mathrm{triv}}_-(z)=D_+(z)-T^{\mathrm{pole}}_-(z),
   $$
   $$
   T^{\mathrm{triv}}_+(z)=D_-(z)-T^{\mathrm{pole}}_+(z).
   $$

The trivial-zero obstruction is regularized infinite capacity. The proof must
separate genuine transport capacity from gamma regularization constants
without reintroducing negative zero-radius cost.

## Resulting Target

The Transport Capacity Balance Identity reduces to two component tasks:

```text
finite pole-pair capacity calculation
+ infinite trivial-zero capacity balance
-> sidewise packet drift demand.
```

The finite pole task is explicit. The infinite trivial-zero task is the main
analytic burden.

The explicit pole-pair capacity calculation is recorded in
[Pole-Pair Odd Capacity](pole_pair_odd_capacity.md).

The first structural analysis of the infinite reservoir is recorded in
[Trivial-Zero Reservoir Capacity](trivial_zero_reservoir_capacity.md).
