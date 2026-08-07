# Heuristics Derived from Witness Offset Structure

The observed concentration of GWR witness offsets at small integers supports the following practical heuristics.
Each heuristic remains compatible with the exact GWR selection rule and the proved universal bound.

## Heuristic 1: Early-Window Priority Scan

Scan the first 20 integers after each prime first.
Most winners already appear inside that short window.
Extend the scan only when the current minimum divisor count stays high after the early window.

Rationale: more than 99 percent of measured offsets are at most 10.
A window of 20 covers essentially all ordinary cases.

## Heuristic 2: Running-Minimum Early Abort

Track the smallest divisor count found so far while walking the gap.
Stop the search for a better winner once the remaining distance exceeds the current running minimum under the known bound.
This cuts unnecessary divisor computations on the right side of the gap.

## Heuristic 3: Envelope-Guided Window

Fit a slow-growing upper envelope to the observed maximum offsets.
Use that empirical envelope for ordinary searches.
Reserve the larger proved bound max(64, 0.5 (ln q)^2) only for certification or formal proof work.

## Heuristic 4: Layered Candidate Ranking

Rank candidate integers inside the early window by expected divisor count.
Prefer squares and odd semiprimes first.
These types produce the low-divisor winners that dominate the lower bands in the plot.

## Heuristic 5: Offset-Frequency Prior

Build a frequency table of observed offsets from the dense horizontal layers.
Use the table as a prior when sampling candidate locations for larger untested ranges.
This guides probabilistic or beam-search methods toward high-probability offsets.

## Heuristic 6: Adaptive Step Size

Increase the step size after a long stretch of high-divisor integers.
The plot shows that large offsets remain rare.
A larger step still respects the overall compression.

## Implementation Notes

All heuristics preserve exactness when the final selection still applies the true Gap Winner Rule.
They only change the order or the early termination of the search.
Timing experiments on the 10 to 10^6 surface can quantify the average reduction in divisor evaluations.
