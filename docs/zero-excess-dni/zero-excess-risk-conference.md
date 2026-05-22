# Zero-Excess DNI Risk Conference

This document consolidates the four-agent risk conference for the
Zero-Excess DNI migration.

The source object is unchanged: divisor counts place primes at exact returns
to the prime condition `tau(n)=2`. The proposed coordinate writes that same
source fact as zero excess:

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For `n > 1`,

$$
E(n)=0 \iff \tau(n)=2 \iff n \text{ is prime}.
$$

The migration risk is not mathematical novelty. The risk is semantic drift:
readers, scripts, or future agents may treat a coordinate change as a new
theorem, may replace the zeta bridge load with excess alone, or may break
legacy Z-Band compatibility.

## Conference Setup

Four read-only agents reviewed the branch from different risk positions:

| Agent | Role | Primary question |
| --- | --- | --- |
| Math/notation | Symbol and theorem hazards | Can the new coordinate be misread or misapplied? |
| Documentation/status | Public and reviewer-facing prose | Can the migration cause proof-status drift? |
| Code/compatibility | Runtime, tests, APIs, schemas | Can additive migration become a breaking rename? |
| Migration/release | Sequencing, artifacts, branch hygiene | Can the branch create contradictory live surfaces? |

The conference ran in two rounds. First, each agent produced an independent
risk memo. Second, the agents saw the shared findings and revised their
priority calls.

## Conference Decision

Proceed only as a staged semantic migration.

The first implementation phase must include the root explanatory docs and the
LLM-facing status guardrails together. The conference rejected a sequence where
root docs move first and FAQ/RH status pages move later. Broad RH prose rewrites
can wait, but the status surfaces must move with the root docs so the branch
does not teach mixed semantics.

Phase 1 should therefore include a small guardrail bundle:

- `DIVISOR_NORMALIZATION_IDENTITY.md`
- `README.md`
- `RESULTS.md`
- `PROOF.md`
- `LEFTMOST_MINIMUM_DIVISOR_RULE.md`
- `docs/faq/_style-guide.md`
- `docs/faq/reviewer-guidance/status-ledger.md`
- `docs/rh/status-ledger.md`
- `docs/rh/README.md`
- `research/00-index/status-map.md`

The phase 1 wording must carry four facts everywhere the new coordinate is
introduced:

```text
exact coordinate reformulation
for n > 1, E(n)=0 iff n is prime
F(n)=-E(n), so argmax F = leftmost argmin E
zero-excess floor is integer-side; the critical line is zeta-side
```

## Highest Risks

### 1. Status Drift Around RH

Severity: high.

Risk:

Zero-excess language can make the PGS-to-RH case easier to see, but it can also
make readers think the zero-excess coordinate itself is a new proof or that
`PROOF.md` directly proves RH. This conflicts with the repository contract:
`PROOF.md` controls the local PGS theorem status, while `docs/rh` carries the
downstream PGS-to-RH reading path.

Affected surfaces:

- `PROOF.md`
- `README.md`
- `RESULTS.md`
- `docs/rh/README.md`
- `docs/rh/status-ledger.md`
- `docs/faq/_style-guide.md`
- `docs/faq/reviewer-guidance/status-ledger.md`
- `research/00-index/continuity/START_HERE.md`

Required mitigation:

```text
PROOF.md proves the local PGS source theorems. The zero-excess coordinate is an
exact coordinate reformulation of the same source layer. The RH-facing bundle
uses that source layer downstream after exact DNI-to-zeta compression and
source-side residual closure.
```

Status label to add:

```text
exact coordinate reformulation
```

### 2. Losing The Bridge Load

Severity: high.

Risk:

The zeta-facing numerator cannot become excess alone. The live DNI-to-zeta
bridge uses the divisor load

$$
\frac{\tau(n)\log n}{2}.
$$

In zero-excess coordinates,

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

If a doc or script replaces `H(n)` with `E(n)`, the exact identity

$$
R(s)=-\frac{\zeta'(s)}{\zeta(s)}
$$

is no longer the same bridge.

Affected surfaces:

- `docs/rh/dni-to-zeta-compression.md`
- `research/12-rh-bridge/docs/dni_rh_bridge.md`
- `src/python/z_band_prime_rh_bridge/bridge.py`
- `research/12-rh-bridge/tests/test_bridge.py`

Required mitigation:

```text
The zeta-compression numerator is H(n)=log n+E(n)=tau(n)log(n)/2.
The excess-only series is not the DNI-to-zeta numerator and must not be called
K(s) or used in R(s).
```

Required test if bridge code changes:

```text
FIXED_POINT_V * normalization_load[n] == log(n) + exact_zero_excess(n)
```

for representative `n >= 2`.

### 3. The `n=1` Zero

Severity: high.

Risk:

`E(1)=0` because `log(1)=0`. Therefore the statement "`E(n)=0` iff `n` is
prime" is false unless it carries the domain guard `n > 1`.

Affected surfaces:

- `docs/zero-excess-dni/README.md`
- `docs/zero-excess-dni/change-scope.md`
- `DIVISOR_NORMALIZATION_IDENTITY.md`
- `docs/rh/dni-to-zeta-compression.md`
- any coefficient table that starts at `n=1`

Required mitigation:

```text
For n > 1, E(n)=0 iff n is prime. The value n=1 also has zero excess because
log(1)=0; it is not a prime return, gap endpoint, or member of any prime-gap
interior.
```

### 4. Sign Reversal In The Local Theorem

Severity: high.

Risk:

The local proof score is

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.
$$

The zero-excess coordinate gives

$$
F(n)=-E(n).
$$

The old theorem says the selected interior integer maximizes `F`. In
zero-excess language, the same selected integer minimizes `E`. Any phrase such
as "maximize excess" is wrong.

Affected surfaces:

- `PROOF.md`
- `LEFTMOST_MINIMUM_DIVISOR_RULE.md`
- `RESULTS.md`
- `research/02-gwr-dni/**`
- `research/11-gap-ridge/**`

Required mitigation:

```text
On the same nonempty prime-gap interior, w = argmax F = leftmost argmin E.
The theorem status is unchanged; only the coordinate sign changes.
```

### 5. Symbol Collision Around `E`

Severity: high.

Risk:

`E(n)` and `E(q)` already appear in unrelated live or semi-live surfaces. A
global zero-excess rollout can make future readers merge different quantities.

Known collisions:

- bounded-compression `E(q)` in `RESULTS.md`,
  `RECURSIVE_PRIME_WALK.md`, `research/04-bounded-compression/README.md`, and
  `pgs-math-explainer/index.html`;
- divisor-field-extremals `E(n)=(sigma(n)-n)/n` under
  `pgs-unsolved-problems/divisor-field-extremals/`;
- RSA endpoint-cell `E` notation under
  `research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/`.

Required mitigation:

```text
E(n) means zero excess only when explicitly defined as
E(n)=(tau(n)/2-1)log n. Other live E(...) notations must be renamed, locally
reserved, or marked non-zero-excess before zero-excess language lands nearby.
```

### 6. Public API And Schema Breakage

Severity: high.

Risk:

The legacy Z-Band surfaces are public compatibility surfaces. The migration
must not silently rename API names, JSON keys, vector fields, CLI names, or
benchmark schema fields.

Preserve in phase 1:

- `z-band-prime-prefilter`
- `Z-Band`
- `CDLPrimeZBandPrefilter`
- `proxy_z`
- `z_hat`
- `d_est`
- `fixed_point_v`
- `z_at_fixed_point`
- `FIXED_POINT_V`
- `FIXED_POINT_TOLERANCE`
- `exact_z_normalize`
- `is_prime_candidate`
- `is_probable_prime`
- `spec/vectors/*.json`
- gap-ridge fields such as `best_n_z`, `best_d_z`, `next_peak_offset`,
  `current_peak_offset`, `log_score_margin`, and `min_log_score_margin`

Required mitigation:

```text
Add zero-excess crosswalks. Do not rename public Z-Band fields, committed
vector schemas, or gap-ridge output fields in phase 1.
```

If code is touched, add `exact_zero_excess(n)` additively in the invariant
package. Do not implement it as `-log(exact_z_normalize(n))`, because the
existing exact-Z helper has compatibility behavior for `n <= 1` and can
underflow for large composites.

### 7. Generated And Historical Artifact Churn

Severity: high.

Risk:

A repo-wide rename would produce noisy diffs in generated, historical, binary,
or benchmark artifacts and would make the migration impossible to audit.

Out of scope for phase 1:

- `research/*/output/`
- `research/04-bounded-compression/docs/generated/`
- `research/02-gwr-dni/experiments/chatgpt/`
- `research/00-index/archive/`
- `research/06-cryptology-rsa/archive/`
- `research/06-cryptology-rsa/experiments/archive/`
- `pgs-math-explainer/audio/`
- `pgs-math-explainer/scene-videos/`
- `pgs-unsolved-problems/*/*.csv`
- `pgs-unsolved-problems/*/*.json`
- `docs/gap-structure-factor-brief-evidence/**/output/`
- `data/external/primegap_list_records_1e12_1e18.csv`
- `gists/try-yourself/plots/`
- `apps/prime-gap-structure-interactive-mockup/`
- existing `.png`, `.svg`, `.pdf`, `.docx`, `.mp3`, `.mp4`, `.json`,
  `.jsonl`, and `.csv` outputs unless a later artifact pass names the source
  path and regeneration command.

Required mitigation:

```text
Do not bulk-edit generated, historical, binary, benchmark, or archived outputs.
Regenerate only from named source paths in a separate artifact pass.
```

### 8. Prime-Generator Spec And Release Contract Tension

Severity: medium-high.

Risk:

The live release contract for the production generator says the emitted record
is exactly:

```json
{"p": 11, "q": 13}
```

Any spec page that describes inference metadata in the output layer must be
treated as historical, proposed, or reconciled before it becomes a migration
target.

Affected surfaces:

- `docs/specs/prime-gen/tech_spec_pgs_prime_generator.md`
- `docs/releases/pgs_inference_generator_v1_1_pgs_only.md`
- `PRIME_GAP_GENERATOR.md`
- `src/c/high-scale-pgs/**`

Required mitigation:

```text
Production generator output remains exactly {"p": ..., "q": ...}. Zero-excess
diagnostics, if added later, belong in sidecar records.
```

## Revised Migration Sequence

### Phase 0: Lock The Risk Contract

Artifacts:

- `docs/zero-excess-dni/README.md`
- `docs/zero-excess-dni/change-scope.md`
- this risk conference document

Exit gate:

- risk register exists;
- status labels and required mitigation language are ready for phase 1;
- no runtime code changed.

### Phase 1: Root Docs Plus Guardrail Surfaces

Scope:

- canonical root explanatory docs;
- minimal FAQ/RH status guardrails;
- notation ledger for `E(n)`;
- no broad research corpus migration;
- no public API rename;
- no vector/schema rewrite.

Required phrase:

```text
The zero-excess coordinate is an exact coordinate reformulation.
```

Exit gate:

- `n > 1` guard appears wherever `E(n)=0` characterizes primes;
- `F(n)=-E(n)` appears wherever proof notation is translated;
- RH guardrail pages distinguish zero-excess floor from critical line;
- `H(n)=log n+E(n)` appears on bridge surfaces;
- status ledgers include `exact coordinate reformulation`.

### Phase 2: RH And FAQ Prose Migration

Scope:

- `docs/rh/**` narrative pages;
- FAQ objection handling;
- source-order bridge language.

Exit gate:

- no page implies the zero-excess floor is the critical line;
- no page implies RH places primes close to the zero-excess floor;
- no page replaces the bridge load with `E(n)` alone.

### Phase 3: Additive Code Helpers And Tests

Scope:

- add `exact_zero_excess(n)` to `src/python/z_band_prime_invariant/core.py`;
- export additively from `src/python/z_band_prime_invariant/__init__.py`;
- add tests without renaming public APIs.

Required tests:

- `E(n)=(tau(n)/2-1)log n`;
- `E(n)=-log Z(n)` only where `Z(n)>0`;
- primes `n > 1` have `E(n)=0`;
- composites have `E(n)>0`;
- `n=1` behavior is explicit;
- `F(n)=-E(n)`;
- `FIXED_POINT_V * normalization_load[n] == log(n)+E(n)`.

Mandatory checks if code changes:

```text
python3 -m pytest tests/python/prefilter
python3 -m pytest research/12-rh-bridge/tests/test_bridge.py
python3 -m pytest research/02-gwr-dni/tests research/11-gap-ridge/tests
```

Run C checks only if C changes:

```text
make -C src/c/high-scale-pgs test
```

### Phase 4: Compatibility Review For Any Schema Or API Change

Scope:

- new vector family only if needed;
- aliases before renames;
- public API changes only after explicit approval.

Exit gate:

- committed vectors are unchanged unless a schema migration is explicitly
  approved;
- old fields remain present when aliases are added;
- release docs still preserve minimal generator output.

## Conference Disagreements

The agents converged on the core migration but disagreed with the original
sequencing in one place.

Initial migration/release view:

```text
Defer RH, FAQ, research corpus, visual media, code helpers, schemas, and legacy
prefilter docs until after the root docs.
```

Final conference view:

```text
Defer broad RH and FAQ prose rewrites, but do not defer RH/FAQ status
guardrails. The LLM-facing status pages must move with the root docs.
```

The reason is direct: stale reviewer/status surfaces would preserve the old
`Z=1.0` frame while root docs introduce `E(n)=0`, creating exactly the mixed
semantics the migration is meant to prevent.

## Go/No-Go Checklist

Before implementation proceeds beyond planning:

- [ ] `E(n)` symbol collisions are listed in the migration doc.
- [ ] Phase 1 includes FAQ/RH status guardrails, not only root docs.
- [ ] `docs/specs/prime-gen/tech_spec_pgs_prime_generator.md` is either
      reconciled with the v1.1 release contract or moved out of phase 1.
- [ ] The bridge-load rule `H(n)=log n+E(n)` is treated as mandatory.
- [ ] Public Z-Band names and vector schemas are explicitly protected.
- [ ] Generated and historical artifacts are explicitly out of scope.
- [ ] Code changes, if any, are additive and tested against prefilter/vector
      compatibility.

## Open Decisions

1. Whether to rename bounded-compression `E(q)` before or during phase 1.
2. Whether to reserve `E(n)` globally for zero-excess and require local
   renaming of divisor-field-extremals sigma-excess notation.
3. Whether `docs/specs/prime-gen/tech_spec_pgs_prime_generator.md` should be
   reconciled with the release contract or marked historical before migration.
4. Whether to add the zero-excess category-error FAQ page in phase 1 or only
   update status ledgers in phase 1.
5. Whether the first code pass should include bridge tests only, invariant
   helpers only, or both.
