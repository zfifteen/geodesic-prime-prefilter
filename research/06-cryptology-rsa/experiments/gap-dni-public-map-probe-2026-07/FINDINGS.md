# Gap+DNI public map probe FINDINGS

**Date:** 2026-07-18  
**Experiment:** `research/06-cryptology-rsa/experiments/gap-dni-public-map-probe-2026-07/`  
**Hypothesis package:** `research/next-breakthroughs/2026-07-18-gap-dni-public-map.md`  
**Ledger claim:** `gap-dni-public-map-primary-residual-atlas-2026-07-18`

## Verdict (measured only)

**Hypothesis has legs on named fixtures:** residual atlas (Layer 3) discriminates certificate vs joint residual cell without classical inference fields and without using a candidate list as the decision surface.

Status: **measured on named fixtures only**. Residual rank map remains **hypothesis**. Not theorem. Not RSA solve. No verified/validated language (no map-family 10^18).

## What ran

```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  research/06-cryptology-rsa/experiments/gap-dni-public-map-probe-2026-07/run_map_probe.py
```

Inputs:

- Live public resolver on `rsa-v3/fixtures/regression_cases.jsonl` (40-bit + 50-bit)
- Unit public certificate fields for 64-bit true-close pin (residual-cell geometry)
- Historical false endpoint anti-admission check

Outputs under `output/`: `map_layers.jsonl`, `gate_report.json`, `summary.json`, `RESULT.md`.

## Gate results (all PASS)

| Gate | Result |
| --- | --- |
| G1 40-bit certificate class | PASS (`map_class=certificate`) |
| G2 50-bit joint cell C1T2L1 | PASS (`named_residual`, cell C1T2L1, residual `unresolved_by_joint_cell_C1T2L1`) |
| G3 true-close not C1T2L1 | PASS (cell C0T0L0, stack holds) |
| G4 no classical inference fields | PASS |
| G5 Layer 4 not used as inference | PASS (null candidate list) |
| G6 anti-admission false class | PASS |
| G7 residual discrimination 50 vs 64 | PASS (C1T2L1 vs C0T0L0) |

## Interpretation

The map emitter, built only from public resolver diagnostics and residual ranks, behaves as designed on these pins:

- Resolve class for 40-bit is certificate, not a residual cell.
- 50-bit remains honest named residual C1T2L1 with residual vector present.
- True-close geometry lands C0T0L0 and is not mis-tagged C1T2L1.
- Decision layer never needed gcd / `%` / isprime / candidate lists.

That is evidence the **residual-atlas-primary** framing is executable, not only prose. It is **not** evidence that large moduli factor, that residual ranks are a law, or that search-space percentage alone is the product metric.

## Kill conditions not triggered (on this surface)

- True mutual-close did **not** land C1T2L1.
- No resolve required classical gates.
- Candidate-list layer was deliberately null; residual taxonomy still separated classes (so the map is not “only list shrink”).

## Next pressure (if continue)

1. Emit map rows for additional public ladder rungs (64-bit live runner if certificates public).
2. Hold fixed first-tail windows; reject any probe that widens windows to force certificate.
3. Prefer new residual subclass or certificate on **new** public pins over renorming the same two fixtures.
4. Still forbid verified/validated residual-family language without 10^18 map surface.

## Repro

Same command as above. Requires Python with `gmpy2` (repo production path used: Frameworks 3.13).
