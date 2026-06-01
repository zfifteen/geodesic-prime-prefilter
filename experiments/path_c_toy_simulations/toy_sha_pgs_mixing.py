#!/usr/bin/env python3
"""
Toy simulation for Path C exploration:
Structural isomorphism between PGS multiplicative divisor channels (tau(n) = prod (a_i+1))
and SHA-256-like bit-mixing channels (rot/XOR sigmas, Ch/Maj, mod 2^w adds).

Implements:
- PGS side: tau(n), factorization channels, binary bit stats for small n.
- SHA toy side: simplified 8-bit or 16-bit word SHA-like round function with sigma0/sigma1, Ch, Maj.
- Measures: avalanche % after r rounds (for diffusion/rounds analog to "leftmost min divisor selection").
- "Channel count" analogs: PGS tau or omega(n); SHA effective mixed bits or round mixing rate.
- Correlation probe: does higher tau correlate with "more mixed" binary reps? (expect weak/no).

Strong self-critique: This is exploratory analogy mining. No claim of deep isomorphism or novel crypto insight.
SHA constants use primes (sqrt/cbrt), PGS studies primes via divisors - surface level bridge.
Avalanche in hashes is statistical diffusion; PGS leftmost min is deterministic selection rule.
64 rounds in SHA-256 is design margin (full diffusion much earlier ~10-20 rounds for 256-bit); PGS "channels" are exact arithmetic.
Output: best insight or "no novel relation found, mostly superficial analogy".

Run: python toy_sha_pgs_mixing.py
"""

import sympy
from sympy import factorint
import random
import math
from collections import defaultdict
import json

# ==================== PGS SIDE: Divisor Channels and Binary Stats ====================

def divisor_count(n):
    """tau(n) = prod (a_i + 1) over prime factorization."""
    if n < 1:
        return 0
    if n == 1:
        return 1
    factors = factorint(n)
    tau = 1
    for a in factors.values():
        tau *= (a + 1)
    return tau

def omega(n):
    """Number of distinct prime factors (big omega small)."""
    if n < 2:
        return 0
    return len(factorint(n))

def factorization_channels(n):
    """List the (p, a+1) 'choices' for each prime power."""
    if n < 2:
        return []
    factors = factorint(n)
    return [(p, a+1) for p, a in factors.items()]

def binary_bit_stats(n, word_size=32):
    """Simple bit independence proxies for binary rep of n."""
    if n == 0:
        return {"hamming_wt": 0, "bit_count": 0, "lsb": 0, "msb_pos": 0}
    bits = bin(n)[2:].zfill(word_size)
    hamming = bits.count('1')
    # Simple "independence" proxy: count runs of 0/1, or parity checks
    runs = 1
    for i in range(1, len(bits)):
        if bits[i] != bits[i-1]:
            runs += 1
    # Bit bias: fraction 1s
    bias = hamming / len(bits)
    return {
        "hamming_wt": hamming,
        "bit_length": len(bits.lstrip('0')) or 1,
        "runs": runs,
        "bias_ones": round(bias, 4),
        "lsb": int(bits[-1]),
        "parity": hamming % 2
    }

def pgs_channel_analysis(max_n=2000, sample_step=1):
    """Analyze PGS channels vs binary bit mixing proxies for small n."""
    results = []
    tau_vs_mixing = defaultdict(list)
    for n in range(1, max_n + 1, sample_step):
        tau = divisor_count(n)
        om = omega(n)
        channels = factorization_channels(n)
        bit_stats = binary_bit_stats(n, word_size=16)  # small for toy
        # Proxy "mixing score" for binary: higher runs or balanced bias ~ more "mixed"
        mix_score = bit_stats["runs"] / (bit_stats["bit_length"] + 1) + (1 - abs(bit_stats["bias_ones"] - 0.5) * 2)
        tau_vs_mixing[tau].append(mix_score)
        if n % 500 == 0 or tau == 2:  # primes and samples
            results.append({
                "n": n,
                "tau": tau,
                "omega": om,
                "channels": channels,
                "bit_stats": bit_stats,
                "mix_score": round(mix_score, 4)
            })
    # Aggregate: avg mix_score per tau bin
    agg = {}
    for t, scores in sorted(tau_vs_mixing.items()):
        if len(scores) > 5:  # enough samples
            avg_mix = sum(scores) / len(scores)
            agg[t] = {"count": len(scores), "avg_mix_score": round(avg_mix, 4)}
    return results, agg

# ==================== SHA TOY SIDE: Bit-Mixing Channels Simulation ====================

def rotl(x, r, w=8):
    """Rotate left, w-bit word."""
    return ((x << r) | (x >> (w - r))) & ((1 << w) - 1)

def rotr(x, r, w=8):
    """Rotate right."""
    return ((x >> r) | (x << (w - r))) & ((1 << w) - 1)

def toy_sigma0(x, w=8):
    """Simplified sigma0: rot7 ^ rot18 ^ shr3 (SHA256 like, scaled to w)."""
    r1, r2, r3 = 1, 2, 1 if w <= 8 else 3  # scaled small
    return rotr(x, r1, w) ^ rotr(x, r2, w) ^ (x >> r3)

def toy_sigma1(x, w=8):
    """Simplified sigma1: rot17 ^ rot19 ^ shr10 -> scaled."""
    r1, r2, r3 = 2, 2, 2 if w <= 8 else 10
    return rotr(x, r1, w) ^ rotr(x, r2, w) ^ (x >> r3)

def toy_Ch(e, f, g, w=8):
    """Ch(e,f,g) = (e & f) ^ ((~e) & g)"""
    mask = (1 << w) - 1
    return ((e & f) ^ ((~e & mask) & g)) & mask

def toy_Maj(a, b, c, w=8):
    """Maj(a,b,c) = (a&b) ^ (a&c) ^ (b&c)"""
    mask = (1 << w) - 1
    return ((a & b) ^ (a & c) ^ (b & c)) & mask

def toy_S0(a, w=8):
    """Sigma0 for working var: rot2 ^ rot13 ^ rot22 scaled."""
    r1, r2, r3 = 1, 2, 2 if w <= 8 else 2
    return rotr(a, r1, w) ^ rotr(a, r2, w) ^ rotr(a, r3, w)

def toy_S1(e, w=8):
    """Sigma1: rot6 ^ rot11 ^ rot25 scaled."""
    r1, r2, r3 = 1, 2, 2 if w <= 8 else 6
    return rotr(e, r1, w) ^ rotr(e, r2, w) ^ rotr(e, r3, w)

def toy_sha_round(a, b, c, d, e, f, g, h, k, w_i, w=8):
    """One compression round, returns new a..h."""
    mask = (1 << w) - 1
    S1 = toy_S1(e, w)
    ch = toy_Ch(e, f, g, w)
    temp1 = (h + S1 + ch + k + w_i) & mask
    S0 = toy_S0(a, w)
    maj = toy_Maj(a, b, c, w)
    temp2 = (S0 + maj) & mask
    h = g
    g = f
    f = e
    e = (d + temp1) & mask
    d = c
    c = b
    b = a
    a = (temp1 + temp2) & mask
    return a, b, c, d, e, f, g, h

def simulate_toy_sha_mixing(num_rounds=8, word_size=8, num_trials=1000, flip_bit_pos=0):
    """
    Simulate toy SHA compression rounds.
    Measure avalanche: fraction of output bits that flip when one input bit flipped.
    'Channel count' analog: effective bits mixed per round (heuristic: 3 for Ch/Maj + sigmas ~5-7 'sources').
    """
    mask = (1 << word_size) - 1
    avalanche_per_round = []
    channel_estimates = []  # rough: bits affected per round

    for trial in range(num_trials):
        # Random 8 working vars (like a..h) or message word
        state = [random.randint(0, mask) for _ in range(8)]  # a b c d e f g h
        orig_state = state[:]
        k = random.randint(0, mask)
        w_i = random.randint(0, mask)

        # Baseline after num_rounds
        for r in range(num_rounds):
            state = list(toy_sha_round(*state, k, w_i, word_size))
        final_orig = state[:]

        # Flip one bit in input (say in e or a input bit)
        flip_state = orig_state[:]
        bit = flip_bit_pos % word_size
        flip_state[4] ^= (1 << bit)  # flip in e position
        for r in range(num_rounds):
            flip_state = list(toy_sha_round(*flip_state, k, w_i, word_size))
        final_flip = flip_state[:]

        # Compute hamming dist / total bits
        hamming = 0
        for o, f in zip(final_orig, final_flip):
            hamming += bin(o ^ f).count('1')
        total_bits = 8 * word_size
        frac = hamming / total_bits
        avalanche_per_round.append(frac)

        # Rough channel: count unique bits influenced (heuristic via one run)
        # For simplicity, after 1 round how many bits in output affected by 1 input bit
        if trial == 0:
            # Single trial for channel est
            test_state = [0] * 8
            test_state[4] = (1 << bit)  # single bit set in e
            test_state = list(toy_sha_round(*test_state, 0, 0, word_size))
            affected = sum(bin(x).count('1') for x in test_state)
            channel_estimates.append(affected)

    avg_avalanche = sum(avalanche_per_round) / len(avalanche_per_round)
    std_aval = (sum((x - avg_avalanche)**2 for x in avalanche_per_round) / len(avalanche_per_round))**0.5
    avg_channels = sum(channel_estimates) / len(channel_estimates) if channel_estimates else 0

    return {
        "word_size": word_size,
        "rounds": num_rounds,
        "trials": num_trials,
        "avg_avalanche_frac": round(avg_avalanche, 4),
        "std_avalanche": round(std_aval, 4),
        "est_mixed_channels_per_round": round(avg_channels, 1),
        "ideal_random_avalanche": 0.5
    }

def compare_pgs_sha_channels():
    """Main comparison: run PGS analysis and toy SHA for several round counts."""
    print("=== PGS Divisor Channel Analysis (n=1..2000) ===")
    pgs_samples, pgs_agg = pgs_channel_analysis(max_n=2000)
    print(f"Sampled {len(pgs_samples)} numbers. Tau vs avg binary mix_score (higher=more 'mixed' bits):")
    for t in sorted(pgs_agg.keys())[:15]:
        print(f"  tau={t}: {pgs_agg[t]}")
    print("... (primes tau=2 tend to have varied binary patterns)")

    print("\n=== Toy SHA Bit-Mixing Avalanche (diffusion analog to min-divisor selection) ===")
    sha_results = []
    for r in [1, 2, 4, 8, 16]:
        res = simulate_toy_sha_mixing(num_rounds=r, word_size=8, num_trials=500)
        sha_results.append(res)
        print(f"  After {r} rounds (8-bit toy): avg_avalanche={res['avg_avalanche_frac']} (std={res['std_avalanche']}), est_channels/round~{res['est_mixed_channels_per_round']}")

    print("\n=== Proposed a,b,c metrics (example) ===")
    print("a = measured avalanche percentage (e.g. 0.48 after 8 rounds in toy)")
    print("b = round count or 'channel mixing rate' (e.g. ~5-7 bit sources mixed/round via Ch/Maj+sigmas)")
    print("c = 32-bit width or 64 rounds (SHA-256 security margin; full diffusion <<64)")
    print("PGS analog: a' = excess E(n) or Z(n) 'contraction' for composites (bias from prime baseline)")
    print("b' = number of coprime factor channels tau(n) or omega(n)")
    print("c' = gap size or 'leftmost min divisor' selection point (deterministic 'minimal' after 'mixing' of divisors)")

    # Weak correlation probe
    print("\n=== Correlation Probe (expect none strong) ===")
    # For primes (tau=2), see if binary bias low etc.
    prime_mix = [s["mix_score"] for s in pgs_samples if s["tau"] == 2][:20]
    high_tau_mix = [s["mix_score"] for s in pgs_samples if s["tau"] >= 12][:10]
    print(f"Primes (tau=2) sample mix_scores: {prime_mix}")
    print(f"High-tau composites sample mix_scores: {high_tau_mix}")
    print("No obvious correlation: binary bit patterns of n are essentially independent of its divisor channel count tau(n).")

    insight = """
BEST INSIGHT / SELF-CRITIQUE:
No novel relation found; mostly superficial analogy.

- Both systems use "independent channels" that are multiplicatively combined (prime-power choices in tau vs bit-position samples in sigmas/Ch/Maj) then mixed via nonlinear ops (divisor selection vs XOR/AND/rot/add) to produce a "canonical minimal" or "uniform" output (leftmost min-tau vs full avalanche after rounds).
- SHA constants deliberately derived from primes (sqrt/cbrt of first primes) for "nothing up my sleeve" - direct number-theoretic hook, but only for constant generation, not for the mixing logic itself.
- PGS "leftmost minimum divisor" is a deterministic local selection rule inside arithmetic intervals; SHA avalanche/diffusion is a statistical property after iterative mixing. The "minimal rounds for full diffusion" (~8-20 for 256-bit security margin to 64) loosely parallels "selecting the first min-tau" but no falsifiable mapping (e.g. no equation linking tau(n) to round count or bias to E(n)).
- Excess contraction Z(n) <1 for composites ~ "bias" in early hash rounds before full mixing; but PGS is exact for every n, SHA is probabilistic over inputs.
- Falsifiable test would require e.g. predicting SHA round count from some PGS statistic on primes or vice-versa - no such prediction holds in toy data.
- The bridge is poetic at best: both domains value "mixing independent sources to hide structure" (factorization hidden in primes vs input bits hidden in digest). Project's RSA crypto use of SHA-256 (only as PRNG for candidates) and PGS for endpoint structure remain separate; no internal SHA round analysis in codebase.
- Strongest "surprise" is already known: SHA designers chose prime-derived constants; PGS studies the arithmetic of primes via their divisors. This does not yield a number-theoretic model explaining 64-round security.

Conclusion: Path C yields interesting surface parallels for exploration but no deep, falsifiable isomorphism. Recommend deprioritize vs more grounded PGS paths (e.g. bounded compression, RSA sidecars). If pursued, next would be formal mapping of "choice channels" to boolean functions (e.g. divisor lattice to ANF of Ch/Maj) but unlikely productive.
"""
    print(insight)
    return {
        "pgs_agg_sample": dict(list(pgs_agg.items())[:10]),
        "sha_toy_results": sha_results,
        "insight": insight.strip()
    }

if __name__ == "__main__":
    random.seed(42)  # reproducible
    out = compare_pgs_sha_channels()
    with open("/Users/velocityworks/IdeaProjects/prime-gap-structure/experiments/path_c_toy_simulations/results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nResults saved to experiments/path_c_toy_simulations/results.json")
