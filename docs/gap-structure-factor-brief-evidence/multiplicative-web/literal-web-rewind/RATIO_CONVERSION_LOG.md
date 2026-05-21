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

Baseline result after change: passed.

Commit: recorded in final report after commit creation.
