# A1 Algorithm (endpoint-resolver-v3)

## Input (inference)

Public rows only:

- `case_id`
- `bits`
- `N`

Inference never reads private factors, audit labels, or confidence fields.

## Stages

### Stage 1: Public orientation

Compute `center = isqrt(N)`. The square root separates lower and upper sides.
It does not define a fixed additive candidate chamber.

### Stage 2: Initial lower anchor

Find the previous public endpoint before `center`. That endpoint is step zero
of one lower endpoint chain.

### Stage 3: Chamber-reset certificate

At each lower anchor, derive a PGSPG chamber-reset certificate containing:

- reset endpoint
- carrier_w / carrier_d (GWR-selected carrier fields)
- lock_carrier fields
- threat / tail offsets
- reset deadline and reset signature

### Stage 4: Oriented transport coordinate

```text
x = lower.reset_endpoint  when lower.reset_endpoint <= center
x = lower.anchor          otherwise
```

### Stage 5: Floor transport

```text
y = floor(N / x)
```

This is public reciprocal transport. It is not a divisibility test and does not
check product closure.

### Stage 6: Upper certificate

Find the previous public endpoint before `y`. Derive the upper chamber-reset
certificate.

### Stage 7: Closure order

1. **Strict reset closure** first:
   - floor transport images match reset endpoints both ways
   - reset signatures match
2. **Deadline-signature correction** second (one induced correction)
3. **Named GWR-carrier transport closure** predicates (inference, not audit):
   - `gwr_carrier_fields_present`
   - `gwr_dual_gap_carrier_floor_transport_bound` (**live residual discriminator D**)
     - `T = floor(N / lower.carrier_w)`
     - `delta = |T - upper.carrier_w|`
     - `boundD = max(20, floor(1.2 * (g_lo + g_up)))` with public gap defaults 20
     - D holds iff `delta <= boundD`
   - `gwr_carrier_floor_transport_within_gap_bound` (legacy lower-only; diagnostic only)
   - `gwr_first_tail_reciprocal_proximity` (when deadline=tail)
   - `gwr_lower_lock_dominance` (when required by chain step)
   - `gwr_matched_profile_counts` (when required by chain step)

Live residual code for dual-gap failure remains
`unresolved_by_reciprocal_carrier_misalignment`. If D holds and a later named
predicate fails, residual migrates to that predicate's code (honest subclass).

### Stage 8: Emit

- On success: public endpoint class + structural certificate package
- On failure: unresolved residual with residual code and diagnostics

## Forbidden as inference

trial division, Miller-Rabin, ECPP, isprime/nextprime, sieve generation, gcd as
selector, N % x as factor selector, product closure, hidden factors, audit
labels, factor APIs, random search, fallback search.

## Allowed transport facts

floor(N / anchor), floor(N / reset_endpoint), floor(N / deadline), previous
public endpoint before a transported coordinate, equality of public transported
coordinates and signatures, GWR-selected carrier fields from chamber-reset state.

## rule_id

```text
reciprocal_pgs_gwr_carrier_transport_v3
```
