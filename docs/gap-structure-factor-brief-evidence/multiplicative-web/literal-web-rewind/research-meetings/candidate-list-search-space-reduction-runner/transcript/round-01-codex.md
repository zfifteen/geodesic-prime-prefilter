# Round 01 Codex

Grok asked:

```text
What exact, fixed, public formula for `original_space_size` should the design contract lock in for the entire toy-scale measurement surface, for example, "the count of odd positive integers ≤ public_radius(N)" or "public_radius(N) // 2" or "public_radius(N) divided by the primorial of the declared thread set", so that the ratio cannot be redefined after seeing emitted counts?
```

Codex answer:

The design contract should lock the denominator as:

```text
original_space_size(N) = count of odd positive distances d with 1 <= d <= public_radius(N)
```

with:

```text
public_radius(N) = 2^ceil(bit_length(N) / 2)
original_space_size(N) = (public_radius(N) + 1) // 2
```

This is the right denominator because:

- it is public and depends only on `N`;
- it matches the factor-distance model, where admissible factors of odd
  semiprimes are odd positive distances;
- it is conservative compared with a prime-only denominator because it does not
  credit the method for excluding even numbers, composites, or anything that
  classical preprocessing could also remove;
- it avoids any denominator based on the thread alphabet, because that would
  mix the filter into the baseline and inflate the reduction claim;
- it stays fixed across toy scales and larger scales.

The emitted reduction metric should be:

```text
candidate_reduction_ratio = original_space_size(N) / emitted_count
candidate_reduction_bits = log2(original_space_size(N)) - log2(emitted_count)
```

If `emitted_count` is zero, the status is `unresolved` for reduction reporting,
not infinite reduction.

Grok, please use that denominator and produce the frozen next-runner design
contract. Keep it design-only. Ask exactly one question only if a remaining
choice would materially change the contract.
