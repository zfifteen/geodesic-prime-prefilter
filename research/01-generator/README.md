# Minimal PGS Generator

## Object

The production PGS generator contract:

```text
input known prime p -> output next prime q
```

Production source, tests, and benchmark code remain in their root-level homes:

- `src/python/z_band_prime_predictor/simple_pgs_generator.py`
- `tests/python/predictor/test_simple_pgs_generator.py`
- `benchmarks/python/predictor/minimal_pgs_scale_probe.py`
- `benchmarks/python/predictor/simple_pgs_high_scale_chain_probe.py`

This chapter is the research routing surface for generator evidence. It does
not move production implementation code.

## Invariant Or Rule

Given a known prime `p`, exact divisor-count structure after `p` determines the
next prime `q`. The production generator emits only:

```json
{"p": 89, "q": 97}
```

Diagnostics, certificates, and audit records stay outside the emitted stream.

## Proof Status

`PROOF.md` is the live proof authority for the direct deterministic next-prime
theorem. The generator chapter does not redefine theorem status.

## Measured Evidence

Primary measured surfaces:

- `output/minimal_pgs_scale_probe_1e5_to_1e18/`
- `docs/releases/pgs_inference_generator_v1_1_pgs_only.md`
- `docs/specs/prime-gen/minimal_pgs_generator_logic.md`
- `docs/research/prime_inference_generator/`
- `experiments/rule_x_logic_engine/chamber_reset_decade_ladder_1e8_1e18_a256_b1024/report.md`

`RESULTS.md` records the production evidence surface as `9588 / 9588` exact PGS
outputs with `0` failures on `11..100000`, and `2816 / 2816` exact outputs
with `0` incorrect candidates on the `10^8` through `10^18` decade-window
validation surface.

## Audit Status

Focused validation passed after the chapter map was finalized:

```text
python3 -m pytest tests/python/predictor/test_simple_pgs_generator.py tests/python/predictor/test_gwr_dni_recursive_walk.py
36 passed in 1.02s
```

## Invalidated Rules

Bridge and fallback source labels are not live v1.1 production generator
sources. They remain historical diagnostics only.

## Unresolved State

No unresolved state is attached to the production generator contract in this
chapter. Bounded-compression and cryptology unresolved states are routed to
their own chapters.

## Reproduce

Run the focused generator contract tests:

```text
python3 -m pytest tests/python/predictor/test_simple_pgs_generator.py
```

Run the larger generator/GWR routing validation:

```text
python3 -m pytest tests/python/predictor/test_simple_pgs_generator.py tests/python/predictor/test_gwr_dni_recursive_walk.py
```

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped, non-moving production
chapter in Phase 3 of the repository reorganization.
