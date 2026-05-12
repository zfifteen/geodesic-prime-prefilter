# Square-Tail Moving-Cover Audit

## Status

Measured moving-cover audit. This is not a proof of the square-tail theorem.

## Finding

The obstruction prefix for the current record nearly covers the full moving
cutoff window by exact residue classes, but it leaves a small deterministic
defect set.

For

```text
r = 424,171,123
```

the full counterexample word length is

```text
floor(C / 2) = 395.
```

The actual obstruction prefix has length `368` and contains `99` distinct
least factors. Each observed least factor `ell` covers exactly one residue
class of offsets:

```text
r^2 == 2m mod ell.
```

Those `99` prefix factor classes cover `385` of the `395` positions in the
full moving cutoff window.

The uncovered offsets are:

```text
738, 740, 750, 756, 758, 762, 770, 776, 782, 786
```

The actual predecessor-prime offset `738` is uncovered by the prefix factor
classes. Two more uncovered offsets are also prime on this record:

```text
756, 758
```

The remaining uncovered composite offsets have least factors:

```text
683, 44971, 8880233, 2689, 503, 4219, 367
```

After adding those seven actual composite-defect least factors to the cover,
the factor set has `106` members and covers `392 / 395` positions. The only
remaining uncovered offsets are the actual prime positions:

```text
738, 756, 758
```

## Audit Artifact

```text
research/04-bounded-compression/output/square_tail_cover_audit_424171123.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_cover_audit.py
```

Run:

```text
python3 research/04-bounded-compression/scripts/square_tail_cover_audit.py \
  --root 424171123 \
  --output research/04-bounded-compression/output/square_tail_cover_audit_424171123.json
```

## Proof Consequence

A complete square-tail counterexample is an exact moving residue cover:

```text
for every 1 <= m <= floor(C / 2), some least factor ell < r satisfies
r^2 == 2m mod ell.
```

The current record shows that the observed prefix factor classes already carry
most of that cover, but the cover fails at the predecessor-prime offset and a
small suffix defect set.

The next proof route is therefore sharper than graph descent:

```text
show that the moving residue cover cannot fill its defect set while preserving
least-factor minimality and the selected-square condition.
```

Equivalently, a hypothetical counterexample must explain the exact injection
of new least factors into every uncovered suffix position before the dynamic
cutoff.

On the current record, the composite suffix defects are absorbed by seven new
least factors, and the remaining obstruction is exactly prime-valued. The
all-scale theorem needs a deterministic reason that this prime-valued defect
cannot disappear on a selected-square branch.
