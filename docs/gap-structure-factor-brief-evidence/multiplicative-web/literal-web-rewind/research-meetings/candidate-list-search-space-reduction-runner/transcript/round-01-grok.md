# Round 01 Grok

## Restatement Of The Intended Research Shift

The user is deliberately pivoting from the prior sparse top-K CRT web
nomination, which emitted a hard cap of 30 distances and produced compliant
`missed` outcomes on the 128-bit and 256-bit rungs, to a new public `N`-only
runner whose explicit purpose is to quantify search-space reduction.
Triangulation here is a public filter that starts from the large interval of
possible factor-distance positions and applies successive modulus-link closures
over the thread set to emit a drastically smaller, ordered candidate list.

The sole admissible success signal remains post-freeze membership of the true
hidden factor in that list. The primary measured win is the concrete ratio
between the declared public baseline space size and the emitted list
cardinality. All work must begin at toy scales so that the actual reduction
factor can be observed and the list shape refined before any larger claim.

## Proposed Runner Design

Public inputs:

- `--n <N>`;
- `--out-dir <path>`;
- a public pinned policy spec or hardcoded public constants.

Public emitted artifacts:

- `public_output.jsonl`, one candidate distance per line;
- `public_manifest.json`, including `N`, `N_bits`, policy name, thread set,
  `min_depth`, `max_candidates`, original-space definition, emitted count,
  reduction ratio, source SHA, elapsed time, and deterministic scoring key.

Candidate generation mechanism:

- use public thread residues of `N`;
- construct candidate distances by iterative CRT extension;
- retain completed distances satisfying a minimum triangulation depth;
- do not use trial division, `gcd`, candidate divisibility checks, or any
  private factor information.

Triangulation score ingredients:

- primary: triangulation depth;
- secondary: shared thread count;
- then total coverage;
- then deterministic public tie-breaker.

Candidate-list size controls:

- `min_depth`;
- `max_candidates`, for an emitted list in the few-hundreds regime.

Toy-scale measurement surface:

- public `N`-only corpus;
- public runner freezes candidate lists;
- canonical membership checker audits afterward;
- report emitted count, original-space size, reduction ratio, and recovered or
  missed status.

Admissible metrics:

- recovery only if canonical checker reports `recovered`;
- reduction ratio = `original_space / emitted_count`;
- no private rank outside the emitted list.

## Largest Compliance Risk

Grok identified the main compliance risk as pre-freeze oracle influence on
public policy parameters: thread set, `min_depth`, `max_candidates`, scoring
tuple, and original-space formula could be unconsciously tuned using already
known factor outcomes.

## Grok Question

What exact, fixed, public formula for `original_space_size` should the design
contract lock in for the entire toy-scale measurement surface so the ratio
cannot be redefined after seeing emitted counts?
