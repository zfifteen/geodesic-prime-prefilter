# GWR And DNI

## Object

Gap Winner Rule (GWR), Divisor Normalization Identity (DNI),
divisor-count structure, chamber mechanics, and recursive next-prime walk
surfaces.

Primary homes remain:

- `LEFTMOST_MINIMUM_DIVISOR_RULE.md`
- `DIVISOR_NORMALIZATION_IDENTITY.md`
- `RECURSIVE_PRIME_WALK.md`
- `gwr/`
- `output/gwr_proof/`
- `output/gwr_dni_recursive_gap_scaling_2_to_18/`
- `docs/research/predictor/`

## Invariant Or Rule

GWR selects the leftmost interior integer with minimum divisor count in a
prime-gap interior. DNI supplies the fixed score:

```text
Z(n) = n^(1 - d(n)/2)
```

Every prime has `Z = 1`, and composites fall below that value.

## Proof Status

`PROOF.md` proves the prime-gap maximizer theorem under its stated hypotheses.
The finite audit surfaces certify implementations and measured regimes; they
do not bound the universal theorem.

## Measured Evidence

Primary measured surfaces:

- `output/gwr_proof/`
- `output/gwr_dni_recursive_gap_scaling_2_to_18/`
- `docs/research/predictor/gwr_dni_exact_recursive_prime_walk_note.md`
- `docs/research/predictor/gwr_interval_presieve_rollout/index.html`

The recursive scaling summary records exact hit rate `1.0`, `0` skipped gaps,
and sampled powers `10^2` through `10^18`.

## Audit Status

Focused validation passed after the chapter map was finalized:

```text
python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py tests/python/predictor/test_gwr_dni_recursive_walk.py
36 passed in 1.02s
```

## Invalidated Rules

No GWR or DNI theorem was invalidated by this reorganization. Bounded cutoff
invalidations are routed to `research/04-bounded-compression/`.

## Unresolved State

No unresolved theorem state is introduced here. Open bounded-compression,
state-budget, and cryptology questions remain in their own chapters.

## Reproduce

Run the recursive walk validation:

```text
python3 -m pytest tests/python/predictor/test_gwr_dni_recursive_walk.py
```

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped GWR/DNI chapter in
Phase 3 of the repository reorganization.
