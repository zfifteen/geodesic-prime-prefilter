# D2 Pilot — Deferred

**Author:** claude  
**Date:** 2026-07-15  
**Status:** hard defer with concrete blocker  
**References:** `KILL_ADJUDICATION_R0.md` §D2 section; `KILL_SHAPES.md` K2-b

---

## Decision: Defer

D2 cannot execute a valid gap-width-matched comparison until D1 R1 establishes the continuous gap-width stratification protocol.

## Concrete blocker

K1-b and K1-c both fire at R0. D2's design relies on comparing constellation-anchor interiors against gap-width-matched controls (see K2-b). Those controls require a stable, tested stratification methodology — specifically, the continuous percentile-cohort reclass developed in K1-b's redesign — to be validated at R1 scale first.

Running D2 at R0 produces a confounded comparison: constellation anchors (especially twin-prime anchors) automatically have small gaps; any interior difference observed would be indistinguishable from the K1-b gap-width effect, not from the constellation label. The test would have no discriminating power.

## What unblocks D2

1. D1 R1 (p ≤ 10^7) runs with the continuous gap-width quartile protocol.
2. The reclass method proves stable across log-bins at R1 scale.
3. D2 imports the control design directly from D1 R1 stratification.

## What D2 is not waiting for

- It is not waiting for gap > 1000 to appear naturally (that is the old H-fixed framing, not the redesigned one).
- It is not waiting for a theory breakthrough; only the measurement methodology needs to be established.

## Next step for D2

Once D1 R1 summary is on disk and stable, D2 re-opens with this structure:

1. Sieve enumerates admissible constellation hits (p, p+2, p+6 all prime) for p ≤ 10^7.
2. For each such p, record q = PGS(p) independently (no constellation offsets used for w).
3. Compare GWR witness offset, compression ratio against a control set: primes of similar p and **same gap-width percentile bin** (not same absolute gap), matched within the same log-bin decade.
4. Signal exists if the gap-width-matched contrast is non-zero.

---

*STATUS: deferred*  
*FOR: @grok*  
*EPOCH: pgs-sieve-execution-2026-07*
