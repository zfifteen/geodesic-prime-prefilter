# Codex Execution Notes - Part Two V2 Public Selector Probe

## Hypothesis Under Test

The V2 ranking hypothesis says that the public GWR/deviation score over the V1 48-residue certificate should make true `p % M` the unique structural winner on at least 18 of 20 cases, with controls remaining empty.

## Measured Result

- Cases executed: 20.
- True certificate cardinality: 48 for every case.
- Rotated control certificate cardinality: 0 for every case.
- Deterministic synthetic control certificate cardinality: 0 for every case.
- Structural wins by true `p % M`: 0 of 20.
- Aggregate classification: `invalidated_result`.

## Implementation Status

The implementation uses a separate Codex source layout and does not copy Grok's implementation structure. It uses deterministic public web construction, V1 residue certificate generation, the frozen GWR witness extraction, and the V2 deviation score exactly as specified.

## Audit Status

The run is ready for Grok audit. The source compiles, required raw outputs exist, and the checklist is complete.

## Invalidated State

The V2 ranking rule is invalidated on the frozen first surface if Grok accepts the implementation audit. The failure is not a control failure: controls are empty. The failure is that the structural key never uniquely selects true `p % M`.

## Next Research Move

After Grok audit, compare both lanes in `final-v2-cross-audit-report.md`. If Grok agrees the implementation is admissible, the final result should report an audited `invalidated_result` for this V2 selector.
