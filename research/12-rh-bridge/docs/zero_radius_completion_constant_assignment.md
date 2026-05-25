# Zero-Radius Completion Constant Assignment

Date: 2026-05-24

Status: completion-side assignment note for the Completion Localization Lemma.

The completion-term decomposition leaves only the zero-radius terms as
possible localization violators:

```text
gamma regularization constants
+ scale/main constant 1/2 log pi.
```

In the centered transport coordinate, these terms have support at

$$
x=0.
$$

For every nonempty chamber packet,

$$
M_{p,q}=\max_{n\in P(p,q)}|x_n|>0,
$$

so a negative packetwise atom at `x = 0` would violate the support condition

$$
|x|\ge M_{p,q}.
$$

## Zero Odd-Transport Capacity

The odd kernel is

$$
J_z(x)=\frac{x}{z+x^2}.
$$

At the zero-radius point,

$$
J_z(0)=0.
$$

The even folded kernel is

$$
K_z(x)=\frac{1}{z+x^2},
$$

so

$$
K_z(0)=\frac1z>0.
$$

Therefore a negative zero-radius packetwise assignment would contribute
negative folded even cost but no odd drift cancellation:

$$
\text{odd capacity}=0,
\qquad
\text{negative even cost}>0.
$$

Such an assignment cannot improve the transport inequality. It only lowers
the completion transport radius.

## Assignment Rule

> **Zero-Radius Completion Constant Assignment Rule.**
> Gamma regularization constants and the scale/main constant are not assigned
> to the packetwise negative folded-cost measure
> $$
> \eta^-_{p,q,z}.
> $$
> They are assigned either to the global even normalization background or to a
> nonnegative packetwise folded contribution.

Under this rule, their contribution to the negative packet cost is

$$
C^-_{p,q,\mathrm{zero}}(z)=0.
$$

Thus the zero-radius constants do not violate the Completion Localization
Lemma.

## Result

The zero-radius completion constants have no odd transport capacity. Assigning
them negatively to an individual packet would create pure negative folded cost
at forbidden radius. The transport-compatible assignment is therefore to keep
them out of

$$
\eta^-_{p,q,z}.
$$

With this assignment rule, the only negative folded-cost contributions that
remain in the packetwise completion correction are the pole and trivial-zero
transport terms already shown to lie at radius at least `1/2`, outside every
prime-gap packet excursion.

The global consistency conditions for assembling the packetwise corrections
are recorded in
[Global Completion Negative-Cost Conditions](global_completion_negative_cost_conditions.md).
