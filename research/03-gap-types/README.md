# Gap Types

## Object

Gap-type grammar, public framing, visual sequence surfaces, and reduced
finite-state model evidence.

Primary homes:

- `PRIME_GAP_GENERATIVE_MODEL.md`
- `docs/research/prime_gap_grammar_infographics/`
- `output/gwr_dni_gap_type_catalog_summary.json`
- `output/gwr_dni_gap_type_engine_v1_summary.json`
- `output/gwr_dni_gap_type_sequence_probe_summary.json`
- `output/gwr_dni_gap_type_generative_probe_summary.json`
- `benchmarks/python/predictor/gwr_dni_gap_type_*.py`

## Invariant Or Rule

The chapter studies reduced gap-type surfaces derived from GWR/DNI-selected
state. The central measured object is the persistent `14`-state reduced
gap-type core and its Semiprime Wheel Attractor.

## Proof Status

This chapter records a measured model surface, not a theorem about the full raw
prime-gap sequence.

## Measured Evidence

`output/gwr_dni_gap_type_engine_v1_summary.json` records:

- surface: persistent `14`-state reduced gap-type surface;
- local fidelity pooled-window concentration L1 `0.0116`;
- balanced profile pooled-window concentration L1 `0.0150`;
- long-horizon full-walk three-step concentration `0.6278`.

## Audit Status

Focused validation passed after the chapter map was finalized:

```text
python3 -m pytest tests/python/predictor/test_gwr_dni_gap_type_catalog.py tests/python/predictor/test_gwr_dni_gap_type_sequence_probe.py tests/python/predictor/test_gwr_dni_gap_type_engine_synthesis.py
9 passed in 3.75s
```

## Invalidated Rules

No deterministic full-sequence controller is claimed. The current boundary is
that no single deterministic controller on the present surface simultaneously
reaches pooled-window concentration L1 below `0.015` and full-walk three-step
concentration above `0.62`.

## Unresolved State

The model frontier remains a measured reduced-surface controller problem, not a
proved generative law for all prime gaps.

## Reproduce

Run the focused gap-type validation:

```text
python3 -m pytest tests/python/predictor/test_gwr_dni_gap_type_catalog.py tests/python/predictor/test_gwr_dni_gap_type_sequence_probe.py tests/python/predictor/test_gwr_dni_gap_type_engine_synthesis.py
```

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped gap-type chapter in
Phase 3 of the repository reorganization.
