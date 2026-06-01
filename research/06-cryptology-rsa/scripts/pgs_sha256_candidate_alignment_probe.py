#!/usr/bin/env python3
"""
PGS-SHA256 Candidate Alignment Probe (Path B)

Purpose: Grounded exploration of whether the deterministic candidates produced
by the project's SHA-256 namespace/index/counter stream exhibit measurable
PGS structures (tau(n), GWR leftmost min-divisor selection, DNI Z(n)/E(n))
that differ from uniform random odd integers in the same range. This tests for
a hidden structural relation between the bit-mixing of SHA-256 and the
divisor-count field of PGS, beyond the known engineering use of SHA as a
PRNG for the legacy DNI prefilter.

This script is research scaffolding only. It follows:
- AGENTS.md: PGS-first (start from tau, GWR, DNI objects and invariants;
  classical factor checks only for audit proxy).
- Global code style 4-phase authoring (this file is Phase 1 scaffolding).
- No randomness in selection logic; SHA stream is the sole generator under test.
- Deliverable: real executed artifact with JSON report + human summary.

All reasoning begins from PGS objects:
  - tau(n): number of positive divisors
  - GWR / leftmost minimum-divisor: w = first n in gap with min tau
  - DNI: Z(n) = n^(1 - d(n)/2) at v = e^2/2 ; primes at Z == 1.0 exactly
  - Excess E(n) = (d(n)/2 - 1) * ln(n) ; primes at E == 0

The probe does not claim or use any classical primality or factoring as
inference mechanism for the relation; they are downstream measurement tools.

"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

# Project imports for exact DNI (when available and n small enough)
try:
    ROOT = Path(__file__).resolve().parents[4]
    SOURCE_DIR = ROOT / "src" / "python"
    if str(SOURCE_DIR) not in sys.path:
        sys.path.insert(0, str(SOURCE_DIR))
    from z_band_prime_invariant import (
        FIXED_POINT_V,
        exact_divisor_count,
        exact_z_normalize,
    )
    HAVE_EXACT_INVARIANT = True
except Exception:
    HAVE_EXACT_INVARIANT = False
    FIXED_POINT_V = math.e ** 2 / 2.0

# Fallback to sympy for tau when invariant not usable or for control
try:
    from sympy import divisor_count as sympy_divisor_count
    from sympy import factorint as sympy_factorint
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False
    sympy_divisor_count = None  # type: ignore
    sympy_factorint = None  # type: ignore

DEFAULT_NAMESPACE = "cdl-crypto-prefilter"
DEFAULT_BIT_LENGTH = 24  # small enough for fast exact tau on 1000+ samples
DEFAULT_COUNT = 512
DEFAULT_CONTROL_SEED = 42
SMALL_FACTOR_LIMIT = 1000  # proxy for "gated table" rejection in prefilter

# -------------------------------------------------------------------
# PHASE 1 SCAFFOLDING ONLY - NO IMPLEMENTATION CODE INSIDE FUNCTIONS
# -------------------------------------------------------------------

def deterministic_odd_candidate(
    bit_length: int,
    index: int,
    namespace: str = DEFAULT_NAMESPACE,
) -> int:
    """
    Replicate exactly the deterministic odd candidate generator from
    research/06-cryptology-rsa/legacy-prefilter/scripts/candidate_benchmark.py

    Detailed logic to be implemented in Phase 3:
    - Compute byte_length = (bit_length + 7) // 8
    - Initialize empty bytearray for digest
    - counter = 0
    - While len(digest) < byte_length:
        payload = f"{namespace}:{bit_length}:{index}:{counter}".encode("utf-8")
        digest.extend( hashlib.sha256(payload).digest() )
        counter += 1
    - value = int.from_bytes( digest[:byte_length], "big" )
    - value &= (1 << bit_length) - 1
    - value |= (1 << (bit_length - 1))   # force high bit set (in range)
    - value |= 1                         # force odd
    - Return value

    Acceptance criteria for later test:
    - Returned int is odd (LSB set)
    - bit_length of returned value == bit_length (MSB set)
    - Reproducible: same (namespace, bit_length, index) always yields same int
    - No use of random; pure deterministic SHA stream
    - Must match the production benchmark byte-for-byte on small test vectors

    PGS context: this is the exact "SHA-256 namespace/index stream" used to
    feed the legacy prefilter. The probe will treat the output integers as
    the observable objects on which PGS invariants (tau, Z, E) are measured.
    """
    # SCAFFOLDING: implementation deferred to Phase 3 incremental
    # Detailed control flow, error handling, and edge cases (bit_length < 2,
    # negative index, etc.) described in the benchmark source.
    raise NotImplementedError("Phase 1 scaffolding only")


def deterministic_odd_candidates(
    bit_length: int,
    count: int,
    namespace: str = DEFAULT_NAMESPACE,
) -> List[int]:
    """
    Generate count unique deterministic odd candidates.

    Detailed logic to be implemented in Phase 3:
    - Use a set for dedup
    - index = 0
    - While len(candidates) < count:
        c = deterministic_odd_candidate(bit_length, index, namespace)
        if c not in seen:
            add it
        index += 1
    - Return the list in generation order (or sorted for determinism)

    Acceptance: exactly 'count' unique values, all odd, correct bit length,
    fully reproducible, no duplicates even across long runs.
    """
    raise NotImplementedError("Phase 1 scaffolding only")


def compute_pgs_metrics(n: int) -> Dict[str, Any]:
    """
    Compute exact PGS objects for a single integer n (treated as candidate).

    Detailed logic to be implemented in Phase 3:
    - Prefer project exact_divisor_count + exact_z_normalize from
      z_band_prime_invariant when available and n fits (small bit_length).
    - Fallback to sympy.divisor_count and manual E/Z calculation using math.
    - tau = d(n)
    - E = (tau / 2.0 - 1.0) * math.log(n) if n > 1 else 0.0
    - Z = math.exp(-E)   or equivalently n ** (1.0 - tau / 2.0) clipped
    - Also record omega (distinct prime factors) via factorint if available
    - Record whether n is "prime-like" under PGS (tau == 2 and Z near 1.0)
    - Record a simple "small factor proxy rejection": whether n has any
      factor <= SMALL_FACTOR_LIMIT (audit only, not inference)

    PGS-first contract: tau and the resulting E/Z are the primary observables.
    Classical factor discovery is only a downstream measurement proxy for
    what the legacy prefilter does with gated tables.

    Return dict with keys: n, tau, E, Z, omega, has_small_factor, is_prime_like
    All values must be exact or high-precision floats where required.
    """
    raise NotImplementedError("Phase 1 scaffolding only")


def generate_control_corpus(
    bit_length: int, count: int, seed: int = DEFAULT_CONTROL_SEED
) -> List[int]:
    """
    Generate control corpus of uniform random odd integers in the same
    [2^{bit-1}, 2^bit) range as the SHA stream, for statistical comparison.

    Detailed logic to be implemented in Phase 3:
    - Use random.Random(seed) for reproducibility
    - For each of count:
        draw random int with bit_length bits
        force MSB and LSB set (odd, in range)
        collect
    - No SHA, no structure; pure uniform for baseline.

    Acceptance: statistically uniform in the interval, all odd, correct
    bit length, reproducible from seed, zero overlap with any deterministic
    stream by construction.
    """
    raise NotImplementedError("Phase 1 scaffolding only")


def analyze_alignment(
    sha_candidates: List[int], control_candidates: List[int]
) -> Dict[str, Any]:
    """
    Core analysis: compare PGS metric distributions between SHA stream and
    uniform random control. Look for any non-random structure or alignment
    with DNI invariant or GWR-like patterns.

    Detailed logic to be implemented in Phase 3:
    - For both corpora, compute list of metrics via compute_pgs_metrics
    - Aggregate:
        - tau histogram / Counter
        - mean/median/std of tau, E, Z
        - fraction with Z < 0.5, Z < 0.1, Z < 0.01 (strong contraction)
        - fraction rejected by small-factor proxy
        - for small enough samples, crude "gap" analysis: sort the candidates,
          look at intervals between them, see if leftmost min-tau appears
          more/less often than in control (proxy for GWR visibility)
    - Compute simple effect sizes or ratios (SHA vs control)
    - Propose and compute the Z-mapping triplet for this path:
        a = observable = fraction of candidates with strong DNI contraction
            (Z < 0.1) or small-factor proxy rejection rate
        b = dynamic = rate of change in alignment (e.g. delta mean_E per
            additional counter iteration or per bit_length increase)
        c = binding constraint = SMALL_FACTOR_LIMIT or the bit_length scale
            or the number of SHA counter iterations needed for one candidate
    - effective_intensity = a * (b / c)   (or equivalent interpretable ratio)
    - Interpretation section in output: what low/high values would mean for
      "PGS transparency" of the generator.

    PGS contract: any "alignment" signal must be stated as measured
    correlation or difference in the divisor-count field, not as proof of
    causation or hidden isomorphism. If no statistically clear difference
    from control, the path yields "no hidden structural relation at this scale".

    Output dict with all raw aggregates, histograms, the proposed a/b/c,
    the computed ratio, qualitative interpretation, and a clear
    "signal_detected" boolean based on pre-defined threshold (e.g. >5% relative
    difference in key fractions + consistent direction across runs).
    """
    raise NotImplementedError("Phase 1 scaffolding only")


def run_probe(
    bit_length: int = DEFAULT_BIT_LENGTH,
    count: int = DEFAULT_COUNT,
    namespace: str = DEFAULT_NAMESPACE,
    control_seed: int = DEFAULT_CONTROL_SEED,
    output_dir: Path | None = None,
) -> Dict[str, Any]:
    """
    Orchestrator.

    Detailed logic to be implemented in Phase 3:
    - Print header with PGS objects under test and SHA stream description
    - Generate sha_corpus = deterministic_odd_candidates(...)
    - Generate control_corpus = generate_control_corpus(...)
    - analysis = analyze_alignment(sha_corpus, control_corpus)
    - Assemble full report dict containing:
        - metadata (timestamp, versions, parameters, HAVE_EXACT_INVARIANT, etc.)
        - sha_corpus_stats
        - control_corpus_stats
        - analysis (including a/b/c and ratio)
        - conclusion: "signal_detected" or "no measurable hidden alignment
          beyond uniform random at this scale and count"
        - paths to any saved artifacts
    - If output_dir, write report.json and human-readable summary.txt
    - Return the report dict for further use or printing

    Acceptance: fully deterministic run (same inputs -> identical report),
    all numbers backed by exact PGS computations where possible, clear
    separation of measured result from any interpretation, explicit statement
    of scope (small bit_length only; larger scales would require segmented
    sieve or other for tau).
    """
    raise NotImplementedError("Phase 1 scaffolding only")


def main() -> None:
    """
    CLI entry.

    Detailed logic to be implemented in Phase 3:
    - Parse args for bit_length, count, namespace, seed, output
    - Call run_probe(...)
    - Pretty-print key findings (mean tau/E/Z for SHA vs control,
      signal_detected, the a/b/c values and ratio)
    - Exit 0 on success

    Must remain small, auditable, and tied exactly to the experiment contract.
    """
    raise NotImplementedError("Phase 1 scaffolding only")


if __name__ == "__main__":
    main()
