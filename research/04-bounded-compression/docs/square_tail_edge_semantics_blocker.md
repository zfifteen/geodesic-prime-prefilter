# Square-Tail Edge-Semantics Blocker

## Status

Unresolved proof blocker.

## Object

Let `r` be a selected-square root and let

```text
S = r^2
C = max(64, ceil(0.5 * log(S)^2))
M = floor(C / 2).
```

After all repeat-capable carriers `ell <= M` are applied, the remaining
positions are the M-rough defects:

```text
S - 2m has no prime factor <= M.
```

If an M-rough defect is composite, then it has least factor

```text
ell > M
```

and

```text
r^2 - 2m = ell * c.
```

Equivalently,

```text
r^2 == 2m mod ell.
```

The rough-descent audit projects such a composite defect to the smaller prime
root `ell`.

## What The Child Closure Says

The child root `ell` is closed by its own rough-defect audit when there exists
some child offset `2u` such that

```text
ell^2 - 2u
```

is prime inside the child moving window.

This is a statement about the child square `ell^2`.

## What Does Not Follow

The parent edge

```text
r^2 - 2m = ell * c
```

and the child closure

```text
ell^2 - 2u is prime
```

do not imply a contradiction under the current definitions.

They also do not imply that `r^2 - 2m` is prime, nor that a different parent
M-rough defect must be prime-valued.

The missing bridge is not computational. It is a theorem-level transport law.

## Required Transport Law

To make rough-defect descent a proof, the repo needs a deterministic law of
the following form:

```text
If r^2 - 2m = ell * c is a composite parent M-rough defect and the child root
ell is closed by a prime-valued M_ell-rough defect ell^2 - 2u, then the parent
complete-composite rough-defect state is impossible.
```

Equivalently, the needed law must connect child square closure to parent
rough-defect elimination:

```text
child prime-valued rough defect
-> parent prime-valued rough defect or parent-cover contradiction.
```

No current artifact proves this implication.

## Second-Opinion State

Grok agreed that no deterministic edge-semantics implication follows from the
current algebra alone:

```text
r^2 == 2m mod ell
```

together with

```text
ell^2 - 2u is prime
```

does not force parent primality or contradiction.

## Consequence

Closed rough-defect child audits are useful measured cascade anatomy. They do
not complete the square-tail theorem.

The live proof routes are now exactly:

1. Prove the M-rough prime-defect lemma directly:

   ```text
   Every selected-square root has at least one prime-valued M-rough defect.
   ```

2. Prove a new rough-defect transport law connecting child closure to parent
   elimination.

3. Produce a finite reduction with exact verification.

4. Produce a counterexample certificate.

The local CRT rough-cover model in

```text
research/04-bounded-compression/docs/square_tail_rough_cover_model_blocker.md
```

also rules out a pure residue-cover contradiction. The missing transport law
must use more than local congruence consistency.

That model also has a prime selected-square representative whose actual
previous prime appears after the modeled window. The missing law must therefore
use the dynamic cutoff tail itself, not only root primality or selected-square
membership.
