# Uncovered-Set Decay For Essential Cover Weight

Date: 2026-05-24

Status: candidate proof route for the Essential Shifted-Cover Weight Lemma.

The bare active-prime covering sum is too loose. A large singleton label `p>N`
has small density `1/p`, but there are many possible large primes. The missing
factor is the least-divisor exclusion: before `p` can label an offset, every
smaller odd prime channel must miss that offset.

The right object is therefore not an unrestricted family of active covering
systems. It is the uncovered-set process obtained by revealing prime channels
in increasing order.

## Residue Process

Fix odd-offset length `N` and let

$$
Y=\sqrt{2X}.
$$

For each odd prime `p <= Y`, the even center `M=2m` determines one residue
class

$$
a_p(M)\pmod p
$$

such that

$$
p\mid M-(2s+1)
\quad\Longleftrightarrow\quad
s\equiv a_p(M)\pmod p.
$$

Define the uncovered set after processing odd primes up to `y`:

$$
U_y(M)=
\{0\le s<N:s\not\equiv a_p(M)\pmod p
\text{ for every odd prime }p\le y\}.
$$

The canonical least-divisor word is exactly the first-hit record of this
process. An offset gets label `p` precisely when it lies in `U_{p^-}` and is
hit by the class `a_p mod p`.

A complete odd-offset cover is the extinction event

$$
U_Y(M)=\varnothing.
$$

## Target Decay Estimate

The Essential Shifted-Cover Weight Lemma follows from:

> **Uncovered-Set Extinction Bound.**
> For dyadic centers `M in [X,2X]`,
> $$
> \#\{M:U_{\sqrt{2X}}(M)=\varnothing\}
> \ll
> X(\log X)^B/N^2.
> $$

Equivalently, in the ideal CRT residue model where the classes `a_p` are
uniform, one wants

$$
\mathbb P(U_Y=\varnothing)
\ll
\frac{(\log X)^B}{N^2}.
$$

This is the exact probability version of the canonical word entropy theorem.
It includes inactive smaller-prime misses automatically.

## Induction On Prime Channels

Condition on the uncovered set `U` just before prime `p` is revealed. For
each residue class `a mod p`, let

$$
h_p(a;U)=\#\{s\in U:s\equiv a\pmod p\}.
$$

Revealing `a_p=a` sends

$$
U\mapsto U\setminus\{s\in U:s\equiv a\pmod p\}.
$$

A generating-function induction would study

$$
F_y(t)=\mathbb E[t^{|U_y|}].
$$

The one-prime transition is

$$
\mathbb E[t^{|U_p|}\mid U_{p^-}=U]
=
\frac1p
\sum_{a\bmod p}t^{|U|-h_p(a;U)}.
$$

The extinction probability is

$$
F_Y(0).
$$

Thus a proof can aim to show that the transition product keeps `F_Y(0)` below
`(\log X)^B/N^2`.

## Expected Size Is Not Enough

The expected uncovered size follows the familiar sieve scale:

$$
\mathbb E|U_y|
=
N\prod_{3\le p\le y}\left(1-\frac1p\right)
\asymp
\frac{N}{\log y}.
$$

For `y=sqrt(2X)`, this gives expected size about

$$
N/\log X.
$$

This controls the first moment of survivors. It does not by itself bound the
lower tail

$$
\mathbb P(U_Y=\varnothing).
$$

The needed estimate is a lower-tail or extinction bound for the shifted sieve
process.

## Two Regimes

**Small offset length: `N <= (log X)^C`.**
The desired bound

$$
X(\log X)^B/N^2
$$

is weak enough that finite-base and first-moment estimates may absorb this
range after choosing `B` large.

**Long offset length: `N >> log X`.**
The expected uncovered set has size growing with `N/log X`. Extinction should
be rare. The proof needs a quantitative lower-tail estimate showing that the
uncovered set does not collapse to zero too often.

## Candidate Analytic Tools

**Second moment of survivors.**
Let

$$
Z_Y(M)=|U_Y(M)|.
$$

If one can prove a variance bound strong enough to keep `Z_Y` near its mean,
then extinction is rare when `N/log X` is large.

**Janson-type covering inequality.**
The event `U_Y=empty` is a random-cover event for the interval `[0,N)`.
Dependency comes from nearby offsets sharing small prime channels. A
Janson-style inequality for the shifted sieve would directly bound the
probability that all offsets are covered.

**Deterministic Selberg-weight majorant.**
Instead of probabilistic language, one can majorize the extinction indicator by
a Selberg sieve weight for the absence of reduced residues in the odd-offset
window. This would keep the result arithmetic and dyadic rather than relying
on a full-period random model.

## Principal Obstacles

**Full-period CRT is larger than the dyadic block.**
The product of prime moduli up to `sqrt X` is enormous. Uniform random residue
language is exact on a full CRT period, but the theorem needs centers in
`[X,2X]`. The proof must be phrased as a sieve majorant or with controlled
finite-modulus truncation.

**Extinction is a lower-tail event.**
First-moment sieve estimates count expected survivors. The bridge needs the
probability of no survivor at all.

**Short primes create dependencies.**
A single small prime residue class removes many offsets. This makes survivor
events correlated and blocks a naive independent-offset estimate.

**The result is equivalent in force to a prime-gap tail.**
The extinction event says that no odd zero-excess endpoint occurs in the
window. Proving the `N^-2` tail is the even-channel return-time theorem in
uncovered-set language.

## Minimal New Estimate

The next theorem should be stated as:

> **Shifted Sieve Extinction Estimate.**
> For `Y=sqrt(2X)` and every `N`, the odd-prime residue process attached to
> even centers `M in [X,2X]` satisfies
> $$
> \#\{M\in[X,2X]:U_Y(M)=\varnothing\}
> \ll
> X(\log X)^B/N^2.
> $$

This estimate would prove the Essential Shifted-Cover Weight Lemma with the
least-divisor exclusions included, and therefore close the canonical word
entropy obstruction.

## Result

The active proof route is uncovered-set decay. It converts least-divisor word
entropy into an extinction estimate for a shifted divisor-channel sieve. The
remaining obstruction is a quantitative lower-tail bound, not LCM growth and
not local GWR ordering.
