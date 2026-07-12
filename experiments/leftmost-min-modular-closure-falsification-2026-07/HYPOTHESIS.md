# Hypothesis under falsification

**Source:** Grok share session  
`https://x.com/i/grok/share/1f4cf4bbb79542c3af9957e0dd043553`

**Status of this document:** formalization of a **hypothesis** extracted from the share.  
Not a theorem. Does not amend `PROOF.md`.

**Post-experiment (2026-07-11):** H-absolute remains **invalidated**.  
H-comparative is **falsified** on regime `p in [11, 2.5e7]`. See `FINDINGS.md`.

---

## Core insight (verbatim theme)

> The Leftmost Minimal-Divisor Probe Converts Partial Modular Data into Gap-Closure Rules

In gap-reading systems that start from consecutive primes, the leftmost interior
minimum of the divisor-count field turns remainder-zero counts on a fixed
primorial modulus vector into a gap-closure signal. Alternative probes that
ignore leftmost position or ignore divisor-count minimization lose that
sufficiency.

## Formal claims under test

### H-absolute (forcing sufficiency)

**Status before this experiment:** already **invalidated** as a universal rule
in `PROOF.md` (Twin-Prime Resonance / Super-Signal, certificates
`ce_17666309`, `ce_22284029`).

Claim: if the GWR witness `w` (leftmost interior min-`tau`) satisfies
`z(w) >= 4` on `M_v1 = (2, 3, 5, 7, 30, 210, 2310)`, then gap size `g = q - p = 2`.

This experiment reconfirms the known counterexamples inside the same harness
used for the comparative claim. Reconfirmation does not re-open GWR or the
modular zero lemma.

### H-comparative (selector necessity)

**Status before this experiment:** **hypothesis**

On any consecutive-prime regime containing several thousand gaps, redefining
the witness as either:

- **(a) global min-tau without leftmost bias** (here: rightmost interior n that
  achieves the global minimum of `tau`; when the min is unique this equals GWR;
  when ties exist it differs from GWR), or
- **(b) first interior** `w = p + 1` (position-only; no min-tau selection),

will produce **at least one mismatch**, where a mismatch is:

```text
z(w) >= 4  and  g > 2
```

Further comparative edge stated by the share: the leftmost-min combination is
what creates the incompatibility; alternatives lose sufficiency. Operational
falsifier for superiority:

```text
mismatches(alt_a) < mismatches(GWR)
  OR
mismatches(alt_b) < mismatches(GWR)
```

on the same measured regime (strict inequality).

### H-rate (alignment language)

The share says GWR `z >= 4` "aligns with gap size exactly 2 at a rate matching
existing zero-counterexample measurements." This is a **measured** comparison
to known residual-class surfaces, not a proof claim. Report exact counts only.

---

## What would falsify / support

| Outcome | Meaning |
| --- | --- |
| Any GWR row with `z >= 4` and `g > 2` | H-absolute remains **invalidated** (universal forcing false) |
| Zero mismatches for alt-a or alt-b on a multi-thousand-gap regime | H-comparative "at least one mismatch" **falsified** for that alternative |
| `mismatches(alt) < mismatches(GWR)` for a or b | H-comparative superiority / necessity **falsified** |
| Both alts have `>= 1` mismatch and neither has fewer mismatches than GWR | H-comparative **not falsified** on the tested regime (measured support only) |

## Scope boundaries

- Gap-reading only: consecutive known primes `p < q`.
- Twin gaps `g = 2` have a length-1 interior `{p + 1}` (not empty). On twins,
  GWR, rightmost min-tau, and first-interior all select the same point `p + 1`,
  which is composite (not the right prime `q`). Twin gaps are counted in regime
  size; all three selectors agree there.
- On gaps with `g > 2`, multi-way min-tau ties are where leftmost and rightmost
  min-tau can differ (the decisive comparative cases).
- Classical sieves build the prime list and `tau` field only. They do not
  choose the PGS decision.
- No `verified` / `validated` language without an executed `10^18` surface.
