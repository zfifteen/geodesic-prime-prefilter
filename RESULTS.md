## Three Headline Results

- **Direct Deterministic Next-Prime Theorem and Leftmost Minimum-Divisor Rule
  (GWR):** as proved in [PROOF.md](PROOF.md), exact divisor counts determine the
  next prime from a known prime `p`, and the divisor-normalization score picks
  exactly the leftmost interior integer with minimum divisor count in every
  prime gap with a nonempty interior.
- **Prime Gap Generative Model v1.0:** on the persistent reduced gap-type
  surface, prime-gap types close to a frozen hierarchical finite-state model
  with a stable `14`-state core.
- **PGS Prime Generator:** the generator outputs one two-key
  `{"p": ..., "q": ...}` record per given prime `p`, keeps diagnostics outside
  the outputted stream, and selects the successor prime `q` from deterministic
  prime-gap-structure chamber state. The production path excludes trial
  division, Miller-Rabin, probabilistic primality tests, sieve-based prime
  generation, fallback prime search, and oracle-style `nextprime` calls inside
  generation. The current production iteration is `v1.1`.

## What This Repository Carries

This repository now carries three visible lines of work:

- the proved direct next-prime theorem and GWR theorem, whose single live proof
  reference is [PROOF.md](PROOF.md);
- the reduced gap-type model and pattern results on the persistent reduced
  surface;
- the PGS Prime Generator and downstream deterministic DNI-based
  predictor and prefilter work.

The Divisor Normalization Identity supplies the score foundation. The direct
deterministic next-prime theorem and the GWR theorem are the proved theorem
foundation. NLSC is an exact closure consequence of GWR and a structural bridge
to the generator. The gap-type model is the second headline prime-gap result.
The PGS Prime Generator is the current operational inferred-prime generator
milestone. The recursive walk and deterministic filter are downstream
deterministic instruments built from the same normalization.

## Novel Structures in This Repository

The repository now carries the following named structures and results:

- **Direct Deterministic Next-Prime Theorem and Leftmost Minimum-Divisor Rule
  (GWR):** exact divisor counts determine the next prime from a known prime
  `p`; inside any prime gap with a nonempty interior, the log-score argmax is
  exactly the leftmost integer with minimum interior divisor count. These are
  the universal theorems proved in [PROOF.md](PROOF.md), the single live proof
  reference.
- **Divisor Normalization Identity (DNI):** `Z(n) = n^(1 - d(n)/2)` is an
  exact arithmetic identity collapsing all primes to `Z = 1.0`.
- **Gap-type catalog / reduced state surface:** the repository defines a
  deterministic reduced gap-type surface and catalogs it through sampled
  windows to `10^18`, with a persistent `14`-state core on the settled
  high-scale surface. See
  [gwr/findings/gap_type_catalog_through_1e18.md](gwr/findings/gap_type_catalog_through_1e18.md)
  and
  [gwr/findings/gap_type_sequence_grammar_findings.md](gwr/findings/gap_type_sequence_grammar_findings.md).
- **Semiprime Wheel Attractor:** the triad
  `o2_odd_semiprime|d<=4`, `o4_odd_semiprime|d<=4`,
  `o6_odd_semiprime|d<=4` is the dominant dynamical object on the persistent
  reduced gap-type surface. See
  [gwr/findings/gap_type_engine_v1_freeze.md](gwr/findings/gap_type_engine_v1_freeze.md).
- **Hierarchical finite-state model:** on the persistent reduced gap-type
  surface, the frozen `v1.0` model combines a `14`-state core grammar, a
  transition-rule layer, and a higher-divisor-triggered long-horizon controller. See
  [docs/releases/prime_gap_generative_engine_v1_0.md](docs/releases/prime_gap_generative_engine_v1_0.md)
  and
  [gwr/findings/gap_type_engine_v1_rulebook.md](gwr/findings/gap_type_engine_v1_rulebook.md).
- **PGS Prime Generator:** the generator outputs exactly `p` and `q`
  for each given prime `p`, with downstream audit and source diagnostics
  outside the outputted stream. Unlike a conventional prime generator, it selects
  the successor prime from the arithmetic consistency of the interval after
  `p`, without trial division, Miller-Rabin, probabilistic primality tests,
  sieve-based prime generation, fallback prime search, or `nextprime` inside
  generation. The current production path has `9588 / 9588` exact PGS outputs
  with `0` failures on `11..100000`, and
  `2816 / 2816` exact PGS outputs with `0` incorrect candidates on the `10^8`
  through `10^18` decade-window validation surface.
- **No-Later-Simpler-Composite (NLSC) condition:** once the GWR-selected integer
  appears, no later interior composite with strictly smaller divisor count
  precedes the next prime. This is an exact corollary of the proved GWR theorem.
  The separate stress surface through `10^18` records zero observed violations.
- **Dominant d=4 arrival reduction:** under square exclusion, the GWR-selected integer
  is exactly the first interior integer with `d(n)=4`. Exact on full scans through
  `2x10^7`.
- **Dynamic cutoff conjecture:** `C(q) = max(64, ceil(0.5 * log(q)^2))` bounds
  the GWR-selected integer offset for the bounded walker. Empirically calibrated through
  `p <= 10^6`. The fixed map `{2:44, 4:60, 6:60}` is falsified at
  `q = 24,098,209`.

