# Formal residual partition

Status labels in this document follow the repository contract:
**theorem / measured / audit / hypothesis / unresolved / invalidated**.

This note freezes the mathematical objects implemented in
`scripts/residual_partition.py`. It does not restore Super-Signal.

## Fixed modulus vector

```text
M_v1 = (2, 3, 5, 7, 30, 210, 2310)
```

This is the Super-Signal remainder vector from `PROOF.md`. It is a fixed
implementation constant for this chapter, not a claim that Super-Signal is
proved.

**Proved (elsewhere):** on `M_v1`,

```text
z(w) >= 4  <=>  30 | w
```

where `z(w)` counts zeros in the remainder vector of `w` modulo each entry of
`M_v1`. See `PROOF.md` section Twin-Prime Resonance (modular lemma survives;
universal twin lock is **invalidated**).

## Remainder vector and zero count

For integer carrier `w` and moduli tuple `M = M_v1`:

```text
R_vec(w) = (w mod m)_{m in M}
z(w)     = |{ m in M : w mod m = 0 }|
```

## Wheel from modular zeros

**Definition (wheel).** Let `w` be a carrier. For each modulus `m in M` with
`m | w`, adjoin every prime factor of `m` to a set `W(w)`:

```text
W(w) = union { prime factors of m : m in M and m | w }
```

Call `W(w)` the **wheel** induced by remainder zeros of `w` on `M`.

**Examples.**

| w | zeros force | W(w) |
| ---: | --- | --- |
| 30 | 2,3,5,30 | `{2,3,5}` |
| 210 | 2,3,5,7,30,210 | `{2,3,5,7}` |
| 2310 | 2,3,5,7,30,210,2310 | `{2,3,5,7,11}` |
| 17,666,310 | 2,3,5,30 (z=4) | `{2,3,5}` |

## Residual set

For a candidate integer `n > 1` and wheel `W`:

```text
R(n, W) = { r prime : r <= floor(sqrt(n)) and r not in W }
```

`R(n, W)` is a pure set description. Membership of residual primes in the
factorization of `n` is **not** part of the residual-state decision. Checking
whether some `r in R` divides `n` is classical audit only.

## Residual state

```text
if n <= 1:
    state is undefined for ERMC (implementation returns residual-open)
elif R(n, W) = empty:
    modular-closed
else:
    residual-open
```

| State | Meaning | PGS action under this certificate |
| --- | --- | --- |
| modular-closed | residual empty | resolved prime under ERMC |
| residual-open | residual nonempty | **unresolved** under ERMC |

## Empty Residual Modular Certificate (ERMC)

**Theorem (elementary; classical packaging).**  
Let `W` be a finite set of primes, `n > 1`, and suppose every prime
`p <= floor(sqrt(n))` lies in `W`. Suppose further that no prime of `W`
divides `n` (as holds for neighbors of a multiple of all primes in `W`).
Then `n` is prime.

**Operational form used here.**  
If the carrier `w` is divisible by every prime in `W(w)`, and the candidate is
`n = w +/- 1` (so no prime of `W(w)` divides `n` when `n > max(W(w))`), and
`R(n, W(w))` is empty, then `n` is prime.

**Status:** elementary certificate. **Not** a Super-Signal replacement. Empty
residual occurs only in a tiny regime for primorial-scale wheels (notably
`S = 30` for both neighbors).

## Forbidden shapes (not part of the formal system)

| Shape | Status |
| --- | --- |
| "likely / often prime near dense composites" | outside spine (probabilistic) |
| Trial residual primes to choose the PGS output | outside spine (classical inference) |
| `z(GWR) >= 4 => g = 2` as universal law | **invalidated** |
| H-210 / H-tau16 as theorems | **hypothesis / measured only** |

## Implementation mapping

| Formal object | Function in `scripts/residual_partition.py` |
| --- | --- |
| `M_v1` | `M_V1` |
| Optional extended family | `M_DYNAMIC_HYPOTHESIS` (**hypothesis only**) |
| Dynamic family from primes | `moduli_family_from_primes` (**hypothesis only**) |
| Family validation | `normalize_moduli_family` |
| `R_vec`, `z` | `remainder_vector`, `zero_count` |
| `W(w)` | `wheel_from_carrier` (optional `moduli=`) |
| `R(n, W)` | `residual_set` |
| closed / open | `residual_state` |
| package for `w` and neighbor | `classify_neighbor` |

## Optional dynamic modulus family (hypothesis)

Default moduli is always `M_v1`. Callers may pass another family (for example
`M_DYNAMIC_HYPOTHESIS` or `moduli_family_from_primes([2,3,5,7,11])`).

```text
Status: hypothesis / optional tooling
Not a proved modulus vector
Not a Super-Signal replacement
Does not change residual decision shape (still R empty vs nonempty)
```

## Status summary

| Claim | Status |
| --- | --- |
| Definitions of `W`, `R`, closed/open | design object (formalized here; implemented) |
| ERMC implication empty residual => prime | elementary theorem (classical) |
| Dynamic moduli beyond `M_v1` | **hypothesis / optional** |
| Super-Signal universal twin lock | **invalidated** |
| Soft density salvage as inference | **rejected** |
