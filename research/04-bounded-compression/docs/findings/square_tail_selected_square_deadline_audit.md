# Square-Tail Selected-Square Deadline Audit

## Status

Audit evidence. Not a proof.

## Finding

The selected-square condition supplies a broad deadline, not the dynamic
cutoff.

For a prime root `r`, let `s` be the previous prime root. The selected-square
condition is

```text
s^2 < P(r^2) < r^2.
```

In offset form, this says

```text
r^2 - P(r^2) < r^2 - s^2.
```

The right-hand side is the selected-square deadline. It can be much larger
than the dynamic cutoff.

| Root | Previous-root gap | Actual offset | Dynamic cutoff | Selected-square deadline |
|---:|---:|---:|---:|---:|
| `424171123` | `30` | `738` | `790` | `25450266480` |
| `89726961223544427015292389839` | `112` | `338` | `8889` | `20098839314073951651425495311392` |

For the standing record, the selected-square deadline is about
`32,215,527` times the dynamic cutoff. For the CRT representative, it is about
`2.26e27` times the dynamic cutoff.

## Boundary

Selected-square membership proves that a prime appears before the previous-root
square deadline. It does not by itself put that prime inside the dynamic cutoff.

The missing theorem remains the short-tail statement:

```text
selected-square root
-> at least one prime-valued M-rough row before the dynamic cutoff.
```

## Second Opinion

Grok response `a0cc47fb-af0f-fad2-8abb-196d89de80d1` agreed with this
boundary: selected-square membership supplies the deadline `r^2 - s^2`, and
does not by itself supply the dynamic cutoff. The next proof target is the
deterministic coupling between selected-square root state and M-rough row
elimination inside the short window.

The artifact is:

```text
research/04-bounded-compression/output/square_tail_selected_square_deadline_audit.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_selected_square_deadline_audit.py
```
