**Round 3 (closing) recorded.** All six completeness checkpoints are confirmed exactly as stated. The deliverable is complete.

**Final contract outline (frozen):**

- v1 certificate generation (M=210, 48-member unit group via conflict-check + CRT on top-4 thread-degree r's) remains unchanged and cross-audited.
- GWR witness extraction: singular oriented leftmost minimum-divisor row `g` (first in ascending-offset order achieving `d_min`); deterministic support window of at most one qualifying neighbor per side with `d <= d_min + 2`.
- Primary score: `dev_primary(a) = min(d, M - d)` where `d = (t_g * inverse(a, M)) % M`.
- Secondary score: `support_score(a) = sum(dev_supp(a, t_supp) for t_supp in support window)` using the identical `min(...)` expression on each support offset.
- Ranking key (lexicographic): `(dev_primary(a), support_score(a), a)`.
- Nomination rule: true `p % M` must be the **unique** structural winner by the first two keys; a win decided solely by the final `a` reporting tie-break is classified `boundary_measurement`.
- Controls, surface (same 20 cases), artifacts, success/falsification conditions, and 12-item+ checklist are the direct v1 analogues with the new structural-winner target substituted for the old constant-score rank-1 target.
- Status: the ranking rule itself is a **hypothesis** until executed and cross-audited.

**Meeting deliverable declared complete.**  

Codex is authorized to write the self-contained HTML contract immediately at:

`docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/residue_certificate_v2_public_selector_contract.html`

No methodological blocker remains. The single pending arithmetic choice (aggregate) was supplied and accepted; every formula, extraction rule, and success criterion is now unambiguous and parameter-free. The meeting closes after the HTML is emitted.

Transcript and minutes are updated (`round-03-grok.md`, `minutes.md`). The v2 public selector for certificate ranking is ready for implementation and cross-audit under the same disciplined lane structure.
ctly as Definition A.
- **Public ranking layer (new):** for every a in C compute the two-key score exactly as the formulas you supplied and the Round-2 proposal. Lexicographic order `(dev_primary, support_score, a)`. The lowest key is the unique structural nominee (or tied group).
- **Nomination & classification rule:** the true `p % M` must be the unique structural winner (structural keys decide before the final `a` reporting key). If `p % M` wins only via the `a` tie-break, or if it is not the unique lowest structural key, the case is `boundary_measurement`.
- **Controls:** rotated-offset and deterministic-synthetic surfaces run the identical v1 certificate step; ranking is never applied to an empty C. Both controls must remain empty at the certificate layer (as measured).
- **Success condition (first surface):** on the identical 20-case surface (16 original + 4 natural-ratio), at least 14 cases must have the true `p % M` as the unique structural winner by the two-key score.
- **Falsification / boundary conditions:** 3+ cases in which true `p % M` is absent from the structural top or wins only by `a`; any control producing a non-empty certificate; any deviation from the exact public arithmetic after `build_case`.
- **Artifacts:** `summary.json`, `certificate.jsonl` (augmented with dev_primary, support_score, rank, is_structural_winner, classification), runtime logs showing every inverse and multiplication that produced a dev, `summary.md` with per-case table and aggregate success/falsification counts.
- **Acceptance checklist:** 12-item witness list (adapted from v1) plus two new lines confirming (a) the GWR extraction and support logic match Definition A and (b) the deviation arithmetic uses only the listed public values and never materializes a candidate integer.
- **Status of the selector:** the ranking rule and the claim that it supplies a tight public residue nomination inside the certificate are **hypotheses** until the surface is executed and both independent lanes are cross-audited admissible. The v1 coherence detection remains a measured boundary result.

**Meeting Deliverable - Declared Complete**

The negotiated deliverable for this research meeting is now complete.

Codex may immediately write the self-contained HTML contract file at:

`docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/residue_certificate_v2_public_selector_contract.html`

using the outline above, the exact formulas from Round 2, the GWR Definition A you supplied, the sum aggregate, and the success/falsification/acceptance language. No further design rounds, no additional parameters, and no open methodological questions remain inside the stated boundaries.

Once the HTML exists and is reviewed by the witness, a new implementation lane (Part One Grok / Part Two Codex or vice versa) can be opened against the same 20-case surface under the identical cross-audit discipline. All prior invariants (PGS objects only, no hidden factors, no candidate walks, three mandatory controls, construction/audit separation) are preserved.

The meeting is ready to close after the HTML is emitted. The selector itself remains a hypothesis until measured and audited.

**No question**

There is no remaining methodological blocker. The single pending item was the aggregate rule; it has been supplied and accepted. The deliverable is closed.