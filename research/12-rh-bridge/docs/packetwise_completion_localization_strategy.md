# Packetwise Completion Localization Strategy

Date: 2026-05-24

Status: strategy for proving packetwise completion localization after the
Direct Full-Radius BDH closure.

The remaining bridge input is:

> **Packetwise Completion Localization.**  
> Assign the pole, gamma, trivial-zero, and main-term completion correction to
> chamber packets so that every negative folded-cost contribution used to
> cancel packet drift has transport radius at least
> $$
> M_{p,q}=\max_{n\in P(p,q)}|x_n|.
> $$

## Radius Geometry

For consecutive primes `p<q`, every packet point satisfies `p<n<=q`, hence

$$
M_{p,q}\le {1\over2}\log {q\over p}.
$$

By Bertrand's theorem, `q<2p`, so

$$
M_{p,q}< {1\over2}\log2< {1\over2}.
$$

The pole pair has centered radius `1/2`, and the trivial-zero atoms have
centered radii

$$
2m+{1\over2},
\qquad
m\ge0.
$$

Therefore every pole or trivial-zero transport atom lies outside every packet
excursion:

$$
|x|\ge {1\over2}>M_{p,q}.
$$

## Zero-Radius Constants

The only completion terms not protected by radius are the zero-radius
regularization constants:

```text
gamma regularization constants
+ scale/main constant
```

At `x=0`,

$$
J_z(0)=0,
\qquad
K_z(0)>0.
$$

Thus a negative zero-radius assignment creates negative folded even cost with
no odd transport capacity. It cannot cancel packet drift. The localization
rule is:

$$
\eta^-_{p,q,z}\text{ receives no zero-radius mass.}
$$

Zero-radius constants are assigned to the global even background or to
packetwise nonnegative folded parts.

## Localization Proof Skeleton

With this assignment:

1. every negative drift-canceling atom comes from the pole/trivial-zero
   transport reservoir;
2. every atom in that reservoir has radius at least `1/2`;
3. every packet excursion has `M_{p,q}<1/2`;
4. therefore
   $$
   \operatorname{supp}(\eta^-_{p,q,z})
   \subseteq
   \{x:|x|\ge M_{p,q}\}.
   $$

Consequently

$$
\rho_{p,q}(z)\ge M_{p,q}.
$$

## Remaining Inputs Beyond Localization

Localization alone does not construct the full packetwise completion
assembly. The remaining inputs are:

1. **Transport capacity balance.**
   The safe pole/trivial-zero transport reservoir must have enough signed odd
   capacity to match the packet drifts `D_{p,q}(z)`.

2. **Exact assembly.**
   Packet allocations must sum back to the standard completion correction
   $$
   -{1\over s}-{1\over s-1}
   +{1\over2}\log\pi
   -{1\over2}{\Gamma'\over\Gamma}(s/2).
   $$

3. **Controlled summation.**
   The packetwise negative folded costs must be summable. The closed Direct
   Full-Radius BDH route supplies the analytic residual control needed for
   this side of the assembly.

4. **Analytic compatibility in `z`.**
   The allocation may be built at the folded-kernel level, but its assembled
   transform must equal the completion correction on the common domain.

## Interface With The Folded Packet Drift Inequality

Once transport capacity and exact assembly are supplied, localization gives

$$
\rho_{p,q}(z)\ge M_{p,q}.
$$

The packet arithmetic gives

$$
|D_{p,q}(z)|\le M_{p,q}R_{p,q}(z).
$$

Therefore

$$
|D_{p,q}(z)|\le \rho_{p,q}(z)R_{p,q}(z),
$$

which is the Aggregate Completion-Cost Bound and hence the Folded Packet
Drift Inequality.

## Result

Packetwise localization itself follows from three concrete facts:

```text
M_{p,q}<1/2
+ pole/trivial-zero transport radii >=1/2
+ zero-radius constants excluded from negative folded cost
```

The remaining completion-side work is no longer support localization. It is
transport capacity balance plus exact assembly of the standard completion
correction.
