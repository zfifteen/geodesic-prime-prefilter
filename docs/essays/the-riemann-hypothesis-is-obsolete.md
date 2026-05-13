# The Riemann Hypothesis Is Obsolete

## Abstract

The Riemann Hypothesis is obsolete as the default dependency for exact
prime-structure methods. Its historical role is conditional control: if the
nontrivial zeros of the zeta function lie on the critical line, then error
terms in prime-distribution theorems obey sharp global constraints.

Every integer carries a divisor structure: the positive integers that divide it
evenly. A prime has exactly two such divisors, $1$ and itself. A composite has
more than two. The divisor count records that structure as a number. The
Divisor Normalization Identity, abbreviated DNI, turns this existing
divisor-count structure into a scale centered on the prime state. If $\tau(n)$
is the number of positive divisors of $n$, then DNI fixes the normalized score

$$
Z(n)=n^{1-\tau(n)/2}.
$$

Every prime has $\tau(n)=2$, so every prime maps exactly to $Z=1$. Every
composite has $\tau(n)>2$, so every composite maps below $1$. DNI turns the
prime condition into an invariant arithmetic level rather than a conditional
analytic estimate.

Consecutive primes enclose a finite stretch of composite integers. Each
integer in that stretch has a divisor count. Those counts have a smallest value
inside the gap, and that smallest value appears first at a definite integer.
Prime Gap Structure, abbreviated PGS, studies that ordered interior structure.
The Leftmost Minimum-Divisor Rule, abbreviated GWR in this repository, names
the rule that selects the first interior integer where the smallest divisor
count appears. That selected integer is the unique maximizer of the logarithmic
comparison score $F(n)=(1-\tau(n)/2)\log n$, and it forces an ordered exclusion
profile across the gap interior.

This is a methodological regime change. The proof foundation already present
in this repository gives exact local next-prime recovery and the gap-interior
maximizer theorem. The analytic bridge already present in this repository
shows that the native DNI Dirichlet-series objects reconstruct
$-\zeta'(s)/\zeta(s)$, the classical prime-power detector. The remaining global
theorem target is equally precise: show that the DNI-derived continued ratio
has all nontrivial poles on $\operatorname{Re}(s)=1/2$.

## 1. The Conditional Regime

The Riemann Hypothesis concerns the zeros of the zeta function. In its usual
form, it states that every nontrivial zero $\rho$ of $\zeta(s)$ satisfies

$$
\operatorname{Re}(\rho)=\frac12.
$$

Its power in number theory comes from translation. Zero placement controls
oscillation in prime-counting and related arithmetic functions. A method that
uses RH usually consumes a consequence of the hypothesis: a bound, an error
term, a density restriction, or a cancellation estimate that follows from the
zero geometry.

That is the conditional regime. The method asks for a prime-distribution fact.
The proof imports RH to control the analytic error. The final statement becomes
conditional even when the arithmetic object under study is finite, ordered, and
exact.

The conditional regime was natural when the analytic side was the strongest
available handle on prime distribution. It is no longer the only natural
starting point.

## 2. The Divisor-Count Regime

The arithmetic starting point is ordinary and exact. For a positive integer
$n$, let $\tau(n)$ be the number of positive divisors of $n$. An integer
$n>1$ is prime exactly when

$$
\tau(n)=2.
$$

This turns prime location into a statement about an ordered divisor-count
sequence. Given a known prime $p$, the next prime $q$ is

$$
q=\min\{n>p:\tau(n)=2\}.
$$

The integers between $p$ and $q$ form a finite ordered profile of composite
divisor counts. Inside that interval, the Prime Gap
Structure frame asks which divisor-count values appear, where the minimum first
appears, and how the sequence returns to the prime value $\tau=2$.

The same facts produce a normalized prime fixed point. The Divisor
Normalization Identity centers the arithmetic by assigning each integer the
score

$$
Z(n)=n^{1-\tau(n)/2}.
$$

Every prime maps to $Z=1$. Every composite maps below $1$. The integer line is
therefore read as an exact normalized surface: primes return to the invariant
level, and composites fall below it according to their divisor load.

This construction is deterministic. It reads an exact divisor-count field
rather than a probabilistic candidate verdict.

## 3. The Local Theorem Foundation

The local theorem foundation starts from two visible arithmetic facts.

First, exact divisor-count traversal determines the next prime after a known
prime. The rule is direct: inspect integers greater than $p$ in increasing
order and stop at the first integer with exactly two positive divisors. The
first such integer is the next prime.

Second, the composite integers inside a nonempty gap have an ordered
divisor-count profile. That profile has a smallest divisor count, and one
interior integer is the first place where that smallest count appears. That
integer is the unique maximizer of

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.
$$

Let

$$
I=\{p+1,\ldots,q-1\}
$$

and define

$$
w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}.
$$

Then $w$ is the unique maximizer of $F(n)$ on $I$.

This is a prime-distribution statement at the chamber level. Here a chamber is
the finite interior between one prime and the next. Consecutive primes cannot
enclose arbitrary interior divisor-count profiles. Before the selected integer
$w$, every earlier interior integer has divisor count strictly larger than
$\tau(w)$. After $w$, every later interior integer has divisor count at least
$\tau(w)$ until the next prime closes the gap.

The gap has an exact forbidden-prefix structure and an exact constrained-suffix
structure. RH supplies global analytic control from zero placement. PGS supplies
local arithmetic control from ordered divisor-count exclusion.

## 4. The Analytic Bridge

The Riemann Hypothesis lives on the analytic side of the same arithmetic world.
The divisor-count normalization reaches that side directly.

Start with the divisor-count Dirichlet series on
$\operatorname{Re}(s)>1$:

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

The next building block is the logarithmic load carried by the same divisor
count. The DNI divisor-normalization load is

$$
\kappa(n)=\frac{\tau(n)\log n}{e^2}.
$$

Its generating series is

$$
K(s)=\sum_{n\ge1}\frac{\kappa(n)}{n^s}
=\frac{1}{e^2}\sum_{n\ge1}\frac{\tau(n)\log n}{n^s}.
$$

Termwise differentiation gives

$$
D'(s)=-\sum_{n\ge1}\frac{\tau(n)\log n}{n^s},
$$

so

$$
K(s)=-\frac{1}{e^2}D'(s).
$$

At the native DNI scaling parameter $v=e^2/2$,

$$
\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac12\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The right-hand side is the classical logarithmic derivative of the zeta
function:

$$
-\frac{\zeta'(s)}{\zeta(s)}
=\sum_{n\ge1}\frac{\Lambda(n)}{n^s},
$$

where $\Lambda(n)$ is the von Mangoldt function.

This is the exact bridge. The native DNI objects built from divisor count and
logarithmic load reconstruct the standard analytic prime-power detector.

## 5. Why RH Becomes Methodologically Obsolete

RH is a condition on the analytic continuation of the zeta function. The
divisor-count side begins with the object whose Dirichlet series is
$\zeta(s)^2$, then normalizes its logarithmic derivative to recover
$-\zeta'(s)/\zeta(s)$. That is the DNI bridge in analytic form.

The consequence is structural. A method that currently relies on RH should be
decomposed into the exact statement it borrows from RH. That borrowed statement
then becomes a proof target inside Prime Gap Structure.

The replacement ledger has the following form:

```text
RH-dependent step
-> exact analytic consequence being used
-> relevant PGS object
-> relevant PGS invariant
-> proved PGS theorem, unresolved PGS target, or invalidated route
```

This changes the role of RH. It stops being the master assumption and becomes
an index of replacement targets. Each conditional lemma asks for its own
PGS-native proof.

The strongest form of the regime change is:

$$
\text{conditional on RH}
\quad\longrightarrow\quad
\text{proved from DNI/PGS structure}.
$$

The local theorem foundation already demonstrates the pattern. Exact
divisor-count traversal determines the next prime. The interior maximizer
theorem identifies the unique gap-selected integer from the ordered
divisor-count profile. The analytic bridge places the same divisor-count
normalization at the logarithmic derivative of zeta.

## 6. The Global Theorem Target

The complete global bridge has a precise theorem target. Define the
DNI-derived continued ratio

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}.
$$

On $\operatorname{Re}(s)>1$,

$$
R(s)=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The poles of $-\zeta'(s)/\zeta(s)$ occur at zeros and poles of $\zeta(s)$,
with residues recording their multiplicities. The literal RH-level theorem
target is therefore:

$$
\text{Every nontrivial pole of } R(s) \text{ lies on }
\operatorname{Re}(s)=\frac12.
$$

That statement is the exact algebraic form of the claim that DNI proves RH. It
names the object, the continuation, and the pole placement property.

The method-level replacement program is broader than that single theorem. Many
RH-dependent arguments use specific consequences rather than the full zero-line
statement. Each such consequence admits a sharper audit:

1. What bound or structural fact does RH provide here?
2. Which arithmetic object is being controlled?
3. Which PGS chamber invariant controls that object directly?
4. Is the PGS statement proved, measured, unresolved, or invalidated?

That audit converts conditional analytic dependence into exact arithmetic proof
obligations.

## 7. Status

The proved theorem foundation is local and exact. It includes the direct
deterministic next-prime rule and the gap-interior maximizer theorem under
their stated hypotheses.

The measured implementation surfaces certify generator behavior and recursive
walk behavior over their recorded regimes. They are implementation evidence
rather than theorem boundaries.

The analytic bridge is exact on $\operatorname{Re}(s)>1$ and determines the
same meromorphic continuation through the zeta identity:

$$
D(s)=\zeta(s)^2,\qquad
K(s)=-\frac1{e^2}D'(s),\qquad
R(s)=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The global pole-location theorem remains the explicit RH-level target.

The regime change is already real at the level of method. RH-dependent methods
no longer need to be treated as permanently conditional whenever their consumed
RH consequence has an exact divisor-count chamber replacement. The correct
question is no longer whether RH is assumed. The correct question is which
PGS-native invariant proves the exact result that RH had been used to supply.

## References

- [Proof](../../PROOF.md)
- [Results Map](../../RESULTS.md)
- [DNI and the Riemann Hypothesis](../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [Prime-Gap Exclusion Consequences of GWR](../../research/02-gwr-dni/docs/prime_gap_exclusion_consequences.md)
