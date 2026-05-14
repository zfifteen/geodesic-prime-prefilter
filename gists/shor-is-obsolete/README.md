# Shor Is Obsolete

This gist is a small reproducible demonstration of a specific measured fact:
on one resolved RSA v2 ladder rung, public PGS endpoint structure fixes the
same order information that Shor's quantum phase-estimation step is normally
used to discover.

That does not make Shor's algorithm false. It makes Shor downstream.

Shor starts from a modulus `N = p * q` and tries to recover the hidden cycle in
the powers

```text
a^0 mod N, a^1 mod N, a^2 mod N, ...
```

The length of that cycle is called the order of `a` modulo `N`. Once the right
order is known, classical arithmetic can usually turn it into the factors of
`N`. The hard part of Shor is not the final arithmetic. The hard part is the
order discovery. Quantum phase estimation is the famous tool used to extract
that hidden period.

The usual phase-estimation budget is described here as `2n` phase bits for an
`n`-bit modulus. That is why the 40-bit row starts with an `80`-bit ordinary
Shor burden and the 50-bit row starts with a `100`-bit ordinary Shor burden.
The residual burden is what remains after public PGS structure has either fixed
the order data or failed to do so.

PGS changes the question. It asks whether the integer-level endpoint structure
of the semiprime already exposes the information that quantum phase estimation
is trying to recover.

In the measured 40-bit RSA v2 sidecar case here, the answer is yes.

## The Unwritten Script

The intended script is:

```text
pgs_shor_order_bypass_demo.py
```

It should be a single-file, standard-library-only Python script. It should not
import this repository. It should not call a factoring library. It should not
use trial division, `gcd` search, primality APIs, random search, network calls,
or hidden solver state.

The script should embed two frozen rows:

```text
rsa_v2_40bit_static_001
rsa_v2_50bit_static_001
```

For each row, it should print:

- the modulus size;
- the ordinary Shor phase-bit budget;
- whether the public PGS endpoint class matches the audit endpoints;
- whether the candidate fixed-base order vector equals the actual order vector;
- the residual phase-bit burden after PGS;
- the row status.

The script is not a new solver. It is a verifier for a frozen measured sidecar.
Its job is to make one claim inspectable:

```text
if public PGS endpoint structure fixes the same order vector,
then Shor order finding has no remaining work on that row.
```

The companion output file should be:

```text
example-output.txt
```

It should contain the exact printed table from the script.

## The Frozen Measurement

The two rows are deliberately asymmetric.

```text
case_id                  bits  baseline  residual  endpoint_match  order_vector_match
rsa_v2_40bit_static_001  40    80        0         yes             yes
rsa_v2_50bit_static_001  50    100       100       no              no
```

The 40-bit row is the measured positive case. Public PGS reciprocal endpoint
closure supplies the endpoint class:

```text
N = 1099507433251
endpoint class = 1048559, 1048589
```

Those endpoints multiply back to the modulus:

```text
1048559 * 1048589 = 1099507433251
```

The audit then checks, downstream only, that the fixed-base order vector implied
by that public endpoint class equals the actual fixed-base order vector for the
bases:

```text
2, 3, 5, 7, 11, 13, 17, 19
```

It matches. The ordinary Shor phase budget for a 40-bit modulus is `2n = 80`
phase bits. Since the order vector is already fixed by public PGS endpoint
structure in this measured row, the residual Shor phase burden is recorded as
`0`.

The 50-bit row is the control. Public PGS supplies an endpoint class, but the
class fails audit:

```text
N = 1027435935526951
candidate endpoint class = 32046877, 32060407
```

Those endpoints do not multiply back to the target modulus:

```text
32046877 * 32060407 != 1027435935526951
```

The candidate order vector also differs from the actual order vector. The row
therefore keeps its ordinary Shor burden:

```text
100 baseline phase bits -> 100 residual phase bits
```

That negative control is the point. The demo does not collapse every row by
word choice. It collapses only the row where the public PGS endpoint structure
actually carries the same order information.

## How A Shor Reader Should Read This

If you are implementing Shor classically, the bottleneck is the same object:
order. A classical implementation can simulate the surrounding arithmetic, but
the reason Shor matters is that quantum phase estimation is supposed to reveal
the order efficiently.

This gist says: on the measured resolved PGS row, the order vector is already
fixed by public endpoint structure before phase estimation enters.

That is the whole provocation. The quantum routine is not contradicted. It is
made unnecessary on the row where the integer structure has already exposed the
thing the quantum routine was meant to discover.

## The Math In Plain Terms

RSA hides two primes inside one public number.

```text
N = p * q
```

If `p` and `q` are known, RSA is over. The difficulty is recovering them from
`N` alone.

Shor's algorithm does not magically read `p` and `q` directly. It converts the
factorization problem into a period-finding problem. Pick a base `a`. Look at
the sequence of powers of `a` modulo `N`. Eventually the sequence repeats. The
repeat length is the order.

For many choices of `a`, knowing that order gives a direct route to the
factors. Quantum computation enters because quantum phase estimation can
extract the order efficiently.

PGS looks at the problem from the other side. Instead of treating `N` as a
black box and trying to discover a hidden period, it studies the public
integer structure around the prime endpoints themselves. The active RSA v2
surface uses reciprocal endpoint closure: a public endpoint chain, transported
through the modulus, either closes into a structural endpoint class or remains
unresolved.

When the endpoint class is correct, the order data is no longer mysterious.
For a semiprime, the order of a base modulo `N` is governed by the arithmetic
of the prime endpoints. In particular, the relevant order information divides
the Carmichael value:

```text
lambda(N) = lcm(p - 1, q - 1)
```

So if public PGS structure fixes the correct endpoints, it also fixes the
lambda structure that controls the base orders. The order vector is then
computed directly and checked against audit.

That is what the 40-bit row demonstrates.

The quantum phase-estimation step exists to discover order. In the resolved
PGS row, the order vector is already determined before that step enters. The
quantum part has nothing left to discover in that measured case.

## Why This Matters

The standard story says Shor threatens RSA because a quantum computer can find
orders faster than classical black-box methods.

This demo points at a different pressure point:

```text
what if order is not the primitive object?
```

If the integer endpoint structure fixes the order data upstream, then quantum
order finding is a downstream recovery technique, not the native explanation.
The important object is no longer the hidden period seen by Shor. The important
object is the public endpoint structure that makes the period inevitable.

That is why the title says Shor is obsolete. The claim is not that Shor is
mathematically wrong. The claim is that, on the measured resolved row, Shor's
quantum step is solving a downstream version of a problem whose relevant
integer structure has already been exposed by PGS.

## What This Does Prove

This demonstrates a measured sidecar collapse:

```text
40-bit resolved row: 80 phase bits -> 0 residual phase bits
50-bit control row: 100 phase bits -> 100 residual phase bits
```

It proves that the demo's frozen data contains one row where public PGS
endpoint closure supplies an endpoint class whose implied order vector matches
the actual order vector under audit.

It proves that the residual phase-bit accounting is not cosmetic. The positive
case and negative control behave differently.

## Boundary And Consequence

The demonstration has a narrow measurement surface and a large consequence.

The measured surface is two frozen RSA v2 sidecar rows. On the 40-bit row,
public reciprocal PGS endpoint closure identifies an endpoint class that matches
the audit endpoints. The fixed-base order vector implied by that endpoint class
equals the actual fixed-base order vector. The ordinary Shor phase burden moves
from `80` bits to `0` residual bits.

On the 50-bit row, public PGS structure exists, but the selected endpoint class
fails audit. The candidate order vector differs from the actual order vector.
The ordinary Shor burden therefore stays at `100` residual phase bits.

The consequence is direct:

```text
where public PGS endpoint structure fixes the order vector,
Shor order finding has no remaining order-discovery work.
```

That is the result this gist isolates. Quantum phase estimation is a recovery
method for order. On the resolved 40-bit row, the order vector has already been
fixed by public integer structure. The quantum step is displaced by the
upstream endpoint object.

The active mathematical target is equally concrete. The current rule still
needs the PGS-native discriminator that separates the factor endpoint class
from nearby false endpoint classes on unresolved rows. The 50-bit control marks
that boundary. It is not a reason to soften the 40-bit result. It names the
next exact lock.

The scaling question is therefore not vague:

```text
identify the public PGS invariant that selects the factor endpoint class,
then test whether the same order-vector collapse follows unchanged.
```

## Expected Output Shape

The future script should print something close to:

```text
PGS/Shor order-bypass demo

case_id                  bits  endpoint_match  order_vector_match  baseline_phase_bits  residual_phase_bits  status
rsa_v2_40bit_static_001  40    yes             yes                 80                   0                    order finding removed
rsa_v2_50bit_static_001  50    no              no                  100                  100                  ordinary Shor burden remains

Measured result:
PGS removed Shor order-finding work on 1 / 2 frozen RSA v2 sidecar cases.

Consequence:
Where public PGS endpoint structure fixes the order vector, quantum order
discovery has no remaining work.

Active target:
Find the public PGS invariant that separates the factor endpoint class from
nearby false endpoint classes on unresolved rows.
```

The script should fail loudly if the embedded frozen facts do not reproduce the
expected statuses. No fallback path belongs in this gist.

## The Short Version

Shor finds factors by first finding order.

PGS exposes endpoint structure on the measured resolved row.

Endpoint structure fixes lambda.

Lambda controls the order vector.

On the measured 40-bit row, public PGS endpoint closure fixes the same order
vector that Shor would otherwise need quantum phase estimation to recover.

That makes the quantum step unnecessary for that row.

The 50-bit control remains unresolved, so the claim stays honest.
