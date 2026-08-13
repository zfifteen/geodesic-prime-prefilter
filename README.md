# Prime Gap Structure

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--08--13-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Lean 4](https://img.shields.io/badge/Lean%204-audit%20mirror%20M0--M5-success)
![Lean](https://img.shields.io/badge/lean--toolchain-v4.30.0-purple)

![Prime Gap Structure hero](visualizations/conceptual/prime-gap-structure-hero.jpg)

**Abstract**  
Prime Gap Structure studies the ordered divisor-count field inside prime gaps and builds an experimental engine that tries to use that field to walk to the next prime. Local theorems prove how the interior minimum (the Gap Winner) is selected and how the next prime is the first later return of divisor count 2. The same core stack has a completed Lean 4 audit mirror (program Definition of Done M0-M5). That mirror checks logical structure. It does not select primes and it does not rewrite theorem status in `PROOF.md`.

A 30-second status map lives in [`docs/STATUS_TIERS.md`](docs/STATUS_TIERS.md).

| Tier | Meaning | In this repository |
| --- | --- | --- |
| **Proved** | Local integer theorems under `PROOF.md` | Next-prime rule, GWR, modular zero lemma, universal bounded compression, Prime-Square Proximity Theorem |
| **Measured** | Finite executed surfaces, including `10^18` | No-Later-Simpler-Composite zero violations, generator decade ladder, RSA endpoint-class ledger |
| **Experimental** | Hypothesis / probe / reading path | RSA v2/v3 reciprocal closure, Mersenne exponent wall, DNI-to-zeta and `docs/rh/` |

These rows keep ambition. They add precision. They do not demote proved theorems.

---

## Table of Contents

- [1. Quick Intuitive Understanding](#1-quick-intuitive-understanding)
- [Key Concepts (Mini-Glossary)](#key-concepts-mini-glossary)
- [2. Core Results](#2-core-results)
  - [2.1 What Is Proved](#21-what-is-proved)
  - [2.2 What Is Measured](#22-what-is-measured)
- [3. Getting Started](#3-getting-started)
- [4. Deeper Theory & Formal Proofs](#4-deeper-theory--formal-proofs)
- [5. Machine-Checked Verification (Lean 4)](#5-machine-checked-verification-lean-4)
- [6. PGS-to-RH Reading Path & Open Questions](#6-pgs-to-rh-reading-path--open-questions)
- [A Different Way To Generate Primes](#a-different-way-to-generate-primes)
- [Where This Leads](#where-this-leads)
- [Repository Map](#repository-map)
- [Reading Further](#reading-further)
- [Python API](#python-api)

---

## 1. Quick Intuitive Understanding

Most people learn that prime numbers are fundamentally unpredictable. They appear to pop up at irregular intervals, almost as if they are scattered at random across the number line. Textbooks and popular explanations reinforce this view: primes become rarer as numbers grow larger, the gaps between them can be arbitrarily wide, and there is no simple formula that will always tell you exactly where the next one sits. The common belief is that the only practical ways to find the next prime are to test candidates one by one or to rely on probabilistic estimates. Prime gaps themselves are treated as empty stretches of composites, nothing more than the boring distance you have to cross before the next interesting number arrives.

That picture feels natural because it matches everyday experience with large numbers. When you look at a long stretch of integers, most of them are obviously composite, and the primes seem to hide without any clear signal. The word "gap" itself nudges us to think of the space between two primes as meaningless background noise.

**The truth is the exact opposite.**

Start with one prime. Look at the integers that come right after it. Those integers are not random obstacles. They carry precise factor structure, and that structure is exactly what determines where the next prime must appear. The next prime can be found directly by reading the numbers that follow the one you already have. Nothing is left to chance or probability once you know how to look.

At first glance, what follows can read like a mere tautology: the next prime is the first later integer whose divisor count is exactly two. That definition is only the endpoint. Prime Gap Structure studies the arithmetic *before* the endpoint: the ordered divisor-count field inside the gap, the selected interior minimum, the zero-excess coordinate that places primes and composites on one scale, and the measured chamber patterns that survive far beyond the toy examples.

### Look Between 23 and 29

It helps to see this idea with a small, concrete example so you can watch the pattern unfold step by step.

Take the primes 23 and 29. They are consecutive, which means every integer between them is composite. Write them out and you get this simple picture:

23 | 24 25 26 27 28 | 29

At first glance the gap looks like nothing but a distance of six. That is what most people notice, and it is why the middle feels empty. But stop and look more closely at what is actually sitting inside that interval. Each of those five composites has its own complete list of positive divisors. When you count how many divisors each one has, something changes in how you see the gap.

Here is the same interval again, but now with the divisor counts written underneath:

number:        24  25  26  27  28  
divisor count:  8   3   4   4   6

The numbers themselves have not changed. What has changed is that we are now seeing an ordered list of divisor counts. Among those counts the smallest value is 3, and it appears at the very first position where it can, at the number 25.

That single observation is surprising because it contradicts the idea that the interior is meaningless. Instead of empty space, the gap now has an internal shape that is completely determined by ordinary arithmetic. The lowest divisor count inside the gap is not hidden or random; it emerges clearly once you simply count.

**Plain-English takeaway**: The first time the minimal divisor count appears inside the gap marks a special composite (the Gap Winner). This is not coincidence; it is the arithmetic structure of the gap itself.

### When The Lowest Count Appears Multiple Times

One small gap could be a lucky coincidence. To see that the pattern is reliable, it is useful to look at another example where the situation is a little less tidy.

Consider the gap from 89 to 97:

89 | 90 91 92 93 94 95 96 | 97

Again the interior numbers are all composite. Their divisor counts are:

number:        90  91  92  93  94  95  96  
divisor count: 12   4   6   4   4   4  12

This time the smallest count inside the gap is 4. Notice that 4 appears four different times, at 91, 93, 94, and 95. Yet when you read the list from left to right, the very first time that lowest count of 4 shows up is at 91.

The same principle that appeared in the smaller gap is still at work. Inside any prime gap with at least one interior number, there is always a first interior number that carries the lowest divisor count. The gap is telling you two things at once: what the lowest count is and exactly where that count first occurs. The pattern is not fragile; it survives even when the lowest count repeats.

**Plain-English takeaway**: Even when the minimal divisor count repeats, the *leftmost* occurrence is the structurally significant one. The gap encodes its own selected interior witness.

### How The Gap Ends

So far we have focused on the interior of the gap. Now shift your attention to the right-hand edge, where the gap actually closes.

Recall what makes a number prime: it has exactly two positive divisors, 1 and itself. Every composite number has at least three. If you start at any known prime and simply read forward through the integers, every composite you encounter will have a divisor count strictly greater than 2. The next prime is the first number after your starting prime whose divisor count drops to exactly 2.

Return to the 23-to-29 gap and extend the divisor-count list one more step:

number:        24  25  26  27  28  29  
divisor count:  8   3   4   4   6   2

You can watch the count stay safely above 2 through the entire interior. Then, at 29, it becomes exactly 2 and the gap ends. The endpoint is not chosen by trial and error or by guessing; it is the inevitable place where the divisor count first reaches 2 after the starting prime.

This is why the interior and the endpoint belong together. They are two parts of the same continuous story told by the same ordered list of divisor counts.

### Interior And Endpoint Together

Once you see the gap as a single ordered sequence rather than a meaningless jump, the whole picture snaps into focus. The selected composite inside the gap (the first interior number with the lowest divisor count) and the endpoint prime (the first later number with divisor count exactly 2) are both visible in the same list. They are not separate phenomena; they are the natural consequences of reading the factor structure that sits between two consecutive primes.

For the gap from 23 to 29 the selected composite is 25 and the endpoint is 29. For the gap from 89 to 97 the selected composite is 91 and the endpoint is 97. In every case the arithmetic inside the gap carries the information that points directly to the next prime.

This is the larger reversal the repository explores. A prime gap is no longer just a size or a distance. It has a clear internal shape, a selected composite that marks the lowest point inside that shape, and a right endpoint that is fixed by the divisor count returning to 2. The middle is not meaningless; it is full of information. The usual story treats the numbers between primes as an obstacle. Here they are the evidence.

---

## Key Concepts (Mini-Glossary)

These one-line definitions capture the central objects used throughout the repository.

- **Gap Winner Rule (GWR)**: The leftmost composite inside a nonempty prime gap that carries the minimal divisor count is always the raw-Z maximizer and serves as the selected interior witness for the gap's termination.
- **Divisor Normalization Identity (DNI)**: The coordinate `E(n) = (d(n)/2 − 1) ln n` places every prime greater than 1 exactly at zero excess. Composites sit strictly above this floor. The dual coordinate is `Z(n) = e^{-E(n)}`, with primes at `Z = 1.0`.
- **Selected interior witness / leftmost min-d(n) carrier**: The first number inside the gap that achieves the lowest divisor count. This is the GWR-selected composite.
- **Bounded compression**: For every consecutive prime gap with nonempty interior, the GWR-selected witness appears within `max(64, ceil(0.5 * log(q)^2))` of the left endpoint. This bound is proved at Cramér scale from divisor-count structure.
- **Prime-Square Proximity Theorem** (proved 2026-07-05): When the selected witness is a prime square `r²`, the distance `r² − p` cannot exceed the bounded-compression cutoff without forcing a modulus-link collision.
- **Modular zero lemma on $M_{v1}$**: On the fixed remainder vector modulo $(2,3,5,7,30,210,2310)$, four or more zeros occur if and only if $30 \mid w$. Modular fact only; not a gap-size lock.
- **No-Later-Simpler-Composite**: Immediate corollary of leftmost min-`d(n)` selection. The committed `10^18` stress surface records zero violations. That sweep is measured, not a separate infinite proof.

---

## 2. Core Results

Public status is split on purpose. Proved statements live in `PROOF.md`.
Measured surfaces live in `docs/RESULTS.md` and the 10^18 evidence package.
The one-page map is [`docs/STATUS_TIERS.md`](docs/STATUS_TIERS.md).

### 2.1 What Is Proved

> **Proved status (as of July 2026, unchanged by this reframe)**  
> The following local theorems are formally proved in `PROOF.md`. They stand independently of any conjectures about the Riemann Hypothesis or global prime distribution. They are not bounded by the 10^18 measured sweep.

- **Next-prime rule**: Given a prime *p*, the next prime *q* is the first integer after *p* whose divisor count returns to exactly 2. See `PROOF.md` Headline 1.
- **Gap Winner Rule (GWR)**: The leftmost min-*d(n)* composite inside the gap is the raw-Z maximizer and the structurally selected interior witness. See `PROOF.md` Headline 2. The No-Later-Simpler-Composite condition (no later interior integer has strictly smaller `tau`) is an immediate corollary of this leftmost selection.
- **Modular zero lemma on $M_{v1}$**: Four or more remainder zeros on the fixed primorial vector if and only if $30 \mid w$ (proved; modular only). See `PROOF.md` Modular zero lemma.

#### Bounded Compression at the Cramér Scale

- **Universal bounded compression** at Cramér scale: The GWR-selected witness always appears within `max(64, ceil(0.5 * log(q)^2))` of *p*. This is a proved bound on the selected-witness offset `w - p`, not on raw gap size `q - p`. See `PROOF.md` Headline 3.
- **Prime-Square Proximity Theorem** (proved 2026-07-05): When the witness is a prime square, its offset from *p* is bounded by the same compression limit. This closes the square branch of universal bounded compression.

These statements are proved from the arithmetic of divisor counts and the ordering inside gaps, together with the named finite premises and classical imports recorded in `PROOF.md`. They do not rely on probabilistic models or unproved global assumptions.

See `PROOF.md` for the complete formal stack and supporting lemmas. For the independent Lean 4 audit mirror of that stack (program DoD M0-M5), see [§5](#5-machine-checked-verification-lean-4) and open `docs/lean-pgs-verification/index.html`.

### 2.2 What Is Measured

These are finite executed surfaces. They corroborate implementations and named stress conditions. They are not infinite proofs.

- **No-Later-Simpler-Composite through 10^18**: Zero observed violations on the committed stress surface. Once the GWR-selected integer appears, no later interior composite with strictly smaller divisor count is seen before the next prime. Pointers: `docs/RESULTS.md`, `assert_results.tsv`, `visualizations/gallery/`.
- **Generator decade ladder**: `2816 / 2816` exact `{"p", "q"}` records from `10^8` through `10^18`. Implementation evidence for the walk engine.
- **RSA endpoint-class ledger**: Curated 40-bit and 64-bit rows are audit-confirmed endpoint classes. The 50-bit row remains unresolved under the v2 runner. See `research/06-cryptology-rsa/` and Tier 3 for the probe claim boundary.

---

## 3. Getting Started

```bash
git clone https://github.com/zfifteen/prime-gap-structure.git
cd prime-gap-structure
python3 -m pip install -e ./src/python
```

The installed package provides the core deterministic primitives for walking prime gaps via divisor-count structure and GWR selection.

For concrete runnable demonstrations:
- Minimal gap illustrations (including the 23→29 example) are available in the research notebooks and scripts.
- Larger-scale validation runs and generator examples live in `research/` and `experiments/`.
- The full test and assertion surface is tracked in `assert_results.tsv`.

After installation you can import the core modules and begin exploring the ordered divisor-count field between any two consecutive primes.

---

## 4. Deeper Theory & Formal Proofs

The repository develops the above results in greater depth.

- `PROOF.md`: The formal proofs of the next-prime rule, GWR, bounded compression, Prime-Square Proximity Theorem, and supporting lemmas.
- `docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md`: Detailed exploration of the rule that identifies the special composite inside each gap.
- `docs/core/DIVISOR_NORMALIZATION_IDENTITY.md`: Full treatment of the zero-excess normalization `E(n)` and its dual `Z(n)`.
- `docs/core/PRIME_GAP_GENERATIVE_MODEL.md` and `docs/core/RECURSIVE_PRIME_WALK.md`: The broader generative model and recursive behavior.
- `docs/RESULTS.md`: Measured results and surfaces.

Visualizations of the core objects live in `visualizations/`. Prefer the catalog plot library at `visualizations/gallery/index.html` (status chips + regimes). The hub router is `visualizations/index.html`.

---

## 5. Machine-Checked Verification (Lean 4)

**Status: Lean audit-program DoD met (M0-M5, 2026-07-23).** Lean checks logical structure. Finite premises `gwr_finite_base_v1`, `bounded_compression_base_v1`, and `residual_k128_v1` enter as named hypothesis bundles with pinned certificate paths and hashes. Lean does not rerun those exhaustions. The only core-path axiom is `tau_prime_square_eq_three` (CL-003). Core `sorry` count is zero. See [`lean-4/SORRY_AXIOM_INVENTORY.md`](lean-4/SORRY_AXIOM_INVENTORY.md).

In addition to the prose proofs in `PROOF.md` and large-scale computational surfaces, the repository ships a finished **Lean 4 machine-checked mirror** of the core theorem stack. That layer is a **downstream audit only**: it mechanically checks statements already established in `PROOF.md`. It does not generate primes, feed the generator, or rewrite theorem status.

| What you get | Where |
| --- | --- |
| Public status surface (plain English first) | [`docs/lean-pgs-verification/index.html`](docs/lean-pgs-verification/index.html) |
| One-command mechanical DoD checks | `bash scripts/lean4-dod-check.sh` |
| Peer D1–D7 accept record | [`lean-4/peer/M5_DOD_ACCEPT.md`](lean-4/peer/M5_DOD_ACCEPT.md) |
| Living `sorry` / axiom inventory | [`lean-4/SORRY_AXIOM_INVENTORY.md`](lean-4/SORRY_AXIOM_INVENTORY.md) |
| Parent program tracker (closed DONE) | [GitHub issue #53](https://github.com/zfifteen/prime-gap-structure/issues/53) |

### Core stack mirrored in Lean

| PROOF.md block | Lean surface | Milestone |
| --- | --- | --- |
| tau / prime characterization (`τ = 2`) | `PGS/Basic.lean` | M1 |
| Deterministic next-prime / weak L_FCL packaging | `PGS/ChamberReset.lean`, `PGS/NextPrime.lean` | M2 |
| Ordered Comparison + Interior Maximizer (GWR) | `PGS/GWR.lean` | M3 |
| Universal bounded compression + Prime-Square Proximity (non-vacuous cutoff `C(n)`) | `PGS/BoundedCompression.lean` | M4 |
| Certified finite bases as named hypothesis bundles | `PGS/FiniteBases.lean` | M5 |

Finite premises (`gwr_finite_base_v1`, `bounded_compression_base_v1`, `residual_k128_v1`) enter Lean as **named packages** with pinned certificate paths and hashes. Lean does not re-run those exhaustions. The only core-path `axiom` is the labeled audit premise `tau_prime_square_eq_three` (CL-003). Core `sorry` count: **zero**.

### Verify the Lean library locally

```bash
# Full mechanical DoD gate (build, smoke, sorry, axiom allowlist, empty-shell scan)
bash scripts/lean4-dod-check.sh

# Or step by step
cd lean-4
lake build
lake env lean smoke-test.lean
```

Toolchain pin: Lean / Mathlib **v4.30.0** (`lean-4/lean-toolchain`).

### Governance and contracts

- [`lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md`](lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md) — audit-only scope, PGS-first frame
- [`lean-4/DEFINITION_OF_DONE.md`](lean-4/DEFINITION_OF_DONE.md) — D1–D7 gates (program exit recorded)
- [`lean-4/README.md`](lean-4/README.md) — build notes and module map

Further analytic discharge of named packages is optional **extension** work (DoD D7.3). It does not reopen the completed core-stack program unless hollow-shell or silent-axiom regressions reappear.

---

## 6. PGS-to-RH Reading Path & Open Questions

The PGS-to-RH argument starts from the same observable object: divisor counts inside prime gaps and endpoint returns to `tau(n)=2`. The bridge coordinate is `H(n) = log n + E(n)`.

```
divisor counts → PGS local theorems → DNI-to-zeta compression
→ source-side residual closure → pole placement / RH sentence
```

`PROOF.md` proves the local source theorems. It does not itself prove the Riemann Hypothesis. `docs/rh/` is a reading path (Tier 3), not an RH proof.  
`docs/rh/` carries the proposed reading path built on that source layer and maintains the current status ledger.

Open questions and unsolved problems are tracked in `pgs-unsolved-problems/`.

---

## A Different Way To Generate Primes

Because the structure inside each gap is so direct, it becomes possible to generate the next prime in a completely different manner from the usual methods.

Traditional prime generators work by proposing candidate numbers and testing them for primality. They reject composites and keep trying until one survives. Even the most efficient sieves or probabilistic tests still follow that propose-test-reject cycle.

The approach in this repository starts from a known prime and reads the factor structure that follows it. Using the divisor-count pattern, it identifies exactly where the next gap must close. The output is therefore tiny and precise:

```json
{"p": 89, "q": 97}
```

That record simply says: start here, the next prime is there. No trial division, no Miller-Rabin rounds, no probabilistic guesses are needed to choose the answer. Verification testing follows as confirmation and is not part of selection, but primality audit is still required. The arithmetic structure itself shows where the gap ends.

The same principle extends to a dedicated Mersenne-prime generator. Instead of starting from an ordinary prime, the Mersenne variant starts from an accepted Mersenne exponent, reads the prime-gap structure around the exponent wall `2^e`, and emits the next exponent whose left boundary lands exactly at `2^e - 1`.

The same structural reading has been extended to RSA moduli as a probe. The runner traverses locked endpoint chains, attempts floor transport and reciprocal closure, and emits a structural certificate or an explicit unresolved state with residual. It scales to curated 40, 50, 64, 128, and 256-bit examples as probe only. The 50-bit row remains unresolved under the v2 runner. The 40-bit and 64-bit rows are audit-confirmed endpoint classes only. See `research/06-cryptology-rsa/`. No RSA-scale resolver theorem is claimed. No factorization claim is made unless a named audit row reports `factor_found=true`.

---

## Where This Leads

Once you begin seeing prime gaps through this lens, many natural follow-up questions arise. You can trace what that first special composite inside each nonempty gap actually means and why it always appears where it does. You can examine the zero-excess normalization that places every prime greater than 1 at exactly `E = 0`, keeps composites at positive excess, and preserves `Z(n) = e^{-E(n)}` as the dual coordinate. You can watch how the same kind of structure repeats across thousands or millions of gaps and begin to model its behavior. You can follow the exact recursive process of walking from prime to prime using only the information carried inside each gap.

Every one of these paths grows from the same simple shift in perspective: stop treating the interior as empty space and start counting what is really there. The numbers themselves do the rest of the work.

---

## Repository Map

- `src/`: Python package (install with `pip install -e ./src/python`)
- `PROOF.md`: Formal proofs and theorem stack (authority for theorem status)
- `docs/core/`: Foundational explanations (GWR, DNI, generative model, recursive walk, etc.)
- `docs/STATUS_TIERS.md`: Proved / Measured / Experimental map (start here for claim status)
- `docs/rh/`: PGS-to-RH reading path and status (reading path, not an RH proof)
- `docs/lean-pgs-verification/`: Public Lean 4 status HTML (core-stack DoD complete)
- `research/`: Deep experiments (RSA engine, Mersenne generator, continuity notes, 00-index/)
- `visualizations/`: Plot library + gallery (primary), explorers, historical dumps (router: `index.html`)
- `lean-4/`: Lean 4 audit mirror of the core stack (M0-M5 DoD). Named finite bases. One core-path axiom.
- `scripts/lean4-dod-check.sh`: One-command Lean build / smoke / inventory gates
- `experiments/`, `scripts/`, `tests/`, `data/`: Supporting code, runs, and artifacts
- `pgs-unsolved-problems/`: Open questions
- `AGENTS.md`: Collaboration contract for agentic work

---

## Reading Further

- `docs/STATUS_TIERS.md`: What is proved, what is measured to 10^18, and what is experimental
- `docs/reframe/AUDIT.md`: Quoted mixture sites that this reframe addresses
- `docs/lean-pgs-verification/index.html`: Lean 4 audit-mirror status surface
- `lean-4/peer/M5_DOD_ACCEPT.md`: Program DoD peer accept (D1–D7)
- `research/00-index/continuity/START_HERE.md`: Continuity and resume entrypoint for future sessions
- `research/00-index/README.md`: Maps the research corpus by chapter and status
- `docs/RESULTS.md`: Measured results and surfaces
- `visualizations/gallery/index.html`: Catalog plot gallery with status chips
- Full list of core documents with one-line purposes appears in `docs/OVERVIEW.md`

---

## Python API

Install the Python package from the repo root:

```bash
python3 -m pip install -e ./src/python
```

The package exposes the core deterministic gap-walking and GWR selection primitives used throughout the research.
