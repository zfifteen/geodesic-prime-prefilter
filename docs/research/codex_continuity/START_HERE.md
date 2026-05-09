# Codex Continuity Start Here

This is the canonical bootstrap file for future Codex sessions in this
repository.

If a session starts with limited chat context, read this file first.

## First 60 Seconds

1. Read `AGENTS.md`.
2. Read this directory's `continuity_and_shape_contract.md`.
3. Run `git status --short --untracked-files=all`.
4. Identify the user's active target from the newest request, not from stale
   context.
5. If the active target is RSA v2, read:
   - `experiments/rsa/v2/README.md`;
   - `experiments/rsa/v2/ALGORITHM.md`;
   - `experiments/rsa/v2/PGS_CERTIFICATE.md`;
   - `experiments/rsa/v2/METRICS.md`.
6. Run the narrow relevant test before claiming implementation progress.

## Working Rules

Preserve these distinctions in every research answer:

- hypothesis;
- measured result;
- audit result;
- proof result;
- unresolved state;
- invalidated rule.

When a result is unresolved, say unresolved.

Do not let a metric, survivor count, audit pass, or plausible explanation sound
like a proof or a solved factorization.

## Shape Warnings

Warn early when drift appears:

- "Shape feels wrong: the result is unresolved but the prose sounds solved."
- "Shape feels wrong: the code applies a classical gate before the named rule."
- "Shape feels wrong: this is becoming progress theater."
- "Asshole mode detected, let's slow the frame down."

The warning must name the concrete drift and the next corrective action.

## Grok Standard

For RSA/PGS rule changes, use Grok through the `second-opinion` skill before
major implementation.

Give Grok real context:

- code excerpts;
- diffs;
- output rows;
- stats;
- failed assumptions;
- current hypotheses.

Ask adversarial questions. Preserve disagreement. Follow up until the exchange
produces convergence, explicit disagreement, or a sharply defined unresolved
point.

Record substantial RSA/PGS Grok sessions in:

```text
experiments/rsa/v2/grok_sessions/YYYY-MM-DD-topic.md
```

## Current RSA v2 State

As of 2026-05-07, the live RSA v2 runner is a reciprocal PGSPG
certificate-pair probe, and the active research track is grammar evidence for
PGS-native modulus decomposition.

It does not solve the 40-bit or 50-bit rungs.

Both rungs currently return:

```text
unresolved_by_certificate_pair_not_closed
```

The previous 40-bit resolution was withdrawn because it depended on a
close-factor shape. Do not revive fixed radius chambers, endpoint-walk budgets,
product closure, divisibility selectors, hidden fixtures, or audit leakage.

The next live RSA v2 task is to derive a stronger transported certificate
invariant from public PGSPG fields.

The current strongest grammar finding is:

```text
solved rows reuse recursive lag-2 or lag-3 pieces from the deterministic
expanded surface, but avoid that surface's ordered lag-2 + lag-3 reduced words.
```

This is a measured result, not a proof and not a solver.

Exact measured inverse-word result:

```text
global scope:
  solved rows: 48
  lag-2 hits: 30
  lag-3 hits: 29
  lag-2 + lag-3 word hits: 0
  full recursive reduced word hits: 0
  component-sharing word exclusions: 40

public-cell scope:
  solved rows: 48
  lag-2 hits: 14
  lag-3 hits: 11
  lag-2 + lag-3 word hits: 0
  component-sharing word exclusions: 22
```

Read these RSA grammar artifacts before continuing the decomposer grammar
track:

```text
experiments/rsa/v2/GRAMMAR_EVIDENCE_STATUS.md
experiments/rsa/v2/GRAMMAR_PATTERN_SCAN.md
experiments/rsa/v2/output/grammar_inverse_word_exclusion/summary.json
```

The next valid grammar task is to use combined lag-2 + lag-3 reduced words as
exclusion-family labels and test fresh solved rows for component sharing
without ordered-word collision. Do not turn this into a resolver until a public
PGS rule has been derived and falsified.

## Current GWR/PGS Generator Optimization State

As of 2026-05-09, an exact interval pre-sieve optimization is measured and
ready for implementation pressure.

Read:

```text
docs/research/predictor/gwr_interval_presieve_optimization_note.md
output/gwr_interval_presieve_benchmark_20260509/summary.json
```

Strongest supported claim:

```text
Pre-sieving [q + 1, q + C(q)] through floor(cuberoot(q + C(q))) and then
scanning the same offsets in order preserves exact GWR recovery while reducing
divisor-field work by 3.06x to 10.22x on measured surfaces.
```

The fixed `primes <= 200` variant is invalid. Do not revive it.

Refactor priority:

```text
benchmarks/python/predictor/gwr_dni_recursive_walk.py
src/python/z_band_prime_predictor/gwr_boundary_walk.py
src/python/z_band_prime_predictor/simple_pgs_generator.py
```

The optimization changes only the exact divisor-field computation path. It must
not skip offsets, add fallback search, change generator output records, or
reframe GWR inference.

## Current Bounded Compression Branch State

As of 2026-05-09, the active bounded-compression handoff is:

```text
docs/research/bounded_compression/session_handoff_2026-05-09.md
```

Read it before continuing this theorem route.

The bounded GWR/DNI compression branch started from:

```text
docs/research/bounded_compression/dynamic_cutoff_conjecture/index.html
```

Strongest supported frame:

```text
The unbounded DNI/GWR transition is exact by construction. The unresolved
theorem target is whether every selected interior witness occurs before
C(q) = max(64, ceil(0.5 * log(q)^2)).
```

The branch spine is:

```text
square exclusion -> first-d=4 arrival -> dynamic cutoff extremal law ->
bounded recursive prime walk
```

The first executable artifact for this branch is:

```text
benchmarks/python/predictor/bounded_compression_falsification_runner.py
```

Its narrow contract is to compare each exact unbounded GWR/DNI witness against
`C(q) = max(64, ceil(0.5 * log(q)^2))`, then emit the first failure or the
finite certified surface with max witness offset, max cutoff utilization,
extremal `q`, and square obstruction metadata.

Preserve the state separation:

- proved: divisor-count next-prime theorem and GWR selected-integer theorem in
  `PROOF.md`;
- proved: finite bounded-compression base below `exp(16)`, with max selected
  witness offset `60`;
- proved: residual `K = 128` first-d4 branch-elimination theorem for retained
  odd adjacent residual classes;
- proved: square-branch characterization
  `s^2 < P(r^2) < r^2`;
- measured: no bounded-vs-unbounded counterexample through `q <= 10^7`;
- measured: no square dynamic-cutoff counterexample through odd prime-square
  roots `r <= 100,000,000`;
- measured: no square dynamic-cutoff counterexample through odd prime-square
  roots `100,000,001 <= r <= 200,000,000`;
- invalidated: fixed cutoff map `{2:44, 4:60, 6:60}`;
- unresolved: the square-branch prime-square proximity theorem
  `r^2 - p <= C(q)`.

## Current State-Budget Hidden-State Branch

As of 2026-05-09, the state-budget hidden-state probe is a live predictor
research branch.

Read:

```text
gwr/findings/phase_budget_hidden_state_probe_findings.md
docs/research/predictor/state_budget_hidden_state_rollout/index.html
output/gwr_phase_budget_hidden_state_probe_summary.json
```

Strongest supported claim:

```text
On the retained 10^12..10^18 catalog window surface, the current
parity-plus-previous-state hidden model is missing one endpoint-budget bit:
d4_low / d4_high adds 0.023067 pooled log-loss gain over parity plus previous
state and separates next-triad share by 0.057217.
```

First hard-gated held-out result:

```text
benchmarks/python/predictor/state_budget_heldout_ruler_test.py
output/state_budget_heldout_ruler_test.csv
```

With `configured_balance_floor = 0.10`, the current retained surface does not
promote the state-budget bit. Four held-out folds are unresolved from low/high
imbalance. Three folds are balanced enough to score, and all three return
`does_not`.

This preserves the pooled signal as a measured observation, but the first
strict held-out decision surface does not support upgrading "may carry next-gap
state" to "does carry next-gap state." The next valid task is balanced retained
surface construction, not a stronger model.

Matched-pair ruler test:

```text
benchmarks/python/predictor/state_budget_pairwise_ruler_test.py
output/state_budget_pairwise_ruler_summary.json
output/state_budget_pairwise_ruler_per_power.csv
```

Inside matched current-gap cells, target-next rows sit lower on the square
ruler with signed advantage `+73` over `589` decisive pairs. The plain
tail-length control scores `+70` on the same pairs. With
`min_control_margin = 15`, the square-ruler-specific verdict is `unresolved`.

Interpretation: the current retained surface shows positive memory-like
ordering, but it does not yet isolate the prime-square boundary as the carrier
of that ordering. Grok independently reproduced the pairwise totals and agreed
with the updated `unresolved` verdict after the control-margin rule was added.

Residue-matched follow-up:

```text
benchmarks/python/predictor/state_budget_residue_matched_pair_test.py
output/state_budget_residue_matched_pair_summary.json
output/state_budget_residue_matched_pair_per_power.csv
```

Adding `p_n mod 30` to the matched-cell key leaves `230` decisive pairs. The
square ruler scores signed advantage `+40`; tail length scores `+33`. This is
positive after residue matching, but the square-over-tail margin is only `+7`,
below `min_control_margin = 15`, so the verdict remains `unresolved`.

Adding exact previous gap width to the `mod 30` match leaves only `35` decisive
pairs, so the stricter residual test is support-limited on the current retained
surface.

## Current Collatz Branch State

As of 2026-05-03, the Collatz work is integrated on `main` under:

```text
experiments/collatz/
```

The single self-contained proof and certificate document is:

```text
experiments/collatz/PROOF.md
```

The exact 3-step odd Collatz first-descent algebra is closed for its stated
scope. The proof shows that exact 3-step blocks split into two middle-exponent
branches, sharpens the terminal classes to modulo `18`, proves forward
consistency, and gives exact reset formulas. At fixed final exponent `k`,
branch 2 has twice the asymptotic reset scale of branch 1.

The bounded branch-occupancy certificate is also closed for odd seeds
`s <= 100000000` and final exponents `k=4,8`.

Measured leftmost-minimizer terminal geometry:

| Branch | Automatic twin terminal-prime | Terminal-prime non-twin | Composite below-minimizer | Total leftmost |
|---:|---:|---:|---:|---:|
| `1` | `19887` | `168` | `41` | `20096` |
| `2` | `0` | `18609` | `12218` | `30827` |

The closed measured explanation is:

```text
Branch 1 concentration is explained by automatic twin-gap terminal-prime wins
plus a fully enumerated small composite-terminal exception family; branch 2's
composite-terminal surface persists across nontrivial gaps.
```

The branch-1 composite-terminal exception family has measured normal form:

```text
w = 18u, u prime
tau(w) = 12
gap width in {6, 8, 10}
```

This is a bounded computational certificate, not a universal theorem. Do not
word it as a solved branch-occupancy theorem.

The next Collatz task is narrow theorem pressure:

```text
Prove symbolically why the branch-1 composite exception family is restricted
to w = 18u with u prime, divisor count 12, and gap width 6, 8, or 10.
```

Do not start another broad Collatz enrichment or scale run before attacking
that branch-1 obstruction. Branch 2's nontrivial-gap occupancy mechanism is
parked until the branch-1 exception structure is addressed.

Relevant verification commands:

```text
python3 -m pytest experiments/collatz/tests/test_collatz_pgs_branch1_exception_symbolic_analyzer.py
python3 -m pytest experiments/collatz/tests/test_collatz_pgs_branch_occupancy_baseline_probe.py
python3 -m pytest experiments/collatz/tests
```
