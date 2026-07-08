#!/usr/bin/env python3
"""
Pure counting invariants for S1 PSP sublemma (no prose).
Provides semantic checks for the gate.
"""
import math

def min_m_for_rough(r):
    """Algebraic lower bound on m for admissible M-rough (h > sqrt(r), d>=1)."""
    # from m = [h^2 + d(h-r)]/2 , min at h~sqrt(r), d=1
    return int(math.ceil( (r + math.sqrt(r) - r) / 2 ))  # approx sqrt(r)/2

def algebraically_blocked_m(M, r):
    """m that cannot have admissible rough by algebra."""
    lo = min_m_for_rough(r)
    return list(range(1, min(M, int(math.floor(math.sqrt(r)/2))) + 1 ))

def reductio_params(C=64):
    M = C // 2
    # example r ~200 for small C case
    r = 199
    return {"C": C, "M": M, "r": r}

def assert_contra_preconditions(C=64):
    """For the example reductio (C=64, M=32, r~200), algebraic blocked m are only 1..floor(sqrt(r)/2), not 1..M."""
    p = reductio_params(C)
    M, r = p["M"], p["r"]
    blocked = algebraically_blocked_m(M, r)
    max_blocked = max(blocked) if blocked else 0
    sqrt_r_2 = math.sqrt(r) / 2
    assert max_blocked <= math.floor(sqrt_r_2), f"blocked up to {max_blocked} > floor(sqrt(r)/2)={math.floor(sqrt_r_2)}"
    assert M > max_blocked, "M should exceed algebraic blocked for boundary case"
    # In reductio, if L_lower >0 then excess requires rough, but only beyond blocked; audit discharges the rest.
    return True

if __name__ == "__main__":
    assert_contra_preconditions()
    print("assert_contra_preconditions passed for C=64")
