import math
import sympy
import gmpy2

def compute_C(q: int) -> int:
    return max(64, math.ceil(0.5 * (math.log(q) ** 2)))

def least_prime_factor(n: int) -> int:
    if n <= 1:
        return 1
    # Simple trial division up to sqrt(n)
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

def audit_square_branches(limit_r: int):
    print(f"Auditing square branches for r up to {limit_r}...")
    
    worst_case_ratio = 0.0
    worst_case_info = None

    # We iterate over odd primes r
    for r in sympy.primerange(3, limit_r):
        w = r * r
        p = int(gmpy2.prev_prime(w))
        q = int(gmpy2.next_prime(w))
        
        # Check if w is the left-most minimum in (p, q).
        # We need tau(n) >= 4 for all p < n < w.
        # Let's use sympy.divisor_count for simplicity since the range is small.
        is_winner = True
        for n in range(p + 1, w):
            if sympy.divisor_count(n) < 4:
                is_winner = False
                break
        
        if not is_winner:
            continue
            
        C_q = compute_C(q)
        M = C_q // 2
        offset = w - p
        
        ratio = offset / C_q
        if ratio > worst_case_ratio:
            worst_case_ratio = ratio
            
            # Analyze rows
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
                
                # Check admissibility
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
                "injectivity_holds": injectivity_holds
            }

    print("\n--- Worst Case Square Branch ---")
    if worst_case_info:
        print(f"r = {worst_case_info['r']} (w = {worst_case_info['w']})")
        print(f"Gap: ({worst_case_info['p']}, {worst_case_info['q']})")
        print(f"w - p = {worst_case_info['offset']} | C(q) = {worst_case_info['C_q']}")
        print(f"Ratio: {worst_case_info['ratio']:.4f}")
        print(f"Injectivity on M-rough rows holds: {worst_case_info['injectivity_holds']}")
        print(f"Total rows M = {worst_case_info['M']}, Valid rows (2m < w-p) = {len(worst_case_info['rows'])}")
        print(f"M-rough rows count: {len(worst_case_info['m_rough_rows'])}")
        
        print("\nLeast-factor sequences (Top 10 rows):")
        for row in worst_case_info["rows"][:10]:
            rough_str = " [M-ROUGH]" if row["is_m_rough"] else ""
            sym_str = " [SYMMETRIC]" if row["is_symmetric"] else ""
            print(f"  m={row['m']:<3} | x_m={row['x_m']:<10} | l_m={row['l_m']:<5} | h_m={row['h_m']:<4} | d_m={row['d_m']:<4}{rough_str}{sym_str}")
        
    else:
        print("No valid square branches found.")

if __name__ == "__main__":
    # Run up to r=5000 (w=25,000,000) for a quick audit.
    # We can increase this later for deeper stress testing.
    audit_square_branches(10000)
