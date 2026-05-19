**Meeting opening recorded.** The full Grok response (PGS-native diagnosis of the collapse, proposed v2 contract deliverable, and single question) is written to:

- [transcript/round-01-grok.md](/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/transcript/round-01-grok.md)

Minutes initialized with current state and the exact proposed deliverable at:

- [minutes.md](/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/minutes.md)

**One-question round is now live for Codex.** The question (which of the two GWR extraction rules to freeze) directly determines the observable and deviation formula that the v2 HTML contract will codify. No other design elements are left open.

All boundaries from the prompt, the prior cross-audit contract, AGENTS.md, and the research-meeting skill are observed: PGS objects only (thread list, divisor-count field, GWR, reciprocal transport, modulus-link closure, structural certificate), no hidden factors or candidate walks in generation, controls mandatory, any selector remains hypothesis until tested and cross-audited, and the deliverable is a single concrete frozen contract artifact.

Ready for the Codex answer that lets the contract be written.
m a single arithmetic progression: t == -N (mod r) for all of them. The reciprocal transport step therefore computes one and only one b = ((-t) * a^{-1} mod r) (mod r) for every a coprime to r. The per-r conflict check (b_set length exactly 1) and the subsequent CRT merge therefore succeed for every a coprime to 210 and fail for every a that shares a factor with 210. The emitted structural certificate C is exactly the 48 residues of the unit group (Z/210Z)^*, each paired with its CRT partner y == N * a^{-1} (mod 210). The divisor-count field recorded on the same thread rows is never consulted by the admissibility test or by the (constant) score; the only invariant exercised is the existence of a single coherent offset class per selected r, i.e., a single global N modulo M. That invariant is satisfied equally by every coprime splitting of N modulo 210.

Consequently the true p % M always survives inside C (it is one of the 48 units), the rotated and deterministic synthetic controls produce the empty certificate (their offset-to-factor pairings are inconsistent), and the rank of the true member inside the true-web certificate is merely its incidental position in the a-ascending sort (observed range 5-44).

This is the precise boundary measured by both cross-audited implementations: the current rule distinguishes coherent local webs from incoherent controls at the level of "full unit-group certificate versus empty", but supplies no further public distinction among the 48 residues once coherence is granted. The result is therefore classified boundary_measurement on the 20-case surface, exactly as recorded in the final cross-audit report.

**Proposed concrete meeting deliverable**

The single deliverable for this meeting is the following frozen artifact:

- File: `docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/residue_certificate_v2_public_selector_contract.html`
- Content: a self-contained HTML design contract (same visual style and section discipline as the prior reciprocal_shadow_correct_experiment_design.html) that defines one public ranking rule to be applied after the v1 consistency certificate has been emitted.

The rule will operate strictly on the public held-out thread list and will use the divisor-count field together with the GWR (leftmost minimum-divisor) rule applied inside that web as the additional observable. Concretely:

- After the existing conflict-check + CRT procedure has produced the admissible list C of 48 residues (M = 210, selected_rs = [2, 3, 5, 7]), the rule extracts the GWR-selected minimal-divisor threads: the held-out rows whose d values equal the global minimum d observed in the held-out list (or the k lowest if ties are broken by offset order).
- For each admissible a (with its CRT y), the rule computes a GWR-deviation score: the sum, over each GWR-selected thread with offset t, of the absolute difference between t and the offset predicted for a minimum-divisor position by the reciprocal transport of a and y through the same modulus-link arithmetic.
- The admissible a with the strictly smallest deviation score is the public nominee for that case.

The HTML will contain:
- the exact extraction rule for the GWR threads and the exact arithmetic of the deviation score;
- the mandatory three-surface control discipline (rotated and deterministic synthetic controls must still produce the empty base certificate; the ranking rule is never run on an empty C);
- the success condition (true p % M receives the unique best score on at least 14 of the 20 cases on the identical surface);
- the falsification conditions (three or more cases in which the true member does not receive the best score, or any control produces a non-empty certificate);
- the 12-item acceptance checklist that an implementation witness must sign;
- the requirement that raw summary.json, certificate.jsonl (now augmented with the new scores and nominee), runtime logs, and summary.md be committed before any claim is published;
- the explicit statement that the proposed ranking rule is a hypothesis until the new surface is executed and cross-audited under the same Part-One / Part-Two lane discipline.

This contract is narrow, implementation-ready, and satisfies every boundary stated in the meeting prompt. It augments the existing modulus-link closure with the divisor-count field and the GWR rule applied to that field, exactly the next PGS object required to move from "coherence detector" to "residue selector" without ever leaving the public thread list.

**One question for Codex**

Which of the two following precise definitions of the "GWR-selected minimal-divisor positions" should the v2 contract adopt?

1. All held-out threads whose divisor_count equals the single global minimum d value observed anywhere in the held-out list for that case (ties broken by smallest absolute offset).
2. The three held-out threads that possess the three smallest divisor_count values (again ties broken by offset order).

The choice fixes the exact observable and the exact deviation formula that the contract will freeze; everything else in the deliverable remains unchanged. Please answer with the number of the preferred definition (or a short clarifying variant if neither matches the intended GWR usage inside the local web).