# Place in src/python/prime_gap_structure/decompwlj.py
# Then: from prime_gap_structure.decompwlj import decomp_prime, generate_hybrid_csv

import math
import csv
from typing import Dict, List, Optional, Any
from prime_gap_structure import gap_walk, tau, dni  # core primitives

def _get_divisors(n: int) -> List[int]:
    """Trial-division divisors (sufficient for ell ~ p; optimize with sympy/factors for scale)."""
    if n <= 0:
        return []
    divs: List[int] = []
    sqrt_n = int(math.sqrt(n)) + 1
    for i in range(1, sqrt_n):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    return sorted(set(divs))

def decomp_prime(p: int, q: int) -> Optional[Dict[str, Any]]:
    """
    Joint decompwlj + PGS enrichment for consecutive primes p < q.
    Returns None when decomposition does not exist (rare cases p=2,3,7 and some small gaps).
    """
    if p < 2 or q <= p:
        return None
    g = q - p
    ell = 2 * p - q          # = p - g
    if ell <= g:
        return None

    # decompwlj core
    candidates = [k for k in _get_divisors(ell) if k > g]
    if not candidates:
        return None
    k = min(candidates)
    L = ell // k
    classification = "weight" if k <= L else "level"

    # PGS Gap Winner (microscope on interior)
    interior = range(p + 1, q)
    if not interior:
        return None

    tau_list = [(n, tau(n)) for n in interior]
    min_tau = min(t for _, t in tau_list)
    w = min(n for n, t in tau_list if t == min_tau)   # leftmost = GWR

    # DNI coordinates (reuse package if available)
    try:
        E_w = dni.E(w)
        Z_w = dni.Z(w)
    except AttributeError:
        E_w = (tau(w) / 2 - 1) * math.log(w)
        Z_w = math.exp(-E_w)

    is_square_branch = (tau(w) == 3)   # prime square
    compress = w - p

    return {
        "p": p,
        "q": q,
        "g": g,
        "ell": ell,
        "k": k,
        "L": L,
        "class": classification,
        "w": w,
        "tau_w": tau(w),
        "E_w": round(E_w, 6),
        "Z_w": round(Z_w, 6),
        "is_square": is_square_branch,
        "compress": compress,
    }

def collect_primes(start: int = 2, count: int = 1000) -> List[int]:
    """Iteratively collect primes using PGS gap_walk."""
    primes = []
    current = start
    for _ in range(count):
        primes.append(current)
        try:
            current = gap_walk(current)
        except Exception:
            break
    return primes

def generate_hybrid_csv(
        num_primes: int = 1000000,
        output_file: str = "hybrid_decomp_pgs.csv",
        start_p: int = 2,
) -> List[Dict]:
    """Build the joint dataset (decompwlj columns + PGS Gap Winner / DNI columns)."""
    primes = collect_primes(start_p, num_primes)
    records = []
    for i in range(len(primes) - 1):
        rec = decomp_prime(primes[i], primes[i + 1])
        if rec:
            records.append(rec)

    if records:
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
        print(f"Wrote {len(records)} joint records to {output_file}")
    return records
