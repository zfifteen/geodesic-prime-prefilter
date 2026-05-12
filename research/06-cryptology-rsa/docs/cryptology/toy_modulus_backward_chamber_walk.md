# Toy Modulus Backward Chamber Walk

## Claim

A toy modulus demonstrates the PGS distinction cleanly. Starting from a
composite coordinate `n`, the backward chamber walk traverses prime endpoints
by divisor-count law. The endpoints are not accepted by a primality oracle.
They are reached when the chamber walk hits `tau(k) = 2`.

Use the toy modulus:

$$n=35=5\cdot 7$$

The factor labels `5` and `7` are audit annotations for the toy example. The
walk below does not use divisibility by `35`, multiplication checks, `gcd`,
factorization, `isprime`, `nextprime`, Miller-Rabin, or a sieve.

## Chamber Rule

For each integer `k` encountered while walking backward, compute the exact
divisor count `tau(k)`.

The backward chamber closes at the first lower coordinate with:

$$\tau(k)=2$$

That coordinate is a prime endpoint on the deterministic chain.

## Walk From `35`

| Backward chamber read | Divisor-count sequence | Endpoint reached |
|---|---:|---:|
| `35, 34, 33, 32, 31` | `4, 4, 4, 6, 2` | `31` |
| `30, 29` | `8, 2` | `29` |
| `28, 27, 26, 25, 24, 23` | `6, 4, 4, 3, 8, 2` | `23` |
| `22, 21, 20, 19` | `4, 4, 6, 2` | `19` |
| `18, 17` | `6, 2` | `17` |
| `16, 15, 14, 13` | `5, 4, 4, 2` | `13` |
| `12, 11` | `6, 2` | `11` |
| `10, 9, 8, 7` | `4, 3, 4, 2` | `7` |
| `6, 5` | `4, 2` | `5` |

The backward endpoint chain traversed from `35` is:

```text
31 -> 29 -> 23 -> 19 -> 17 -> 13 -> 11 -> 7 -> 5
```

The toy modulus factors `7` and `5` appear as ordinary traversed endpoints on
the same deterministic prime chain.

## What This Demonstrates

The modulus coordinate does not contain hidden primes in the PGS frame. It sits
on the same deterministic number line as every other integer. Walking backward
through chamber structure reaches prime endpoints by law.

The classical question is:

```text
Which hidden primes multiply to n?
```

The PGS question is:

```text
Which already-fixed chain endpoints are traversed from the chamber coordinate n?
```

For `n = 35`, the backward chamber walk traverses both endpoint coordinates
that the audit annotation names as the factors. The traversal itself is
law-facing, not oracle-facing.

## Separation Of Roles

The chamber walk identifies prime-chain endpoints by `tau(k)=2`.

The product relation `35 = 5 * 7` is not used by the walk. It is the toy audit
fact that names why the traversed endpoints `7` and `5` matter for this
example.

This separation is the point of the demonstration:

```text
PGS traversal: chamber coordinate -> endpoint chain
RSA coupling: endpoint pair -> modulus relation
```

At toy scale, both are visible in one table. The chamber walk shows that the
prime endpoints are not hidden objects. They are not-yet-traversed coordinates
until the deterministic walk reaches them.
