# High-Scale PGS C99 Generator Requirements

## Purpose

This document defines the requirements for a separate high-scale C99 PGS
generator.

The goal is a command shaped like:

```bash
pgs_cli 10^1233
```

The output must remain PGS-only. The generator must not use Z5DP, Miller-Rabin,
`nextprime`, trial division primality testing, sieve-based prime generation,
ECPP, PARI primality checks, or any other primality oracle to choose the output.

Classical methods may appear only in downstream audit commands.

## Existing Reference Points

The current Python PGS production generator has this contract:

```text
input prime p -> output next prime q
```

The current C Z5DP CLI has a different contract:

```text
input index n -> output probable prime near p_n
```

`z5d_cli` accepts an arbitrary-size decimal integer string. The repository's
big-`n` benchmark scripts expand expressions such as `10^1233` before passing
the decimal value to `z5d_cli`.

The C `prime_generator` parser already accepts strings of the form `a^b` and
plain decimal integers. The high-scale PGS CLI should use that input grammar.

## C Z5DP Implementation Style Guide

The C Z5DP implementation is a useful style reference for high-scale integer
handling:

- Public big-integer entry points receive initialized `mpz_t` output values
  from the caller and accept input as `const mpz_t`.
- The CLI parses the user-supplied decimal input into `mpz_t` immediately,
  checks `mpz_sgn(input) > 0`, and keeps the large value out of fixed-width
  integer types.
- The legacy `uint64_t` Z5DP compatibility APIs are technical debt. The C PGS
  generator should not introduce a parallel fixed-width public API.
- Fixed-width integers remain only where the value is inherently bounded by
  the program structure: loop counters, status codes, array lengths,
  candidate-bound metadata, bit-count metadata, and small committed test
  fixtures.
- The arbitrary-size path sizes MPFR precision from the GMP bit length:

  $$\mathrm{precision} = \max(320, \mathrm{bitlen}(n) + 2048)$$

- Temporary GMP and MPFR values are initialized in the smallest scope that owns
  them and cleared before returning from that scope.
- Decimal output uses GMP formatting or GMP string conversion instead of
  converting through native integer types.
- The build is intentionally narrow: C99-style source, Apple Silicon only,
  Apple Clang, Homebrew GMP/MPFR paths, `-O3 -march=native`, and explicit
  fail-fast platform and dependency checks.

The PGS generator should copy the successful arbitrary-precision engineering
boundaries, not the legacy fixed-width compatibility surface. One major
contract difference remains: Z5DP's off-grid prime refinement calls
`mpz_nextprime`. That call is forbidden in PGS generation. For PGS, GMP is an
arithmetic backend, not a primality oracle.

## Required Contract

The high-scale PGS C99 generator accepts one scale argument:

```text
pgs_cli <SCALE>
```

where `<SCALE>` is either:

- a plain decimal integer;
- an exponent expression `a^b`, such as `10^1233`.

The first production contract is:

```text
scale S -> integer start n -> PGS chamber -> q
```

The emitted prime record is:

```json
{"n": "...", "q": "..."}
```

`n` is the parsed integer start. It is not required to be prime. `q` is the
PGS-selected next-prime endpoint after `n`. The emitted record must not include source labels, confidence fields,
diagnostics, proof objects, audit status, or timing metadata.

Sidecar diagnostics may record:

- the parsed scale;
- the parsed integer start;
- the PGS chamber certificate;
- candidate-bound state;
- unresolved state;
- timing.

The generated stream remains physically minimal.

## Scale-To-Integer Rule

The scale argument is the integer start.

For `pgs_cli 10^1233`, the generator constructs the integer:

```text
1000...000
```

with `1233` zeros. The PGS chamber begins to the right of that integer.

This creates a separate high-scale generator contract:

```text
integer start n -> PGS-selected q
```

No previous-prime recovery, committed anchor table, delta law, or scale-to-prime
construction is required. If the chamber cannot resolve from `n` inside the
supplied bound, generation fails explicitly with no output record.

## Forbidden Generation Calls

The C99 generator path must not call:

- `mpz_nextprime`;
- `mpz_probab_prime_p`;
- OpenSSL `BN_generate_prime`;
- OpenSSL `BN_is_prime*`;
- Miller-Rabin;
- Baillie-PSW;
- Lucas probable-prime tests;
- trial division primality testing;
- sieve-based prime generation;
- Z5DP prediction or refinement;
- Python, SymPy, PARI, Sage, or shell helper prime locators.

GMP may be used for arbitrary-precision integer arithmetic, modular arithmetic,
division, multiplication, comparison, and parsing. GMP must not be used as a
primality oracle in the generator.

## Big-Integer Refactor Requirement

The current Python backend cannot be ported mechanically to `10^1233`.

The current divisor-count helper uses `numpy int64` arrays:

```python
values = np.arange(lo, hi, dtype=np.int64)
```

This cannot represent high-scale integers. The C99 implementation must use
`mpz_t` or another explicit arbitrary-precision integer representation for all
candidate values.

The high-scale generator must not depend on fixed-width integer overflow
behavior. Every candidate value, offset addition, residue computation, divisor
state field, and emitted integer must be valid beyond 64-bit and beyond
128-bit ranges.

## PGS Chamber Requirements

The high-scale generator must preserve the current production chamber
semantics:

1. Start from parsed integer `n`.
2. Build wheel-open candidate offsets to the right of `n`.
3. Maintain PGS search-interval state.
4. Reject candidates closed by composite state.
5. Preserve unresolved semiprime-shadow landmarks as unresolved state.
6. Lock carrier state only after a resolved candidate exists.
7. Apply lower-divisor threat state after lock.
8. Output the first resolved survivor `q`.
9. Fail explicitly if the chamber does not resolve inside the supplied bound.

The high-scale C99 implementation may introduce a new internal representation
of divisor-count state, but it must preserve the endpoint contract:

$$q = B(n, S, w, d(w))$$

where `S` is the local PGS search-interval state used to make the endpoint
choice single-valued.

## Exactness Standard

The generator claim is:

```text
PGS-selected next-prime endpoint from an integer start.
```

The generator must not call an audit backend to choose `q`.

Downstream audit may confirm:

```text
q == nextprime(n)
```

but that check must run after generation and must not feed back into the output.

## CLI Requirements

Minimum CLI:

```bash
pgs_cli 10^1233
```

Optional flags:

```bash
pgs_cli 10^1233 --candidate-bound 4096
pgs_cli 10^1233 --diagnostics diagnostics.json
pgs_cli 10^1233 --audit audit.json
```

The default stdout record is one LF-terminated JSON object:

```json
{"n":"...","q":"..."}
```

Numbers should be emitted as decimal strings at high scale to avoid downstream
JSON integer truncation.

Audit output is a separate file. Diagnostics are a separate file.

## Error Requirements

The generator must fail explicitly for:

- invalid scale syntax;
- unsupported exponent size;
- unsupported scale for the current exact chamber backend;
- unresolved PGS chamber;
- arithmetic allocation failure;
- malformed diagnostics path.

The generator must not silently widen scope, call fallback prime search, or
substitute a non-PGS result.

## Initial C99 File Layout

Proposed new C module:

```text
src/c/high-scale-pgs/
  Makefile
  include/pgs_high_scale.h
  src/pgs_cli.c
  src/pgs_parse.c
  src/pgs_chamber.c
  src/pgs_emit.c
  src/pgs_diagnostics.c
  tests/test_parse.c
  tests/test_integer_chamber.c
```

The initial C99 implementation should not modify the Python production
generator. The Python generator remains the current low-scale production
reference.

## Milestones

### Milestone 1: CLI And Integer Start

- Parse plain decimals and `a^b`.
- Treat the parsed scale as the integer start `n`.
- Emit `{"n":"...","q":"..."}` on success.
- Fail explicitly when the exact chamber backend cannot support the scale.

### Milestone 2: Small-Scale C99 Integer Chamber

- Implement the chamber rule for small integer starts.
- Match `nextprime(n)` under downstream audit for committed small starts.
- Preserve minimal output.
- Add tests for unresolved chambers.

### Milestone 3: Arbitrary-Precision Chamber Arithmetic

- Replace all candidate integer operations with `mpz_t`.
- Compute wheel residues with GMP arithmetic.
- Compute offsets and candidate values without fixed-width truncation.
- Preserve C99 discipline within the Apple Silicon/Homebrew GMP scope. Do not
  add portability fallbacks for other platforms.

### Milestone 4: High-Scale Integer Probe

- Run `pgs_cli 10^1233`.
- If the chamber resolves, emit `{"n":"...","q":"..."}`.
- If it does not resolve, emit no prime record and return an explicit
  unresolved status.
- Run downstream audit separately.

## Open Research Question

The unresolved hard part is the high-scale exact PGS state representation.

At low scale, exact divisor-count state can be computed directly. At `10^1233`,
full exact divisor counts for every candidate in the chamber are not a normal
fixed-cost operation. The high-scale C99 generator must either:

- implement a PGS-valid local state that is sufficient for endpoint selection
  without classical primality testing; or
- report unresolved.

It must not replace the missing PGS state with Miller-Rabin, `nextprime`, Z5DP,
or any other prime-search mechanism.
