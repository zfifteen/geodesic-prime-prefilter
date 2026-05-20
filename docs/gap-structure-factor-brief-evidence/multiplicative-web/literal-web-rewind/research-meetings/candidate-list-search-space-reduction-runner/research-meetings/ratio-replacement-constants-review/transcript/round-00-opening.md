Agenda: Review the proposed replacement of hard constants in the active thread-triangulation runner with scale-derived ratios, preserving public-state-only inference and the original triangulation mechanism.

User request, verbatim:

> I agree with your determination on which contants should be replaced with ratios. Review your replacement proposals with grok, then show my your final proposal.

Current artifact surface:

- Active runner: `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/thread_triangulation_v01_1_runner.py`
- Original design contract: `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/design_contract.html`
- Explanatory evidence amendment: `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/explanatory_evidence_amendment_contract.html`
- Recent explanatory report: `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/grok_explanatory_findings_report.md`

Boundary:

- Do not edit files in this meeting.
- Do not propose hidden factor use, `gcd`, `N % candidate`, primality APIs, factor APIs, randomness, fallback search, or product closure.
- The next runner must change scale behavior by public ratios only.
- Known `p` and `q` are not available to inference and cannot be used to choose any ratio, cap, window, alphabet, threshold, score, or stop condition.
- Success in later experiments means the public candidate list actually emits `p` or `q` as a candidate distance before audit reads the known factors.

Constants Codex proposed replacing first:

1. `MAX_CANDIDATES = 512`
   - Current role: hard cap on emitted public candidate distances.
   - Problem: creates cap failure when the factor distance is in the public constructed set but outside the fixed retained list.
   - Proposed direction: replace with a candidate-retention ratio relative to original public search space, or a target reduction ratio that scales with `N`.

2. `MIN_DEPTH = 5`
   - Current role: fixed minimum number of incorporated public thread constraints.
   - Problem: fixed depth becomes too strict or too loose as the thread alphabet changes.
   - Proposed direction: replace with a depth ratio, such as `ceil(depth_ratio * active_thread_count)`.

3. `THREAD_SET = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)`
   - Current role: fixed thread alphabet for triangulation.
   - Problem: a fixed alphabet does not scale with `N`; the method needs the same mechanism with a scale-derived amount of public thread evidence.
   - Proposed direction: replace with a public alphabet rule derived from `N.bit_length()` or public radius. The alphabet should remain deterministic and auditable.

Constants Codex proposed preserving:

- Parity base modulus `2` and residue `1`.
- Left/right side alphabet.
- Public radius formula as the baseline square-root-scale window, though an explicit public window multiplier may be introduced as a ratio.
- Compliance token list and forbidden-method audit constants.

Question for Grok:

Review this replacement proposal. Is it methodologically correct for the next runner? Please identify the strongest objection, then give a final ratio-based proposal for `THREAD_SET`, `MIN_DEPTH`, and `MAX_CANDIDATES`. Keep the method public-state-only and preserve triangulation. Propose one concrete deliverable for this meeting, and ask exactly one question at the end.
