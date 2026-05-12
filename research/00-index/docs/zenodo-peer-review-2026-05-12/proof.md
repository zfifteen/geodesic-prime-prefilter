# An Exact Deterministic Method for Next-Prime Selection

## Abstract

Every positive integer has an exact number of positive divisors. A prime is
exactly an integer greater than $1$ with divisor count $2$. The Prime Number
Theorem describes the global asymptotic density of primes, but it does not
determine the next prime from a given prime. This note addresses that local
question using divisor counts alone.

The first theorem proves that, given a known prime $p$, the next prime $q$ is
determined by the exact divisor-count rule

$$
q=\min\{n>p:\tau(n)=2\},
$$

where $\tau(n)$ is the number of positive divisors of $n$.

This is an exact characterization and selection rule using $\tau(n)$. It is
not a closed-form shortcut that bypasses the computation of divisor counts.

The second theorem proves that, if $p<q$ are consecutive primes and

$$
I=\{p+1,\ldots,q-1\}
$$

is nonempty, then the first integer $w$ in $I$ whose divisor count is minimal
on $I$ is the unique maximizer on $I$ of

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.
$$

Both statements are universal under their stated hypotheses. The proof uses a
finite base below $5,000,000,001$ and then closes the remaining earlier-integer
side by exact divisor-count arithmetic. Implementation audits are included in
appendices for provenance and reproducibility. They do not limit the universal
theorems. The appendices also record the current bounded-compression boundary,
measured implementation surfaces, invalidated routes, and explicit non-claims.

## 1. Definitions

For a positive integer $n$, let $\tau(n)$ denote the number of positive divisors
of $n$.

An integer $n>1$ is prime exactly when its only positive divisors are $1$ and
$n$. Equivalently,

$$
n \text{ is prime} \quad\Longleftrightarrow\quad \tau(n)=2.
$$

For a known prime $p$, define the divisor-count successor value

$$
Q(p)=\min\{n>p:\tau(n)=2\}.
$$

The set is nonempty because there is always a prime greater than $p$.

If $p<q$ are consecutive primes, define the prime-gap interior

$$
I(p,q)=\{p+1,\ldots,q-1\}.
$$

When the gap interior is nonempty, define its minimum divisor count

$$
d_*=\min\{\tau(n):n\in I(p,q)\}.
$$

Define the leftmost minimum-divisor interior witness

$$
w=\min\{n\in I(p,q):\tau(n)=d_*\}.
$$

The comparison function used throughout the maximizer theorem is

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.
$$

For composite $n$, $\tau(n)\ge 3$, so

$$
F(n)=-\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

## 2. The Divisor-Count Structure

If

$$
n=r_1^{a_1}\cdots r_s^{a_s}
$$

is the prime-power factorization of $n$, then

$$
\tau(n)=\prod_{i=1}^{s}(a_i+1).
$$

This formula counts the divisors of $n$. For each prime power $r_i^{a_i}$, a
divisor chooses one exponent from $0$ through $a_i$. The choices are independent
across distinct prime factors, so the counts multiply.

Inside the interior of a prime gap, every integer is composite. A smaller
divisor count is therefore an ordinary comparison of exact integer values. The
witness $w$ is the first interior integer where $\tau(n)$ attains its minimum
on that finite list.

## 3. Theorem 1: Direct Deterministic Next-Prime Selection

**Theorem.** Let $p$ be a known prime. Let

$$
q=\min\{n>p:\tau(n)=2\}.
$$

Then $q$ is the next prime after $p$.

**Proof.** An integer $n>1$ is prime exactly when $\tau(n)=2$.

There is always a prime greater than $p$, so the set of primes greater than
$p$ has a least element. Call that least prime $q_0$.

Every integer $n$ with $p<n<q_0$ is not prime, hence $\tau(n)\ne 2$. The
integer $q_0$ is prime, hence $\tau(q_0)=2$.

Therefore the first integer greater than $p$ with divisor count $2$ is exactly
$q_0$. Thus $q=q_0$, the next prime after $p$. $\square$

## 4. Theorem 2: The Prime-Gap Interior Maximizer

**Theorem.** Let $p<q$ be consecutive primes, and assume

$$
I=\{p+1,\ldots,q-1\}
$$

is nonempty. Let

$$
w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}.
$$

Then $w$ is the unique integer in $I$ where

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n
$$

is largest.

The proof treats later and earlier interior integers separately. The earlier
side is closed by the prime-square case, the threshold comparison, and a
short-interval divisor-average argument.

### 4.1 Ordered Comparison Lemma

**Lemma.** Let $a<b$ be composite integers. If $\tau(a)\le \tau(b)$, then

$$
F(a)>F(b).
$$

**Proof.** For composite $n$, $\tau(n)\ge 3$, so

$$
\frac{\tau(n)}{2}-1>0
$$

and

$$
F(n)=-\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

Since $a<b$, $\log a<\log b$. Since $\tau(a)\le \tau(b)$,

$$
\frac{\tau(a)}{2}-1\le \frac{\tau(b)}{2}-1.
$$

Both factors are positive, hence

$$
\left(\frac{\tau(a)}{2}-1\right)\log a
<
\left(\frac{\tau(b)}{2}-1\right)\log b.
$$

Multiplying by $-1$ reverses the inequality:

$$
F(a)>F(b).
$$

$\square$

### 4.2 Later Integers

Every integer $t\in I$ with $t>w$ satisfies

$$
\tau(t)\ge \tau(w),
$$

because $w$ has the minimum divisor count in $I$. The ordered comparison lemma
therefore gives

$$
F(w)>F(t).
$$

No later integer matches or exceeds $F(w)$.

### 4.3 Divisor-Count Tail Closure

The interval $I$ ends at the first later divisor-count-two integer. Since
$p<q$ are consecutive primes, every $n$ with $p<n<q$ is composite and
$\tau(n)>2$.

For any $x$ with $p<x\le q$, define $D(x)$ as the minimum value of $\tau(n)$
among integers $n$ with $p<n<x$, when that set is nonempty. At $x=q$,

$$
D(q)=\min\{\tau(n):n\in I\}.
$$

The witness $w$ is the first integer in $I$ with $\tau(w)=D(q)$.

There cannot be $t$ with $w<t<q$ and $\tau(t)<\tau(w)$; that would contradict
the definition of $w$. There is no competing integer after $q$ in the same
gap interior, because the gap interior has ended.

This closes the right-side tail without any upper bound on $\tau(w)$.

### 4.4 Earlier Integers

Let $k<w$ be an earlier integer in $I$. Since $w$ is the first integer in $I$
with the minimum divisor count,

$$
\tau(k)>\tau(w).
$$

Write

$$
e=\tau(k),\qquad d=\tau(w).
$$

The desired inequality $F(k)<F(w)$ is equivalent to

$$
(e-2)\log k>(d-2)\log w.
$$

The earlier side is closed by the prime-square case, a threshold comparison,
and a short-interval divisor-average argument.

### 4.5 Prime-Square Case

Suppose $w$ is the square of a prime:

$$
w=r^2.
$$

The prime $r$ cannot lie strictly between $p$ and $q$, because no prime lies
strictly between consecutive primes. Therefore $r\le p$.

Every earlier integer $k\in I$ satisfies $k>p$, hence $k>r$. Since $w=r^2$,

$$
k>\sqrt{w}.
$$

If an earlier integer $k$ had $\tau(k)=3$, then $k$ would also be the square of
a prime. It would have the same divisor count as $w$ and would occur before
$w$, contradicting the definition of $w$ as the first interior integer with
minimum divisor count. Therefore every earlier integer $k$ has $\tau(k)\ge 4$.

Thus

$$
F(k)\le -\log k
$$

while

$$
F(w)=-\frac12\log w.
$$

Since $k>\sqrt{w}$, $\log k>\frac12\log w$, and therefore

$$
F(k)<F(w).
$$

The prime-square case is closed.

### 4.6 Threshold Lemma

Assume now that $w$ is not a prime square. Then $d=\tau(w)\ge 4$.

Bertrand's theorem states that for every prime $p>1$, there is a prime less
than $2p$. Since $q$ is the next prime after $p$, this gives

$$
q<2p.
$$

Every integer in $I$ is less than $2p$, and every earlier integer $k$ is
greater than $p$.

For every earlier integer considered in this lemma,

$$
e=\tau(k)>\tau(w)=d.
$$

The inequality $F(k)<F(w)$ is guaranteed by the stronger inequality

$$
(e-2)\log p>(d-2)\log(2p).
$$

This is equivalent to

$$
p^{e-d}>2^{d-2}.
$$

Define

$$
T(d,e)=2^{(d-2)/(e-d)}.
$$

If $p>T(d,e)$, then every earlier integer with divisor count $e$ has
$F(k)<F(w)$.

For fixed $d$, $T(d,e)$ decreases as $e$ increases. Therefore the adjacent
case $e=d+1$ is the largest threshold for that fixed $d$.

For fixed $e$, $T(d,e)$ increases as $d$ increases. Therefore the largest
threshold for that fixed $e$ occurs at $d=e-1$.

For $d=4$ and $e=5$, the threshold is $T(4,5)=4$. Thus every gap with $p>4$
is closed by the threshold lemma. The only smaller prime gap with nonempty
interior is $3<5$, whose interior is $\{4\}$ and has no earlier integer before
$w$.

### 4.7 Finite Base Lemma

The finite base covers all prime gaps with

$$
2\le p<5,000,000,001.
$$

For each consecutive prime pair in that range, the verification enumerated the
integers in the gap, computed each exact divisor count, selected the first
integer with the smallest divisor count, and checked every earlier integer
$k$ for the failure condition $F(k)\ge F(w)$.

The failure count was $0$.

| Left-prime range | Prime gaps checked | Earlier integers checked | Failures |
| ---: | ---: | ---: | ---: |
| $2\le p<20,000,001$ | $1,163,198$ | $3,349,874$ | $0$ |
| $20,000,001\le p<100,000,001$ | $4,157,943$ | $13,321,098$ | $0$ |
| $100,000,001\le p<1,000,000,001$ | $42,101,885$ | $149,214,917$ | $0$ |
| $1,000,000,001\le p<5,000,000,001$ | $172,913,029$ | $660,287,089$ | $0$ |
| Total | $220,336,055$ | $826,172,978$ | $0$ |

This finite base closes the theorem for all gaps below the stated left-prime
bound. The remaining proof assumes $p>5,000,000,000$.

### 4.8 Short Divisor-Average Lemma

**Lemma.** Let $N>1$, let $L=\log N$, and let $1\le H<N$. For the interval

$$
J=\{N-H,\ldots,N-1\},
$$

we have

$$
\sum_{n\in J}\tau(n)\le H(L+2)+2\sqrt N.
$$

**Proof.** For each divisor pair of an integer $n<N$, at least one member of
the pair is at most $\sqrt n<\sqrt N$. Therefore

$$
\tau(n)\le 2\#\{a\le\sqrt N:a\mid n\}.
$$

Summing over $J$ gives

$$
\sum_{n\in J}\tau(n)
\le
2\sum_{a\le\sqrt N}\#\{n\in J:a\mid n\}.
$$

Among $H$ consecutive integers, the number divisible by $a$ is at most
$H/a+1$. Hence

$$
\sum_{n\in J}\tau(n)
\le
2\sum_{a\le\sqrt N}\left(\frac Ha+1\right).
$$

Using $\sum_{a\le R}1/a\le 1+\log R$ with $R=\sqrt N$,

$$
\sum_{n\in J}\tau(n)
\le
2H(1+\log\sqrt N)+2\sqrt N
=H(L+2)+2\sqrt N.
$$

$\square$

### 4.9 Large-Divisor Adjacent Closure

Assume $p>5,000,000,000$, since the finite base has already closed all smaller
left primes. Let

$$
d=\tau(w)\ge 4,\qquad L=\log w.
$$

By Bertrand's theorem, $w<q<2p$, so $p>w/2$.

It is enough to close the adjacent earlier divisor count $e=d+1$, because the
threshold $T(d,e)$ decreases as $e$ increases.

If

$$
(d-2)\log 2\le L-\log 2,
$$

then

$$
2^{d-2}\le \frac w2<p,
$$

so the Threshold Lemma closes the adjacent row and every larger earlier
divisor count.

It remains to consider

$$
(d-2)\log 2>L-\log 2.
$$

Then

$$
d-L-2>\left(\frac1{\log 2}-1\right)L-1.
$$

Since $w>5,000,000,000$,

$$
\left(\frac1{\log 2}-1\right)L-1>\frac{32}{L}.
$$

The function

$$
\left(\frac1{\log 2}-1\right)L-1-\frac{32}{L}
$$

is increasing for $L>0$, and it is already positive at
$L=\log(5,000,000,000)$.

Therefore

$$
d>L+2+\frac{32}{L}.
$$

Set

$$
H=\left\lfloor\frac{wL}{4(d-1)}\right\rfloor.
$$

For every integer $n$, $\tau(n)\le 2\sqrt n$, so $d=\tau(w)\le 2\sqrt w$.
Thus

$$
\frac{wL}{4(d-1)}\ge \frac{\sqrt w\,L}{8}>2,
$$

and therefore

$$
H\ge \frac{wL}{8(d-1)}.
$$

Here we used the elementary fact that if $A>2$, then $\lfloor A\rfloor\ge A/2$.

Apply the Short Divisor-Average Lemma to

$$
J=\{w-H,\ldots,w-1\}.
$$

The average divisor count on $J$ is at most

$$
L+2+\frac{2\sqrt w}{H}
\le
L+2+\frac{16(d-1)}{\sqrt w\,L}
\le
L+2+\frac{32}{L}
<d.
$$

So some $n\in J$ has $\tau(n)<d$. If $p<n<w$, then $n$ would be an earlier
interior integer with smaller divisor count than $w$, contradicting the choice
of $w$. Hence $n\le p$.

Every earlier integer $k<w$ in the gap satisfies

$$
k>p\ge n\ge w-H.
$$

Let $x=H/w$. Since

$$
d-1>\frac{L}{\log 2}>L,
$$

we have

$$
x\le \frac{L}{4(d-1)}<\frac14,
$$

and

$$
\log\frac{w}{w-H}
=-\log(1-x)
< \frac{x}{1-x}
<\frac{L}{d-1}.
$$

Therefore

$$
(d-1)\log(w-H)>(d-2)\log w.
$$

Since $k\ge w-H+1>w-H$ and $e-2\ge d-1$,

$$
(e-2)\log k>(d-2)\log w.
$$

Thus every earlier integer $k<w$ satisfies $F(k)<F(w)$.

### 4.10 Proof Of The Maximizer Theorem

The later-integer argument gives $F(w)>F(t)$ for every $t>w$ in $I$.

The earlier-integer argument gives $F(k)<F(w)$ for every $k<w$ in $I$.

Therefore $w$ is the unique integer in $I$ where $F(n)$ is largest. $\square$

## 5. Boundary Of The Main Theorems

The two universal theorems above do not depend on bounded dynamic cutoff,
generator implementation surfaces, state-budget measured results, or
semiprime/RSA audit results.

The direct next-prime theorem is a divisor-count characterization of the next
prime.

The interior maximizer theorem is a statement about the ordered divisor-count
structure inside a fixed prime gap.

The prime-square case in Section 4.5 is part of the maximizer proof only. It
uses the facts that, if $w=r^2$, then $r\le p$, every earlier interior integer
$k$ satisfies $k>\sqrt{w}$, and no earlier integer also has divisor count
$3$. It does not bound the distance $r^2-p$.

The separate prime-square proximity question in Appendix B concerns bounded
compression. That question asks whether the selected square branch always
satisfies a logarithmic-square distance bound from the left boundary prime.
That bounded-compression question is independent of the proof that $w$
maximizes $F$ inside the already fixed gap.

The appendices below record additional finite certificates, implementation
audits, measured results, invalidated routes, and unresolved research
boundaries. They do not weaken or bound the two main theorems.

## Appendix A. Finite Certificates And Residual Theorems

### A.1 Maximizer Finite Base

The maximizer proof uses the finite base in Section 4.7:

| Left-prime range | Prime gaps checked | Earlier integers checked | Failures |
| ---: | ---: | ---: | ---: |
| $2\le p<20,000,001$ | $1,163,198$ | $3,349,874$ | $0$ |
| $20,000,001\le p<100,000,001$ | $4,157,943$ | $13,321,098$ | $0$ |
| $100,000,001\le p<1,000,000,001$ | $42,101,885$ | $149,214,917$ | $0$ |
| $1,000,000,001\le p<5,000,000,001$ | $172,913,029$ | $660,287,089$ | $0$ |
| Total | $220,336,055$ | $826,172,978$ | $0$ |

A separate stress sample near $10^{12}$ checked $137,771$ prime gaps and
$649,769$ earlier integers with $0$ unresolved cases. Its median offset was
$1$, its 99th percentile offset was $14$, and its worst offset was $42$.

### A.2 Finite Bounded-Compression Base

This finite lemma is not an all-scale bounded-compression theorem. It records
the exact finite side needed by the dynamic cutoff target.

Let $p<q$ be consecutive primes with nonempty interior and with

$$
q<\lceil e^{16}\rceil=8,886,111.
$$

Let $w$ be the first integer in $\{p+1,\ldots,q-1\}$ whose divisor count is
minimal in that interval. Then

$$
w-p\le 60.
$$

Consequently,

$$
w-p\le 64\le \max(64,\lceil 0.5\log(q)^2\rceil).
$$

The verification enumerated the exact divisor counts for every consecutive
prime gap with successor prime below $8,886,111$. It checked $542,081$
nonempty prime-gap interiors. The maximum selected-witness offset was $60$,
attained at

| $p$ | $q$ | $w$ | $\tau(w)$ | $w-p$ |
| ---: | ---: | ---: | ---: | ---: |
| $1,885,069$ | $1,885,151$ | $1,885,129$ | $3$ | $60$ |

No selected-witness offset exceeded $64$ on this finite surface.

### A.3 Residual $K=128$ First-d4 Branch-Elimination Lemma

This lemma records finite first-d4 residual checks from the earlier
classification route. The main maximizer proof now closes the earlier-integer
side by the divisor-average argument in Section 4.9, so this residual table is
certified provenance rather than a dependency of the theorem.

Let $d$ be an odd divisor count and let the adjacent earlier divisor count be
$d+1$. In each stated finite interval, enumerate every integer $w$ with
$\tau(w)=d$ whose preceding prime $p$ lies in the stated finite threshold
window above the exact base. For each containing prime gap $(p,q)$, compute
exact divisor counts in the interior.

If that containing gap has minimum divisor count $4$ and its first interior
integer with divisor count $4$ occurs at offset at most $128$, then $w$ is not
the selected witness for that gap. An earlier interior integer has smaller
divisor count than $d$, so $w$ cannot be the first integer where the gap
minimum divisor count is attained.

The residual checks applied this exact elimination as follows:

| Earlier divisor count | Witness divisor count | Preceding-prime window | Integers enumerated | Eliminated by first-d4 window | Remaining exceptions | Result |
| ---: | ---: | --- | ---: | ---: | ---: | --- |
| $36$ | $35$ | $(5,000,000,000,8,589,934,592]$ | $5$ | $5$ | $0$ | no $\tau=35$ winner branch remains |
| $40$ | $39$ | $(5,000,000,000,137,438,953,472]$ | $655$ | $623$ | $32$ | exceptions realize $0$ $\tau=39$ winner gaps |
| $56$ | $55$ | $(5,000,000,000,9,007,199,254,740,992]$ | $439$ | $412$ | $27$ | exceptions realize $0$ $\tau=55$ winner gaps |

Thus, on these residual finite branches, the $K=128$ first-d4 window eliminates
the listed witness branches, with remaining exceptions closed by exact
enumeration.

## Appendix B. Bounded Compression Status

The active dynamic cutoff expression is

$$
C(q)=\max(64,\lceil 0.5\log(q)^2\rceil).
$$

The finite base in Appendix A.2 is proved on its stated finite range. The
$K=128$ branch-elimination theorem in Appendix A.3 is proved on its stated
finite branches.

The all-scale bounded dynamic cutoff theorem remains unresolved on the square
branch.

### B.1 Square-Branch Characterization

This appendix uses prime squares in a different role from Section 4.5. Section
4.5 proves the earlier-integer comparison needed for the interior maximizer
theorem. This appendix records the separate bounded-compression problem of how
far the selected prime square lies from the left boundary prime.

Let $p<q$ be consecutive primes with nonempty interior $I$, and let $w$ be the
first integer in $I$ whose divisor count is minimal in $I$.

In the square branch,

$$
\tau(w)=3.
$$

The integers with divisor count $3$ are exactly prime squares. Therefore

$$
w=r^2
$$

for some prime $r$.

Let $s$ be the prime immediately before $r$, and let $P(r^2)$ be the greatest
prime below $r^2$. Then $r^2$ is the selected prime-square witness for its
containing prime gap exactly when

$$
s^2<P(r^2)<r^2.
$$

If $P(r^2)\le s^2$, then $s^2$ is also inside the gap before $r^2$, so $r^2$
is not the leftmost divisor-count-three integer in the gap. Conversely, if
$s^2<P(r^2)<r^2$, then the gap after $P(r^2)$ contains $r^2$ and contains no
earlier prime square.

The square-branch condition gives the deterministic band bound

$$
r^2-P(r^2)<r^2-s^2=(r-s)(r+s).
$$

It does not prove the logarithmic-square cutoff. The unresolved target is:

$$
r^2-p\le \max(64,\lceil 0.5\log(r^2)^2\rceil)
$$

for every consecutive prime gap whose first interior prime square is $r^2$.

### B.2 Measured Bounded-Compression Surfaces

The exact bounded-compression compare scan through $q\le 10,000,000$ checked
$664,575$ gaps. It found no counterexample. The maximum exact peak offset was
$60$, and the maximum cutoff utilization was $0.6153846153846154$.

The square dynamic-cutoff search over odd prime-square roots
$3\le r\le 100,000,000$ checked $5,761,454$ prime roots. It found no
counterexample. The maximum utilization was $0.8120300751879699$, attained at

| root $r$ | $r^2$ | previous prime below $r^2$ | offset | cutoff | utilization |
| ---: | ---: | ---: | ---: | ---: | ---: |
| $82,357,433$ | $6,782,746,770,349,489$ | $6,782,746,770,348,949$ | $540$ | $665$ | $0.8120300751879699$ |

The next square dynamic-cutoff segment,
$100,000,001\le r\le 200,000,000$, checked $5,317,482$ prime roots. It found
no counterexample. The maximum utilization was $0.6784140969162996$, attained
at

| root $r$ | $r^2$ | previous prime below $r^2$ | offset | cutoff | utilization |
| ---: | ---: | ---: | ---: | ---: | ---: |
| $102,017,779$ | $10,407,627,232,092,841$ | $10,407,627,232,092,379$ | $462$ | $681$ | $0.6784140969162996$ |

These are finite audit surfaces. They do not prove the all-scale
prime-square proximity theorem.

## Appendix C. Implementation And Audit Surfaces

The following surfaces certify implementation behavior.
They are not theorem boundaries for the two universal theorems.

### C.1 Generator Audit Surfaces

The production generator surface from $11$ through $100,000$ produced
$9,588/9,588$ exact outputs with $0$ failures.

The production generator surface from $11$ through $1,000,000$ produced
$78,494/78,494$ outputs with $0$ unresolved cases and $0$ audit failures.

The high-scale decade-window surface used $256$ consecutive primes per decade
from $10^8$ through $10^{18}$. It produced

$$
2,816/2,816
$$

exact outputs with $0$ incorrect candidates.

### C.2 Recursive Walk Surfaces

The transition rule is exact on $743,075/743,075$ rows from the combined
$10^6+10^7$ next-gap surface.

The recursive walk records $664,578/664,578$ exact consecutive next-prime
recoveries from prime $11$ through prime $10,000,121$, with $0$ skipped gaps.

The sampled decade ladder from $10^2$ through $10^{18}$ had exact hit rate
$1.0$ with $0$ skipped gaps across $860$ measured recursive steps.

The No-Later-Simpler-Composite condition follows exactly from the proved
interior maximizer theorem: for every interior integer after $w$, no later
interior composite has strictly smaller divisor count before the next prime. A
separate stress surface through $10^{18}$ records $0$ violations on that audit
surface.

## Appendix D. Later Research Status Not Used In The Main Proof

### D.1 State-Budget Measured Result

On the deterministic $8,192$-row-per-power surface from $10^{12}$ through
$10^{18}$, the measured value $d4\_count$ separates next-triad ordering under
the stated ordering rule.

The strongest measured row is:

| Field | Value |
| --- | --- |
| match mode | `mod30_prev_gap_exact` |
| measure | `d4_count` |
| decisive pairs | $7,881$ |
| held-out powers above $100$ decisive pairs | $7/7$ |
| positive oriented held-out folds | $6/7$ |
| oriented signed advantage | $299$ |
| endpoint-tail control signed advantage | $230$ |
| edge over endpoint-tail control | $69$ |
| required edge | $50$ |
| verdict | `ordering_carrier_found` |

This is a measured result. The symbolic reason why $d4\_count$ carries
next-triad ordering information remains unresolved, and replication on a
disjoint high-window construction remains unresolved.

### D.2 Semiprime Branch Audit

The semiprime branch has a committed $127$-bit official gate audit:

| Field | Value |
| --- | --- |
| scale | $127$ bits |
| cases | $12$ |
| first passing rung | $2$ |
| router top-1 recall | $1.0$ |
| router top-4 recall | $1.0$ |
| exact recovery recall | $0.75$ |
| archived exact case | recovered on official path |

This is an audit result. It is not a blind factorization claim, not a generic
all-regime semiprime recovery theorem, and not an RSA-4096 break.

## Appendix E. Invalidated Routes And Non-Claims

The old fixed cutoff map

$$
\{2:44,\ 4:60,\ 6:60\}
$$

is false. It fails at $q=24,098,209$, where the square branch gives
$E(q)=72>60$.

The literal prior-square Lemma A is false. It fails at $q=113$, where the exact
witness is the later square $121=11^2$.

The dynamic cutoff $C(q)=\max(64,\lceil 0.5\log(q)^2\rceil)$ is not an
unconditional theorem in this draft.

The measured $d4\_count$ ordering rule is not a proved symbolic law.

The semiprime $127$-bit audit is not blind factorization, a generic semiprime
theorem, or an RSA-4096 break.

## Appendix F. Reproducibility Contract

All computations summarized in this draft use exact integer divisor counts on
the stated finite ranges or deterministic audit contracts on the stated test
surfaces.

For the maximizer finite base, each row follows the same contract:

1. enumerate consecutive prime pairs in the stated left-prime range;
2. enumerate every interior integer in each nonempty gap;
3. compute exact divisor counts;
4. select the first integer with the minimum interior divisor count;
5. compare every earlier integer against $F(w)$;
6. count a failure if any earlier integer has $F(k)\ge F(w)$.

For bounded-compression scans, each row follows the contract:

1. compute the unbounded selected witness from exact divisor-count structure;
2. compute the cutoff $C(q)=\max(64,\lceil 0.5\log(q)^2\rceil)$;
3. record the first counterexample if $w-p>C(q)$;
4. otherwise record maximum offset and maximum utilization on the tested
   surface.

For generator audits, each row follows the contract:

1. input a known prime $p$;
2. emit exactly one successor record $(p,q)$;
3. verify by an audit step that $q$ is the actual next prime;
4. keep diagnostics outside the emitted record.

For state-budget and semiprime appendices, the tables state measured or audit
status only. They do not participate in the proof of the two universal
theorems.
