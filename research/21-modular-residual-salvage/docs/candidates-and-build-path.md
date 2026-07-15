# Candidates and build path

Prerequisite reading:

- [background-x-exchange.md](./background-x-exchange.md)
- [deterministic-kernel.md](./deterministic-kernel.md)

## Goal

List only objects that keep PGS shape:

```text
object -> invariant -> named rule -> resolved | unresolved | invalidated
```

No "likely", no trial ladder as decision path, no historical z≥4⇒g=2 claim revival.

## Candidate A: Empty Residual Modular Certificate (ERMC)

**Statement.** If `R(n, W)` is empty and `n > 1`, then `n` is prime.

**Status:** elementary deterministic certificate (classical packaging allowed
only as exposition).

**Build value:** taxonomy and teaching; freezes why 29 and 31 are forced at
`S = 30` without probability.

**Non-build:** do not install ERMC as a large-scale twin generator. Residual
opens by `210`.

## Candidate B: Residual-open / modular-closed state (primary chapter object)

**Statement (design).** For a carrier `w` whose modular zeros determine a
wheel `W`, and a candidate endpoint `e` (typically `w + 1`):

```text
R(e, W) empty     =>  modular-closed under residual certificate
R(e, W) nonempty  =>  residual-open under residual certificate
```

**Status:** **hypothesis frame / design object** (not a theorem; not
implemented as generator path yet).

**Build value:** correct shape. Nonempty residual becomes **unresolved under
this certificate**, matching the program's explicit-unresolved contract.

**Required discipline:**

- Do not close residual-open states by trial division inside PGS inference.
- Other proved or named PGS rules may still resolve `e` by different means.
- Audit may use classical tools after the fact.

**Suggested next documentation/experiment steps:**

1. Pin a pure-function definition of `R(e, W)` for `W` derived from the
   remainder-vector zeros actually present on `w` (not a hand-picked
   primorial).
2. Measure, on a stated regime, how often modular-closed occurs for GWR
   carriers with `z(w) >= 4`.
3. Report modular-closed hits as **measured**, never as a restored universal
   twin lock.

## Candidate C: H-210 (deeper modular seat)

**Statement (hypothesis only).**

```text
If GWR w satisfies 210 | w, then g = 2.
```

**Status:** **hypothesis / measured** in the Hypothesis U experiment suite:
zero false positives in the tested regimes of that run. **Not a theorem.**

**Link to salvage:** deeper primorial seat than 30, still modular, still
deterministic as a claim shape (implication, not rate).

**Build value:** natural CE-pressure target in the same adversarial style as
`@0x2719`.

**Risk:** one counterexample kills it. Empty scans do not prove it.

**Source:** `experiments/removed unique-min z4 residual probe

## Candidate D: H-tau16 (tau-strengthened seat)

**Statement (hypothesis only).**

```text
If z(w) >= 4 and tau(w) > 16, then g = 2.
```

**Status:** **hypothesis / measured** (zero false positives in the same
tested regimes). **Not a theorem.**

**Link to salvage / CE family:** bare z4 CEs sit at `tau(w) = 16`
with a large prime cofactor (`30 * large_prime`). Strengthening `tau`
attacks that geometry without probability language.

**Build value:** residual obstruction via divisor count, still PGS-native.

**Source:** same findings file as H-210.

## Candidate E: Explicit non-builds

| Idea | Why not |
| --- | --- |
| Soft density near smooth composites as inference | probabilistic shape |
| Trial primes up to sqrt as generator decision | classical candidate testing |
| Restore historical z≥4⇒g=2 claim via "often twins near 30k" | universal claim invalidated |
| Hypothesis U (unique tau-min + z >= 4 => g = 2) | **falsified** (`p = 156942923`) |
| Promote H-210 or H-tau16 without CE pressure | theorem inflation |

## Relationship diagram

```text
X salvage (classical packaging)
        |
        +-- refuse: density / trial ladder
        |
        +-- extract: residual partition
                |
                +-- ERMC (tiny closed regime)           [Candidate A]
                |
                +-- residual-open state language        [Candidate B]  <-- primary
                |
                +-- deeper seats for CE pressure
                        |
                        +-- H-210                       [Candidate C]
                        +-- H-tau16                     [Candidate D]
```

## Recommended build order

1. **Freeze language** (this chapter): residual-open / modular-closed;
   ERMC as certificate only. **Done** (`FORMAL_DEFINITION.md`).
2. **Specify** how `W` is read from the remainder vector of a concrete `w`
   (Candidate B formalization). **Done** (`wheel_from_carrier` on `M_v1`).
3. **Measure** modular-closed frequency on a pinned regime (measured only).
   **Done** on `[11, 50000)` and broader `[11, 250000)` (see `MEASURED_RESULTS.md`).
4. **Pressure** H-210 and H-tau16 with dedicated CE hunts (same standard as
   historical z≥4⇒g=2 claim: one CE kills universality). **Done** for regime
   `[11, 200000)`: both `not_falsified_in_tested_regime` (hypothesis only).
5. **Optional dynamic wheel** beyond `M_v1`. **Done** as hypothesis API
   (`M_DYNAMIC_HYPOTHESIS`, `moduli_family_from_primes`) + unit tests.
6. **Do not** wire residual trial into the Minimal PGS Generator or any
   inference path. **Standing rule.**

## Acceptance criteria for future work in this folder

A future change is in-shape if and only if:

- claims use theorem / measured / audit / hypothesis / unresolved /
  invalidated labels correctly;
- z4 twin lock remains invalidated;
- no probabilistic words appear as inference ("likely", "often", "usually"
  as decision language);
- classical primality/factor tools stay in audit or comparison roles;
- new positive claims either force a state or return unresolved.

## Immediate non-goals

- Lean formalization of historical z≥4⇒g=2 claim twin lock (withdrawn).
- Public packaging of H-210 as proved.
- Re-opening classical density as "what PGS still has."

## Pointers

| Item | Path |
| --- | --- |
| Invalidated historical z≥4⇒g=2 claim | `PROOF.md` |
| CE verify | `research/01-generator/tests/test_mod30_adjacent_carrier_generator.py` |
| Hypothesis U findings | `experiments/removed unique-min z4 residual probe |
| Live status for this track | [STATUS.md](./STATUS.md) |
