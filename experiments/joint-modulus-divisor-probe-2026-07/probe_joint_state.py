import argparse
import json
import sys
import math
from typing import List, Tuple, Dict, Any

# M_v1 moduli set defined in PROOF.md
M_V1_MODULI = [2, 3, 5, 7, 30, 210, 2310]

def get_tau(n: int) -> int:
    """
    Compute exact divisor count (tau) for n.
    """
    if n <= 1:
        return 1
    count = 0
    limit = int(math.isqrt(n))
    for i in range(1, limit + 1):
        if n % i == 0:
            count += 2
    if limit * limit == n:
        count -= 1
    return count

def get_least_prime_factor(n: int) -> int:
    """
    Find the least prime factor of n.
    Returns n if n is prime.
    """
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    limit = int(math.isqrt(n))
    for i in range(5, limit + 1, 6):
        if n % i == 0:
            return i
        if n % (i + 2) == 0:
            return i + 2
    return n

def get_F(n: int, tau_n: int) -> float:
    """
    Compute the GWR comparison function F(n) = (1 - tau(n)/2) * log(n).
    """
    return (1.0 - tau_n / 2.0) * math.log(n)

def is_prime(n: int) -> bool:
    """
    Determine if n is prime by its divisor count.
    """
    return get_tau(n) == 2

def next_prime(p: int) -> int:
    """
    Direct next-prime rule. Compute exact divisor counts for integers > p,
    stop at the first integer with exactly two positive divisors.
    """
    n = p + 1
    while True:
        if get_tau(n) == 2:
            return n
        n += 1

def analyze_gap(p: int, q: int) -> Dict[str, Any]:
    """
    Analyze the interior of the gap (p, q).
    Extracts the GWR selected witness, minimum tau, residual vectors, 
    and dynamic cutoff bounds.
    """
    interior = list(range(p + 1, q))
    if not interior:
        return None

    # Compute bounds from PROOF.md
    c_q = max(64, math.ceil(0.5 * (math.log(q) ** 2)))

    # Compute tau, LPF, and F(n) for the entire interior
    taus = [get_tau(n) for n in interior]
    lpfs = [get_least_prime_factor(n) for n in interior]
    F_vals = [get_F(n, taus[i]) for i, n in enumerate(interior)]
    
    # Leftmost Minimum-Divisor Rule (GWR)
    min_tau = min(taus)
    w_offset = taus.index(min_tau)
    w = p + 1 + w_offset

    # Extract residual vectors for boundaries and witness
    p_res = {f"mod_{m}": p % m for m in M_V1_MODULI}
    q_res = {f"mod_{m}": q % m for m in M_V1_MODULI}
    w_res = {f"mod_{m}": w % m for m in M_V1_MODULI}
    
    # For very fine-grained analysis, we also dump the remainder tracks 
    # of the core primorials (2, 3, 5, 30) for the whole interior.
    interior_residuals_30 = [n % 30 for n in interior]
    interior_residuals_210 = [n % 210 for n in interior]

    return {
        "p": p,
        "q": q,
        "gap": q - p,
        "C_q_bound": c_q,
        "w": w,
        "w_offset": w - p,
        "min_tau": min_tau,
        "tau_w": min_tau, 
        "F_w": F_vals[w_offset],
        "boundary_residuals": {
            "p": p_res,
            "q": q_res
        },
        "witness_residuals": w_res,
        "interior_data": {
            "taus": taus,
            "least_prime_factors": lpfs,
            "F_vals": [round(f, 4) for f in F_vals],
            "mod_30": interior_residuals_30,
            "mod_210": interior_residuals_210
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Joint Modulus-Link and Divisor-Count Probe")
    parser.add_argument("--start", type=int, default=11, help="Starting prime")
    parser.add_argument("--count", type=int, default=1000, help="Number of gaps to probe")
    parser.add_argument("--out", type=str, help="Output JSONL file (default: stdout)")
    
    args = parser.parse_args()
    
    p = args.start
    if not is_prime(p):
        p = next_prime(p)

    out_file = open(args.out, 'w') if args.out else sys.stdout

    try:
        for _ in range(args.count):
            q = next_prime(p)
            
            result = analyze_gap(p, q)
            if result:
                out_file.write(json.dumps(result) + "\n")
            
            p = q
    finally:
        if args.out:
            out_file.close()

if __name__ == "__main__":
    main()
