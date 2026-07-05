# Prime Gap Structure

![Prime Gap Structure hero](visualizations/conceptual/prime-gap-structure-hero.jpg)

This is not a repository of conjectures or informal observations. It provides:

- Formal proofs (see [PROOF.md](PROOF.md)): the direct next-prime rule, the interior maximizer (GWR), and universal bounded compression at Cramér scale — including the Prime-Square Proximity Theorem (proved 2026-07-05)
- Working code and reference implementations
- Reproducible artifacts, measured surfaces, and audit data that others can independently run and validate

Visualizations of the core objects (the divisor-count row, GWR selection, ridges, U_□ diagrams, conceptual rulers, interactive explorers, and video narrations) live in [visualizations/](visualizations/index.html).

## The First Contradiction

Most people learn that prime numbers are fundamentally unpredictable. They appear to pop up at irregular intervals, almost as if they are scattered at random across the number line. Textbooks and popular explanations reinforce this view: primes become rarer as numbers grow larger, the gaps between them can be arbitrarily wide, and there is no simple formula that will always tell you exactly where the next one sits. The common belief is that the only practical ways to find the next prime are to test candidates one by one or to rely on probabilistic estimates. Prime gaps themselves are treated as empty stretches of composites, nothing more than the boring distance you have to cross before the next interesting number arrives.

That picture feels natural because it matches everyday experience with large numbers. When you look at a long stretch of integers, most of them are obviously composite, and the primes seem to hide without any clear signal. The word "gap" itself nudges us to think of the space between two primes as meaningless background noise.

The truth is the exact opposite.

Start with one prime. Look at the integers that come right after it. Those integers are not random obstacles. They carry precise factor structure, and that structure is exactly what determines where the next prime must appear. The next prime can be found directly by reading the numbers that follow the one you already have. Nothing is left to chance or probability once you know how to look.

***

At first glance, what follows can read like a mere tautology: the next prime is the first later integer whose divisor count is exactly two. That definition is only the endpoint. Prime Gap Structure studies the arithmetic before the endpoint: the ordered divisor-count field inside the gap, the selected interior minimum, the zero-excess coordinate that places primes and composites on one scale, and the measured chamber patterns that survive far beyond the toy examples.

***

## Look Between 23 and 29

It helps to see this idea with a small, concrete example so you can watch the pattern unfold step by step.

Take the primes 23 and 29. They are consecutive, which means every integer between them is composite. Write them out and you get this simple picture:

23 | 24 25 26 27 28 | 29

At first glance the gap looks like nothing but a distance of six. That is what most people notice, and it is why the middle feels empty. But stop and look more closely at what is actually sitting inside that interval. Each of those five composites has its own complete list of positive divisors. When you count how many divisors each one has, something changes in how you see the gap.

Here is the same interval again, but now with the divisor counts written underneath:

number:        24  25  26  27  28
divisor count:  8   3   4   4   6

The numbers themselves have not changed. What has changed is that we are now seeing an ordered list of divisor counts. Among those counts the smallest value is 3, and it appears at the very first position where it can, at the number 25.

That single observation is surprising because it contradicts the idea that the interior is meaningless. Instead of empty space, the gap now has an internal shape that is completely determined by ordinary arithmetic. The lowest divisor count inside the gap is not hidden or random; it emerges clearly once you simply count.

## When The Lowest Count Appears Multiple Times

One small gap could be a lucky coincidence. To see that the pattern is reliable, it is useful to look at another example where the situation is a little less tidy.

Consider the gap from 89 to 97:

89 | 90 91 92 93 94 95 96 | 97

Again the interior numbers are all composite. Their divisor counts are:

number:        90  91  92  93  94  95  96
divisor count: 12   4   6   4   4   4  12

This time the smallest count inside the gap is 4. Notice that 4 appears four different times, at 91, 93, 94, and 95. Yet when you read the list from left to right, the very first time that lowest count of 4 shows up is at 91.

The same principle that appeared in the smaller gap is still at work. Inside any prime gap with at least one interior number, there is always a first interior number that carries the lowest divisor count. The gap is telling you two things at once: what the lowest count is and exactly where that count first occurs. The pattern is not fragile; it survives even when the lowest count repeats.

What makes this observation powerful is that it comes directly from counting ordinary arithmetic properties that anyone can verify by hand. No advanced machinery is required. The numbers themselves reveal the structure the moment you look at them this way.

## How The Gap Ends

So far we have focused on the interior of the gap. Now shift your attention to the right-hand edge, where the gap actually closes.

Recall what makes a number prime: it has exactly two positive divisors, 1 and itself. Every composite number has at least three. If you start at any known prime and simply read forward through the integers, every composite you encounter will have a divisor count strictly greater than 2. The next prime is the first number after your starting prime whose divisor count drops to exactly 2.

Return to the 23-to-29 gap and extend the divisor-count list one more step:

number:        24  25  26  27  28  29
divisor count:  8   3   4   4   6   2

You can watch the count stay safely above 2 through the entire interior. Then, at 29, it becomes exactly 2 and the gap ends. The endpoint is not chosen by trial and error or by guessing; it is the inevitable place where the divisor count first reaches 2 after the starting prime.

This is why the interior and the endpoint belong together. They are two parts of the same continuous story told by the same ordered list of divisor counts.

## Interior And Endpoint Together

Once you see the gap as a single ordered sequence rather than a meaningless jump, the whole picture snaps into focus. The [selected composite](LEFTMOST_MINIMUM_DIVISOR_RULE.md) inside the gap (the first interior number with the lowest divisor count) and the endpoint prime (the first later number with divisor count exactly 2) are both visible in the same list. They are not separate phenomena; they are the natural consequences of reading the factor structure that sits between two consecutive primes.

For the gap from 23 to 29 the selected composite is 25 and the endpoint is 29. For the gap from 89 to 97 the selected composite is 91 and the endpoint is 97. In every case the arithmetic inside the gap carries the information that points directly to the next prime.

This is the larger reversal the repository explores. A prime gap is no longer just a size or a distance. It has a clear internal shape, a selected composite that marks the lowest point inside that shape, and a right endpoint that is fixed by the divisor count returning to 2. The middle is not meaningless; it is full of information. The usual story treats the numbers between primes as an obstacle. Here they are the evidence.

## Bounded Compression at the Cramér Scale

Prime gaps are not only ordered — their interiors are **compressed**. For every consecutive prime gap with nonempty interior, the first interior integer with minimum divisor count (the GWR-selected witness) appears within

```text
max(64, ceil(0.5 * log(q)^2))
```

of the left endpoint. This bound sits at the scale of Cramér's conjecture. It is proved deterministically from divisor-count structure, not assumed from random models.

The final piece — the **Prime-Square Proximity Theorem** — closed on 2026-07-05: when the selected witness is a prime square `r^2`, the distance `r^2 - p` cannot exceed that cutoff without forcing a modulus-link collision in the composite rows beneath `r`.

This is a proved bound on the selected-witness offset. It does not by itself prove the Riemann Hypothesis, the Prime Number Theorem, or every classical formulation of Cramér's conjecture for raw gap size `q - p`. See [PROOF.md](PROOF.md) for the full theorem stack and boundaries.

The preferred coordinate for that same reading is now zero excess. For an integer `n > 1`, the Divisor Normalization Identity writes

$$E(n)=\left(\frac{d(n)}{2}-1\right)\ln n$$

Primes greater than `1` are exactly the zero-excess floor, `E(n)=0`. Composites sit above that floor. The older `Z` score remains the exact dual coordinate:

$$Z(n)=e^{-E(n)}$$

So the statement "primes greater than `1` sit at `Z = 1.0`" and the statement "primes greater than `1` have zero excess" are the same normalization read in opposite coordinates.

## PGS-To-RH Reading Path

The PGS-to-RH argument starts from the same observable object: divisor counts
inside prime gaps and endpoint returns to `tau(n)=2`. Read
[docs/rh](docs/rh/README.md) for the downstream RH chain, where the bridge
coordinate is `H(n)=log n+E(n)`:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-side residual closure -> pole placement/RH sentence
```

`PROOF.md` proves the local source theorems. It does not itself prove RH.
`docs/rh` carries the RH reading path built on that source layer.

## A Different Way To Generate Primes

Because the structure inside each gap is so direct, it becomes possible to [generate the next prime](PRIME_GAP_GENERATOR.md) in a completely different manner from the usual methods.

Traditional prime generators work by proposing candidate numbers and testing them for primality. They reject composites and keep trying until one survives. Even the most efficient sieves or probabilistic tests still follow that propose-test-reject cycle.

The approach in this repository starts from a known prime and reads the factor structure that follows it. Using the divisor-count pattern, it identifies exactly where the next gap must close. The output is therefore tiny and precise:

{"p": 89, "q": 97}

That record simply says: start here, the next prime is there. No trial division, no Miller-Rabin rounds, no probabilistic guesses are needed to choose the answer. The arithmetic structure itself shows where the gap ends. Any verification testing that follows is only confirmation; it is not part of the generation step.

The same principle extends to a dedicated [Mersenne-prime generator](research/09-exponents/README.md). Instead of starting from an ordinary prime, the Mersenne variant starts from an accepted Mersenne exponent, reads the prime-gap structure around the exponent wall `2^e`, and emits the next exponent whose left boundary lands exactly at `2^e - 1`. This is a remarkable lift of the core method: the generator is not looking up known Mersenne primes or asking a primality oracle to find them. It is reading the local divisor-count structure of the wall and producing the next Mersenne exponent as a direct PGS successor.

The same structural reading has been extended to RSA moduli. The program has completed the transition from rung-specific measured demonstrations to a general, deterministic PGS-native engine. Given an RSA modulus (or family of moduli), the engine traverses locked endpoint chains using only PGS objects and rules — GWR-selected carriers inside chamber-reset certificates, floor transport, reciprocal endpoint closure conditions, and modulus-link residual classification — and emits a public structural certificate when the invariants close to an oriented endpoint class, or an explicit, diagnosable "unresolved" state (with residual) when they do not. It scales to representative 256-bit, 512-bit, and 1024-bit+ examples while remaining strictly inside the generator contract and AGENTS.md cryptology contract. See `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/`.

## Where This Leads

Once you begin seeing prime gaps through this lens, many natural follow-up questions arise. You can trace what that first special composite inside each nonempty gap actually means and why it always appears where it does. You can examine the [zero-excess normalization](DIVISOR_NORMALIZATION_IDENTITY.md) that places every prime greater than `1` at exactly `E = 0`, keeps composites at positive excess, and preserves `Z(n)=e^{-E(n)}` as the dual coordinate. You can watch how the same kind of structure repeats across thousands or millions of gaps and begin to [model its behavior](PRIME_GAP_GENERATIVE_MODEL.md). You can follow the [exact recursive process of walking from prime to prime](RECURSIVE_PRIME_WALK.md) using only the information carried inside each gap.

Every one of these paths grows from the same simple shift in perspective: stop treating the interior as empty space and start counting what is really there. The numbers themselves do the rest of the work.

## Reading Further

The rest of the repository develops these ideas in greater depth, including the [measured results and surfaces](RESULTS.md).

- [research/00-index/continuity/START_HERE.md](research/00-index/continuity/START_HERE.md) is the continuity and resume entrypoint for future Codex sessions.
- [research/00-index/README.md](research/00-index/README.md) maps the research corpus by chapter and status.
- [PROOF.md](PROOF.md) gives the formal proofs of the next-prime rule, the interior maximizer, and universal bounded compression — including the Prime-Square Proximity Theorem (2026-07-05).
- [docs/rh](docs/rh/README.md) gives the PGS-to-RH reading path and status ledger.
- [LEFTMOST_MINIMUM_DIVISOR_RULE.md](LEFTMOST_MINIMUM_DIVISOR_RULE.md) explores the rule that identifies the special composite inside each gap.
- [DIVISOR_NORMALIZATION_IDENTITY.md](DIVISOR_NORMALIZATION_IDENTITY.md) explains the zero-excess normalization and its dual `Z(n)=e^{-E(n)}` coordinate.
- [PRIME_GAP_GENERATOR.md](PRIME_GAP_GENERATOR.md) describes how the generator reads the structure.
- [PRIME_GAP_GENERATIVE_MODEL.md](PRIME_GAP_GENERATIVE_MODEL.md) and [RECURSIVE_PRIME_WALK.md](RECURSIVE_PRIME_WALK.md) examine the broader model and recursive behavior.
- [RESULTS.md](RESULTS.md) presents the measured results and surfaces.
- The general PGS-native RSA endpoint engine lives in [research/06-cryptology-rsa/experiments/live-solver/rsa-v2/](research/06-cryptology-rsa/experiments/live-solver/rsa-v2/).

## Python API

Install the Python package from the repo root:

```bash
python3 -m pip install -e ./src/python
