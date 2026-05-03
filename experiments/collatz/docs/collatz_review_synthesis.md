# Collatz Review Synthesis

## Summary

The useful review feedback is adopted as framing and definition cleanup. The
measured claims are unchanged: same-gap enrichment leads, reset-profile
separation follows, below-minimizer terminal localization identifies the sharp
carrier, and the residue identity is the exact algebraic normal form for that
carrier.

## Adopted Review Points

- `01-review.md` is reclassified as the original essay draft, not an
  independent review.
- The public and research entrypoints now separate the empirical enrichment
  claim from the deterministic residue normal form.
- The first-descent block length, reset strength, terminal source, leftmost
  divisor-count minimizer, nearest odd cells, and same-gap background rate are
  defined explicitly.
- The exact below-minimizer residue condition is stated as
  $3w \equiv 2 \pmod {2^{k}}$ and
  $3w \not\equiv 2 \pmod {2^{k+1}}$.
- The reset inequality target is kept on the short-block terminal-residue
  families rather than on a generic enrichment claim.

## Parity Correction

`04-review.md` contains a parity slip: it says "for odd `w-1` with `w` odd."
If `w-1` is odd, then `w` is even. The adopted framing uses the correct
terminal-adjacent condition: below-minimizer terminal sources have `n=w-1`
odd, so the corresponding minimizer `w` is even.

## Pressure Tests

The short-block reset candidate probe has now run the first deterministic
versions of the review-requested pressure tests:

- minimizer parity distribution over unique visited final-source gaps;
- gap-width stratification for the exact 3-step final-`v2` `4`/`8` surface;
- independent residue-bias check over unique visited final-source gaps;
- explicit `k=4` and `k=8` branch tables.
- targeted inverse counterexample scan through odd seeds `<= 100000000`.

The remaining stronger version is global rather than visited-surface-local:
measure minimizer parity, exact below-residue rates, and branch hit rates over
all prime gaps up to a fixed endpoint bound, independent of Collatz visits.

This work intentionally does not add random permutation tests. The deterministic
experiment record remains the source of the current claims.
