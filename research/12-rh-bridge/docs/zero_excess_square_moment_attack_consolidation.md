# Zero-Excess Square-Moment Attack Consolidation

Date: 2026-05-24

Status: attack-surface consolidation for the Zero-Excess Return
Square-Moment Theorem.

The live endpoint-chain theorem is

$$
\sum_{X<q\le2X}(q-p(q))^2
\ll
X(\log X)^B.
$$

This note consolidates the equivalent forms and the candidate proof routes.

## Equivalent Forms

The theorem can be attacked through several equivalent or sufficient forms.

1. **Dyadic gap square moment.**
   $$
   \sum_{X<q\le2X}g(q)^2
   \ll
   X(\log X)^B.
   $$

2. **Reciprocal gap energy.**
   $$
   \sum_q\frac{g(q)^2\log q}{q^2}<\infty.
   $$

3. **Zero-excess age energy.**
   $$
   \sum_{X<n\le2X}a(n)
   \ll
   X(\log X)^B.
   $$

4. **Age-divisor recurrence potential.**
   $$
   \sum_{X<n\le2X}a(n)(\tau(n)-2)
   \ll
   X(\log X)^B.
   $$

5. **Positive-excess return tail.**
   $$
   N_X(H)\ll X(\log X)^B/H^2.
   $$

6. **Endpoint-lattice crossing energy.**
   The `d=2` divisor-channel crossing energy satisfies
   $$
   \mathfrak C_2(X)\ll X(\log X)^B.
   $$

These forms all encode the same endpoint-chain obstruction.

## Candidate Lines Of Attack

### 1. Age-Divisor Recurrence

Use the PGS-native potential

$$
\Phi(n)=a(n)(\tau(n)-2).
$$

This is the most direct source-side object. It vanishes at zero-excess
endpoints, is positive inside chambers, and has quadratic per-run cost.

Required new theorem:

```text
dyadic total of Phi(n) is O(X log^B X).
```

Main obstruction:

```text
no current theorem controls accumulated age-divisor load over all chambers.
```

### 2. Divisor-Channel Age Orthogonality

Expand the age-divisor potential through divisor channels and prove

$$
\sum_{\substack{X<n\le2X\\ d\mid n}}a(n)
\ll
\frac{X}{d}(\log X)^B
$$

uniformly for `d <= sqrt(2X)`.

Required new theorem:

```text
endpoint-modulus age recurrence for every divisor channel.
```

Main obstruction:

```text
long gaps raise all channel ages at once; channel sums are positively
correlated, not automatically orthogonal.
```

### 3. Endpoint Occupancy

Prove directly that endpoint samples

$$
\sum_{q\le X}g(q)\frac{\log q}{q}
$$

have the same finite part as

$$
\sum_{2<n\le X}\frac{\log n}{n}.
$$

Required new theorem:

```text
sampling error has finite limit.
```

Main obstruction:

```text
sampling error is controlled by reciprocal gap energy, so this route still
needs the square-moment theorem.
```

### 4. Quantitative Chamber Grammar

Promote measured finite-state or finite-memory chamber grammar into an
all-scale width-tail theorem:

$$
N_X(H)\ll X(\log X)^B/H^2.
$$

Required new theorem:

```text
proved all-scale grammar with a width-energy Lyapunov function.
```

Main obstruction:

```text
current grammar work is measured evidence, not an admissibility theorem with
tail constants.
```

### 5. Modulus-Link Endpoint-Lattice Closure

Use endpoint residual sequences against divisor-channel lattices.

Required new theorem:

```text
uniform crossing-energy closure for d <= sqrt(2X).
```

Main obstruction:

```text
d=2 already equals one quarter of the gap-square moment, so modulus-link
closure does not bypass the central square-moment theorem.
```

## Most Promising Line

The strongest current line is the Age-Divisor Recurrence route.

It is closest to the PGS source:

```text
zero-excess age
divisor surplus
positive-excess persistence
quadratic return-time cost
```

It gives a concrete recurrence potential rather than an external distribution
claim. The next theorem to attack is:

> **Age-Divisor Energy Bound.**
> $$
> \sum_{X<n\le2X}(n-p(n))(\tau(n)-2)
> \ll
> X(\log X)^B.
> $$

## Deepest Remaining Obstruction

Every route requires a local-to-global recurrence theorem:

```text
local divisor-count structure forces zero-excess returns often enough that
return-time squares have dyadic total O(X log^B X).
```

Current PGS machinery proves exact local placement and local chamber ordering.
It does not yet prove a global return-time frequency law.

That is the deepest remaining obstruction behind the endpoint-chain side of
the Chamber-Centered Von Mangoldt finite-part program.
