import time
import sys
sys.path.insert(0, 'src/python')

from z_band_prime_composite_field.field import _segmented_primes
from z_band_prime_predictor.simple_pgs_generator import emit_record as emit_v1
from z_band_prime_predictor.simple_pgs_generator_v2 import emit_record as emit_v2

def run_benchmark():
    # Gather a large sample of primes to test
    print("Gathering test primes up to 1,000,000...")
    # Skip the first few to avoid tiny anomalies
    primes = list(_segmented_primes(1_000_000))[10:]
    
    print(f"Total primes to process: {len(primes)}")
    
    # Run V1
    print("Running v1.1.0 generator (Standard)...")
    start_time_v1 = time.perf_counter()
    for p in primes:
        emit_v1(p)
    end_time_v1 = time.perf_counter()
    time_v1 = end_time_v1 - start_time_v1
    
    # Run V2
    print("Running v1.2.0 generator (Super-Signal)...")
    start_time_v2 = time.perf_counter()
    for p in primes:
        emit_v2(p)
    end_time_v2 = time.perf_counter()
    time_v2 = end_time_v2 - start_time_v2
    
    print("\n--- Benchmark Results ---")
    print(f"V1.1.0 Total Time: {time_v1:.4f} seconds")
    print(f"V1.2.0 Total Time: {time_v2:.4f} seconds")
    
    if time_v2 < time_v1:
        speedup = (time_v1 - time_v2) / time_v1 * 100
        print(f"V1.2.0 is {speedup:.2f}% faster.")
    else:
        print("V1.2.0 is slower in this benchmark.")
        
if __name__ == '__main__':
    run_benchmark()
