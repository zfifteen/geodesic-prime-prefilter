# Hand Verification Record (Phase 4)

Date: 2026-06-30

## Command lines used
- Validation run: `python research/remainders/collect_remainder_stats.py --max-p 600 --output-dir research/remainders/output/tiny_val/`
- Python: 3.13 (see RUN_LOG.md in output)
- Machine note: macOS (M1 Max class)

## Small fully-factored gaps (plan examples)

### Gap after 113 (q=127, g=14)
- Interiors: 13
- GWR winner (leftmost min d): n=121 (k=8), d(n)=3 (11^2)
- Verified: remainder vector and is_current_min_d flag present and consistent with direct build_records calls.
- Cross-checked multiple times during impl.

### Gap after 139 (q=149, g=10)
- Interiors: 9
- GWR winner: n=141 , d=4

### Gap after 199 (q=211, g=12)
- Interiors: 11
- GWR winner: n=201 , d=4

All match independent runs of build_records_for_gap and full collector.

## Cross-check regime
- All n in tiny_val < 700 < 10^6.
- d(n) sourced from same divisor_counts_segment used by GWR and production generator.
- No classical primality used to select outputs.

## Repro
Re-running the exact --max-p 600 command on same python produces bit-identical raw_records.jsonl (deterministic walk).

Future larger surfaces will append similar entries.
