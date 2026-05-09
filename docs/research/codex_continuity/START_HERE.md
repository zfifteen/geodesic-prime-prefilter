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

PGS-native forbidden-transition follow-up:

```text
benchmarks/python/predictor/state_budget_forbidden_transition_test.py
output/state_budget_forbidden_transition_summary.json
output/state_budget_forbidden_transition_folds.csv
output/state_budget_forbidden_transition_catalog_2048/state_budget_forbidden_transition_summary.json
```

The "cannot be" framing tested whether square-room side forbids exact next
reduced states inside matched current PGS chamber facts. On the current
256-row retained surface, the broad base cell returns `does_not`: `703`
eligible held-out rows, `227` violations, violation rate `0.322902`.
The exact-tail cell has zero violations but only `4` eligible rows, so it is
`unresolved`.

A larger deterministic retained surface was generated with `2048` consecutive
catalog rows at each power `10^12..10^18`. It contains `11470` current `d=4`
transitions. That larger surface rejects exact next-state exclusion in every
mode:

```text
base:             10030 eligible, 1698 violations, violation rate 0.169292
mod30:             5665 eligible,  813 violations, violation rate 0.143513
exact_tail:        2690 eligible,  746 violations, violation rate 0.277323
mod30_exact_tail:  1331 eligible,  286 violations, violation rate 0.214876
```

This invalidates the square-room-side-as-forbidden-transition rule on the
retained high-window surfaces. The original memory-like signal is not a hard
next-state exclusion law.

Expanded pairwise readout on the same `2048` surface:

```text
output/state_budget_forbidden_transition_catalog_2048/state_budget_pairwise_ruler_summary.json
output/state_budget_forbidden_transition_catalog_2048/state_budget_residue_matched_pair_summary.json
```

The larger pairwise surface resolves the earlier square-over-tail ambiguity
against the independent square-boundary interpretation:

```text
base matched cells:
  square_ruler signed advantage: +1026 over 37116 decisive pairs
  tail_length signed advantage:  +1024 over 37116 decisive pairs
  square-over-tail edge: +2

mod30 matched cells:
  square_ruler signed advantage: +149 over 14305 decisive pairs
  tail_length signed advantage:  +135 over 14305 decisive pairs
  square-over-tail edge: +14, below min_control_margin = 15

mod30 + previous gap:
  square_ruler signed advantage: -19 over 2463 decisive pairs
  tail_length signed advantage:  -30 over 2463 decisive pairs
```

Interpretation at the `2048` surface: the retained high-window signal is real
as a weak ordering effect, but that surface does not isolate the next
prime-square boundary as the independent carrier. The signal tracks endpoint
tail length too closely. The research state after this surface was:

- measured: weak memory-like ordering exists inside matched current PGS cells;
- invalidated: square-room side forbids exact next reduced state;
- invalidated on expanded retained windows: square ruler clearly beats tail
  length as an independent mechanism;
- unresolved: the actual PGS-native carrier of the weak residual ordering.

Long-running `8192` breakthrough:

```text
docs/research/predictor/d4_count_observer_note/index.html
docs/research/predictor/state_budget_long_running_research_goal/index.html
output/state_budget_long_running_catalog_8192/state_budget_long_running_research_report.md
output/state_budget_long_running_catalog_8192/state_budget_divisor_carrier_sweep_summary.json
output/state_budget_long_running_catalog_8192/state_budget_divisor_carrier_sweep_folds.csv
benchmarks/python/predictor/state_budget_divisor_carrier_sweep.py
tests/python/predictor/test_state_budget_divisor_carrier_sweep.py
```

The long-running goal stopped with:

```text
breakthrough: ordering carrier found
```

Strongest supported measured claim:

```text
On the deterministic retained 8192-row-per-power 10^12..10^18 surface, the
current chamber's d4_count is a PGS-native ordering carrier for the next triad
state under the ordering-carrier gate.
```

Exact breakthrough row:

```text
match mode: mod30_prev_gap_exact
measure: d4_count
decisive pairs: 7881
held-out powers above 100 decisive pairs: 7 / 7
positive oriented held-out folds: 6 / 7
oriented signed advantage: 299
endpoint-tail control signed advantage: 230
edge over endpoint-tail control: 69
required edge: 50
verdict: ordering_carrier_found
```

`d4_count` is the number of divisor-count `4` positions inside the current
ordered prime-gap chamber. It is defined from the current PGS divisor-count
field, not from the next chamber label.

State separation:

- measured: `d4_count` is a held-out ordering carrier on the retained
  `8192`-row-per-power `10^12..10^18` surface;
- invalidated: square-room side as a hard next-state exclusion rule;
- invalidated: prime-square boundary clearly beating endpoint tail as the
  independent carrier on expanded retained windows;
- unresolved: symbolic reason why current-chamber `d4_count` carries next-triad
  ordering information;
- unresolved: replication on a disjoint retained high-window construction.

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
