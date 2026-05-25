# Reciprocal Endpoint Counterterm Finite-Part Route

Date: 2026-05-24

Status: concrete PGS-native route toward the finite-part packet identity.

The finite-part packet identity is

$$
\operatorname{F.p.}
\sum_{(p,q)}D_{p,q}(z)
=
-B_{\mathrm{comp}}^{\mathrm{fp}}(z).
$$

This note develops the reciprocal endpoint counterterm route.

## Packet Sum Split

For consecutive primes `p<q`, write

$$
x_q={1\over2}\log {q\over p}.
$$

Split the packet drift into endpoint and interior prime-power parts:

$$
D_{p,q}(z)
=
\log q\,J_z(x_q)
+
\sum_{\substack{p<n<q\\ n=r^a,\ a\ge2}}
\Lambda(n)J_z\left(\log {n\over\sqrt{pq}}\right).
$$

For a cutoff `X`, define

$$
E_X(z)
=
\sum_{q\le X}
\log q\,J_z\left({1\over2}\log {q\over p(q)}\right),
$$

and

$$
I_X(z)
=
\sum_{\substack{n=r^a\le X\\ a\ge2}}
\Lambda(n)
J_z\left(\log {n\over\sqrt{p(n)q(n)}}\right).
$$

Then

$$
S_X(z)=E_X(z)+I_X(z)
$$

is the ordinary cutoff packet first moment.

## Counterterm

The PGS-native counterterm is the endpoint return sum:

$$
C_X(z)=E_X(z).
$$

It uses only consecutive-prime endpoint data and the same reciprocal transport
kernel as the packet drift. The finite-part packet identity becomes the
requirement that

$$
\lim_{X\to\infty}\left(S_X(z)-C_X(z)\right)
+
\operatorname{F.p.}E_X(z)
=
-B_{\mathrm{comp}}^{\mathrm{fp}}(z).
$$

Equivalently,

$$
\lim_{X\to\infty} I_X(z)
+
\operatorname{F.p.}E_X(z)
=
-B_{\mathrm{comp}}^{\mathrm{fp}}(z).
$$

This is now a precise endpoint-counterterm law.

## Reduction To Endpoint Occupancy

The existing endpoint log-gap candidate applies to the leading term of
`E_X(z)`. Set

$$
x_q={1\over2}\log {q\over p(q)}.
$$

Then

$$
E_X(z)
=
\sum_{q\le X}\log q\,{x_q\over z+x_q^2}.
$$

The linear endpoint drift is

$$
E_X^{(1)}(z)
=
{1\over z}\sum_{q\le X}\log q\,x_q
=
{1\over 2z}
\sum_{q\le X}\log q\log {q\over p(q)}.
$$

The endpoint log-gap summatory law candidate states

$$
G(X):=
\sum_{q\le X}\log q\log {q\over p(q)}
=
{1\over2}(\log X)^2+C_{\mathrm{eg}}+o(1).
$$

Thus it supplies the leading endpoint finite part

$$
\operatorname{F.p.}E_X^{(1)}(z)
=
{C_{\mathrm{eg}}\over2z},
$$

with divergent counterterm

$$
{(\log X)^2\over4z}.
$$

The endpoint occupancy theorem candidate gives a PGS route to this law:

$$
\sum_{q\le X}{g(q)\log q\over q}
-
\sum_{2<n\le X}{\log n\over n}
\to C_{\mathrm{occ}},
$$

together with the nonlinear log-gap correction

$$
\sum_{q\le X}
\log q
\left[
\log {q\over p(q)}-{g(q)\over q}
\right]
\to C_{\mathrm{nonlin}}.
$$

The precise arithmetic gap for the leading counterterm is therefore the
reciprocal endpoint occupancy theorem, or the sufficient reciprocal gap-energy
condition

$$
\sum_q {g(q)^2\log q\over q^2}<\infty.
$$

## Full-Kernel Endpoint Remainder

The counterterm uses the full reciprocal kernel, not only its linear part.
Define the nonlinear endpoint-kernel remainder

$$
R_X^{\mathrm{end}}(z)
=
E_X(z)-E_X^{(1)}(z)
=
\sum_{q\le X}
\log q
\left[
{x_q\over z+x_q^2}-{x_q\over z}
\right].
$$

The endpoint occupancy/log-gap law supplies the leading finite part. To
upgrade it to the full endpoint counterterm, PGS must also prove

$$
R_X^{\mathrm{end}}(z)\to R_{\mathrm{end}}(z)
$$

or provide its completion-compatible finite part from endpoint returns rather
than from the gamma factor. A sufficient direct condition is a reciprocal
endpoint transport remainder bound controlling

$$
\sum_q \log q\,{|x_q|^3\over z(z+x_q^2)}.
$$

In gap notation this is controlled by a higher reciprocal gap-energy estimate
of the form

$$
\sum_q {\log q\,g(q)^3\over q^3}<\infty,
$$

or by a direct finite-part theorem for `R_X^end(z)`.

Therefore the endpoint counterterm route reduces to the prior endpoint
invariants as follows:

```text
Reciprocal Endpoint Occupancy
+ nonlinear endpoint-kernel remainder control
-> F.p. E_X(z)
```

## Interior Prime-Power Remainder

The interior term

$$
I_X(z)
$$

is supported only on prime powers. Its convergence or finite part requires a
global control law for prime-power positions inside gaps. A sufficient input
is:

> **Interior Prime-Power Reciprocal Remainder Bound.**  
> The centered interior prime-power sum
> \[
> \sum_{\substack{n=r^a\\a\ge2}}
> \Lambda(n)
> J_z\left(\log {n\over\sqrt{p(n)q(n)}}\right)
> \]
> converges, or has a completion-compatible finite part, after the endpoint
> counterterm is removed.

This input is not supplied by local GWR envelopes. It is a global gap/packet
position theorem.

## Minimal PGS Invariants Needed

The endpoint-counterterm route closes if PGS supplies:

1. **Endpoint finite-part law.**
   A canonical finite part for `E_X(z)` from endpoint returns.

2. **Interior prime-power remainder law.**
   Convergence or finite-part control of `I_X(z)`.

3. **Gamma match.**
   The sum of those two PGS finite parts equals the centered completion
   finite part:
   $$
   \lim I_X(z)+\operatorname{F.p.}E_X(z)
   =
   -B_{\mathrm{comp}}^{\mathrm{fp}}(z).
   $$

4. **Compatibility with Direct BDH summation.**
   The finite-part operation must use the same smoothing and completion
   normalization as the Direct Full-Radius BDH closure.

## Obstruction

The existing GWR/chamber ordering theorems do not prove these global finite
parts. They give local packet order and coefficient envelopes, while
`E_X(z)` is a global endpoint-return sum. This is why the finite-part identity
is a new PGS arithmetic invariant rather than a consequence of local
selector dominance.

## Packet-Frame Byproduct Condition

A strengthened Unified Packet-Frame Source theorem could replace this route
only if it proves the exact first-moment identity:

$$
\operatorname{F.p.}S_X(z)
=
-B_{\mathrm{comp}}^{\mathrm{fp}}(z),
$$

not merely residual energy, mass, and concentration bounds.

## Result

The reciprocal endpoint counterterm route gives an explicit PGS-native
counterterm:

$$
C_X(z)=
\sum_{q\le X}
\log q\,J_z\left({1\over2}\log {q\over p(q)}\right).
$$

The remaining theorem is the endpoint finite-part plus interior prime-power
remainder law matching the centered gamma finite part.
