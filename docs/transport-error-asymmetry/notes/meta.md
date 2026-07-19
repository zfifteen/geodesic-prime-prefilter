This is an important claim to audit carefully, and your repo context helps. I pulled `zfifteen/prime-gap-structure` - its core objects are the ordered divisor-count field inside prime gaps, the Gap Winner Rule (leftmost min-$d(n)$ carrier), and the Divisor Normalization Identity DNI.

Your "Transport Error Asymmetry" report does not show a new RSA law. It shows a correct arithmetic calculation wrapped in a causal story that does not follow.

Here is the technical audit:

### 1. What your data point actually is

You report:

* $w_L = 1,048,572$, $w_U = 1,048,574$, $E_{gap}=2$
* $\lfloor N / w_L \rfloor = 1,048,575$
* $\lambda(C_L)=d(w_L)=96$, $\lambda(C_U)=d(w_U)=4$

Verification:

* $1,048,572 = 2^2 \cdot 3^3 \cdot 7 \cdot 19 \cdot 73$ -> $d = (2+1)(3+1)2\cdot2\cdot2 = 96$
* $1,048,574 = 2 \cdot 524287$ where $524287 = 2^{19}-1$ is prime -> $d=4$

That part is correct.

From $\lfloor N / w_L \rfloor = 1,048,575$ we can recover $N$:

$N \in [ w_L \cdot 1,048,575,\; w_L \cdot 1,048,576 -1 ] = [1,099,506,384,900,\; 1,099,507,433,471]$

Note $\sqrt{N} \approx 1,048,573.5$. You are operating exactly at the square root, as in Fermat factoring. $w_L \cdot w_U = 1,099,505,336,328$, so $N$ was chosen to be $w_L$ times $(w_U+1)$.

Then transport error is forced by arithmetic:

$$ \text{error} = \left\lfloor \frac{N}{w_L} \right\rfloor - w_U = \left\lfloor \frac{w_L w_U + \Delta}{w_L} \right\rfloor - w_U = \left\lfloor \frac{\Delta}{w_L} \right\rfloor $$

If you set $N = w_L(w_U+1) + r$ with $0 \le r < w_L$, the error is 1 by construction. No divisor function is involved in that division.

### 2. The DNI is algebraically tautological

You define:

$$\kappa(n) = \frac{d(n) \ln n}{e^2}, \quad v = \frac{e^2}{2}$$

$$Z(n) = \frac{n}{\exp(v\kappa(n))} = \frac{n}{\exp\left(\frac{d(n)\ln n}{2}\right)} = \frac{n}{n^{d(n)/2}} = n^{1-d(n)/2}$$

$$E(n) = -\ln Z(n) = \left(\frac{d(n)}{2}-1\right)\ln n$$

The "beautiful cancellation" is not a discovery, it is how $v$ was chosen. $e^2$ cancels by design. The consequence:

* If $d(n)=2$ (prime), $E=0$, $Z=1$
* If $d(n)>2$ (composite), $E>0$, $Z<1$

This is a monotone transform of $d(n)$. It restates "primes have 2 divisors" in exponential coordinates. It does not predict $d(n)$.

Your values:

* $E(1,048,572) = (96/2-1)\ln(1,048,572) \approx 651.5$
* $E(1,048,574) = (4/2-1)\ln(1,048,574) \approx 13.86$

High excess = high divisor count. That is true by definition, not a mechanical force pushing a reciprocal.

### 3. Why divisor asymmetry does not lock transport error

The report states: when lock-label differential is maximal (96 vs 4), transport error is deterministically pinned to the ceiling, ratio 1.0.

Problems:

**a) One point cannot falsify randomness.** You claim this falsifies "uniformly distributed noise." To show pinning, you need a distribution across many $N$ showing $P(\text{error}=max | d_{diff} > T) = 1$ with $T$ large, vs $P(\text{error}=max | d_{diff} \text{ small}) < 1$. With $E_{gap}=2$, any non-zero error already gives ratio 0.5 or 1.0. This is a small-number effect.

**b) No causal link.** $\lfloor N / w_L \rfloor$ depends only on $N$ and $w_L$. $d(w_L)$ does not enter the CPU's integer division. Correlation you see is because numbers near $2^{20}=1,048,576$ that are highly divisible by small primes naturally have large $d(n)$. $1,048,572$ is divisible by $4, 27, 7...$ because you are $4$ below a power of two. That also makes $w_L$ close to $\sqrt{N}$. Proximity to sqrt drives the transport error, not $d(n)$.

**c) RSA regime mismatch.** In real RSA, true carriers are primes: $d(p)=d(q)=2$, so $\lambda(C_L)=\lambda(C_U)=2$, differential $0$. Your example uses composite carriers (96 and 4 divisors). Those can never be valid RSA factors. An RSA-v2 certificate that tests mutual closure between composite $w_L, w_U$ is not testing RSA factorization, it is testing composites near sqrt. If $w_L$ actually divides $N$, then $\lfloor N/w_L \rfloor = N/w_L$ exactly, error $0$, regardless of divisor count.

The table in section 2.1 lists Predicate A and Proposed Structural Rule with the same mathematical expression $\lfloor N / w_L \rfloor - w_U$. There is no new predicate to evaluate.

### 4. The Mirror and the Lock analogy

The mirror (reciprocal transport $N/w_L$) is indeed not flat, it has curvature $N/x$. The floor introduces at most $1$ error. The lock (divisor count) does not shape the mirror. A better analogy: you painted the balls with different colors (96 vs 4 divisors) after throwing them, then noticed the red ball landed at the edge, and concluded red paint steers the ball.

### 5. Significance and Impact for RSA-v2

**Current significance: low.**

* Does not replace a 1.2x safety net, because no production RSA implementation uses a heuristic safety net for $\lfloor N / w \rfloor$, it computes it exactly in one integer division.
* Does not enable structural rejection of false positives beyond what trial division already does: if $N \bmod w_L \neq 0$, $w_L$ is not a factor. $d(w_L)$ is irrelevant.
* Does not generalize to 2048-bit RSA. At 40-bit static scale you are at $10^{12}$. RSA-2048 is at $10^{616}$. Behavior of $d(n)$ at $2^{20}$ does not predict behavior at $2^{1024}$.

**What would make it significant:**

1. Formalize: "For $N$ in $[2^{2k-1},2^{2k})$, define $T(N,w_L)= \lfloor N/w_L \rfloor - w_U$. Define $\Delta d = |d(w_L)-d(w_U)|$. Show $E[T | \Delta d]$ is monotonic with $\Delta d$ across $>10^6$ random $N$."
2. Show it holds when $w_L,w_U$ are restricted to primes (the actual RSA case). If differential is always $0$ for primes, your rule predicts no asymmetry, so no impact.
3. Prove $E(n) = (d/2-1)\ln n$ implies a bound on $T$ that is tighter than the trivial bound $|T| \le \lceil |N - w_L w_U|/w_L \rceil$.

Right now steps 1-3 are missing.

If you want, I can scaffold a large-scale test harness for your repo that enumerates many $N$ around $2^{40}$, computes transport error vs divisor differential, and plots the null distribution. That would turn the anecdote into testable data and let you see if there is any residual correlation beyond the trivial $N$ selection effect.
