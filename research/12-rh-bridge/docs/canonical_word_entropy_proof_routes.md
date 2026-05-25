# Canonical Word Entropy Proof Routes

Date: 2026-05-24

Status: candidate approaches and obstacles for the Canonical Least-Divisor Word
Entropy Theorem.

The Canonical Least-Divisor Word Entropy Theorem asks for a weighted bound on
the complete-cover words that actually occur around even centers. The right
object is not the symbolic word itself. It is the residue covering system that
the word induces on the offset line.

## First-Hit Covering System

For an even center `M=2m`, write odd offsets as

$$
j=2s+1,
\qquad
0\le s<N.
$$

If `p` is an odd prime divisor channel, then

$$
p\mid M-(2s+1)
$$

holds on exactly one residue class

$$
s\equiv a_p(M)\pmod p.
$$

Thus a radical `R` with active prime set `P(R)` induces the covering system

$$
[0,N)
\subset
\bigcup_{p\mid R}
\{s:s\equiv a_p\pmod p\}.
$$

A canonical least-divisor word adds order:

```text
s is labeled by the least active prime p whose residue class contains s.
```

So the proof should count residue systems

$$
\mathcal A=\{(p,a_p):p\in P\}
$$

that cover `[0,N)`, weighted by

$$
\operatorname{wt}(\mathcal A)=\prod_{p\in P}\frac1p.
$$

This is exactly the `1/L` density of the congruence class for the active
radical.

## Weighted Covering Target

The entropy theorem follows from a covering-system estimate of the form

$$
\sum_{\mathcal A\in \mathfrak C_N^{\mathrm{can}}}
\prod_{p\in P(\mathcal A)}\frac1p
\ll
\frac{(\log X)^B}{N^2},
$$

where `C_N^can` is the family of essential canonical systems satisfying:

1. the residue classes cover every `s in [0,N)`;
2. every active prime covers at least one offset not already covered by a
   smaller active prime;
3. the induced least-hit word is compatible with an even center in `[X,2X]`.

This is the cleanest proof target. It removes arbitrary certificate
nonuniqueness and counts only the residue systems that can be canonical.

## Decomposition By Prime Size

A proof should split the active primes into two classes.

**Short channels: `p <= N`.**
One residue class modulo `p` can cover at most

$$
\lceil N/p\rceil
$$

offsets. These channels have enough reach to create overlap. Their entropy
cost is weak because there are `p` possible residue classes and each costs
`1/p`.

The needed gain must come from essentiality and least-divisor ordering: a
larger short channel contributes only where all smaller active channels miss.

**Long channels: `p > N`.**
One residue class modulo `p` hits at most one offset in `[0,N)`. These labels
are singleton channels. They carry strong LCM growth, but their large-L
singleton count is the dangerous term: many different large primes can realize
one-offset labels.

The needed gain must come from the fact that a singleton label at offset `s`
is allowed only after every smaller odd prime misses `s`.

## Candidate Sieve Mechanism

Define the uncovered set after processing active primes up to `y`:

$$
U_y(\mathcal A)=
\{s<N:s\not\equiv a_p\pmod p
\text{ for all active }p\le y\}.
$$

A canonical word processes labels in increasing prime order. When a new prime
`p` is activated, it may label only

$$
U_{p^-}(\mathcal A)\cap\{s:s\equiv a_p\pmod p\}.
$$

Thus the contribution of `p` is not a free choice of a residue class. It is a
hit on the currently uncovered set.

The desired sieve estimate is:

> **Uncovered-Set Decay Bound.**
> In the weighted residue-system measure
> $$
> \prod_{p\in P}1/p,
> $$
> the total mass of systems for which the uncovered set reaches zero by length
> `N` is
> $$
> O((\log X)^B/N^2).
> $$

This is a shifted-sieve extinction estimate: complete cover means the
uncovered set has become empty.

## Why Ordinary LCM Growth Does Not Supply This

LCM growth proves that a complete cover cannot use only a low-radical set of
channels. It gives

$$
L(W)\gg N^2/(\log X)^B.
$$

The entropy theorem asks for

$$
\sum_W 1/L(W)
\ll
(\log X)^B/N^2.
$$

Those are different statements. A family can have every member large while
still having large total weighted mass.

The missing cancellation is not analytic sign cancellation. It is structural
exclusion: least-divisor words form a nested sieve, so larger labels are
allowed only on offsets missed by all smaller labels.

## Minimal New Lemma

The smallest useful theorem is:

> **Essential Shifted-Cover Weight Lemma.**
> Let `N <= X`. For canonical first-hit residue systems on `[0,N)` using odd
> prime channels up to `sqrt(2X)`,
> $$
> \sum_{\substack{\mathcal A\ \mathrm{essential}\\[0,N)\subseteq
> \cup_{p\in P(\mathcal A)}(a_p\bmod p)}}
> \prod_{p\in P(\mathcal A)}\frac1p
> \ll
> \frac{(\log X)^B}{N^2}.
> $$

Essential means that each active prime labels at least one offset not labeled
by a smaller active prime. This is the word-level form of the least-divisor
condition.

If this lemma holds, then:

```text
essential shifted-cover weight
-> canonical word entropy
-> odd divisor-covering tail
-> even-channel age recurrence
-> zero-excess square-moment bound
-> reciprocal endpoint occupancy
-> finite-part packet balance route
```

## Principal Obstacles

**Short-channel entropy cancels density.**
For `p <= N`, the `p` possible residue classes cancel the `1/p` density cost
unless essentiality supplies extra decay.

**Long-channel singleton explosion.**
For `p > N`, each active channel can label only one offset, but there are many
possible large primes. Controlling those labels requires the full
least-divisor exclusion against smaller primes.

**The theorem resembles a prime-gap tail bound.**
A complete canonical cover is the absence of an odd zero-excess endpoint in a
length-`N` backward window. Proving its `N^-2` weighted frequency is essentially
the even-channel return-time theorem in sieve language.

**Current PGS theorems do not count first-hit systems.**
`PROOF.md` gives exact chamber-local ordering and the GWR selected minimum.
It does not prove an extinction bound for shifted divisor-channel residue
systems over a dyadic block.

## Result

The proof route is now explicit. The entropy theorem is equivalent to an
essential shifted-cover weight estimate for least-divisor first-hit systems.
This is the next arithmetic obligation. It is sharper than generic
certificate counting and strictly stronger than the Jacobsthal LCM-growth
bound.
