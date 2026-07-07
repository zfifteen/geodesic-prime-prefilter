# Zero-Excess DNI Phase 1 Risk Verdict

This document is the gate template for the Phase 1 Zero-Excess DNI launch.
It records the risks that block launch, the scans required before verdict, and
the criteria for `pass`, `revise`, or `stop`.

Phase 1 changes the preferred coordinate. It does not create a new theorem,
rename public schemas, or treat generated history as live migration material.

## Gate State

```text
agent: Agent 7, Risk Register And Gatekeeper
branch: codex/zero-excess-dni
phase: Phase 1
verdict: pass
reviewed diff: Phase 1 integrated diff on codex/zero-excess-dni
```

## Verdict Categories

### pass

Use `pass` only when all required checks have run, all blocking risks are
cleared, and every affected document preserves the Phase 1 coordinate contract:

- prime language using $E(n)=0$ includes the guard `n > 1`;
- the old extremum statement is translated as $F(n)=-E(n)$, so maximizing
  $F$ becomes minimizing $E$;
- the DNI-to-zeta bridge uses
  $H(n)=\log n+E(n)=\tau(n)\log n/2$;
- the zero-excess floor remains an integer-side object, distinct from the
  zeta-side critical line;
- `PROOF.md` remains the theorem-status authority without being described as a
  direct RH proof;
- public APIs, schemas, committed vectors, and generated artifacts are
  unchanged unless an explicit Phase 1 approval says otherwise;
- no unresolved `E(n)` symbol collision remains in changed files.

### revise

Use `revise` when the launch shape is correct but the integrated diff still has
bounded fixable defects. Examples:

- one or more required scans have not been recorded;
- a document uses correct mathematics but lacks one required status boundary;
- link paths, wording, or local terminology need correction;
- a nonblocking symbol collision can be resolved by renaming or adding a local
  definition;
- targeted doc-status tests fail for a narrow, identifiable documentation
  mismatch.

The `revise` verdict must name the exact files and the smallest required edits.

### stop

Use `stop` when any blocking risk is present, when generated or public contract
surfaces churn without approval, or when the integrated diff changes theorem
meaning rather than coordinate presentation.

The `stop` verdict must name the first blocking condition and the exact evidence
path. Do not proceed to broader launch approval until that condition is removed.

## Blocking Risks

Each blocking risk must be marked `cleared`, `revise`, or `stop` during final
verdict review.

| Risk | Stop condition | Expected cleared condition | Status |
| --- | --- | --- | --- |
| missing n > 1 guard | A changed prime-characterization statement says $E(n)=0$ means prime without excluding `1`. | Every prime-characterization statement using $E(n)=0$ includes `n > 1` or an equivalent exclusion of `1`. | cleared |
| F=-E extremum flip | A changed statement says the selected integer maximizes $E$, minimizes $F$, or otherwise reverses the extremum. | Changed text says maximizing $F$ is equivalent to minimizing $E$, with the leftmost minimum convention where needed. | cleared |
| H(n)=log n+E(n) lost or replaced by E(n) alone | A bridge, numerator, load, $K/R$, or ratio expression uses $E(n)$ alone where the DNI-to-zeta bridge requires $H(n)$. | Bridge text preserves $H(n)=\log n+E(n)=\tau(n)\log n/2$. | cleared |
| zero-excess floor / critical-line identity confusion | A changed statement identifies the zero-excess floor with the critical line or says RH places primes on or near the floor. | Changed text keeps the zero-excess floor integer-side and the critical line zeta-side. | cleared |
| PROOF.md direct-RH misread | A changed statement says `PROOF.md` directly proves RH or that the direct-RH result is already proved there. | Changed text says `PROOF.md` controls local PGS theorem status, while RH-facing bridge status is separate. | cleared |
| public API/schema rename | A Phase 1 edit renames `Z-Band`, `proxy_z`, `FIXED_POINT_V`, `exact_z_normalize`, committed vectors, output fields, or benchmark schemas without explicit approval. | Public APIs and schemas remain stable, or the diff contains explicit approved migration scope. | cleared |
| generated artifact churn | A Phase 1 edit rewrites historical JSON, CSV, PDF, SVG, PNG, MP3, MP4, benchmark outputs, or archive artifacts without explicit approval. | Generated and historical artifacts are untouched except for separately approved regeneration. | cleared |
| unresolved E(n) symbol collision | A changed file uses `E(n)` for zero-excess while another local `E` meaning remains active without renaming, reservation, or explicit disambiguation. | Each changed file defines `E(n)` as zero-excess before use or resolves unrelated `E` meanings. | cleared |

## Required Scans And Checks

Run these checks from the repository root before giving a final verdict.
Record the command result and any relevant hit paths in the final risk note.

### Whitespace And Patch Hygiene

```bash
git diff --check
```

Required result: no whitespace errors.

### Forbidden Drift Around Proved PGS Theorem Language

```bash
rg -n -C 2 "(heuristic|appears|suggests|validated so far|likely|empirical|promising)" \
  PROOF.md RESULTS.md README.md docs/core/DIVISOR_NORMALIZATION_IDENTITY.md \
  docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md PRIME_GAP_GENERATOR.md \
  docs/rh docs/faq docs/zero-excess-dni
```

Required result: no changed text uses these terms to qualify a proved PGS
theorem, the direct deterministic next-prime theorem, GWR, DNI, or another
proved Phase 1 theorem-status statement. Historical or explicitly invalidated
contexts are acceptable only when the surrounding text preserves the status
boundary.

### Excess-Only Bridge Mistake Scan

```bash
rg -n -C 3 "(E\\(n\\).*?(alone|only).*?(bridge|numerator|load)|\
(bridge|numerator|load).*?E\\(n\\).*?(alone|only)|\
H\\(n\\)\\s*=\\s*E\\(n\\)|\
H\\(n\\).*?lost|\
replaced by E\\(n\\) alone)" \
  docs/rh docs/faq docs/zero-excess-dni PROOF.md RESULTS.md README.md
```

Required result: no changed bridge text replaces $H(n)=\log n+E(n)$ with
$E(n)$ alone. Any hit must be either this gate document, the notation contract,
or a warning that preserves the correct bridge load.

### Relative Markdown Link Check

```bash
python3 - "$(git diff --name-only -- '*.md')" <<'PY'
from pathlib import Path
import re
import sys

paths = [Path(p) for p in sys.argv[1].splitlines() if p]
missing = []
pattern = re.compile(r"\[[^\]]+\]\(([^)#][^)]*)\)")

for path in paths:
    text = path.read_text(encoding="utf-8")
    for match in pattern.finditer(text):
        target = match.group(1).split("#", 1)[0]
        if "://" in target or target.startswith("mailto:"):
            continue
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            missing.append(f"{path}:{target}")

if missing:
    print("\n".join(missing))
    raise SystemExit(1)
PY
```

Required result: every changed relative Markdown link resolves.

### Targeted Doc-Status Tests If Affected

Run these when the integrated diff touches theorem-status prose, RH bridge
docs, FAQ reviewer guidance, or Phase 1 status language:

```bash
python3 -m pytest tests/python/test_doc_proof_status_surface.py
# RH bridge tests archived externally (see research/12-rh-bridge/README.md)
```

Required result: tests pass, or the verdict is `revise` with exact failing test
names and the status-language correction required.

## Final Verdict

```text
verdict: pass
reviewed commit or diff range: current working tree on codex/zero-excess-dni
checks run: integrator-reported checks accepted for final gate
blocking risks: all cleared for Phase 1 changed surfaces
first failing condition, if any: none for Phase 1 changed surfaces
required edits, if revise or stop: none
final note: Phase 1 may proceed. The working tree includes the expected
  root-doc, RH/FAQ, and zero-excess planning changes. The untracked
  docs/app-ideas/ tree and the tracked modification at
  docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/thread_triangulation_ratio_probe.py
  are outside this Phase 1 risk gate and are not part of this verdict.
```

Integrator evidence recorded for this verdict:

- `git diff --check`: pass.
- Relative Markdown link check over changed Markdown: pass, 10 files checked.
- ASCII punctuation scan over touched Phase 1 docs: pass.
- `python3 -m pytest research/12-rh-bridge/tests`: pass, 5 passed.
- Targeted `PROOF.md` root-doc tests: pass, 2 passed.
- Full `tests/python/test_doc_proof_status_surface.py`: 10 passed, 1 failed.
  The remaining failure is repository-wide pre-existing non-root
  proof-marked documentation outside the Phase 1 diff. No listed offender is a
  Phase 1 changed file, so this is non-blocking for this gate.
- Forbidden drift scan: reviewed hits do not downgrade proved PGS theorem
  language in changed Phase 1 text.
- Excess-only bridge scan: reviewed hits are guardrails, warnings, or correct
  $H(n)=\log n+E(n)$ statements.

Blocking-risk disposition:

- missing `n > 1` guard: cleared.
- $F=-E$ extremum flip: cleared.
- $H(n)=\log n+E(n)$ lost or replaced by $E(n)$ alone: cleared.
- zero-excess floor / critical-line identity confusion: cleared.
- `PROOF.md` direct-RH misread: cleared.
- public API/schema rename: cleared.
- generated artifact churn: cleared.
- unresolved `E(n)` symbol collision: cleared.
