# Square-Tail Infinite-Tail Pause Handoff

## Status

Research paused. The infinite-tail proof is unresolved.

The active objective was:

```text
Find a deterministic infinite-tail proof for the remaining PGS tail structure
using PGS-native reduction, recursion, and elimination rather than
probabilistic or classical heuristic framing.
```

The objective is not complete. No deterministic infinite-tail proof, finite
reduction, or counterexample certificate exists in the repo.

## Strongest Supported Claim

The square-tail problem has been reduced to a deterministic obstruction word.

For a prime root `r`, set

```text
S = r^2
C = max(64, ceil(0.5 * log(S)^2))
M = floor(C / 2).
```

For each row

```text
x_m = r^2 - 2m, 1 <= m <= M,
```

remove every row with a prime factor `<= M`. The remaining rows are the
M-rough defects.

The unresolved theorem is exactly:

```text
Every selected-square root has at least one prime-valued M-rough defect before
the cutoff.
```

Equivalently, no selected-square root can satisfy:

```text
O(r): every M-rough row is composite with least factor > M.
```

## Proof Results Preserved

The recent work produced permanent deterministic reductions. These are proof
results, not empirical observations.

| Result | Artifact |
|---|---|
| M-rough prime factors are row-private inside the parent window. | `square_tail_rough_factor_disjointness_lemma.md` |
| Under `2M < r`, every M-rough composite row has a factorization straddling the root. | `square_tail_near_root_factor_lemma.md` |
| Symmetric rows are exactly `m = 2a^2` with `x_m = (r - 2a)(r + 2a)`. | `square_tail_symmetric_row_lemma.md` |
| Nonsymmetric rows satisfy the quotient equation `d ell = h^2 - 2m`. | `square_tail_nonsymmetric_quotient_lemma.md` |
| Parity forces `h = 2a` and `d = 2b`, giving one centered equation for all M-rough composite rows. | `square_tail_halved_quotient_lemma.md` |
| Nonsymmetric rows have `b >= 1`, hence `d >= 2`, strengthening the distance bound. | `square_tail_halved_quotient_lemma.md` |
| Near-root band counting alone is invalid as a proof route. | `square_tail_band_counting_boundary.md` |

The strongest current row formula is:

```text
x_m = (r - 2a_m)(r + 2a_m + 2b_m)
m = 2a_m^2 - b_m(r - 2a_m).
```

The symmetric rows are exactly:

```text
b_m = 0
m = 2a_m^2.
```

Every nonsymmetric row satisfies:

```text
b_m >= 1
h^2 + 2h >= 2r + 2m
2a^2 + 2a >= r + m.
```

Thus nonsymmetric least factors are excluded from the final roughly
`sqrt(2r)`-wide band below `r`. This is a real constraint, but not a complete
proof.

## Measured Evidence

The standing record remains:

```text
r = 424171123
M = 395
```

Its rough-defect audit records:

| Quantity | Value |
|---|---:|
| M-rough defects | `65` |
| Prime-valued M-rough defects | `3` |
| Composite M-rough defects | `62` |
| First prime-valued offset | `738` |
| Minimum least factor among rough composites | `419` |

A direct assertion check on this record confirmed the centered form and the
strengthened nonsymmetric distance bound on all `62` composite rough rows.

A quick exact scan over prime roots

```text
11 <= r < 1000000
```

found no selection-free obstruction. This is measured evidence only. It is not
a theorem boundary.

The sharpest scanned root in that check was:

```text
r = 183389
M = 147
rough defects = 29
rough prime defects = 1
first rough-prime offset = 92
selected-square condition = true
```

## Invalidated Routes

Do not revive these as proof routes without a new invariant:

- pointwise child projection;
- direct child-prime back-cover into the parent cutoff;
- local CRT contradiction;
- local assigned-carrier obstruction inheritance;
- local first-arrival obstruction inheritance;
- child selected-square inheritance alone;
- selected-square deadline alone;
- cofactor roughness alone;
- centered-remainder language alone;
- near-root band counting alone.

The cofactor roughness observation is true:

```text
if ell is the least factor of x_m = ell * c, then every prime factor of c is
>= ell.
```

But this is not a new invariant by itself. It restates least-factor minimality
plus row-private factor disjointness.

The centered-remainder map is also not a new invariant. It is the
halved-quotient equation written modulo `ell`.

## Current Missing Invariant

The exact missing invariant is:

```text
a global constraint on small-ell nonsymmetric placements that prevents the
M-rough rows from being filled independently by row-private least factors.
```

The current local row equations permit nonsymmetric rows whose least factors
sit outside the final near-root band:

```text
ell <= r - 2 ceil((-1 + sqrt(1 + 2(r + m))) / 2).
```

The proof still needs a global obstruction-collapse mechanism for those
small-`ell` placements.

## Live Candidate Direction

The most recent second-opinion exchange identified one possible next
direction:

```text
actual-root small-representative constraint.
```

A local CRT model can freely assign carrier residues and then find a large CRT
representative. An actual obstruction word is stricter:

- the same concrete prime root `r` satisfies every row congruence;
- `r` is not an arbitrary CRT representative;
- each `ell_m` is the actual least prime factor of `r^2 - 2m`;
- each row satisfies the centered factorization;
- all row factors remain private inside the M-rough obstruction word.

This is a possible finite-reduction or contradiction route, not a proved
lemma.

The next session should test whether the actual-root condition yields an
explicit inequality, small-representative bound, or exact finite reduction.
If it only restates `O(r)`, record that boundary and move on.

## Grok / Second-Opinion State

Recent Grok response IDs and meanings:

| Response ID | Meaning |
|---|---|
| `54bff914-3f49-9de6-967f-42ba79d0f98b` | verified nonsymmetric quotient lemma and least-factor caveat |
| `e1f53b81-e55b-4493-8600-5e9372baaace` | acknowledged square-tail proof frame before halved-quotient review |
| `2ffd77ed-e1f8-99a8-a21e-be472516b364` | verified halved-quotient parity lemma |
| `ee798e36-c22c-95d7-a729-9592daf22153` | rejected centered-remainder map as cosmetic |
| `e12a9f20-fbe3-e36f-1388-1e083fbfb232` | verified strengthened nonsymmetric distance bound |
| `7519afb4-5675-988c-ae2e-85208635fac1` | proposed near-root band-counting route |
| `d1bec1af-7b71-54b5-86aa-6f89f6e3aa67` | agreed band-counting inference is invalid |
| `ee24fc25-a395-10d7-dd6f-e6f4a22e2b36` | identified cofactor roughness as restatement, not strengthening |
| `924c5f1d-c2cd-96cb-a078-d7fac9d856bb` | marked actual-root small-representative constraint as a possible new invariant |

Preserve disagreement. The invalid band-counting suggestion was corrected and
recorded.

## Recent Commits

The current square-tail reduction series ends at:

```text
4b2ee670 Record square tail band counting boundary
e8b7676e Strengthen nonsymmetric distance bound
4f1e4c14 Prove halved quotient lemma
7dcc8122 Prove nonsymmetric quotient lemma
9b4a1860 Prove symmetric rough row lemma
47cd7635 Refine near-root factor split
e750e5bd Prove near-root rough factor lemma
9232b5fa Prove rough factor disjointness lemma
```

## Reproduction Commands

Check the current proof-status audit:

```text
sed -n '1,260p' research/04-bounded-compression/docs/square_tail_infinite_tail_completion_audit.md
```

Inspect the live target:

```text
sed -n '1,340p' research/04-bounded-compression/docs/square_tail_global_obstruction_collapse_target.md
```

Run the rough-defect audit for the standing record:

```text
python3 research/04-bounded-compression/scripts/square_tail_rough_defect_audit.py \
  --root 424171123
```

Run the full bounded-compression test suite before claiming implementation
progress:

```text
python3 -m pytest research/04-bounded-compression/tests
```

For documentation-only changes, `git diff --check` is enough to catch
whitespace and line-ending damage.

## Dirty Worktree Boundary

At pause time, unrelated local artifacts existed outside the square-tail proof
track:

```text
visualizations/apps/ (formerly apps/ at time of pause)
research/03-gap-types/output/composite_gap_field_plot.png
research/03-gap-types/output/gwr_winner_ulam_spiral*.png
research/03-gap-types/scripts/composite_gap_field_plot.py
research/03-gap-types/scripts/gwr_winner_spiral_plot.py
research/06-cryptology-rsa/experiments/rsa/v2/shor_order_entropy_probe.py
research/06-cryptology-rsa/experiments/rsa/v2/output/shor_order_entropy_probe/
research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py
```

Do not revert or stage those files as part of square-tail proof work unless
the user explicitly asks.

## Next Session First Move

Start from the live missing invariant:

```text
small-ell nonsymmetric placements under actual-root least-factor constraints.
```

The clean first question is:

```text
Does the actual-root small-representative condition produce a deterministic
bound or finite reduction beyond local CRT consistency?
```

If yes, write the lemma and send it to Grok before committing it.

If no, record the boundary explicitly and move to a different route:

1. direct exclusion of `O(r)`;
2. global parent-to-child transport law;
3. exact finite reduction;
4. counterexample certificate.
