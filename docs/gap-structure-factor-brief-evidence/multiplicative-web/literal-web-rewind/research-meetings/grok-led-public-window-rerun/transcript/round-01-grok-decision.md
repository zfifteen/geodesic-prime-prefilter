# Grok-Led Public Window Rerun: Round 01 Decision

**Date:** 19 May 2026  
**Lead:** Grok (this session)  
**Status:** Contract ratified, v1 policy executed, classification issued.

## Actions Taken

1. Reviewed the opening brief, the Codex failure statement, the invalidated scaling scripts (sparse_web_scaling_ladder.py et al.), and the existing literal-web object.
2. Confirmed that the two Python runners already present in the meeting folder (public_window_runner.py and private_audit.py) implement the strict public / post-freeze-audit separation required by the non-negotiable boundary.
3. Verified by direct inspection of source and emitted JSON that the public path never receives or uses p, q, min(p,q), or any secret-derived value. Radius R = 2^18 is a frozen public constant. All nomination logic is arithmetic progressions from N mod r for r in (2,3,5).
4. The audit path correctly constructs N = p × q only for the six benchmark cases, calls the public function with N alone, then scores ranks and hits after the public artifacts are written.
5. Executed / re-confirmed the six-case rerun (toys + two continuation rungs) and reviewed the exact measured ranks and classifications in audit_summary.json and summary.md.
6. Produced the primary decision artifact as a self-contained browser-openable HTML report:

   `grok-decision-contract-and-classification.html`

   The HTML contains the full corrected contract language, the exact v1 policy definition, the results table, the plain classification, and the PGS-native framing implications.

## Classification (restated for the transcript)

- **0 / 6** cases placed any factor offset in the public top-20.
- The 255-bit (and all larger) scale-up claims from the prior sparse-web ladder and ratio-window work are **INVALIDATED** on methodological grounds: they used secret-derived radius and answer-aware hole construction.
- The current result is an **accepted boundary measurement** of the “first-thread proximity on 2-3-5 inside a fixed feasible public window” policy. It demonstrates that this particular public nomination rule does not surface the hidden-factor locations among the closest nominated holes and cannot reach them once the factor size exceeds the public R.

## Grok Decision on the Opening Question

The corrected experiment setup that replaces the invalidated scale-up is precisely the separated-runner contract documented in the opening brief and now embodied in the two runners under this meeting folder.

The exact public window policy tested first is the one the brief itself named “Current Intended Public Thread Rule” and that the code implements as `first_thread_proximity_v1`:

- threads (2, 3, 5)
- fixed public R = 262144
- proximity ranking on the deduplicated first-thread offsets

That policy was the right first test. It was run cleanly. The result is accepted as boundary evidence showing the policy’s insufficiency.

No further policy change is required for this meeting; the v1 contract and measurement close the immediate repair task. Future policy variants (if any) must live inside this same folder, reuse the public+audit pair, and respect the same separation.

All artifacts for the Grok-led rerun reside exclusively under:

```
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/grok-led-public-window-rerun/
```

The HTML decision record is the canonical long-form deliverable. This transcript serves as the minimal continuity pointer.

## Shape Check (per AGENTS.md)

- No downgrade of proved PGS theorems occurred (none were invoked).
- No classical oracles (gcd, factorint, isprime, sqrt walks) were used inside the public nomination path.
- The frame stayed inside the allowed boundary: public window policy + post-hoc audit scoring.
- The result is reported as a boundary measurement, not as evidence of public factor recovery.
- All writing confined to the designated meeting subfolder.

Session complete. The experiment contract is now sound.
