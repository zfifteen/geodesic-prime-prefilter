"""Pure-Python remainder (residue) utilities for prime-gap interior analysis.

This module supplies the minimal, dependency-free building block for
remainder-vector feature extraction inside ordered prime-gap state.

It is deliberately isolated from all divisor-count, primality, and
generation logic so that remainder features can be studied as an
independent observable attribute of gap interiors.

PGS context:
- An ordered prime gap after prime p consists of interior composites
  n with p < n < q.
- For each such n we may attach its remainder vector relative to a
  fixed ordered list of moduli M (commonly the primorial sequence).
- These vectors are later joined with the divisor-count field d(n),
  the GWR leftmost-minimum flag (is_current_min_d), and the
  distance-to-termination label for statistical measurement only.

Contract for this module (Phase-1 scaffold):
- Single public function: compute_residues.
- Pure stdlib. No numpy, gmpy2, sympy, or external imports.
- Returns immutable tuple so vectors are hashable and comparable.
- All arithmetic uses Python's exact % on nonnegative integers.
- Explicit, early errors for invalid inputs.

This file follows the four-phase authoring procedure and the local
PGS contract: remainder vectors are measurement-layer features.
They do not participate in choosing q or in the GWR selection rule.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

# Versioned default moduli set.
# M_v1 corresponds to the sequence of primorials up to 11# = 2310.
# This matches the initial set in the Remainder Statistics Collection Plan.
# Later extensions must bump the version (M_v2 etc.) and record the
# change in RUN_LOG and aggregate metadata so surfaces remain comparable.
MODULI_PRIMORIAL_V1: Final[list[int]] = [2, 3, 5, 7, 30, 210, 2310]


def compute_residues(
    n: int, moduli: Sequence[int] | None = None
) -> tuple[int, ...]:
    """Return the ordered tuple of remainders (n % m for m in moduli).

    When moduli is None the default M_v1 primorial sequence is used.

    Args:
        n: The integer whose residues are required. Must be nonnegative.
           In PGS gap work this is always an interior composite n > p >= 2.
        moduli: Ordered sequence (list or tuple) of positive integer moduli.
                Typical use is the primorial sequence so that the vector
                encodes the simultaneous avoidance (or alignment) with the
                first k small primes. Must not be empty after default
                resolution.

    Returns:
        Tuple of integers r_i satisfying 0 <= r_i < m_i for each modulus m_i.
        The length equals len(moduli). The tuple is immutable.

    Raises:
        ValueError: if n < 0, or if any modulus m <= 0, or if the
                    (resolved) moduli sequence is empty.
        TypeError: if n is not int or moduli contains non-int after
                   resolution (defensive; Python % would also fail).

    Invariants (must hold for every successful call):
        - len(result) == len(chosen_moduli)
        - for i, m in enumerate(chosen_moduli): 0 <= result[i] < m
        - result is a tuple (not list)
        - the mapping is deterministic and exact (no rounding).

    Failure modes and notes:
        - m == 1 always yields remainder 0 (by definition of %).
        - Very large n is supported because Python integers are arbitrary
          precision; % remains exact.
        - This function performs no primality work, no divisor counting,
          and no search. It is a pure coordinate projection onto the
          chosen modulus axes.
        - In the collector this will be called for every interior n of
          every gap while walking with the existing d(n) routines.

    Phase-1 scaffolding status:
        The body below contains only detailed comments describing the
        intended executable logic. No arithmetic or control flow that
        performs the residue computation exists yet. Implementation
        occurs in a later incremental phase after explicit review.
    """
    # --- Phase-1 scaffolding comments (detailed intended logic) ---
    # 1. Resolve the moduli list:
    #    if moduli is None:
    #        chosen = list(MODULI_PRIMORIAL_V1)   # copy to protect constant
    #    else:
    #        chosen = list(moduli)                # accepts any Sequence[int]
    #
    # 2. Input validation (early, explicit, with informative messages):
    #    - if not isinstance(n, int): raise TypeError(...)
    #    - if n < 0: raise ValueError("n must be nonnegative integer...")
    #    - if not chosen: raise ValueError("moduli sequence must not be empty")
    #    - for m in chosen:
    #          if not isinstance(m, int): raise TypeError(...)
    #          if m <= 0: raise ValueError(f"modulus must be positive, got {m}")
    #
    # 3. Compute the residues exactly:
    #    residues = []
    #    for m in chosen:
    #        r = n % m          # Python's % on ints is exact and nonnegative
    #                           # for n >= 0 and m > 0.
    #        residues.append(r)
    #
    # 4. Return an immutable view:
    #    return tuple(residues)
    #
    # Edge cases to be exercised in tests (documented here for the skeleton):
    # - n == 0, m in [2,3,5] -> (0,0,0)
    # - n == 2310, default moduli -> (0,0,0,0,0,0,0)  (multiple of all)
    # - n == 113 (a known small prime, but treated only as integer here),
    #   mod 30 -> 113 % 30 = 23
    # - modulus 1 appears -> remainder always 0 for that slot
    # - single-element moduli list -> 1-tuple
    # - very large n (e.g. 10**100 + 7) % small m still exact
    #
    # Why tuple not list: allows use as dict key, set member, and
    # guarantees the caller cannot mutate the vector after creation.
    #
    # Why no caching here: remainders are cheap; any memoization belongs
    # in a higher collector if profiling shows need.
    #
    # Separation of concerns: this module knows nothing about gaps,
    # d(n), GWR, or termination distance. Those arrive from the caller
    # (the collector script) that walks the gap state using the
    # project's existing divisor-count routines.
    #
    # After Phase-3 implementation the body will be a direct translation
    # of the comments above. No additional behavior will be introduced.
    # -----------------------------------------------------------

    # --- Begin executable implementation (Phase-3 incremental) ---
    if not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")

    if n < 0:
        raise ValueError(f"n must be nonnegative, got {n}")

    if moduli is None:
        chosen: list[int] = list(MODULI_PRIMORIAL_V1)
    else:
        chosen = list(moduli)

    if not chosen:
        raise ValueError("moduli sequence must not be empty")

    for m in chosen:
        if not isinstance(m, int):
            raise TypeError(
                f"each modulus must be int, got {type(m).__name__} for {m!r}"
            )
        if m <= 0:
            raise ValueError(f"modulus must be positive, got {m}")

    residues: list[int] = []
    for m in chosen:
        # Python % on nonnegative n and positive m yields 0 <= r < m exactly.
        r = n % m
        residues.append(r)

    return tuple(residues)
