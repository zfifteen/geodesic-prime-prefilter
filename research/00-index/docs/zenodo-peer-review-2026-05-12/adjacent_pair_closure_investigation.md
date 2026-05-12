# Adjacent Pair Closure Investigation

Date: 2026-05-12

## Finding

The reviewer examples `(36,37)`, `(64,65)`, and `(72,73)` are closed. The
large-prime ratio lemma closes those concrete rows directly, and the new
short-interval divisor-average closure closes the full adjacent-pair tail.
The pair `(64,65)` also closes by direct enumeration of every possible
`tau(k)=65` earlier carrier in its Bertrand unresolved window.

The reproducibility script is:

```text
research/02-gwr-dni/scripts/proof/adjacent_pair_closure_certificate.py
```

The emitted certificate is:

```text
research/02-gwr-dni/output/gwr_proof/adjacent_pair_closure_certificate_20260512.json
```

The large-prime ratio certificate fixes the concrete reviewer objection for
pairs like `(64,65)`. The universal tail closure is supplied by the
short-interval divisor-average argument recorded below and patched into the
proof.

## Large-Prime Ratio Lemma

Let `p<q` be consecutive primes and assume the committed finite base has
already closed every gap with

```text
p < 5,000,000,000.
```

For the remaining gaps put

```text
P0 = 5,000,000,000
alpha = 1 + 1 / (25 log(P0)^2)
      = 1.0000802005564475...
```

The explicit prime-gap ratio bound gives

```text
q / p < alpha
```

for every remaining gap. If `k<w` is an earlier integer with
`e = tau(k)` and `d = tau(w) < e`, then `k>p` and `w<q<alpha p<alpha k`.

The hardest comparison for fixed `e` is the adjacent case `d=e-1`. Therefore
it is enough to prove

```text
k^(e-2) > w^(e-3).
```

Since `w < alpha k`, this follows from

```text
k > alpha^(e-3).
```

Thus every earlier divisor class `e` is closed whenever

```text
M(e) > alpha^(e-3),
```

where `M(e)` is the least positive integer with exactly `e` divisors.

## Reviewer Pairs

Using the same `P0 = 5,000,000,000` ratio:

| Winner divisor count `d` | Earlier divisor count `e` | `M(e)` | `alpha^(e-3)` | Result |
|---:|---:|---:|---:|---|
| `36` | `37` | `68,719,476,736` | `1.0027304304325557` | closed |
| `64` | `65` | `331,776` | `1.0049846171891061` | closed |
| `72` | `73` | `4,722,366,482,869,645,213,696` | `1.0056296008196461` | closed |

For `(64,65)`, the proof is especially small:

```text
M(65) = 331,776 > alpha^62.
```

So every earlier `tau=65` integer has `F(k)<F(w)` against any later
`tau=64` winner in the post-base regime.

## Independent Exact Carrier Enumeration For `(64,65)`

The Bertrand unresolved window for `(64,65)` has

```text
T(64,65) = 2^62,
q < 2T = 2^63.
```

Because `65` is odd, every integer with `65` divisors is a square. The only
exponent patterns below `2^63` are:

```text
(64)
(12, 4)
```

The exact enumeration found:

| Quantity | Value |
|---|---:|
| `tau=65` carriers below `2^63` | `1,318` |
| carriers with preceding prime in `(5e9, 2^62]` | `1,118` |
| realized `tau=64` winner branches after such a carrier | `0` |
| realized `(64,65)` earlier-winner pairs | `0` |

This is an independent deterministic closure of the concrete `(64,65)` branch.

## Extended Class Scan

The fixed-ratio lemma with `P0=5e9` closes every earlier divisor class

```text
4 <= e <= 262,144.
```

A direct scan from `e=600,001` through `e=1,048,576` found the first
fixed-ratio unresolved adjacent row at

```text
(d,e) = (645,119, 645,120).
```

Adding the winner-side lower bound `w >= M(d)` tightens the prime-gap ratio.
For each fixed-ratio unresolved row through `e=1,048,576`, this two-sided
ratio check closes the row.

The two-sided ratio check is still not a universal tail proof. Power-of-two
probes show later failures of this mechanism:

| `e` | `d=e-1` | `log M(d)` | `log M(e)` | two-sided threshold log | Result |
|---:|---:|---:|---:|---:|---|
| `2^28` | `268,435,455` | `347.18447738327893` | `88.10745538137895` | `89.07983304013777` | not closed by this mechanism |
| `2^30` | `1,073,741,823` | `486.4563487884003` | `97.0149323589077` | `181.49815514000943` | not closed by this mechanism |

## Universal Adjacent-Pair Closure

The infinite adjacent-pair tail is closed by a deterministic divisor-average
argument.

Let `p<q` be consecutive primes above the finite base, let `w` be the first
interior integer with minimum divisor count, and put

```text
d = tau(w) >= 4
L = log(w)
```

Bertrand gives `w<q<2p`, hence `p>w/2`. If

```text
(d - 2) log(2) <= L - log(2),
```

then `2^(d-2) <= w/2 < p`, so the Threshold Lemma closes the adjacent row
`(d,d+1)` and therefore every larger earlier divisor count.

In the remaining case,

```text
(d - 2) log(2) > L - log(2).
```

Since `w>5e9`, this implies

```text
d > L + 2 + 32/L.
```

Set

```text
H = floor(w L / (4(d - 1))).
```

For any interval `J={w-H,...,w-1}`,

```text
sum_{n in J} tau(n) <= H(L + 2) + 2 sqrt(w).
```

This follows by pairing divisors and counting multiples of each
`a <= sqrt(w)` across the `H` consecutive integers.

Since `tau(w)=d <= 2 sqrt(w)`, the chosen `H` satisfies

```text
H >= w L / (8(d - 1)).
```

Therefore the average divisor count on `J` is at most

```text
L + 2 + 2 sqrt(w)/H
<= L + 2 + 32/L
< d.
```

So some `n in J` has `tau(n)<d`. That integer cannot lie strictly between
`p` and `w`, because `w` is the first interior integer where the gap minimum
divisor count is attained. Hence `n<=p`, and every earlier competitor `k`
satisfies

```text
k > p >= n >= w - H.
```

With `x=H/w`, we have

```text
x <= L/(4(d - 1)) < 1/4
```

and therefore

```text
log(w/(w-H)) < x/(1-x) < L/(d - 1).
```

Thus

```text
(d - 1) log(w - H) > (d - 2) log(w).
```

For every earlier integer with `e=tau(k)>d`,

```text
e - 2 >= d - 1
```

and `k>=w-H+1>w-H`, so

```text
(e - 2) log(k) > (d - 2) log(w).
```

That is exactly `F(k)<F(w)`.

## Proof Implication

The Zenodo proof no longer needs the retained-row classification table for the
earlier side. The finite base handles `p<5,000,000,001`; above that base, the
threshold case and the short-interval divisor-average case close every
adjacent pair. The concrete rows `(36,37)`, `(64,65)`, and `(72,73)` are
instances of this deterministic closure.
