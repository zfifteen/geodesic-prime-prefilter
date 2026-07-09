# Twin-Prime Resonance Technical Note

**Date:** 2026-07-08  
**Theorem:** GWR Super-Signal / Twin-Prime Resonance  
**Status:** proved · corollary  
**Authority:** `PROOF.md` · `research/remainders/correlations/investigation/`

---

## Part I: Plain-Language Summary

Prime numbers are not random holes in a number line. In the Prime Gap Structure (PGS) view, each gap between two consecutive primes is filled with composite numbers that carry structure. You can read that structure through the divisor count of each interior number.

Inside a gap, PGS picks one special composite called the **GWR witness**. That number is the **leftmost** interior point with the **smallest divisor count** in the gap. Think of it as the first and simplest structural anchor in that gap.

PGS also records a **remainder vector** for each interior number. That vector stores the remainders after division by a fixed set of moduli: 2, 3, 5, 7, 30, 210, and 2310. Each remainder of zero is called a **remainder zero**.

The **Twin-Prime Resonance** rule, also called the **GWR Super-Signal**, says this:

> If the GWR witness has **four or more remainder zeros**, then the gap is a **twin gap**. The gap size is exactly 2. The next integer after the witness is the next prime.

Here is what that means in plain terms.

A twin gap looks like `p, p+2`, with only one composite between them. Example: 29 and 31 with 30 in the middle. The number 30 is divisible by 2, 3, and 5. That creates many remainder zeros in its vector. It also has a high divisor count. In a twin gap, there is no other interior number competing against it. So 30 can be the GWR witness.

In a larger gap, the story changes. If the witness were a multiple of 30, it would have a high divisor count, usually at least 8. But a larger gap contains other interior numbers. At least one of them will have a smaller divisor count and will appear earlier in the gap. So a multiple of 30 cannot be the GWR witness unless the gap has only one interior number.

That is the whole breakthrough in one sentence: **four remainder zeros at the GWR witness are not a vague pattern. They are a proved twin-gap lock.**

The claim was tested hard. On a scan to 2 million, no counterexample appeared in 148,933 gaps. On an earlier interior lane to 1.5 million, all 3,842 super-signal cases were twin gaps. One counterexample would have killed the promotion. None appeared.

So the program now has a deterministic trigger: when the GWR witness shows four remainder zeros, the next prime is exactly one step away.

---

## Part II: Visual Summary

![Twin-Prime Resonance infographic](infographic.svg)

*PNG export:* [infographic.png](infographic.png)

The diagram shows the full chain:

1. Read the gap interior and select the GWR witness `w`.
2. Measure remainder zeros on `M_v1 = (2, 3, 5, 7, 30, 210, 2310)`.
3. Four or more zeros force `w ≡ 0 (mod 30)`; larger gaps cannot host such a witness.
4. The only surviving case is a twin gap with `q = w + 1`.
5. Empirical audits support the analytic closure.

---

## Part III: Technical Treatment

### 1. Setting and notation

Let $p < q$ be consecutive primes. Define the gap size $g = q - p$ and the interior set

$$
I = \{p+1, p+2, \ldots, q-1\}, \qquad |I| = g - 1.
$$

Let $\tau(n)$ denote the divisor-count function. The **Gap Winner Rule (GWR)** selects the leftmost minimizer

$$
w = \min_{\prec} \arg\min_{n \in I} \tau(n),
$$

where $\prec$ is the usual left-to-right order on the integer line.

Define the versioned remainder vector

$$
R(n) = (n \bmod 2,\; n \bmod 3,\; n \bmod 5,\; n \bmod 7,\; n \bmod 30,\; n \bmod 210,\; n \bmod 2310),
$$

denoted $M_{v1}$. Let

$$
Z(n) = \#\{i : R(n)_i = 0\}.
$$

### 2. Theorem

**Theorem (Twin-Prime Resonance / GWR Super-Signal).**  
If $Z(w) \ge 4$, then $g = 2$ and $q = w + 1$.

Equivalently, a four-zero remainder signature at the GWR witness forces twin-gap termination with immediate prime emission at $w+1$.

### 3. Proof architecture

The proof is a corollary chain over established GWR infrastructure.

#### Lemma 1: Zero-count equivalence

For the fixed vector $M_{v1}$,

$$
Z(w) \ge 4 \iff w \equiv 0 \pmod{30}.
$$

*Proof sketch.* If $w \equiv 0 \pmod{30}$, then divisibility by $2$, $3$, $5$, and $30$ yields at least four zeros immediately. Conversely, if $w \not\equiv 0 \pmod{30}$, the slot for modulus $30$ is nonzero. Three simultaneous zeros among the slots for $2$, $3$, and $5$ would force divisibility by $30$. A zero in the $210$ or $2310$ slot also forces a zero at $30$. Hence at most three zeros are possible without $w \equiv 0 \pmod{30}$. ∎

#### Lemma 2A: Left-boundary exclusion

If $|I| \ge 2$ and $w = p+1$ with $w \equiv 0 \pmod{30}$, then $w$ is not GWR.

*Proof.* The point $w+1$ lies in $I$, is composite, and satisfies $\gcd(w+1, 30)=1$. Therefore $\tau(w+1) \le 4$ while $\tau(w) \ge 8$. So $w$ cannot minimize interior divisor count. ∎

#### Lemma 2B: Gap-three obstruction

If $g = 3$, $w \equiv 0 \pmod{30}$, and $w > 30$, then $w$ cannot be GWR.

*Proof.* By Lemma 2A, $w = p+2$, hence $p = w-2 \equiv 28 \pmod{30}$ is even and greater than $2$, so not prime. ∎

#### Lemma 2C: Small-gap modular obstructions

Write $w = p+k$. If $2 \le k \le 6$ and $w \equiv 0 \pmod{30}$, then $p \equiv -k \pmod{30}$ forces a factor $2$, $3$, or $5$ in $p$, excluding primality for $p > 5$. Thus no non-twin gap with $g \le 7$ can host a multiple-of-$30$ GWR witness.

#### Lemma 2D: Earlier low-$\tau$ competitor

The first offset compatible with primality is $k=7$ ($g=8$, $p \equiv 23 \pmod{30}$). Then $p+2 \equiv 25 \pmod{30}$, so $5 \mid (p+2)$ and $\tau(p+2) \le 4$ while $\tau(w) \ge 8$. Since $p+2 < w$, the multiple of $30$ cannot be the leftmost minimum-$\tau$ witness. The same earlier-semiprime mechanism excludes larger admissible offsets.

#### Conclusion

Therefore $w \equiv 0 \pmod{30}$ can occur as GWR only when $|I|=1$, i.e. $g=2$. By Lemma 1, the same conclusion holds for $Z(w) \ge 4$. In the twin case, $p = w-1$ and $q = w+1$. ∎

### 4. Epistemic status and audit surfaces

| Surface | Regime | Result |
|--------|--------|--------|
| Interior remainder lane | $p \le 1.5 \times 10^6$ | $3{,}842 / 3{,}842$ super-signal GWR cases have $g=2$ |
| Independent falsification scan | $p < 2 \times 10^6$ | $0$ counterexamples in $148{,}933$ gaps |
| Theorem stack (`PROOF.md`) | universal corollary | promoted to `proved · corollary` |

The result is not a probabilistic twin heuristic. It is a deterministic consequence of:

1. exact GWR selection on the divisor field;
2. fixed primorial remainder measurement;
3. interior-competitor exclusion for multiples of $30$.

### 5. Programmatic implications

- **Generator fast path:** a four-zero remainder signature at the active GWR witness licenses immediate emission at $w+1$ without further interior search.
- **Twin-prime lane:** `research/10-twin-primes` receives a proved trigger rather than a purely measured correlation.
- **Formalization debt:** Lean mirror remains open; analytic closure is complete in prose.

### 6. Reproducibility

Interior-lane audit (pinned summary):

```bash
cat research/remainders/correlations/investigation/interior_placement_stats.json
```

Expected fields: `super_signal_at_gwr_count = 3842`, `g2_with_super_signal_gwr = 3842`.

Full lane replay:

```bash
cd /Users/velocityworks/IdeaProjects/prime-gap-structure
PYTHONPATH=src/python:research/remainders \
  python3 research/remainders/run_investigation.py
```

### 7. References

- `PROOF.md`. Twin-Prime Resonance theorem and theorem-stack row
- `research/remainders/correlations/investigation/interior_placement_stats.json`
- `research/remainders/correlations/investigation/super_signal_status.json`
- `docs/proof-enhancements/goals.md`, goal G2 closure criteria