## PGS Prime Generator

The third headline result is the PGS Prime Generator. It outputs one
record for each given prime:

```json
{"p": 89, "q": 97}
```

The outputted stream is deliberately small: exactly `p` and `q`. Source labels,
diagnostics, verification records, and audit results stay outside the generator output.

The current production iteration is
[PGS Inference Generator v1.1](docs/releases/pgs_inference_generator_v1_1_pgs_only.md).

The extraordinary result is not that the PGS Prime Generator is fast.
Conventional prime generation works by scanning candidate numbers and testing
them until one proves prime. The PGS Prime Generator is different. It starts
from a given prime `p`, examines a finite chamber to the right of `p`, and
uses deterministic prime-gap-structure state in that chamber to infer the
successor prime `q`.

The generator treats the gap as a consistency problem:

```text
Which candidate q leaves a valid prime gap interval after p?
```

The key structural discovery is that once the first candidate `q` is forced by
the interval to its left, later candidates are no longer possible successors of
the original `p`. They belong to intervals that begin after `q`. That
distinction turned the remaining not-yet-excluded candidates into evidence
that the gap had already closed.

The generator is now PGS-only. The production generator contains no trial
division, no Miller-Rabin, no probabilistic primality test, no sieve-based
prime generation, no fallback prime search, and no oracle-style `nextprime`
call inside generation. Classical verification remains downstream audit after
generation, not a mechanism for choosing `q`.

The following surfaces validate the bounded production implementation. They are
not theorem boundaries: the exact divisor-count next-prime theorem is proved in
[PROOF.md](PROOF.md).

On the current production generator surface, exact output is preserved and the
PGS selection rule applies exact divisor-count GWR/NLSC search-interval-reset state:

```text
surface: 11..100000
candidate interval width: 128
primes tested: 9588
PGS-labeled outputs: 9588
failed outputs: 0
incorrect candidates: 0
coverage: 100.00%
```

The same production selection rule now reproduces the high-scale decade-window
surface through `10^18`:

```text
surface: 256 consecutive primes per decade, 10^8 through 10^18
candidate interval width: 1024
primes tested: 2816
exact matches: 2816
undecided cases: 0
incorrect candidates: 0
search-window misses: 0
coverage: 100.00%
```

The C high-scale generator also carries a deterministic `10^1233` certificate
path for the integer-start chamber contract.

The implementation contract and lower-level mechanism are recorded in
[Generator Logic Specification](docs/specs/prime-gen/minimal_pgs_generator_logic.md).
The current release note is
[PGS Inference Generator v1.1](docs/releases/pgs_inference_generator_v1_1_pgs_only.md).
The detailed technical note is the
[algorithm report](docs/research/prime_inference_generator/rule_x_consistency_collapse_logic_engine.md),
and the high-scale validation report is
[Decade-Window Validation Report](experiments/rule_x_logic_engine/chamber_reset_decade_ladder_1e8_1e18_a256_b1024/report.md).

