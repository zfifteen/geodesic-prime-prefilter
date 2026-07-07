# Leftmost Minimum-Divisor Rule

The first thing a prime gap gives you is not a formula. It gives you a row of composite numbers.

Between `23` and `29`, the row is short:

```text
23 | 24 25 26 27 28 | 29
```

If you only measure the width of the gap, you get the number `6`. That is true, but it throws away the arithmetic inside the interval. The interior numbers are composite, and every composite has a divisor count.

Write the counts underneath the same row:

```text
number:        24  25  26  27  28
divisor count:  8   3   4   4   6
```

Now the gap is no longer just a distance. It has an ordered interior. The smallest divisor count is `3`, and it appears at `25`.

That number is the selected composite of the gap. It is not the next prime. It is the first place inside the gap where the interior reaches its lowest divisor count.

## Why Leftmost Matters

A single small gap can make the rule look easier than it really is. In the gap from `23` to `29`, only one number has the lowest count. There is no tie to resolve.

The gap from `89` to `97` shows why the left-to-right order matters:

```text
89 | 90 91 92 93 94 95 96 | 97
```

The divisor counts are:

```text
number:        90  91  92  93  94  95  96
divisor count: 12   4   6   4   4   4  12
```

The lowest count is `4`, and it appears at `91`, `93`, `94`, and `95`. The gap is not only telling you which count is smallest. It is also telling you where that count first appears. Read from left to right, the first lowest-count composite is `91`.

That is the Leftmost Minimum-Divisor Rule: inside a prime gap with at least one interior integer, find the lowest divisor count in the interior, then take the first integer where that count appears.

The repository also uses the historical name `GWR` for this rule. The name matters less than the visible arithmetic. The selected composite is the first interior number that carries the minimum divisor count of the gap. In the preferred zero-excess coordinate, it is the leftmost interior number with minimum excess.

## What The Rule Contradicts

The usual way to talk about prime gaps treats the composites between primes as failed candidates. They are numbers you pass over while looking for the next prime.

The rule reverses that view. The interior composites are not just discarded numbers. They carry the ordered divisor-count pattern of the gap. The selected composite is the first minimum in that pattern.

This is why the rule is a local arithmetic choice rather than a statistical summary. It does not say what usually happens across many gaps. It points to one exact integer inside one exact gap.

## Why The Score Exists

Divisor count already shows the rule in ordinary arithmetic. But the project also wants a single comparison value for every interior composite, so the whole gap can be read as an ordered list of scores.

The score is built around the prime baseline. A prime greater than `1` has divisor count `2`. Under the zero-excess coordinate, every prime greater than `1` lands at `E = 0`, while composites have positive excess:

$$E(n)=\left(\frac{d(n)}{2}-1\right)\ln(n)$$

That makes the selected composite easy to interpret: among the composites inside the gap, it is the first one at the minimum excess level. The historical normalized score remains the exact dual coordinate:

$$Z(n)=n^{1-d(n)/2}=e^{-E(n)}$$

The logarithm of the dual score is:

$$F(n)=\ln Z(n)=\left(1-\frac{d(n)}{2}\right)\ln(n)$$

Since `F(n)=-E(n)`, maximizing `F(n)` is the same ordered comparison as minimizing `E(n)`. Maximizing `Z(n)` picks the same selected composite. The score is not decorative language. It is the normalized version of the same choice the divisor-count table already made visible: lowest divisor count first, then leftmost position among ties.

## Proof Status

The theorem proved in [PROOF.md](../../PROOF.md) has two connected parts. First, exact divisor counts determine the next prime after a known prime. Second, inside the resulting prime gap with nonempty interior, the logarithmic comparison function is maximized at exactly the leftmost interior integer with minimum divisor count. In zero-excess coordinates, this says the selected integer is the leftmost minimum-excess interior integer.

GWR identifies *where* the minimum sits once the gap interior is fixed. It does
not by itself bound how far that minimum can sit from the left endpoint. That
distance bound is a separate proved theorem: universal bounded compression
(2026-07-05), with the square branch closed by the Prime-Square Proximity
Theorem. See [PROOF.md](../../PROOF.md) §Prime-Square Proximity Theorem.

The theorem is universal under its stated hypotheses. Audit tables in `PROOF.md` preserve certification and provenance; they are not limits on the theorem.
