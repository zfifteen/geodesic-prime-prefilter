import time
import sys
import sympy

sys.path.insert(0, 'src/python')

from z_band_prime_predictor.simple_pgs_generator import emit_record as emit_v1
from z_band_prime_predictor.simple_pgs_generator_v2 import emit_record as emit_v2

def run_decade_benchmark():
    primes_to_test = []
    
    print("Generating benchmark primes (256 per decade from 10^8 to 10^18)...")
    for exponent in range(8, 19):
        base = 10**exponent
        p = sympy.nextprime(base)
        decade_primes = []
        for _ in range(256):
            decade_primes.append(p)
            p = sympy.nextprime(p)
        primes_to_test.extend(decade_primes)
        
    print(f"Total primes gathered: {len(primes_to_test)}")
    
    # Run V1
    print("Running v1.1.0 generator (Standard)...")
    start_time_v1 = time.perf_counter()
    for p in primes_to_test:
        emit_v1(p, candidate_bound=1024)
    end_time_v1 = time.perf_counter()
    time_v1 = end_time_v1 - start_time_v1
    
    # Run V2
    print("Running v1.2.0 generator (mod30 guard)...")
    start_time_v2 = time.perf_counter()
    for p in primes_to_test:
        emit_v2(p, candidate_bound=1024)
    end_time_v2 = time.perf_counter()
    time_v2 = end_time_v2 - start_time_v2
    
    print("\n--- Benchmark Results (10^8 to 10^18) ---")
    print(f"V1.1.0 Total Time: {time_v1:.4f} seconds")
    print(f"V1.2.0 Total Time: {time_v2:.4f} seconds")
    
    if time_v2 < time_v1:
        speedup = (time_v1 - time_v2) / time_v1 * 100
        print(f"V1.2.0 is {speedup:.2f}% faster.")
    else:
        print("V1.2.0 is slower in this benchmark.")
        
if __name__ == '__main__':
    run_decade_benchmark()
