# Paragraph 02 Evidence: Proved Gap Foundation

## Public Claim To Support

The branch rests on a proved deterministic foundation: exact divisor counts
identify the next prime after a known prime, and inside the gap the selected
interior composite is the first point where divisor-count load is minimal.

## Supporting Evidence

- `PROOF.md` proves the direct deterministic next-prime theorem:
  compute exact divisor counts after a known prime and stop at the first
  integer with exactly two divisors.
- `PROOF.md` proves the selected-integer theorem inside the resulting gap:
  the leftmost interior integer with minimum divisor count is the unique
  maximizer of the logarithmic comparison value.
- `docs/RESULTS.md` separates these theorem claims from generator and measured
  surfaces. It states that the theorem proof lives in `PROOF.md`, and that
  audit tables are not theorem boundaries.
- `RESULTS.md` records implementation evidence for the generator:
  `9588 / 9588` exact outputs on `11..100000`, and `2816 / 2816` exact outputs
  on the `10^8` through `10^18` decade-window validation surface.

## Status Boundary

- Proved: exact divisor-count next-prime rule under stated hypotheses.
- Proved: selected interior composite theorem under stated hypotheses.
- Measured: generator surfaces and validation runs.
- Not proved here: factor recovery from a semiprime modulus.

## Infographic Concept

A prime `p` starts a horizontal gap. Composite marks appear after it with small
divisor-count labels. The next prime `q` appears at the first mark labeled
`2`. Inside the gap, one composite is highlighted as the earliest lowest-load
point.

