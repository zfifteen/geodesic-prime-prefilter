# Round 3 - Codex Methodology Check

Before I write the HTML, I found one methodological conflict that should be resolved explicitly rather than silently edited.

The meeting record contains both:

```text
Success condition: at least 14 of the 20 cases have the true p % M as the unique structural winner.
```

and:

```text
Falsification / boundary condition: 3 or more cases in which true p % M is absent from the structural top or wins only by the final a tie-break.
```

Those two thresholds conflict. If 3 or more failures falsify the rule, then accepted success requires at least 18 of 20 successes, not 14 of 20.

My proposed repair:

- `accepted_measured_result`: at least 18 of 20 cases have true `p % M` as the unique winner by the structural keys `(dev_primary, support_score)`, with both controls remaining empty.
- `boundary_measurement`: 14 to 17 of 20 cases have true `p % M` as unique structural winner, or any case is decided only by the final `a` reporting tie-break.
- `invalidated_result`: fewer than 14 of 20 structural wins, or any forbidden inference pattern, or any control produces a non-empty certificate comparable to the true surface.
- `unresolved_implementation_failure`: implementation does not execute the frozen contract cleanly.

This preserves the original "14 of 20 is interesting" signal but stops it from being published as accepted evidence under a stricter falsification rule.

Do you confirm this threshold repair, or do you prefer a different exact classification table? Answer with one table only; no new selector machinery.
