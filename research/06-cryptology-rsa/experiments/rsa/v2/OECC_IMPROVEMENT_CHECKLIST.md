    # OECC Improvement Checklist

This checklist tracks improvements after `OECC_LINEAR_V1`.

Use strikethrough for completed items:

```text
- [x] ~~completed item~~
```

## Efficiency And Computational Cost

- [x] ~~Cache PGSPG certificates per case.~~
- [x] ~~Cache `previous_endpoint(value)` per case.~~
- [x] ~~Add counters for `previous_endpoint` calls, certificate lookups, certificate builds, endpoint-chain steps, and closure attempts in a sidecar diagnostic.~~
- [x] ~~Replace repeated exact divisor segment reconstruction in `previous_endpoint()` with a window cache.~~
- [ ] Build a batch endpoint iterator so the lower endpoint chain is generated once per case instead of by repeated backward searches.
- [x] ~~Add a non-persistent measurement mode for baseline cost: endpoint steps, cache hit rate, elapsed time.~~
- [x] ~~Split `endpoint_chain_closure()` into smaller law-preserving units so hot paths can be measured independently.~~
- [x] ~~Add a baseline comparator test so optimizations must emit the same endpoint class as `OECC_LINEAR_V1`.~~

## Scalability

- [x] ~~Move large-coordinate exact interval support into the shared `divisor_counts_segment(...)` backend and remove `SMALL_REGIME_MAX_BITS = 50`.~~
- [ ] Implement `OECC_RECURSIVE_V2` as a side-by-side runner, not a replacement.
- [ ] Compare recursive jumps against `OECC_LINEAR_V1` and reject the recursive version if it skips the first baseline structural closure.
- [ ] Add cycle detection for recursive candidate versions.
- [ ] Add explicit balance-boundary unresolved status for endpoint-chain exhaustion.
- [ ] Test recursive jump policies based on transported corrected coordinates and deadline images.
- [ ] Add exact first-structural-closure regression tests for 48-bit and 50-bit before scaling.

## Law Clarity And Research Hygiene

- [ ] Add `implementation_label = OECC_LINEAR_V1` to summary or sidecar output.
- [ ] Add a 48-bit fixture row for `249882542035169`.
- [ ] Separate structural endpoint class resolved from exact factor pair audit passed in output naming.
- [ ] Rename structural output fields away from `p` and `q` for non-audit-passing endpoint classes, or add explicit `endpoint_class_lower` and `endpoint_class_upper`.
- [ ] Remove or rename stale status `unresolved_by_reset_endpoint_crosses_orientation`.
- [ ] Add a promotion gate document for candidate law revisions: preserve baseline endpoint classes, reduce measured work, no audit/classical inference.

## Candidate Law Experiments

- [ ] Test strict reset closure inside the endpoint-chain traversal as an experiment, not as current law.
- [ ] Test typed-coordinate square-root chamber closure as an experiment, not as current law.
- [ ] Test whether first structural closure is a staging artifact or a meaningful law boundary.
- [ ] Test whether exact-factor audit pass appears at a later structural closure and what public predicate distinguishes it.
