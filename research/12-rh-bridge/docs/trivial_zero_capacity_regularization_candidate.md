# Trivial-Zero Capacity Regularization Candidate

Date: 2026-05-24

Status: candidate regularization for the infinite part of the Transport
Capacity Balance Identity.

The raw trivial-zero reservoir has atoms

$$
y_m=-2m-\frac12,
\qquad
m\ge0,
$$

with signed odd capacities

$$
O_m(z)=
\frac{-2m-1/2}{z+(2m+1/2)^2}.
$$

Thus the raw reservoir supplies negative odd capacity only. Its formal
negative capacity is

$$
B_N(z)=
\sum_{m=0}^{N}
\frac{2m+1/2}{z+(2m+1/2)^2},
$$

which diverges logarithmically.

## Candidate Regularization

Use a Hadamard finite-part regularization of the one-sided capacity:

$$
T^{\mathrm{triv,reg}}_-(z)
=
\operatorname{F.p.}_{N\to\infty}
\left[
B_N(z)-L_N(z)
\right],
$$

where `L_N(z)` is the counterterm forced by the regularized digamma expansion
of

$$
-\frac12\frac{\Gamma'}{\Gamma}(s/2).
$$

The positive trivial-zero capacity remains zero:

$$
T^{\mathrm{triv,reg}}_+(z)=0.
$$

This candidate preserves the raw transport orientation of the trivial-zero
atoms instead of adding mirror atoms not present in the completion term.

## Resulting Balance Conditions

With the explicit pole capacities

$$
T^{\mathrm{pole}}_+(z)=T^{\mathrm{pole}}_-(z)=\frac{1}{2(z+1/4)},
$$

the Transport Capacity Balance Identity becomes

$$
\frac{1}{2(z+1/4)}
+T^{\mathrm{triv,reg}}_-(z)
=
D_+(z),
$$

and

$$
\frac{1}{2(z+1/4)}
=
D_-(z).
$$

Thus this regularization is sharply falsifiable:

```text
negative packet-drift demand must be exactly the pole positive capacity;
positive packet-drift demand must be pole negative capacity plus
regularized trivial-zero negative capacity.
```

## Main Analytic Requirements

1. **Counterterm identification.**
   The counterterm `L_N(z)` must be derived from the same digamma
   regularization that preserves the completed quotient.

2. **Finite-part existence.**
   The limit defining `T^{triv,reg}_-(z)` must exist on the folded-kernel
   domain.

3. **Sidewise identity.**
   The finite part must satisfy
   $$
   T^{\mathrm{triv,reg}}_-(z)
   =
   D_+(z)-\frac{1}{2(z+1/4)},
   $$
   while the opposite side satisfies
   $$
   D_-(z)=\frac{1}{2(z+1/4)}.
   $$

4. **No mirror insertion.**
   The proof must not introduce positive-side trivial-zero capacity unless it
   is derived from an exact alternative representation of the completion
   correction.

## Proof-State Result

The candidate keeps the completion representation honest: trivial zeros remain
one-sided. The resulting burden is severe and checkable. If

$$
D_-(z)\ne\frac{1}{2(z+1/4)},
$$

then this one-sided regularization cannot prove the Transport Capacity Balance
Identity, and a different exact representation of the gamma/trivial-zero
completion term is required.

The resulting negative-drift packet condition is stated in
[Negative-Drift Pole Capacity Condition](negative_drift_pole_capacity_condition.md).
