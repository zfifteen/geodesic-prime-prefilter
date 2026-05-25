# Canonical Least-Divisor Word Entropy Obstruction

Date: 2026-05-24

Status: counting obstruction after the Odd Cover LCM-Growth Jacobsthal
reduction.

The Jacobsthal reduction shows that every complete odd-offset cover has large
certificate LCM. The remaining problem is the union over realized certificates.
Large LCM gives a strong density bound for one fixed certificate; it does not
by itself bound how many canonical certificates occur in `[X,2X]`.

## Canonical Word

Let `M=2m` be an even center and write the odd offsets as

$$
j=2s+1,
\qquad
0\le s<N.
$$

For a complete odd-offset cover define the canonical least-divisor word

$$
W_N(M)=(p_0,\ldots,p_{N-1}),
$$

where `p_s` is the least odd proper divisor of

$$
M-(2s+1).
$$

Since the least divisor greater than `1` is prime, every label `p_s` is an odd
prime.

The word imposes:

$$
M\equiv 2s+1\pmod {p_s},
$$

and the least-divisor exclusions

$$
M\not\equiv 2s+1\pmod r
\qquad
(r<p_s,\ r\text{ odd prime}).
$$

If `p_s=p_t=p`, compatibility requires

$$
s\equiv t\pmod p.
$$

Distinct prime labels impose compatible Chinese-remainder constraints.

## Fixed-Word Density

For a compatible word `W`, set

$$
L(W)=\operatorname{lcm}(p_0,\ldots,p_{N-1})
=\prod_{p\in P(W)}p.
$$

The congruence part of `W` places `M` in at most one residue class modulo
`L(W)`. The least-divisor exclusions only remove centers from that class.
Thus

$$
\#\{M\in[X,2X]:W_N(M)=W\}
\le
X/L(W)+1.
$$

The LCM-growth reduction gives

$$
L(W)\gg N^2/(\log X)^B
$$

for every full word. This controls a single word.

## Required Entropy Bound

Let

$$
\mathcal W_{N,X}
$$

be the set of canonical words realized by even centers `M in [X,2X]`.
The exact counting target is

$$
\sum_{W\in\mathcal W_{N,X}}
\#\{M\in[X,2X]:W_N(M)=W\}
\ll
X(\log X)^B/N^2.
$$

A sufficient small-period form is

$$
\sum_{W\in\mathcal W_{N,X}}
\frac1{L(W)}
\ll
(\log X)^B/N^2,
$$

together with a separate control on words with `L(W)>X`, where the `+1` term
in the fixed-word bound is not harmless.

This is the needed certificate entropy statement. It must say that realized
least-divisor words are sparse enough, in weighted residue measure, that the
`X/L(W)` saving survives the union.

## Residue-Window Reformulation

The word count should be converted into a residue-window count.

For an odd squarefree radical `R`, let `B_R(N)` be the number of residue
classes

$$
a\pmod R
$$

such that

$$
\gcd(s-a,R)>1
\qquad
(0\le s<N).
$$

These are the shifted Jacobsthal windows of length `N` modulo `R`. A center
whose canonical word has radical `R` contributes to one of these classes.

The entropy theorem can be stated as:

> **Canonical Shifted-Sieve Entropy Bound.**
> After imposing the least-divisor exclusions and the requirement that every
> prime in `R` is actually used by the canonical word,
> $$
> \sum_R \frac{B_R^{\mathrm{can}}(N)}{R}
> \ll
> \frac{(\log X)^B}{N^2}.
> $$

Here `B_R^{can}(N)` is the number of residue classes whose induced
least-divisor word has radical exactly `R`.

This is stronger than the pure Jacobsthal maximum-gap statement. Jacobsthal
bounds the length of the largest bad window for one modulus. The entropy bound
must control the total weighted measure of all realized bad windows across
all possible radicals.

## Candidate Mechanism

The canonical least-divisor exclusions give the only visible source of entropy
loss.

For each offset `s`, the label `p_s` means:

```text
all smaller odd prime channels miss s,
the channel p_s hits s.
```

A new prime label multiplies the congruence modulus by `p`. A repeated prime
label is possible only on offsets in one residue class modulo `p`, so the
prime `p` can cover at most

$$
\lceil N/p\rceil
$$

positions in a word of length `N`.

The desired proof would combine:

1. new-prime density cost from the `1/p` congruence factors;
2. repeated-prime capacity limits from the residue class `s mod p`;
3. least-divisor exclusions, which prevent a word from freely choosing larger
   labels where smaller active channels already hit.

The target is to turn these three facts into the weighted estimate

$$
\sum_R B_R^{\mathrm{can}}(N)/R
\ll
(\log X)^B/N^2.
$$

## Principal Obstacles

**Large LCM is not enough.**
Even if every word has `L(W) >= N^2`, there may be many realized words. A
union bound over symbolic words can destroy the fixed-certificate saving.

**The `+1` term is real.**
When `L(W)>X`, a fixed word has at most one center in `[X,2X]`. Summing this
over realized words is circular unless a separate large-L word count is
proved.

**Jacobsthal is a maximum-gap theorem.**
It says a low-radical modulus cannot support a long complete cover. It does
not count how many high-radical shifted covers occur.

**Current GWR machinery is local.**
The Interior Maximizer Theorem controls the selected minimum inside a realized
chamber. It does not count the number of shifted least-divisor covering words
among even centers in a dyadic block.

## Smallest Additional Estimate

The smallest new theorem that would continue the bridge is:

> **Canonical Least-Divisor Word Entropy Theorem.**
> For odd-offset length `N` and dyadic block `[X,2X]`, the weighted residue
> measure of realized canonical complete-cover words satisfies
> $$
> \sum_{W\in\mathcal W_{N,X}}\frac1{L(W)}
> \ll
> \frac{(\log X)^B}{N^2},
> $$
> with large-L singleton words controlled by the same shifted-sieve partition.

This theorem, combined with the Jacobsthal LCM-growth reduction, would give
the Odd Divisor-Covering Tail Theorem and therefore the even-channel
age-recurrence bound.

## Result

The next obstruction is not the size of the LCM. It is the entropy of realized
canonical least-divisor covering words. The bridge now requires a shifted-sieve
entropy theorem for the PGS divisor-channel word, not another local
GWR-selector refinement.
