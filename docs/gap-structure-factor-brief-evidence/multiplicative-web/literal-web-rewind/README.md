# Literal Web Rewind

## Current Reset

The active research path has been rewound to the literal multiplicative web.

Read `REWIND_TO_LITERAL_WEB.md` before modifying or extending this branch. It parks the ratio candidate-list detour and defines the current success boundary: public web evidence must emit the exact offset `p` or `q` before audit labels are read.

## Finding

The literal web object has signal before any residue compression is introduced.

In four toy semiprime cases, direct rows containing the audit factors `p` or `q` were held out. Public factor threads from the remaining rows still pointed to missing offsets. The top supported missing offsets were overwhelmingly the held-out `p` and `q` thread rows:

| case | direct rows | supported direct rows | direct hits in top 18 holes |
| --- | ---: | ---: | ---: |
| toy_23x31 | 24 | 24 | 18 |
| toy_43x59 | 20 | 20 | 18 |
| toy_61x83 | 18 | 18 | 18 |
| toy_89x113 | 18 | 18 | 18 |

This does not prove factor discovery. It restores the original object: factor threads, their missing slots, and their intersections. The next valid target is a blind rule that identifies the hidden-thread hole pattern without audit labels.

## Artifacts

- `literal_web_hole_trace.py`: deterministic experiment script.
- `literal_web_hole_trace_ladder.py`: scale ladder for the same method.
- `index.html`: compact visual report.
- `output/summary.md`: measured table and per-case notes.
- `output/literal_web_hole_trace.json`: full case records.
- `output/top_holes.jsonl`: supported missing offsets.
- `output/literal_web_hole_trace_ladder/summary.md`: scale ladder result.

## Scale Ladder

The scale ladder keeps the same literal method and uses `radius = 6 * p`, because the visible hidden-thread holes first appear at offsets that are multiples of `p` and `q`.

Result: the signal held through every rung that was run, up to `8009 x 10007` with radius `48054`.

Stop: the next rung, `9001 x 11003`, requires radius `54006`, exceeding the current `MAX_RADIUS = 50000`. This is a feasibility stop, not a pattern failure. The literal method works in the tested range, but it currently scales by widening the composite-factorization window linearly with `p`.

## Boundary

This experiment uses `p` and `q` only to create audit holdout labels. It does not use modular ranking, residue certificates, candidate walks, prime streams, or divisibility gates against `N` to infer a factor.
