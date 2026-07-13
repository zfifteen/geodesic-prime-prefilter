# Hypothesis under attack: left-endpoint parity modular bias

**Status of this document:** formalization of a **hypothesis**.  
Not a theorem. Does not amend `PROOF.md`.

**Related prior package:**  
`experiments/leftmost-min-modular-closure-falsification-2026-07/`  
(that package falsified *leftmost necessity* for modular closure; this package
attacks a different claim: *parity / left-endpoint bias* as the mechanism of
mismatch inflation under min-`tau` selection.)

---

## Core insight (HYPOTHESIS)

Left-endpoint parity creates a systematic modular bias when using
minimal-divisor-count witnesses in observed prime gaps.

**Mechanism (hypothesis, not theorem):**

When reading a real prime gap with min-`tau` witness selection, leftmost choice
preferentially includes `p + 1` (always even for odd prime `p`). Forced factor
2 under primorial moduli elevates small-prime hits. When multiple interiors tie
for min `tau`, leftmost more often lands on even `p + 1`, inflating `z` and
`z >= 4` mismatches versus actual gap length. Rightmost among the same minima
largely avoids that forced-even position. Invisible if one assumes all min-`tau`
interiors are modularly equivalent. Specific to gap-reading frames (not pure
construction).

## Formal claims

### H-parity (primary signature)

Under GWR (leftmost interior min-`tau`), on any consecutive-prime regime with
many gaps:

```text
rate(mismatch | w even)  >  rate(mismatch | w odd)
```

where mismatch means `z(w) >= 4` and `g = q - p > 2`.

**Structural note (not a free empirical claim):** on fixed `M_v1`, any integer
with `z >= 4` is divisible by 30 (modular zero lemma, `PROOF.md`), hence even.
Odd GWR witnesses therefore cannot mismatch under the `z >= 4` definition.
Prediction H-parity is **logically forced** by that lemma plus the mismatch
definition, not an independent modular-bias discovery. The probe reports this
explicitly and moves the decisive load to non-degenerate signatures below.

### H-endpoint (distinguishing signature)

Mismatches under leftmost min-`tau` concentrate on witnesses with `w = p + 1`
(the forced-even left endpoint), not merely on "any even" interior.

```text
Among GWR mismatches: fraction with w == p + 1 is high
Among multi-way min-tau ties that include p+1: leftmost selects p+1 often
```

### H-rightmost (comparative)

Rightmost min-`tau` produces **strictly fewer** total mismatches than leftmost
min-`tau` on any new range with at least several hundred thousand gaps.

Prior package already measured this on `p in [11, 2.5e7]` (rightmost 0, GWR 2).
This package re-tests on a **fresh** band disjoint from that decisive window.

### H-tie-break (control isolation)

The effect is driven by **leftmost among ties that include `p + 1`**, not by
"even numbers have more factors" alone.

Controls:

1. **Unique min-`tau` only:** when the min is unique, left and right agree; no
   leftmost tie-break. Report mismatch / `z4` rates split by unique-even vs
   unique-odd and by unique-at-`p+1` vs not.
2. **Ties only:** when left and right differ, report parity of each, whether
   left is `p + 1`, and mismatch counts.
3. **z-threshold sensitivity:** also count mismatches at `z >= 3` (where odd
   witnesses can fire) to test whether even/odd rate gaps survive without the
   `30 | w` collapse.

## Disconfirmation criteria (pre-registered)

| ID | Criterion | If met |
| --- | --- | --- |
| D-a | No measurable even-vs-odd mismatch difference under leftmost at `z >= 4` | H-parity **falsified** (or vacuous if both zero and degenerate) |
| D-a3 | At `z >= 3`, even and odd mismatch rates equal within the regime (or odd higher) | non-degenerate parity claim **falsified / weakened** |
| D-b | Rightmost produces **more** mismatches than leftmost on a fresh large band | H-rightmost **falsified** |
| D-c | GWR mismatches are **not** concentrated at `w = p + 1` (fraction low) | H-endpoint **weakened / falsified** |
| D-d | Unique-min control shows the same even/`p+1` inflation without ties | pure "even has more factors" alternative **supported**; tie-break story **weakened** |

## What "survives" means

| Outcome | Label |
| --- | --- |
| Fresh band still has rightmost mismatches < leftmost | H-rightmost **survives** (measured on that regime) |
| Mismatches sit at `w = p + 1` on multi-way ties | H-endpoint **survives** (measured) |
| H-parity only holds via `z >= 4 => even` | H-parity **weakened** as independent insight (logically forced) |
| D-a3 or D-d kills the narrative | overall insight **weakened** or **falsified** on that arm |

## Scope

- Gap-reading only: consecutive known primes `p < q`, odd primes (`p >= 11`).
- Twin gaps `g = 2`: interior is `{p + 1}` only; all selectors agree; `p + 1` is even.
- Classical sieves prepare primes and `tau` only. No classical gate chooses the
  PGS decision.
- No `verified` / `validated` language without an executed `10^18` surface.
- Status words: **hypothesis** / **measured** / **falsified** / **weakened** /
  **survives** (measured) / **unresolved** / **theorem** (only for PROOF items).
