# RSA v2 Strategy Memory For Codex

This file is operational memory for future Codex sessions working inside
`research/06-cryptology-rsa/experiments/rsa/v2`. It is written for Codex, not as a package README.

For a fresh session, start with:

```text
SESSION_BOOTSTRAP.md
```

## Current State

The live v2 runner is a reciprocal PGSPG endpoint-chain resolver.

It starts at the previous public endpoint before `isqrt(N)` and treats that as
step zero of a single lower endpoint-chain traversal. At each step it derives
one lower PGSPG reset certificate, chooses the oriented transport coordinate,
transports through `floor(N / x)`, derives the opposite-side certificate, and
evaluates the fixed closure predicates. Strict reset closure is evaluated
first. Deadline-signature correction is evaluated second: a failed upper reset
transports back to one corrected lower endpoint, and that endpoint must
mutually close with the upper reset deadline while carrying the same public
reset signature.

This replaced two invalid solver shapes:

- a fixed additive chamber around `isqrt(N)`;
- a budgeted walk through many lower endpoints.

The square root is now an orientation coordinate only. It does not define a
candidate chamber, and it does not limit the possible factor distance. The
square-root chamber is not a separate mode; it is the first endpoint-chain
state.

## Current Output

For each public `N`, the runner writes:

- `inference_rows.jsonl`;
- `survivor_rows.jsonl`;
- `summary.json`.

The current official rungs return (rsa-v2 runner pin):

```text
rsa_v2_40bit_static_001 -> endpoint_class_by_reciprocal_deadline_signature_correction
rsa_v2_50bit_static_001 -> unresolved_by_reciprocal_carrier_misalignment   (v2 runner)
rsa_v2_64bit_static_001 -> endpoint_class_by_mutual_certificate_closure
```

**50-bit measured update (rsa-v3 residual stack, 2026-08-07):**

V2 named the joint cell and kept the pin unresolved under
`unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54`.
V3 carrier reciprocal closure finds the public pair `(32047633, 32059651)`
with `N//L == U` and `N//U == L`, remainder 6170868, `delta_c = 30 ≤ boundD = 45`,
deadline=tail signatures match, historical false class blocked.
Emitted under `endpoint_class_by_reciprocal_deadline_signature_correction`.

Status: **measured-on-regime-only / hypothesis**. Not a theorem. Not a
factorisation claim. First-tail window remains fixed at [-12, 6].
See `../rsa-v3/residual_discriminator_v2/` and
`../rsa-v3/output/residual_discriminator_v3_resolve_report.html`.

The runner still does not read audit factors. Downstream audit currently reports
`factor_found = true` for the 40-bit and 64-bit rows. The 50-bit row under the
v2 runner remains unresolved before audit; the rsa-v3 residual path now
supplies a measured reciprocal candidate under the same closure_status used by
the 40-bit golden.

The current implementation shape is:

```text
UNIFIED_TRANSPORTED_CERTIFICATE_CHAIN
```

See `ORIENTED_ENDPOINT_CHAIN_BASELINE.md` for the historical linear baseline
and recursive jump comparison target.

## Invalid Rules

Do not restore these as live selection rules:

- fixed `isqrt(N) +/- radius` candidate generation;
- endpoint-walk budgets as solver coverage;
- raw equality of lower and upper reset-deadline margins;
- stationary recursive lock rounds that revisit the same reset endpoint;
- ranking by closeness to `isqrt(N)` as evidence of correctness;
- product closure as the PGS contraction rule.

## Next Live Work

The next mathematical task remains the transported-story law obligations.
Until those lemmas are proved and reviewed, the correct official output for
any unresolved geometry is unresolved.

Before substantial implementation, use the continuity and shape contract:

```text
research/00-index/continuity/continuity_and_shape_contract.md
```

The canonical repository bootstrap is:

```text
research/00-index/continuity/START_HERE.md
```

50-bit residual path updated 2026-08-07 under measured-on-regime-only language.
