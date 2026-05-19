# Explanatory Evidence Amendment Meeting

## Task

Design a public-only amendment to the toy v01 candidate-list experiment so we
can understand failures without using private ranks, containment diagnostics,
or hidden-factor positions.

This meeting is not about changing recovery criteria. It is not about scaling.
It is not about private diagnostics.

## Current Result

The certified v01 run recovered 3 of 10 toy semiprimes and missed 7 of 10.

Grok's findings report:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/grok_findings_report.md`

Summary:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/output/toy_v01/summary.json`

## Hard Boundary

The amendment may add only public fields derived before private audit:

- no known-factor rank;
- no hidden-factor containment;
- no private band position;
- no "how close was the true factor";
- no per-missed-case private explanation.

Any explanation must be based on public structure visible before canonical
membership audit.

## Desired Evidence

We need enough public explanatory evidence to distinguish:

- filter too sparse: few distances reach the required depth;
- cap saturation: many candidates reach the required depth but list is capped;
- score concentration: a few high-depth candidates dominate;
- weak differential signal: recovered and missed cases have similar public
  depth distributions;
- scale pressure: reduction increases because the cap dominates, while
  recovery does not improve.

## Requested Deliverable

Produce a concise amendment contract specifying:

- exact public-only fields to add to `public_manifest.json`;
- any optional public sidecar file, if needed;
- unchanged private-audit boundary;
- how to rerun the current toy corpus;
- how Grok will certify the amended runner before execution;
- how findings should be reported without private diagnostics.

Ask exactly one question only if a material design choice remains.
