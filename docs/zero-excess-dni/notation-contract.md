# Zero-Excess DNI Phase 1 Notation Contract

This document fixes the Phase 1 notation for Zero-Excess DNI work. It is an
operational contract for writing, reviewing, and comparing artifacts in this
track.

## Core Coordinate

For $n \geq 1$, define the zero-excess coordinate

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

This is the exact logarithmic coordinate reformulation of

$$
Z(n)=n^{1-\tau(n)/2}.
$$

Taking logarithms gives

$$
\log Z(n)=\left(1-\frac{\tau(n)}{2}\right)\log n=-E(n).
$$

Thus zero excess means $E(n)=0$.

## Prime Guard

The prime interpretation requires the guard $n>1$.

For $n>1$,

$$
E(n)=0 \iff \tau(n)=2 \iff n \text{ is prime}.
$$

At $n=1$,

$$
E(1)=\left(\frac{\tau(1)}{2}-1\right)\log 1=0,
$$

because $\log 1=0$. This is a boundary artifact, not a prime return.

## Gap Ordering

Define

$$
F(n)=-E(n).
$$

On the same nonempty prime-gap interior, maximizing $F$ is equivalent to
minimizing $E$:

$$
\operatorname*{argmax} F=\operatorname*{argmin} E.
$$

When the minimum is attained more than once, the Phase 1 convention is the
leftmost minimizer:

$$
\operatorname*{argmax} F=\text{leftmost }\operatorname*{argmin} E.
$$

Do not describe the selection as "maximizing excess." The direct statement is:
select the leftmost minimum of $E$, equivalently the leftmost maximum of $F$.

## DNI-To-Zeta Bridge Load

The DNI-to-zeta bridge load is

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

$E(n)$ alone is not the numerator in the bridge expression. The bridge load is
$H(n)$, which contains both $\log n$ and the excess coordinate.

Any $K/R$ or numerator-style expression in this track must preserve this
distinction. An excess-only numerator is invalid notation unless it is explicitly
marked as a different, non-bridge object.

## Floor And Critical Line

The zero-excess floor is an integer-side object. It marks the $E(n)=0$ coordinate
for integer divisor structure under the $n>1$ prime guard.

The critical line is a zeta-side object. It belongs to the analytic structure of
the zeta function.

Analogy is permitted. Identity is not. Do not write as if the zero-excess floor
is the critical line, or as if a zeta critical-line statement is already a PGS
integer-side theorem.

## Symbol Collision Rule

$E(n)$ means zero-excess only after this definition is explicitly in force:

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

Other uses of $E(\cdot)$ in this project must be renamed, reserved, or marked
non-zero-excess. Do not overload $E$ silently across entropy, error, energy,
expectation, edge, or unrelated excess notation.

## Prohibited Phrases And Mistakes

Do not use these phrases or claims in Phase 1 Zero-Excess DNI artifacts:

- "zero line" as the primary term for $E(n)=0$;
- "RH places primes close to the floor";
- "maximize excess";
- an excess-only $K/R$ numerator;
- "$E(n)$ alone is the DNI-to-zeta numerator";
- "`PROOF.md` directly proves RH";
- "the zero-excess floor is the critical line";
- "the critical line is the zero-excess floor."

The approved primary terms are:

- zero-excess coordinate;
- zero-excess floor;
- leftmost minimum of $E$;
- bridge load $H(n)$;
- integer-side floor;
- zeta-side critical line.
