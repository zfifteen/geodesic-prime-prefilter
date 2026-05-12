# Context-Free nth-Prime Expression

This is the self-contained expression to send to another LLM.

For $n \ge 1$:

$$p_n = 1 + \sum_{m=1}^{2^n}\left\lfloor {1 \over 1 + \left\lfloor \Pi(m)/n \right\rfloor^2} \right\rfloor,$$

where

$$\Pi(m) = \sum_{j=2}^{m} I_2(j),$$

$$I_2(j) = \left\lfloor {1 \over 1 + (d(j) - 2)^2} \right\rfloor,$$

and

$$d(j) = \sum_{a=1}^{j} [a \mid j].$$

Here $[a \mid j]$ equals $1$ when $a$ divides $j$ and equals $0$ otherwise.

## Why the Equation Works

The quantity $d(j)$ counts the positive divisors of $j$. A positive integer
$j \ge 2$ is prime exactly when $d(j) = 2$.

The indicator

$$I_2(j) = \left\lfloor {1 \over 1 + (d(j) - 2)^2} \right\rfloor$$

therefore equals $1$ for primes and $0$ for composites. The prefix sum
$\Pi(m)$ counts primes at or below $m$.

The outer summand equals $1$ exactly while $\Pi(m) < n$ and equals $0$ once
$\Pi(m) \ge n$. The sum therefore counts the integers before the nth prime,
and adding $1$ returns the nth prime itself.

## LLM-Executable Procedure

```text
function nth_prime(n):
    total = 1
    for m from 1 to 2^n:
        prime_count = 0
        for j from 2 to m:
            divisor_count = 0
            for a from 1 to j:
                if j mod a == 0:
                    divisor_count = divisor_count + 1
            if divisor_count == 2:
                prime_count = prime_count + 1
        if prime_count < n:
            total = total + 1
    return total
```

The upper bound $2^n$ is enough because the nth prime is at most $2^n$ for
$n \ge 1$ on this indexing. The expression uses only exact divisor counts and
finite sums.

## PGS Successor Form

The same content in the repository's local successor language is:

$$p_1 = 2,\quad p_2 = 3,\quad p_3 = 5,\quad p_n = F^{\,n-3}(5)\ \text{for}\ n \ge 3,$$

with

$$F(p) = B(p, S_p, w_p, d(w_p)).$$

The context-free expression above expands the same divisor-count fixed-point
condition without requiring the reader to already know the repository's symbols.
