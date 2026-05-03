# Collatz Short-Block Reset Algebra

## Status

This document proves the exact algebra for the 3-step odd Collatz
first-descent family whose terminal source is one below a prime-gap
divisor-count minimizer.

The proved result is branch algebra: exact 3-step blocks split into two
inverse branches with reset scales differing by a factor of $2$.

The measured result is branch occupancy: in the scanned $k=4$ and $k=8$
surface, the doubled branch occurs vastly more often as a below-minimizer
terminal hit.

Both branches occur in the scanned surface. A concrete branch-1 example is
given below, followed by the measured branch-occupancy certificate.

## Definitions

The accelerated odd Collatz map is:

$$C(n)=\frac{3n+1}{2^{v_2(3n+1)}}$$

where $n$ is odd and $v_2(m)$ is the exponent of $2$ dividing $m$.

For an odd seed $s$, a first-descent block is the finite odd orbit segment
ending at the first odd target $t < s$. Its reset strength is:

$$R(s)=\frac{s}{t}$$

Let:

$$s \to a \to n \to t$$

be an exact 3-step first-descent block, so $a \geq s$, $n \geq s$, and $t < s$.

Let $p < q$ be consecutive primes. A leftmost divisor-count minimizer in the
prime gap is the first integer $w$ in $p < w < q$ whose divisor count is
minimal over that open interval.

The below-minimizer terminal case is:

$$n=w-1$$

where $n$ is the terminal source of the 3-step block.

Let:

$$k=v_2(3n+1)=v_2(3w-2)$$

## Theorem 1: Exact 3-Step Blocks Have Two Branches

For every exact 3-step odd first-descent block $s \to a \to n \to t$ with odd
seed $s \geq 3$, the first exponent is $1$, and the second exponent is either
$1$ or $2$.

### Proof

Write the first exponent as $e_1$. Since the first source is odd,
$e_1 \geq 1$, and:

$$a=\frac{3s+1}{2^{e_1}}$$

The block has exact length $3$, so the first target has not yet descended:

$$a \geq s$$

Therefore:

$$3s+1 \geq 2^{e_1}s$$

If $e_1 \geq 2$, then $2^{e_1} \geq 4$, so:

$$3s+1 \geq 4s$$

which implies $1 \geq s$, impossible for odd $s \geq 3$. Hence:

$$e_1=1$$

Now:

$$a=\frac{3s+1}{2}$$

Write the second exponent as $e_2$. Then:

$$n=\frac{3a+1}{2^{e_2}}=\frac{9s+5}{2^{e_2+1}}$$

The second target has also not yet descended:

$$n \geq s$$

Therefore:

$$9s+5 \geq 2^{e_2+1}s$$

If $e_2 \geq 3$, then $2^{e_2+1} \geq 16$, so:

$$9s+5 \geq 16s$$

which implies $5 \geq 7s$, impossible for $s \geq 1$. Since $e_2 \geq 1$, the only
possibilities are:

$$e_2 \in \{1,2\}$$

This proves the claim.

## Theorem 2: Below-Minimizer Terminal Branch Formulas

Let $s \to a \to n \to t$ be an exact 3-step first-descent block with terminal
source $n=w-1$. Let $k=v_2(3w-2)$.

If the middle exponent is $1$, then:

$$w \equiv 0 \pmod 9$$

and:

$$s=\frac{4w-9}{9}$$

If the middle exponent is $2$, then:

$$w \equiv 5 \pmod 9$$

and:

$$s=\frac{8w-13}{9}$$

### Proof

By Theorem 1, the first exponent is $1$. Let the middle exponent be $m$, where
$m$ is either $1$ or $2$.

Invert the middle step:

$$a=\frac{2^m n-1}{3}$$

Invert the first step:

$$s=\frac{2a-1}{3}$$

Substitute the expression for $a$:

$$s=\frac{2^{m+1}n-5}{9}$$

Since $n=w-1$, this becomes:

$$s=\frac{2^{m+1}(w-1)-5}{9}$$

For $m=1$:

$$s=\frac{4w-9}{9}$$

The numerator must be divisible by $9$, so $4w \equiv 0 \pmod 9$. Since $4$ is
invertible modulo $9$, this is equivalent to:

$$w \equiv 0 \pmod 9$$

For $m=2$:

$$s=\frac{8w-13}{9}$$

The numerator must be divisible by $9$, so $8w \equiv 4 \pmod 9$. Since
$8^{-1} \equiv 8 \pmod 9$, this is equivalent to:

$$w \equiv 5 \pmod 9$$

This proves the two branch formulas.

## Theorem 3: Exact Reset Formulas

Under the hypotheses of Theorem 2, the branch-1 reset strength is:

$$R(s)=\frac{2^k(4w-9)}{9(3w-2)}$$

and the branch-2 reset strength is:

$$R(s)=\frac{2^k(8w-13)}{9(3w-2)}$$

For fixed $k$, the large-$w$ reset asymptotes are:

$$\frac{2^{k+2}}{27}$$

for branch 1, and:

$$\frac{2^{k+3}}{27}$$

for branch 2. Thus branch 2 has exactly twice the asymptotic reset scale of
branch 1 at fixed $k$.

### Proof

The terminal target is:

$$t=C(w-1)=\frac{3w-2}{2^k}$$

By definition, $R(s)=s/t$.

For branch 1, substitute $s=(4w-9)/9$:

$$R(s)=\frac{(4w-9)/9}{(3w-2)/2^k}$$

so:

$$R(s)=\frac{2^k(4w-9)}{9(3w-2)}$$

Taking $w$ to infinity gives:

$$\lim_{w\to\infty}R(s)=\frac{2^k\cdot4}{9\cdot3}=\frac{2^{k+2}}{27}$$

For branch 2, substitute $s=(8w-13)/9$:

$$R(s)=\frac{(8w-13)/9}{(3w-2)/2^k}$$

so:

$$R(s)=\frac{2^k(8w-13)}{9(3w-2)}$$

Taking $w$ to infinity gives:

$$\lim_{w\to\infty}R(s)=\frac{2^k\cdot8}{9\cdot3}=\frac{2^{k+3}}{27}$$

The branch-2 asymptote divided by the branch-1 asymptote is $2$.

## Theorem 4: Final-Exponent Residue Normal Form

In the below-minimizer terminal case $n=w-1$, the final exponent condition
$v_2(3w-2)=k$ is equivalent to:

$$3w \equiv 2 \pmod {2^k}$$

and:

$$3w \not\equiv 2 \pmod {2^{k+1}}$$

### Proof

The final Collatz numerator is:

$$3(w-1)+1=3w-2$$

The statement $v_2(3w-2)=k$ means exactly that $2^k$ divides $3w-2$, and
$2^{k+1}$ does not divide $3w-2$. This is precisely:

$$3w \equiv 2 \pmod {2^k}$$

and:

$$3w \not\equiv 2 \pmod {2^{k+1}}$$

This proves the residue normal form.

## Concrete Branch-1 Example

The first branch-1 below-minimizer terminal hit found by the targeted inverse
scan is:

| Quantity | Value |
|---|---:|
| seed `s` | `6000471` |
| first target `a` | `9000707` |
| terminal source `n` | `13501061` |
| terminal target `t` | `2531449` |
| witness `w` | `13501062` |
| final exponent `k` | `4` |
| middle exponent | `1` |
| reset strength | `2.3703700923858233` |

The exact Collatz transitions are:

| Source | Target | Exponent |
|---:|---:|---:|
| `6000471` | `9000707` | `1` |
| `9000707` | `13501061` | `1` |
| `13501061` | `2531449` | `4` |

The prime gap is:

$$13501057 < w < 13501063$$

The divisor counts inside the gap are:

| Integer | Divisor count |
|---:|---:|
| `13501058` | `32` |
| `13501059` | `24` |
| `13501060` | `24` |
| `13501061` | `16` |
| `13501062` | `12` |

Thus $w=13501062$ is the leftmost divisor-count minimizer in its prime gap,
and the terminal source is $w-1$. Also:

$$13501062 \equiv 0 \pmod 9$$

so this is a branch-1 below-minimizer terminal hit.

## Computed Branch Occupancy Certificate

The targeted inverse scan through odd seeds $s \leq 100000000$ produced:

| Family | Candidate count | Hit count | Hit rate |
|---|---:|---:|---:|
| `k=4`, branch `1` | `781250` | `36` | `0.00004608` |
| `k=4`, branch `2` | `390625` | `11510` | `0.0294656` |
| `k=8`, branch `1` | `48828` | `5` | `0.00010240026214467109` |
| `k=8`, branch `2` | `24415` | `708` | `0.028998566455048128` |

The corresponding median reset strengths are:

| Final exponent | Branch | Hits | First seed | Median reset |
|---:|---:|---:|---:|---:|
| `4` | `1` | `36` | `6000471` | `2.370370339879278` |
| `4` | `2` | `11510` | `9675` | `4.740740657317454` |
| `8` | `1` | `5` | `25957527` | `37.925925522691756` |
| `8` | `2` | `708` | `4171` | `75.85185042289021` |

This table is a computed certificate, not a proof of the branch-occupancy law.
It supports the next proof target:

```text
Explain why leftmost divisor-count minimizers in prime gaps become
below-minimizer terminal witnesses far more often on branch 2 than branch 1
among inverse-eligible exact 3-step witnesses.
```

## Artifact Links

The deterministic scripts and outputs are:

```text
scripts/collatz_pgs_short_block_reset_candidate_probe.py
scripts/collatz_pgs_short_block_branch_counterexample_probe.py
output/collatz_pgs_short_block_reset_candidate_probe/summary.json
output/collatz_pgs_short_block_branch_probe/summary.json
```
