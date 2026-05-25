# Folded Packet Drift Inequality

Date: 2026-05-24

Status: standalone target inequality for the Chamber-Deconvolved Reciprocal
Balance Lemma.

The current local control is coefficient-level. For a consecutive-prime
chamber `p < q`, the deconvolved positive mass is supported on

$$
P(p,q)=\{q\}\cup\{n\in(p,q):n=r^a,\ r\text{ prime},\ a\ge2\},
$$

with

$$
\lambda(q)=\log q,\qquad \lambda(r^a)=\log r.
$$

GWR ordering bounds those coefficients relative to the selected minimum. The
remaining task is to state the exact inequality that turns that packet control
into a nonnegative reciprocal-balanced folded object after completion.

## Centered Packet Measure

Use the chamber-centered log coordinate

$$
x_n=\log\frac{n}{\sqrt{pq}}.
$$

The deconvolved packet measure before completion is

$$
\nu_{p,q}=\sum_{n\in P(p,q)}\lambda(n)\delta_{x_n}.
$$

The endpoint atom has

$$
x_q=\log\frac{q}{\sqrt{pq}}>0.
$$

Interior prime powers can lie on either side of the chamber center. Completion
adds the pole, gamma, main-term, and trivial-zero corrections required to pass
from

$$
R(s)=-\frac{\zeta'(s)}{\zeta(s)}
$$

to

$$
Q(s)=-\frac{\xi'(s)}{\xi(s)}.
$$

For this local target, write the completion correction assigned to the packet
as a signed measure

$$
\eta_{p,q}.
$$

The completed local packet is

$$
\sigma_{p,q}=\nu_{p,q}+\eta_{p,q}.
$$

The fold into `z = u^2` is the pushforward of `sigma_{p,q}` under

$$
x\mapsto x^2.
$$

## Statement

> **Folded Packet Drift Inequality.**
> For every consecutive-prime chamber `p < q`, the completion-corrected packet
> measure
> $$
> \sigma_{p,q}=\nu_{p,q}+\eta_{p,q}
> $$
> is reciprocal-balanced and nonnegative after folding:
> for every Borel set $A\subset(0,\infty)$,
> $$
> \sigma_{p,q}(A)-\sigma_{p,q}(-A)=0,
> $$
> and
> $$
> \sigma_{p,q}(A)+\sigma_{p,q}(-A)\ge0.
> $$

Equivalently, the folded measure

$$
\mu_{p,q}(B)=\sigma_{p,q}(\{x:x^2\in B\})
$$

is a nonnegative measure on `[0,infinity)`.

This is the local packet form of the Chamber-Deconvolved Reciprocal Balance
Lemma. Summing these packet measures over chambers would give the completed
Stieltjes kernel

$$
S(z)=\int_0^\infty\frac{d\mu(t)}{z+t}.
$$

## Kernel Form

For `z > 0`, define the reciprocal-balance and folded-mass kernels

$$
J_z(x)=\frac{x}{z+x^2},
\qquad
K_z(x)=\frac{1}{z+x^2}.
$$

The same target is:

$$
B_{p,q}(z)=\int J_z(x)\,d\sigma_{p,q}(x)=0,
$$

and

$$
M_{p,q}(z)=\int K_z(x)\,d\sigma_{p,q}(x)\ge0.
$$

Writing packet and completion parts separately gives the two equations that
must be closed:

$$
\sum_{n\in P(p,q)}
\lambda(n)J_z(x_n)
+
\int J_z(x)\,d\eta_{p,q}(x)
=0,
$$

and

$$
\sum_{n\in P(p,q)}
\lambda(n)K_z(x_n)
+
\int K_z(x)\,d\eta_{p,q}(x)
\ge0.
$$

Thus the completion correction must cancel the odd packet drift without
creating more negative even folded mass than the prime-power packet supplies.

## Drift-Cost Inequality

Define the packet drift and packet folded reserve:

$$
D_{p,q}(z)=
\sum_{n\in P(p,q)}\lambda(n)J_z(x_n),
$$

and

$$
R_{p,q}(z)=
\sum_{n\in P(p,q)}\lambda(n)K_z(x_n).
$$

The Folded Packet Drift Inequality is equivalent to the following local
completion-cost pair:

$$
\int J_z(x)\,d\eta_{p,q}(x)=-D_{p,q}(z),
$$

and

$$
-\int K_z(x)\,d\eta_{p,q}(x)\le R_{p,q}(z).
$$

The first line is reciprocal balance. The second line is the nonnegative
folded-mass inequality.

This is the exact bridge from packet control to the `z = u^2` Stieltjes
condition.

## What Existing Control Already Supplies

Let

$$
w=\min\{n\in(p,q):\tau(n)=\min_{m\in(p,q)}\tau(m)\},
\qquad
d=\tau(w).
$$

The current local note supplies three pieces.

### Pointwise Endpoint Dominance

For every interior prime power `n = r^a < q`,

$$
\lambda(n)=\log r=\frac{\log n}{a}<\frac12\log q<\log q=\lambda(q).
$$

Thus the endpoint mass dominates every individual interior prime-power mass.
In the drift-cost notation, this controls individual coefficients in
`D_{p,q}(z)` and `R_{p,q}(z)`, but it does not control the aggregate weighted
sum over all interior prime powers.

### Selector-To-Packet Coefficient Envelope

The GWR selector gives

$$
n<w\Rightarrow
\lambda(n)<\frac{\log w}{d},
$$

and

$$
w<n<q\Rightarrow
\lambda(n)<\frac{\log q}{d-1}.
$$

These inequalities insert directly into the packet drift:

$$
\left|D_{p,q}(z)-\lambda(q)J_z(x_q)\right|
\le
\sum_{\substack{n\in P(p,q)\\ n<w}}
\frac{\log w}{d}\,\left|J_z(x_n)\right|
+
\sum_{\substack{n\in P(p,q)\\ w<n<q}}
\frac{\log q}{d-1}\,\left|J_z(x_n)\right|.
$$

They also insert into the folded reserve:

$$
R_{p,q}(z)
\le
\lambda(q)K_z(x_q)
+
\sum_{\substack{n\in P(p,q)\\ n<w}}
\frac{\log w}{d}\,K_z(x_n)
+
\sum_{\substack{n\in P(p,q)\\ w<n<q}}
\frac{\log q}{d-1}\,K_z(x_n).
$$

The first inequality controls the possible odd drift. The second bounds the
available folded reserve from above, so it is not enough by itself for
positivity. A closing proof needs a lower bound for the reserve or a direct
upper bound for completion's negative even cost.

### Restricted Pre-Selector Position Bound

In the large-divisor divisor-average branch, every earlier interior integer
satisfies

$$
k>w-H,
\qquad
H=\left\lfloor\frac{w\log w}{4(d-1)}\right\rfloor.
$$

Therefore every pre-selector interior prime power satisfies

$$
0<\log\frac{w}{n}<\frac{\log w}{d-1}.
$$

This gives a branch-local bound on the kernel arguments `x_n` for
pre-selector prime powers. It controls where those atoms sit before folding.
It does not control the number of such atoms or the completion cost required
to cancel their odd drift.

## Smallest Additional Local Estimate

The missing estimate is aggregate and folded. The current pointwise and
selector-envelope controls become sufficient once the following local bound is
proved:

> **Aggregate Completion-Cost Bound.**
> For every chamber `p < q` and every `z > 0`, the completion correction
> assigned to the packet satisfies
> $$
> -\int K_z(x)\,d\eta_{p,q}(x)
> \le
> \lambda(q)K_z(x_q)
> +
> \sum_{\substack{n\in P(p,q)\\ n<q}}
> \lambda(n)K_z(x_n),
> $$
> while its odd part cancels the packet drift:
> $$
> \int J_z(x)\,d\eta_{p,q}(x)
> =
> -\lambda(q)J_z(x_q)
> -
> \sum_{\substack{n\in P(p,q)\\ n<q}}
> \lambda(n)J_z(x_n).
> $$

The second equality is the reciprocal-balance assignment. The first inequality
is the single missing positivity estimate. It says that the even cost of
canceling one-sided packet drift is no larger than the folded reserve already
present in the endpoint plus interior prime-power packet.

With this aggregate completion-cost bound, the Folded Packet Drift Inequality
follows immediately:

$$
M_{p,q}(z)
=
R_{p,q}(z)+\int K_z(x)\,d\eta_{p,q}(x)
\ge0.
$$

## Proof-State Result

The exact local target is no longer "some dominance." It is the
completion-cost inequality above.

The existing chamber technology proves atomwise endpoint dominance,
selector-to-packet coefficient bounds, and a restricted pre-selector position
bound. Those controls shape `D_{p,q}(z)` and `R_{p,q}(z)`.

They do not prove the aggregate completion-cost bound. That bound is the
smallest additional local estimate needed to close the Folded Packet Drift
Inequality and feed the Chamber-Deconvolved Reciprocal Balance Lemma.

The aggregate-cost reduction is recorded in
[Aggregate Completion-Cost Bound](aggregate_completion_cost_bound.md).
