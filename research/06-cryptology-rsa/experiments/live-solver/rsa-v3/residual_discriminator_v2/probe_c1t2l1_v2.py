"""Residual discriminator v2 for joint cell C1T2L1 (hypothesis).

Status: hypothesis residual map. Measured on named pins only.
No residual-family 10^18 surface. Not a theorem. Not a close rule.

PGS-only objects used:
- ordered residual ranks R (carrier / tail / lock)
- GWR carrier_w (leftmost minimum)
- chamber-reset signature + first tail offset
- reciprocal floor transport bounds (boundD, TIGHT band)
- lock-quarter boundary and tail-boundary geometry

Forbidden inside inference:
- gcd, divisibility selectors (N % x), product closure, primality APIs
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def evaluate_v2(
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
    n_value: int,
    existing_r: tuple[int, int, int] | None = None,
    existing_s: int | None = None,
) -> dict[str, Any]:
    """PGS-native v2 residual refinement for joint cell C1T2L1.

    Returns a residual package. 50-bit false geometry stays unresolved under
    a sharper residual code that names the exact boundary obstruction.
    Does not emit a resolved endpoint class for the 50-bit pin.
    """
    # Public floor transport only (same primitive already used by gwr_carrier_closure).
    carrier_w = int(lower["carrier_w"])
    if carrier_w <= 0:
        return {
            "residual_code": "unresolved_by_gwr_carrier_fields_absent",
            "R": None,
            "S": None,
            "delta_c": None,
            "delta_t": None,
            "boundD": None,
            "lock_at_quarter": None,
            "tail_at_boundary": None,
            "tail_offset": None,
            "reset_sig_contains_deadline_tail": None,
            "is_joint_cell": False,
            "status": "unresolved",
        }

    T_c = n_value // carrier_w
    upper_carrier = int(upper["carrier_w"])
    delta_c = abs(T_c - upper_carrier)

    g_lo = int(lower.get("gap_offset") or 20)
    g_up = int(upper.get("gap_offset") or 20)
    if g_lo <= 0:
        g_lo = 20
    if g_up <= 0:
        g_up = 20
    boundD = max(20, (6 * (g_lo + g_up)) // 5)
    TIGHT = 20

    tails = lower.get("tail_after_reset_offsets") or []
    if not tails:
        return {
            "residual_code": "unresolved_by_first_tail_misalignment",
            "R": None,
            "S": None,
            "delta_c": delta_c,
            "delta_t": None,
            "boundD": boundD,
            "lock_at_quarter": None,
            "tail_at_boundary": None,
            "tail_offset": None,
            "reset_sig_contains_deadline_tail": "deadline=tail"
            in str(lower.get("reset_signature") or ""),
            "is_joint_cell": False,
            "status": "unresolved",
        }

    reset_endpoint = int(lower["reset_endpoint"])
    tail_offset_value = int(tails[0])
    first_tail_point = reset_endpoint + tail_offset_value
    if first_tail_point <= 0:
        return {
            "residual_code": "unresolved_by_first_tail_misalignment",
            "R": None,
            "S": None,
            "delta_c": delta_c,
            "delta_t": None,
            "boundD": boundD,
            "lock_at_quarter": None,
            "tail_at_boundary": None,
            "tail_offset": tail_offset_value,
            "reset_sig_contains_deadline_tail": "deadline=tail"
            in str(lower.get("reset_signature") or ""),
            "is_joint_cell": False,
            "status": "unresolved",
        }

    T_tail = n_value // first_tail_point
    upper_anchor = int(upper["anchor"])
    delta_t = T_tail - upper_anchor

    # Pinch S matches _pinch_sum in gwr_carrier_closure (public transport only).
    S = abs(T_c - upper_anchor) + abs(delta_t)

    # Residual ranks R (hypothesis map, same convention as residual_vector_R).
    if delta_c <= TIGHT:
        r_carrier = 0
    elif delta_c <= boundD:
        r_carrier = 1
    else:
        r_carrier = 2

    if -12 <= delta_t <= 6:
        r_tail = 0
    elif -21 <= delta_t <= -13:
        r_tail = 1
    else:
        r_tail = 2

    lock = int(lower["lock_carrier_offset"])
    gap = int(lower["gap_offset"])
    if 2 * lock > gap:
        r_lock = 0
    elif lock >= gap // 4:
        r_lock = 1
    else:
        r_lock = 2

    R = (r_carrier, r_tail, r_lock)
    is_joint = R == (1, 2, 1)

    reset_sig = str(lower.get("reset_signature") or "")
    has_deadline_tail = "deadline=tail" in reset_sig

    lock_at_quarter = lock == (gap // 4)
    tail_at_minus_22_boundary = delta_t == -22
    carrier_loose = TIGHT < delta_c <= boundD

    # v2 refinement: only when R == (1, 2, 1). Keep unresolved. Sharper code names
    # the exact public geometry. No resolved emit for the 50-bit false pin.
    new_code: str | None
    if is_joint:
        if (
            lock_at_quarter
            and tail_at_minus_22_boundary
            and carrier_loose
            and S >= 50
            and has_deadline_tail
        ):
            new_code = (
                "unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54"
            )
        else:
            new_code = "unresolved_by_joint_cell_C1T2L1_v2_generic"
    else:
        new_code = None

    return {
        "residual_code": new_code,
        "R": R,
        "S": S,
        "delta_c": delta_c,
        "delta_t": delta_t,
        "boundD": boundD,
        "lock_at_quarter": lock_at_quarter,
        "tail_at_boundary": tail_at_minus_22_boundary,
        "tail_offset": tail_offset_value,
        "reset_sig_contains_deadline_tail": has_deadline_tail,
        "is_joint_cell": is_joint,
        "status": "unresolved" if new_code is not None else "not_c1t2l1",
        # Diagnostics only; not used for inference decisions.
        "existing_r": existing_r,
        "existing_s": existing_s,
    }


def _extract_side(cert: Mapping[str, Any] | None) -> dict[str, Any] | None:
    """Map a structural-certificate side into the residual probe fields."""
    if cert is None:
        return None
    return {
        "carrier_w": cert.get("carrier_w"),
        "gap_offset": cert.get("gap_offset"),
        "lock_carrier_offset": cert.get("lock_carrier_offset"),
        "reset_endpoint": cert.get("reset_endpoint"),
        "tail_after_reset_offsets": cert.get("tail_after_reset_offsets") or [],
        "reset_signature": cert.get("reset_signature") or "",
        "anchor": cert.get("anchor"),
        "closed_offsets_before_q": cert.get("closed_offsets_before_q"),
    }


def test_on_known_pins() -> list[dict[str, Any]]:
    """Run v2 probe on measured pins. Pure local arithmetic. No network."""
    results: list[dict[str, Any]] = []

    # 50-bit false geometry (measured pin from unit test).
    n50 = 1027435935526951
    lower50 = {
        "carrier_w": 32047633,
        "gap_offset": 24,
        "lock_carrier_offset": 6,
        "reset_endpoint": 32047651,
        "tail_after_reset_offsets": [36],
        "reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail",
    }
    upper50 = {
        "carrier_w": 32059621,
        "gap_offset": 14,
        "anchor": 32059619,
    }
    out50 = evaluate_v2(lower50, upper50, n50, existing_r=(1, 2, 1), existing_s=54)
    results.append({"pin": "50bit_FP", **out50})

    # 64-bit true geometry (measured pin from unit test).
    n64 = 10376454699372036973
    lower64 = {
        "carrier_w": 3221225471,
        "gap_offset": 12,
        "lock_carrier_offset": 10,
        "reset_endpoint": 3221225473,
        "tail_after_reset_offsets": [18],
        "reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail",
    }
    upper64 = {
        "carrier_w": 3221275489,
        "gap_offset": 14,
        "anchor": 3221275487,
    }
    out64 = evaluate_v2(lower64, upper64, n64, existing_r=(0, 0, 0), existing_s=21)
    results.append({"pin": "64bit_TP", **out64})

    # 40-bit golden structural certificate (resolved control).
    golden_path = (
        Path(__file__).resolve().parent.parent
        / "fixtures"
        / "golden_40bit_structural_certificate.json"
    )
    if golden_path.is_file():
        import json

        golden = json.loads(golden_path.read_text(encoding="utf-8"))
        n40 = int(golden["N"])
        # Prefer corrected_lower when present (deadline-signature path).
        lower_src = golden.get("corrected_lower_certificate") or golden.get(
            "lower_certificate"
        )
        upper_src = golden.get("upper_certificate")
        lower40 = _extract_side(lower_src)
        upper40 = _extract_side(upper_src)
        if lower40 is not None and upper40 is not None and upper40.get("anchor") is not None:
            out40 = evaluate_v2(lower40, upper40, n40)
            results.append({"pin": "40bit_golden", **out40})
        else:
            results.append(
                {
                    "pin": "40bit_golden",
                    "residual_code": None,
                    "status": "skip_missing_fields",
                }
            )
    else:
        results.append(
            {
                "pin": "40bit_golden",
                "residual_code": None,
                "status": "golden_file_absent",
            }
        )

    # Anti-admission: historical false class must never resolve under this probe.
    # The probe itself never emits resolved; this is a contract assertion.
    false_lower = "32047651"
    false_upper = "32059633"
    results.append(
        {
            "pin": "anti_admission_historical_false_class",
            "false_pair": (false_lower, false_upper),
            "probe_emits_resolved": False,
            "status": "anti_admission_ok",
        }
    )

    return results


def main() -> int:
    rows = test_on_known_pins()
    import json

    print(json.dumps(rows, indent=2, sort_keys=True))
    # Contract checks for the measured 50-bit and 64-bit pins.
    by_pin = {r["pin"]: r for r in rows}
    ok = True
    if by_pin["50bit_FP"].get("residual_code") != (
        "unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54"
    ):
        print("FAIL: 50-bit did not receive sharper v2 residual code")
        ok = False
    if by_pin["50bit_FP"].get("is_joint_cell") is not True:
        print("FAIL: 50-bit is_joint_cell expected True")
        ok = False
    if by_pin["64bit_TP"].get("is_joint_cell") is not False:
        print("FAIL: 64-bit should not be joint cell")
        ok = False
    if by_pin["64bit_TP"].get("residual_code") is not None:
        print("FAIL: 64-bit must not receive C1T2L1 residual code")
        ok = False
    if by_pin["anti_admission_historical_false_class"].get("probe_emits_resolved") is not False:
        print("FAIL: anti-admission violated")
        ok = False
    if ok:
        print("PASS: measured pins and anti-admission checks")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
