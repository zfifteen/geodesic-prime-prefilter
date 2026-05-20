# Ratio Replacement Constants Review

## Context

The active v01.1 thread-triangulation runner still contains three hard controls that shape scale behavior:

- `THREAD_SET`: fixed first 12 odd primes;
- `MIN_DEPTH`: fixed depth threshold of 5;
- `MAX_CANDIDATES`: fixed public candidate cap of 512.

The user asked to review replacing these constants with ratios. The meeting reviewed the proposal with Grok under the public-state-only boundary: no hidden `p/q`, no `gcd`, no `N % candidate`, no factor APIs, no primality APIs, no randomness, no product closure, and no post-freeze tuning.

## Participants

- Codex: facilitator and final proposal owner.
- Grok CLI: adversarial reviewer.

## Grok Opening Objection

Grok initially objected to scaling the thread alphabet because a variable alphabet changes depth comparability across cases and risks computational explosion in the recursive CRT extension tree. Grok initially proposed keeping the 12-thread alphabet fixed while replacing depth and candidate cap with ratio-derived values.

## Codex Objection To Grok

Codex rejected two parts of Grok's first proposal:

- fixed absolute floors and ceilings such as `ABS_FLOOR = 256` and `ABS_CEIL = 16384`, because they reintroduce hard constants and recreate cap failure;
- a permanently fixed 12-thread alphabet, because it leaves the largest evidence-budget constant untouched.

## Convergence

Grok concurred that, under the user's stated goal, v02 should reject fixed floors, fixed ceilings, and a permanently locked 12-thread alphabet.

The agreed rule is to keep the triangulation mechanism unchanged while deriving the evidence budget and output budget from public ratios.

## Final Proposal

Locked public ratio constants:

```text
RETENTION_DIVISOR = 1024
THREAD_COUNT_RATIO = 3/8
DEPTH_RATIO = 5/12
```

Public stream:

```text
thread_stream = the ordered odd primes beginning 3, 5, 7, 11, ...
```

Per-N formulas:

```text
active_thread_count = ceil((3/8) * public_radius(N).bit_length())
thread_set = first active_thread_count entries from thread_stream
min_depth = ceil((5/12) * active_thread_count)
max_candidates = ceil(original_space_size(N) / 1024)
```

No absolute floor. No absolute ceiling.

## Scope Boundary

The v02 scaling corpus should use a derived scope boundary, not an arbitrary bit-size floor.

Require:

```text
min_depth >= 3
```

Under the agreed formulas this is equivalent to:

```text
active_thread_count >= 5
public_radius(N).bit_length() >= 11
```

Cases below that boundary belong in a separate toy-calibration surface, not in the v02 scaling corpus.

## Required Manifest Fields

Every public manifest must emit:

- `public_radius`;
- `original_space_size`;
- `retention_divisor`;
- `thread_count_ratio`;
- `depth_ratio`;
- `active_thread_count`;
- concrete `thread_set`;
- computed `min_depth`;
- computed `max_candidates`;
- the seven v01.1 explanatory fields.

## Computational Risk

The current recursive CRT extension tree branches by active thread count. `THREAD_COUNT_RATIO = 3/8` keeps the next 64-bit surface feasible with roughly 13 active threads. Larger N may require either ratio adjustment under a new frozen contract or a more efficient implementation that preserves the exact same public derivation.

## Decision

The clean v02 proposal to show the user is:

```text
Replace the fixed 12-thread alphabet, fixed depth 5, and fixed candidate cap 512 with public ratio formulas. Keep the triangulation mechanism unchanged. Do not add absolute floors, absolute ceilings, fallback paths, or private audit influence.
```
