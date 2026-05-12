# Bounded Compression Session Handoff, 2026-05-09

## Strongest Supported Claim

The bounded dynamic cutoff theorem is reduced to one unresolved square-branch
obligation.

The proved and recorded pieces are:

- finite base: for every consecutive prime pair `p < q` with
  `q < ceil(exp(16)) = 8,886,111`, the selected witness satisfies
  `w - p <= 60`, hence `w - p <= 64`;
- residual `K = 128` first-d4 branch-elimination theorem for the retained odd
  adjacent residual classes;
- square-branch characterization: for prime root `r`, previous prime root
  `s`, and greatest prime `P(r^2) < r^2`, the square `r^2` is the selected
  prime-square witness for its containing gap exactly when

  ```text
  s^2 < P(r^2) < r^2.
  ```

This gives only the band bound

```text
r^2 - P(r^2) < r^2 - s^2 = (r - s)(r + s).
```

It does not prove the requested logarithmic-square cutoff.

## Unresolved State

The remaining theorem is:

```text
For every selected square branch, r^2 - p <= C(q),
where C(q) = max(64, ceil(0.5 * log(q)^2)).
```

Because `r^2 < q`, it is enough to prove the stronger statement

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

This prime-square proximity theorem is not proved by the Interior Maximizer
Theorem, the first-d4 theorem, finite square-branch surfaces, or residue-only
local exclusions.

## Measured Results

The direct square-prime search is stronger than selected-square-only evidence,
because it checks every odd prime square in the stated root range.

Retained surfaces:

| Surface | Prime-square roots tested | First counterexample | Max utilization | Extremal root |
|---|---:|---|---:|---:|
| `3 <= r <= 100,000,000` | `5,761,454` | `none` | `0.8120300751879699` | `82,357,433` |
| `100,000,001 <= r <= 200,000,000` | `5,317,482` | `none` | `0.6784140969162996` | `102,017,779` |

Latest segment artifact:

```text
research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_1e8_2e8/square_branch_dynamic_cutoff_search_summary.json
research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_1e8_2e8/square_branch_dynamic_cutoff_search_frontier.csv
```

The latest segment tested roots from `100,000,007` through `199,999,991`.
The extremal row was:

```text
r = 102,017,779
r^2 = 10,407,627,232,092,841
p = 10,407,627,232,092,379
r^2 - p = 462
C(p) = 681
utilization = 0.6784140969162996
```

## Invalidated Or Insufficient Routes

Do not revive these as proof:

- fixed cutoff map `{2:44, 4:60, 6:60}`;
- literal d=4 fallback;
- finite utilization below `1`;
- Cramer-style density language as theorem;
- residue-only coverage of fixed offsets;
- Interior Maximizer Theorem alone;
- first-d4 arrival alone, because divisor count `4` cannot undercut a prime
  square.

## Grok / Second-Opinion State

Grok converged on the same boundary:

- current PGS artifacts do not prove the square branch;
- no unconditional known general prime-gap theorem gives the needed
  logarithmic-square predecessor bound;
- residue-cover constructions do not provide a credible refutation route at
  the moving `log^2` scale;
- the next valid theorem step must prove the prime-square proximity statement
  or produce a genuine counterexample.

## Reproduce The Current Evidence

Run the square-branch unit tests:

```text
pytest -q research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py
```

Re-run the latest finite segment:

```text
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 100000001 \
  --max-prime 200000000 \
  --output-dir research/02-gwr-dni/output/gwr_proof/square_branch_dynamic_cutoff_search_1e8_2e8
```

Expected summary:

```text
primes=5317482
first_counterexample=none
max_utilization=0.6784140969162996
max_p=102017779
```

## Resume Here

Start from `PROOF.md` and
`research/04-bounded-compression/docs/square_branch_blocker_acceptance.md`.

The next session should not re-litigate the finite base or residual `K=128`
lemma. The live task is only:

```text
prove or falsify the prime-square proximity theorem.
```

The cleanest mathematical object is the backward prime distance before prime
squares:

```text
D(r) = r^2 - P(r^2).
```

The theorem target is:

```text
D(r) <= max(64, ceil(0.5 * log(r^2)^2))
```

on the selected-square branch, with selected-square condition

```text
s^2 < P(r^2) < r^2.
```

## Completion Audit

Objective:

```text
Extract the first-d=4 window lemma at K=128 as a formal theorem.
Prove the finite base q < exp(16): selected-witness offset <= 64.
Prove the square-branch selected-prime-square offset bound <= C(q).
```

Checklist:

| Requirement | Evidence | Status |
|---|---|---|
| first-d4 window lemma at `K = 128` | `PROOF.md`, section `Residual K=128 First-d4 Branch-Elimination Lemma` | complete only in the supported residual branch-elimination scope |
| finite base `q < exp(16)` selected witness offset `<= 64` | `PROOF.md`, section `Finite Bounded-Compression Base`, maximum offset `60` across `542,081` nonempty interiors | complete |
| square-branch selected-prime-square offset `<= C(q)` | `PROOF.md`, section `Square-Branch Reduction`, and this handoff | incomplete |

The goal must remain active because the square-branch universal inequality is
not proved. The current artifacts prove the square-branch characterization and
record finite evidence, but they do not prove

```text
r^2 - p <= C(q).
```
