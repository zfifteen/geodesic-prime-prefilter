# Invalidated 64-Bit New Rungs

The first 52 through 64-bit new-rung script is invalid as inference evidence.

## Failure

The script used the hidden audit factor `p` as the lower bound of the candidate
stream. That means the run did not test whether the local multiplicative web
found a factor from public structure.

## Exact Cause

```text
flags = segmented_prime_flags(p_value, sqrt_n)
candidate = p_value + offset
```

This made the candidate interval depend on a factor that the inference method
was supposed to discover.

## Status

```text
invalidated = true
reason = hidden p bounded candidate stream
usable_as_inference_evidence = false
usable_as_failure_artifact = true
```

## Replacement Contract

The replacement blind restart uses `p` and `q` only for case construction and
final audit. The candidate stream starts at public `floor(sqrt(N))`, scans
downward in fixed public segments, scores every prime candidate it sees, and
only then checks whether the scored candidate or its partner estimate matches
an audit factor.
