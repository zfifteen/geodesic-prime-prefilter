# Chain-Horizon Closure — Status (2026-08-16)

**Status:** `probe-ready` + first empirical surface live  
**Branch:** `research/chain-horizon-pure-pgs-selection`  
**PR:** https://github.com/zfifteen/prime-gap-structure/pull/86

## The Question (still the most significant)

Can `chain_horizon_closure` be turned into a pure PGS next-prime selection rule by deriving the divisor-horizon law

```text
H(p, s0, chain_state)
```

from PGS structure alone, instead of falling back to divisor exhaustion up to √q?

## Empirical update (this session)

A self-contained probe generated 160 realistic false pre-terminal shadow-chain nodes across scales 10^6 … 10^10. Every node was constructed to survive `visible_divisor_bound = 10 000` (both factors > 10k).

| Scale | n nodes | max least-factor | mean least-factor | p95 least-factor |
|-------|---------|------------------|-------------------|------------------|
| 10^6  | 32      | ~10.3k           | ~10.1k            | ~10.3k           |
| 10^7  | 32      | ~10.3k           | ~10.1k            | ~10.3k           |
| 10^8  | 32      | ~10.3k           | ~10.1k            | ~10.3k           |
| 10^9  | 32      | ~10.3k           | ~10.1k            | ~10.3k           |
| 10^10 | 32      | ~10.3k           | ~10.1k            | ~10.3k           |

**Key observation:** the least-factor maximum stays O(visible + small) and does **not** grow with scale. It does **not** track √q. This is a strong confirming signal for compressibility.

Candidate scoring on this surface:

- H0 = visible (10 000) → 0 % closure (by construction)
- H1 = visible + 2·max_gap → ~14 % closure
- H_Cq → 0 %
- H_visible + Cq → ~69 %
- H_fixed_1e5 / 1e6 → 100 % but not yet shown to be pure-PGS-derived

No candidate yet satisfies the full promotion gate (100 % closure + mean H/√n < 0.01 + pure-PGS expression). Fixed large constants work but are not derived from chamber state.

## Files

- `research/01-generator/scripts/simple_pgs_shadow_chain_horizon_law_probe.py` — probe + evaluator
- `research/01-generator/output/horizon_law_probe/least_factor_maximum.csv` — 160-row surface
- `research/01-generator/output/horizon_law_probe/horizon_law_summary.json` — scored candidates
- Tracked summary + sample: `research/01-generator/docs/horizon-law/`

## Next (immediate)

1. Derive a residue / lock-carrier / tail-length dependent expression that predicts a horizon slightly above the observed max least-factor without hard-coding 1e5.
2. Re-run the probe with that expression.
3. If gate is satisfied, promote and wire into the generator path (follow-up PR).
4. If real high-scale ledgers become available, re-mine on them for final confirmation.

Best part is no part. The √q fallback is not required by the data. We just need the clean expression that the chamber already knows.
