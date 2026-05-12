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

The artifact is:

```text
research/04-bounded-compression/output/square_tail_rough_cover_model_509.json
```

The executable model builder is:

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
model, not a prime root with an actual complete composite window.

It does prove that the following route is insufficient:

```text
derive contradiction only from the residue classes of repeat-capable carriers
and one large carrier per rough defect.
```

The proof must use additional structure:

1. primality of the root in the actual integer line;
2. selected-square branch structure;
3. a new rough-defect transport law;
4. an exact finite reduction;
5. or a counterexample certificate.
