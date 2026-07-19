"""
weight_gap_classifier.py
Built from hybrid_decomp_pgs_50000.csv (p up to 611k, 49,996 gaps)
Combines decompwlj weight k with PGS Gap Winner data.

Implements the deterministic gap sieve:
- k = min divisor of ell=p-g with divisor > g
- g < k, g even, p ≡ g (mod k)
- For small k, possible g set is tiny (k=3->{2}, k=5->{4})

Provides:
- build table (precomputed JSON)
- get_possible_gaps(k)
- is_consistent(k,g)
- predict_next_gap(p) using hypothesized g's
- filter candidates using PGS winner check (optional tau)
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

TABLE_PATH = Path(__file__).parent / "weight_gap_table_50k.json"

# Load precomputed table if available
def load_table(path: Path = TABLE_PATH) -> Dict[int, Dict]:
    if not path.exists():
        # fallback to /mnt/data for notebook env
        alt = Path("/mnt/data/weight_gap_table_50k.json")
        if alt.exists():
            path = alt
        else:
            raise FileNotFoundError(f"Table not found at {path} or /mnt/data/weight_gap_table_50k.json")
    with open(path) as f:
        raw = json.load(f)
    # keys are str in JSON
    return {int(k): v for k, v in raw.items()}

try:
    _TABLE = load_table()
except Exception:
    _TABLE = {}

def get_table() -> Dict[int, Dict]:
    return _TABLE

def get_possible_gaps(k: int, table: Dict[int, Dict] = None) -> Set[int]:
    """Return set of g that have ever occurred with this weight k in 50k data."""
    tbl = table or _TABLE
    if k in tbl:
        return set(tbl[k]['possible_g'])
    return set()

def is_consistent(k: int, g: int, table: Dict[int, Dict] = None) -> bool:
    """Check if gap g is in historically allowed set for weight k."""
    return g in get_possible_gaps(k, table)

def divisors(n: int) -> List[int]:
    if n <= 0:
        return []
    divs = set()
    r = int(math.isqrt(n))
    for i in range(1, r+1):
        if n % i == 0:
            divs.add(i)
            divs.add(n//i)
    return sorted(divs)

def compute_k_for_hypothesized_gap(p: int, g: int) -> Optional[int]:
    """
    Given current prime p and hypothesized even gap g,
    compute what decompwlj weight k would be: min divisor of ell=p-g > g.
    Returns None if ell <= g or no divisor > g (should not happen for p>7).
    """
    if g % 2 == 1:
        return None
    ell = p - g
    if ell <= g:
        return None
    for d in divisors(ell):
        if d > g:
            # need smallest > g, divisors sorted
            # but divisors() returns sorted, so first > g is min
            return d
    return None

def compute_k_for_hypothesized_gap_sorted(p: int, g: int) -> Optional[int]:
    ell = p - g
    if ell <= g or g % 2 == 1:
        return None
    for d in sorted(divisors(ell)):
        if d > g:
            return d
    return None

def predict_next_gap_candidates(p: int, max_g: int = 100, table: Dict[int, Dict] = None) -> List[Dict]:
    """
    For a given prime p, enumerate even g=2,4,6,... up to max_g,
    compute implied k = k(p,g), and keep only those where g is in allowed set for that k
    (i.e., historically consistent). This is the deterministic sieve.
    Returns list of dicts sorted by g.
    """
    tbl = table or _TABLE
    candidates = []
    for g in range(2, max_g+1, 2):
        ell = p - g
        if ell <= g:
            continue
        # compute k
        divs = divisors(ell)
        k = None
        for d in divs:
            if d > g:
                k = d
                break
        if k is None:
            continue
        possible = get_possible_gaps(k, tbl)
        # If k unseen in table, we allow it but mark as novel
        consistent = (not possible) or (g in possible)
        if consistent:
            candidates.append({
                'g': g,
                'ell': ell,
                'k': k,
                'L': ell//k,
                'class': 'level' if k*k > ell else 'weight',
                'num_options_for_k': len(possible) if possible else 0,
                'is_novel_k': len(possible)==0,
                'mean_g_for_k': tbl.get(k, {}).get('mean_g'),
            })
    return candidates

def pgs_gap_winner(p: int, g: int):
    """Minimal PGS check: find tau-minimizer in (p,p+g). Requires tau."""
    # local import to avoid hard dep
    try:
        from prime_gap_structure import tau
    except ImportError:
        # fallback trial tau
        def tau(n):
            cnt=0
            r=int(math.isqrt(n))
            for i in range(1,r+1):
                if n%i==0:
                    cnt+=1 if i*i==n else 2
            return cnt
    interior = range(p+1, p+g)
    if not interior:
        return None
    best_n, best_tau = None, None
    for n in interior:
        t = tau(n)
        if best_tau is None or t < best_tau:
            best_tau = t
            best_n = n
    return {'w': best_n, 'tau_w': best_tau, 'compress': best_n-p if best_n else None}

def filtered_next_prime_search(p: int, max_g: int = 100, use_pgs_prune: bool = True, table: Dict[int, Dict] = None):
    """
    Combined decompwlj + PGS filter:
    1. Enumerate g candidates via weight consistency (reduces from max_g/2 to ~3-6 options for small k)
    2. Optionally rank by PGS compress (prefer small compress) and tau_w
    """
    cands = predict_next_gap_candidates(p, max_g, table)
    # Enrich with PGS winner
    for c in cands:
        pw = pgs_gap_winner(p, c['g'])
        if pw:
            c.update(pw)
    # Sort: first by whether k small (mean_g small), then compress
    cands_sorted = sorted(cands, key=lambda x: (x.get('num_options_for_k',99), x.get('compress',99), x['g']))
    return cands_sorted

# Precomputed stats summary
SUMMARY = {
    'total_distinct_k': len(_TABLE),
    'mean_options_given_k': sum(v['num_possible_g'] for v in _TABLE.values())/len(_TABLE) if _TABLE else 0,
}

if __name__ == "__main__":
    # demo on some primes
    test_primes = [113, 523, 259033, 610921]
    for p in test_primes:
        cands = predict_next_gap_candidates(p, max_g=50)
        print(f"\n p={p} -> {len(cands)} consistent g out of 25 evens (up to 50):")
        for c in cands[:10]:
            print(f"  g={c['g']:2d} ell={c['ell']} k={c['k']:6d} L={c['L']:6d} {c['class']:6s} options_for_k={c['num_options_for_k']} mean_g_for_k={c.get('mean_g_for_k')}")
