# Literal Web Ratio Conversion Log

## Baseline

Starting point: the rewound literal-web runner used hard-coded toy radii and fixed output preview counts.

Baseline command set:

```text
python3 -m py_compile docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/literal_web_hole_trace.py
python3 docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/literal_web_hole_trace.py
```

Baseline result: all four toy cases passed. Each case emitted an exact factor-distance offset at public rank 1, and every direct held-out row had public support.

## Accepted: Toy Case Radii

Original constant: per-case hard-coded `radius`.

Role: selects the public composite window around `N`.

Ratio formula:

```text
radius = ceil((1 / 18) * N)
```

Parameter rationale: `1 / 18` is public and depends only on `N`. It keeps the window large enough to preserve rank-1 exact factor-distance recovery on all four toy cases while removing the per-case manually chosen radii.

Baseline result after change: passed. The four toy radii became `40`, `141`, `282`, and `559`; each case still emitted an exact factor-distance offset at rank 1.

Commit: `90cee3e7`.

## Accepted: Emitted Hole Count

Original constant: `top_holes = holes[:18]`.

Role: sets the number of public supported holes emitted for audit.

Ratio formula:

```text
emitted_hole_count = ceil((1 / 20) * radius)
```

Parameter rationale: `1 / 20` derives the output size from the public inspected window. It keeps the candidate list small at toy scale while making the emitted list grow when the visible web window grows.

Baseline result after change: passed. The four emitted public list sizes became `2`, `8`, `14`, and `20`; each case still emitted an exact factor-distance offset at rank 1.

Commit: recorded in final report after commit creation.
