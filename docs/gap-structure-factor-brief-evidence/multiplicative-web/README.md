# Multiplicative Web Probe

This folder contains a deterministic visualization probe for the fresh
factor-web perspective.

The probe draws composites near a public semiprime `N = p q`, factors those
nearby composites exactly, and connects each composite to its prime-factor
threads. Shared factor nodes become visible intersections. When the known audit
factors `p` and `q` appear in those threads, the graph marks them as connections
back to the factor neighborhoods.

## Boundary

This is a visualization and audit surface. It is not live PGS inference, not a
factor resolver, and not a proof that the web uniquely determines `p` and `q`.

The purpose is to make the proposed object inspectable:

```text
composites near N -> exact factor threads -> shared intersections -> factor-gap neighborhoods
```

## Reproduce

```text
python3 plot_multiplicative_web.py --p 43 --q 59 --radius 70 --out-dir output/toy_43x59_r70
```

Outputs:

- `web.svg` - visual multiplicative web
- `graph.json` - nodes, edges, factors, and audit metadata
- `summary.md` - compact measured summary

## Reciprocal Shadow Vote Probe

Run the first holdout test of the indirect-web hypothesis:

```text
python3 reciprocal_shadow_vote_probe.py
```

Output:

```text
output/reciprocal_shadow_vote_probe/
```

Finding:

```text
RECIPROCAL_SHADOW_VOTE_FINDING.md
```

## 48-Bit Ladder

Run the fixed-radius candidate-walk ladder through 48-bit semiprimes. This is
retained as a boundary measurement, not factor-selection evidence:

```text
python3 reciprocal_shadow_vote_ladder_48.py
```

Output:

```text
output/reciprocal_shadow_vote_ladder_48/
```

## Invalidated 64-Bit New Rungs

The first 64-bit new-rung script is retained as invalidated audit evidence.
It must not be cited as inference evidence because it used the hidden audit
factor `p` as the lower bound of the candidate stream.

```text
python3 reciprocal_shadow_vote_ladder_64_new_rungs.py
```

Output:

```text
output/reciprocal_shadow_vote_ladder_64_new_rungs/
```

Invalidation note:

```text
INVALIDATED_64_BIT_NEW_RUNGS.md
```

## Blind Restart

Run the replacement blind ladder. This uses `p` and `q` only for case
construction and final audit, but it remains a numeric candidate walk:

```text
python3 reciprocal_shadow_vote_blind_restart.py
```

Output:

```text
output/reciprocal_shadow_vote_blind_restart/
```

Boundary note:

```text
BLIND_RESTART_BOUNDARY.md
```
