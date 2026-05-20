"""Classify higher-tau reciprocal blockers for tau-4 GWR carriers.

The probe reads prime-gap interiors through exact divisor fields. Endpoints are
recognized by tau(n) = 2. The GWR carrier is the leftmost interior minimum of
tau. Sigma and phi are measured only after the carrier is selected.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


LIMIT = 2_000_000
OUT_DIR = Path(__file__).with_name("output")
SUMMARY_PATH = OUT_DIR / "2026-05-20-higher-tau-reciprocal-blockers-summary.json"
WITNESS_PATH = OUT_DIR / "2026-05-20-higher-tau-reciprocal-blockers-witnesses.csv"


def build_divisor_fields(limit: int) -> tuple[list[int], list[int], list[int], list[int]]:
    tau = [0] * (limit + 1)
    sigma = [0] * (limit + 1)
    phi = list(range(limit + 1))
    spf = [0] * (limit + 1)

    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            tau[multiple] += 1
            sigma[multiple] += divisor

    for value in range(2, limit + 1):
        if spf[value] == 0:
            spf[value] = value
            for multiple in range(value, limit + 1, value):
                phi[multiple] -= phi[multiple] // value
            square = value * value
            if square <= limit:
                for multiple in range(square, limit + 1, value):
                    if spf[multiple] == 0:
                        spf[multiple] = value

    return tau, sigma, phi, spf


def factorization(value: int, spf: list[int]) -> list[tuple[int, int]]:
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


def signature(value: int, spf: list[int]) -> str:
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


def factor_string(value: int, spf: list[int]) -> str:
    pieces = []
    for prime, exponent in factorization(value, spf):
        if exponent == 1:
            pieces.append(str(prime))
        else:
            pieces.append(f"{prime}^{exponent}")
    return "*".join(pieces)


def frac_lt(left_num: int, left_den: int, right_num: int, right_den: int) -> bool:
    return left_num * right_den < right_num * left_den


def update_counter(counters: dict[str, int], key: str) -> None:
    counters[key] = counters.get(key, 0) + 1


def role_better(
    role: str,
    candidate: int,
    carrier: int,
    sigma: list[int],
    phi: list[int],
) -> bool:
    if role == "sigma":
        return frac_lt(sigma[candidate], candidate, sigma[carrier], carrier)
    return frac_lt(candidate - phi[candidate], candidate, carrier - phi[carrier], carrier)


def choose_sigma_min(values: range, sigma: list[int]) -> int:
    best = values.start
    for value in range(values.start + 1, values.stop):
        if frac_lt(sigma[value], value, sigma[best], best):
            best = value
    return best


def choose_phi_deficit_min(values: range, phi: list[int]) -> int:
    best = values.start
    for value in range(values.start + 1, values.stop):
        if frac_lt(value - phi[value], value, best - phi[best], best):
            best = value
    return best


def analyze() -> tuple[dict[str, object], list[dict[str, object]]]:
    tau, sigma, phi, spf = build_divisor_fields(LIMIT)
    summary: dict[str, object] = {
        "limit": LIMIT,
        "endpoint_rule": "tau(n) == 2",
        "carrier_rule": "leftmost interior minimum tau",
        "nonempty_gaps": 0,
        "tau4_carrier_gaps": 0,
        "same_tau4_pair_checks": 0,
        "same_tau4_split_pairs": 0,
        "higher_tau_only_failures": {"sigma": 0, "phi": 0},
        "higher_tau_only_by_tau": {"sigma": {}, "phi": {}},
        "higher_tau_only_by_signature": {"sigma": {}, "phi": {}},
        "all_higher_tau_role_splits": {"phi_only": 0, "sigma_only": 0, "both": 0},
        "first_higher_tau_only": {"sigma": None, "phi": None},
        "first_higher_tau_role_split": {"phi_only": None, "sigma_only": None, "both": None},
    }
    witnesses: list[dict[str, object]] = []
    witness_keys: set[tuple[str, str, str]] = set()
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

        summary["nonempty_gaps"] = int(summary["nonempty_gaps"]) + 1
        interior = range(previous_endpoint + 1, endpoint)
        carrier = min(interior, key=lambda value: (tau[value], value))
        if tau[carrier] != 4:
            previous_endpoint = endpoint
            continue

        summary["tau4_carrier_gaps"] = int(summary["tau4_carrier_gaps"]) + 1
        carrier_sig = signature(carrier, spf)
        if carrier_sig not in {"semiprime", "prime_cube"}:
            raise RuntimeError(f"unexpected tau-4 carrier signature at {carrier}: {carrier_sig}")

        same_tau4_improves = {"sigma": False, "phi": False}
        for other in range(carrier + 1, endpoint):
            if tau[other] != 4:
                continue
            summary["same_tau4_pair_checks"] = int(summary["same_tau4_pair_checks"]) + 1
            sigma_better = role_better("sigma", other, carrier, sigma, phi)
            phi_better = role_better("phi", other, carrier, sigma, phi)
            if sigma_better:
                same_tau4_improves["sigma"] = True
            if phi_better:
                same_tau4_improves["phi"] = True
            if sigma_better != phi_better:
                summary["same_tau4_split_pairs"] = int(summary["same_tau4_split_pairs"]) + 1

        for other in range(carrier + 1, endpoint):
            if tau[other] <= 4:
                continue
            sigma_better = role_better("sigma", other, carrier, sigma, phi)
            phi_better = role_better("phi", other, carrier, sigma, phi)
            if not sigma_better and not phi_better:
                continue
            split_key = "both"
            if phi_better and not sigma_better:
                split_key = "phi_only"
            elif sigma_better and not phi_better:
                split_key = "sigma_only"
            role_splits = summary["all_higher_tau_role_splits"]
            assert isinstance(role_splits, dict)
            role_splits[split_key] = int(role_splits[split_key]) + 1
            first_split = summary["first_higher_tau_role_split"]
            assert isinstance(first_split, dict)
            if first_split[split_key] is None:
                first_split[split_key] = {
                    "p": previous_endpoint,
                    "q": endpoint,
                    "carrier": carrier,
                    "carrier_factors": factor_string(carrier, spf),
                    "carrier_signature": carrier_sig,
                    "competitor": other,
                    "competitor_tau": tau[other],
                    "competitor_factors": factor_string(other, spf),
                    "competitor_signature": signature(other, spf),
                    "sigma_better": sigma_better,
                    "phi_better": phi_better,
                }

        for role in ("sigma", "phi"):
            if same_tau4_improves[role]:
                continue
            if role == "sigma":
                best = choose_sigma_min(interior, sigma)
            else:
                best = choose_phi_deficit_min(interior, phi)
            if not role_better(role, best, carrier, sigma, phi):
                continue
            if tau[best] <= 4:
                continue

            failures = summary["higher_tau_only_failures"]
            by_tau = summary["higher_tau_only_by_tau"]
            by_signature = summary["higher_tau_only_by_signature"]
            assert isinstance(failures, dict)
            assert isinstance(by_tau, dict)
            assert isinstance(by_signature, dict)
            failures[role] = int(failures[role]) + 1
            role_by_tau = by_tau[role]
            role_by_signature = by_signature[role]
            assert isinstance(role_by_tau, dict)
            assert isinstance(role_by_signature, dict)
            update_counter(role_by_tau, str(tau[best]))
            update_counter(role_by_signature, signature(best, spf))

            row = {
                "role": role,
                "p": previous_endpoint,
                "q": endpoint,
                "carrier": carrier,
                "carrier_tau": tau[carrier],
                "carrier_signature": carrier_sig,
                "carrier_factors": factor_string(carrier, spf),
                "competitor": best,
                "competitor_tau": tau[best],
                "competitor_signature": signature(best, spf),
                "competitor_factors": factor_string(best, spf),
                "sigma_carrier_num": sigma[carrier],
                "sigma_carrier_den": carrier,
                "sigma_competitor_num": sigma[best],
                "sigma_competitor_den": best,
                "phi_carrier_num": phi[carrier],
                "phi_carrier_den": carrier,
                "phi_competitor_num": phi[best],
                "phi_competitor_den": best,
                "same_tau4_witness_exists": False,
            }
            first_higher = summary["first_higher_tau_only"]
            assert isinstance(first_higher, dict)
            if first_higher[role] is None:
                first_higher[role] = row
            witness_key = (role, str(tau[best]), signature(best, spf))
            if witness_key not in witness_keys:
                witness_keys.add(witness_key)
                witnesses.append(row)

        previous_endpoint = endpoint

    return summary, witnesses


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    summary, witnesses = analyze()
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with WITNESS_PATH.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "role",
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
            "sigma_carrier_num",
            "sigma_carrier_den",
            "sigma_competitor_num",
            "sigma_competitor_den",
            "phi_carrier_num",
            "phi_carrier_den",
            "phi_competitor_num",
            "phi_competitor_den",
            "same_tau4_witness_exists",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(witnesses)


if __name__ == "__main__":
    main()
