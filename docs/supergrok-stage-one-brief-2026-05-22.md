# SuperGrok Brief: PGS Stage-One RSA Search-Space Reduction

Date: 2026-05-22

## Roles

- Project Sponsor: the user.
- Research Lead: Codex.
- Research Assistant: Grok.
- External Research Collaborator: SuperGrok.

## Locked Research Goal

This branch is Stage One of a two-stage RSA-facing research program.

Stage One goal:

```text
public RSA challenge modulus N
-> public PGS structure
-> motif / invariant / grammar pruning
-> substantially smaller, auditable factor-neighborhood search space
```

Stage Two is out of scope for this branch:

```text
reduced search space -> actual factor recovery
```

Do not measure this branch by whether it finds `p` or `q`. Measure it by how much of the public factor-search space it can remove, how deterministically it does so, how auditable the reduction report is, and how honestly it reports unresolved coverage gaps.

## Non-Negotiable Boundary

The reducer must be public-only and deterministic.

Allowed in Stage One:

- public modulus `N`;
- public PGS gap structure derived from `N`;
- GWR / DNI attractor and phase motifs;
- grammar-rule pruning;
- explicit unresolved states;
- downstream audit labels that do not feed pruning.

Forbidden as pruning inputs or pruning logic:

- hidden factors `p` or `q`;
- product closure to identify factors;
- divisibility checks against candidates;
- `gcd`;
- factor APIs;
- primality APIs as inference;
- random search;
- fallback factorization;
- recovery metrics such as recovered / missed / factor rank.

If a public motif or rule does not resolve pruning, the correct Stage-One output is remaining search space or unresolved state, not a Stage-Two workaround.

## Current Evidence Surfaces

Keep these surfaces separate in all analysis and reporting.

### 1. Frozen Toy Evidence Surface

This is the protected validation surface using precomputed public motifs for a fixed 10-case toy corpus.

Current measured state:

- Rule set: 84 public grammar rules, PG-001 through PG-084.
- Average reduction: 65.45%.
- Primary motif family: 8 cases of `o2_d4_a2_d4_odd@mid`.
- Primary reduction: 141 / 198 pruned = 71.21%.
- Secondary motif family: 2 cases of `o4_d4_a4_d4_odd@mid`.
- Secondary reduction: 84 / 198 pruned = 42.42%.
- Total pruned instances across corpus: 1296.

Interpretation:

This is the strongest validated evidence that the public PGS grammar lever can remove a large fraction of the factor-neighborhood hypothesis space when the motif is known-good.

### 2. Live Derivation Surface

This is the scaling reality check.

Measured path:

```text
public semiprime N
-> derive_public_motif(N)
-> prune_factor_space(motif)
-> reduction row
```

Current approximate state:

- Mid-scale live derivation has recently been around 45% average reduction.
- Coverage is weaker than the toy surface because larger semiprimes produce exotic / high-a motif families not fully covered by the current rule set.
- This gap is the main engineering signal for Stage One.

Interpretation:

The live derivation surface is the surface that matters for moving toward the Wikipedia RSA challenge moduli. The frozen toy surface shows the lever exists; live derivation shows how much survives once raw public `N` must produce its own motif.

### 3. Synthetic Motif-Mix Surface

Synthetic ladders are instrument and sensitivity checks, not RSA evidence.

Recent reference run:

- Mode: synthetic.
- Levels: 48, 56, 64, 72, 80.
- Samples: 30 deterministic motifs per level.
- Output directory in the local working tree: `output/ladder/synthetic_48_80_samples_30/`.

Headline result:

| Bits | Avg Reduction | Std Dev | Min | Max | Unresolved |
|------|---------------|---------|-----|-----|------------|
| 48 | 71.21% | 0.00% | 71.2% | 71.2% | 0 |
| 56 | 49.75% | 8.87% | 42.4% | 71.2% | 0 |
| 64 | 60.40% | 20.98% | 15.7% | 74.8% | 0 |
| 72 | 71.21% | 0.00% | 71.2% | 71.2% | 0 |
| 80 | 40.55% | 12.03% | 15.7% | 53.5% | 0 |

Interpretation:

This curve is motif-mix sensitivity. It is not a bit-length scaling law. Levels dominated by `o2_d4_a2_d4_odd@mid` sit near 71%; levels with more weakly covered motifs drop.

## Active Probe In Flight

Grok has launched Real-Derivation Probe v1.

Contract:

```text
deterministically constructed public semiprime N
-> derive_public_motif(N)
-> prune_factor_space(motif)
-> reduction report
```

Shape:

- Mode: real.
- Levels: 64, 72, 80.
- Samples: 3 deterministic public semiprimes per level.
- Output directory in the local working tree: `output/ladder/real_semiprime_64_80_samples_3/`.

Completion gate:

- Report resolved count and unresolved count.
- Report average reduction over all cases.
- Report average reduction over resolved cases.
- Report min and max reduction.
- List motif coverage gaps.
- Do not include `p` or `q` in per-case evidence.
- Do not use recovered / missed / factor-rank language.

The fixture may use deterministic public `(p, q)` pairs to construct `N`, but `p` and `q` must be discarded before pruning. They must not influence motif derivation, rule firing, scoring, or reduction.

## SuperGrok's Useful Role

SuperGrok should help pressure-test Stage One, not drift into Stage Two.

Useful contributions:

- Identify whether a reported reduction surface is toy, synthetic, live derivation, or RSA-facing.
- Check whether any hidden factor information contaminates pruning.
- Find motif families that are under-covered in live derivation.
- Propose public-only grammar rules or coverage diagnostics.
- Audit whether summaries preserve the difference between validated reduction, measured scaling, and unresolved gaps.
- Challenge any claim that sounds like factor recovery when the artifact only proves search-space reduction.

Not useful in this branch:

- trying to factor RSA challenge numbers;
- optimizing search inside the reduced space;
- adding fallback factorization;
- using `p`, `q`, `gcd`, divisibility, or product checks as pruning mechanisms.

## Current Research Lead Direction

The next accepted evidence surface should be the completed Real-Derivation Probe v1, reviewed against the Stage-One contract.

Do not update the main scaling snapshot again until that probe is complete and reviewed. If accepted, it can become a v3 evidence update. If it exposes coverage gaps, the next work should target those motifs with public-only grammar mining.

## One-Sentence Alignment

This branch exists to make a public RSA modulus produce a much smaller, auditable, PGS-derived factor-search space; it does not exist to recover the factors in this stage.
