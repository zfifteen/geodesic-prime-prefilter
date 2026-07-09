# Experiment design — falsify Hypothesis U

## Goal

Search for a counterexample to Hypothesis U:

```text
GWR w with z(w) ≥ 4 and unique τ-minimum  ⇒  g = 2
```

One CE falsifies. Zero CEs in a stated regime is measured support only.

## Protocol

### Phase A — full gap enumeration (sieve)

- Build prime list and `τ` table up to `P_MAX_A` (default `5×10^7`).
- For every consecutive prime pair with left prime `p ∈ [11, P_MAX_A)` and nonempty interior:
  - Compute GWR `w`, `τ(w)`, tie count, `z(w)`.
  - **Primary:** if `z ≥ 4` and `ties == 1` and `g > 2` → CE (Hypothesis U falsified).
  - **Control:** if `z ≥ 4` and `g > 2` → bare Super-Signal FP (expected; documents CE family).
  - **Secondary:** track `210 | w` with `g > 2`; track `z ≥ 4` and `τ(w) > 16` with `g > 2`.

### Phase B — extension beyond Phase A (sympy interiors)

- Enumerate consecutive primes with left prime in `[P_MAX_A, P_MAX_B)` (default `P_MAX_B = 1.2×10^8`).
- Same predicates on each gap interior via `divisor_count` (audit only).
- Ensures pressure **beyond** the prior `10^8` partial clean band for unique-min.

### Success / fail for the experiment runner

- Exit code `0` always if the scan completes (science run).
- JSON + stdout always report:
  - `hypothesis_u_counterexamples` list
  - `verdict`: `falsified` | `not_falsified_in_tested_regime`
  - exact regime bounds and gap counts

## Non-interpretation rules

- Do not print “proved” or “validated theorem.”
- Classical primality / divisor count = **audit** only.
- Do not demote GWR pillars based on this run.

## Reproduction

```bash
python3 experiments/hypothesis-u-unique-supersignal-falsification-2026-07/run_hypothesis_u.py
# optional:
python3 experiments/hypothesis-u-unique-supersignal-falsification-2026-07/run_hypothesis_u.py --p-max-a 50000000 --p-max-b 120000000
```
