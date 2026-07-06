def is_prime(n):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, int(n**0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def get_gap(n):
    p = n - 1
    while not is_prime(p):
        p -= 1
    q = n + 1
    while not is_prime(q):
        q += 1
    return p, q

def main():
    import math
    def d(n):
        count = 0
        limit = int(math.isqrt(n))
        for i in range(1, limit + 1):
            if n % i == 0:
                count += 2
        if limit * limit == n:
            count -= 1
        return count
    
    print("Gap 308003 to 308017:")
    min_d = 9999
    gwr_n = None
    for n in range(308004, 308017):
        dn = d(n)
        print(f"n={n}, d(n)={dn}")
        if dn < min_d:
            min_d = dn
            gwr_n = n
            
    print(f"GWR winner: {gwr_n} with d={min_d}")
    
if __name__ == '__main__':
    main()
