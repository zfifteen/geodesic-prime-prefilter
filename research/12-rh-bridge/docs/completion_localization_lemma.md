# Completion Localization Lemma

Date: 2026-05-24

Status: completion-side target lemma for the Chamber-Deconvolved Reciprocal
Balance Lemma.

Let `P(p,q)` be a chamber packet and let

$$
M_{p,q}=\max_{n\in P(p,q)}|x_n|.
$$

For `z > 0`, let `\eta_{p,q,z}` be the packetwise completion correction in
the centered coordinate. Write its Jordan decomposition as

$$
\eta_{p,q,z}=\eta^+_{p,q,z}-\eta^-_{p,q,z},
$$

where `\eta^+_{p,q,z}` and `\eta^-_{p,q,z}` are positive mutually singular
measures. The measure `\eta^-_{p,q,z}` is the packetwise negative
folded-cost measure.

## Lemma Statement

> **Completion Localization Lemma.**
> For every chamber packet `P(p,q)` and every `z > 0`, the packetwise negative
> folded-cost measure satisfies
> $$
> \operatorname{supp}(\eta^-_{p,q,z})
> \subseteq
> \{x:|x|\ge M_{p,q}\}.
> $$

## Consequence

Under the support condition,

$$
\int |x|K_z(x)\,d\eta^-_{p,q,z}(x)
\ge
M_{p,q}\int K_z(x)\,d\eta^-_{p,q,z}(x).
$$

Therefore the completion transport radius

$$
\rho_{p,q}(z)=
\frac{\int |x|K_z(x)\,d\eta^-_{p,q,z}(x)}
{\int K_z(x)\,d\eta^-_{p,q,z}(x)}
$$

satisfies

$$
\rho_{p,q}(z)\ge M_{p,q}
$$

whenever the denominator is positive. If the denominator is zero, there is no
negative folded-cost contribution to bound.

This lemma is completion-side only. It adds no new arithmetic assumption on
the prime-power packet.

The standard completion terms are decomposed for this support condition in
[Completion Term Decomposition For Localization](completion_term_decomposition_for_localization.md).
