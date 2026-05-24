# Local Control of Prime-Power Packets by GWR Ordering

Date: 2026-05-24

Status: diagnostic-and-bound note for the Prime-Power Packet Dominance Input.

The chamber data already gives a concrete local control theorem. Let `p < q`
be consecutive primes, let

$$
I(p,q)=\{p+1,\ldots,q-1\},
$$

and let

$$
w=\min\{n\in I(p,q):\tau(n)=\min_{m\in I(p,q)}\tau(m)\}.
$$

Write

$$
d=\tau(w).
$$

The deconvolved positive mass in the closed-right packet

$$
C(p,q)=\{p+1,\ldots,q\}
$$

is supported at the endpoint prime `q` and at interior prime powers. Thus

$$
P(p,q)=\{q\}\cup\{n\in I(p,q):n=r^a,\ r\text{ prime},\ a\ge2\},
$$

with

$$
\lambda(q)=\log q,\qquad \lambda(r^a)=\log r.
$$

The GWR selector controls prime-power packets through divisor-count exponents.
It does not force the selector itself to carry deconvolved mass.

## Coefficient Envelope

Let `n = r^a` be an interior prime power in `I(p,q)`.

If `n < w`, then `n` occurs before the leftmost minimum. Therefore

$$
\tau(n)>d.
$$

Since `n = r^a` has

$$
\tau(n)=a+1,
$$

we get

$$
a\ge d.
$$

Hence every pre-selector prime-power packet mass satisfies

$$
\lambda(n)=\log r=\frac{\log n}{a}<\frac{\log w}{d}.
$$

If `n = w`, then the selector carries deconvolved mass exactly in the
prime-power case. In that case `w = r^a`, `a+1=d`, and

$$
\lambda(w)=\frac{\log w}{d-1}.
$$

If `w < n < q`, then the minimality of `w` gives

$$
\tau(n)\ge d,
$$

so

$$
a\ge d-1
$$

and every post-selector interior prime-power packet mass satisfies

$$
\lambda(n)=\frac{\log n}{a}<\frac{\log q}{d-1}.
$$

This is the strongest selector-to-packet coefficient statement supplied
directly by the Interior Maximizer Theorem.

## Pointwise Endpoint Dominance

The endpoint mass dominates every individual interior prime-power mass.

For `n = r^a` with `a >= 2` and `n < q`,

$$
\lambda(n)=\log r=\frac{\log n}{a}<\frac12\log q<\log q=\lambda(q).
$$

Therefore every interior carrier is pointwise smaller than the endpoint
carrier.

This proves a restricted endpoint-dominance statement:

```text
endpoint prime mass > each individual interior prime-power mass.
```

It does not prove aggregate endpoint dominance, since the present theorem does
not bound the completed folded contribution of the sum of all interior
prime-power carriers.

## Position From Existing Proof Machinery

The threshold and divisor-average machinery in `PROOF.md` gives position
control only in specific branches.

### Threshold Branch

For `w` not a prime square, `d >= 4`. The Witness Threshold Lemma closes an
earlier divisor-count row when

$$
p>T(d,e)=2^{(d-2)/(e-d)}.
$$

The adjacent row `e = d + 1` gives the largest threshold for fixed `d`.

This proves the ordered comparison

$$
F(k)<F(w)
$$

for earlier integers in the closed threshold branch. It does not locate
prime-power support inside the chamber and it does not estimate the folded
packet contribution. The threshold argument sees divisor counts and endpoint
scale; it is blind to whether a controlled earlier or later integer is a
prime power.

### Large-Divisor Divisor-Average Branch

In the large-left-prime proof branch where the adjacent threshold does not
close immediately, `PROOF.md` sets

$$
L=\log w,\qquad
H=\left\lfloor\frac{wL}{4(d-1)}\right\rfloor
$$

and proves that every earlier integer in the chamber satisfies

$$
k>w-H.
$$

Consequently every pre-selector interior prime power `n = r^a < w` in that
branch satisfies

$$
0<\log\frac{w}{n}<\log\frac{w}{w-H}<\frac{L}{d-1}.
$$

Together with the coefficient envelope, this gives the branch-local packet
control

$$
\lambda(n)<\frac{L}{d}
\qquad\text{and}\qquad
\log(w/n)<\frac{L}{d-1}.
$$

This is genuine GWR-to-packet control. It is still a one-sided pre-completion
bound. It does not imply nonnegative reciprocal-balanced folded mass.

### Finite-Base Material

The finite base in `PROOF.md` checks all prime gaps with

$$
2\le p<5,000,000,001
$$

for the absence of earlier maximizer failures. That table certifies the local
Interior Maximizer Theorem on the finite side of the proof. It does not record
packet sums, reciprocal folded moments, or endpoint/interior packet dominance
data.

The finite bounded-compression base gives a separate restricted position fact:
for `q < ceil(exp(16))`,

$$
w-p\le60.
$$

Hence, on that finite bounded-compression surface, every pre-selector packet
point lies in a chamber segment of length at most `59` before `w`. This is
finite position control, not a folded-mass theorem.

## Diagnostic Chambers

### `(5,7]`

The chamber has

$$
I(5,7)=\{6\},\qquad w=6,\qquad d=\tau(6)=4.
$$

The selector is not a prime power, so

$$
\lambda(w)=0.
$$

The packet is endpoint-only:

$$
P(5,7)=\{7\}.
$$

This chamber satisfies pointwise endpoint dominance vacuously. It still
requires the completion/folding step to explain how endpoint-only mass enters
the reciprocal-balanced `z = u^2` kernel.

### `(13,17]`

The chamber has

$$
w=14,\qquad d=\tau(14)=4,
$$

and a later interior prime power

$$
16=2^4.
$$

Since `16 > w`, the selector-to-packet envelope gives

$$
\lambda(16)=\log2<\frac{\log17}{3}.
$$

The endpoint has mass

$$
\lambda(17)=\log17,
$$

so pointwise endpoint dominance holds. The current machinery does not turn
that pointwise inequality into folded reciprocal balance.

### `(31,37]`

The chamber has

$$
w=33,\qquad d=\tau(33)=4,
$$

and an earlier interior prime power

$$
32=2^5.
$$

Since `32 < w`, the pre-selector envelope gives

$$
\lambda(32)=\log2<\frac{\log33}{4}.
$$

The endpoint has mass

$$
\lambda(37)=\log37.
$$

This example shows the useful part of the GWR control: earlier packet mass is
forced into a higher prime-power exponent than the selected divisor-count
minimum. It also shows the remaining gap: exponent suppression alone does not
pair the pre-selector carrier with a completed reciprocal counterpart.

## Status Of The Three Dominance Forms

**Endpoint dominance.** A pointwise endpoint theorem is proved:

$$
\lambda(q)>\lambda(n)
$$

for every interior prime-power carrier `n`. Aggregate endpoint dominance and
completed folded endpoint dominance are not established by `PROOF.md`.

**Selector-to-packet dominance.** A coefficient envelope is proved:

$$
n<w\Rightarrow \lambda(n)<\frac{\log w}{d},
\qquad
w<n<q\Rightarrow \lambda(n)<\frac{\log q}{d-1}.
$$

The divisor-average branch adds a pre-selector position bound

$$
\log(w/n)<\frac{\log w}{d-1}.
$$

These are restricted selector-to-packet controls. They do not establish the
completed nonnegative folded kernel.

**Adjacent-packet dominance.** No adjacent-packet theorem follows from the
current proof machinery. The theorems in `PROOF.md` are chamber-local. They do
not supply a deterministic rule pairing a zero-selector-mass chamber with a
neighboring endpoint or interior prime-power packet.

## Smallest Additional Local Lemma

The missing statement is a folded packet inequality, not another selector
identity.

> **Folded Packet Drift Inequality.**
> For every consecutive-prime chamber `C(p,q)`, after assigning the completion
> correction for the same log-coordinate packet, the deconvolved packet
> $$
> P(p,q)=\{q\}\cup\{n\in I(p,q):n=r^a,\ a\ge2\}
> $$
> has nonnegative folded contribution to the completed Stieltjes kernel in
> `z = u^2`.

At coefficient level, the lemma must use the established envelope:

$$
\lambda(q)=\log q,\qquad
n<w\Rightarrow \lambda(n)<\frac{\log w}{d},
\qquad
w<n<q\Rightarrow \lambda(n)<\frac{\log q}{d-1}.
$$

It must add exactly the missing analytic comparison:

```text
endpoint mass + exponent-suppressed interior packet
-> completed reciprocal fold
-> nonnegative local z-kernel contribution.
```

The current chamber technology reaches the first line. The folded packet
inequality is the independent local theorem obligation required to turn
Prime-Power Packet Dominance into the Chamber-Deconvolved Reciprocal Balance
Lemma.
