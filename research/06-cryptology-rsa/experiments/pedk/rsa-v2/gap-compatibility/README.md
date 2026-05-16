# PEDK Gap Compatibility

## Current Finding

The measured sidecar evidence supports the gap-compatibility hypothesis:

```text
gap-neighborhood(p) x gap-neighborhood(q) -> phased gap(N)
```

The public gap containing `N` is not independent of the gap neighborhoods around
`p` and `q`. The strongest current surface is:

```text
F(p, q) = unordered factor-neighborhood signature
S(N) = reduced_state(gap(N)) @ phase(N inside gap(N))
```

## Canonical Evidence

The canonical evidence path is:

```text
core-evidence/
```

That folder contains the PGS-native experiment, the measured result summary,
the hypothesis document, the preliminary candidate exclusion rule, and the
machine-readable outputs.

The current core corpus has:

```text
semiprime_triple_count = 3834
factor_neighborhood_signature_count = 45
phased_n_state_count = 33
supported_phased_n_state_count = 12
candidate_phased_exclusion_count = 64
factor_phased_neighborhood_signature_count = 483
```

## Design Surface

The next richer corpus shape is documented in:

```text
design/
```

That surface is for future structured neighborhood rows, not current proof.

## Archive

Earlier trial-and-error material is preserved under:

```text
archive/
```

Archive contents are non-canonical. They include exploratory scripts that used
prime APIs, stale first-pass labels, random sampling, generated cache files, and
an invalid placeholder catalog. They remain useful for provenance, but they are
not the evidence chain.

## Status Boundary

The current rule is a candidate sidecar rule. It is not a theorem and not live
PEDK inference.
