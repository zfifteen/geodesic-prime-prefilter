# Literal Web Ratio Rules

This file records the active ratio rules used by `literal_web_hole_trace.py`.

The ratios below are current method parameters. They are not a changelog.

## Radius

Formula:

```text
radius = floor(sqrt(N))
```

Ratio form:

```text
radius = floor((1 / 1) * sqrt(N))
```

Rationale: for a semiprime `N = p * q` with `p <= q`, the smaller factor satisfies `p <= sqrt(N)`. The factor-thread offsets at `N - p` and `N + p` therefore lie inside the public window `[-floor(sqrt(N)), floor(sqrt(N))]` without using `p` or `q`.

This is the full public first-factor coverage window. Smaller radii should be treated as later compression experiments, not as the baseline rule.

## Emitted Hole Set

Formula:

```text
max_support = maximum support count over all public holes
support_ratio(hole) = support(hole) / max_support
emit hole if support_ratio(hole) = 1
emitted_hole_count = count(emitted holes)
```

Rationale: the emitted set is the strongest public support shell. The web determines the output size by its own support distribution instead of receiving a fixed top-k budget or a fitted fraction of the window.

This rule uses only public thread evidence. A later failure means the strongest support shell did not isolate a factor-thread offset; it is not a candidate-cap failure.

## Supporting Factor Retention

Formula:

```text
support_detail_ratio(hole) = emitted_supporting_factors(hole) / total_supporting_factors(hole)
support_detail_ratio(hole) = 1
```

Implementation rule:

```text
supporting_factors = all public supporters for the emitted hole
support_truncated = false
```

Rationale: supporting factors are public evidence. Since the emitted hole set is already restricted to the max-support shell, the raw artifact should retain the complete public thread support for every emitted hole. If later displays need shortening, that belongs in presentation rendering, not in the evidence record.

## Report Emission

Formula:

```text
report_detail_ratio = displayed_emitted_holes / total_emitted_holes
report_detail_ratio = 1
```

Implementation rule:

```text
Markdown report shows every emitted hole.
HTML report shows every emitted hole.
```

Rationale: the emitted hole set is already the strongest public support shell. Human-readable reports should display the complete public nomination set instead of applying a second arbitrary preview filter.

## Marker Size

Formula:

```text
marker_radius = axis_height / 8
```

Rationale: marker size is display geometry, not inference. The report currently shows only the max-support shell, so every displayed hole has support ratio `1`. The marker size therefore derives from the SVG axis height instead of hard-coded support pixels.

## Current Toy Result

Current runner output:

| case | N | radius | emitted holes | first exact factor offset |
| --- | ---: | ---: | ---: | --- |
| `toy_23x31` | 713 | 26 | 1 | rank 1, `-23` |
| `toy_43x59` | 2537 | 50 | 1 | rank 1, `43` |
| `toy_61x83` | 5063 | 71 | 1 | rank 1, `61` |
| `toy_89x113` | 10057 | 100 | 1 | rank 1, `89` |

Verification commands:

```text
python3 -m py_compile docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/literal_web_hole_trace.py
python3 docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/literal_web_hole_trace.py
```
