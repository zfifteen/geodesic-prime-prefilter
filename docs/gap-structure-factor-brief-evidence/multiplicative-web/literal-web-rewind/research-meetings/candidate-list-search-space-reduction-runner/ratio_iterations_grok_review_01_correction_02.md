# Ratio Iteration 01 Correction 02 Review Request

## Task

Re-review the corrected private harness before running iteration 01.

The previous execution attempt exposed a relative-path bug: the harness passed a relative output path into a public subprocess whose working directory is the experiment folder, then attempted to read the manifest from the caller-relative path.

## Correction

File:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/run_ratio_probe_iteration.py`

Correction:

```text
args.out_dir = args.out_dir.resolve()
```

was added once at startup, before creating output directories and before any subprocess call.

New SHA-256:

`38803e341f4eeb38da4dc5db9ec51909a031f74f387ad3ca7053f6cfab1b017c`

`python3 -m py_compile` passes.

The public probe source is unchanged:

`thread_triangulation_ratio_probe.py`

SHA-256:

`8dc166e92045bf0871c5d1069380dd933833c82241185473f0a79960a6e8a594`

## Proposed Iteration 01 Setting Remains

```text
thread_count_ratio = 1/2
depth_ratio = 5/12
retention_divisor = 1024
```

## Requested Output

Return exactly one approval classification:

- `approved_for_iteration_01`
- `not_approved`
- `approved_with_required_corrections`

If approved, state whether the correction preserves the source-separation boundary and whether iteration 01 may run.
