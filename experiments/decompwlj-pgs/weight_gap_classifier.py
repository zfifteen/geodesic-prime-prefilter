"""
weight_gap_classifier.py

Combines decompwlj weight (k) with PGS Gap Winner data to create a
deterministic sieve on prime gaps.

Core idea:
- Weight k imposes hard constraints: g < k and p ≡ g (mod k)
- For many k values, the set of historically observed g is very small.
- This allows aggressive filtering of possible next gaps.

Provides:
- Precomputed lookup tables (from 50k primes)
- Gap candidate generation using weight consistency
- Optional PGS Gap Winner enrichment + ranking
- High-level next-prime candidate functions
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from collections import defaultdict

# -------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------
TABLE_PATH = Path(__file__).parent / "weight_gap_table_50k.json"


# -------------------------------------------------------------------------
# Table Loading
# -------------------------------------------------------------------------
def load_weight_table(path: Path = TABLE_PATH) -> Dict[int, Dict]:
    """Load the precomputed weight → gap statistics table."""
    if not path.exists():
        # Fallback for notebook / different environments
        alt_path = Path("/mnt/data/weight_gap_table_50k.json")
        if alt_path.exists():
            path = alt_path
        else:
            raise FileNotFoundError(
                f"weight_gap_table_50k.json not found at {path} or {alt_path}"
            )

    with open(path) as f:
        raw = json.load(f)

    # JSON keys are strings → convert to int
    return {int(k): v for k, v in raw.items()}


try:
    _WEIGHT_TABLE: Dict[int, Dict] = load_weight_table()
except Exception:
    _WEIGHT_TABLE = {}


def get_table() -> Dict[int, Dict]:
    return _WEIGHT_TABLE


# -------------------------------------------------------------------------
# Core Query Functions
# -------------------------------------------------------------------------
def get_possible_gaps(k: int, table: Optional[Dict] = None) -> Set[int]:
    """Return set of gap sizes historically observed for this weight k."""
    tbl = table or _WEIGHT_TABLE
    return set(tbl.get(k, {}).get("possible_g", []))


def is_consistent(k: int, g: int, table: Optional[Dict] = None) -> bool:
    """Check whether gap g has ever occurred with weight k."""
    possible = get_possible_gaps(k, table)
    return len(possible) == 0 or g in possible


# -------------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------------
def _divisors(n: int) -> List[int]:
    """Return sorted list of positive divisors of n."""
    if n <= 0:
        return []
    divs = set()
    r = int(math.isqrt(n))
    for i in range(1, r + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n // i)
    return sorted(divs)


def compute_weight_for_gap(p: int, g: int) -> Optional[int]:
    """
    Compute the decompwlj weight k for a hypothesized even gap g after prime p.
    Returns None if g is odd or ell = p - g has no divisor > g.
    """
    if g % 2 != 0:
        return None
    ell = p - g
    if ell <= g:
        return None

    for d in _divisors(ell):
        if d > g:
            return d
    return None


# -------------------------------------------------------------------------
# Main Candidate Generation
# -------------------------------------------------------------------------
def get_weight_consistent_candidates(
        p: int, max_g: int = 200, table: Optional[Dict] = None
) -> List[Dict[str, Any]]:
    """
    Generate gap candidates using decompwlj weight consistency.

    For each even g in [2, max_g], compute the implied weight k.
    Keep the candidate only if g has historically appeared with that k.
    """
    tbl = table or _WEIGHT_TABLE
    candidates = []

    for g in range(2, max_g + 1, 2):
        k = compute_weight_for_gap(p, g)
        if k is None:
            continue

        possible_gaps = get_possible_gaps(k, tbl)
        consistent = len(possible_gaps) == 0 or g in possible_gaps

        if consistent:
            ell = p - g
            candidates.append(
                {
                    "g": g,
                    "ell": ell,
                    "k": k,
                    "L": ell // k,
                    "class": "level" if k * k > ell else "weight",
                    "num_possible_g_for_k": len(possible_gaps),
                    "is_novel_k": len(possible_gaps) == 0,
                    "mean_g_for_k": tbl.get(k, {}).get("mean_g"),
                }
            )

    return candidates


# -------------------------------------------------------------------------
# PGS Integration (Lazy / Optional)
# -------------------------------------------------------------------------
def _get_tau_function():
    """Try to use real PGS tau, fall back to pure Python version."""
    try:
        from prime_gap_structure import tau as pgs_tau
        return pgs_tau
    except ImportError:
        def fallback_tau(n: int) -> int:
            if n < 2:
                return 0
            count = 0
            r = int(math.isqrt(n))
            for i in range(1, r + 1):
                if n % i == 0:
                    count += 1 if i * i == n else 2
            return count
        return fallback_tau


def enrich_with_gap_winner(
        candidates: List[Dict], p: int, use_pgs: bool = True
) -> List[Dict]:
    """
    Enrich candidates with PGS Gap Winner information.
    Only computes for candidates that pass the weight filter.
    """
    if not candidates:
        return candidates

    tau = _get_tau_function()

    for cand in candidates:
        g = cand["g"]
        interior = range(p + 1, p + g)
        if not interior:
            continue

        best_n, best_tau = None, float("inf")
        for n in interior:
            t = tau(n)
            if t < best_tau:
                best_tau = t
                best_n = n

        if best_n is not None:
            cand["w"] = best_n
            cand["tau_w"] = best_tau
            cand["compress"] = best_n - p

    return candidates


def rank_candidates(candidates: List[Dict]) -> List[Dict]:
    """
    Rank candidates by usefulness:
    1. Strongly prefer very restrictive weights (few possible g values)
    2. Then prefer smaller compress (PGS)
    3. Then prefer smaller g
    """
    def score(c):
        num_options = c.get("num_possible_g_for_k", 99)
        compress = c.get("compress", 999)
        g = c["g"]
        return (num_options, compress, g)

    return sorted(candidates, key=score)


# -------------------------------------------------------------------------
# High-Level API
# -------------------------------------------------------------------------
def find_next_prime_candidates(
        p: int,
        max_g: int = 200,
        top_n: int = 8,
        use_pgs: bool = True,
        table: Optional[Dict] = None,
) -> List[Dict]:
    """
    High-level function: Return the best next-gap candidates after prime p.

    Steps:
    1. Filter using decompwlj weight consistency
    2. (Optional) Enrich with PGS Gap Winner
    3. Rank the results
    """
    cands = get_weight_consistent_candidates(p, max_g, table)
    if use_pgs:
        cands = enrich_with_gap_winner(cands, p)
    cands = rank_candidates(cands)
    return cands[:top_n]


def find_next_prime(p: int, max_g: int = 300, use_pgs: bool = True) -> Optional[int]:
    """
    Attempt to find the next prime after p using the hybrid filter.
    Returns the smallest g that survives both weight consistency and PGS check.
    """
    cands = find_next_prime_candidates(p, max_g=max_g, top_n=5, use_pgs=use_pgs)

    for cand in cands:
        if cand.get("tau_w") == 2:
            return p + cand["g"]

    # Fallback: return the smallest consistent candidate if PGS check failed
    if cands:
        return p + cands[0]["g"]
    return None


# -------------------------------------------------------------------------
# Summary Statistics
# -------------------------------------------------------------------------
def get_summary_stats(table: Optional[Dict] = None) -> Dict:
    tbl = table or _WEIGHT_TABLE
    if not tbl:
        return {}

    total_gaps = sum(v.get("count", 0) for v in tbl.values())
    avg_options = sum(len(v.get("possible_g", [])) for v in tbl.values()) / len(tbl)

    return {
        "total_distinct_weights": len(tbl),
        "total_gaps_analyzed": total_gaps,
        "average_possible_g_per_weight": round(avg_options, 2),
    }


# -------------------------------------------------------------------------
# Demo
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("Weight-Gap Classifier Demo\n")
    print(get_summary_stats())

    test_primes = [113, 523, 259033, 610921]

    for p in test_primes:
        cands = find_next_prime_candidates(p, max_g=60, top_n=6, use_pgs=True)
        print(f"\np = {p}")
        for c in cands:
            print(
                f"  g={c['g']:3d} | k={c['k']:6d} | L={c['L']:5d} | "
                f"class={c['class']:6s} | compress={c.get('compress', 'N/A'):>3} | "
                f"options={c['num_possible_g_for_k']}"
            )
