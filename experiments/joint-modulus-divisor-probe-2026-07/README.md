# Joint Modulus-Link and Divisor-Count Probe

## Objective

This probe is designed to test the unresolved hypothesis that the exact gap width (`q - p`) can be deterministically forced by the intersection of the divisor-count field and the modulus-link residual state.

Currently, `PROOF.md` establishes a universal bounded compression on the selected-witness offset (`w - p`), but leaves the raw gap size implication unresolved. This probe explicitly records the interior divisor counts, the GWR comparison values, and the modulus-link residuals to find if a structural certificate exists that locks the endpoint closure.

## Methodology

The required frame for this research is: `locked PGS endpoint chain -> floor transport through modulus -> reciprocal endpoint closure -> modulus-link residual -> structural certificate or unresolved state`.

1. **Divisor-Count Field & Minimizer**: For each gap `(p, q)`, we calculate the exact divisor count `tau(n)` for every interior integer. We locate the Leftmost Minimum-Divisor Rule (GWR) selected witness `w` and compute the comparison function `F(n) = (1 - tau(n)/2) * log(n)`.
2. **Modulus-Link Residual State**: We record the remainder vector $M_{v1}$ (modulo `2, 3, 5, 7, 30, 210, 2310`) for the boundaries (`p`, `q`) and the selected witness `w`. We also track the `mod_30` and `mod_210` sequences for the entire gap interior.
3. **Coprimality Structure**: We compute the least prime factor for all interior integers. Since every interior integer is composite, this tracks exactly which factorization paths are occupied.
4. **Synthesis**: By combining these metrics into a single output, we can analytically search for deterministic rules (not probabilistic sieves) that force `tau(n) = 2`, thereby defining exactly when the gap must close. We also track the dynamic cutoff bound `C_q` for direct reference.

## Usage

```bash
python3 probe_joint_state.py --start 11 --count 1000 --out results.jsonl
```

### Output Schema

The output is JSONL. Each record contains:
- `p`, `q`, `gap`: The boundaries and raw gap width
- `C_q_bound`: The dynamic cutoff bound from the Prime-Square Proximity Theorem
- `w`, `w_offset`: The GWR selected witness integer and offset
- `min_tau`, `tau_w`: The minimum divisor count in the gap
- `F_w`: The GWR log-comparison maximum value at `w`
- `boundary_residuals`: Moduli remainder vectors on `p` and `q`
- `witness_residuals`: Moduli remainder vectors on `w`
- `interior_data`: Arrays containing the `taus`, `least_prime_factors`, `F_vals`, and remainders (`mod_30`, `mod_210`) for the entire gap interior.

## Constraints
This probe adheres to the `AGENTS.md` constraint: "PGS is deterministic in kind." We are searching for structural certificates that lock the next prime, not probabilistic heuristics.
