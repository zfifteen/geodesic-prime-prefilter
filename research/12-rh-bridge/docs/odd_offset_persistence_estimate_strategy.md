# Odd-Offset Persistence Estimate Strategy

Date: 2026-05-24

Status: second-step note for the Even-Channel Age Recurrence attack.

The Even-Channel Age Recurrence theorem asks for

$$
\sum_{\substack{X<n\le2X\\ 2\mid n}}(n-p(n))
\ll
X(\log X)^B.
$$

Equivalently, even centers with long backward distance to the previous
zero-excess endpoint must have a square-summable tail.

## Odd-Offset Persistence

Let `n = 2m` be an even center and let

$$
a(2m)=2m-p(2m).
$$

If

$$
a(2m)\ge H,
$$

then every odd integer in the backward interval

$$
2m-H < r < 2m
$$

is composite unless it is the previous endpoint itself at the left boundary.

Thus a long even-channel age means a long block of odd offsets before `2m`
has positive excess:

$$
E(2m-j)>0
\qquad
j=1,3,5,\ldots,H'
$$

for the relevant odd offsets.

The needed estimate is:

> **Odd-Offset Persistence Estimate.**
> $$
> \#\{2m\in[X,2X]:a(2m)\ge H\}
> \le
> C X(\log X)^B/H^2.
> $$

## Divisor-Channel Covering Form

Each odd composite

$$
2m-j
$$

has at least one odd proper divisor channel. Therefore a long persistence
event gives a complete covering of the odd offset set

$$
\{1,3,5,\ldots,H'\}
$$

by congruence conditions

$$
2m-j\equiv0\pmod d,
\qquad
d>1,\ d\text{ odd}.
$$

Equivalently,

$$
2m\equiv j\pmod d.
$$

So the even-channel persistence problem can be stated as:

```text
count even centers 2m for which every odd offset up to H is covered by at
least one odd divisor-channel congruence.
```

This is a PGS-native divisor-covering problem.

## Candidate Mechanism

A proof would need to show that complete odd-offset divisor coverings of
length `H` are rare:

```text
long odd-offset positive-excess profile
-> many simultaneous divisor-channel congruence requirements
-> center 2m lies in a small set of residue configurations
-> number of centers with full coverage has H^-2 tail.
```

The mechanism is not primality testing. It counts persistence of positive
excess in the odd offsets before even centers.

## Structural Obstacles

**Certificates are not unique.**
An odd composite can have many proper divisors. The proof must count covered
offset profiles without overcounting arbitrary divisor-certificate choices.

**The covering is center-dependent.**
For each center `2m`, the available divisors of `2m-j` vary with `j` and `m`.
There is no fixed covering system for all centers.

**Average divisor surplus is insufficient.**
Knowing that many offsets have divisor channels does not prove that full
coverage of all odd offsets is rare with an `H^-2` tail.

**GWR sees only realized chambers.**
The GWR selector identifies the minimum-excess point once a chamber is known.
The odd-offset persistence estimate counts possible long backward profiles
around every even center. Current GWR machinery does not count those profiles.

## Required New Ingredient

The missing theorem is:

> **Odd Divisor-Covering Tail Theorem.**
> Odd-offset intervals of length `H` that are completely covered by proper
> divisor-channel congruences occur with frequency
> $$
> O(X(\log X)^B/H^2)
> $$
> among even centers in `[X,2X]`.

This theorem would prove the even-channel age recurrence theorem and therefore
the zero-excess return square-moment theorem.

## Result

The even-channel attack has reduced to a concrete divisor-field covering
problem over odd offsets. The current PGS machinery does not yet provide the
required covering-tail theorem.
