# Existing Global Machinery Survey For Packet Balance

Date: 2026-05-24

Status: survey note for the Packet Net Finite-Part Balance Lemma.

The Packet Net Finite-Part Balance Lemma requires a regularized global
summation law:

$$
\operatorname{F.p.}\sum_{(p,q)}D_{p,q}(z)
=
B^{\mathrm{fp}}_{\mathrm{triv}}(z).
$$

The existing PGS framework supplies important local structure and exact
compression identities. It does not currently contain this global finite-part
summation theorem.

## PROOF.md

`PROOF.md` proves the local integer-level foundation:

```text
direct next-prime rule
interior maximizer theorem
zero-excess coordinate equivalence
finite-base and residual branch records
```

The useful inputs for the packet-balance problem are:

- consecutive-prime chambers are exact;
- the GWR selector is the leftmost minimum-excess point in each nonempty
  chamber;
- local divisor-count ordering is universal under the stated hypotheses;
- finite residual records and bounded-compression records are separated from
  global theorem status.

What `PROOF.md` does not supply is a global summation law over all chambers.
It does not sum kernel-weighted packet moments, define a finite-part
regularization over chambers, or connect chamber-centered prime-power
displacements to the digamma finite part.

## Zero-Excess DNI Work

The zero-excess work contributes a clean coordinate contract:

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n,
$$

and the exact bridge load

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

It also preserves the exact zeta-compression identity:

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2,
\qquad
R(s)=-\frac{\zeta'(s)}{\zeta(s)}.
$$

This is essential framing. It prevents the packet-balance problem from being
misstated as an excess-only identity.

It still does not prove the packet finite-part balance. The target sum is not
the original Dirichlet series for `tau(n)` or `Lambda(n)`. It is the
chamber-centered kernel moment

$$
\Lambda(n)
J_z\left(\log\frac{n}{\sqrt{p(n)q(n)}}\right),
$$

where `p(n)` and `q(n)` are the chamber endpoints assigned to `n`.

That endpoint assignment is additional structure beyond the global Dirichlet
coefficient identity.

## Gap Grammar And Motif Work

The gap-type grammar notes and motif/pruner work record real deterministic
structure in compressed chamber states:

```text
stable reduced gap-state vocabularies,
second-order transition signal,
motif-conditioned exclusions,
measured public grammar reductions.
```

These surfaces are useful for operational pattern discovery. They do not
contain a theorem for a completed-kernel finite part.

Their state variables are coarse chamber descriptors such as reduced gap
family, divisor bucket, motif, or transition context. The Packet Net
Finite-Part Balance Lemma needs an all-scale weighted sum over exact
logarithmic displacements inside every chamber:

$$
x_n=\log\frac{n}{\sqrt{p(n)q(n)}}.
$$

No existing grammar artifact records an exact summation law for these
`J_z(x_n)` moments, and the measured grammar surfaces are implementation
evidence rather than theorem inputs.

## Bounded-Compression And Residual Records

The bounded-compression and residual records provide finite or branch-local
control of selected-witness offsets and related chamber features.

They can be leveraged to control special finite surfaces and restricted
branches. They cannot prove the packet finite-part identity because the target
requires a regularized all-chamber sum and an exact digamma finite part.

The residual records are explicitly not global occupancy theorems. They do
not determine the distribution of prime-power packet displacement over all
prime gaps.

## What Can Be Leveraged

The existing framework can support the new lemma in four ways.

1. **Exact chamber assignment.**
   Every packet term has a canonical chamber `(p,q]`.

2. **Deconvolved support.**
   After deconvolution, packet mass is exactly von Mangoldt mass:
   endpoint primes and interior prime powers.

3. **Local coefficient envelopes.**
   GWR ordering bounds interior prime-power coefficients relative to the
   selector and endpoint.

4. **Exact compression target.**
   The DNI-to-zeta identity fixes the completion-side finite part that the
   packet sum must match.

These are necessary inputs. They are not sufficient.

## Deepest Structural Gap

The missing theorem is a global regularized chamber-centering law.

The current local machinery answers:

```text
inside a given chamber, which integer is selected and how interior
prime-power packet coefficients are bounded.
```

The Packet Net Finite-Part Balance Lemma asks:

```text
after assigning every von Mangoldt carrier to its chamber center, what is the
finite-part sum of all centered odd kernel moments?
```

Those are different kinds of statements. The first is local ordering. The
second is global regularized summation.

## Required New Principle

The lemma requires a new global arithmetic principle:

> **Chamber-Centered Von Mangoldt Finite-Part Principle.**
> The chamber endpoint assignment
> $$
> n\mapsto(p(n),q(n))
> $$
> sends the von Mangoldt mass to a regularized centered first-moment sum whose
> finite part is exactly the centered gamma/trivial-zero finite part:
> $$
> \operatorname{F.p.}
> \sum_{n=r^a}
> \Lambda(n)
> J_z\left(\log\frac{n}{\sqrt{p(n)q(n)}}\right)
> =
> B^{\mathrm{fp}}_{\mathrm{triv}}(z).
> $$

This principle is not presently proved by `PROOF.md`, the zero-excess DNI
coordinate work, the gap grammar/motif surfaces, or the bounded-compression
records.

## Survey Result

Existing PGS machinery can frame, localize, and constrain the Packet Net
Finite-Part Balance Lemma. It cannot prove it as currently recorded.

The lemma therefore requires a new global arithmetic theorem. The deepest
structural gap is the absence of an exact finite-part summation law for
chamber-centered von Mangoldt first moments.
