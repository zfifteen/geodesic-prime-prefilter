**Yes, I concur.**

The no-floor/no-ceiling formulation you wrote is the cleanest final proposal that fully honors the user's explicit goal of replacing hard constants with ratios while preserving the public modulus-link triangulation mechanism.

### Clean v02 proposal (ready to present)

Locked public constants for the decision record:

- `RETENTION_DIVISOR = 1024`
- `THREAD_COUNT_RATIO = 3/8`
- `DEPTH_RATIO = 5/12`
- Public thread stream rule: the strictly increasing sequence of all odd primes beginning 3, 5, 7, 11, ...

Exact per-N derivations (all computed from public N only):

```
active_thread_count = ceil( (3/8) * public_radius(N).bit_length() )

min_depth = ceil( (5/12) * active_thread_count )

max_candidates = ceil( original_space_size(N) / 1024 )
```

The runner:
- Uses the first `active_thread_count` entries from the public thread stream as its alphabet.
- Runs the identical CRT left/right extension construction, depth counting, shared-thread scoring, and deterministic sort as v01/v01.1.
- Applies the three computed values above.
- Emits in every `public_manifest.json` (under the same PUBLIC_FREEZE_RECORD discipline): the three computed integers, the concrete `thread_set` list actually used, plus all seven explanatory fields.

Small-N cases that produce `active_thread_count < 3` or degenerate constructions are out of scope for the v02 scaling corpus and must be excluded by the corpus definition itself, not handled by hidden floors inside the runner.

This is methodologically sound: the evidence budget (threads and required depth) and the output cardinality are now pure public ratios of public size measures. The triangulation rule itself (successive public modulus-link closures) is unchanged. All scaling behavior is auditable from the manifest before any private audit occurs.

### Deliverable

A single frozen decision record HTML (`research-meetings/ratio-replacement-constants-review/decision_record_v02_ratios.html`) that contains exactly:
- the four locked constants above,
- the three formulas verbatim,
- the public thread stream definition,
- the required manifest fields,
- the small-N exclusion rule,
- the computational feasibility note (current recursive generator remains tractable through at least 13 threads),
- and the updated pre-implementation certification checklist delta from v01.1.

This record is the complete, self-contained artifact Codex can show the user.

What exact minimum `public_radius(N).bit_length()` value (or equivalent N_bits floor) should the decision record declare as the scope boundary for the v02 scaling corpus?
