# Chamber-Centered Von Mangoldt Finite-Part Strategy

Date: 2026-05-24

Status: candidate statement and proof strategy for the new global
finite-part principle.

The Packet Net Finite-Part Balance Lemma requires a new global arithmetic
principle. The principle must regularize the endpoint-dominated packet first
moment and identify its finite part with the centered trivial-zero finite
part.

## Chamber-Centered Packet Sum

For each von Mangoldt carrier `n = r^a`, assign the unique consecutive-prime
chamber `(p(n),q(n)]` with

$$
p(n)<n\le q(n).
$$

Define the centered coordinate

$$
x_n=\log\frac{n}{\sqrt{p(n)q(n)}}.
$$

For `X > 0`, set

$$
S_X(z)=
\sum_{\substack{n=r^a\\ n\le X}}
\Lambda(n)J_z(x_n).
$$

The target finite part is

$$
\operatorname{F.p.}_{X\to\infty}S_X(z)
=
B^{\mathrm{fp}}_{\mathrm{triv}}(z),
$$

where

$$
B^{\mathrm{fp}}_{\mathrm{triv}}(z)
=
-\frac12
\left(
\operatorname{Re}\psi\left(\frac14+\frac{i\sqrt z}{2}\right)
+
\gamma
\right).
$$

## Endpoint Divergence

Endpoint primes contribute

$$
x_q=\log\frac{q}{\sqrt{pq}}
=
\frac12\log\frac{q}{p}.
$$

For fixed `z > 0` and large chambers, `x_q` is small. The endpoint kernel has
the expansion

$$
J_z(x_q)=\frac{x_q}{z}+O_z(x_q^3).
$$

Thus the leading endpoint contribution is

$$
\frac{1}{2z}
\sum_{q\le X}
\log q\log\frac{q}{p(q)}.
$$

This is the visible divergence in ordinary packet partial sums. At the
coarsest scale it has the expected size

$$
\frac{(\log X)^2}{4z},
$$

which matches the observed endpoint-dominated growth on the finite diagnostic
surface.

## Candidate Finite-Part Statement

The PGS-native finite part should subtract the endpoint linear drift:

$$
L_X(z)=
\frac{1}{2z}
\sum_{q\le X}
\log q\log\frac{q}{p(q)}.
$$

The candidate principle is:

> **Chamber-Centered Von Mangoldt Finite-Part Principle.**
> For every `z > 0` in the folded-kernel domain,
> $$
> \lim_{X\to\infty}
> \left(
> S_X(z)-L_X(z)
> \right)
> =
> B^{\mathrm{fp}}_{\mathrm{triv}}(z).
> $$

Equivalently, the endpoint linear drift is the packet-side counterterm, and
the remaining finite part is exactly the centered gamma/trivial-zero finite
part.

## Minimal Proof Strategy

A proof would need four steps.

1. **Endpoint drift asymptotic.**
   Prove a PGS-native summatory law for
   $$
   \sum_{q\le X}\log q\log\frac{q}{p(q)}.
   $$
   The law must identify the divergent part used by the finite-part
   subtraction.

2. **Endpoint nonlinear remainder control.**
   Show that
   $$
   \sum_{q\le X}\log q
   \left(
   J_z(x_q)-\frac{x_q}{z}
   \right)
   $$
   has a finite limit after the same regularization.

3. **Interior prime-power compensation.**
   Prove that the interior prime-power contribution
   $$
   \sum_{\substack{n=r^a<X\\ p(n)<n<q(n)}}
   \Lambda(n)J_z(x_n)
   $$
   converges or has a controlled finite part compatible with the endpoint
   remainder.

4. **Digamma identification.**
   Identify the combined finite part with
   $$
   -\frac12
   \left(
   \operatorname{Re}\psi\left(\frac14+\frac{i\sqrt z}{2}\right)
   +
   \gamma
   \right).
   $$

The first three steps are arithmetic and chamber-centered. The fourth is the
completion-side identification.

## Additional Ingredients Needed

Current local GWR and chamber machinery do not provide these four steps. The
new principle requires additional global inputs.

**Endpoint log-gap summatory law.**
The project needs an exact all-scale law or finite-part theorem for

$$
\sum_{q\le X}\log q\log\frac{q}{p(q)}.
$$

This is a global endpoint-chain statement, not a local selected-witness
statement.

**Interior prime-power summatory law.**
Pointwise endpoint dominance and selector envelopes do not determine the sum
of interior prime-power kernel moments. A global law for the sparse
prime-power packet support is required.

**Kernel remainder bound.**
The replacement

$$
J_z(x_q)\mapsto\frac{x_q}{z}
$$

must be justified with a summable remainder, uniformly on the folded-kernel
domain under discussion.

**Completion-compatible finite-part prescription.**
The packet-side counterterm must be the same finite-part prescription as the
gamma/trivial-zero counterterm. Otherwise the equality can be shifted by an
arbitrary constant.

## Structural Gap

The deepest gap is no longer local packet dominance. It is the absence of a
PGS-native finite-part summation theorem for the endpoint chain and interior
prime-power packet support.

The local GWR theorem identifies the ordered chamber interior. The new
principle must identify the regularized global first moment of all
chamber-centered von Mangoldt carriers.

This is the minimal new arithmetic theorem needed before the symmetric
completion-capacity route can become a proof rather than a calibrated
decomposition.
