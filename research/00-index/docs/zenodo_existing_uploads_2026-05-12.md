# Zenodo Existing Uploads Inventory

Date: 2026-05-12

This note records the authenticated Zenodo upload inventory used as the local
publication baseline for the formal PGS proof package. The token itself is not
stored here. All entries below are public record metadata returned by the
Zenodo depositions API.

## Strongest Finding

The existing Zenodo pattern is a two-record publication shape:

- the scholarly note is a publication record, usually
  `upload_type=publication` and `publication_type=technicalnote`;
- the GitHub repository release is a software record, `upload_type=software`;
- the publication points to the software with `isSupplementedBy`;
- the software points back to the publication with `isDocumentedBy`.

For the formal PGS proof, the proof should be the publication object and the
repository/release should be supporting material.

## Published Uploads

| Record | Type | DOI | File |
| --- | --- | --- | --- |
| zfifteen/research: gaussian-hill-surface v0.1.0 (Conservative DOI Draft) | software | `10.5281/zenodo.18847306` | `zfifteen/research-v0.1.0.zip` |
| Gaussian Hill Surface / PhaseWall | software | `10.5281/zenodo.18856931` | `zfifteen/gaussian-hill-surface-v0.2.0.zip` |
| Two Computable Invariants for Fourier Approximation of Piecewise-Smooth Signals | publication, technicalnote | `10.5281/zenodo.18865671` | `technical_note.pdf` |
| The Gibbs Invariant: Energy Concentration and Radius Budget Theorems for Fourier Representations of Piecewise-Smooth Signals | software | `10.5281/zenodo.18869128` | `zfifteen/gibbs-invariant-v0.1.1.zip` |
| A Threshold Theory of Layer Domination in Adaptive Linear Approximation | publication, softwaredocumentation | `10.5281/zenodo.19151833` | `layer-domination-threshold-technical-note.pdf` |
| curvature-budget-collapse: Threshold law, diagnostic fingerprint, and adaptive BVP benchmarks for thin stiff layers | software | `10.5281/zenodo.19151950` | `zfifteen/curvature-budget-collapse-v0.1.0.zip` |
| Cross-Figure Vertex Pinning: The Remote Triangle Anchor Effect | publication, technicalnote | `10.5281/zenodo.19154081` | `remote-triangle-anchor-technical-note.pdf` |
| remote-triangle-anchor: Research materials for cross-figure vertex pinning in Euclidean geometry | software | `10.5281/zenodo.19154179` | `zfifteen/remote-triangle-anchor-v1.0.0.zip` |
| noether-early-warning: Atomic benchmark suite for drift as an earlier warning signal than direct symmetry detection | software | `10.5281/zenodo.19184861` | `zfifteen/noether-early-warning-v0.1.0.zip` |
| Early Warning from Drift Before Direct Symmetry Detection | publication, technicalnote | `10.5281/zenodo.19184906` | `noether-early-warning-technical-note.pdf` |

## Local Metadata Examples

The cleanest local examples for the PGS proof package are:

- `/Users/velocityworks/IdeaProjects/remote-triangle-anchor/.zenodo.json`
- `/Users/velocityworks/IdeaProjects/remote-triangle-anchor/technical-note/zenodo-deposit-metadata.json`
- `/Users/velocityworks/IdeaProjects/remote-triangle-anchor/zenodo/README.md`
- `/Users/velocityworks/IdeaProjects/curvature-budget-collapse/.zenodo.json`
- `/Users/velocityworks/IdeaProjects/curvature-budget-collapse/technical-note/zenodo-deposit-metadata.json`
- `/Users/velocityworks/IdeaProjects/curvature-budget-collapse/zenodo/README.md`
- `/Users/velocityworks/IdeaProjects/noether-early-warning/.zenodo.json`
- `/Users/velocityworks/IdeaProjects/noether-early-warning/technical-note/zenodo-deposit-metadata.json`
- `/Users/velocityworks/IdeaProjects/noether-early-warning/zenodo/README.md`

## PGS Package Implication

The PGS formal proof deposit should start with a technical-note style metadata
payload:

- `upload_type`: `publication`
- `publication_type`: `technicalnote`
- `license`: `cc-by-4.0`
- `access_right`: `open`
- supporting identifier: GitHub repository URL
- later supporting identifier: minted software DOI or existing Zenodo software
  record DOI, if a release record is created

The repository/software record should use:

- `upload_type`: `software`
- `license`: `mit` or repository license
- related identifier: proof DOI with `relation=isDocumentedBy` and
  `resource_type=publication-technicalnote`
