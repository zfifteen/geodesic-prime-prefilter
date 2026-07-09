# Three Kinds of Prime Generators

This document clarifies the fundamental differences between three distinct approaches to generating primes, using concrete implementations as examples.

## 1. Counting-Oracle Indexed (Rust example: haskallcurry/primes)

**Core primitive:** Given an arbitrary index `k`, compute the exact `k`-th prime `p_k`.

**How it works:**
- Maintains a fast combinatorial prime counting function π(x) (Meissel-Lehmer style).
- Uses a good analytic seed (inverse logarithmic integral).
- Binary searches or brackets using repeated π(x) calls until it finds the smallest x where π(x) = k.

**Strengths:**
- Always returns the mathematically exact p_k for any k (within practical range).
- No "near miss", correctness is by construction via the definition of π(x).
- General-purpose for any index.

**Weaknesses:**
- Performance degrades as k grows because each π(x) call becomes more expensive.
- Requires significant engineering for the counting function.

**Example performance (this machine):**
- k = 123,456,789 → ~43 ms
- k = 1,000,000,000 → ~129 ms
- k = 10,000,000,000 → ~961 ms

## 2. Legacy Analytic Density Comparison (Z5D, archived)

**Core primitive:** Given an index `k`, return a high-quality probable prime near the true `p_k`.

**How it works:**
- Calibrated closed-form approximation (PNT base + d(n) and e(n) correction terms).
- Table lookup for exact known values on a small grid (powers of 10 up to 10^18).
- For everything else: evaluate the analytic seed then apply a small forward refinement using a primality library (`gmpy2.next_prime`, GMP `mpz_nextprime`, Java `nextProbablePrime`).

**Strengths:**
- Extremely fast, even at enormous scales (hundreds or thousands of digits in the index).
- The analytic core is O(1) work + small number of primality tests.
- Excellent when you want a very good candidate quickly and can tolerate "near" rather than exact for arbitrary k.

**Weaknesses:**
- Off the published grid it does **not** guarantee the exact p_k: only a probable prime near it.
- The distance to the true p_k grows as you move away from the calibration points (though the error remains small in relative terms for the scales tested).

**Example performance (this machine):**
- k = 123,456,789 → ~3 ms (exact via grid or very close)
- k = 1,000,000,000 → ~3 ms (exact via table)
- Works in low milliseconds even for k with 100+ digits.

## 3. Structural Gap-Chamber Successor (PGS C: this project)

**Core primitive:** Given a starting integer `n` (typically a known prime), find the immediate next prime after it using the internal arithmetic structure of the gap.

**How it works:**
- Treats the interval after `n` as a structured object whose divisor-count field contains the information needed to locate the endpoint.
- Combines:
  - Small-factor sieving / wheel closure (GMP-based).
  - Higher-level gap-structure rules (chambers, carriers, "leftmost minimum divisor count", GWR/NLSC-style reset logic derived from Prime Gap Structure theory).
- Searches within a bounded candidate window.
- Returns the exact next prime when the structural rules resolve inside the bound. Errors with "unresolved" rather than guessing if it cannot.

**Strengths:**
- Deterministic and exact for successor when it resolves.
- Avoids general primality testing in the production path by exploiting local multiplicative structure.
- Designed for high-scale work (the theory and some certified paths target extremely large numbers).

**Weaknesses:**
- Currently a **successor** engine, not a native indexed engine. It does not directly answer "what is the k-th prime?"
- Resolution is bounded. At sufficient scale or with default bounds it can return unresolved (observed around 10^20 in testing).
- The general (non-certified) path still performs a bounded search rather than a pure O(1) structural jump in all cases.

**Example performance (this machine, successor after known primes):**
- After p ≈ 10^9 → ~19 ms
- After p ≈ 10^10 → ~43 ms
- After p ≈ 10^11 → ~111 ms
- After p ≈ 10^12 → ~338 ms

At ~1.12 × 10^20 it returned "PGS chamber unresolved" with default candidate bound.

## Summary Table

| Aspect                    | Rust (Counting-Oracle)      | Z5D (Legacy Analytic Density)     | PGS C (Structural Successor)      |
|---------------------------|-----------------------------|-----------------------------------|-----------------------------------|
| Primary operation         | Exact p_k for any k        | Predict probable prime near p_k  | Exact next prime after p         |
| Exactness for arbitrary k | Always exact               | Only on small grid; else "near"  | N/A (successor only)             |
| Speed at 1e9 to 1e10 scale   | 40 to 150 ms                  | ~3 ms                            | 19 to 40 ms (successor)             |
| Behavior at 10^20+        | Slow / expensive π(x)      | Still fast (analytic)            | Can unresolved with current bounds |
| Core technique            | Prime counting + search    | Calibrated closed form + refinement | Gap structure + bounded chamber rules |
| Dependencies in hot path  | None (pure counting)       | MPFR/GMP or gmpy2                | GMP + structural rules           |

## Key Insight

These are not three implementations of the same thing. They are three different **kinds** of prime generators:

- One counts globally.
- One predicts analytically.
- One reads local gap structure.

Your PGS generator belongs firmly in the third category. It is not "failing" at being a fast exact indexed finder, it is solving a different, structural problem. This distinction is important both for technical evaluation and for public positioning.

---

*Document created to capture the category distinction clearly.*