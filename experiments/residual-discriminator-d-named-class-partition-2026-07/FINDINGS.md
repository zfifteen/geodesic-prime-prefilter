# Findings: residual discriminator D vs named residual classes

**Date:** 2026-07-13  
**Status labels:** D = **hypothesis**; this run = **measured** on 40/50-bit fixtures only; 50-bit = **unresolved**; no residual-family `10^18`; not verified/validated.

## Objects (do not confuse)

1. **RSA residual discriminator D** (this track): dual-gap carrier floor transport bound in `rsa-v3/gwr_carrier_closure.py`.
2. **historical z≥4⇒g=2 claim residual classes A/B/C/D** (`experiments/gwr-remainder-zero-residual-classes-2026-07`): different domain (prime-gap `z` / ties). Same letter D is **not** the same object.

## Hypothesis under test

Public dual-gap D **partitions** named residual codes on the rsa-v3 golden fixtures:

| D outcome | Required named residual class |
| --- | --- |
| fails | `unresolved_by_reciprocal_carrier_misalignment` |
| holds + no public close | a **different** taxonomy code (pin: first-tail) |
| holds + public close | named endpoint class from public chain only |

## Measured regime

`research/06-cryptology-rsa/experiments/live-solver/rsa-v3/fixtures/regression_cases.jsonl` only:

- `rsa_v2_40bit_static_001` (40-bit)
- `rsa_v2_50bit_static_001` (50-bit)

Command:

```bash
python3 research/06-cryptology-rsa/experiments/live-solver/rsa-v3/run_resolver.py \
  --cases research/06-cryptology-rsa/experiments/live-solver/rsa-v3/fixtures/regression_cases.jsonl \
  --output-dir experiments/residual-discriminator-d-named-class-partition-2026-07/output/resolver_run
```

## Results

| case | D | decision residual / close | endpoint emit |
| --- | --- | --- | --- |
| 40-bit | (close path) | `endpoint_class_by_reciprocal_deadline_signature_correction` | yes |
| 50-bit | **holds** `delta=30;boundD=45;g_lo=24;g_up=14` | `unresolved_by_first_tail_misalignment` | no |

50-bit joint ledger (same residual row):

| component | holds |
| --- | --- |
| dual-gap D | true |
| first-tail | false (`delta=-22`) **decision** |
| lock dominance | false (`lock=6;gap=24`) diagnostic |
| profile counts | false on this run (diagnostic; decision already first-tail) |

**Verdict on this regime:** `PARTITION_HOLDS` (not falsified). D is **not** the residual decision on the 50-bit pin; residual honestly migrates to first-tail.

## What this does *not* show

- D is not a theorem or a residual law.
- Constants `1.2` and `20` remain free parameters (hypothesis / possible overfit).
- historical z≥4⇒g=2 claim class A/B/C/D map is untouched.
- No RSA-scale solve; no verified/validated language.

## Next pressure (from Heavy synthesis)

1. **Do not** retune boundD to “fix” 50-bit.
2. Pressure **first-tail reciprocal geometry** and **lock dominance** as the live obstruction class, without widening windows to admit false classes.
3. Keep anti-admission of historical false class `(32047651, 32059633)`.
4. Expand fixture bit ladder only with the same residual honesty rules.

Artifacts: `output/resolver_run/`, `output/partition_report.json`.
