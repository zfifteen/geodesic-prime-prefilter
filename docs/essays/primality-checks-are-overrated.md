**Primality Checks are Overrated**

The usual story of prime numbers begins like a courtroom drama staged by accountants. An integer is dragged into the light. Everyone clears a throat. Trial division adjusts its spectacles. Miller-Rabin asks several pointed questions. Elliptic curves arrive with the quiet menace of consultants billing by the theorem. At the end, the accused receives the only verdict anyone came to hear: prime, or not prime.

This is a respectable procedure. It is also a strange way to understand a landscape. It is like judging a city by knocking on one door, asking the resident whether they are the mayor, and then walking away with the confidence of a census bureau.

The local question is not wrong. Does this integer have exactly two positive divisors? That is a serious question, and sometimes seriousness is unavoidable. But the cult of candidate interrogation has become theatrical. It imagines the next prime as a shy dignitary hiding somewhere in the number line, waiting for enough witnesses, certificates, and procedural safeguards before consenting to exist.

The integers after a known prime $p$ are not a queue of suspicious strangers hoping to pass inspection. They are an ordered sequence with arithmetic memory. Each integer has a divisor count. Those counts appear in order. The composites before the next prime are not failed auditions for primality. They are the interval through which the next prime is reached.

The comedy is that the rejected numbers were talking the whole time. We kept asking each integer, in isolation, whether it was special. Meanwhile the interval was quietly laying out its own evidence: composite divisor counts below, the first return to divisor count $2$ at the next prime $q$, and a finite ordered profile between the two.

Primality checks remain useful for confirmation. They are the passport control of arithmetic: necessary at borders, less inspiring as a theory of geography. They have been promoted beyond their natural station. As the primary conceptual mechanism for locating primes, primality checking is overrated.

### The Gap Is Not Empty Space

Consider the primes $23$ and $29$. The integers between them are $24,25,26,27,28$. Their divisor counts are $8,3,4,4,6$. The lowest count is $3$, and it occurs first at $25$.

That fact is not a primality test. It is a fact about the whole interval between two consecutive primes. The interval has a first integer where the divisor count reaches its minimum.

A larger example shows the same structure with ties. Between $89$ and $97$, the interior integers are $90,91,92,93,94,95,96$. Their divisor counts are $12,4,6,4,4,4,12$. The minimum value $4$ appears four times, at $91,93,94,95$. The first occurrence is $91$.

The gap does not merely separate two primes. It contains an ordered arithmetic profile. One part of the profile identifies the first integer with the smallest interior divisor count. Another part identifies the next prime: the first later integer with divisor count $2$.

The first minimum is not automatically next to the next prime. The formula $q=w+1$ is false in general. The first minimum is an ordinary integer inside the interval. It tells us where the divisor count first reaches its lowest value before the next prime appears.

### Divisor Counts

For a positive integer $n$, let $\tau(n)$ be the number of positive divisors of $n$. If

$$n=r_1^{a_1}r_2^{a_2}\cdots r_s^{a_s},$$

then

$$\tau(n)=\prod_{i=1}^{s}(a_i+1).$$

This formula records a concrete arithmetic property. A divisor of $n$ is made by choosing an exponent from each prime-power factor. The number of choices is the product of the available choices in each factor.

A prime has exactly two positive divisors. A composite has more than two. That single fact is enough to define the next prime after a known prime.

The important move is to stop treating the composites before the next prime as failed candidates. Their divisor counts are ordered data. They describe the interval through which the next prime is reached.

### The Direct Next-Prime Algorithm

Given a known prime $p$, compute exact divisor counts for the integers greater than $p$ in increasing order. Stop at the first integer $n$ with exactly two positive divisors. That integer is the next prime $q$.

In symbols:

$$q=\min\{n>p:\tau(n)=2\}.$$

The proof is direct. There is a least prime greater than $p$; call it $q$. Every integer strictly between $p$ and $q$ is composite, so no integer in that open interval has divisor count $2$. The algorithm cannot stop before $q$. The integer $q$ is prime, so $\tau(q)=2$. The algorithm must stop at $q$.

This result does not depend on probability. It does not depend on a witness base, a pseudoprime exception list, or a later confirmation step. It says that exact divisor-count traversal after a known prime deterministically returns the next prime.

The measured quantity is not a disguised yes-or-no primality verdict. The value $\tau(n)$ records the divisor structure of $n$, not merely whether $n$ passed an examination. A primality test collapses the answer to one bit: prime or composite. Exact divisor-count traversal preserves the ordered values before the next prime, and those values identify both the interior minimum and the return to $\tau=2$.

### The Interior Minimum

Once the next prime $q$ after $p$ has been identified, the open interval between them is

$$I=\{p+1,\ldots,q-1\}.$$

Assume $I$ is nonempty. Let $w$ be the first integer in $I$ whose divisor count is minimal over the interval:

$$w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}.$$

For $p=23$ and $q=29$, this gives $w=25$. For $p=89$ and $q=97$, this gives $w=91$.

This definition uses exact arithmetic. It asks for a minimum of the divisor-count sequence inside a finite set, then chooses the first place where that minimum appears.

The integer $w$ is not a prime and is not a proposed next prime. It is the first place inside the interval where the composite divisor count is smallest.

### A Logarithmic Comparison

The same interior integer is described by a score. Define

$$F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.$$

For a composite integer $n$, $\tau(n)\ge3$, so $F(n)$ is negative. If two composites $a<b$ satisfy $\tau(a)\le\tau(b)$, then

$$F(a)>F(b).$$

To see this, rewrite the score as

$$F(n)=-\left(\frac{\tau(n)}{2}-1\right)\log n.$$

For composites, the factor $\tau(n)/2-1$ is positive. If $a<b$ and $\tau(a)\le\tau(b)$, then the positive factor attached to $a$ is no larger, and $\log a<\log b$. The negative of the first product is therefore larger than the negative of the second product.

Now return to the interval $I$ between consecutive primes. Every later integer $t>w$ has $\tau(t)\ge\tau(w)$, because $w$ already has the minimum divisor count in the interval. By the comparison above, every later integer has $F(t)<F(w)$.

Every earlier integer $k<w$ has $\tau(k)>\tau(w)$, because $w$ is the first place where the minimum divisor count occurs. The smaller index of $k$ favors $k$; the larger divisor count overrides it. The exact comparison shows that the larger divisor count dominates the smaller logarithm.

For prime squares this is immediate. If $w=r^2$ for a prime $r$, then $r$ cannot lie strictly between consecutive primes $p$ and $q$, so $r\le p$. Every earlier interior integer $k$ satisfies $k>p$, hence $k>r=\sqrt{w}$. Since an earlier integer with divisor count $3$ would be an earlier prime square and would contradict the choice of $w$, every earlier $k$ has divisor count at least $4$. Therefore $F(k)\le-\log k$, while $F(w)=-(1/2)\log w$. Because $k>\sqrt{w}$, we have $F(k)<F(w)$.

For the remaining cases, the comparison reduces to the inequality

$$\left(e-2\right)\log k>\left(d-2\right)\log w,$$

where $e=\tau(k)$ and $d=\tau(w)$. Since $p<k<w<q$ and Bertrand's theorem gives $q<2p$ for $p>1$, it is enough to prove the stronger inequality

$$\left(e-2\right)\log p>\left(d-2\right)\log(2p).$$

This is equivalent to

$$p^{e-d}>2^{d-2}.$$

The inequality shows why earlier integers with larger divisor counts cannot beat the first interior minimum. The larger divisor count dominates the smaller logarithm.

The adjacent cases where $e=d+1$ and the threshold $2^{d-2}$ is large enough that the preceding inequality does not close the comparison are:

| $d=\tau(w)$ | $e=\tau(k)$ | Threshold for $p$ |
|---:|---:|---:|
| $4$ | $5$ | $4$ |
| $9$ | $10$ | $128$ |
| $13$ | $14$ | $2048$ |
| $17$ | $18$ | $32768$ |
| $19$ | $20$ | $131072$ |
| $21$ | $22$ | $524288$ |
| $25$ | $26$ | $8388608$ |
| $26$ | $27$ | $16777216$ |
| $27$ | $28$ | $33554432$ |
| $29$ | $30$ | $134217728$ |
| $33$ | $34$ | $2147483648$ |
| $35$ | $36$ | $8589934592$ |
| $39$ | $40$ | $137438953472$ |
| $41$ | $42$ | $549755813888$ |
| $43$ | $44$ | $2199023255552$ |
| $49$ | $50$ | $140737488355328$ |
| $51$ | $52$ | $562949953421312$ |
| $53$ | $54$ | $2251799813685248$ |
| $55$ | $56$ | $9007199254740992$ |
| $59$ | $60$ | $144115188075855872$ |

For each row, all larger earlier divisor counts are easier for the same $d$, because the threshold decreases as $e$ increases. For each earlier divisor count $e$, smaller values of $d$ are easier, because the threshold decreases as $d$ decreases. The table therefore isolates the hard adjacent comparisons. Direct enumeration closes the finite low ranges; the remaining large rows are closed by the least integer with the corresponding divisor count, which exceeds the threshold in each case. Once these rows are closed, every earlier integer has $F(k)<F(w)$.

Thus the first interior integer with the smallest divisor count is also the unique maximizer of $F(n)$ inside the gap.

### A Normalized Divisor-Count Scale

The same score is expressed without logarithms by defining

$$Z(n)=n^{1-\tau(n)/2}.$$

For any prime $p$, $\tau(p)=2$, so

$$Z(p)=p^0=1.$$

For a composite $n$, $\tau(n)\ge3$, so the exponent is negative and

$$Z(n)<1.$$

A prime square has $\tau=3$ and maps to $n^{-1/2}$. A semiprime has $\tau=4$ and maps to $1/n$. Higher divisor counts push the value farther below the prime baseline.

Inside a prime gap, every interior value lies below $1$. The next prime returns to $1$. The divisor-count sequence can therefore be read as a normalized sequence in which primes sit exactly at $1$ and composites sit below $1$.

The logarithmic score is simply

$$F(n)=\log Z(n).$$

The first interior integer with minimum divisor count is therefore the interior point with the largest value below the prime value $1$. The raw divisor-count description and the normalized-score description identify the same integer.

### Why This Is Not Merely Testing In Disguise

A primality test asks a local question about one integer. The divisor-count traversal asks where the ordered sequence after a known prime first returns to the value $\tau=2$.

Those are different questions.

In a candidate-testing view, composites are rejected and mostly forgotten. In the interval view, composites are evidence. Their divisor counts tell us where the interval first reaches its minimum, how the later values stay at or above that minimum, and where the next prime returns to the divisor-count value of a prime.

The same integer remains available for primality inspection after it is found. That does not mean the test was the locating mechanism. Confirmation and discovery are different roles.

### A Deterministic Procedure

The direct algorithm is stated as a procedure:

1. Start with a known prime $p$.
2. Inspect $p+1,p+2,p+3,\ldots$ in order.
3. Compute $\tau(n)$ exactly for each inspected integer.
4. Stop at the first $n$ with $\tau(n)=2$.
5. Output $(p,n)$.

For example:

```json
{"p": 89, "q": 97}
```

This algorithm does not propose a candidate and then ask whether the candidate should be accepted. It reads exact divisor counts in order. The next prime is the first return to divisor count $2$.

The procedure is deterministic. If exact divisor counts are computed correctly, it cannot skip the next prime and cannot stop early. Every earlier integer after $p$ is composite and has divisor count greater than $2$. The next prime has divisor count $2$.

The ordered divisor-count sequence determines the next prime, and the intermediate values remain part of the calculation instead of being discarded as failed candidates.

### Bounded Practical Searches

A practical implementation avoids inspecting every integer when it applies residue classes. For example, after the small primes $2,3,5$ are accounted for, any prime greater than $5$ must lie in one of the residue classes

$$1,7,11,13,17,19,23,29 \pmod{30}.$$

Integers outside those classes are already known to be composite. A search therefore focuses possible next-prime positions on those residue classes while still using exact divisor-count information inside the interval.

Such a bounded search preserves the same contract. It reduces work by using residue classes, divisor-count thresholds, or interval structure. It does not silently switch to a different prime-search method when the stated rule has not identified the next prime inside the chosen bound. If the bounded rule does not identify the next prime inside that bound, the honest result is that the bound was insufficient.

This distinction protects the mathematical content of the experiment. A deterministic structural method and a conventional prime search both return correct primes, but only the first tests whether the ordered divisor-count structure is doing the locating.

### Repetition

The direct algorithm iterates. Once it returns $q$, use $q$ as the next input prime and repeat.

The first few steps after $11$ are:

```json
{"p": 11, "q": 13}
{"p": 13, "q": 17}
{"p": 17, "q": 19}
{"p": 19, "q": 23}
{"p": 23, "q": 29}
```

No new principle appears at the next step. Each transition is the same rule applied again. The current prime anchors the interval. The divisor-count sequence to its right is read in order. The first return to $\tau=2$ gives the next prime.

This repeated walk exposes the real contrast with candidate testing. A candidate-testing procedure spends most of its work proposing and rejecting numbers. The divisor-count view reads the interval. The composites between consecutive primes are not discarded as failed attempts; they are the measured path between primes.

### Compression and Practical Filters

The interval structure supplies natural compression. The lowest possible composite divisor count is $3$, attained by prime squares. The next level is $4$, attained by semiprimes and prime cubes. In an interval with no prime square before the next prime, the first divisor-count-$4$ value is the leftmost minimum. The same ordered divisor-count sequence that fixes the next prime also identifies the earliest composite with minimum divisor count.

Residue classes, divisor-count thresholds, and early interval inspection reduce the amount of arithmetic that has to be read before the next prime is identified. These filters do not change the rule. They preserve it. The final identification of the next prime remains governed by exact arithmetic: the first return to $\tau(n)=2$.

The direct next-prime theorem is universal under its stated hypothesis. The interior-maximizer theorem is universal for every nonempty interval between consecutive primes. Bounded or filtered procedures preserve that exactness inside their declared ranges because they locate the next prime by reading ordered divisor-count evidence rather than by proposing candidates for external testing. When a chosen bound is insufficient, the result is that the bound was insufficient; the arithmetic rule has not changed.

### The Computational Claim

Exact divisor-count traversal produces the complete ordered structure of the gap; a primality test produces one bit. That structure contains the first interior minimum, the later values constrained by that minimum, the normalized values below $1$, and the first return to divisor count $2$.

This changes what computation is allowed to use. Candidate testing centers the proposed prime and treats composites as discarded failures. Divisor-count traversal centers the interval and treats composites as evidence. The procedure reads exact divisor counts, outputs the first return to $\tau=2$, and leaves primality testing for independent confirmation.

The method is correct when it has one path. It computes exact divisor counts, applies the stated rule, and either identifies the next prime or says that the chosen bound was insufficient. Silent use of a conventional search belongs to a different engineering problem; here it erases the fact being tested: the ordered divisor-count structure itself locates the next prime.

### The Core Claim

Given a known prime $p$, the next prime is determined by the first return to divisor count $2$:

$$q=\min\{n>p:\tau(n)=2\}.$$

Inside the resulting nonempty interval

$$I=\{p+1,\ldots,q-1\},$$

the first integer with minimum divisor count,

$$w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\},$$

is the unique maximizer of

$$F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.$$

The same comparison is written on the normalized scale

$$Z(n)=n^{1-\tau(n)/2},$$

where primes have value $1$ and composites have values below $1$.

The result is not that primality testing is useless. It remains the natural tool for certification. The result is that primality testing is overrated as the necessary center of prime location. The arithmetic between primes is not debris. It is the evidence. The ordered divisor-count structure after a known prime tells us where the next prime must stand.
