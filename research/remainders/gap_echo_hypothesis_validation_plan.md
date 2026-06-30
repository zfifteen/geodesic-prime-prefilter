# Plan: Validate or Falsify "Gap Echo Memory Selects the Winner" Hypothesis

## Hypothesis (from Core Insight)
Gaps whose final remainder vectors (using reduced state vec[:6] for mod<=210) contain exact repeats of earlier vectors in that gap ("has echo" in late positions) will have a higher rate at which the next prime arrives immediately after the GWR leftmost minimum-d(n) position, compared to gaps without such repeats.

This is due to "accumulating modular memory" from path-dependent repeats that makes the GWR position the terminal one more often.

## Precise Definitions
- **Remainder state**: tuple(remainder_vector[:6])  -- residues mod 2,3,5,7,30,210 (projection to avoid n-uniqueness in mod 2310 for small n)
- **Late positions**: the last min(3, g) interior composites in the gap (absolute last few, works for small g)
- **Has echo (late repeat)**: late_repeat_count > 0 , where late_repeat_count is the number of late positions whose state matches any earlier state in the gap (computed via _count_prior_repeats on states)
- **GWR_last**: the record where is_gwr_winner (or is_current_min_d) is True has distance_to_next_prime == 1 (or termination_distance ==1). I.e., the GWR winner is the last interior before q.

## Data Sets
1. Tiny validation set: existing enriched/tiny_enriched.jsonl (108 gaps, max g=17 <210)
2. Scaled set: run collector to p~1e6 or higher to get more gaps and check for any g >=210 (where repeats become possible in principle)
3. Synthetic set: artificially constructed per-gap sequences of states with controlled has_echo and GWR_last flags to test the analysis code's ability to recover differential rates.

## Metrics and Comparison
- Compute fraction of gaps with GWR_last in the "has_echo" class vs "no_echo" class.
- Baseline: overall GWR_last rate in the data.
- For synthetic: inject bias (e.g. 60% GWR_last in has_echo gaps, 30% in no_echo), run the classifier, verify recovered rates close to injected.
- If has_echo class has 0 samples, report as "condition not met in data; hypothesis not testable positively in this regime".

## Execution Steps
1. Use existing functions compute_intra_gap_repeat_stats and compute_per_gap_late_repeat_feature on the tiny set. Record rates.
2. Run collector to at least 1e5-1e6, enrich the output if needed (or use direct since recent collector emits the fields), run the stats, check max g and if any has_echo.
3. Generate synthetic: 1000 'gaps'.
   - For 500 has_echo: generate sequences with at least one repeat in last 3, set GWR_last=True with prob 0.6
   - For 500 no: no late repeat, GWR_last=True with prob 0.3
   - 'records' with minimal fields p, k, g, remainder_vector (set states), is_gwr_winner, distance_to_next_prime (set accordingly for last).
   - Run stats on synthetic, compare observed rates to injected.
4. Document findings: support, falsify, or inconclusive.
5. Append to CORRELATION_REPORT.md under the hypothesis section or new.
6. Add any necessary code/tests if functions need extension (keep pure).
7. Run targeted tests.
8. Commit only under research/remainders/

## Expected Outcomes and Falsification Criteria
- If in real data with has_echo samples, the GWR_last rate in has_echo is NOT higher (or lower) than in no_echo by significant margin: falsifies or weakens the hypothesis.
- If rates similar: no support for "selects".
- Synthetic serves as positive control for the measurement code.
- Note regime limitation: repeats impossible for g < 210 with current state definition.

## Success Criteria for Plan
- Clear numbers for tiny and synthetic.
- If scaled data run, report if any echoes found.
- Report states support/falsify/inconclusive with PGS framing.
- Code changes minimal, tests pass.

## Notes
- Stick to PGS objects: ordered gap state, remainder vectors as coordinates, GWR rule.
- No classical methods for inference.
- All measured, not proved.

Date: 2026-06-30
