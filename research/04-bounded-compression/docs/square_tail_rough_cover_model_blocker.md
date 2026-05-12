# Square-Tail Rough-Cover Model Blocker

## Status

Invalidated proof route.

## Finding

A pure residue-cover contradiction is not enough to prove the square-tail
theorem.

For a fixed root, preserve the exact small-prime residue pattern for every
repeat-capable carrier

```text
3 <= ell <= M.
```

Then assign one new large prime carrier to each M-rough defect position. The
CRT system is consistent on the `509` root model:

| Quantity | Value |
|---|---:|
| Root used for small residues | `509` |
| `M` | `39` |
| Repeat-capable small primes | `11` |
| M-rough defect positions | `9` |
| Assigned large carriers | `9` |
| CRT residue coprime to modulus | `true` |
| Local model consistent | `true` |
| Small residue pattern preserved | `true` |
| Large carriers cover all rough defects | `true` |

The CRT residue is coprime to the CRT modulus. The local congruence system does
not itself force the modeled root class to be composite.

The first prime representative found in the CRT class is also selected-square:

| Quantity | Value |
|---|---:|
| Representative index `k` | `4` |
| Representative root | `89726961223544427015292389839` |
| Previous-prime offset below root square | `338` |
| Closing position `m` | `169` |
| Modeled even window | `78` |
| Dynamic cutoff | `8889` |
| Closing offset beyond modeled window | `true` |
| Closing explained by modeled carriers | `false` |
| No prime in modeled window | `true` |
| Closed by cutoff | `true` |
| Selected-square condition | `true` |

The prime-representative artifact is:

```text
research/04-bounded-compression/output/square_tail_rough_cover_prime_class_audit_509.json
```

The prime-representative executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_rough_cover_prime_class_audit.py
```

The base CRT model artifact is:

```text
research/04-bounded-compression/output/square_tail_rough_cover_model_509.json
```

The base CRT model executable builder is:

```text
research/04-bounded-compression/scripts/square_tail_rough_cover_model.py
```

Run:

```text
python3 research/04-bounded-compression/scripts/square_tail_rough_cover_model.py \
  --root 509 \
  --output research/04-bounded-compression/output/square_tail_rough_cover_model_509.json
```

## Proof Boundary

This does not produce a square-tail counterexample. It is a local congruence
model plus one prime representative audit, not an actual complete composite
window through the representative's dynamic cutoff.

It does prove that the following route is insufficient:

```text
derive contradiction only from the residue classes of repeat-capable carriers
and one large carrier per rough defect.
```

It also proves that merely adding primality of the root and the selected-square
condition does not eliminate this local obstruction pattern. The representative
root has no prime in the modeled window, satisfies the selected-square
condition, and still closes later by an actual previous prime at offset `338`.
That closing offset is not explained by the modeled small-prime carriers or the
nine assigned large-carrier classes.

The proof must use additional structure:

1. a law forcing prime-valued M-rough defects before the dynamic cutoff;
2. a new rough-defect transport law;
3. an exact finite reduction;
4. or a counterexample certificate.
