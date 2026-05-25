# Trivial-Zero Finite-Part Split Obstruction

Date: 2026-05-24

Status: finite-part analysis for the Canonical Alpha Normalization Lemma.

The centered trivial-zero capacity has an explicit finite part. That finite
part controls the net odd contribution of the trivial-zero reservoir. It does
not determine the positive/negative sidewise split parameters `alpha_m(z)`.

This is the core obstruction to extracting `alpha_m(z)` directly from the
gamma finite part.

## Centered Raw Capacity

The trivial-zero transport atoms sit at

$$
y_m=-2m-\frac12.
$$

Write

$$
r_m=|y_m|=2m+\frac12.
$$

The raw magnitude of the negative odd capacity is

$$
A_m(z)=|J_z(y_m)|
=
\frac{r_m}{z+r_m^2}.
$$

The partial sums

$$
B_N(z)=\sum_{m=0}^{N}A_m(z)
$$

diverge logarithmically.

## Hadamard Finite Part

Since

$$
r_m=2\left(m+\frac14\right),
$$

set

$$
a=\frac14,
\qquad
t=\frac{\sqrt z}{2}.
$$

Then

$$
A_m(z)
=
\frac14
\left(
\frac{1}{m+a-it}
+
\frac{1}{m+a+it}
\right).
$$

Subtract the harmonic counterterm supplied by the digamma expansion:

$$
\frac{1}{2(m+1)}.
$$

The finite part is

$$
B^{\mathrm{fp}}_{\mathrm{triv}}(z)
=
\sum_{m=0}^{\infty}
\left(
A_m(z)-\frac{1}{2(m+1)}
\right).
$$

Using

$$
\psi(b)
=
-\gamma
+
\sum_{m=0}^{\infty}
\left(
\frac{1}{m+1}-\frac{1}{m+b}
\right),
$$

we obtain

$$
\boxed{
B^{\mathrm{fp}}_{\mathrm{triv}}(z)
=
-\frac12
\left(
\operatorname{Re}\psi\left(\frac14+\frac{i\sqrt z}{2}\right)
+
\gamma
\right).
}
$$

This scalar is the renormalized sidewise difference of the raw one-sided
trivial-zero odd contribution. It is a finite-part value, not automatically a
nonnegative capacity magnitude.

## Effect Of The Alpha Split

Apply the sign-regularized split

$$
\delta_{y_m}
=
(1+\alpha_m(z))\delta_{y_m}
-
\alpha_m(z)\delta_{y_m}.
$$

Assume the added split has finite odd capacity:

$$
\sum_{m\ge0}\alpha_m(z)A_m(z)<\infty.
$$

Then the positive trivial-zero capacity is

$$
T_+^{\mathrm{triv,\alpha}}(z)
=
\sum_{m\ge0}\alpha_m(z)A_m(z),
$$

while the renormalized negative side is

$$
T_-^{\mathrm{triv,\alpha}}(z)
=
B^{\mathrm{fp}}_{\mathrm{triv}}(z)
+
\sum_{m\ge0}\alpha_m(z)A_m(z).
$$

For this to be read as a nonnegative sidewise capacity, the chosen split must
also satisfy

$$
B^{\mathrm{fp}}_{\mathrm{triv}}(z)
+
\sum_{m\ge0}\alpha_m(z)A_m(z)
\ge0.
$$

Therefore

$$
\boxed{
T_-^{\mathrm{triv,\alpha}}(z)
-
T_+^{\mathrm{triv,\alpha}}(z)
=
B^{\mathrm{fp}}_{\mathrm{triv}}(z).
}
$$

The finite part fixes only the difference of the two sidewise capacities. It
does not determine the size of either side separately.

## Consequence For Sidewise Balance

The pole capacities are equal:

$$
T_+^{\mathrm{pole}}(z)=T_-^{\mathrm{pole}}(z).
$$

Thus the sidewise Transport Capacity Balance Identity implies the net
condition

$$
\boxed{
D_+(z)-D_-(z)=B^{\mathrm{fp}}_{\mathrm{triv}}(z).
}
$$

This is the net completion balance. It is independent of the alpha split.

If the net condition holds and

$$
A_+(z)=D_-(z)-T_+^{\mathrm{pole}}(z)\ge0,
$$

then the alpha split must satisfy the scalar constraint

$$
\sum_{m\ge0}\alpha_m(z)A_m(z)=A_+(z).
$$

But this scalar constraint still does not determine the individual
`alpha_m(z)`.

## No Intrinsic Extraction From The Finite Part Alone

The finite part supplies:

```text
net trivial-zero odd balance
```

and, after packet demand is known, at most:

```text
total positive trivial-zero capacity required.
```

It does not supply:

```text
a canonical distribution of that capacity across trivial-zero atoms.
```

Any sequence `alpha_m(z)` with the same weighted sum

$$
\sum_m\alpha_m(z)A_m(z)
$$

has the same sidewise totals. The finite part cannot distinguish between
nearest-atom, folded-kernel proportional, Abel-cutoff, or other distributions.

Therefore the gamma finite part alone cannot prove the Canonical Alpha
Normalization Lemma.

## Proof-State Result

The finite-part computation reduces the completion-side problem to two
separate obligations.

1. **Net finite-part balance.**
   Prove
   $$
   D_+(z)-D_-(z)=B^{\mathrm{fp}}_{\mathrm{triv}}(z).
   $$

2. **Canonical distribution rule.**
   Add an independent deterministic rule assigning the required scalar
   positive capacity across the trivial-zero atoms with controlled folded
   negative cost.

The first obligation is intrinsic to the completed quotient. The second is a
normalization choice for packetwise transport. Without the second rule, the
alpha split remains underdetermined.
