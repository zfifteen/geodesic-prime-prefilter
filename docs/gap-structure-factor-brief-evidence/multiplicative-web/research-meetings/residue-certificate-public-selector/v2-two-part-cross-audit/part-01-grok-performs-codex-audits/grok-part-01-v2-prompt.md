# Grok Part One Prompt - V2 Public Selector Experiment

You are the performer for Part One of the V2 two-part cross-audited public selector experiment. Codex will audit your output before any result is considered admissible.

## Write Scope

Write only inside:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/v2-two-part-cross-audit/part-01-grok-performs-codex-audits/
```

Required artifacts:

```text
reciprocal_shadow_v2_public_selector_probe_grok.py
output/summary.json
output/certificate.jsonl
output/runtime_residue_crt_log.jsonl
output/summary.md
self_checklist.md
grok_execution_notes.md
```

Do not edit files outside the Part One folder.

## Controlling Sources

Read these before coding:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/residue_certificate_v2_public_selector_contract.html
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/final-cross-audit-report.md
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-01-grok-performs-codex-audits/codex_audit.md
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/grok_audit.md
```

## Experiment Contract

This experiment tests a public certificate-ranking hypothesis only. It is not numeric factor discovery.

Allowed uses of `p` and `q`:

- benchmark case construction;
- direct-row holdout;
- final audit membership of `p % M` after certificates and structural scores already exist.

Forbidden inside generation or ranking:

- hidden `p`/`q`;
- candidate integer intervals;
- prime streams;
- segmented sieves;
- root walks;
- `gcd(candidate, N)`;
- `N % candidate`;
- divisibility gates;
- product-closure gates;
- random controls;
- any threshold not fixed in the V2 contract.

## Required Surface

Use exactly the same 20 cases as V1:

```python
CASES = [
    (23, 31), (43, 59), (61, 83), (89, 113),
    (101, 137), (131, 167), (173, 211), (229, 277),
    (307, 367), (401, 503), (557, 661), (701, 887),
    (1009, 1231), (1601, 2003), (3001, 4001), (5003, 7001),
    (7500013, 29999989), (6000011, 37499947),
    (4500007, 49999991), (3000017, 74999647),
]
```

Use fixed radius `300`.

## Required V1 Layer

Reproduce the V1 certificate layer exactly:

1. Build public composite rows around `N`.
2. Hold out any row whose factorization contains `p` or `q`.
3. Create true, rotated-offset, and deterministic synthetic-offset surfaces.
4. Select the four highest-degree held-out thread factors, with the prior 3-factor fallback if product exceeds `5_000_000`.
5. For each `a in range(M)`, perform per-`r` conflict-check:

```text
b_r = (-offset * inverse(a mod r)) mod r
```

6. If every selected `r` has exactly one `b_r`, merge by CRT and emit `a`.

## Required V2 Ranking Layer

Apply V2 ranking to the non-empty true certificate:

1. Sort held-out rows by offset ascending.
2. Let `d_min = min(row["divisor_count"])`.
3. Let `g` be the first row in ascending offset order with `divisor_count == d_min`.
4. Let `t_g = g["offset"]`.
5. Left support is the nearest row with `offset < t_g` and `divisor_count <= d_min + 2`, if any.
6. Right support is the nearest row with `offset > t_g` and `divisor_count <= d_min + 2`, if any.
7. For each admissible `a`:

```text
inv_a = inverse(a mod M)
d_primary = (t_g * inv_a) mod M
dev_primary = min(d_primary, M - d_primary)
```

8. For each support row offset `t_s`:

```text
d_s = (t_s * inv_a) mod M
dev_s = min(d_s, M - d_s)
```

9. `support_score = sum(dev_s for each support row)`.
10. Structural key is `(dev_primary, support_score)`.
11. Reporting key may be `(dev_primary, support_score, a)`, but `a` cannot create an accepted structural win.

## Required Classification

Count the number of cases in which true `p % M` is the unique structural winner by `(dev_primary, support_score)`.

- `accepted_measured_result`: 18-20 of 20 structural wins, both controls empty, no forbidden pattern.
- `boundary_measurement`: 14-17 of 20 structural wins, or any top result decided only by final `a` tie-break.
- `invalidated_result`: fewer than 14 structural wins, any forbidden inference pattern, or any comparable non-empty control certificate.
- `unresolved_implementation_failure`: implementation deviates from contract or fails required artifacts/logs.

## Output Requirements

`summary.json` must include:

- per-case N, p, q, p_mod_M;
- selected_r, M;
- true/rotated/synthetic certificate cardinalities;
- GWR witness row and support rows;
- true p structural winner boolean;
- winner `a`;
- number of residues tied on structural key;
- per-case classification;
- aggregate structural win count and final classification.

`certificate.jsonl` must include one row per emitted true certificate residue with:

- case_id;
- surface;
- `a`, `y`, `M`, selected_r;
- `dev_primary`;
- `support_score`;
- structural rank;
- structural tie size;
- final reporting rank;
- `p_mod_M`;
- `is_p_member`;
- `is_structural_winner`.

`runtime_residue_crt_log.jsonl` must include enough data to audit:

- V1 per-r inverse/residue calculations and CRT steps for admitted residues;
- V2 inverse/deviation calculations for every true certificate residue.

`summary.md` must present a compact per-case table and aggregate classification.

`self_checklist.md` must explicitly answer all V2 contract checklist items.

`grok_execution_notes.md` must state the result plainly and separate hypothesis, measured result, audit status, and unresolved next step.

Proceed with the implementation and run. Do not publish an accepted measured claim unless the classification table allows it.
