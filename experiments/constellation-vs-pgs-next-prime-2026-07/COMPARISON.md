# Constellation admissibility vs PGS next-prime operator

**Track:** classical comparison only (not PGS inference)  
**Updated:** 2026-07-14  
**Video:** Euclidea, `0_CSs2UYDAI` (auto transcript: `experiments/grok-share-reads-2026-07-13/yt_0_CSs2UYDAI.txt`)  
**Not this note:** Rowland gcd recurrences (separate track: `experiments/rowland-pgs-category-split-2026-07/`)

## One-line split

Constellation theory asks whether several primes can sit at **fixed offsets at once**, forever or infinitely often. PGS asks, given a known prime **p**, what is the **next** prime **q** and what structure sits in the single ordered gap **(p, q)**.

## Contract table

| Axis | Constellation / k-tuple (classical) | PGS next-prime operator |
| --- | --- | --- |
| Input | A fixed offset pattern H = {0 = h1 < h2 < … < hk} | One known prime p |
| Output | Occurrences of n such that all n+hi are prime | Record `{"p","q"}` with q the successor of p |
| Core question | Infinitely many n? At most finitely many? Unique? | What is q, and what is the interior of (p,q)? |
| Settled tool | Modular covering / admissibility (miss a residue mod every prime) | Divisor field, DNI, GWR, chamber structure |
| Settled example | (3,5,7) pattern H={0,2,4} is unique (mod-3 covering) | Next-prime, GWR maximizer, UBC/PSP: **theorem** in `PROOF.md` under stated hypotheses |
| Open core | Twin prime conjecture; Hardy–Littlewood k-tuples; gap-2 from bounded-gap 246 | Residual honesty (e.g. first-tail on hard moduli); public residual → endpoint class |
| Engine role of modular arithmetic | Primary classical sieve geometry | Comparison/audit only; not first frame; not generation gate |

## (3,5,7) in consecutive-gap language

**Classical theorem (external, elementary):** the only primes p < r < s with r−p = s−r = 2 are 3,5,7.

**Consecutive-gap reading (same fact, no PGS promotion):**

- A twin gap is a consecutive pair with gap g = 2 (empty interior; q = p+2).
- Two successive gap-2 steps starting at p means the three primes p, p+2, p+4 are all prime: pattern 0,2,4 on the line.
- For any odd integer m > 3, among m, m+2, m+4 the residues mod 3 cover {0,1,2}, so one term is divisible by 3 and greater than 3, hence composite.
- Therefore you get **at most one** twin-twin chain of consecutive primes on the whole line, and it is exactly 3 → 5 → 7.

Status: **classical theorem**. It is **not** a PGS theorem, not required for the proved next-prime rule, and not evidence for or against twin-prime infinitude.

## Residual class A / Super-Signal non-claims

Program history (status already fixed elsewhere):

- Super-Signal claim `z(w) ≥ 4 ⇒ g = 2` is **invalidated**.
- Modular lemma `z(w) ≥ 4 ⇔ 30 | w` on fixed `M_v1` is **theorem** (`PROOF.md`) on that vector only.
- Residual catalogs (including twin-like gap events and R0-style false-positive classes) are **measured** maps, not twin-prime laws.

**Explicit non-claims for residual / class tables:**

1. Residual class A (or any measured twin-gap enrichment) does **not** free the pattern 0,2,4.
2. High counts of g=2 do **not** imply a free triple-twin or “prime triplet always.”
3. `z(w) ≥ 4` structure does **not** certify two successive gap-2 steps.
4. No residual table may be read as “triple twins free outside 3,5,7.” Classical covering already kills that forever.
5. Bounded compression / PSP (witness offset) is **not** the Zhang–Maynard bound 246 on prime pairs, and neither implies the other.

## What each may claim

**Constellation side may claim:**

- Pattern H is inadmissible ⇒ at most finitely many (often unique) hits; (3,5,7) is the unique 0,2,4 prime triple.
- Pattern H is admissible ⇒ not modularly banned; infinitude is **conjecture** (Hardy–Littlewood) unless a separate proof exists.
- Bounded gaps: infinitely many prime pairs with gap ≤ 246 (Zhang–Maynard–Polymath line) is a **classical theorem** of that program; gap 2 remains open.

**PGS side may claim:**

- Next prime after p is determined by the min-τ rule (**theorem**).
- Interior maximizer at GWR witness (**theorem**).
- Selected-witness offset bound UBC/PSP (**theorem**); not raw gap size as twin-prime claim.
- Measured residual inventories of gap patterns on named regimes, with exact limits.
- Explicit **unresolved** when structure does not close (e.g. cryptology residual codes).

**Neither side may claim from the other:**

- PGS next-prime does not prove twin primes.
- Twin-prime conjecture does not restate GWR.
- Admissible k-tuple does not issue a GWR/endpoint certificate.
- Residual class counts do not “verify” constellation conjectures.

## Live program alignment

Keep pressure on **public residual → endpoint class** (first-tail honesty on the 50-bit pin and kin). Do **not** open a twin-prime campaign, sieve-first generator, or k-tuple search as residual close from this video.

## Reject list

- Sieve-first or k-tuple search as PGS generation or residual close
- Modular covering as PGS inference gate for choosing q
- “PGS proves twins via residual A”
- “UBC/PSP ⇒ gap ≤ 246” or the reverse slogan merge
- Merging Rowland gcd recurrences into this constellation note
