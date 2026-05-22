# Zero-Excess DNI Migration Plan

The current Divisor Normalization Identity places every prime at the fixed
score `Z = 1.0` and every composite below that score. The planned
zero-excess formulation keeps the same mathematics and changes the coordinate
system:

```text
old coordinate: primes have Z(n) = 1
new coordinate: primes have E(n) = 0
```

This is a significant documentation and script migration. The goal is not to
change the local PGS theorems. The goal is to make the arithmetic source easier
to see: primes are exact zero-excess returns, gap interiors are positive-excess
chambers, and the selected interior integer is the leftmost minimum-excess
point before the next zero return.

For the deeper repo-wide scope inventory, see
[Zero-Excess DNI Change Scope](change-scope.md).

For the four-agent risk conference and revised migration gates, see
[Zero-Excess DNI Risk Conference](zero-excess-risk-conference.md).

Phase 1 launch controls:

- [Notation Contract](notation-contract.md)
- [Boundary Checklist](phase-1-boundary-checklist.md)
- [Risk Verdict Gate](phase-1-risk-verdict.md)

Phase 2 launch control:

- [Phase 2 Risk Verdict Gate](phase-2-risk-verdict.md)

Phase 3 launch control:

- [Phase 3 Risk Verdict Gate](phase-3-risk-verdict.md)

## Branch Scope

Working branch:

```text
codex/zero-excess-dni
```

This branch should first establish the migration contract, then update docs,
then update code and tests where the code surface actually benefits from the
new coordinate. Historical outputs, benchmark reports, and legacy public APIs
should be preserved unless a later step explicitly migrates them.

## Mathematical Contract

The existing DNI is

$$
Z(n)=n^{1-\tau(n)/2}.
$$

The zero-excess coordinate is the negative logarithm of the same quantity:

$$
E(n)=-\log Z(n)
=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For `n > 1`,

$$
E(n)=0 \iff \tau(n)=2 \iff n \text{ is prime},
$$

and

$$
E(n)>0
$$

for every composite `n`.

The domain guard matters: `n=1` has `log(1)=0`, so it also gives `E(1)=0`.
All prime-placement statements must say `n > 1` or otherwise exclude `1`.

The existing local score in `PROOF.md` is

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.
$$

Therefore

$$
F(n)=-E(n).
$$

The Interior Maximizer Theorem can be read without changing its content:

```text
old reading: w uniquely maximizes F(n)
new reading: w uniquely minimizes E(n)
```

Inside a nonempty prime gap, every interior integer has positive excess. The
GWR-selected integer is the first interior point with minimum positive excess.
The next prime is the next exact return to the zero-excess floor.

## DNI-To-Zeta Contract

The zero-excess coordinate must preserve the exact zeta-compression identity.
The current bridge uses the divisor-normalization load

$$
\kappa(n)=\frac{\tau(n)\log n}{e^2}
$$

and the scaling

$$
v=\frac{e^2}{2}.
$$

The scaled load is

$$
v\kappa(n)=\frac{\tau(n)\log n}{2}.
$$

In zero-excess language this is

$$
\frac{\tau(n)\log n}{2}
=\log n+E(n).
$$

So the exact numerator used by the DNI-to-zeta bridge is not just excess. It is
the baseline logarithmic size plus excess:

```text
bridge load = log n + zero excess
```

Let

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Then

$$
H(s)=\sum_{n\ge1}\frac{H(n)}{n^s}
=-\frac{1}{2}D'(s),
$$

where

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

The continued DNI ratio remains

$$
R(s)=\frac{H(s)}{D(s)}
=-\frac{1}{2}\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

This is the key migration fact. Zero-excess DNI changes the integer-side
coordinate while preserving the exact compression route through `D`, `H`, and
`R`.

## RH Communication Contract

The zero-excess formulation should strengthen the PGS-to-RH bridge without
collapsing source and compression objects.

Use this distinction:

```text
zero-excess floor: integer-side, arithmetic, exact, local
critical line: zeta-side, analytic, compressed, global
```

The zero-excess floor is not the critical line. The intended analogy is:

```text
PGS source side: primes are exact zero-excess returns.
Zeta/RH side: the compressed source is read through pole placement on the
critical line.
```

The documentation should invite that analogy while preventing identity
confusion. Do not say that RH places primes close to the zero-excess floor. Say
that RH is the pole-placement sentence of the zeta-compressed record of a
source where primes are exact zero-excess returns.

## Naming Contract

Preferred terms:

- Zero-Excess DNI
- zero-excess coordinate
- zero-excess floor
- zero-excess return
- positive-excess chamber
- minimum-excess selected integer

Terms to keep but demote to legacy or dual-coordinate status:

- raw-Z
- `Z = 1.0`
- fixed-point locus
- log-score
- prime-centered score

Terms to avoid as primary names:

- zero line
- zero locus
- zeta zero line

`zero line` is useful conversationally, but it collides with zeta zeros and
the critical line. Documentation should use `zero-excess floor`.

## Downstream Impact Inventory

### Root Documentation

- `README.md`: replace "primes at Z = 1.0" language with zero-excess floor
  language after the concrete divisor-count examples. Preserve the current
  narrative flow.
- `RESULTS.md`: update the Divisor Normalization Identity section so it gives
  both coordinates and treats zero-excess as the preferred explanatory
  coordinate.
- `PROOF.md`: do not change theorem claims. Add the equivalence
  `F(n)=-E(n)` where it helps readers see the minimizer translation.
- `DIVISOR_NORMALIZATION_IDENTITY.md`: likely the primary rewrite target.
  It should become the source document for the dual coordinate:
  `Z(n)=n^{1-\tau(n)/2}` and `E(n)=-log Z(n)`.
- `LEFTMOST_MINIMUM_DIVISOR_RULE.md`: translate "raw-Z/log-score maximizer"
  to "minimum-excess selected integer" while preserving the old formula as the
  dual coordinate.
- `RECURSIVE_PRIME_WALK.md`: update "log-score maximizer" language to the
  zero-excess chamber reading.
- `PRIME_GAP_GENERATOR.md` and generator-facing specs: introduce "next
  zero-excess return" as the endpoint language only where it improves clarity.

### RH Bundle And FAQ

- `docs/rh/README.md`: add the zero-excess floor as the integer-side source
  coordinate before DNI-to-zeta compression.
- `docs/rh/source-order.md`: insert the source order
  `divisor counts -> zero-excess returns -> PGS local theorems -> ...`.
- `docs/rh/dni-to-zeta-compression.md`: add the `H(n)=log n+E(n)` bridge load
  so the zeta compression remains exact.
- `docs/rh/pole-placement.md`: distinguish zero-excess floor from critical
  line.
- `docs/rh/critical-line-and-zero-geometry.md`: add an explicit guard:
  source-side zero-excess floor is not the analytic critical line.
- `docs/rh/off-critical-pole-exclusion.md`: decide whether the residual test
  names excess as part of the source-side carrier inventory.
- `docs/rh/status-ledger.md` and `docs/rh/reviewer-map.md`: add a status label
  for zero-excess coordinate reformulation. It should be an exact coordinate
  change, not a new theorem.
- `docs/faq/README.md`: add a Zero-Excess DNI entry if a new FAQ page is made.
- `docs/faq/core-frame/*`: update source-object and RH-downstream pages to
  include zero-excess returns.
- `docs/faq/zeta-compression/*`: update compression pages with the
  `H(n)=log n+E(n)` relation.
- `docs/faq/category-errors/*`: add or update a page explaining why the
  zero-excess floor is analogous to, but not identical with, the critical line.
- `docs/faq/reviewer-guidance/status-ledger.md`: add the status label
  `exact coordinate reformulation`.

### Vocabulary And Public Writing

- `docs/vocabulary/nonstandard_terms_dictionary.md`: update entries for
  `DNI`, `raw-Z`, `log-score`, `Z-Band`, `proxy_z`, `fixed-point locus`, and
  add `zero-excess floor`.
- `docs/essays/01_genesis_of_dni.md`: likely needs a substantial rewrite if
  it presents DNI as a `Z = 1.0` discovery.
- `docs/essays/the-riemann-hypothesis-is-obsolete.md`: add the zero-excess
  floor as the source-side visual bridge if it does not interrupt the essay.
- `docs/essays/substack/series/*`: update public prose only after root docs
  are stable.
- X-post assets under `docs/x-posts/` and `research/12-rh-bridge/assets/x-posts/`:
  images or captions using `Z = 1.0`, raw-Z, or fixed-point language may need
  refreshed versions. Historical assets can remain archived.

### Research Documentation

- `research/12-rh-bridge/README.md`: align with `docs/rh` after the public
  docs settle.
- `research/12-rh-bridge/docs/dni_rh_bridge.md`: add the exact
  zero-excess-to-bridge-load relation.
- `research/12-rh-bridge/docs/prime-structure-program/index.html`: update
  visual language if it uses old fixed-point scoring.
- `research/02-gwr-dni/README.md`: translate the chapter overview from raw-Z
  peak language to zero-excess floor language.
- `research/02-gwr-dni/docs/*`: update live docs that describe log-score,
  raw-Z, and selected integers. Archive or generated reports can keep
  historical terminology if marked as historical.
- `research/02-gwr-dni/story/story/*`: update story prose and plot labels if
  the story is still public-facing.
- `research/04-bounded-compression/docs/*`: update "GWR/DNI selected witness"
  wording only where zero-excess makes the bounded witness easier to read.
- `research/00-index/continuity/START_HERE.md` and
  `research/00-index/status-map.md`: add this branch/project once migration
  work begins beyond this plan.

### Python Packages And Tests

- `src/python/z_band_prime_invariant/core.py`: add a direct function for
  zero excess, likely `exact_zero_excess(n)` or `exact_excess(n)`, while
  preserving `exact_z_normalize`.
- `src/python/z_band_prime_invariant/__init__.py`: export the new function
  after tests exist.
- `src/python/z_band_prime_gap_ridge/runs.py`: current score is
  `(1.0 - d/2) * log(n)` with `argmax`. The zero-excess version is
  `(d/2 - 1.0) * log(n)` with `argmin`. Output schema names such as
  `best_n_z` should not be changed until a compatibility decision is made.
- `src/python/z_band_prime_rh_bridge/bridge.py`: incorporate or test the
  `H(n)=log n+E(n)` formulation. The exact ratio must remain unchanged.
- `src/python/z_band_prime_prefilter/prefilter.py`: keep `proxy_z`,
  `FIXED_POINT_V`, and Z-Band public names in the first pass. This is a legacy
  API and benchmark surface.
- `tests/python/prefilter/test_prefilter.py`: preserve current API tests. Add
  zero-excess tests separately if the invariant package grows a new function.
- `tests/python/prefilter/test_vectors.py`: golden vectors include
  `z_at_fixed_point` and `proxy_z`; do not churn them in a documentation-first
  branch.
- `tests/python/test_doc_proof_status_surface.py`: update only if doc phrases
  it checks change.
- `research/02-gwr-dni/tests/*`: add equivalence tests for
  `argmax F = argmin E` before changing script names.

### C And High-Scale Generator

- `src/c/high-scale-pgs/*`: likely low impact because the high-scale path is
  divisor-count and chamber based, not raw-Z based. Audit diagnostics for
  "score" or "normalization" before assuming no impact.
- C tests should not change unless exposed diagnostics or docs change.

### Legacy Prefilter

The legacy cryptographic prefilter is the main compatibility risk.

Keep these as legacy/public API in the first migration pass:

- `Z-Band`
- `proxy_z`
- `FIXED_POINT_V`
- `exact_z_normalize`
- `Z = 1.0` pass-through convention
- existing benchmark reports and technical note language

The zero-excess migration can add explanatory crosswalks, but it should not
rename or change the legacy API without a separate compatibility plan.

### Generated Outputs And Historical Artifacts

Do not bulk-edit historical JSON, CSV, benchmark reports, PDFs, or generated
plot images. Prefer one of these statuses:

- live documentation: migrate to zero-excess language;
- live code/tests: add dual-coordinate support and compatibility tests;
- historical artifact: leave as-is and label as historical if referenced;
- generated image: regenerate only when the source script is migrated.

## Implementation Phases

1. Planning contract
   - Create this document.
   - Inventory old coordinate language.
   - Decide canonical function and vocabulary names.

2. Core docs
   - Rewrite `DIVISOR_NORMALIZATION_IDENTITY.md`.
   - Update `README.md`, `RESULTS.md`, `LEFTMOST_MINIMUM_DIVISOR_RULE.md`,
     and `RECURSIVE_PRIME_WALK.md`.
   - Keep `PROOF.md` theorem status unchanged and add only the
     `F(n)=-E(n)` reading.

3. RH docs and FAQ
   - Update `docs/rh` to use zero-excess floor as the source-side coordinate.
   - Add the zero-excess floor versus critical line distinction.
   - Update FAQ objection handling.

4. Code support
   - Add zero-excess helper functions without breaking existing Z-Band APIs.
   - Add equivalence tests:
     `E(n)=-log Z(n)`, `F(n)=-E(n)`, and selected integer parity.

5. Script migration
   - Migrate live GWR/DNI scripts from raw-Z argmax wording to zero-excess
     argmin wording.
   - Preserve output compatibility or write a schema migration note.

6. Public and visual surfaces
   - Regenerate public plots only after scripts and labels are stable.
   - Update essays and X-post source material last.

## Acceptance Checks

Documentation checks:

```text
rg -n "Z = 1.0|Z=1.0|raw-Z|fixed-point locus|log-score|prime-centered score" \
  README.md RESULTS.md DIVISOR_NORMALIZATION_IDENTITY.md \
  LEFTMOST_MINIMUM_DIVISOR_RULE.md RECURSIVE_PRIME_WALK.md docs/rh docs/faq
```

Expected result after migration: hits are either removed, labeled legacy, or
paired with the zero-excess coordinate.

Equivalence checks:

```text
E(n) = -log Z(n)
F(n) = -E(n)
argmax(F over a gap interior) = argmin(E over the same interior)
E(n) = 0 iff n > 1 and tau(n) = 2
E(n) > 0 for composite n
```

Code checks should include the existing prefilter tests if any public API is
touched:

```text
python3 -m pytest tests/python/prefilter
```

and the focused GWR/DNI tests if live scripts are migrated:

```text
python3 -m pytest research/02-gwr-dni/tests
```

## Risks And Guardrails

- Do not imply a new theorem. This is an exact coordinate reformulation.
- Do not claim `PROOF.md` itself proves RH. It proves the local PGS theorems.
- Do not identify the zero-excess floor with the critical line.
- Do not say RH places primes close to the zero-excess floor.
- Do not break `proxy_z` or Z-Band benchmark semantics in the first pass.
- Do not bulk-edit historical artifacts to hide old terminology.
- Do not forget the `n=1` exception.
- Do not flip score comparisons without tests. `argmax F` becomes `argmin E`.

## Open Decisions

- Canonical function name in code: `exact_zero_excess`, `zero_excess`, or
  `exact_excess`.
- Whether `DIVISOR_NORMALIZATION_IDENTITY.md` remains the primary document or
  becomes an index pointing to a new `ZERO_EXCESS_DNI.md`.
- Whether live GWR/DNI output schemas keep names like `best_n_z` during the
  first migration.
- Whether the legacy prefilter gets only explanatory crosswalks or a new
  optional zero-excess report column.
- Whether to add a dedicated FAQ page named "Is the zero-excess floor the
  critical line?".

## First Suggested Edit Sequence

1. Rewrite `DIVISOR_NORMALIZATION_IDENTITY.md` around the dual coordinate.
2. Update `LEFTMOST_MINIMUM_DIVISOR_RULE.md` to say the selected integer is the
   leftmost minimum-excess interior point.
3. Add one compact zero-excess section to `docs/rh/README.md`.
4. Add the `H(n)=log n+E(n)` derivation to
   `docs/rh/dni-to-zeta-compression.md`.
5. Add code helpers and equivalence tests in `src/python/z_band_prime_invariant`.

That sequence changes the explanation before changing runtime behavior. It
keeps the branch auditable and prevents a broad terminology migration from
silently changing proved theorem status or legacy benchmark meaning.
