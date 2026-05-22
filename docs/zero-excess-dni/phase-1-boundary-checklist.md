# Zero-Excess DNI Phase 1 Boundary Checklist

Phase 1 is a documentation and status migration. It updates how live docs
describe the same DNI coordinate structure, with zero-excess language preferred
where the current explanatory surface benefits from it. Phase 1 does not move
code, schemas, generated outputs, historical reports, binary assets, benchmark
records, or public compatibility surfaces.

The release rule is narrow: migrate the explanatory status of live documents,
preserve artifact contracts, and stop when a file requires a code, schema,
vector, benchmark, or historical-output decision.

## Phase 1 Contract

- Phase 1 is docs/status migration, not code migration.
- Phase 1 is docs/status migration, not schema migration.
- No production generator behavior changes are part of Phase 1.
- No public API rename is part of Phase 1.
- No committed vector rewrite is part of Phase 1.
- No benchmark schema rewrite is part of Phase 1.
- No historical output rewrite is part of Phase 1.
- No binary or generated artifact rewrite is part of Phase 1.

## Out Of Scope

The following artifact classes are out of scope for Phase 1:

- generated artifacts;
- historical artifacts;
- binary artifacts;
- benchmark artifacts;
- archived reports;
- committed vector payload rewrites;
- generated JSON, CSV, PDF, SVG, PNG, MP3, or MP4 outputs;
- compatibility schema migrations;
- production generator record-format changes.

The unrelated untracked directory `docs/app-ideas/` is out of scope. Do not
inspect, normalize, stage, move, delete, or edit it as part of this launch.

## Compatibility Names To Preserve

These names and public surfaces must be preserved in Phase 1:

- `Z-Band`
- `proxy_z`
- `z_hat`
- `fixed_point_v`
- `z_at_fixed_point`
- `FIXED_POINT_V`
- `exact_z_normalize`
- `spec/vectors/*.json`
- gap-ridge legacy fields

Phase 1 docs may add crosswalk language such as `Z=1.0 <-> E=0` where useful,
but they must not rename or rewrite those compatibility surfaces.

## Generator Artifact Boundary

The production generator output remains exactly:

```json
{"p": 11, "q": 13}
```

For every resolved input prime, the production stream remains:

```json
{"p": ..., "q": ...}
```

Do not add zero-excess fields, diagnostics, certificates, source labels,
confidence labels, counters, audit results, or migration metadata to the
production generator output.

If zero-excess diagnostics are added later, they belong in sidecar records. They
do not belong in the production generator stream.

## Prime Generator Spec Hold

`docs/specs/prime-gen/tech_spec_pgs_prime_generator.md` must be reconciled with
the v1.1 release contract before it is migrated.

The reconciliation must confirm that the spec preserves:

- the input/output contract `input known prime p -> output next prime q`;
- production output records exactly shaped as `{"p": ..., "q": ...}`;
- audit, certificate, diagnostic, and zero-excess metadata outside the
  production stream;
- explicit unresolved state where the PGS rule does not resolve;
- no fallback search, no classical selector, and no audit result choosing `q`.

Until that reconciliation is complete, the spec is a compatibility hold, not a
normal Phase 1 wording target.

## Phase 1 Pre-Commit Checks

Run these checks before committing Phase 1 boundary or documentation migration
work:

- Confirm `git branch --show-current` returns `codex/zero-excess-dni`.
- Confirm `git status --short` shows no unintended edits outside the assigned
  Phase 1 write scope.
- Confirm generated, historical, binary, benchmark, and vector artifacts were
  not modified.
- Confirm `docs/app-ideas/` remains untouched and unstaged.
- Confirm no production generator code was edited.
- Confirm no schema, vector, or benchmark field was renamed.
- Search changed files for public compatibility names and verify they are
  preserved when mentioned:
  `Z-Band`, `proxy_z`, `z_hat`, `fixed_point_v`, `z_at_fixed_point`,
  `FIXED_POINT_V`, `exact_z_normalize`, `spec/vectors/*.json`, and gap-ridge
  legacy fields.
- Search changed files for production generator records and verify the emitted
  stream remains `{"p": ..., "q": ...}` only.
- Confirm any zero-excess diagnostic wording points to sidecar records, not the
  production generator stream.
- Confirm `docs/specs/prime-gen/tech_spec_pgs_prime_generator.md` is either
  already reconciled with the v1.1 release contract or explicitly held out of
  migration.
- Confirm Markdown uses LF line endings.
- Confirm any math uses GitHub-safe `$...$` or `$$...$$` notation.

## Go / No-Go Checklist

### Go

- Phase 1 changes are limited to live documentation and status wording.
- The existing theorem status is preserved.
- Zero-excess wording is introduced as an exact coordinate reformulation.
- Public API and vector names remain stable.
- Production generator output remains exactly `{"p": ..., "q": ...}`.
- Diagnostics and certificates remain outside the production output stream.
- Generated, historical, binary, benchmark, and vector artifacts are untouched.
- `docs/app-ideas/` is untouched.
- The prime-generator technical spec has been reconciled before migration, or
  held back explicitly.

### No-Go

- A code file changed as part of Phase 1.
- A schema, vector, benchmark, or legacy field changed as part of Phase 1.
- A generated, historical, binary, or benchmark artifact changed.
- A public compatibility name was renamed or removed.
- The production generator output gained fields beyond `p` and `q`.
- Zero-excess diagnostics were placed in the production generator stream.
- `docs/specs/prime-gen/tech_spec_pgs_prime_generator.md` was migrated before
  reconciliation with the v1.1 release contract.
- The unrelated `docs/app-ideas/` directory was touched, staged, moved, or
  deleted.
