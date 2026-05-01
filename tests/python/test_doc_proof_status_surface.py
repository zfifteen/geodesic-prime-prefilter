"""Doc-surface consistency checks for the live proof reference."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEPRECATED_DIR = ROOT / "docs" / "deprecated"


def is_deprecated(path: Path) -> bool:
    """Return whether a path is inside the deprecated document tree."""
    return DEPRECATED_DIR in path.parents or path == DEPRECATED_DIR


def test_root_proof_document_is_the_live_reference():
    """The repository should expose exactly one live proof document."""
    proof = ROOT / "PROOF.md"
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert proof.exists()
    assert "single live proof reference is [PROOF.md](PROOF.md)" in readme
    assert "The single live proof reference is `PROOF.md`" in agents


def test_old_proof_marked_markdown_is_deprecated():
    """Proof/theorem/lemma-marked markdown files should not remain live."""
    offenders: list[str] = []
    markers = ("proof", "theorem", "lemma")

    for path in ROOT.rglob("*.md"):
        if is_deprecated(path):
            continue
        if path == ROOT / "PROOF.md":
            continue
        relative_parts = path.relative_to(ROOT).parts
        if any(any(marker in part.lower() for marker in markers) for part in relative_parts):
            offenders.append(str(path.relative_to(ROOT)))

    assert not offenders, "live proof-marked markdown files found:\n" + "\n".join(offenders)


def test_root_proof_uses_conventional_language():
    """The live proof should avoid project-invented terms and acronyms."""
    text = (ROOT / "PROOF.md").read_text(encoding="utf-8").lower()
    banned_terms = [
        "dni",
        "gwr",
        "pgs",
        "fixed-point locus",
        "shadow seed",
        "endpoint",
        "chamber",
        "bridge",
        "lock",
        "pressure",
    ]

    offenders = [term for term in banned_terms if term in text]

    assert not offenders, "project terms found in PROOF.md: " + ", ".join(offenders)


def test_root_proof_uses_github_safe_math_blocks_only():
    """Avoid inline dollar math because some Markdown previews show delimiters."""
    lines = (ROOT / "PROOF.md").read_text(encoding="utf-8").splitlines()
    offenders: list[str] = []

    for line_number, line in enumerate(lines, start=1):
        if "$" not in line:
            continue
        stripped = line.strip()
        if stripped.startswith("$$") and stripped.endswith("$$"):
            continue
        offenders.append(f"{line_number}: {line}")

    assert not offenders, "non-block dollar math found:\n" + "\n".join(offenders)


def test_root_proof_has_no_hidden_external_proof_dependencies():
    """The live proof should be readable without proof-critical repo artifacts."""
    text = (ROOT / "PROOF.md").read_text(encoding="utf-8")
    banned_phrases = [
        "the repository records this",
        "supporting record",
        "output/",
        "as shown in",
        "see also",
        "http://",
        "https://",
    ]

    offenders = [phrase for phrase in banned_phrases if phrase in text]

    assert not offenders, "external proof dependency language found: " + ", ".join(offenders)


def test_root_proof_preserves_universal_status():
    """The root proof should not downgrade the theorem to a finite check."""
    text = (ROOT / "PROOF.md").read_text(encoding="utf-8")
    required_phrases = [
        "This is a universal statement about every prime gap with a nonempty interior.",
        "The theorem above is universal.",
    ]
    banned_phrases = [
        "The all-scale proof for earlier integers in every prime gap is still open.",
        "finite checked fact",
        "finite checked theorem",
        "What remains open is a short proof",
        "likely true",
        "conjectural",
        "merely empirical",
        "offset 128",
    ]
    banned_patterns = [
        r"all-scale.*open",
    ]

    missing = [phrase for phrase in required_phrases if phrase not in text]
    offenders = [phrase for phrase in banned_phrases if phrase in text]
    pattern_offenders = [pattern for pattern in banned_patterns if re.search(pattern, text, re.IGNORECASE)]

    assert not missing, "universal proof-status wording missing: " + ", ".join(missing)
    assert not offenders, "finite-limited proof wording found: " + ", ".join(offenders)
    assert not pattern_offenders, "finite-limited proof pattern found: " + ", ".join(pattern_offenders)


def test_root_proof_contains_standalone_threshold_classification():
    """The earlier-integer proof should expose the threshold classification."""
    text = (ROOT / "PROOF.md").read_text(encoding="utf-8")
    normalized_text = re.sub(r"\s+", " ", text)
    required_phrases = [
        "T(d,e)",
        "For fixed `d`, `T(d,e)` decreases as `e` increases.",
        "Therefore the adjacent case `e = d + 1` is the largest threshold",
        "Odd Adjacent Branch Lemma",
        "Witness Threshold Lemma",
        "Finite Base Lemma",
        "Classification Lemma",
    ]

    missing = [phrase for phrase in required_phrases if phrase not in normalized_text]

    assert not missing, "stand-alone threshold classification missing: " + ", ".join(missing)
