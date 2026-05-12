# Square-Tail M-Rough Defect Audit

## Status

Measured rough-defect audit. This is not a proof of the square-tail theorem.

## Finding

The square-tail theorem reduces exactly to a prime-valued defect after all
repeat-capable carriers are applied.

For

```text
r = 424,171,123
```

the moving window has

```text
M = floor(C / 2) = 395.
```

A repeat-capable carrier is a prime `ell <= M`. Such a carrier covers every
position

```text
r^2 == 2m mod ell.
```

After all repeat-capable carriers are applied, the remaining positions are the
`M`-rough defect set: values `r^2 - 2m` with no prime factor at most `M`.

For the current record:

| Quantity | Value |
|---|---:|
| Repeat-capable prime carriers `3 <= ell <= M` | `76` |
| Positions covered by repeat-capable carriers | `330 / 395` |
| M-rough defect positions | `65` |
| Prime-valued rough defects | `3` |
| Composite rough defects | `62` |
| Minimum least factor among rough composites | `419` |
| Rough composite least factors all exceed `M` | `true` |

The prime-valued rough defects occur at offsets:

```text
738, 756, 758
```

The first of these is the actual predecessor-prime offset.

Every rough composite in the certificate has least factor greater than `M`.
This is the exact witness that the rough-defect set is the part of the window
left after all repeat-capable carriers have been applied.

## Audit Artifact

```text
research/04-bounded-compression/output/square_tail_rough_defect_audit_424171123.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_rough_defect_audit.py
```

Run:

```text
python3 research/04-bounded-compression/scripts/square_tail_rough_defect_audit.py \
  --root 424171123 \
  --output research/04-bounded-compression/output/square_tail_rough_defect_audit_424171123.json
```

## Proof Consequence

This is the clean non-tautological form of the square-tail problem.

A complete square-tail counterexample is equivalent to:

```text
Every M-rough defect value r^2 - 2m is composite, with least factor greater
than M.
```

Therefore the all-scale theorem is equivalent on the square branch to:

```text
Every selected-square root has at least one prime-valued M-rough defect before
the cutoff.
```

The current record satisfies that statement at three offsets. The proof is
still missing: the artifact identifies the exact deterministic object that
must be forced by reduction, recursion, or elimination.
