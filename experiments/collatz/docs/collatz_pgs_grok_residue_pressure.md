# Collatz-PGS Grok Residue Pressure Check

## Question

Does the below-witness terminal contact result look like a mechanism-bearing
arithmetic object, or only an empirical reset marker?

## Context Sent

The second-opinion check received the measured chain through the
below-witness family decomposition:

- same-gap witness hit ratio `1.7637165846198448` at odd seeds
  `3 <= s <= 999999`;
- witness-contact blocks reset harder/faster in the same-gap scale probe;
- exact reset-length strata preserve a positive matched-weighted mean of
  stratum median reset ratio `1.6163417109769`;
- terminal exact and adjacent contact both remain positive against no-witness
  blocks, with adjacent stronger than exact;
- below-witness terminal contact carries the adjacent-side advantage;
- below-witness stability is positive against above-witness at median, P90,
  and P99, but against no-witness it is median-positive and P90/P99-negative;
- exact `(odd_steps_to_first_descent, final_v2)` family decomposition preserves
  the median-positive and tail-negative below-vs-no-witness result;
- if the terminal source is `witness - 1` and final `v2=k`, then
  `witness` satisfies `w ≡ 2 * 3^{-1} mod 2^k`.

## Grok Answer

Grok's strongest reading was:

```text
below-witness terminal contact is a mechanism-bearing arithmetic object: the
exact residue condition w ≡ 2 * 3^{-1} mod 2^k directly filters terminal
sources to produce the observed side-specific median reset advantage.
```

Grok's main pressure point was that the upper-tail reversals show the median
effect is not globally stable. The residue identity explains side specificity,
but it does not yet explain why short exact-step families carry the positive
mass or why families such as `(12, 11)` reverse the tail.

## Concrete Next Action

Grok recommended moving from broad measurement to algebra:

```text
Algebraically expand the 2-3 map for the single highest-weighted positive
carrier family (odd_steps=3, final_v2=4) under the fixed residue
w ≡ 2 * 3^{-1} mod 16, then close the form after one full descent block and
measure the exact reset-length contraction ratio against the non-residue case.
```

## Disposition

The second opinion confirms the local conclusion. The reset-certificate
experiment has produced a real arithmetic object, not only a visual pattern:
terminal adjacent PGS contact is Collatz residue contact on the PGS witness.

The same result also sets the stop condition for this experimental phase.
More broad enrichment and reset-profile probes are now low value. The next
phase is proof pressure on short-block residue families.
