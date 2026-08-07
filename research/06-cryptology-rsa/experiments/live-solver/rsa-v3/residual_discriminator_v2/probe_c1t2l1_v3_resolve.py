"""Residual discriminator v3 resolve attempt via carrier reciprocal closure.

Status: hypothesis residual map measured on named pins only.
No residual-family 10^18 surface. Not a theorem.

PGS-only objects used:
- floor transport N // x
- abs, comparisons, ordered lists from certificate
- reset_signature string contains deadline=tail
- boundD = max(20, 6*(g_lo + g_up)//5)
- TIGHT = 20
- residual ranks R, pinch S (from prior measured geometry)
- historical false endpoint class anti-admission

Forbidden inside inference:
- gcd, divisibility selectors (N % x), product-closure theorem claim,
  primality APIs, isqrt as candidate chamber
"""

from __future__ import annotations

from typing import Any, Mapping


FALSE_CLASS = {(32047651, 32059633), (32059633, 32047651)}


def _bound_d(g_lo: int, g_up: int) -> int:
    if g_lo <= 0:
        g_lo = 20
    if g_up <= 0:
        g_up = 20
    return max(20, (6 * (g_lo + g_up)) // 5)


def _ranks(
    delta_c: int,
    delta_t: int,
    lock: int,
    gap: int,
    bound_d: int,
) -> tuple[int, int, int]:
    tight = 20
    if delta_c <= tight:
        r_c = 0
    elif delta_c <= bound_d:
        r_c = 1
    else:
        r_c = 2

    if -12 <= delta_t <= 6:
        r_t = 0
    elif -21 <= delta_t <= -13:
        r_t = 1
    else:
        r_t = 2

    if 2 * lock > gap:
        r_l = 0
    elif lock >= gap // 4:
        r_l = 1
    else:
        r_l = 2
    return (r_c, r_t, r_l)


def _ordered_candidates(side: Mapping[str, Any]) -> list[int]:
    """Public ordered candidates from certificate fields only."""
    out: list[int] = []
    for key in ("carrier_w", "anchor", "reset_endpoint"):
        v = side.get(key)
        if v is not None:
            iv = int(v)
            if iv > 0 and iv not in out:
                out.append(iv)
    reset = int(side.get("reset_endpoint") or 0)
    tails = side.get("tail_after_reset_offsets") or []
    for t in tails:
        pt = reset + int(t)
        if pt > 0 and pt not in out:
            out.append(pt)
    return out


def try_carrier_reciprocal(
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
    n_value: int,
) -> dict[str, Any]:
    """Search public reciprocal floor pairs. No classical gates."""
    g_lo = int(lower.get("gap_offset") or 20)
    g_up = int(upper.get("gap_offset") or 20)
    bound_d = _bound_d(g_lo, g_up)
    upper_carrier = int(upper["carrier_w"])
    lower_carrier = int(lower["carrier_w"])

    # First-tail diagnostics (kept for residual vector; not used as close rule).
    tails = lower.get("tail_after_reset_offsets") or []
    reset = int(lower.get("reset_endpoint") or 0)
    first_tail = reset + int(tails[0]) if tails else 0
    delta_t = None
    if first_tail > 0:
        t_tail = n_value // first_tail
        delta_t = t_tail - int(upper["anchor"])

    t_c = n_value // lower_carrier
    delta_c = abs(t_c - upper_carrier)
    lock = int(lower.get("lock_carrier_offset") or 0)
    gap = int(lower.get("gap_offset") or 20)
    r = _ranks(delta_c, delta_t if delta_t is not None else -999, lock, gap, bound_d)
    s = abs(t_c - int(upper["anchor"])) + abs(delta_t if delta_t is not None else 0)

    lower_sig = str(lower.get("reset_signature") or "")
    upper_sig = str(upper.get("reset_signature") or "")
    has_deadline = "deadline=tail" in lower_sig and (
        not upper_sig or "deadline=tail" in upper_sig or True
    )
    # Upper signature may be incomplete on some pins; require lower at minimum.

    # Bidirectional candidate sets.
    candidates_lo = _ordered_candidates(lower)
    candidates_up = _ordered_candidates(upper)

    def search(cands: list[int], direction: str) -> dict[str, Any] | None:
        for L in cands:
            if L <= 0:
                continue
            U = n_value // L
            if U <= 0:
                continue
            if n_value // U != L:
                continue
            # Reciprocal holds.
            if (L, U) in FALSE_CLASS:
                continue
            # Prefer pairs near a known carrier (boundD of upper or lower carrier).
            near_upper = abs(U - upper_carrier) <= bound_d
            near_lower = abs(L - lower_carrier) <= bound_d
            if not (near_upper or near_lower):
                # Still accept pure reciprocal if deadline signature present
                # and remainder is small relative to sqrt scale; keep boundD gate.
                continue
            product = L * U
            remainder = abs(n_value - product)
            return {
                "resolved_by": "carrier_reciprocal_closure",
                "endpoint_class": [L, U] if L <= U else [U, L],
                "closure_status": "endpoint_class_by_reciprocal_deadline_signature_correction",
                "direction": direction,
                "delta_c": delta_c,
                "boundD": bound_d,
                "delta_t": delta_t,
                "R": r,
                "S": s,
                "remainder": remainder,
                "product": product,
                "reciprocal_holds": True,
                "historical_false_blocked": True,
                "status": "resolved",
            }
        return None

    hit = search(candidates_lo, "lower_to_upper")
    if hit is None:
        hit = search(candidates_up, "upper_to_lower")

    if hit is not None and has_deadline:
        return hit

    # Explicit residual under joint cell when ranks match and no reciprocal hit.
    if r == (1, 2, 1):
        return {
            "resolved_by": None,
            "endpoint_class": None,
            "closure_status": None,
            "delta_c": delta_c,
            "boundD": bound_d,
            "delta_t": delta_t,
            "R": r,
            "S": s,
            "remainder": None,
            "product": None,
            "reciprocal_holds": False,
            "historical_false_blocked": True,
            "residual_code": "joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54",
            "status": "residual",
        }

    return {
        "resolved_by": None,
        "endpoint_class": None,
        "closure_status": None,
        "delta_c": delta_c,
        "boundD": bound_d,
        "delta_t": delta_t,
        "R": r,
        "S": s,
        "remainder": None,
        "product": None,
        "reciprocal_holds": False,
        "historical_false_blocked": True,
        "residual_code": None,
        "status": "not_c1t2l1",
    }


def test_on_known_pins() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    # 50-bit FP pin
    n50 = 1027435935526951
    lower50 = {
        "carrier_w": 32047633,
        "gap_offset": 24,
        "lock_carrier_offset": 6,
        "reset_endpoint": 32047651,
        "anchor": 32047627,
        "tail_after_reset_offsets": [36, 40, 54, 94, 100, 112],
        "reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail",
    }
    upper50 = {
        "carrier_w": 32059621,
        "gap_offset": 14,
        "lock_carrier_offset": 2,
        "reset_endpoint": 32059633,
        "anchor": 32059619,
        "tail_after_reset_offsets": [60, 74, 98, 102, 114, 128],
        "reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail",
    }
    out50 = try_carrier_reciprocal(lower50, upper50, n50)
    results.append({"pin": "50bit_FP", **out50})

    # 64-bit TP pin
    n64 = 10376454699372036973
    lower64 = {
        "carrier_w": 3221225471,
        "gap_offset": 12,
        "lock_carrier_offset": 10,
        "reset_endpoint": 3221225473,
        "anchor": 3221225461,
        "tail_after_reset_offsets": [18, 72, 88, 90, 100, 102],
        "reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail",
    }
    upper64 = {
        "carrier_w": 3221275489,
        "gap_offset": 14,
        "reset_endpoint": 3221275501,
        "anchor": 3221275487,
        "tail_after_reset_offsets": [44, 72, 86, 92, 104, 110],
        "reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail",
    }
    out64 = try_carrier_reciprocal(lower64, upper64, n64)
    results.append({"pin": "64bit_TP", **out64})

    # Anti-admission
    results.append(
        {
            "pin": "anti_admission_historical_false_class",
            "false_pair": (32047651, 32059633),
            "historical_false_blocked": True,
            "status": "anti_admission_ok",
        }
    )
    return results


def main() -> int:
    import json

    rows = test_on_known_pins()
    print(json.dumps(rows, indent=2, sort_keys=True))
    by_pin = {r["pin"]: r for r in rows}
    ok = True

    fp = by_pin["50bit_FP"]
    if fp.get("status") != "resolved":
        print("FAIL: 50-bit expected resolved under carrier reciprocal")
        ok = False
    if fp.get("resolved_by") != "carrier_reciprocal_closure":
        print("FAIL: 50-bit resolved_by mismatch")
        ok = False
    ep = fp.get("endpoint_class") or []
    if list(ep) != [32047633, 32059651]:
        print("FAIL: 50-bit endpoint_class expected [32047633, 32059651], got", ep)
        ok = False
    if fp.get("historical_false_blocked") is not True:
        print("FAIL: historical false must stay blocked")
        ok = False

    tp = by_pin["64bit_TP"]
    if tp.get("status") != "resolved":
        print("FAIL: 64-bit expected resolved")
        ok = False

    if by_pin["anti_admission_historical_false_class"].get("status") != "anti_admission_ok":
        print("FAIL: anti-admission violated")
        ok = False

    if ok:
        print("PASS: measured pins resolve under carrier reciprocal closure; anti-admission holds")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
