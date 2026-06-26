#!/usr/bin/env python3
"""
Chamber Reset Integrity Checker
Reusable tool that takes a series of load/excess values (E or H) from gap interiors
and reports the alternation (rocking) health as a simple integrity signal for local rules.

This implements the tracker from the bridge diagnostics as a standalone module
for integration into chamber/packet/reset simulations.

Usage:
    from chamber_reset_integrity import check_alternation_integrity
    result = check_alternation_integrity(e_series)
    print(result["flip_rate"], result["max_break"])
"""

import numpy as np

def check_alternation_integrity(series):
    """
    Input: list or array of E or H values across consecutive gaps.
    Output: dict with flip_rate (higher = healthier local rocking),
            mean_run, max_run (lower max = fewer long breaks),
            and a simple status string.
    """
    series = np.array(series, dtype=float)
    if len(series) < 2:
        return {
            "flip_rate": 0.0,
            "mean_run": 0.0,
            "max_run": 0,
            "status": "insufficient_data"
        }
    
    deltas = np.diff(series)
    signs = np.sign(deltas)
    
    # Flip count
    flips = sum(1 for j in range(len(signs)-1)
                if signs[j] != 0 and signs[j+1] != 0 and signs[j] != signs[j+1])
    flip_rate = flips / (len(signs) - 1) if len(signs) > 1 else 0.0
    
    # Run lengths
    run_lengths = []
    current = 1
    for j in range(1, len(signs)):
        if signs[j] == signs[j-1] and signs[j] != 0:
            current += 1
        else:
            if current > 1:
                run_lengths.append(current)
            current = 1
    if current > 1:
        run_lengths.append(current)
    
    mean_run = float(np.mean(run_lengths)) if run_lengths else 0.0
    max_run = int(np.max(run_lengths)) if run_lengths else 0
    
    # Simple status
    if flip_rate > 0.35 and max_run < 10:
        status = "healthy_local_rocking"
    elif max_run > 20:
        status = "long_break_detected_investigate"
    else:
        status = "moderate"
    
    return {
        "flip_rate": float(flip_rate),
        "mean_run": mean_run,
        "max_run": max_run,
        "status": status,
        "num_points": len(series)
    }

if __name__ == "__main__":
    # Quick self-test with dummy data mimicking alternation
    test_series = [10, 12, 9, 11, 8, 13, 7, 14]  # artificial rocking
    result = check_alternation_integrity(test_series)
    print("Self-test result:", result)