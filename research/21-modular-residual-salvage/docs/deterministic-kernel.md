# Deterministic kernel of the salvage

## Purpose

Separate what `@0x2719` packaged as classical density from the deterministic
object that can live under the PGS shape contract.

Prerequisite reading: [background-x-exchange.md](./background-x-exchange.md).

Authoritative formal definitions and implementation mapping:
[FORMAL_DEFINITION.md](./FORMAL_DEFINITION.md) and
`scripts/residual_partition.py`.

## Three layers in the salvage text

| Layer | Content | Kind | Role in PGS |
| --- | --- | --- | --- |
| A. Soft density | "likely / often prime near dense composites" | probabilistic | **Forbidden as inference** |
| B. Trial ladder | "check remaining primes up to sqrt(n)" as the path that chooses primality | classical search | **Audit / comparison only** |
| C. Modular residual partition | primes in the smooth wheel are excluded from neighbors; only a residual set can still kill them | deterministic residual accounting | **Extract and develop** |

Layer C is the kernel. Layers A and B are packaging.

## Objects

### Wheel and smooth carrier

Fix a finite set of primes `W` (a **wheel**).

```text
S = product of primes in W
```

Examples from the salvage:

| W | S |
| --- | ---: |
| `{2, 3, 5}` | 30 |
| `{2, 3, 5, 7}` | 210 |

In the historical z≥4⇒g=2 claim remainder vector, zeros on positions that force
`30 | w` already place the GWR seat on a 30-smooth modular class
(proved modular lemma on `M_v1` in `PROOF.md`).

### Neighbor candidates

```text
n in {S - 1, S + 1}
```

More generally, for a carrier `w` with wheel `W` forced by modular zeros,
the natural next-integer candidate is `e = w + 1` (twin-gap geometry when
`w` is the sole interior).

### Residual set

```text
R(n, W) = { primes r : r <= sqrt(n) and r not in W }
```

Interpretation:

- Every prime in `W` is **already excluded** as a divisor of `n` (for `n`
  larger than those primes), because `n = S +/- 1` is coprime to `S`.
- Only primes outside `W` and at most `sqrt(n)` remain as possible proper
  prime factors of `n`.

That partition is deterministic. It does not assert that `n` is "likely"
prime.

## Empty Residual Modular Certificate (ERMC)

**Rule (deterministic certificate).**

```text
If n > 1 and R(n, W) = empty set, then n is prime.
```

**Reason.** Any proper prime factor of `n` would be `<= sqrt(n)`. Every such
prime is either in `W` (cannot divide `n`) or not in `W` (but then it would
lie in `R`, which is empty). Contradiction. Hence `n` is prime.

No probability. No trial loop. Empty residual forces the state.

### Worked salvage examples under ERMC

| S | n | sqrt(n) approx | R(n, W) | ERMC verdict | Actual |
| ---: | ---: | ---: | --- | --- | --- |
| 30 | 29 | 5 | empty | **prime (closed)** | prime |
| 30 | 31 | 5 | empty | **prime (closed)** | prime |
| 210 | 209 | 14 | `{11, 13}` | **not closed** | composite (`11 * 19`) |
| 210 | 211 | 14 | `{11, 13}` | **not closed** | prime |

What the salvage called "likely" at 30 was actually **modular-closed**: the
wheel covers every prime up to the square root.

What the salvage called "check 11 and 13" at 210 was **residual-open**: the
certificate does not resolve; classical trial is only one way to finish, and
that way is not PGS inference.

### Scale of empty residual on primorials

For primorials `P#k` (product of the first `k` primes), empty residual on
both `P#k +/- 1` holds only in a tiny regime (roughly through `30`). At
`210` and above, residual is nonempty and grows quickly.

**Implication:** ERMC explains the 29/31 twin toy cleanly. It is **not** a
scalable historical z≥4⇒g=2 claim replacement and must not be written as one.

## Residual-open versus modular-closed (PGS state language)

Rewrite Layer C as a state machine:

```text
carrier S from wheel W
  -> candidate n (neighbor or endpoint)
  -> compute residual set R(n, W) as a set description
  -> if R = empty:
         modular-closed under this certificate
         (resolved prime under ERMC)
     if R nonempty:
         residual-open under this certificate
         (unresolved under ERMC; do not trial to finish)
```

| State | Meaning | Allowed next move inside PGS |
| --- | --- | --- |
| modular-closed | residual empty | accept prime under this certificate |
| residual-open | residual nonempty | leave unresolved under ERMC; other named PGS rules may still act |
| invalidated rule | universal claim killed by CE | do not cite as theorem |

**Discipline.** Nonempty residual is **not** an invitation to run trial
division as the generator path. Trial may appear only in audit sidecars or
explicit classical comparison.

## How this relates to historical z≥4⇒g=2 claim and the CE

### Surviving modular fact

On `M = (2, 3, 5, 7, 30, 210, 2310)`:

```text
z(w) >= 4  <=>  30 | w
```

Proved in `PROOF.md`. The salvage's focus on "dense" multiples of small
primes is adjacent to this modular seat, not a replacement for it.

### Why historical z≥4⇒g=2 claim still dies

The invalidated claim was:

```text
z(GWR) >= 4  =>  g = 2
```

That claims a **gap size**, not a residual certificate for a single neighbor.
Even when `30 | w`:

- residual for `w + 1` is usually open at scale;
- GWR may sit on a 30-multiple inside a **larger** gap because of **tau ties**
  (or even unique min; Hypothesis U is also falsified).

### The CE neighborhood kills soft density on contact

```text
w = 17,666,310 = 30 * 588,877
w - 1 = 17,666,309   prime (left gap endpoint)
w + 1 = 17,666,311   composite (13 * 31 * 59 * 743)
```

The salvage's "plus or minus one often prime" fails on the very carrier of the
disproof. Residual accounting predicts openness, not likelihood of twinness.

## Formal sketch (ERMC only)

Let `W` be a finite set of primes, `S = prod(W)`, `n = S + eps` with
`eps in {-1, +1}` and `n > 1`.

1. For every `p in W`, `p` does not divide `n`.
2. Let `R = { r prime : r <= floor(sqrt(n)), r not in W }`.
3. If `R` is empty, then no prime `<= sqrt(n)` divides `n`, so `n` is prime.

This is ordinary elementary number theory. Its value for PGS is **shape**:
it shows how to state a neighbor certificate as residual emptiness without
emitting likelihood.

## What this kernel is not

| Claim | Status |
| --- | --- |
| Universal twin lock from four remainder zeros | **invalidated** |
| Unique tau-min + four zeros implies twin (Hypothesis U) | **falsified** |
| ERMC scales to large primorial twins | **false** (residual opens) |
| Trial up to sqrt is PGS inference | **forbidden shape** |
| Soft density near smooth composites is a PGS law | **outside spine** |

## Status labels for this document

| Object | Status |
| --- | --- |
| ERMC implication (empty residual => prime) | proved as elementary certificate (classical) |
| Residual-open / modular-closed partition language | design object for this chapter |
| Use of residual partition to restore historical z≥4⇒g=2 claim | **invalidated / not adopted** |
| Soft density salvage as inference | **rejected** |

Next: buildable candidates and forbidden paths in
[candidates-and-build-path.md](./candidates-and-build-path.md).
