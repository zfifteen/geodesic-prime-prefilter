# Reciprocal Shadow Vote Finding

The fixed-window scale run supports the indirect-web hypothesis across all
sixteen tested semiprimes.

The observation window is held constant at radius `300`. Only the size of
`N = p q` changes. After removing every nearby composite row whose
factorization contains the audit factors `p` or `q`, the remaining composite
threads still rank the lower hidden factor `p` first in every case.

Only one factor is needed for success. In these semiprime cases `p < q`, so
the lower-endpoint surface tests one-factor recovery directly by asking
whether `p` ranks first. Recovering both factors would be stronger, but it is
not required for the factorization bridge.

For the eight larger cases, `p` and `q` are outside the fixed radius, so the
window contains no direct factor rows to remove. The same reciprocal-shadow
score still ranks `p` first.

The signal is not explained by the marginal factor multiset alone. A rotated
control that preserves the same factor rows but breaks the true
offset-to-factor pairing drops `p` to the bottom or near-bottom of the candidate
ranking in every case.

The first ladder run through 48-bit semiprimes is now treated as a boundary
measurement, not as factor-selection evidence. It kept radius `300`, placed the
lower audit factor at `97 / 100` of the target square-root scale for every rung,
and stopped a numeric candidate walk when it hit an audit factor. That does not
establish that the reciprocal-shadow field selected the factor.

The first 64-bit new-rung extension is invalid as inference evidence. It used
the hidden audit factor `p` as the lower bound of the candidate stream. That
made the result an audit-bounded hit counter rather than a blind test of
whether the local web finds a factor from public structure.

The blind restart repairs the hidden-factor bound, but it is not yet valid
factor-selection evidence. It starts the candidate stream at public
`floor(sqrt(N))`, so a long enough numeric scan reaches the lower factor `p`.
That makes the result a public candidate-walk measurement with a reciprocal
score at the audit hit, not a proof that the local web selected the factor.

## Measured Surface

```text
cases = 16
fixed_radius = 300
one_factor_success = 16 / 16
p_rank_first = 16 / 16 on the lower-endpoint surface
p_coherence = 1.0 in every true-offset case
direct_rows_removed = 0 in 8 / 16 cases
rotated_control_p_rank_near_bottom = 16 / 16
rotated_control_p_coherence_range = 0.016658..0.090989
N_range = 713..35026003
ladder_rungs = 9
ladder_bits = 16..48
ladder_inference_status = boundary, not factor selection
ladder_48_bit_scored_until_hit = 21900 / 779638
invalidated_new_rungs = 52, 56, 60, 64
invalidated_reason = hidden p bounded candidate stream
blind_restart_rungs = 20..52
blind_restart_hidden_factor_candidate_bound = none
blind_restart_inference_status = boundary, not factor selection
```

## Interpretation

Each non-direct composite thread has the form:

```text
r divides N + t
```

For a candidate lower endpoint `x`, that thread imposes a reciprocal residue
condition on the candidate's partner estimate. The true lower factor satisfies
all of those reciprocal residue shadows because the true offset and factor
thread pairing is globally consistent with `N = p q`.

The rotated control shows that the agreement is attached to the actual local
neighboring-composite pattern. When the offsets are assigned to the wrong
factor rows, the hidden factor no longer receives coherent votes.

## Boundary

This is a fixed-radius measurement and an audit-backed visualization probe. It
is not a universal theorem and not a live factor resolver.

The current score still uses the public hyperbola partner estimate
`round(N / x)`. The next stricter version should infer the partner residue from
the vote field itself before comparing against audit factors.
