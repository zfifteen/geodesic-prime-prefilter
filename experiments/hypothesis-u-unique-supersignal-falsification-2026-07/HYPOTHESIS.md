# Hypothesis U — Unique Super-Signal

**Status:** `invalidated` (2026-07-09 experiment CE `p=156942923`)  
**Date formalized:** 2026-07-09  
**Parent context:** Invalidated universal Super-Signal `z(GWR) ≥ 4 ⇒ g = 2` in `PROOF.md`

---

## Objects

- **Prime gap:** consecutive primes `p < q`, gap size `g = q − p`, interior `I = {p+1, …, q−1}` (nonempty when `g ≥ 2`).
- **Divisor count:** `τ(n)` = number of positive divisors of `n`.
- **GWR witness `w`:** leftmost `n ∈ I` achieving `min{τ(m) : m ∈ I}` (leftmost minimum-divisor carrier).
- **Tie count:** number of interiors with `τ(n) = τ(w)`. **Unique minimum** means tie count `= 1`.
- **Remainder vector on `M_v1`:** moduli `(2, 3, 5, 7, 30, 210, 2310)`.
- **Zero count:** `z(n) = #{ m ∈ M_v1 : m | n }`.

---

## Hypothesis U (primary)

**Statement.**  
Let `w` be the GWR witness of a nonempty prime-gap interior.  
If

1. `z(w) ≥ 4` on `M_v1` (equivalently, by the proved modular lemma, `30 | w`), **and**
2. the interior `τ`-minimum is **unique** (exactly one interior attains `τ(w)`),

then

```text
g = 2    and    q = w + 1.
```

**Contrapositive form (CE search target).**  
A counterexample is any consecutive prime pair with:

```text
g > 2
  AND  w = GWR(p, q)
  AND  z(w) ≥ 4
  AND  tie_count(w) = 1
```

One such gap **falsifies** Hypothesis U.

---

## Status separation (mandatory)

| Claim | Status |
| --- | --- |
| Bare Super-Signal `z(GWR) ≥ 4 ⇒ g = 2` | **Invalidated** (CE family; see `PROOF.md`) |
| Modular lemma `z ≥ 4 ⇔ 30 \| w` on `M_v1` | **Proved** (case analysis) |
| **Hypothesis U** (unique min + `z ≥ 4 ⇒ g = 2`) | **Invalidated** (CE `p=156942923`, `g=8`, `ties=1`, `z=4`) |
| Empty CE hunt on a finite range | **Measured support only** — never “proved” |

GWR maximizer, next-prime rule, and bounded-compression pillars are **not** at issue here.

---

## Why this hypothesis (not “5 zeros”)

- On `M_v1`, `z = 5` is impossible; `z ≥ 5` collapses to `z ≥ 6` (`210 | w`).
- Every known bare Super-Signal CE has `z = 4`, `τ(w) = 16`, `g = 8`, and **ties ≥ 3**.
- Hypothesis U adds the side condition those CEs violate: **unique** minimum.

Secondary related hypotheses (not primary formalization):

- **H-210:** `210 | w` as GWR ⇒ `g = 2` (equivalently `z ≥ 6`).
- **H-τ16:** `z ≥ 4` and `τ(w) > 16` ⇒ `g = 2`.

---

## Falsification contract

| Outcome | Meaning |
| --- | --- |
| ≥1 CE found | Hypothesis U **falsified** |
| 0 CEs in stated regime | **Not falsified in tested regime** (measured); remains hypothesis |
| 0 CEs forever | Not established by finite scan |

---

## Authority

- `PROOF.md` — invalidated Super-Signal section; surviving modular lemma  
- This folder — hypothesis text, experiment, findings  
