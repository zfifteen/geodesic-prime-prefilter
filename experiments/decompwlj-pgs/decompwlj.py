import math
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Ensure src/python is in Python's search path
ROOT = Path(__file__).resolve().parents[2]
SRC_PYTHON = ROOT / "src" / "python"
if str(SRC_PYTHON) not in sys.path:
    sys.path.insert(0, str(SRC_PYTHON))

from prime_gap_structure import gap_walk, tau, dni  # core primitives


def _get_divisors(n: int) -> List[int]:
    """Trial-division divisors (fast enough for p up to several million)."""
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
    Returns None for the rare cases where decomposition does not exist.
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

    # PGS Gap Winner
    interior = range(p + 1, q)
    if not interior:
        return None

    tau_list = [(n, tau(n)) for n in interior]
    min_tau = min(t for _, t in tau_list)
    w = min(n for n, t in tau_list if t == min_tau)   # leftmost = GWR

    # DNI coordinates
    try:
        E_w = dni.E(w)
        Z_w = dni.Z(w)
    except AttributeError:
        E_w = (tau(w) / 2 - 1) * math.log(w)
        Z_w = math.exp(-E_w)

    is_square_branch = (tau(w) == 3)
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


def collect_primes(start: int = 2, count: int = 50000) -> List[int]:
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
        num_primes: int = 50000,
        output_file: str = "hybrid_decomp_pgs_50k.csv",
        start_p: int = 2,
) -> List[Dict]:
    """Build the joint decompwlj + PGS dataset."""
    print(f"Collecting first {num_primes} primes using gap_walk...")
    primes = collect_primes(start_p, num_primes)
    print(f"Collected {len(primes)} primes. Now computing hybrid records...")

    records = []
    total = len(primes) - 1

    for i in range(total):
        rec = decomp_prime(primes[i], primes[i + 1])
        if rec:
            records.append(rec)

        # Simple progress every 5,000 gaps
        if (i + 1) % 5000 == 0 or i == total - 1:
            print(f"Processed {i + 1}/{total} gaps → {len(records)} valid records")

    if records:
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
        print(f"\n✅ Wrote {len(records)} hybrid records to: {output_file}")
    else:
        print("No records generated.")
    return records


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate hybrid DecompWLJ + PGS dataset (weight/level + Gap Winner)."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=50000,
        help="Number of primes to process (default: 50000)",
    )
    args = parser.parse_args()

    output_path = os.path.join(os.path.dirname(__file__), f"hybrid_decomp_pgs_{args.n}.csv")
    generate_hybrid_csv(num_primes=args.n, output_file=output_path)
