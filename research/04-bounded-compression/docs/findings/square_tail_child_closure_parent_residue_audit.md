# Square-Tail Child Closure Parent-Residue Audit

## Status

Invalidated proof route.

## Finding

Child closing primes do not directly cover the measured parent windows.

For each composite M-rough parent row, take its least-factor child root. For
each prime-valued M-rough row in that child, use the child closing prime as a
candidate carrier back in the parent square. The induced parent residue is
outside the parent M-window in both measured surfaces.

| Source | Parent `M` | Child closing-prime rows checked | Inside parent `M` |
|---|---:|---:|---:|
| Standing record actual composite rough children | `395` | `664` | `0` |
| Representative actual composite rough tail children | `4444` | `167` | `0` |

## Boundary

The direct back-cover route is false on the measured PGS surfaces:

```text
child prime-valued M-rough defect
-> same prime carrier covers a parent M-rough row inside parent M.
```

The remaining transport target must be a global cascade, a covering
impossibility, or a direct exclusion of all-composite M-rough defects. It is not
the pointwise return of child closing primes into the parent cutoff window.

## Second Opinion

Grok response `06124636-7c99-99e2-b9d6-468bdeac8776` agreed with this
boundary. The zero parent residues inside `M` falsify direct pointwise
back-cover by child closing primes on the measured surfaces. This is real
progress because it removes one concrete ordered transport mechanism and
narrows the remaining routes to global cascade, covering impossibility, or
direct all-composite M-rough exclusion.

The artifact is:

```text
research/04-bounded-compression/output/square_tail_child_closure_parent_residue_audit.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_child_closure_parent_residue_audit.py
```
