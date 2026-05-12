# Prime-Gap Structure and the Cryptologic Meaning of Prime Generation

## Abstract

Prime-Gap Structure changes the mathematical object used to reason about
prime generation. Classical cryptographic generation treats primes as rare
accepted outcomes of a candidate-testing process. Prime-Gap Structure treats
the next prime after a known prime as the forced endpoint of an ordered
divisor-count field.

This distinction is fundamental. PGS does not weaken RSA, discrete logarithms,
elliptic-curve groups, or other cryptographic hardness assumptions inside their
own problem statements. PGS does different mathematics. It replaces the
candidate-primality question with an interval-law question:

```text
known prime p -> ordered divisor-count state -> successor prime q
```

In this frame, primality is not supplied by an external primality oracle. The
law identifies the endpoint. Classical audit can still confirm the result, but
audit is not the generation mechanism.

The cryptologic implication is direct: the object adversaries and defenders
must study is no longer only the isolated primality of sampled candidates. It
is the recoverability, transport, compression, certification, and acceleration
of ordered prime-gap state.

## 1. The Classical Candidate Frame

Most practical prime generation begins with a large interval and a source of
entropy. A candidate integer is sampled, obvious composite cases are removed by
small-factor tests or sieving, and the survivors are sent through probable-prime
tests such as Miller-Rabin. The process repeats until a candidate survives.

The operational model is:

```text
sample candidate -> test candidate -> reject composite -> accept prime
```

This model has trained cryptologic intuition around two ideas.

First, prime locations are treated operationally as random enough that a
generator must search for them by sampling and rejection.

Second, exact knowledge that an interval contains no earlier prime is treated
as requiring independent exclusion of the candidate integers in that interval.
In the classical accounting, exact divisor-count knowledge is factored through
the cost of factoring or primality-testing disconnected candidates.

Those ideas are natural inside the candidate frame. They are not laws of prime
generation.

## 2. The PGS Frame

PGS begins with a known prime `p` and reads the integers to its right in order.
For each integer `n`, let `tau(n)` denote the number of positive divisors of
`n`. A prime has exactly two positive divisors, so `tau(n) = 2` exactly at
prime integers greater than `1`.

The direct next-prime theorem is:

$$q=\min\{n>p:\tau(n)=2\}$$

Given a known prime `p`, compute exact divisor counts in increasing order after
`p` and stop at the first integer whose divisor count is `2`. That integer is
the next prime `q`.

This is not a probabilistic statement. It is not an estimate of a likely prime
location. It is a deterministic successor rule.

The classical question is:

```text
Is this integer prime?
```

The PGS question is:

```text
Where does the ordered interval after p close?
```

The endpoint is prime because the ordered divisor-count law reaches the prime
condition at that endpoint. No external primality oracle is needed to choose
the endpoint inside generation.

## 3. The Divisor Normalization Identity

The Divisor Normalization Identity places primes and composites on one fixed
scale:

$$Z(n)=n^{1-\tau(n)/2}$$

If `n` is prime, then `tau(n)=2`, so:

$$Z(n)=n^{1-2/2}=1$$

Every prime lands at the fixed-point value `Z = 1`. Every composite has
`tau(n) > 2`, so its exponent is negative and its `Z` value lies below `1`.

This identity converts the ordinary divisor-count sequence into a normalized
prime-centered score. It does not decorate the arithmetic. It expresses the
same ordered structure in invariant form.

Inside a prime gap, all interior integers are composite. The gap is therefore
an ordered finite field of values below the prime fixed point, ending at the
first later return to the fixed point.

## 4. The Leftmost Minimum-Divisor Rule

Let `p < q` be consecutive primes, and let:

$$I=\{p+1,\ldots,q-1\}$$

When `I` is nonempty, every integer in `I` is composite. The leftmost
minimum-divisor integer `w` is:

$$w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}$$

The logarithmic comparison function is:

$$F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n$$

The prime-gap maximizer theorem states that `w` is the unique integer in `I`
where `F(n)` is largest.

This result gives the interior of the gap a precise selected integer. The
selected integer is not the endpoint. It is the first interior composite where
the divisor-choice load reaches its minimum inside the gap.

The No-Later-Simpler-Composite condition follows from this structure. Once the
selected integer has appeared, the same gap does not later produce an interior
composite with strictly smaller divisor count before the endpoint prime closes
the interval.

## 5. Why This Is Not a Primality Oracle

A primality oracle answers an isolated yes-or-no question about one integer.
PGS does not use that form.

The PGS generator reads an ordered interval. It treats the composites between
`p` and `q` as information-bearing arithmetic state. The endpoint is identified
by closure of that state, not by asking a separate oracle whether a guessed
candidate is prime.

The distinction is:

```text
classical: n -> primality answer
PGS: p -> interval law -> q
```

This is the central cryptologic shift. In PGS, the law tells us where the next
prime is. Primality is an internal consequence of interval closure.

## 6. What the Repository Has Established

The live proof reference proves two universal statements under their stated
hypotheses:

- the direct deterministic next-prime theorem;
- the prime-gap maximizer theorem for the leftmost minimum-divisor integer.

The production PGS generator emits one minimal record per resolved input prime:

```json
{"p": 89, "q": 97}
```

The output stream contains no source labels, confidence fields, diagnostics,
counters, proof objects, or audit metadata. Those belong in sidecar records.
Generation and audit are separate acts: generation chooses `q`; audit verifies
the produced record afterward.

The current low-scale production surfaces are exact:

```text
11..1000      164 / 164 outputted, 0 unresolved, 0 audit failures
11..10000     1225 / 1225 outputted, 0 unresolved, 0 audit failures
11..100000    9588 / 9588 outputted, 0 audit failures, 100.00% PGS
11..1000000   78494 / 78494 outputted, 0 unresolved, 0 audit failures
```

The current high-scale decade-window surface is audit-clean:

```text
10^8 through 10^18
256 consecutive input primes per decade
2816 / 2816 outputted
0 unresolved
0 audit failures
```

The exact recursive walk repeats the divisor-count successor rule from prime to
prime. The verified surface records exact transition behavior on `743075 /
743075` rows from the combined `10^6 + 10^7` next-gap surface, and `664578 /
664578` exact consecutive next-prime recoveries from prime `11` through prime
`10000121` with `0` skipped gaps.

The legacy Z-band cryptographic prefilter is a separate validated engineering
artifact. On its tested cryptographic surfaces it reports about `91%`
Miller-Rabin reduction, `2.09x` end-to-end speedup across `300` deterministic
`2048`-bit RSA keypairs, and `2.82x` end-to-end speedup across `50`
deterministic `4096`-bit RSA keypairs.

These results establish both levels of the project: the mathematical successor
law and the practical cryptographic relevance of invariant-driven composite
rejection.

## 7. The Cryptologic Shift

PGS changes the object of cryptologic analysis.

The old object is the sampled candidate:

```text
candidate -> test -> accept or reject
```

The new object is the ordered gap:

```text
known prime -> divisor-count sequence -> selected interior integer -> endpoint
```

That replacement has direct implications.

### 7.1 Prime Locations Are Not the Right Primitive

Prime locations look irregular when observed as a sparse subset of the
integers. PGS studies a different object: the interval after a known prime.
Inside that object, the next prime is not a random event. It is the first return
to the divisor-count condition `tau(n)=2`.

Randomness remains useful for choosing secret starting regions. It does not
explain the local successor transition once the starting prime is fixed.

The cryptologic primitive changes from prime-location randomness to
successor-state law.

### 7.2 Independent Candidate Testing Is the Wrong Cost Unit

Classical accounting charges the interval by asking how much work is needed to
test or exclude each candidate. PGS charges the interval as one ordered object.

The relevant question becomes:

```text
How cheaply can the ordered divisor-count state be generated, transported,
compressed, or certified?
```

This is not the same question as:

```text
How many candidates survived Miller-Rabin?
```

Miller-Rabin counts remain useful engineering measurements. They do not define
the mathematical object PGS is exploiting.

### 7.3 Full Independent Factorization Is Not the Required Conceptual Path

Exact `tau(n)` is factorization-adjacent for an isolated integer. PGS does not
therefore reduce to full independent factorization of every candidate. That
conclusion imports the candidate frame back into an interval-law problem.

PGS treats the divisor-count sequence as a structured field. The endpoint is
read from the ordered field, and the selected interior integer organizes the
closure state. The work to study is field recovery, not disconnected
factorization.

This is the important inversion:

```text
classical: factor or test candidates to find the prime
PGS: read the interval law whose endpoint is the prime
```

### 7.4 Cryptographic Entropy Moves Upstream

PGS does not require randomness inside the local successor transition. Given
the starting prime and exact ordered state, the endpoint is determined.

For private key generation, entropy belongs in choosing the secret seed,
starting region, or construction policy. The successor step itself is a
deterministic arithmetic transition.

This separates two functions that the classical candidate loop blends
together:

```text
entropy selects the private region
law resolves the prime endpoint
```

That separation is an architectural consequence. It enables prime-generation
systems whose randomness and arithmetic closure are audited independently.

### 7.5 Certificates Replace Confidence Language

A probabilistic generation path naturally speaks in confidence levels,
probable primes, and failure probabilities. PGS generation speaks in structural
state, selected integers, closure, and downstream audit.

The production generator already reflects this distinction. It emits only
`p,q` records. Sidecar diagnostics carry the structural certificate material.
Audit verifies after generation.

This is a cleaner separation of roles:

```text
generation: produce q from interval law
certificate: record the structural state
audit: verify the output
```

## 8. Consequences for Current Cryptographic Practice

### RSA

RSA security is the difficulty of recovering the prime factors of a modulus
`N = pq` from `N`. PGS does not need to change that statement to matter.

PGS changes the generation-side mathematics around RSA primes. It replaces
blind candidate rejection with a deterministic prime-walk object. The relevant
research surface becomes the cost of reconstructing or transporting prime-gap
state at RSA sizes, and the engineering surface becomes auditable prime
generation with structural sidecar certificates.

The legacy prefilter already demonstrates that invariant-driven composite
rejection changes RSA key-generation economics on measured `2048`-bit and
`4096`-bit surfaces.

### Diffie-Hellman, DSA, and Schnorr Groups

These systems rely on primes with additional group-order constraints. PGS
turns the search for such primes into a nested interval-structure problem. The
prime endpoint is no longer merely an accepted sample; it is a successor state
that can be paired with additional divisor-count or subgroup-order conditions.

This reframes parameter generation as a structural construction problem rather
than a rejection loop with attached primality tests.

### Elliptic-Curve Cryptography

Elliptic-curve systems use prime fields and group-order arithmetic. The
elliptic-curve discrete logarithm remains the protocol hardness object. PGS
changes the arithmetic substrate from which prime fields and related
parameters are selected.

The consequence is a new audit surface for field-prime selection: not merely
that a prime passed a test, but where it sits as an endpoint in the ordered
successor structure.

### Hardware Security Modules and Embedded Devices

Candidate-testing loops mix entropy, rejection, timing behavior, and
probabilistic tests. PGS separates entropy selection from deterministic
endpoint recovery. That separation is valuable for constrained devices because
the arithmetic path can be made narrow, deterministic, and auditable.

The important hardware target is ordered divisor-count sequencing. Hardware
that accelerates this state changes the cost model for prime recovery more
directly than hardware that only accelerates isolated probable-prime tests.

## 9. The New Adversarial and Defensive Object

The central object for cryptologic analysis is now ordered gap state.

Adversaries study:

- recovery of divisor-count state from partial information;
- transport of state from one endpoint to the next;
- compression of gap interiors into small certificates;
- prediction of successor endpoints from leaked anchors;
- special-prime families as nested successor constraints;
- hardware acceleration of divisor-count sequencing.

Defenders study:

- secret anchor selection;
- deterministic successor generation;
- structural sidecar certificates;
- independent downstream audit;
- side-channel stable interval traversal;
- parameter-generation policies that avoid public deterministic streams.

Both sides are studying the same new object. That is what makes the shift
cryptologic rather than merely computational.

## 10. Why the Shift Is Foundational

The usual prime-generation story gives the primality test the central
epistemic role. A number becomes usable because a test says it is prime.

PGS moves that role to law:

```text
The endpoint is prime because the ordered divisor-count law closes there.
```

That is a foundational shift. It changes the unit of explanation from the
candidate to the interval, from the oracle answer to the structural endpoint,
and from randomness of prime locations to deterministic successor state.

PGS does not break the old cryptographic problems. It changes the mathematics
that surrounds prime discovery and parameter generation. The correct
cryptologic response is to study that new object on its own terms.

## 11. Conclusion

Prime-Gap Structure replaces the candidate-testing view of prime generation
with a deterministic interval law. Given a known prime, the successor prime is
the first return to `tau(n)=2` in the ordered divisor-count field. The
Divisor Normalization Identity places that return at the fixed prime locus
`Z=1`, and the leftmost minimum-divisor rule identifies the selected interior
integer that organizes the gap.

The immediate cryptologic implication is not that RSA, ECC, DSA, or
Diffie-Hellman lose their stated hardness. The implication is larger and more
basic: those systems inherit prime-generation machinery, and PGS shows that
prime generation is not confined to random candidate search.

PGS does different math.

The new object is ordered prime-gap state. Its recoverability, transport,
compression, certification, and hardware acceleration now belong in the
cryptologic research program.

## References

- [PROOF.md](../../../PROOF.md)
- [DIVISOR_NORMALIZATION_IDENTITY.md](../../../DIVISOR_NORMALIZATION_IDENTITY.md)
- [LEFTMOST_MINIMUM_DIVISOR_RULE.md](../../../LEFTMOST_MINIMUM_DIVISOR_RULE.md)
- [PRIME_GAP_GENERATOR.md](../../../PRIME_GAP_GENERATOR.md)
- [RECURSIVE_PRIME_WALK.md](../../../RECURSIVE_PRIME_WALK.md)
- [RESULTS.md](../../../RESULTS.md)
- [Minimal PGS Generator Logic](../../specs/prime-gen/minimal_pgs_generator_logic.md)
- [Legacy Prefilter](../../prefilter/LEGACY_PREFILTER.md)
