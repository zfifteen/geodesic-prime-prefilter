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

Commit: `04547cdb`.

## Accepted: Supporting-Factor Display Cap

Original constant: `supporting_factors[:16]`.

Role: limits the number of supporting public factors written into each output record.

Ratio formula:

```text
support_preview_count = ceil((8 / 9) * emitted_hole_count)
```

Parameter rationale: `8 / 9` ties support-detail visibility to the emitted public list size. This converts a display cap without changing support counts, sorting, or the public hole list itself.

Baseline result after change: passed. The public hole ranking and exact factor-distance rank-1 recovery were unchanged. The smallest case now truncates one support preview list while retaining the true support count.

Commit: `223a79e5`.

## Accepted: Summary Preview Counts

Original constants: Markdown preview `8`; HTML preview `10`.

Role: limits the number of emitted public holes shown in human-readable reports.

Ratio formulas:

```text
md_preview_count = ceil((4 / 9) * emitted_hole_count)
html_preview_count = ceil((5 / 9) * emitted_hole_count)
```

Parameter rationale: both preview sizes now derive from the emitted public list. The Markdown report remains more compact, while the HTML report shows a slightly larger slice for visual inspection. Neither ratio changes the public ranking or emitted candidate records.

Baseline result after change: passed. All four toy cases still emitted an exact factor-distance offset at rank 1.

Commit: `9a2ae501`.
