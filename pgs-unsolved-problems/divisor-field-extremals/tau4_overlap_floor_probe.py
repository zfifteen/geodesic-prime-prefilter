"""Measure the overlap-floor gate for tau-4 carrier headroom exclusion.

The probe keeps the PGS order fixed: endpoints are tau(n) = 2, the carrier is
the leftmost interior minimum of tau, and sigma/phi fields are measured only
after that carrier is selected.
"""

from __future__ import annotations

import csv
import json
from array import array
from pathlib import Path


LIMIT = 10_000_000
OUT_DIR = Path(__file__).with_name("output")
SUMMARY_PATH = OUT_DIR / "2026-05-23-tau4-overlap-floor-summary.json"
WITNESS_PATH = OUT_DIR / "2026-05-23-tau4-overlap-floor-witnesses.csv"


def zero_array(limit: int) -> array:
    return array("I", [0]) * (limit + 1)


def build_divisor_fields(limit: int) -> tuple[array, array, array, array]:
    tau = zero_array(limit)
    sigma = array("Q", [0]) * (limit + 1)
    phi = array("I", range(limit + 1))
    spf = zero_array(limit)

    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            tau[multiple] += 1
            sigma[multiple] += divisor

    for value in range(2, limit + 1):
        if spf[value] != 0:
            continue
        spf[value] = value
        for multiple in range(value, limit + 1, value):
            phi[multiple] -= phi[multiple] // value
            if spf[multiple] == 0:
                spf[multiple] = value

    return tau, sigma, phi, spf


def factorization(value: int, spf: array) -> list[tuple[int, int]]:
    factors: list[tuple[int, int]] = []
    residual = value
    while residual > 1:
        prime = spf[residual]
        exponent = 0
        while residual % prime == 0:
            residual //= prime
            exponent += 1
        factors.append((prime, exponent))
    return factors


def factor_string(value: int, spf: array) -> str:
    pieces = []
    for prime, exponent in factorization(value, spf):
        if exponent == 1:
            pieces.append(str(prime))
        else:
            pieces.append(f"{prime}^{exponent}")
    return "*".join(pieces)


def signature(value: int, spf: array) -> str:
    exponents = sorted((exponent for _, exponent in factorization(value, spf)), reverse=True)
    if exponents == [4]:
        return "prime_fourth_power"
    if exponents == [3]:
        return "prime_cube"
    if exponents == [2, 1]:
        return "square_times_prime"
    if exponents == [1, 1]:
        return "semiprime"
    if exponents == [1, 1, 1]:
        return "three_distinct_primes"
    return "exponents_" + "_".join(str(exponent) for exponent in exponents)


def frac_lt(left_num: int, left_den: int, right_num: int, right_den: int) -> bool:
    return left_num * right_den < right_num * left_den


def frac_ge(left_num: int, left_den: int, right_num: int, right_den: int) -> bool:
    return left_num * right_den >= right_num * left_den


def add_count(counters: dict[str, int], key: str) -> None:
    counters[key] = counters.get(key, 0) + 1


def overlap_floor(value: int, spf: array) -> tuple[int, int, str]:
    factors = factorization(value, spf)
    if len(factors) == 1:
        prime = factors[0][0]
        return 1, prime * prime, "prime_power_square_floor"
    first_prime, first_exponent = factors[0]
    if first_exponent >= 2:
        return 1, first_prime * first_prime, "repeated_smallest_prime_floor"
    second_prime = factors[1][0]
    return 2, first_prime * second_prime, "distinct_pair_floor"


def make_witness(
    label: str,
    previous_endpoint: int,
    endpoint: int,
    carrier: int,
    competitor: int,
    tau: array,
    sigma: array,
    phi: array,
    spf: array,
    floor_num: int,
    floor_den: int,
    floor_kind: str,
    head_num: int,
    head_den: int,
) -> dict[str, object]:
    return {
        "label": label,
        "p": previous_endpoint,
        "q": endpoint,
        "carrier": carrier,
        "carrier_tau": tau[carrier],
        "carrier_signature": signature(carrier, spf),
        "carrier_factors": factor_string(carrier, spf),
        "competitor": competitor,
        "competitor_tau": tau[competitor],
        "competitor_signature": signature(competitor, spf),
        "competitor_factors": factor_string(competitor, spf),
        "floor_kind": floor_kind,
        "floor_num": floor_num,
        "floor_den": floor_den,
        "headroom_num": head_num,
        "headroom_den": head_den,
        "sigma_carrier_num": sigma[carrier],
        "sigma_carrier_den": carrier,
        "sigma_competitor_num": sigma[competitor],
        "sigma_competitor_den": competitor,
        "phi_carrier_num": phi[carrier],
        "phi_carrier_den": carrier,
        "phi_competitor_num": phi[competitor],
        "phi_competitor_den": competitor,
    }


def analyze() -> tuple[dict[str, object], list[dict[str, object]]]:
    tau, sigma, phi, spf = build_divisor_fields(LIMIT)
    summary: dict[str, object] = {
        "limit": LIMIT,
        "endpoint_rule": "tau(n) == 2",
        "carrier_rule": "leftmost interior minimum tau",
        "secondary_fields": "sigma(n)/n and phi(n)/n measured after carrier selection",
        "tau4_carrier_gaps": 0,
        "tau4_carrier_by_signature": {},
        "later_higher_tau_pairs": 0,
        "deficit_band_pairs": 0,
        "deficit_band_by_carrier_signature": {},
        "deficit_band_by_competitor_signature": {},
        "deficit_band_by_floor_kind": {},
        "overlap_floor_eliminated_pairs": 0,
        "overlap_floor_live_pairs": 0,
        "headroom_violations": 0,
        "closest_floor_ratio": None,
        "first_by_competitor_signature": {},
        "first_by_floor_kind": {},
        "first_overlap_floor_live": None,
        "first_headroom_violation": None,
    }
    witnesses: list[dict[str, object]] = []
    previous_endpoint: int | None = None

    for endpoint in range(2, LIMIT + 1):
        if tau[endpoint] != 2:
            continue
        if previous_endpoint is None:
            previous_endpoint = endpoint
            continue
        if endpoint - previous_endpoint <= 1:
            previous_endpoint = endpoint
            continue

        interior = range(previous_endpoint + 1, endpoint)
        carrier = min(interior, key=lambda value: (tau[value], value))
        if tau[carrier] != 4:
            previous_endpoint = endpoint
            continue

        summary["tau4_carrier_gaps"] = int(summary["tau4_carrier_gaps"]) + 1
        carrier_sig = signature(carrier, spf)
        if carrier_sig not in {"semiprime", "prime_cube"}:
            raise RuntimeError(f"unexpected tau-4 carrier signature at {carrier}: {carrier_sig}")
        carrier_by_sig = summary["tau4_carrier_by_signature"]
        assert isinstance(carrier_by_sig, dict)
        add_count(carrier_by_sig, carrier_sig)

        ew_num = sigma[carrier] - carrier
        dw_num = carrier - phi[carrier]

        for competitor in range(carrier + 1, endpoint):
            if tau[competitor] <= 4:
                continue
            summary["later_higher_tau_pairs"] = int(summary["later_higher_tau_pairs"]) + 1

            dt_num = competitor - phi[competitor]
            if not frac_ge(dt_num, competitor, dw_num, carrier):
                continue
            if not frac_lt(dt_num, competitor, ew_num, carrier):
                continue

            summary["deficit_band_pairs"] = int(summary["deficit_band_pairs"]) + 1
            competitor_sig = signature(competitor, spf)
            by_carrier = summary["deficit_band_by_carrier_signature"]
            by_competitor = summary["deficit_band_by_competitor_signature"]
            by_floor = summary["deficit_band_by_floor_kind"]
            assert isinstance(by_carrier, dict)
            assert isinstance(by_competitor, dict)
            assert isinstance(by_floor, dict)
            add_count(by_carrier, carrier_sig)
            add_count(by_competitor, competitor_sig)

            floor_num, floor_den, floor_kind = overlap_floor(competitor, spf)
            add_count(by_floor, floor_kind)
            head_num = ew_num * competitor - dt_num * carrier
            head_den = carrier * competitor
            if head_num <= 0:
                raise RuntimeError("deficit band produced nonpositive headroom")

            witness = make_witness(
                "deficit_band",
                previous_endpoint,
                endpoint,
                carrier,
                competitor,
                tau,
                sigma,
                phi,
                spf,
                floor_num,
                floor_den,
                floor_kind,
                head_num,
                head_den,
            )

            first_by_competitor = summary["first_by_competitor_signature"]
            first_by_floor = summary["first_by_floor_kind"]
            assert isinstance(first_by_competitor, dict)
            assert isinstance(first_by_floor, dict)
            if competitor_sig not in first_by_competitor:
                first_competitor = dict(witness)
                first_competitor["label"] = "first_competitor_signature"
                first_by_competitor[competitor_sig] = first_competitor
                witnesses.append(first_competitor)
            if floor_kind not in first_by_floor:
                first_floor = dict(witness)
                first_floor["label"] = "first_floor_kind"
                first_by_floor[floor_kind] = first_floor
                witnesses.append(first_floor)

            closest = summary["closest_floor_ratio"]
            ratio_num = floor_num * head_den
            ratio_den = floor_den * head_num
            if (
                closest is None
                or ratio_num * int(closest["floor_to_headroom_den"])
                < int(closest["floor_to_headroom_num"]) * ratio_den
            ):
                closest_witness = dict(witness)
                closest_witness["label"] = "closest_floor_ratio"
                closest_witness["floor_to_headroom_num"] = ratio_num
                closest_witness["floor_to_headroom_den"] = ratio_den
                summary["closest_floor_ratio"] = closest_witness

            floor_eliminates = frac_ge(floor_num, floor_den, head_num, head_den)
            if floor_eliminates:
                summary["overlap_floor_eliminated_pairs"] = int(summary["overlap_floor_eliminated_pairs"]) + 1
            else:
                summary["overlap_floor_live_pairs"] = int(summary["overlap_floor_live_pairs"]) + 1
                if summary["first_overlap_floor_live"] is None:
                    live = dict(witness)
                    live["label"] = "overlap_floor_live"
                    summary["first_overlap_floor_live"] = live
                    witnesses.append(live)

            ht_num = sigma[competitor] + phi[competitor] - 2 * competitor
            if frac_lt(ht_num, competitor, head_num, head_den):
                summary["headroom_violations"] = int(summary["headroom_violations"]) + 1
                if summary["first_headroom_violation"] is None:
                    violation = dict(witness)
                    violation["label"] = "headroom_violation"
                    summary["first_headroom_violation"] = violation
                    witnesses.append(violation)

        previous_endpoint = endpoint

    closest = summary["closest_floor_ratio"]
    if closest is not None:
        witnesses.append(closest)
    return summary, witnesses


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    summary, witnesses = analyze()
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fieldnames = [
        "label",
        "p",
        "q",
        "carrier",
        "carrier_tau",
        "carrier_signature",
        "carrier_factors",
        "competitor",
        "competitor_tau",
        "competitor_signature",
        "competitor_factors",
        "floor_kind",
        "floor_num",
        "floor_den",
        "headroom_num",
        "headroom_den",
        "floor_to_headroom_num",
        "floor_to_headroom_den",
        "sigma_carrier_num",
        "sigma_carrier_den",
        "sigma_competitor_num",
        "sigma_competitor_den",
        "phi_carrier_num",
        "phi_carrier_den",
        "phi_competitor_num",
        "phi_competitor_den",
    ]
    with WITNESS_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(witnesses)


if __name__ == "__main__":
    main()
