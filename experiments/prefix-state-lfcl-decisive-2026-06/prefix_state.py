"""Prefix chamber state for L_FCL closure laws (geometry-only track)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from z_band_prime_predictor.simple_pgs_generator import WHEEL_OPEN_RESIDUES_MOD30


def composite_witness(tau: int) -> bool:
    """True when divisor count marks a composite witness."""
    return tau > 2


def wheel_open(p: int, offset: int) -> bool:
    return (p + offset) % 30 in WHEEL_OPEN_RESIDUES_MOD30


def zero_excess(n: int, tau: int) -> float:
    return (tau / 2.0 - 1.0) * math.log(n)


@dataclass
class PrefixSnapshot:
    """State(p, B) at one prefix bound."""

    B: int
    gwr_offset: int | None
    gwr_tau: int | None
    threat_offset: int | None
    partial_budget: float
    admissible: list[int] = field(default_factory=list)


class PrefixStateTracker:
    """Incrementally maintain prefix geometry from τ values only."""

    def __init__(self, p: int, tau: list[int]) -> None:
        self.p = int(p)
        self.tau = tau
        self.gwr_offset: int | None = None
        self.gwr_tau: int | None = None
        self.threat_offset: int | None = None
        self.partial_budget = 0.0
        self._current_B = 0

    def advance_to(self, target_B: int) -> PrefixSnapshot:
        while self._current_B < target_B:
            self._current_B += 1
            self._step(self._current_B)
        return self.snapshot(target_B)

    def snapshot(self, B: int) -> PrefixSnapshot:
        if B != self._current_B:
            raise ValueError(f"tracker at B={self._current_B}, requested B={B}")
        return PrefixSnapshot(
            B=B,
            gwr_offset=self.gwr_offset,
            gwr_tau=self.gwr_tau,
            threat_offset=self.threat_offset,
            partial_budget=self.partial_budget,
            admissible=self._admissible_at(B),
        )

    def _step(self, offset: int) -> None:
        n = self.p + offset
        tau_n = self.tau[n]
        self.partial_budget += zero_excess(n, tau_n)

        if composite_witness(tau_n):
            if self.gwr_tau is None or tau_n < self.gwr_tau:
                self.gwr_offset = offset
                self.gwr_tau = tau_n
                self.threat_offset = None
            if (
                self.gwr_offset is not None
                and offset > self.gwr_offset
                and self.gwr_tau is not None
                and tau_n < self.gwr_tau
                and self.threat_offset is None
            ):
                self.threat_offset = offset

    def _nlsc_ok(self, k: int) -> bool:
        if self.gwr_offset is None or self.gwr_tau is None:
            return False
        for m in range(self.gwr_offset + 1, k):
            tau_m = self.tau[self.p + m]
            if composite_witness(tau_m) and tau_m < self.gwr_tau:
                return False
        return True

    def _admissible_at(self, B: int) -> list[int]:
        if self.gwr_offset is None:
            return []
        result: list[int] = []
        for k in range(1, B + 1):
            if not wheel_open(self.p, k):
                continue
            tau_k = self.tau[self.p + k]
            if not composite_witness(tau_k):
                continue
            if self._nlsc_ok(k):
                result.append(k)
        return result

    def admissible_count(self, B: int) -> int:
        snap = self.advance_to(B)
        return len(snap.admissible)

    def threat_gated_admissible(self, B: int) -> list[int]:
        snap = self.advance_to(B)
        if snap.threat_offset is None:
            return []
        return [k for k in snap.admissible if k >= snap.threat_offset]