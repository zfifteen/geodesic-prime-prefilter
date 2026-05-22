# Zero-Excess DNI Phase 2 Risk Verdict

This document gates the Phase 2 RH and FAQ prose migration.

Phase 2 updates the broad reviewer-facing explanation. It does not change
theorem claims, runtime code, public APIs, committed vectors, generator output,
or historical artifacts.

## Gate State

```text
agent: Integrator plus Risk Gatekeeper
branch: codex/zero-excess-dni
phase: Phase 2
verdict: pass
reviewed diff: Phase 2 integrated diff on codex/zero-excess-dni
```

## Phase 2 Scope

In scope:

- RH bundle narrative pages under `docs/rh/`;
- FAQ core-frame pages;
- FAQ zeta-compression pages;
- FAQ category-error, exact-arithmetic, local/global, analogy, and reviewer
  guidance pages;
- one new FAQ page for the zero-excess floor / critical-line distinction.

Out of scope:

- runtime code;
- tests, except for status checks run by the integrator;
- public API names and vector schemas;
- generated, historical, binary, archive, and benchmark artifacts;
- `docs/app-ideas/`;
- unrelated Grok experiment files.

## Blocking Risks

| Risk | Stop condition | Expected cleared condition | Status |
| --- | --- | --- | --- |
| missing `n > 1` guard | A page says $E(n)=0$ characterizes primes without excluding `1`. | Prime-zero statements include `n > 1` or explicitly exclude `1`. | cleared |
| bridge load drift | A page uses $E(n)$ alone as the DNI-to-zeta numerator. | Bridge pages preserve $H(n)=\log n+E(n)=\tau(n)\log n/2$. | cleared |
| source/compression identity confusion | A page identifies the zero-excess floor with the critical line. | Pages say the floor is integer-side and the critical line is zeta-side. | cleared |
| proof-status drift | A page treats Zero-Excess DNI as a new theorem or says `PROOF.md` directly proves RH. | Pages label zero-excess as exact coordinate reformulation and keep `PROOF.md` local. | cleared |
| theorem downgrade | A page describes proved local PGS theorems as heuristic, empirical, likely, suggestive, or validated only by tests. | Proved local theorem status remains direct. | cleared |
| API/schema/artifact churn | Phase 2 touches code, vectors, generated artifacts, or unrelated experiment files. | Phase 2 diff is documentation-only and scoped to RH/FAQ/zero-excess docs. | cleared |

## Required Checks

Run before verdict:

```bash
git diff --check
```

```bash
rg -n -C 2 "(heuristic|appears|suggests|validated so far|likely|empirical|promising)" \
  docs/rh docs/faq docs/zero-excess-dni
```

```bash
rg -n -C 3 "(E\\(n\\).*?(alone|only).*?(bridge|numerator|load)|\
(bridge|numerator|load).*?E\\(n\\).*?(alone|only)|\
H\\(n\\)\\s*=\\s*E\\(n\\)|\
zero-excess floor is the critical line|\
critical line is the zero-excess floor|\
RH places primes close)" \
  docs/rh docs/faq docs/zero-excess-dni
```

```bash
python3 -m pytest research/12-rh-bridge/tests
```

If theorem-status prose changes, also run the targeted root-proof status tests:

```bash
python3 -m pytest \
  tests/python/test_doc_proof_status_surface.py::test_root_proof_uses_conventional_language \
  tests/python/test_doc_proof_status_surface.py::test_root_proof_contains_standalone_threshold_classification
```

Run a relative Markdown link check over changed Markdown files.

## Final Verdict

```text
verdict: pass
reviewed commit or diff range: current working tree on codex/zero-excess-dni
checks run: Phase 2 gate checks listed below
blocking risks: all cleared for Phase 2 changed surfaces
first failing condition, if any: none for Phase 2 changed surfaces
required edits, if revise or stop: none
final note: Phase 2 may proceed to commit. The out-of-scope Grok experiment
  files and docs/app-ideas/ are excluded from this verdict.
```

Integrator evidence recorded for this verdict:

- `git diff --check`: pass.
- Relative Markdown link check over changed and new Markdown files, excluding
  `docs/app-ideas/`: pass, 33 files checked.
- Stale-coordinate scan over `docs/rh` and `docs/faq`: pass for
  `Z = 1.0`, `Z=1.0`, `raw-Z`, `fixed-point locus`, `zero line`, critical-line
  identity phrases, `RH places primes close`, and `H(n)=E(n)`.
- Forbidden-drift scan: reviewed hits are guardrails, ordinary prose uses, or
  existing bounded-status language; no changed Phase 2 text downgrades proved
  local PGS theorems.
- Excess-only bridge scan: reviewed hits are warnings or correct statements
  preserving $H(n)=\log n+E(n)$.
- `python3 -m pytest research/12-rh-bridge/tests`: pass, 5 passed.
- Targeted doc-status/root-proof tests:
  `test_non_root_proof_marked_markdown_declares_status`,
  `test_root_proof_uses_conventional_language`, and
  `test_root_proof_contains_standalone_threshold_classification`: the two
  root-proof tests passed; the non-root proof-status test still fails only on
  pre-existing research documents outside the Phase 2 diff after the changed
  FAQ proof-marked pages were given explicit proof-status declarations.

Blocking-risk disposition:

- missing `n > 1` guard: cleared.
- bridge load drift: cleared.
- source/compression identity confusion: cleared.
- proof-status drift: cleared.
- theorem downgrade: cleared.
- API/schema/artifact churn: cleared for the Phase 2 staged set.
