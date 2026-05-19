# Paragraph 09 Evidence: Square-Fiber Selector

## Public Claim To Support

The latest useful signal is a public square-fiber selector: the visible
remainder of the product modulo `180` groups the candidate lanes into three
public fibers, and a public gate co-landing test selects exactly the survivor
lanes on the current matrix.

## Supporting Evidence

- `research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/output/codex_round20_public_square_fiber_probe/summary.json`
  records:
  - `same_phase_lane_count = 12`
  - `public_square_fiber_count = 3`
  - each fiber contains `4` lanes
  - two survivor lanes occupy public fibers `97` and `157`
  - `N mod 180` alone does not select the survivor lane inside a fiber
  - the allowed directed public tuple selects exactly the survivor in each
    survivor-bearing fiber on the current matrix
- `research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/output/codex_round21_public_square_fiber_root_selector/summary.json`
  records:
  - `selector_matches_survivors_all_fibers = true`
  - fiber `37` selects none
  - fiber `97` selects `49|13`
  - fiber `157` selects `43|79`
  - `factor_found = false`
  - `theorem_status = hypothesis_not_proved`
- Relevant commits:
  - `ad754741` - Add PEDK round 20 public square fiber probe
  - `ea29166d` - Add PEDK round 21 square fiber root selector

## Status Boundary

- Measured: public fiber grouping and selector match current survivor lanes.
- Not proved: universal selector theorem.
- Not a factor result: the summary explicitly records `factor_found = false`.

## Infographic Concept

Twelve lanes collapse into three boxes labeled by public `N mod 180` values:
`37`, `97`, and `157`. Each box contains four root lanes. A second public gate
marks none in `37`, `49|13` in `97`, and `43|79` in `157`.

