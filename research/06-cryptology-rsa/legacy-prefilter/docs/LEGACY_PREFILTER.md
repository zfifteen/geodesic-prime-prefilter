# Legacy Prefilter

The current center of the repository is the PGS prime generator. The prefilter is different. It is a legacy downstream engineering path built from the same normalization program.

Its setting is cryptographic prime generation.

Cryptographic prime generation spends a great deal of time on candidates that are composite. Those candidates do not need the full probable-prime path if a deterministic table check can reject them earlier.

The legacy prefilter uses the fixed-point separation suggested by the Divisor Normalization Identity as an engineering target. Under the exact identity, confirmed primes live at `Z = 1.0`, while composites fall below that value. The runtime prefilter is not an exact divisor-count evaluator. It is a bounded deterministic surrogate calibrated against that invariant target.

## Deterministic Filter Performance

Because confirmed primes live at $Z = 1.0$ under the exact DNI and composites contract below it, the filter creates a structural separation in normalized space. That separation makes it possible to reject many candidates before paying the full cost of primality testing on the remaining candidates.

Empirically, this extracted Python path produced:

- $2.09\times$ end-to-end speedup across $300$ deterministic $2048$-bit RSA keypairs
- $2.82\times$ end-to-end speedup across $50$ deterministic $4096$-bit RSA keypairs
- $90.97\,\%$ to $91.07\,\%$ Miller-Rabin reduction in the current covered-table configuration

Those numbers are the production consequence of the same invariant program carried through a narrow deterministic runtime path. The prefilter rejects many doomed candidates before Miller-Rabin.

See [benchmarks.md](benchmarks.md) and [technical-note/technical_note.md](../technical-note/technical_note.md).

## Production Filter Path

The exact DNI depends on exact divisor count. That exact path is valuable as the derivation and as the oracle, but it is not the runtime path for cryptographic-scale key generation.

The production implementation therefore uses a deterministic surrogate with the same invariant target:

- generate deterministic odd candidates from a SHA-256 namespace/index stream
- reject immediately when a concrete factor appears in the gated prime tables
- keep candidates that survive table rejection on the locus convention `proxy_z = 1.0`
- run fixed-base Miller-Rabin on those remaining candidates
- apply final `sympy.isprime` confirmation in the current Python path

In this legacy path, `proxy_z = 1.0` means only that the candidate survived the current gated factor tables and therefore advances to Miller-Rabin. It is not a primality proof by itself.

The current measured rejection rate comes from the covered prime-table depth of this implementation. The repository includes deterministic table-depth sweeps to show that dependence directly rather than attributing the `~91%` figure to runtime exact DNI evaluation.

## Empirical Results

### End-to-End RSA Key Generation

- $2048$ bits, $300$ deterministic keypairs: baseline $291938.126792$ ms; accelerated $139942.831833$ ms; speedup $2.09\times$; Miller-Rabin reduction $90.97\,\%$
- $4096$ bits, $50$ deterministic keypairs: baseline $757750.922792$ ms; accelerated $268557.631625$ ms; speedup $2.82\times$; Miller-Rabin reduction $91.07\,\%$

### Candidate-Loop Screening

- $2048$-bit control corpus: proxy rejection $91.02\,\%$; pipeline speedup $2.95\times$
- $4096$-bit control corpus: proxy rejection $91.41\,\%$; pipeline speedup $3.33\times$

### DNI Calibration

- $29/29$ calibration primes stayed on $Z = 1.0$
- $0$ composite false fixed points

### Exact Raw Composite Z Score Values

This is a separate exact score-function concern from the production filter.

Up to $10^6$ on the natural number line, the strongest exact raw composite $Z$ value inside a prime gap lands at edge-distance $2$ in $43.6006\%$ of gaps versus an exact within-gap baseline of $22.1859\%$, and is carried by a $d(n)=4$ composite in $82.9027\%$ of gaps versus a baseline of $20.1401\%$.

[PROOF.md](../../../../PROOF.md) proves the direct deterministic next-prime theorem and sharpens that ridge picture into the current selected integer theorem: the log-score maximizer is the arithmetic choice “minimize interior divisor count, then take the leftmost integer.” The theorems are universal. The tested surfaces provide certification and provenance.

The dedicated closure study then strengthens the right-edge reading further: on the current documented even-band ladder through $10^{18}$, once the selected integer appears, no later strictly simpler composite is observed before the next prime closes the gap.

See [raw_composite_z_gap_edge.md](../../../11-gap-ridge/docs/gap_ridge/raw_composite_z_gap_edge.md), [PROOF.md](../../../../PROOF.md), and [closure_constraint_findings.md](../../../02-gwr-dni/docs/closure_constraint_findings.md).

See [benchmarks.md](benchmarks.md) for the curated benchmark summary and [manual_validation.md](manual_validation.md) for the exact reproduction commands.
