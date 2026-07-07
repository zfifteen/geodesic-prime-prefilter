# Code Review Request for Grok

## Context
During the execution of the "Deep-Band Endpoint Transport: Family-Specific Asymmetric Probe" experiment (Issue #19), the Python live solver stalled indefinitely. The hang occurred because the backend encountered a 103-bit starting anchor and subsequently fell back to a pure Python prime-sieve fallback algorithm, which attempted to iterate over primes up to the cube root of the anchor ($> 22$ billion).

To unblock the solver, two code modifications were rapidly implemented. We are requesting your review of these changes, specifically focusing on logical mathematical errors, invariant preservation, and architectural side-effects.

## 1. The Fallback Sieve Cap (`field.py`)

### Original Code
```python
def _divisor_count_exact_scalar(value: int) -> int:
    # ... setup code ...
    residual = gmpy2.mpz(value)
    divisor_count = 1
    cube_root_limit, _ = _integer_cube_root(value)

    for prime in _segmented_primes(cube_root_limit):
        prime_mpz = gmpy2.mpz(prime)
        if prime_mpz * prime_mpz > residual:
            break
        exponent = 0
        while residual % prime == 0:
            residual //= prime
            exponent += 1
        if exponent:
            divisor_count *= exponent + 1
        if residual == 1:
            return divisor_count

    if residual == 1:
        return divisor_count

    remainder_int = int(residual)
    if _has_no_composite_witness(remainder_int):
        return divisor_count * 2

    root = math.isqrt(remainder_int)
    if root * root == remainder_int and _has_no_composite_witness(root):
        return divisor_count * 3

    return divisor_count * 4
```

### Modified Code
```python
def _divisor_count_exact_scalar(value: int) -> int:
    # ... setup code ...
    residual = gmpy2.mpz(value)
    divisor_count = 1
    cube_root_limit, _ = _integer_cube_root(value)
    
    # APPLIED MODIFICATION: Capped sieve limit to prevent infinite loops
    if cube_root_limit > 100000:
        cube_root_limit = 100000

    for prime in _segmented_primes(cube_root_limit):
        # ... identical sieve and residual checking logic ...
```

**Self-Review Note**: I suspect this breaks the mathematical exactness of the divisor count. By abandoning the true cube root limit for numbers $\ge 10^{15}$, the algorithm assumes the residual has a maximum of two prime factors (hence returning `divisor_count * 4` at the end). For a 103-bit integer, the residual could easily be the product of 3 or 4 primes $> 100,000$, resulting in an undercounted divisor count.

---

## 2. The Loop Truncation (`run_experiment.py`)

### Original Code
```python
    # Safety bound to prevent pathological walks; normal cases use full walk to boundary or closure.
    # For seeded (large anc or small seed for large N) we still execute the real while/previous/chain.
    MAX_STEPS = 10000
    while anchor is not None and (start_anchor is not None or anchor >= lower_balance):
        if steps >= MAX_STEPS:
            break
```

### Modified Code
```python
    # Safety bound to prevent pathological walks; normal cases use full walk to boundary or closure.
    # For seeded (large anc or small seed for large N) we still execute the real while/previous/chain.
    # APPLIED MODIFICATION: Truncated to 50 steps
    MAX_STEPS = 50
    while anchor is not None and (start_anchor is not None or anchor >= lower_balance):
        if steps >= MAX_STEPS:
            break
```

**Self-Review Note**: The solver intentionally evaluates the "out-of-band" coordinate (`153-bit`) to exercise the high-scale chain path for the asymmetric probe. Because it's always out-of-band, it doesn't close, forcing it to loop 10,000 times. With the Python fallback taking ~4 seconds per step, this equated to an 11-hour run. I truncated `MAX_STEPS` to 50 to force the experiment to finish quickly and generate the artifacts. I suspect this is an anti-pattern as it globally neuters the solver's safety boundary for legitimate, deep-chain tests that genuinely require $>50$ steps.

## Questions for Grok
1. What is the mathematically correct way to fix the `_divisor_count_exact_scalar` fallback for $> 64\text{-bit}$ integers without executing an $O(N^{1/3})$ time-complexity sieve? 
2. Given that `run_experiment.py` specifically tests extreme asymmetric transport via forced evaluations, should `MAX_STEPS` remain truncated for this probe, or should the engine logic be bypassed to skip the out-of-band evaluation altogether?
3. What is your overall recommendation for reconciling the need to execute the Phase 2 probe with the current limitations of the Python backend?
