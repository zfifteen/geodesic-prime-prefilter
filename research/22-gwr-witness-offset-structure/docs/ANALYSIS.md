# Analysis of Observed Structures in GWR Witness Offsets

## Data Surface

The primary surface contains every prime gap between 10 and 10^6.
The surface holds 78 493 gaps.
Each gap contributes one witness offset defined by the Gap Winner Rule.

## Visual Structure

The scatter plot of offset versus ln(q) on a logarithmic vertical scale shows three dominant features.

1. Dense horizontal bands at the lowest integers.
   Offsets of 1, 2, 3, 4 and 5 form continuous layers across the entire horizontal range.

2. Rapid density decay with height.
   Points above offset 10 become sparse.
   Points above offset 20 are almost absent.

3. Slow rise of the upper envelope.
   The highest observed offsets increase gradually with ln(q).
   The rise remains far slower than the quadratic-log proved bound.

## Numerical Summary

From the 78 493 measured offsets:

- Median equals 2.0.
- Mean equals approximately 3.15.
- 90th percentile equals 6.
- 95th percentile equals 7.
- 99th percentile equals 10.
- Maximum equals 48.

More than 84 percent of all winners lie at most 5 steps after the left prime.
More than 99 percent lie at most 10 steps after the left prime.

## Interpretation

The leftmost minimum-divisor integer appears very early in almost every gap.
This behavior is consistent with the ordered-dominance argument that closes the later flank of the Gap Winner Rule.
Low-divisor composites (especially squares and odd semiprimes of small depth) tend to occur near the left edge of the gap more often than a uniform model would predict.

The large gap between the empirical cloud and the proved bound shows that the analytic bound, while universal, is conservative on the examined range.

## Implications for Further Work

The extreme concentration supplies a practical search prior.
Any algorithm that walks from p can safely examine a short initial window first.
Only rare cases require the full proved window.

The same concentration may survive on the reduced gap-type surface.
If it does, the finite-state generative engine can be augmented with an offset prior.

## Limitations

The present surface stops at 10^6.
Larger ranges may reveal a slower growth in the upper envelope.
The statistics do not yet condition on the arithmetic type of the winner.
