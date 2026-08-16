# Chain-Horizon Closure — Status (2026-08-16)

**Status:** `probe-ready` (moved from pure unanswered)

**Branch:** `research/chain-horizon-pure-pgs-selection`

## The Question (still the most significant)

Can `chain_horizon_closure` be turned into a pure PGS next-prime selection rule by deriving the divisor-horizon law

```text
H(p, s0, chain_state)
```

from PGS structure alone, instead of falling back to divisor exhaustion up to √q?

## Why this is the bottleneck

High-scale generator surfaces (documented):

- 10¹⁵: 56.63 % of outputs still pass through chain-horizon closure
- 10¹⁸: 58.00 % of outputs still pass through chain-horizon closure

The operational shape is already correct and audit-clean (0 failures). The terminal decision on the shadow-chain is the last non-PGS hinge.

## Empirical position (from prior solution probes)

Multiple independent simulations and pilots already rule out the null that the required horizon tracks √q.

The least-factor maximum of false pre-terminal shadow-chain nodes is far smaller than √q and appears governed by local chamber geometry (visible_divisor_bound, chain gaps, residue state, lock-carrier quantities).

No candidate H has yet been promoted because a full least-factor maximum miner on the real 10¹⁵ / 10¹⁸ probe surfaces has not been executed end-to-end with the promotion gate.

## Immediate next action (this branch)

1. Ship a clean, self-contained probe that logs the least-factor maximum of every false chain node together with the full PGS-visible state vector.
2. Run it against every available high-scale surface that still exists in the repo or can be regenerated.
3. Test the top candidate families:
   - H0 = visible_divisor_bound
   - H1 = visible_divisor_bound + k · max_chain_gap
   - H_Cq = max(64, ceil(0.5 · log(q)²))  (already proved for witness offset)
   - H_wheel / residue-vector forms
4. Promotion gate (harsh):
   - 100 % closure of pre-terminal false nodes on the tested surface
   - same first surviving terminal as current chain_horizon_closure
   - H / √n → 0 with scale
   - H computable from PGS state only (no factorization, no audit labels)

## Files on this branch

- `STATUS.md` (this file)
- `research/01-generator/scripts/simple_pgs_shadow_chain_horizon_law_probe.py` (to be added)
- Continuity notes under `research/00-index/continuity/`

## Ownership

This track owns the conversion of the high-scale bridge. All other residual / RH / unsolved-problem work is downstream of a pure-PGS selection rule.

Best part is no part. Delete the √q fallback.
