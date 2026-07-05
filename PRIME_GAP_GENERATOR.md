# PGS Prime Generator

Most prime generators are candidate testers.

They propose a number and ask whether it is prime. If the number is composite, they reject it and try another. Better generators can make the test faster, or choose candidates more carefully, but the shape is still familiar: propose, test, reject, repeat.

The PGS Prime Generator is built around a different reading of the interval after a known prime.

It starts with one prime `p`. It reads the arithmetic structure to the right of `p`. Its job is to output the successor prime `q` as a minimal record:

```json
{"p": 89, "q": 97}
```

That record says only what matters: start at `89`; the next prime is `97`.

## Why The Output Is So Small

The output stream is deliberately minimal. For each given prime, the generator outputs exactly `p` and `q`.

It does not mix the answer with diagnostics. It does not attach confidence fields. It does not put source labels, audit records, counters, or proof objects into the generated record.

Those things can still exist, but they belong outside the output stream. The generated record itself stays clean:

```json
{"p": 89, "q": 97}
```

This matters because the generator has one job. Given `p`, output the next prime `q`.

## What Makes It Different

Conventional prime generation asks a candidate question:

```text
Is this candidate prime?
```

The PGS Prime Generator asks a gap question:

```text
Where does the interval after p close?
```

That change is the center of the document. The generator is not trying to make an ordinary primality-testing loop sound new. It uses deterministic prime-gap structure in the chamber after `p` to infer the successor prime.

The current generator is the PGS-only `v1.1` production iteration, documented in [PGS Inference Generator v1.1](docs/releases/pgs_inference_generator_v1_1_pgs_only.md).

## The Boundary

The generation step does not choose `q` by trial division.

It does not choose `q` by Miller-Rabin.

It does not choose `q` by a probabilistic primality test.

It does not generate a sieve.

It does not fall back to a conventional prime search.

It does not call `nextprime` inside generation.

Classical checks still matter, but they happen afterward as audit. Audit verifies the generated answer. Audit does not choose the answer.

## The Consistency Picture

The generator treats the interval after `p` as a consistency problem. A proposed endpoint has to leave a valid prime-gap interval behind it.

The structural discovery is that once the first candidate `q` is forced by the interval to its left, later candidates are no longer possible successors of the original `p`. They belong to intervals that begin after `q`. What had looked like unresolved later possibility becomes evidence that the original gap has already closed.

That is the operational form of the same reversal introduced in the README: the numbers after `p` are not random obstacles. They carry the information that tells the interval where to end.

## Structural Foundation

The generator contract is `p -> q` from exact divisor counts. Universal bounded
compression is proved in [PROOF.md](PROOF.md) (2026-07-05): the GWR-selected
witness appears within `max(64, ceil(0.5 * log(q)^2))` of the left endpoint.
The Prime-Square Proximity Theorem closes the square branch at Cramér scale.

This is a proved structural bound on the selected-witness offset. Validation
surfaces below confirm implementation fidelity; they are not theorem boundaries.

## Current Validation Surfaces

The following surfaces validate the bounded production implementation. They are not theorem boundaries. The exact divisor-count next-prime theorem and universal bounded compression are proved in [PROOF.md](PROOF.md).

On the current production generator surface, exact output is preserved and the PGS selection rule applies exact divisor-count GWR/NLSC search-interval-reset state:

```text
surface: 11..100000
candidate interval width: 128
primes tested: 9588
PGS-labeled outputs: 9588
failed outputs: 0
incorrect candidates: 0
coverage: 100.00%
```

The same production selection rule reproduces the high-scale decade-window surface through `10^18`:

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

The C high-scale generator also carries a deterministic `10^1233` certificate path for the integer-start chamber contract.

The implementation contract and lower-level mechanism are recorded in [Generator Logic Specification](docs/specs/prime-gen/minimal_pgs_generator_logic.md). The release note is [PGS Inference Generator v1.1](docs/releases/pgs_inference_generator_v1_1_pgs_only.md). The detailed technical note is the [algorithm report](research/01-generator/docs/rule_x_consistency_collapse_logic_engine.md), and the high-scale validation report is [Decade-Window Validation Report](research/01-generator/output/rule_x_logic_engine/chamber_reset_decade_ladder_1e8_1e18_a256_b1024/report.md).
