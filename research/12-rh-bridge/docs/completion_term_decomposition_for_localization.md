# Completion Term Decomposition For Localization

Date: 2026-05-24

Status: completion-side decomposition note for the Completion Localization
Lemma.

The completed logarithmic derivative is

$$
Q(s)=-\frac{\xi'(s)}{\xi(s)}
=
R(s)
-\frac1s
-\frac1{s-1}
+\frac12\log\pi
-\frac12\frac{\Gamma'}{\Gamma}(s/2),
$$

where

$$
R(s)=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The packet localization condition asks which completion terms can contribute
to the packetwise negative folded-cost measure

$$
\eta^-_{p,q,z}
$$

at centered transport coordinates satisfying

$$
|x|<M_{p,q},
\qquad
M_{p,q}=\max_{n\in P(p,q)}|x_n|.
$$

## Packet Excursion Bound

For consecutive primes `p < q`, every packet point satisfies `p < n <= q`.
Therefore

$$
|x_n|\le\frac12\log\frac qp.
$$

By Bertrand's theorem, `q < 2p`, so

$$
M_{p,q}<\frac12\log2<\frac12.
$$

Thus any completion contribution supported at centered radius at least `1/2`
automatically satisfies the localization condition.

## Term Decomposition

| Completion term | Centered support radius | Localization status |
| --- | ---: | --- |
| Pole pair `-1/s - 1/(s-1)` | `1/2` | safe |
| Trivial-zero atoms from the gamma factor | `2m + 1/2`, `m >= 0` | safe |
| Gamma regularization constants | `0` | possible violator |
| Scale/main constant `1/2 log pi` | `0` | possible violator |

## Pole Pair

The pole terms are centered at `s = 0` and `s = 1`, hence at

$$
u=s-\frac12=\pm\frac12.
$$

Their transport radius is `1/2`. Since

$$
M_{p,q}<\frac12,
$$

the pole pair cannot violate

$$
|x|\ge M_{p,q}.
$$

## Trivial-Zero Part Of The Gamma Factor

The gamma factor contributes the trivial-zero structure at

$$
s=-2m,\qquad m\ge0.
$$

In the centered coordinate,

$$
u=-2m-\frac12,
$$

so the folded radius is

$$
|u|=2m+\frac12\ge\frac12.
$$

These atoms are outside every chamber packet excursion because

$$
M_{p,q}<\frac12.
$$

Thus the trivial-zero part of the gamma factor is localization-safe.

## Zero-Radius Completion Terms

The terms not automatically protected by radius are the regularized constants:

```text
gamma regularization constants
+ scale/main constant 1/2 log pi.
```

Their natural centered support is `x = 0`. For every nonempty chamber packet,

$$
M_{p,q}>0,
$$

so an atom at `x = 0` lies inside the forbidden region

$$
|x|<M_{p,q}.
$$

These terms can violate the Completion Localization Lemma only if they enter
the packetwise negative folded-cost measure. If their packetwise assignment is
nonnegative, or if they are allocated globally outside the negative
folded-cost part, they do not obstruct localization.

## Result

The only completion terms that can violate packet localization are the
zero-radius regularization/main constants. The pole pair and the trivial-zero
atoms are supported at centered radius at least `1/2`, while every prime-gap
packet has

$$
M_{p,q}<\frac12.
$$

The remaining completion-side proof obligation is therefore:

> Show that the zero-radius completion constants do not contribute negative
> packetwise folded cost.

Once that is proved, the support condition in the Completion Localization
Lemma follows.

The zero-radius assignment rule is recorded in
[Zero-Radius Completion Constant Assignment](zero_radius_completion_constant_assignment.md).
