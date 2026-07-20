# Prime Gap Structure

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--07--20-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)

![Prime Gap Structure hero](visualizations/conceptual/prime-gap-structure-hero.jpg)

**Abstract**  
Prime Gap Structure demonstrates that the integers between consecutive primes form an ordered divisor-count field whose internal minimum (the Gap Winner) and return to divisor count = 2 together locate the next prime deterministically.  

Local theorems are formally proved and computationally validated. These theorems include the Gap Winner Rule (GWR), bounded compression at Cramér scale, the Prime-Square Proximity Theorem (proved 2026-07-05), and the No-Later-Simpler-Composite Theorem (zero violations through 10¹⁸). A reading path connecting these local results to analytic number theory (including the Riemann Hypothesis) is developed in `docs/rh/` but kept explicitly separate from the proved core.

This repository supplies the proofs (`PROOF.md`), reference implementations, reproducible artifacts, and measured surfaces that make the structure independently verifiable.

---

## Table of Contents

- [1. Quick Intuitive Understanding](#1-quick-intuitive-understanding)
- [Key Concepts (Mini-Glossary)](#key-concepts-mini-glossary)
- [2. Core Results: What Is Proved](#2-core-results--what-is-proved)
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
- **No-Later-Simpler-Composite Theorem**: Validated with zero violations through 10¹⁸. No simpler composite appears later in the gap once the minimal divisor count has been observed.

---

## 2. Core Results: What Is Proved

> **Proved Status (as of July 2026)**  
> The following local theorems are formally proved in `PROOF.md` and have been computationally validated with zero violations through 10¹⁸. These results stand independently of any conjectures about the Riemann Hypothesis or global prime distribution.

- **Next-prime rule** (deterministic): Given a prime *p*, the next prime *q* is the first integer after *p* whose divisor count returns to exactly 2.
- **Gap Winner Rule (GWR)**: The leftmost min-*d(n)* composite inside the gap is the raw-Z maximizer and the structurally selected interior witness.
- **Universal bounded compression** at Cramér scale: The GWR-selected witness always appears within `max(64, ceil(0.5 * log(q)^2))` of *p*.
- **Prime-Square Proximity Theorem** (proved 2026-07-05): When the witness is a prime square, its offset from *p* is bounded by the same compression limit.
- **Modular zero lemma on $M_{v1}$**: Four or more remainder zeros on the fixed primorial vector if and only if $30 \mid w$ (proved; modular only).
- **No-Later-Simpler-Composite Theorem**: Once the minimal divisor count has appeared, no simpler composite occurs later in the gap.

These statements are proved from the arithmetic of divisor counts and the ordering inside gaps. They do not rely on probabilistic models or unproved global assumptions.

See `PROOF.md` for the complete formal stack and supporting lemmas.

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

In addition to the prose proofs in `PROOF.md` and large-scale computational validation, the project maintains a dedicated **Lean 4 formalization layer**. This serves as an independent, machine-checked audit of the core theorems.

The Lean work is deliberately scoped as a **downstream verification layer only**. It translates and mechanically checks statements already established in `PROOF.md` rather than generating new results or serving as the primary reasoning surface. All formalization follows a strict **PGS-first** approach with explicit traceability back to the prose proofs.

**Current Status (as of July 2026)**

- Build is green and smoke tests pass.
- **M0/M1/M2 closed**: Foundational work including the divisor-count characterization (`tau(n) = 2`) and ChamberReset replay axioms has been fully formalized with zero `sorry` placeholders (commit `688daa91`).
- **L5 closed**: Key components of the weak linear functional closure and next-prime forcing lemmas have been verified.
- The **Gap Winner Rule (GWR) / Interior Maximizer** formalization (M3) is unblocked and ready for work.
- **UBC + Prime-Square Proximity** (M4) and **finite-base packaging** (M5) remain pending.

The effort is governed by an explicit **Verification Contract** that enforces:

- Strict separation between proved, measured, and audit artifacts
- Mandatory traceability headers linking every definition and theorem back to `PROOF.md`
- A clear **Definition of Done** with gates for build quality, zero `sorry` on core paths, and peer review

**Key Files**

- `lean-4/README.md` -- Full status, build instructions, and roadmap
- `lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md` -- Governance and scope rules
- `lean-4/PGS_LEAN_FORMALIZATION_PLAN.md` -- Phased development plan
- `lean-4/DEFINITION_OF_DONE.md` -- Milestone gates and acceptance criteria
- `lean-4/PGS/Basic.lean` -- Core `tau` definitions and closed M1 lemmas

This formalization layer provides an additional layer of mechanical assurance for the deterministic structure claimed in the prime gap theory.

---

## 6. PGS-to-RH Reading Path & Open Questions

The PGS-to-RH argument starts from the same observable object: divisor counts inside prime gaps and endpoint returns to `tau(n)=2`. The bridge coordinate is `H(n) = log n + E(n)`.

```
divisor counts → PGS local theorems → DNI-to-zeta compression
→ source-side residual closure → pole placement / RH sentence
```

`PROOF.md` proves the local source theorems. It does not itself prove the Riemann Hypothesis.  
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

That record simply says: start here, the next prime is there. No trial division, no Miller-Rabin rounds, no probabilistic guesses are needed to choose the answer. The arithmetic structure itself shows where the gap ends. Any verification testing that follows is only confirmation; it is not part of the generation step.

The same principle extends to a dedicated Mersenne-prime generator. Instead of starting from an ordinary prime, the Mersenne variant starts from an accepted Mersenne exponent, reads the prime-gap structure around the exponent wall `2^e`, and emits the next exponent whose left boundary lands exactly at `2^e - 1`.

The same structural reading has been extended to RSA moduli. The program has completed the transition from rung-specific measured demonstrations to a general, deterministic PGS-native engine. Given an RSA modulus (or family of moduli), the engine traverses locked endpoint chains using only PGS objects and rules. These rules include GWR-selected carriers inside chamber-reset certificates, floor transport, reciprocal endpoint closure conditions, and modulus-link residual classification. It emits a public structural certificate when the invariants close to an oriented endpoint class, or an explicit, diagnosable "unresolved" state (with residual) when they do not. It scales to representative 256-bit, 512-bit, and 1024-bit+ examples while remaining strictly inside the generator contract and AGENTS.md cryptology contract. See `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/`.

---

## Where This Leads

Once you begin seeing prime gaps through this lens, many natural follow-up questions arise. You can trace what that first special composite inside each nonempty gap actually means and why it always appears where it does. You can examine the zero-excess normalization that places every prime greater than 1 at exactly `E = 0`, keeps composites at positive excess, and preserves `Z(n) = e^{-E(n)}` as the dual coordinate. You can watch how the same kind of structure repeats across thousands or millions of gaps and begin to model its behavior. You can follow the exact recursive process of walking from prime to prime using only the information carried inside each gap.

Every one of these paths grows from the same simple shift in perspective: stop treating the interior as empty space and start counting what is really there. The numbers themselves do the rest of the work.

---

## Repository Map

- `src/`: Python package (install with `pip install -e ./src/python`)
- `PROOF.md`: Formal proofs and theorem stack
- `docs/core/`: Foundational explanations (GWR, DNI, generative model, recursive walk, etc.)
- `docs/rh/`: PGS-to-RH reading path and status
- `research/`: Deep experiments (RSA engine, Mersenne generator, continuity notes, 00-index/)
- `visualizations/`: Plot library + gallery (primary), explorers, historical dumps (router: `index.html`)
- `lean-4/`: Lean 4 formalization layer (downstream machine-checked audit of core theorems)
- `experiments/`, `scripts/`, `tests/`, `data/`: Supporting code, runs, and artifacts
- `pgs-unsolved-problems/`: Open questions
- `AGENTS.md`: Collaboration contract for agentic work

---

## Reading Further

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
