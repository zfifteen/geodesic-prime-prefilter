# Residue-Certificate Public Selector Research Meeting Minutes

## Meeting Path

`docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/`

## Context And Agenda

The cross-audited V1 residue-certificate experiment produced a clean `boundary_measurement`: the true held-out web emitted a 48-member certificate, while rotated and deterministic synthetic controls emitted empty certificates. The V1 certificate collapsed to the unit group modulo 210 and did not tightly rank `p % M`.

Agenda: review the V1 experiment result and methodology, then produce a stronger public selector for `M` or for certificate ranking that avoids collapsing to the small-prime unit group.

## Participants And Capability Notes

- Codex: facilitator, recorder, methodology reviewer.
- Grok: meeting participant through local Grok CLI.
- Grok CLI was used only through the local command-line session with web search disabled.
- No Agent Bus, xAI API, or browser fallback was used for the meeting.

## Source Evidence

- V1 final report: `../reciprocal-shadow-correct-experiment/final-cross-audit-report.md`
- Part One audit: `../reciprocal-shadow-correct-experiment/part-01-grok-performs-codex-audits/codex_audit.md`
- Part Two audit: `../reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/grok_audit.md`
- V2 contract produced by this meeting: `residue_certificate_v2_public_selector_contract.html`

## Negotiated Deliverable

The negotiated deliverable is complete:

`docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/residue_certificate_v2_public_selector_contract.html`

The contract freezes one public certificate-ranking hypothesis:

- V1 certificate generation remains unchanged.
- GWR witness extraction uses the singular oriented leftmost minimum-divisor row.
- A deterministic support window contains at most one qualifying neighbor on each side.
- Primary score is `dev_primary = min(d, M - d)` where `d = (t_g * inverse(a mod M)) mod M`.
- Secondary score is the plain sum over support-window deviations.
- Structural ranking uses `(dev_primary, support_score)`.
- The final `a` term is a reporting tie-break only and cannot create an accepted structural win.

## Round Log

### Round 0 - Opening

Codex opened the meeting with the user request, the V1 cross-audit result, the relevant file paths, and the research boundaries. Grok was asked to opine first, propose a concrete deliverable, and ask exactly one question.

### Round 1 - Grok Diagnosis

Grok diagnosed the V1 collapse: selected small-prime thread factors made every coprime residue modulo 210 algebraically consistent once offset coherence held. The divisor-count field was not used by V1 scoring, so V1 could distinguish true web coherence from controls but could not distinguish one unit residue from another.

Grok proposed an HTML V2 contract using the divisor-count field and GWR as a ranking layer over the V1 certificate. Grok asked whether GWR-selected rows should mean all global-minimum rows or the three smallest divisor-count rows.

### Round 1 - Codex Answer

Codex rejected both offered definitions as too loose. Codex froze a narrower GWR extraction:

- sort held-out rows by offset ascending;
- find the minimum divisor count `d_min`;
- select the first row with `divisor_count == d_min` as the primary GWR witness;
- use at most one nearby qualifying support row on each side only for tie-breaking.

Codex then asked Grok for the exact public deviation formula.

### Round 2 - Grok Formula

Grok proposed:

```text
d = (t_g * inverse(a mod M)) mod M
dev_primary = min(d, M - d)
```

For support offsets `t_s`, use the same formula and aggregate support deviations as a secondary key. Grok asked whether support aggregation should be a plain sum or a threshold count.

### Round 2 - Codex Answer

Codex chose the plain sum to avoid introducing a new tunable threshold:

```text
support_score = sum(dev_s for each support row)
```

Codex froze the ranking key as `(dev_primary, support_score, a)`, with `a` used only for deterministic reporting. If the true member wins only by `a`, the case is not accepted.

### Round 3 - Grok Closing

Grok confirmed the selector definition and declared the deliverable complete.

### Round 3 - Codex Methodology Check

Codex found a threshold conflict in the proposed success/falsification language: "success at 14 of 20" conflicted with "3 or more failures falsify." Codex proposed a four-class table preserving 14 of 20 as boundary signal and requiring 18 of 20 for accepted measured evidence.

### Round 4 - Grok Threshold Confirmation

Grok confirmed the classification table:

- `accepted_measured_result`: 18-20 of 20 true structural wins, controls empty, no forbidden pattern.
- `boundary_measurement`: 14-17 of 20 true structural wins, controls empty, no forbidden pattern.
- `invalidated_result`: fewer than 14 true structural wins, any forbidden inference pattern, or any comparable non-empty control certificate.
- `unresolved_implementation_failure`: implementation deviates from the frozen contract or fails to emit required artifacts/logs.

## Candidate Insights

- V1 collapsed because it recovered coherence of public `N mod M`, not a selector among the unit residues modulo 210.
- The divisor-count field is the first additional public observable in this line that is not automatically satisfied by every coprime split of `N mod M`.
- The leftmost minimum-divisor witness converts GWR from a broad level set into one public row that every admissible residue must explain.
- The deviation formula stays inside the audited modular arithmetic family: inverse, multiplication, and reduction modulo `M`.

## Falsification Tests

- Fewer than 14 of 20 cases have true `p % M` as the unique structural winner.
- Any control surface emits a comparable non-empty certificate.
- Any implementation uses hidden factors, candidate walks, prime streams, root scans, divisibility gates, product closure, or `gcd(candidate, N)` as inference.
- Any accepted case is decided only by the final `a` reporting tie-break.

## Convergences

- The V2 product should be a ranking rule over the V1 certificate, not a changed numeric factor search.
- The ranking must remain public and deterministic.
- The support aggregate must be parameter-free.
- The strict classification table must prevent premature evidence claims.

## Unresolved Questions

No methodological blocker remains for the V2 contract. The selector itself remains a hypothesis until implemented, executed, and cross-audited.

## Next Research Move

Implement the V2 ranking contract in a fresh cross-audited experiment:

1. One lane performs and the other audits.
2. Roles are flipped with an independent implementation.
3. Both audits check the V2 HTML contract and the inherited V1 forbidden-pattern table.
4. Final evidence is reported only if both lanes agree on classification.
