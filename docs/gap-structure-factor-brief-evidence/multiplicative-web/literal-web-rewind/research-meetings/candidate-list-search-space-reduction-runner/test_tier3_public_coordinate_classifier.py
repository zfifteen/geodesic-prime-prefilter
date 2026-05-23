#!/usr/bin/env python3
"""Deterministic checks for the live tier-3 public-coordinate classifier."""

from __future__ import annotations

import gmpy2

import public_motif_derivation as pmd


def assert_class(value: int, label: str, family: str, bucket: str) -> None:
    actual = pmd.classify_public_coordinate_tier3(gmpy2.mpz(value))
    expected = {
        "divisor_label": label,
        "carrier_family": family,
        "bucket": bucket,
    }
    for key, expected_value in expected.items():
        if actual[key] != expected_value:
            raise AssertionError(
                f"{value}: expected {key}={expected_value}, got {actual[key]} ({actual})"
            )


def test_basic_classes() -> None:
    assert_class(49, "d3", "prime_square", "d<=4")
    assert_class(26, "d4", "d4_even", "d<=4")
    assert_class(15, "d4", "d4_odd", "d<=4")


def test_bucket_boundaries_and_parity() -> None:
    assert_class(30, "5<=d<=16", "higher_divisor_even", "5<=d<=16")
    assert_class(105, "5<=d<=16", "higher_divisor_odd", "5<=d<=16")
    assert_class(240, "17<=d<=64", "higher_divisor_even", "17<=d<=64")
    assert_class(1679616, "d>64", "higher_divisor_even", "d>64")


def test_indeterminate_maps_to_backend_error() -> None:
    original_small_trial_primes = pmd._small_trial_primes
    pmd._classify_public_coordinate_tier3_cached.cache_clear()
    pmd._small_trial_primes = lambda: ()  # type: ignore[assignment]
    try:
        try:
            pmd.classify_public_coordinate_tier3(gmpy2.mpz(37))
        except pmd.PublicMotifBackendError:
            return
        raise AssertionError("expected PublicMotifBackendError for indeterminate classifier state")
    finally:
        pmd._small_trial_primes = original_small_trial_primes  # type: ignore[assignment]
        pmd._classify_public_coordinate_tier3_cached.cache_clear()


def main() -> None:
    test_basic_classes()
    test_bucket_boundaries_and_parity()
    test_indeterminate_maps_to_backend_error()
    print("tier-3 public-coordinate classifier checks passed")


if __name__ == "__main__":
    main()
