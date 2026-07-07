"""Public documentation must reflect proved universal bounded compression."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

TIER1 = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "PROOF.md",
    REPO_ROOT / "docs" / "RESULTS.md",
    REPO_ROOT / "docs" / "current_headline_results.md",
]

STALE_PHRASES = [
    "bounded compression rule is empirical",
    "not an unconditional theorem",
    "all-scale dynamic cutoff theorem remains unresolved",
    "square branch remains unresolved",
]

SCOPED_PUBLIC_DOCS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "PROOF.md",
    REPO_ROOT / "docs" / "RESULTS.md",
    REPO_ROOT / "docs" / "core" / "RECURSIVE_PRIME_WALK.md",
    REPO_ROOT / "docs" / "PRIME_GAP_GENERATOR.md",
    REPO_ROOT / "docs" / "core" / "LEFTMOST_MINIMUM_DIVISOR_RULE.md",
    REPO_ROOT / "docs" / "current_headline_results.md",
    REPO_ROOT / "research" / "04-bounded-compression" / "README.md",
    REPO_ROOT / "research" / "04-bounded-compression" / "docs" / "square_branch_reduction.md",
    REPO_ROOT / "research" / "04-bounded-compression" / "docs" / "square_branch_blocker_acceptance.md",
    REPO_ROOT / "research" / "04-bounded-compression" / "docs" / "prefix_attainment_theorem_target.md",
    REPO_ROOT / "research" / "04-bounded-compression" / "docs" / "findings" / "README.md",
    REPO_ROOT / "research" / "00-index" / "continuity" / "ACTIVE_TARGET.md",
    REPO_ROOT / "research" / "00-index" / "continuity" / "START_HERE.md",
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


def test_proof_downstream_rh_mentions_bounded_compression():
    text = (REPO_ROOT / "PROOF.md").read_text(encoding="utf-8")
    rh_section = text.split("## Downstream Riemann-Hypothesis Reading", 1)[1]
    rh_section = rh_section.split("## What This Proof Establishes", 1)[0]
    assert "universal bounded compression" in rh_section.lower()
    assert "Prime-Square Proximity" in rh_section


def test_proof_document_status_lists_all_pillars():
    text = (REPO_ROOT / "PROOF.md").read_text(encoding="utf-8")
    doc_status = text.split("## Document Status", 1)[1]
    normalized = " ".join(doc_status.split())
    assert "next-prime theorem" in normalized
    assert "maximizer theorem" in normalized
    assert "universal bounded compression" in normalized.lower()
    assert "Prime-Square Proximity" in normalized


def test_proof_audit_tables_intro_no_remaining_obligation():
    text = (REPO_ROOT / "PROOF.md").read_text(encoding="utf-8")
    audit = text.split("## Audit Tables", 1)[1].split("## Theorem Stack Summary", 1)[0]
    normalized = " ".join(audit.split())
    assert "remaining theorem obligation" not in normalized
    assert "Prime-Square Proximity Theorem closes the square branch" in normalized


def test_readme_announces_breakthrough():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in REQUIRED_IN_README:
        assert phrase in text, f"README.md missing: {phrase}"


def test_results_states_proved_not_empirical():
    text = (REPO_ROOT / "docs" / "RESULTS.md").read_text(encoding="utf-8")
    assert "## Bounded Compression (Proved)" in text
    assert "2026-07-05" in text
    assert "bounded compression rule is empirical" not in text


def test_start_here_bounded_compression_frame_proved():
    text = (REPO_ROOT / "research" / "00-index" / "continuity" / "START_HERE.md").read_text(
        encoding="utf-8"
    )
    section = text.split("## Current Bounded Compression Branch State", 1)[1]
    section = section.split("## Current State-Budget", 1)[0]
    assert "unresolved theorem target" not in section.lower()
    assert "Universal bounded compression is proved" in section or "is PROVED" in section


def test_no_stale_language_in_scoped_public_docs():
    for path in SCOPED_PUBLIC_DOCS:
        assert path.is_file(), f"missing scoped doc: {path}"
        text = path.read_text(encoding="utf-8")
        for phrase in STALE_PHRASES:
            assert phrase not in text, f"{path.relative_to(REPO_ROOT)} still contains: {phrase!r}"