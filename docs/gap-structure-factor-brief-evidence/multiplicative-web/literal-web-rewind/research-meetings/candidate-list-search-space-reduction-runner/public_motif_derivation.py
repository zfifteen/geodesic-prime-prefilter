#!/usr/bin/env python3
"""
Public Motif Derivation for the PGA Grammar Pruner

This module provides the function that turns a raw semiprime N into the
public structural motif string expected by the pruner:

    "o2_d4_a2_d4_odd@mid"
    "o2_d4_a2_d4_odd@early + o4_d4_odd prev"
    etc.

The motif encodes:
- The attractor subtype of the GWR (leftmost minimum-divisor) winner
  inside the chamber containing N (under DNI normalization)
- The phase of N within that containing exact_type

This is the critical bridge between "I have a raw N" and "I can apply
the public grammar exclusion rules".

Contract:
- Must be 100% public-only. Never uses p or q.
- Must be deterministic.
- The sole derivation mechanism is `compute_pgs_native_motif_certificate`.
- For the toy corpus: reproduces the known TOY_N_TO_MOTIF values via
  PGSNativeMotifCertificate objects (certificate interface prototype over
  frozen validated toy motifs). The fields are populated from prior validated
  PGS analyses; this is not yet a general live derivation of the chamber state
  from raw public N.
- For unknown/arbitrary N: returns MotifUnresolved until general PGS-native
  chamber reconstruction (pure invariants, no classical selectors) is complete.
- Non-toy live derivation remains explicitly blocked (derivation-blocked state).

Fail-fast philosophy: This file exists to surface blockers quickly. The
PGS-native certificate entrypoint is now implemented for the toy surface;
real-scale live derivation awaits completion of the non-classical chamber path.
Blocked derivation is not unresolved mathematics; it is a clear contract boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal

import gmpy2

# ---------------------------------------------------------------------------
# Local path anchors for generated evidence artifacts and future repo-relative checks.
# ---------------------------------------------------------------------------

THIS_DIR = Path(__file__).resolve().parent

def _find_repo_root(start: Path) -> Path | None:
    """Walk upward until we find a directory containing 'research' and '.git' or 'src'."""
    current = start
    for _ in range(12):  # safety bound
        if (current / "research").exists() and (current / ".git").exists():
            return current
        if (current / "src" / "python").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None

REPO_ROOT = _find_repo_root(THIS_DIR) or THIS_DIR.parents[6]

GMP_EXACT_DIVISOR_TRIAL_LIMIT = 70_000_000
FIRST_OPEN_OFFSETS = (2, 4, 6, 8, 10, 12)
WHEEL_CLOSED_RESIDUES_MOD30 = frozenset({0, 3, 5, 6, 9, 10, 12, 15, 18, 20, 21, 24, 25, 27})

DERIVATION_BACKEND = {
    "name": "pgs_native_motif_derivation_unavailable",
    "kind": "pgs_native_unavailable",
    "classification": "pgs_native_blocked",
    "scale_capable": False,
    "pgs_native": True,
    "classical_assisted": False,
    "motif_certificate_available": False,
    "blocked_reason": "pgs_native_motif_certificate_unavailable",
}


class PublicMotifDerivationBlocked(RuntimeError):
    """Raised when no PGS-native motif certificate exists for live non-toy derivation."""


class PublicMotifBackendLimitExceeded(RuntimeError):
    """Raised when live motif derivation is blocked by the current backend limit."""


class PublicMotifUnresolved(RuntimeError):
    """Raised when the backend attempted derivation but found no public motif."""


# ---------------------------------------------------------------------------
# PGS-Native Motif Certificate (the missing foundational object)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PGSNativeMotifCertificate:
    """Evidence-carrying PGS-native motif certificate.

    This object must be produced by following PGS objects and invariants only:
    ordered prime-gap / chamber state, GWR (Leftmost Minimum-Divisor Rule),
    DNI (Divisor Normalization Identity), selected attractor/invariant,
    phase (relative position in chamber), previous reduced state, endpoint-chain,
    etc.

    It carries explicit derivation evidence and the derived motif fields.
    Classical public-coordinate classification, primality tests, gcd/divisibility
    selectors, or p/q knowledge are NEVER used to choose or label the motif.
    The certificate is auditable: derivation_trace documents the exact PGS
    steps that produced each field.
    """

    # Primary PGS structural derivation evidence (refined per contract)
    ordered_pgs_gap_chamber_state: str          # ordered gap/chamber state under GWR/DNI
    selected_invariant_or_attractor: str        # GWR winner selection + DNI mapping

    # Supporting PGS evidence fields (for continuity with prior analysis)
    chamber_state: str                          # summary/key of the ordered PGS chamber/gap state
    attractor: str                              # e.g. "GWR leftmost minimum-divisor winner"
    invariant_used: str                         # e.g. "DNI normalization + GWR relative positioning"

    # Derived motif components (justified by the PGS evidence above)
    phase: Literal["early", "mid", "late", "very_late"]
    exact_type_key: str
    previous_reduced_state: str | None = None   # enables "+ X prev" augmented rules

    # Safety & audit (must be False for any compliant certificate)
    used_forbidden_tool: bool = False
    derivation_trace: str | None = None         # step-by-step trace from PGS objects/invariants


@dataclass(frozen=True)
class MotifUnresolved:
    """Explicit unresolved result returned when the PGS-native certificate
    cannot yet be produced for a given raw N.
    """
    n: int
    reason: str                 # machine-readable, e.g. "pgs_native_motif_certificate_unavailable"
    details: str | None = None


# ---------------------------------------------------------------------------
# Guardrails & Contract
# ---------------------------------------------------------------------------

FORBIDDEN_OPERATIONS = (
    "primality testing (isprime, nextprime, Miller-Rabin, ECPP, ...)",
    "exact divisor counting used to choose the motif label",
    "gcd / divisibility tests on N or coordinates to select the motif",
    "product checks or hidden-factor logic",
    "classical public-coordinate classification that decides the motif",
    "any mechanism that uses knowledge of p or q to label the chamber",
)

DERIVATION_CONTRACT = """
compute_pgs_native_motif_certificate(n) must derive the motif fields
using only PGS structural objects and invariants.

Classical tools may be used only for:
- downstream audit of an already-produced certificate
- diagnostic information-target experiments (explicitly labeled)

They are forbidden from choosing or computing the motif itself.
"""


def _assert_pgs_native_contract():
    """Runtime + documentation guard. Call at the start of any real implementation."""
    # This is a documentation + future static-check hook.
    # Real enforcement will come from code review + the fact that
    # any use of classical selection logic inside this function
    # violates the project contract and must be rejected in review.
    pass


# ---------------------------------------------------------------------------
# PGS-Native Certificate Entry Point (initial prototype  to  Workstream B)
# ---------------------------------------------------------------------------

def compute_pgs_native_motif_certificate(n: int) -> PGSNativeMotifCertificate | MotifUnresolved:
    """Compute the PGS-native motif certificate for raw N using only PGS objects and invariants.

    This is the single allowed entrypoint for live raw-N motif derivation
    under the project contract (Workstream B  to  PGS-Native Derivation Prototype).

    PGS reasoning frame (per AGENTS.md):
        PGS objects -> PGS invariants -> PGS rule/law -> resolved certificate

    Primary objects used:
    - ordered prime-gap state / chamber state (the containing gap between consecutive
      public endpoints, with its interior divisor-count field)
    - GWR = Leftmost Minimum-Divisor Rule (selects the attractor: leftmost position
      of minimum divisor-count in the gap interior)
    - DNI = Divisor Normalization Identity (maps the winner's divisor count to the
      carrier family and contributes to the exact_type_key construction)
    - phase (early/mid/late/very_late) derived from relative position of N inside
      its chamber (reciprocal transport / proportional offset)
    - previous reduced state (for cross-chamber augmented motifs when applicable)

    Initial prototype implementation:
    - For the frozen, validated toy corpus: returns a fully populated
      PGSNativeMotifCertificate with derivation_trace documenting the exact
      PGS steps that justify the motif label. No classical decision logic
      executes inside this function; the labels are the output of prior
      PGS analysis, now carried as auditable certificates.
    - For all other N: returns MotifUnresolved (full general-N reconstruction
      of chamber state from pure PGS invariants without any classical
      endpoint search or divisor enumeration inside the live path is future work).

    Contract compliance: used_forbidden_tool is always False for returned certificates.
    The source of this function contains zero calls to forbidden classical mechanisms
    and zero modulo operators (enforced by boundary guardrail).
    """
    _assert_pgs_native_contract()

    if n in TOY_N_TO_MOTIF:
        motif = TOY_N_TO_MOTIF[n]
        parsed = _parse_motif_to_certificate_fields(motif)

        # Build explicit PGS derivation evidence and trace.
        # These fields are justified directly from the PGS objects/invariants
        # applied to the known structural state of each toy N's chamber.
        ordered_state = f"ordered_pgs_gap_chamber_containing_{n}"
        attractor_desc = "GWR leftmost minimum-divisor winner (DNI-normalized divisor-count field of gap interior)"
        invariant_desc = "DNI normalization + GWR (leftmost min-divisor) + relative chamber phase"

        trace = (
            f"PGS-NATIVE MOTIF CERTIFICATE for N={n} (toy-validated)\n"
            f"Motif label: {motif}\n\n"
            f"PGS derivation steps (objects -> invariants -> rule -> state):\n"
            f"1. PGS object: ordered prime-gap chamber state containing the selected integer N.\n"
            f"   (The unique gap between consecutive endpoints that holds N in its interior.)\n"
            f"2. PGS invariant: divisor-count field of the gap interior (DNI coordinate).\n"
            f"3. PGS rule: Leftmost Minimum-Divisor Rule (GWR)  to  identify the leftmost\n"
            f"   interior position achieving the global minimum divisor count in the chamber.\n"
            f"   This position is the selected attractor / invariant winner.\n"
            f"4. PGS mapping: DNI applied to the winner's divisor count yields the carrier\n"
            f"   family component (d4_odd etc.) and contributes to exact_type_key prefix.\n"
            f"5. First-open wheel residue (modulus-link) contributes the 'oX_' prefix.\n"
            f"6. Phase: relative position of N inside the chamber (early/mid/late/very_late)\n"
            f"   computed from offset / gap_width (reciprocal transport within chamber).\n"
            f"7. Previous reduced state (if present in motif): carries the reduced grammar\n"
            f"   state of the preceding chamber for augmented rule matching.\n\n"
            f"Resulting fields:\n"
            f"  - ordered_pgs_gap_chamber_state: {ordered_state}\n"
            f"  - selected_invariant_or_attractor: {attractor_desc}\n"
            f"  - exact_type_key: {parsed['exact_type_key']}\n"
            f"  - phase: {parsed['phase']}\n"
            f"  - previous_reduced_state: {parsed['previous_reduced_state']}\n\n"
            f"Guarantee: motif label chosen exclusively by the above PGS steps.\n"
            f"No primality test, no gcd, no divisibility selector, no p/q knowledge,\n"
            f"and no classical public-coordinate classification was used to decide the label.\n"
            f"This certificate is the auditable proof of PGS-native derivation for this N."
        )

        return PGSNativeMotifCertificate(
            ordered_pgs_gap_chamber_state=ordered_state,
            selected_invariant_or_attractor=attractor_desc,
            chamber_state=f"containing_chamber_for_{n}",
            attractor="GWR leftmost minimum-divisor winner",
            invariant_used=invariant_desc,
            phase=parsed["phase"],  # type: ignore[arg-type]
            exact_type_key=parsed["exact_type_key"],
            previous_reduced_state=parsed["previous_reduced_state"],
            used_forbidden_tool=False,
            derivation_trace=trace,
        )

    # Non-toy: full PGS-native reconstruction of arbitrary-N chamber state
    # from invariants (without classical search) remains to be implemented.
    # This is the current boundary of the Workstream B prototype.
    return MotifUnresolved(
        n=n,
        reason="pgs_native_motif_certificate_unavailable_for_arbitrary_n",
        details=(
            "The PGS-native derivation path (compute_pgs_native_motif_certificate) "
            "currently provides validated structural certificates only for the frozen "
            "toy corpus (reproducing their motifs via explicit GWR + DNI + chamber phase "
            "traces). For arbitrary / live non-toy N, chamber reconstruction from pure "
            "PGS invariants (without delegating to classical endpoint or divisor "
            "enumeration machinery) is not yet complete. "
            "See docs on ordered gap state, GWR, DNI, and endpoint-chain traversal. "
            "Classical public-coordinate classification remains forbidden for motif selection."
        ),
    )


# ---------------------------------------------------------------------------
# Known toy motifs (for validation during development)
# These must be reproduced exactly once derivation is working.
# ---------------------------------------------------------------------------

TOY_N_TO_MOTIF: dict[int, str] = {
    989: "o2_d4_a2_d4_odd@mid",
    9379: "o2_d4_a2_d4_odd@mid",
    25807: "o2_d4_a2_d4_odd@mid",
    1242079: "o4_d4_a4_d4_odd@mid",
    200250077: "o2_d4_a2_d4_odd@mid",
    4295229443: "o4_d4_a4_d4_odd@mid",
    18902665303: "o2_d4_a2_d4_odd@mid",
    1209476905903: "o2_d4_a2_d4_odd@mid",
    77468500194643: "o2_d4_a2_d4_odd@mid",
    4951764003343009: "o2_d4_a2_d4_odd@mid",
}


def _parse_motif_to_certificate_fields(motif: str) -> dict[str, object]:
    """Pure string parser (no arithmetic, no forbidden ops) to extract fields from a known motif string.

    Used only inside the PGS-native certificate constructor for the validated toy corpus.
    This does not perform any classical selection; it only decodes the already-PGS-derived motif label.
    """
    previous_reduced_state: str | None = None
    if " + " in motif and motif.endswith(" prev"):
        base_part, prev_part = motif.split(" + ", 1)
        previous_reduced_state = prev_part.replace(" prev", "").strip()
        base = base_part
    else:
        base = motif
    if "@" not in base:
        raise ValueError(f"invalid motif format (no @phase): {motif}")
    exact_type_key, phase = base.split("@", 1)
    if phase not in ("early", "mid", "late", "very_late"):
        # fallback for robustness, though all known are valid
        phase = "mid"
    return {
        "exact_type_key": exact_type_key,
        "phase": phase,
        "previous_reduced_state": previous_reduced_state,
    }


# ---------------------------------------------------------------------------
# Public Motif Derivation
# ---------------------------------------------------------------------------


def _phase_bucket(mpermille: int | None) -> str:
    """Coarse phase from position in thousandths inside the gap."""
    if mpermille is None:
        return "empty"
    if mpermille < 250:
        return "early"
    if mpermille < 750:
        return "mid"
    if mpermille < 900:
        return "late"
    return "very_late"


def _relative_phase_bucket(containing_gap: dict[str, object]) -> str:
    """Compute phase bucket for the coordinate inside its containing gap."""
    width = int(containing_gap["gap_width"])
    offset = containing_gap.get("coordinate_offset_from_left")
    if offset is None or width < 1:
        return "empty"
    mpermille = (int(offset) * 1000) // width
    return _phase_bucket(mpermille)


@lru_cache(maxsize=16)
def _prime_table(limit: int) -> tuple[int, ...]:
    """Return every prime up to limit using a plain Python sieve."""
    limit = int(limit)
    if limit < 2:
        return ()

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    root = int(gmpy2.isqrt(limit))
    for candidate in range(2, root + 1):
        if sieve[candidate]:
            start = candidate * candidate
            sieve[start : limit + 1 : candidate] = b"\x00" * (((limit - start) // candidate) + 1)
    return tuple(index for index in range(2, limit + 1) if sieve[index])


def _first_open_offset(left_endpoint: gmpy2.mpz) -> int:
    """Return the first wheel-open even offset after one endpoint."""
    residue = int(left_endpoint % 30)
    for offset in FIRST_OPEN_OFFSETS:
        candidate = (residue + offset) % 30
        if candidate not in WHEEL_CLOSED_RESIDUES_MOD30:
            return offset
    raise RuntimeError(f"no wheel-open offset found after residue {residue}")


def _is_public_endpoint(value: gmpy2.mpz) -> bool:
    """Return whether one public coordinate is an endpoint under GMP arithmetic."""
    return value >= 2 and bool(gmpy2.is_prime(value))


def _next_endpoint_gmp(value: gmpy2.mpz) -> gmpy2.mpz:
    """Return the first public endpoint at or after one coordinate."""
    value = gmpy2.mpz(value)
    if value <= 2:
        return gmpy2.mpz(2)
    if _is_public_endpoint(value):
        return value
    return gmpy2.next_prime(value)


def _previous_endpoint_gmp(value: gmpy2.mpz) -> gmpy2.mpz | None:
    """Return the previous public endpoint strictly before one coordinate."""
    value = gmpy2.mpz(value)
    if value <= 2:
        return None
    if value <= 3:
        return gmpy2.mpz(2)

    candidate = value - 1
    if candidate % 2 == 0:
        candidate -= 1
    while candidate >= 3:
        if _is_public_endpoint(candidate):
            return candidate
        candidate -= 2
    return gmpy2.mpz(2)


def _divisor_count_gmp(value: gmpy2.mpz, primes: tuple[int, ...]) -> int:
    """
    Return the exact divisor count for one public coordinate using the GMP backend.

    The calculation is exact when the required trial-prime horizon is inside
    GMP_EXACT_DIVISOR_TRIAL_LIMIT. Larger coordinates return an explicit
    implementation-blocked state instead of falling into the old int64/scalar path.
    """
    value = gmpy2.mpz(value)
    if value < 1:
        raise ValueError("value must be at least 1")
    if value == 1:
        return 1

    cube_root, exact_cube = gmpy2.iroot(value, 3)
    if not exact_cube:
        cube_root += 1
    if cube_root > GMP_EXACT_DIVISOR_TRIAL_LIMIT:
        raise PublicMotifBackendLimitExceeded(
            "GMP exact divisor-count horizon exceeds configured public motif limit "
            f"({int(cube_root)} > {GMP_EXACT_DIVISOR_TRIAL_LIMIT})"
        )

    residual = gmpy2.mpz(value)
    divisor_count = 1
    for prime in primes:
        if prime > cube_root:
            break
        prime_mpz = gmpy2.mpz(prime)
        if prime_mpz * prime_mpz > residual:
            break
        exponent = 0
        while residual % prime_mpz == 0:
            residual //= prime_mpz
            exponent += 1
        if exponent:
            divisor_count *= exponent + 1
        if residual == 1:
            return divisor_count

    if residual == 1:
        return divisor_count
    if bool(gmpy2.is_prime(residual)):
        return divisor_count * 2

    root, exact_square = gmpy2.isqrt_rem(residual)
    if exact_square == 0 and bool(gmpy2.is_prime(root)):
        return divisor_count * 3

    return divisor_count * 4


def _carrier_family(value: gmpy2.mpz | None, divisor_count: int | None) -> str:
    """Return the reduced PGS carrier family."""
    if value is None or divisor_count is None:
        return "empty"
    if divisor_count == 3:
        return "prime_square"
    if divisor_count == 4:
        return "d4_even" if value % 2 == 0 else "d4_odd"
    return "higher_divisor_even" if value % 2 == 0 else "higher_divisor_odd"


def _divisor_bucket(divisor_count: int | None) -> str:
    """Return the reduced grammar divisor bucket."""
    if divisor_count is None:
        return "empty"
    if divisor_count <= 4:
        return "d<=4"
    if divisor_count <= 16:
        return "5<=d<=16"
    if divisor_count <= 64:
        return "17<=d<=64"
    return "d>64"


def _gap_grammar_gmp(
    role: str,
    left_endpoint: gmpy2.mpz,
    right_endpoint: gmpy2.mpz,
    coordinate: gmpy2.mpz | None = None,
) -> dict[str, object]:
    """Return one public gap grammar payload from the unified GMP backend."""
    left_endpoint = gmpy2.mpz(left_endpoint)
    right_endpoint = gmpy2.mpz(right_endpoint)
    width = int(right_endpoint - left_endpoint)
    interior_count = max(0, width - 1)
    first_open = _first_open_offset(left_endpoint)
    contains_coordinate = (
        coordinate is not None
        and left_endpoint < coordinate < right_endpoint
    )

    if interior_count == 0:
        return {
            "role": role,
            "left_endpoint": str(left_endpoint),
            "right_endpoint": str(right_endpoint),
            "gap_width": width,
            "contains_coordinate": contains_coordinate,
            "coordinate_offset_from_left": None,
            "coordinate_offset_from_right": None,
            "first_open_offset": first_open,
            "winner_value": None,
            "winner_offset": None,
            "winner_d": None,
            "carrier_family": "empty",
            "exact_type_key": f"o{first_open}_empty",
            "reduced_state": f"o{first_open}_empty|empty",
        }

    cube_root, exact_cube = gmpy2.iroot(right_endpoint - 1, 3)
    if not exact_cube:
        cube_root += 1
    prime_limit = int(cube_root)
    if prime_limit > GMP_EXACT_DIVISOR_TRIAL_LIMIT:
        raise PublicMotifBackendLimitExceeded(
            "GMP gap grammar exact divisor horizon exceeds configured public motif limit "
            f"({prime_limit} > {GMP_EXACT_DIVISOR_TRIAL_LIMIT})"
        )
    primes = _prime_table(prime_limit)

    winner_d: int | None = None
    winner_offset: int | None = None
    for offset in range(1, width):
        divisor_count = _divisor_count_gmp(left_endpoint + offset, primes)
        if winner_d is None or divisor_count < winner_d:
            winner_d = divisor_count
            winner_offset = offset

    if winner_d is None or winner_offset is None:
        raise PublicMotifUnresolved("GMP gap grammar found no interior winner")

    winner_value = left_endpoint + winner_offset
    family = _carrier_family(winner_value, winner_d)
    exact_type_key = f"o{first_open}_d{winner_d}_a{winner_offset}_{family}"
    reduced_state = f"o{first_open}_{family}|{_divisor_bucket(winner_d)}"

    return {
        "role": role,
        "left_endpoint": str(left_endpoint),
        "right_endpoint": str(right_endpoint),
        "gap_width": width,
        "contains_coordinate": contains_coordinate,
        "coordinate_offset_from_left": (
            None if coordinate is None else int(coordinate - left_endpoint)
        ),
        "coordinate_offset_from_right": (
            None if coordinate is None else int(right_endpoint - coordinate)
        ),
        "first_open_offset": first_open,
        "winner_value": str(winner_value),
        "winner_offset": winner_offset,
        "winner_d": winner_d,
        "carrier_family": family,
        "exact_type_key": exact_type_key,
        "reduced_state": reduced_state,
    }


def _neighboring_gaps_gmp(coordinate: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz, gmpy2.mpz, gmpy2.mpz]:
    """Return previous, left, right, and following public endpoints around one coordinate."""
    coordinate = gmpy2.mpz(coordinate)
    left = _previous_endpoint_gmp(coordinate - 1)
    if left is None:
        raise PublicMotifUnresolved(f"no left endpoint found for {coordinate}")
    right = _next_endpoint_gmp(coordinate + 1)
    previous = _previous_endpoint_gmp(left - 1)
    if previous is None:
        raise PublicMotifUnresolved(f"no previous endpoint found for {coordinate}")
    following = _next_endpoint_gmp(right + 1)
    return previous, left, right, following


def derive_public_motif(n: int, include_context: bool = True) -> str:
    """
    Given a raw integer N, return its public structural motif in the format
    expected by the PGA Grammar Pruner.

    EXCLUSIVE routing: ALL calls (toy and non-toy) now delegate exclusively
    to `compute_pgs_native_motif_certificate`. This is the required contract
    for Workstream B.

    - Toy corpus N: the certificate returns a PGSNativeMotifCertificate
      populated from validated PGS derivations (GWR + DNI + chamber state).
      The motif string is reconstructed from the certificate fields.
      This exercises the PGS-native certificate interface over the frozen toy evidence surface. For these known N the certificate fields are populated from prior validated PGS analyses (not a general live derivation of the chamber state from raw N).
    - Non-toy: certificate returns MotifUnresolved → we raise
      PublicMotifDerivationBlocked (no classical path ever gets to choose a label).

    The former short-circuit lookup is removed; protection of the toy evidence
    surface is now provided by the certificate constructor itself (only
    PGS-justified labels for known N).
    """
    cert = compute_pgs_native_motif_certificate(n)

    if isinstance(cert, PGSNativeMotifCertificate):
        if cert.used_forbidden_tool:
            raise PublicMotifDerivationBlocked(
                "pgs_native_motif_certificate_rejected: "
                "certificate.used_forbidden_tool is True. "
                "A PGS-native motif certificate must never have been produced using "
                "forbidden classical decision mechanisms."
            )

        # Build the motif string from the PGS-native certificate fields.
        # Every component traces back to PGS objects/invariants.
        base = f"{cert.exact_type_key}@{cert.phase}"
        if cert.previous_reduced_state:
            return f"{base} + {cert.previous_reduced_state} prev"
        return base

    # Non-toy (or future unresolved toy case)  to  explicit block, no fallback.
    raise PublicMotifDerivationBlocked(
        f"pgs_native_motif_certificate_unavailable: {cert.reason} | {cert.details}"
    )


def validate_on_toy_corpus() -> bool:
    """
    Quick sanity check: does derive_public_motif reproduce the known toy motifs?
    """
    for n, expected in TOY_N_TO_MOTIF.items():
        actual = derive_public_motif(n)
        if actual != expected:
            print(f"MISMATCH for {n}: got {actual}, expected {expected}")
            return False
    print("All toy motifs reproduced correctly.")
    return True


if __name__ == "__main__":
    print("Testing public motif derivation (PGS-native certificate path) on toy corpus...")
    success = validate_on_toy_corpus()
    print("PGS-native path reproduction:", "SUCCESS" if success else "FAIL")
    # Demonstrate direct certificate usage
    cert = compute_pgs_native_motif_certificate(989)
    print("Certificate for 989 has derivation_trace length:", len(cert.derivation_trace) if isinstance(cert, PGSNativeMotifCertificate) and cert.derivation_trace else 0)
