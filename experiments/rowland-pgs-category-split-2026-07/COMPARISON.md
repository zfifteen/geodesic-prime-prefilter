# Rowland as classical encounter map vs PGS as next-prime operator

**Track:** classical comparison only (not PGS inference)  
**Updated:** 2026-07-14  
**Sources:** Rowland, JIS 11 (2008) / arXiv:0710.3217; Chamizo–Raboso–Ruiz-Cabello, Electron. J. Comb. 18(2) (2011) #P10; local video transcript `experiments/grok-share-reads-2026-07-13/yt_OpaKpzMFOpg.txt`  
**Status labels:** classical theorem (external) / classical conjecture (external) / PGS theorem (`PROOF.md`) / measured / hypothesis / unresolved  
**Forbidden:** gcd/lcm/lpf as PGS inference; generator path import; theorem promotion into `PROOF.md`

## Category split (one sentence)

Rowland is a classical dynamical system whose nontrivial events **encounter** primes; PGS is a structural account of ordered gap interiors and **next-prime selection** from a known prime.

## Contract table

| Axis | Rowland encounter map (classical) | PGS next-prime operator |
| --- | --- | --- |
| Input | Single seed `a(1)` (or mid-stream state `a(n1)`) | Known prime `p` |
| State update | `a(n) = a(n−1) + gcd(n, a(n−1))` | Chamber / divisor field on integers `> p` |
| Primary output | Sequence `a(n)`; event stream `g(n) = a(n)−a(n−1) ∈ {1} ∪ primes` under hypotheses | Record `{"p", "q"}` with `q` the next prime |
| Selection rule | Nontrivial `g` forced prime when return-map lemma applies | `q = min{n > p : τ(n) = 2}` (**theorem**, `PROOF.md`) |
| Interior structure | Not about gap interiors between consecutive primes | GWR leftmost min-τ maximizer (**theorem**); UBC / PSP on witness offset (**theorem**) |
| Engine primitives | `gcd`, and for shortcuts `lpf((r−1)n1 − 1)` | Divisor counts, DNI excess, GWR, chamber/endpoint objects |
| Audit role | Primality of jumps is the *content* of the classical theorem | Audit may confirm `q`; audit must not choose `q` |
| Failure mode | Bad large-prime miner: shortcut needs independent factor/primality of `2n−1` | Explicit **unresolved** if structure does not close; no primality fallback |
| Scope of “generates primes” | Event values land in primes ∪ {1} for special seeds / after transience | Deterministic successor operator on every eligible prime input |

## Rowland return map (external theorem, exact)

**Lemma 1 (Rowland).** For `r ∈ {2,3}` and `n1` with `(r−1)n1 ≥ 3`, if `a(n1) = r · n1` and `p = lpf((r−1)n1 − 1)`, then the next nontrivial jump is at `n2 = n1 + (p−1)/(r−1)` with `g(n2) = p` and **return** `a(n2) = r · n2`.

**Theorem 1 (Rowland).** For `a(1) = 7`, every `g(n)` is 1 or prime (`n ≥ 2`), via bootstrap into the `r = 3` lemma.

**Not theorem for arbitrary seeds:** composite jumps exist before any nice regime (e.g. `a(1)=532`, `g(18)=9`). Eventual entry is **classical conjecture** (Rowland Conjecture 1; Chamizo et al. Conjecture 1.2 / 1.5).

## 2011 infinite-primes result in residual-inventory language

Chamizo–Raboso–Ruiz-Cabello do **not** prove “every odd prime appears in Rowland’s stream.”

| Claim | Status (classical external) | Residual-inventory reading |
| --- | --- | --- |
| `a(1)=7` ⇒ `g(n) ∈ {1} ∪ primes` | classical theorem (Rowland) | Full event stream classified on that seed |
| Infinite distinct primes in `{g(k)}` under (i)/(ii)/(iii) of Conjecture 1.5 | classical theorem **conditional** on reaching the nice auxiliary regime (Prop. 3.2) | Once the return regime is entered, the inventory is **unbounded** (infinitely many distinct primes appear as events) |
| Conjecture 1.5: for odd `a1 > 3`, finite `n0`, `m0` with `n0 = m0+1` | classical conjecture; computer support cited for `a1 < 10^8` | “Eventually enters certificate regime” is **unresolved** as a universal statement; large transient `m0` can be forced (Prop. 2.8) |
| Characterization of finite prime blocks (Rowland chains, Prop. 3.3) | classical theorem | Not all finite prime lists are admissible event blocks; coverage has **structural holes**, not only scan limits |
| Every odd prime appears for `a(1)=7` | **unresolved** classically | Missing primes at horizon `N` are **unresolved-not-false**, never “disproved by absence” |
| Prime `2` as a jump | never (odd `2n−1` world) | **Forced absence**, not unresolved |

PGS residual honesty maps cleanly: **forced** vs **unobserved so far** vs **blocked by chain constraints** vs **seed never reaches nice state**. Do not convert a finite missing list into “this prime cannot appear.”

## Measured inventory protocol (classical scan only; no PGS code path)

**Purpose:** inventory which primes appear as nontrivial Rowland events up to horizon `N`, with honest status labels.  
**Location:** keep any runner under this experiment folder or another **classical comparison** path. Do **not** wire into generator, rsa-v3 resolver, or chamber inference.

**Protocol (measured only):**

1. Fix seed `a(1)` (default 7) and horizon `N` (index or event count).
2. Iterate the classical recurrence only inside the comparison harness.
3. Collect multiset `E = { g(n) : 2 ≤ n ≤ N, g(n) > 1 }`.
4. Emit:
   - `primes_seen`: sorted unique primes in `E`
   - `missing_odds_below_B`: odd primes `≤ B` not in `primes_seen` (choose `B` from max event or a fixed bound)
   - `composite_events`: any `g(n) ∉ {1} ∪ primes` (should be empty for seed 7; record if any)
   - `first_hit[p]`: least `n` with `g(n)=p` when present
5. Labels:
   - presence of `p` in `E` → **measured** hit at `first_hit[p]`
   - absence of `p ≤ B` → **unresolved-not-false** at horizon `N` (unless a chain obstruction from Prop. 3.3 applies, then **blocked by chain constraint** as classical structural non-coverage)
   - infinite coverage claims → not available from finite `N`
6. Forbidden in PGS paths: copying this loop into production generator or using `gcd`/`lpf` to choose `q`.

Example smoke regime (when someone runs it): `a(1)=7`, `N=10^5`, `B=500`. Report counts only; no “verified generator” language.

## Sentences that would smuggle Rowland into the generator (reject)

1. “PGS next prime is the next nontrivial Rowland gcd after index p.”
2. “Use `lpf(2n−1)` as a PGS chamber shortcut / floor transport.”
3. “Because Rowland jumps are prime, dual-gap residual may admit the 50-bit endpoint class.”
4. “Implement Rowland recurrence in `src/` as an alternate prime source with audit later.”
5. “Cloitre LCM ratios are a PGS-native residual discriminator.”

**Replacement discipline:** Rowland stays literature contrast and optional classical inventory; PGS keeps `p → q` structure, explicit unresolved, audit after generation.

## What PGS contributes to the Rowland matter (reverse arrow)

- Category diagnosis: encounter map ≠ next-prime operator.
- Efficiency dead end is structural under the audit/inference split.
- Methodology: glamorous value patterns vs index/return residual (same honesty as Super-Signal kill and 50-bit first-tail pin).
- Coverage language: forced absence / unresolved-not-false / chain-blocked / unbounded-after-regime (2011), without mysticism.

## What PGS does not contribute

- No new classical proof of Conjecture 1.2/1.5.
- No claim that every odd prime appears.
- No import of `gcd` into PGS inference.
- No change to `PROOF.md` theorem status.
