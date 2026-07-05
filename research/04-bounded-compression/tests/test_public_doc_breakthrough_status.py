"""Public documentation must reflect proved universal bounded compression."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

TIER1 = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "PROOF.md",
    REPO_ROOT / "RESULTS.md",
    REPO_ROOT / "docs" / "current_headline_results.md",
]

STALE_PHRASES = [
    "bounded compression rule is empirical",
    "not an unconditional theorem",
    "all-scale dynamic cutoff theorem remains unresolved",
    "square branch remains unresolved",
]

REQUIRED_IN_PROOF = [
    "Prime-Square Proximity",
    "Universal bounded compression",
    "2026-07-05",
]

REQUIRED_IN_README = [
    "Bounded Compression at the Cramér Scale",
    "Prime-Square Proximity Theorem",
    "2026-07-05",
]


def test_tier1_files_exist():
    for path in TIER1:
        assert path.is_file(), f"missing public doc: {path}"


def test_proof_headline_lists_bounded_compression():
    text = (REPO_ROOT / "PROOF.md").read_text(encoding="utf-8")
    headline = text.split("## Downstream Riemann-Hypothesis Reading", 1)[0]
    assert "Universal bounded compression" in headline
    for phrase in REQUIRED_IN_PROOF:
        assert phrase in text, f"PROOF.md missing: {phrase}"


def test_readme_announces_breakthrough():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in REQUIRED_IN_README:
        assert phrase in text, f"README.md missing: {phrase}"


def test_results_states_proved_not_empirical():
    text = (REPO_ROOT / "RESULTS.md").read_text(encoding="utf-8")
    assert "## Bounded Compression (Proved)" in text
    assert "2026-07-05" in text
    assert "bounded compression rule is empirical" not in text


def test_no_stale_language_in_scoped_public_docs():
    scoped = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "RESULTS.md",
        REPO_ROOT / "RECURSIVE_PRIME_WALK.md",
        REPO_ROOT / "docs" / "current_headline_results.md",
        REPO_ROOT / "research" / "04-bounded-compression" / "README.md",
        REPO_ROOT / "research" / "00-index" / "continuity" / "ACTIVE_TARGET.md",
        REPO_ROOT / "research" / "00-index" / "continuity" / "START_HERE.md",
    ]
    for path in scoped:
        text = path.read_text(encoding="utf-8")
        for phrase in STALE_PHRASES:
            assert phrase not in text, f"{path.name} still contains stale phrase: {phrase!r}"