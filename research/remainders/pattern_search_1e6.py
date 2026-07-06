import json
from collections import defaultdict
import time
import sys

def main():
    input_file = "research/remainders/output/1e6/raw_records.jsonl"
    
    # We want to find P(dist_to_next == 1 | feature)
    
    total_records = 0
    total_dist_1 = 0
    
    # Feature 1: number of zeros in remainder_vector
    zeros_counts = defaultdict(lambda: {"total": 0, "dist_1": 0})
    
    # Feature 2: remainder mod 30 (index 4)
    mod30_counts = defaultdict(lambda: {"total": 0, "dist_1": 0})
    
    # Feature 3: remainder mod 210 (index 5)
    mod210_counts = defaultdict(lambda: {"total": 0, "dist_1": 0})
    
    # Feature 4: remainder mod 6 (derived from mod 30)
    mod6_counts = defaultdict(lambda: {"total": 0, "dist_1": 0})
    
    # We also want to look at the GWR winner specifically.
    gwr_dist_1 = 0
    gwr_total = 0
    gwr_zeros_counts = defaultdict(lambda: {"total": 0, "dist_1": 0})
    
    t0 = time.time()
    
    with open(input_file, "r") as f:
        for line in f:
            if not line.strip(): continue
            rec = json.loads(line)
            total_records += 1
            
            vec = rec.get("remainder_vector")
            if not vec: continue
            
            dist = rec.get("distance_to_next_prime")
            if dist is None:
                dist = rec.get("termination_distance")
            if dist is None: continue
            
            is_dist_1 = (dist == 1)
            if is_dist_1:
                total_dist_1 += 1
                
            num_zeros = sum(1 for v in vec if v == 0)
            zeros_counts[num_zeros]["total"] += 1
            if is_dist_1: zeros_counts[num_zeros]["dist_1"] += 1
            
            mod30 = vec[4]
            mod30_counts[mod30]["total"] += 1
            if is_dist_1: mod30_counts[mod30]["dist_1"] += 1
            
            mod210 = vec[5]
            mod210_counts[mod210]["total"] += 1
            if is_dist_1: mod210_counts[mod210]["dist_1"] += 1
            
            mod6 = mod30 % 6
            mod6_counts[mod6]["total"] += 1
            if is_dist_1: mod6_counts[mod6]["dist_1"] += 1
            
            is_gwr = rec.get("is_gwr_winner") or rec.get("is_current_min_d")
            if is_gwr:
                gwr_total += 1
                if is_dist_1:
                    gwr_dist_1 += 1
                gwr_zeros_counts[num_zeros]["total"] += 1
                if is_dist_1:
                    gwr_zeros_counts[num_zeros]["dist_1"] += 1
                    
            if total_records % 100000 == 0:
                print(f"Processed {total_records} records...", file=sys.stderr)
                
    t1 = time.time()
    print(f"Time to process: {t1 - t0:.2f}s")
    
    baseline_prob = total_dist_1 / total_records if total_records else 0
    print(f"Total records: {total_records}")
    print(f"Baseline P(dist==1): {baseline_prob:.4f} ({total_dist_1}/{total_records})")
    
    print("\n--- By Number of Zeros ---")
    for k in sorted(zeros_counts.keys()):
        d = zeros_counts[k]
        p = d["dist_1"] / d["total"] if d["total"] else 0
        lift = p / baseline_prob if baseline_prob else 0
        print(f"Zeros={k}: P(dist=1) = {p:.4f} (Lift: {lift:.2f}x) | Total: {d['total']}")
        
    print("\n--- By Mod 6 ---")
    for k in sorted(mod6_counts.keys()):
        d = mod6_counts[k]
        p = d["dist_1"] / d["total"] if d["total"] else 0
        lift = p / baseline_prob if baseline_prob else 0
        print(f"Mod6={k}: P(dist=1) = {p:.4f} (Lift: {lift:.2f}x) | Total: {d['total']}")
        
    print("\n--- Top 5 Mod 30 signals (min 1000 samples) ---")
    valid_mod30 = [(k, v) for k, v in mod30_counts.items() if v["total"] >= 1000]
    valid_mod30.sort(key=lambda x: x[1]["dist_1"]/x[1]["total"], reverse=True)
    for k, d in valid_mod30[:5]:
        p = d["dist_1"] / d["total"]
        lift = p / baseline_prob
        print(f"Mod30={k}: P(dist=1) = {p:.4f} (Lift: {lift:.2f}x) | Total: {d['total']}")
        
    print("\n--- Top 5 Mod 210 signals (min 1000 samples) ---")
    valid_mod210 = [(k, v) for k, v in mod210_counts.items() if v["total"] >= 1000]
    valid_mod210.sort(key=lambda x: x[1]["dist_1"]/x[1]["total"], reverse=True)
    for k, d in valid_mod210[:5]:
        p = d["dist_1"] / d["total"]
        lift = p / baseline_prob
        print(f"Mod210={k}: P(dist=1) = {p:.4f} (Lift: {lift:.2f}x) | Total: {d['total']}")
        
    print("\n--- GWR Winner Analysis ---")
    gwr_prob = gwr_dist_1 / gwr_total if gwr_total else 0
    gwr_lift = gwr_prob / baseline_prob if baseline_prob else 0
    print(f"Overall GWR P(dist=1): {gwr_prob:.4f} (Lift: {gwr_lift:.2f}x) | Total: {gwr_total}")
    for k in sorted(gwr_zeros_counts.keys()):
        d = gwr_zeros_counts[k]
        if d["total"] < 100: continue
        p = d["dist_1"] / d["total"]
        lift = p / baseline_prob
        print(f"  GWR Zeros={k}: P(dist=1) = {p:.4f} (Lift: {lift:.2f}x) | Total: {d['total']}")

if __name__ == '__main__':
    main()
