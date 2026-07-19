**Technical Note**

**The Gap Winner Rule (GWR): Definition and Potential Heuristic Applications**

**Version 1.0** — July 2026

### 1. Introduction

The **Gap Winner Rule (GWR)** is a structural result from the *Prime Gap Structure* (PGS) framework. It identifies a privileged composite inside every prime gap that appears unusually early and tends to have very low divisor complexity. This note defines the rule formally and explores heuristic applications that exploit its deterministic early appearance and bias toward semiprimes.

### 2. Formal Definition

Let \( p_k \) and \( p_{k+1} \) be consecutive primes with gap \( g_k = p_{k+1} - p_k \). Consider the open interval \( I = (p_k, p_{k+1}) \).

**Definition (Gap Winner).**  
The **Gap Winner** \( w(p_k) \) is defined as
\[
w(p_k) := \arg\min_{n \in I} \tau(n),
\]
where ties are broken by taking the smallest such \( n \) (i.e., the *leftmost* minimizer). Here \( \tau(n) \) denotes the number of positive divisors of \( n \).

Equivalently, under the **Divisor Normalization Identity (DNI)**,
\[
E(n) = \left( \frac{\tau(n)}{2} - 1 \right) \log n, \quad Z(n) = e^{-E(n)},
\]
the Gap Winner is the integer in the gap that *maximizes* \( Z(n) \) (or minimizes \( E(n) \)).

**Key Supporting Results (PGS):**
- **Existence and Uniqueness**: The minimizer exists and is unique in position when ties are broken leftmost.
- **Bounded Compression**:
  \[
  w(p_k) - p_k \le \max\bigl(64,\ \lceil 0.5 (\log p_{k+1})^2 \rceil\bigr)
  \]
  with high reliability (verified to \( 10^{18} \)).
- **No-Later-Simpler-Composite Theorem**: Once the minimum \( \tau \) value is attained, no integer later in the same gap has strictly smaller \( \tau \).
- **Prime-Square Proximity**: When \( \tau(w) = 3 \), then \( w = r^2 \) for prime \( r \), and the proximity bound still holds.

### 3. Empirical Properties

Analysis of the first 50,000 primes (hybrid decompwlj + PGS dataset) reveals strong regularities:

- **Dominant complexity**: In ≈91–95% of gaps, the Gap Winner satisfies \( \tau(w) = 4 \) (semiprime).
- **Early appearance**: Average distance \( w - p \) is typically between 3.3 and 4.9 across different regimes.
- **Rare square branch**: \( \tau(w) = 3 \) occurs in <1% of gaps but remains bounded in position.
- **DNI separation**: Gap Winners after level-classified primes (decompwlj) tend to have lower excess \( E(w) \) than those after weight-classified primes.

These properties make the Gap Winner a reliable, low-complexity witness that can be located with only divisor counting.

### 4. Potential Heuristic Applications

The combination of **early deterministic location** + **strong bias toward low \( \tau \)** enables several heuristics.

#### 4.1 Factoring with Partial Information (Small-Factor Scenario)

**Heuristic**: When \( N \) has at least one small prime factor \( s \), scan gaps near multiples of candidate small primes and test whether the Gap Winner (or its prime factors) is divisible by \( s \).

**Rationale**: Gap Winners frequently possess small prime factors. Starting the scan near multiples of a suspected small factor dramatically increases the probability that the Gap Winner is divisible by that factor.

**Applications**:
- Weak RSA keys with one small prime factor.
- Batch factoring where partial information is available.
- Hybrid trial division: prioritize Gap Winners over sequential integers.

**Status**: Direct blind tests (starting near \( \sqrt{N} \)) yield near-zero success. Success improves significantly when scanning is conditioned on multiples of candidate small factors.

#### 4.2 Efficient Generation of Semismooth Numbers

**Heuristic**: Collect Gap Winners (and nearby low-\( \tau \) composites) while walking prime gaps as high-quality candidates for \( B \)-smooth or semismooth numbers.

**Rationale**: Because \( \tau(w) = 4 \) dominates, Gap Winners are disproportionately semiprimes whose prime factors are often smaller than average for their size.

**Applications**:
- Generating test sets for smoothness detection algorithms.
- Preprocessing for the Elliptic Curve Method or Quadratic Sieve.
- Creating structured composite datasets for machine learning in number theory.

**Advantage**: Extremely cheap — requires only divisor counting between primes.

#### 4.3 Parameter Tuning for the Elliptic Curve Method (ECM)

**Heuristic**: Use the smallest prime factor of nearby Gap Winners to adaptively adjust smoothness bounds \( B_1 \) and \( B_2 \), or to seed curve parameters.

**Rationale**: Local Gap Winners provide a cheap sample of the typical factor size in a region. This can outperform purely random or global statistical estimates for curve selection.

**Potential benefit**: Reduced stage-1/2 runtime on certain classes of numbers.

#### 4.4 Hybrid Trial Division and Sieving

**Heuristic**: In ranges being sieved or trial-divided, immediately process the Gap Winner and other early low-\( \tau \) numbers before continuing sequential search.

**Rationale**: Low-\( \tau \) numbers are more likely to factor easily. Front-loading them improves average-case performance of trial division.

**Use cases**:
- Factoring libraries
- Cryptographic challenge solvers
- Pre-sieving stages in NFS

#### 4.5 Other Directions

| Application Area              | Proposed Use of GWR                              | Expected Benefit                     | Maturity |
|-------------------------------|--------------------------------------------------|--------------------------------------|----------|
| Pollard's \( p-1 \)           | Use factors of Gap Winners to build smoothness bounds | Better stage-1 candidates            | Low      |
| Fermat Factoring              | Scan near \( \sqrt{N} \) for algebraic structure | Marginal improvement in close-factor cases | Low   |
| Weak Prime Generator Analysis | Statistical study of Gap Winner properties       | Detection of biased prime generation | Research |
| Deterministic Testing         | Reproducible generation of structured composites | High-quality test vectors            | High     |

### 5. Conclusion and Open Questions

The Gap Winner Rule provides a deterministic, early, and low-complexity witness inside every prime gap. Its most consistent empirical property — the strong preference for semiprimes (\( \tau = 4 \)) — combined with proven bounded proximity makes it a natural building block for heuristics that benefit from cheap access to numbers with small prime factors.

**Promising directions** (in approximate order of practicality):
1. Semismooth number generation
2. Hybrid trial division
3. ECM parameter adaptation
4. Factoring scenarios with partial (especially small-factor) information

**Open Questions**:
- Can Gap Winner factors be used to meaningfully improve ECM success probability on random semiprimes?
- What is the distribution of the smallest prime factor of the Gap Winner as a function of \( p_k \)?
- Can GWR be combined with decompwlj weight/level classification to create stronger joint heuristics?

The Gap Winner Rule offers a lightweight, deterministic lens on prime gap interiors that complements both classical sieving techniques and modern factorization methods.

---

**References** (internal)
- Prime Gap Structure repository (`zfifteen/prime-gap-structure`)
- Hybrid decompwlj + PGS datasets (first 50k primes)
- Earlier experimental notes on factoring heuristics (July 2026)

This note can be extended with formal proofs, larger-scale statistics, or concrete pseudocode for any of the proposed heuristics.
