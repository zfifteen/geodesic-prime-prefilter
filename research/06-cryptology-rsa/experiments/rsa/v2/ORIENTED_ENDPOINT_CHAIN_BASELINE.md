# Oriented Endpoint-Chain Baseline

## Baseline Label

```text
OECC_LINEAR_V1
```

This label names the current implementation in `run_experiment.py`.

The baseline is the first public PGS runner that resolves the square-root
orientation-crossing case by walking the lower public endpoint chain and
applying reciprocal deadline-signature closure.

It is a structural endpoint-class resolver. It is not an exact factor-pair
claim unless the downstream audit separately confirms exact factor equality.

## Current Baseline Flow

```text
input: public modulus N

s = floor(sqrt(N))
lower_bound = floor(s / 2)
upper_bound = 2s

a0 = previous_public_endpoint_before(s)
L0 = pgs_certificate(a0)

if L0.reset_endpoint <= s:
    x0 = L0.reset_endpoint
    y0 = floor(N / x0)
    U0 = pgs_certificate(previous_public_endpoint_before(y0))

    if strict_reset_closure(L0, U0):
        emit resolved endpoint class from reset endpoints
        stop

    if deadline_signature_closure(L0, U0):
        emit resolved endpoint class from corrected lower endpoint and upper deadline
        stop

for each lower public endpoint a from a0 down to lower_bound:
    L = pgs_certificate(a)

    if L.reset_endpoint <= s:
        x = L.reset_endpoint
    else:
        x = L.anchor

    y = floor(N / x)

    if y < s or y > upper_bound:
        continue

    U = pgs_certificate(previous_public_endpoint_before(y))

    if U is missing:
        continue

    z = floor(N / U.reset_endpoint)
    c = previous_public_endpoint_before(z)
    Lc = pgs_certificate(c)
    d = U.reset_deadline_value

    if c < a
       and d > U.reset_endpoint
       and floor(N / c) == d
       and floor(N / d) == c
       and Lc.reset_signature == U.reset_signature:
           emit structural endpoint class (c, d)
           stop

emit unresolved
```

## Baseline Measurements

Committed rows:

```text
rsa_v2_40bit_static_001
  status = resolved_by_reciprocal_deadline_signature_correction
  endpoint class = (1048559, 1048589)
  audit status = inference_audit_pass

rsa_v2_50bit_static_001
  status = resolved_by_oriented_endpoint_chain_closure
  endpoint_chain_steps = 389
  endpoint class = (32046877, 32060407)
  audit status = inference_audit_fail
```

Ad hoc 48-bit row:

```text
N = 249882542035169
status = resolved_by_oriented_endpoint_chain_closure
endpoint_chain_steps = 296
endpoint class = (15802739, 15812609)
```

## Scaling Limits In The Baseline

The baseline is correct as a reference surface, but it does not scale as an
implementation strategy.

Current scaling blockers:

- endpoint-by-endpoint lower-chain traversal;
- repeated `previous_public_endpoint_before(...)` calls;
- repeated exact `divisor_counts_segment(...)` reconstruction;
- no production certificate cache;
- Python `int` conversion before shared interval measurement;
- first structural closure stops the run even when downstream audit says it is
  not the exact factor pair.

## Next Implementation Label

```text
OECC_RECURSIVE_V2
```

This is the next version target. It keeps the same public PGS objects and
closure predicate, but replaces linear endpoint traversal with recursive
transport-induced chamber jumps.

## Recursive V2 Pseudocode

```text
input: public modulus N

s = floor(sqrt(N))
lower_bound = floor(s / 2)
upper_bound = 2s

cache = empty certificate cache keyed by public endpoint
visited = empty set of lower-chain anchors

function certificate_at(endpoint):
    if endpoint not in cache:
        cache[endpoint] = pgs_certificate(endpoint)
    return cache[endpoint]

function oriented_transport_coordinate(L):
    if L.reset_endpoint <= s:
        return L.reset_endpoint
    return L.anchor

function close_from_lower_anchor(a):
    L = certificate_at(a)

    if L is missing:
        return unresolved_missing_lower_certificate

    x = oriented_transport_coordinate(L)
    y = floor(N / x)

    if y < s or y > upper_bound:
        return open_with_next_anchor(previous_public_endpoint_before(a))

    upper_anchor = previous_public_endpoint_before(y)
    U = certificate_at(upper_anchor)

    if U is missing:
        return open_with_next_anchor(previous_public_endpoint_before(a))

    if strict_reset_closure(L, U):
        return resolved(reset_endpoint_class(L, U))

    if deadline_signature_closure(L, U):
        return resolved(deadline_endpoint_class(L, U))

    z = floor(N / U.reset_endpoint)
    c = previous_public_endpoint_before(z)
    Lc = certificate_at(c)
    d = U.reset_deadline_value

    if c < a
       and d > U.reset_endpoint
       and floor(N / c) == d
       and floor(N / d) == c
       and Lc.reset_signature == U.reset_signature:
           return resolved(structural_endpoint_class(c, d))

    next_anchor = recursive_jump_anchor(a, L, U, c, d)
    return open_with_next_anchor(next_anchor)

function recursive_jump_anchor(a, L, U, c, d):
    candidates = [
        c,
        previous_public_endpoint_before(c),
        previous_public_endpoint_before(floor(N / d)),
        previous_public_endpoint_before(floor(N / U.reset_endpoint)),
    ]

    keep candidates that are public lower endpoints
    keep candidates with lower_bound <= candidate < a
    choose the greatest remaining candidate

    if no candidate remains:
        return previous_public_endpoint_before(a)

    return chosen candidate

a = previous_public_endpoint_before(s)

while a is not missing and a >= lower_bound:
    if a in visited:
        emit unresolved_by_recursive_cycle
        stop

    add a to visited

    result = close_from_lower_anchor(a)

    if result is resolved:
        emit result
        stop

    a = result.next_anchor

emit unresolved_by_balance_boundary
```

## Recursive V2 Acceptance Criteria

The recursive version is allowed to replace the baseline only if it satisfies
all of these:

```text
same public inputs
same closure predicate
same resolved endpoint class for the 40-bit row
same first structural endpoint class for the 48-bit row
same first structural endpoint class for the 50-bit row
fewer lower-chain certificate evaluations than OECC_LINEAR_V1 on 48-bit and 50-bit rows
no product closure
no divisibility selector
no gcd
no primality API
no audit endpoint in inference
explicit unresolved state for cycles or balance-boundary exit
```

## Falsifier

`OECC_RECURSIVE_V2` is invalid if it skips the first structural closure emitted
by `OECC_LINEAR_V1` on any row in the current test set.

The comparison target is not merely "a closure." The comparison target is the
first public structural endpoint class under the baseline ordering.
