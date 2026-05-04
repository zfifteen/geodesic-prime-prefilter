## Divisor Normalization Identity

The raw-$Z$ quantity exists because the repo wants a normalization in which the
entire prime class lands at one fixed point while composites fall below it.

The construction starts from the divisor normalization load

$$
\kappa(n) = \frac{d(n) \cdot \ln(n)}{e^{2}}
$$

and then passes that load through the Z-transform:

$$
Z(n) = \frac{n}{\exp(v \cdot \kappa(n))}
$$

where $v$ is the normalization scaling parameter.

For the prime-gap structure program in this repository, the distinguished value is

$$
v = \frac{e^{2}}{2}
$$

because it produces an exact cancellation. Substitute the Divisor Normalization Equation into the Z-transform:

$$
Z(n) = \frac{n}{\exp\left(v \cdot \frac{d(n) \cdot \ln(n)}{e^{2}}\right)}
$$

Now set $v = e^{2}/2$:

$$Z(n) = \frac{n}{\exp\left(\frac{e^{2}}{2} \cdot \frac{d(n) \cdot \ln(n)}{e^{2}}\right)}$$

$$Z(n) = \frac{n}{\exp\left(\frac{d(n)}{2} \cdot \ln(n)\right)}$$

$$Z(n) = \frac{n}{n^{d(n)/2}}$$

$$Z(n) = n^{1 - d(n)/2}$$

So the **Divisor Normalization Identity** (DNI) $Z(n) = n^{1 - d(n)/2}$ is

$$
Z(n) = n^{1 - d(n)/2}
$$

This has an immediate effect:

- Prime: $d(p) = 2$, so $Z(p) = 1$
- Semiprime with two distinct prime factors: $d(n) = 4$, so $Z(n) = 1/n$
- Composite in general: $d(n) > 2$, so $Z(n) < 1$

Under the exact DNI, the entire prime class collapses to the fixed-point locus $Z = 1.0$. Composites are pushed strictly below that locus.

This fixed-point collapse is the mathematical base of the repository. It is
the invariant behind both the prime-gap theorem and the downstream
deterministic filter.

