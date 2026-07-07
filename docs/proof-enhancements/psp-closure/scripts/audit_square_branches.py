import math
import sys
import sympy
import gmpy2

def compute_C(q: int) -> int:
    return max(64, math.ceil(0.5 * (math.log(q) ** 2)))

def least_prime_factor(n: int) -> int:
    if n <= 1:
        return 1
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    d = 5
    while d * d <= n:
        if n % d == 0:
            return d
        if n % (d + 2) == 0:
            return d + 2
        d += 6
    return n

def quick_tau_min_in_gap(p: int, w: int) -> bool:
    """Returns True if all integers strictly between p and w have tau >= 4."""
    gap_len = w - p - 1
    if gap_len <= 0:
        return True
    
    # We will compute tau for all n in [p+1, w-1]
    # To do this quickly without full factorization, we can do a local sieve.
    start = p + 1
    end = w
    
    tau = [1] * gap_len
    residue = list(range(start, end))
    
    # Sieve up to sqrt(w)
    limit = math.isqrt(end) + 1
    for prime in sympy.primerange(2, limit):
        # find first multiple
        first_mult = ((start + prime - 1) // prime) * prime
        for i in range(first_mult - start, gap_len, prime):
            count = 0
            while residue[i] % prime == 0:
                residue[i] //= prime
                count += 1
            tau[i] *= (count + 1)
            
    for i in range(gap_len):
        if residue[i] > 1:
            # check if it's a prime (we know residue <= w, so if it has no prime factor <= sqrt(w) it is prime)
            tau[i] *= 2
            
        if tau[i] < 4:
            return False
            
    return True

def audit_square_branches(limit_r: int):
    print(f"Auditing square branches for r up to {limit_r}...")
    
    worst_case_ratio = 0.0
    worst_case_info = None

    for r in sympy.primerange(3, limit_r):
        w = r * r
        p = int(gmpy2.prev_prime(w))
        q = int(gmpy2.next_prime(w))
        
        # We need tau(n) >= 4 for all p < n < w.
        if not quick_tau_min_in_gap(p, w):
            continue
            
        C_q = compute_C(q)
        M = C_q // 2
        offset = w - p
        
        ratio = offset / C_q
        if ratio > worst_case_ratio:
            worst_case_ratio = ratio
            
            rows = []
            m_rough_rows = []
            l_m_seen = set()
            injectivity_holds = True
            
            for m in range(1, M + 1):
                if 2 * m >= offset:
                    break
                x_m = w - 2 * m
                l_m = least_prime_factor(x_m)
                h_m = r - l_m
                
                d_m = x_m // l_m - r - h_m
                is_symmetric = (d_m == 0)
                is_m_rough = (l_m > M)
                
                row_info = {
                    "m": m,
                    "x_m": x_m,
                    "l_m": l_m,
                    "h_m": h_m,
                    "d_m": d_m,
                    "is_symmetric": is_symmetric,
                    "is_m_rough": is_m_rough
                }
                rows.append(row_info)
                
                if is_m_rough:
                    m_rough_rows.append(row_info)
                    if l_m in l_m_seen:
                        injectivity_holds = False
                    l_m_seen.add(l_m)
            
            available_primes = sympy.primepi(int(r - math.sqrt(r))) - sympy.primepi(M)
                    
            worst_case_info = {
                "r": r,
                "p": p,
                "q": q,
                "w": w,
                "offset": offset,
                "C_q": C_q,
                "M": M,
                "ratio": ratio,
                "rows": rows,
                "m_rough_rows": m_rough_rows,
                "injectivity_holds": injectivity_holds,
                "available_primes": available_primes
            }
            print(f"New worst ratio: {ratio:.4f} at r={r} (w-p={offset}, C(q)={C_q})")
            if ratio > 1.0:
                print(f"!!! BOUND VIOLATION at r={r} !!!")

    print("\n--- Deep Sweep: Worst Case Square Branch ---")
    if worst_case_info:
        print(f"r = {worst_case_info['r']} (w = {worst_case_info['w']})")
        print(f"Gap: ({worst_case_info['p']}, {worst_case_info['q']})")
        print(f"w - p = {worst_case_info['offset']} | C(q) = {worst_case_info['C_q']}")
        print(f"Ratio: {worst_case_info['ratio']:.4f}")
        print(f"Injectivity on M-rough rows holds: {worst_case_info['injectivity_holds']}")
        print(f"Total rows M = {worst_case_info['M']}, Valid rows (2m < w-p) = {len(worst_case_info['rows'])}")
        print(f"M-rough rows count: {len(worst_case_info['m_rough_rows'])}")
        print(f"Available primes in (M, r-sqrt(r)): {worst_case_info['available_primes']}")
        print(f"Saturation: {len(worst_case_info['m_rough_rows'])} / {worst_case_info['available_primes']} used")
        
        print("\nLeast-factor sequences (M-rough rows subset):")
        for row in worst_case_info["m_rough_rows"]:
            sym_str = " [SYMMETRIC]" if row["is_symmetric"] else ""
            print(f"  m={row['m']:<3} | x_m={row['x_m']:<10} | l_m={row['l_m']:<5} | h_m={row['h_m']:<4} | d_m={row['d_m']:<4}{sym_str}")
        
    else:
        print("No valid square branches found.")

if __name__ == "__main__":
    limit = 1_000_000
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    audit_square_branches(limit)
