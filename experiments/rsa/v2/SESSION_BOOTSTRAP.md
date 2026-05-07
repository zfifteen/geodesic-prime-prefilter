# RSA v2 Session Bootstrap

This file exists so a future Codex session can start in `experiments/rsa/v2`
without reverse-engineering the previous work.

## Headline State

The current v2 experiment is honest but unresolved.

The official runner derives reciprocal PGSPG certificate-pair state from public
moduli. It does not currently solve the 40-bit or 50-bit rungs.

The active grammar research track has a new measured result:

```text
inverse recursive grammar appears as component sharing with ordered-word
exclusion.
```

Solved rows reuse recursive pieces from the deterministic expanded surface, but
avoid that surface's ordered lag-2 + lag-3 reduced words.

## Current Commands

From `experiments/rsa/v2`:

```bash
python3 build_ladder_fixtures.py
python3 run_experiment.py
python3 audit_experiment.py
pytest -q ../../../tests/python/test_rsa_v2_scripts.py
```

Expected test result:

```text
43 passed
```

From the repository root, also preserve:

```bash
PYTHONPATH=src/python pytest -q tests/python/predictor/test_scale_pgs_chain_modulus_link.py
```

Expected result:

```text
5 passed
```

## Current Inference Result

The current `output/inference_rows.jsonl` state is:

```text
rsa_v2_40bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
rsa_v2_50bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
```

The correct interpretation is:

```text
PGSPG certificate state is being derived, but no reviewed public invariant has
selected a factor pair.
```

## Current Audit Result

The current `output/audit_results.csv` state is:

```text
rsa_v2_40bit_static_001 integrity_pass inference_audit_fail
rsa_v2_50bit_static_001 integrity_pass inference_audit_fail
```

The audit factor file certifies the public moduli, but inference does not match
the audit factors because inference is unresolved.

## Active Algorithm

The active algorithm is:

```text
public N
-> isqrt(N) as orientation
-> previous public endpoint before isqrt(N)
-> lower PGSPG chamber-reset certificate
-> y = floor(N / lower.reset_endpoint)
-> previous public endpoint before y
-> upper PGSPG chamber-reset certificate
-> strict reciprocal certificate closure
-> resolved only if certificates mutually close
```

The current strict closure candidate requires:

```text
floor(N / lower.reset_endpoint) == upper.reset_endpoint
floor(N / upper.reset_endpoint) == lower.reset_endpoint
lower.reset_signature == upper.reset_signature
```

If those conditions fail, inference returns unresolved.

## Current 40-Bit Certificate Snapshot

```text
lower_reset_endpoint = 1048573
transported_upper_endpoint = 1048574
upper_reset_endpoint = 1048583
transported_lower_endpoint = 1048564
closure_status = unresolved_by_certificate_pair_not_closed
```

## Current 50-Bit Certificate Snapshot

```text
lower_reset_endpoint = 32053649
transported_upper_endpoint = 32053634
upper_reset_endpoint = null
transported_lower_endpoint = null
closure_status = unresolved_by_certificate_pair_not_closed
```

## Invalidated Rules

Do not revive:

- fixed additive chambers around `isqrt(N)`;
- radius-limited candidate generation;
- endpoint-walk budgets as solver coverage;
- raw reset-deadline margin equality;
- stationary recursive rounds that revisit the same endpoint;
- product closure as the PGS contraction rule;
- `N % x`, `gcd`, factor APIs, or primality APIs inside inference;
- audit factors or answer-bearing PGS-state fixtures inside inference;
- per-bit or per-rung resolver branches.

The previous 40-bit resolution was withdrawn because it depended on a
close-factor shape. Do not treat that result as a live solve.

## Current Grammar Evidence

Read these before extending the grammar track:

```text
GRAMMAR_EVIDENCE_STATUS.md
GRAMMAR_PATTERN_SCAN.md
output/grammar_inverse_word_exclusion/summary.json
```

Current inverse-word measurement:

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

Current grammar interpretation:

```text
The inverse relation is not a simple low/high opposition. It is component
sharing with ordered-word exclusion.
```

Status separation:

```text
hypothesis: public grammar excludes incompatible ordered recursive words
measured result: solved rows share pieces but avoid expanded lag-2 + lag-3 words
proof status: not proved
resolver status: not integrated
unresolved state: derive and falsify a public PGS exclusion rule
```

Next grammar task:

```text
Use combined lag-2 + lag-3 reduced words as exclusion-family labels, then test
fresh solved rows for component sharing without ordered-word collision.
```

## Live Files

Read these before changing the algorithm:

- `AGENTS.md`;
- `README.md`;
- `ALGORITHM.md`;
- `ARITHMETIC.md`;
- `METRICS.md`;
- `PGS_CERTIFICATE.md`;
- `run_experiment.py`;
- `tests/python/test_rsa_v2_scripts.py` from the repository root.

The repository-level continuity bootstrap is:

```text
docs/research/codex_continuity/START_HERE.md
```

## Grok Requirement For Rule Changes

Before major RSA/PGS rule changes, use Grok through the `second-opinion` skill.

Give Grok:

- the exact proposed rule;
- relevant `run_experiment.py` excerpts;
- current `survivor_rows.jsonl` rows;
- known invalidated rules;
- the current unresolved outputs;
- the specific question the new rule must answer.

Ask Grok to look for:

- hidden classical gates;
- product-closure leakage;
- audit leakage;
- non-invariant comparisons;
- false resolution risk;
- falsification tests.

Record substantial sessions in:

```text
grok_sessions/YYYY-MM-DD-topic.md
```

## Next Valid Work

The next valid mathematical task is to derive a stronger transported
certificate invariant from public PGSPG fields.

Until that invariant is written down, reviewed, implemented, and tested, the
correct inference status is unresolved.

For the grammar track, the next valid task is to test the inverse word
exclusion family on fresh solved rows. Do not translate the measured grammar
pattern into a resolver until a PGS-native rule has been derived, falsified, and
reviewed.
