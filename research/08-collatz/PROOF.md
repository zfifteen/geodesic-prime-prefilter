# Collatz Short-Block Reset Algebra

## Status

This document proves the exact algebra for 3-step odd Collatz first-descent
blocks whose terminal source is written as $w-1$.

The proved result is branch algebra: exact 3-step blocks split into two
inverse branches with exact reset formulas whose fixed-$k$ large-$w$ scales
differ by an asymptotic factor of $2$.

The algebraic theorems are pure Collatz inverse algebra. The prime-gap
divisor-count condition enters only after specializing $w$ to a leftmost
divisor-count minimizer inside a prime gap.

The measured result is branch occupancy: in the scanned $k=4$ and $k=8$
prime-gap surface, the doubled branch occurs vastly more often as a
below-minimizer terminal hit. The terminal-geometry certificate below explains
the measured imbalance: branch 1's leftmost-minimizer successes are dominated
by automatic twin-gap terminal-prime wins, while branch 2 keeps a large
composite-terminal surface.

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

Write the terminal source as:

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

## Theorem 2: Necessary Terminal Branch Formulas

Let $s \to a \to n \to t$ be an exact 3-step first-descent block with terminal
source $n=w-1$. Let $k=v_2(3w-2)$.

The following formulas are necessary consequences of an existing exact 3-step
block. They do not by themselves assert that every integer $w$ in the listed
modulo-$9$ class produces such a block.

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

This proves the two necessary branch formulas.

## Corollary 3: Necessary Modulo-18 Branch Classes

Under the hypotheses of Theorem 2, $n=w-1$ is odd, so $w$ is even. Therefore
the modulo-$9$ branch classes sharpen to modulo-$18$ branch classes.

If the middle exponent is $1$, then:

$$w \equiv 0 \pmod {18}$$

If the middle exponent is $2$, then:

$$w \equiv 14 \pmod {18}$$

### Proof

The even residues modulo $18$ are $0,2,4,6,8,10,12,14,16$. Among these, the
only residue congruent to $0$ modulo $9$ is $0$, and the only residue congruent
to $5$ modulo $9$ is $14$.

## Lemma 4: Modulo-18 Forward Consistency

The two branch formulas become forward-consistent after adding parity. In
branch 1, let:

$$w \equiv 0 \pmod {18}$$

with $w>0$, equivalently $w=18r$ for an integer $r\geq 1$,

and define:

$$s=\frac{4w-9}{9},\quad a=\frac{2w-3}{3},\quad n=w-1$$

Then $s$, $a$, and $n$ are odd integers, $v_2(3s+1)=1$, and
$C(s)=a$.

Also, $v_2(3a+1)=1$, and $C(a)=n$.

In branch 2, let:

$$w \equiv 14 \pmod {18}$$

with $w>0$, equivalently $w=18r+14$ for an integer $r\geq 0$,

and define:

$$s=\frac{8w-13}{9},\quad a=\frac{4w-5}{3},\quad n=w-1$$

Then $s$, $a$, and $n$ are odd integers, $v_2(3s+1)=1$, and
$C(s)=a$.

Also, $v_2(3a+1)=2$, and $C(a)=n$.

In either branch, if $k=v_2(3w-2)$ and:

$$\frac{3w-2}{2^k}<s$$

then the constructed segment is an exact 3-step first-descent block with
terminal target:

$$t=\frac{3w-2}{2^k}$$

### Proof

For branch 1, write $w=18r$. Then:

$$s=8r-1,\quad a=12r-1,\quad n=18r-1$$

so $s$, $a$, and $n$ are odd. Also:

$$a-s=4r,\quad n-s=10r$$

so the first two targets have not descended for positive $w$. Next:

$$3s+1=24r-2=2(12r-1)=2a$$

so $v_2(3s+1)=1$ and $C(s)=a$. Next:

$$3a+1=36r-2=2(18r-1)=2n$$

so $v_2(3a+1)=1$ and $C(a)=n$.

For branch 2, write $w=18r+14$. Then:

$$s=16r+11,\quad a=24r+17,\quad n=18r+13$$

so $s$, $a$, and $n$ are odd. Also:

$$a-s=8r+6,\quad n-s=2r+2$$

so the first two targets have not descended. Next:

$$3s+1=48r+34=2(24r+17)=2a$$

so $v_2(3s+1)=1$ and $C(s)=a$. Next:

$$3a+1=72r+52=4(18r+13)=4n$$

so $v_2(3a+1)=2$ and $C(a)=n$.

Finally, the terminal step is:

$$C(n)=C(w-1)=\frac{3w-2}{2^{v_2(3w-2)}}$$

Thus, when this value is below $s$, the constructed segment is exactly a
3-step first-descent block.

## Theorem 5: Exact Reset Formulas

For any terminal source $n=w-1$ satisfying one of the two terminal branch
formulas, with $k=v_2(3w-2)$, the branch-1 reset strength is:

$$R(s)=\frac{2^k(4w-9)}{9(3w-2)}$$

and the branch-2 reset strength is:

$$R(s)=\frac{2^k(8w-13)}{9(3w-2)}$$

For fixed $k$, the large-$w$ reset asymptotes are:

$$\frac{2^{k+2}}{27}$$

for branch 1, and:

$$\frac{2^{k+3}}{27}$$

for branch 2. Thus branch 2 has exactly twice the asymptotic reset scale of
branch 1 at fixed $k$.

At finite $w$, the branch-2 reset value is not asserted to be exactly twice the
branch-1 value; the exact finite values are the two rational functions above.

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

## Lemma 6: Final-Exponent Residue Normal Form

In the terminal-source notation $n=w-1$, the final exponent condition
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

## Prime-Gap Specialization

Let $p < q$ be consecutive primes. A leftmost divisor-count minimizer in the
prime gap is the first integer $w$ in $p < w < q$ whose divisor count is
minimal over that open interval.

The below-minimizer terminal case is the specialization where the terminal
source of the 3-step block is:

$$n=w-1$$

with this prime-gap minimizer $w$.

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

$$13501062 \equiv 0 \pmod {18}$$

so this is a branch-1 below-minimizer terminal hit.

## Computed Branch Occupancy Certificate

This section is a bounded computational certificate for the prime-gap
specialization. It is self-contained but not a universal theorem.

For each inverse-eligible branch candidate, write the terminal source as
$n=w-1$. The integer $w$ lies in an open prime gap $p < w < q$. A leftmost
divisor-count minimizer is the first integer in that open interval whose
divisor count is minimal among all integers in the interval.

The candidate becomes a below-minimizer terminal hit exactly when:

- $w$ is the leftmost divisor-count minimizer in its prime gap;
- $w-1$ is composite;
- $w-1$ is the terminal Collatz source of the 3-step block.

### Automatic Twin-Gap Exclusion

If the gap width is $2$, then the open interval contains only one integer.
That integer is automatically the leftmost divisor-count minimizer. In that
case $w-1$ is the lower prime endpoint, so it is not a composite terminal
source. This is the automatic twin-gap terminal-prime channel.

This proves the exclusion for twin gaps: a twin-gap minimizer success is
automatic, but it cannot be a below-minimizer composite terminal hit.

The targeted inverse scan through odd seeds $s \leq 100000000$, restricted to
final exponents $k=4$ and $k=8$, produced:

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

The leftmost-minimizer successes split by terminal geometry as follows:

| Branch | Automatic twin terminal-prime | Terminal-prime non-twin | Composite below-minimizer | Total leftmost |
|---:|---:|---:|---:|---:|
| `1` | `19887` | `168` | `41` | `20096` |
| `2` | `0` | `18609` | `12218` | `30827` |

Thus branch 1 has `20096` leftmost-minimizer successes, but `19887` of them
are automatic twin-gap terminal-prime wins. These cannot become
below-minimizer terminal hits because $w-1$ is a prime endpoint. Branch 1 has
only `41` composite-terminal successes in the measured surface.

Branch 2 has no automatic twin-gap channel in this measured leftmost surface.
It has `12218` composite below-minimizer terminal hits, which is
`39.634087001654394%` of its leftmost-minimizer successes.

The `41` branch-1 composite-terminal exceptions in this certificate all have
divisor count `12` at $w$, and their gap widths are:

| Gap width | Branch-1 composite-terminal exceptions |
|---:|---:|
| `6` | `37` |
| `8` | `3` |
| `10` | `1` |

Every branch-1 composite-terminal exception has the normal form:

$$w=18u$$

where $u$ is prime. Since $u$ is prime and $u$ is not $2$ or $3$, this gives:

$$w=2\cdot 3^2\cdot u$$

and therefore the divisor count of $w$ is:

$$d(w)=d(2)d(3^2)d(u)=2\cdot 3\cdot 2=12$$

The offsets inside the containing prime gap are also concentrated. In `38` of
the `41` exceptions, the terminal source has offset `4` from the lower prime
endpoint and the witness $w$ has offset `5`. In the remaining `3` exceptions,
the terminal source has offset `6` and the witness $w$ has offset `7`.

The measured explanation is:

```text
Branch 1 concentration is explained by automatic twin-gap terminal-prime wins
plus a fully enumerated small composite-terminal exception family; branch 2's
composite-terminal surface persists across nontrivial gaps.
```

This closes the explanation for the measured $s \leq 100000000$, $k=4,8$
surface. The remaining theorem target is symbolic: prove the branch-1
exception-family constraints and prove the branch-2 nontrivial-gap occupancy
mechanism.

The next focused theorem target is narrower than the full occupancy mechanism:

```text
Prove symbolically why the branch-1 composite exception family is restricted
to w=18u with u prime, divisor count 12, and gap width 6, 8, or 10; only after
that return to the branch-2 occupancy mechanism.
```
