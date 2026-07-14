"""Status labels and caption claim-language guards."""

from __future__ import annotations

from enum import Enum
from typing import Iterable

STATUS_VALUES = frozenset(
    {
        "theorem",
        "measured",
        "audit",
        "hypothesis",
        "unresolved",
        "invalidated",
        "mixed",
        "editorial",
        "legacy",
    }
)

# Words that require program-level 10^18 evidence when used as claim language.
FORBIDDEN_PROGRAM_CLAIM_WORDS = (
    "validated",
    "validation pass",
    "verified",
    "implementation validated",
    "implementation verified",
    "measured pass",
    "audit pass",
)


class ClaimLanguage(str, Enum):
    WEAK = "weak"  # toy / local / exact regime only
    PROGRAM = "program"  # may use verified/validated; needs 10^18 surface


def normalize_status(value: str) -> str:
    key = (value or "").strip().lower()
    if key not in STATUS_VALUES:
        raise ValueError(f"Unknown status {value!r}; expected one of {sorted(STATUS_VALUES)}")
    return key


def lint_caption_text(
    text: str,
    *,
    claim_language: str = "weak",
    has_10e18_surface: bool = False,
) -> list[str]:
    """Return lint issues for caption / status_detail text."""
    issues: list[str] = []
    lowered = text.lower()
    claim = (claim_language or "weak").strip().lower()
    if claim not in {"weak", "program"}:
        issues.append(f"claim_language must be weak|program, got {claim_language!r}")
        claim = "weak"

    if claim != "program" or not has_10e18_surface:
        for word in FORBIDDEN_PROGRAM_CLAIM_WORDS:
            if word in lowered:
                issues.append(
                    f"Forbidden claim word {word!r} without claim_language=program "
                    "and has_10e18_surface=true"
                )

    # Soft hedges on theorems are a shape warning when caption claims theorem status.
    return issues


def status_chip_class(status: str) -> str:
    return f"status-{normalize_status(status)}"


def iter_status_issues(entries: Iterable[dict]) -> list[str]:
    """Lint entry metadata and caption bodies for claim-language discipline.

    Captions are public gallery prose. They must obey the same forbidden-word
    rules as title / status_detail / regime. Missing captions are an issue for
    catalog entries (every durable demo needs limits text).
    """
    issues: list[str] = []
    for entry in entries:
        eid = entry.get("id", "<missing-id>")
        try:
            normalize_status(str(entry.get("status", "")))
        except ValueError as exc:
            issues.append(f"{eid}: {exc}")
        claim = str(entry.get("claim_language", "weak"))
        has_10e18 = bool(entry.get("has_10e18_surface", False))
        caption = str(entry.get("_caption", "") or "")
        if not caption.strip():
            issues.append(f"{eid}: missing caption.md (required for gallery entries)")
        blob = " ".join(
            [
                str(entry.get("title", "")),
                str(entry.get("status_detail", "")),
                str(entry.get("regime", "")),
                caption,
            ]
        )
        for issue in lint_caption_text(blob, claim_language=claim, has_10e18_surface=has_10e18):
            issues.append(f"{eid}: {issue}")
        if claim == "program" and not has_10e18:
            issues.append(f"{eid}: claim_language=program requires has_10e18_surface=true")
    return issues
