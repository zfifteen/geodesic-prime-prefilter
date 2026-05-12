# PGS-First Anchor Surface Findings

This note records the first refactor away from the fixed additive chamber.

The fixed chamber solver used:

```text
isqrt(N) +/- 1024 -> reciprocal endpoint/reset checks
```

That gate made the 40-bit rung look solved because its factors were already
near `isqrt(N)`. The 50-bit rung showed the design failure immediately: the
true factors were valid balanced RSA-like endpoints but were outside the fixed
radius.

## Replacement Probe

The replacement tmp probe is:

```text
public N
-> isqrt(N) as orientation only
-> lower balanced interval
-> descending PGS endpoint surface
-> reciprocal map y = floor(N / x)
-> upper endpoint/reset lock
-> reciprocal deadline-state comparison
```

The probe was integrated into the official runner:

```text
research/06-cryptology-rsa/experiments/rsa/v2/run_experiment.py
```

It reads public case rows only. It does not read audit factors.

## 80k Endpoint Probe Result Before Integration

Historical command from the temporary probe:

```bash
python3 research/06-cryptology-rsa/experiments/rsa/v2/tmp/pgs_first_anchor_surface.py \
  --max-lower-endpoints 80000 \
  --output research/06-cryptology-rsa/experiments/rsa/v2/tmp/pgs_first_anchor_surface_80k.json
```

Observed funnel:

| case | lower PGS endpoints seen | reciprocal wheel rows | reciprocal endpoint rows | two-sided locked rows | old deadline locks |
|---|---:|---:|---:|---:|---:|
| `rsa_v2_40bit_static_001` | 38636 | 10511 | 2812 | 2812 | 18 |
| `rsa_v2_50bit_static_001` | 80000 | 21358 | 4609 | 4607 | 143 |

## Critical Finding

The temporary PGS-first endpoint surface reached the 50-bit true lower factor.

The old equal-margin reciprocal deadline lock rejects the true 50-bit factor
pair:

```text
x = 30729371
y = 33434981
lower reset-deadline margin = 2
upper reset-deadline margin = 12
deadline-lock reason = reset_deadline_margin_mismatch
```

Both sides are valid local PGSPG reset locks:

```text
previous lower endpoint -> reset endpoint = 30729371
previous upper endpoint -> reset endpoint = 33434981
```

So the old rule was wrong for RSA-like balanced semiprimes. It compares raw
deadline margins as if the reciprocal map preserved unit scale. It does not.

## Consequence

The old deadline-margin equality rule was not integrated into the official solver.

The next rule must compare reset-deadline state after reciprocal transport. Raw
lower-side and upper-side margins are not expected to be equal when the two
factors are separated from `isqrt(N)`.

The useful surviving pieces are:

- public/audit separation;
- GMP integer coordinates;
- PGSPG endpoint/reset state;
- reciprocal transport by `floor(N / x)`;
- survivor-funnel reporting.

The invalid pieces are:

- fixed additive radius as the candidate gate;
- raw deadline-margin equality as the resolver;
- ranking by distance to `isqrt(N)` as a correctness signal.
