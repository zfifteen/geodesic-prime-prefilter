# RSA v2 Operational Contract

This folder is the clean RSA factorizer experiment.

## Session Bootstrap

When a new Codex session starts inside this folder, read this section first.

Current strongest supported result:

```text
The official v2 runner derives reciprocal PGSPG certificate-pair state from
public N. It resolves the 40-bit rung by reciprocal deadline signature
correction and leaves the 50-bit rung unresolved.
```

Current measured state:

```text
rsa_v2_40bit_static_001 -> resolved_by_reciprocal_deadline_signature_correction
rsa_v2_50bit_static_001 -> unresolved_by_certificate_pair_not_closed
```

Current audit state:

```text
audit factor integrity passes for both rungs;
inference audit passes for 40-bit and fails for 50-bit because 50-bit remains
unresolved.
```

Current implementation contract:

```text
public N -> isqrt(N) orientation -> lower PGSPG certificate
-> reciprocal floor transport -> upper PGSPG certificate
-> reset closure, deadline signature correction, or unresolved
```

Before implementation, read:

- `SESSION_BOOTSTRAP.md`;
- `README.md`;
- `ALGORITHM.md`;
- `PGS_CERTIFICATE.md`;
- `METRICS.md`;
- `docs/research/codex_continuity/START_HERE.md` from the repository root.

Reproduce the current state with:

```bash
python3 build_ladder_fixtures.py
python3 run_experiment.py
python3 audit_experiment.py
pytest -q ../../../tests/python/test_rsa_v2_scripts.py
```

Shape warning:

If the code or prose starts implying that sidecar evidence solved a rung,
say: "Shape feels wrong: a sidecar result is being promoted into inference."

The experiment starts at 40 bits, but every live rule must be compatible with
the RSA-260 path. Do not create a separate toy arithmetic path.

## Goal

Build a PGS Factorizer from the existing PGS Prime Generator machinery.

The current live runner resolves only public reciprocal certificate closures.
It derives reciprocal PGSPG certificate pairs from public `N` and returns
unresolved unless reset closure or deadline signature correction closes.

## Trusted Source Of PGS Concepts

The trusted source of PGS machinery is the PGS Prime Generator, especially:

- search intervals;
- wheel-open offsets;
- exact divisor-count interval state;
- GWR-selected integer structure;
- no-later-simpler-composite ceilings;
- search-interval reset;
- explicit unresolved states;
- downstream audit separation.

Historical RSA experiment code may contain useful algorithmic ideas, but it is
not trusted as an implementation source. Re-derive the useful construct against
this contract before using it.

## Inference Boundary

Inference may use:

- public `N`;
- `isqrt(N)` as orientation;
- PGSPG-derived chamber-reset certificates;
- reciprocal mapping by `N // x`;
- reciprocal reset-deadline transport;
- equality of public transported certificate coordinates.

Inference must not use:

- hidden factors;
- audit factors;
- hand-authored PGS-state rows;
- answer-bearing fixtures;
- factorization APIs;
- primality-test APIs as endpoint sources;
- `gcd` as a selector;
- divisibility by `N` as the contraction method;
- product closure as the contraction method;
- random construction;
- fallback search;
- silent widening or alternate method branches;
- endpoint-walk budgets as solver coverage;
- fixed additive chambers around `isqrt(N)`.

If the PGS contraction does not resolve honestly, return an explicit unresolved
state.

## Ladder Extension Boundary

Rungs are added in `ladder_spec.json`. A rung may add a public `N`, a stable
`case_id`, and a short description.

Audit endpoints belong only in `audit_spec.json`, which is used by the fixture
builder and audit path. The inference runner must not read audit specs or audit
fixtures.

Do not change `run_experiment.py` to accommodate a new bit size. If a rule
change is required, apply it globally and rerun every existing rung.

## Arithmetic Boundary

Use `gmpy2` for factorizer coordinates from the first 40-bit run.

The current exact interval backend is still small-regime. That limitation must
be reported plainly as:

```text
GMP coordinates, small-regime exact interval backend.
```

Do not describe the current runner as RSA-260-ready until the interval backend
itself is GMP-scale.

## Deadline Lock Boundary

The official target is reciprocal certificate closure.

The forbidden pattern is:

```text
scan public candidates -> test product -> call the matching pair PGS
```

The allowed pattern is:

```text
public N -> PGSPG reset certificate -> reciprocal transport
-> opposite-side PGSPG reset certificate -> certificate closure
-> downstream audit certification
```

## Reproducibility Standard

A future session with no chat context must be able to continue the experiment
from the files in this folder and the referenced PGSPG code.

Every script should make its input files, output files, arithmetic path, and
failure state explicit. Every arithmetic operation should have a plain-language
comment explaining what quantity is being computed.

Use LF line endings for Markdown, JSONL, CSV, and plain-text artifacts.
