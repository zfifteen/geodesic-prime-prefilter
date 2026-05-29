TWO_TRACK_GOVERNANCE.md

Date: 2026-05-27
Status: Draft for review
Purpose: This document defines the two-track governance system proposed in FRAME_GOVERNANCE_REVIEW.md. It establishes explicit rules for a Purity Track and a Pressure Track.

1. Purpose

The single-track system (AGENTS.md + continuity contracts) has successfully protected the generator contract and prevented classical contamination. It has also created a self-sealing effect that slows the naming and consolidation of new PGS objects.

This document splits governance into two tracks with different rules. The goal is to allow controlled pressure on the current frame without contaminating production artifacts.

2. Definitions

Purity Track:
- The protected track.
- Governed by the full current rules in AGENTS.md, continuity contracts, and existing status-map routing.
- Owns the generator, all production code that emits records, PROOF.md, and all artifacts that feed the public contract.
- No classical methods may be used for inference or selection. Classical methods are permitted only in downstream audit and benchmark roles.

Pressure Track:
- The exploratory track.
- Explicitly permitted to examine whether the current set of PGS objects and invariants is sufficient or complete.
- May use classical comparisons, alternative framings, or any other method that surfaces mismatches.
- All output must be clearly labeled as Pressure Track material.
- Cannot modify the generator, PROOF.md, or any Purity Track artifact without a formal crossing review.

3. Rules for the Purity Track

- All existing AGENTS.md requirements remain in force without exception.
- All reasoning must begin from PGS objects and invariants as defined in AGENTS.md.
- The generator contract is absolute: output must be exactly {"p": p, "q": q} with no source labels, no confidence fields, and no diagnostics in the emitted record.
- Any work that risks introducing classical inference into selection is forbidden on this track.

4. Rules for the Pressure Track

- Work on this track may begin from any framing that helps identify gaps in the current PGS object inventory.
- All documents, scripts, and notes must carry the header "PRESSURE TRACK" and a clear statement that the material is not authorized for Purity Track use.
- Pressure Track output may reference classical results, but only for the purpose of highlighting where current PGS objects fail to provide clean explanations.
- Pressure Track work is encouraged to produce "mismatch reports" that name specific prime-gap phenomena difficult to express using only the current objects (ordered prime-gap state, DNI, GWR, endpoint-chain traversal, chamber reset, reciprocal transport, modulus-link closure, etc.).

5. Crossing Rules (Pressure Track → Purity Track)

No material may move from Pressure Track to Purity Track without meeting all of the following:

- Explicit written proposal describing the proposed change.
- Review by at least two sessions with full context of both AGENTS.md and this document.
- Clear demonstration that the change does not introduce classical inference into the generator selection logic.
- Update to the relevant sections of AGENTS.md or continuity contracts if the change affects core rules.
- Recording of the crossing decision in a dedicated log (to be created: research/00-index/crossing-log.md).

Crossing is intentionally difficult. The default is that Pressure Track material remains quarantined.

6. Labeling Requirements

Every file, note, or output on the Pressure Track must begin with this exact block:

```
PRESSURE TRACK
This material is not part of the Purity Track.
It may not be used to modify the generator, PROOF.md, or any production artifact
without a formal crossing review as defined in TWO_TRACK_GOVERNANCE.md.
```

7. Protections That Remain Absolute

Regardless of track:
- The generator must never emit anything other than clean {"p": p, "q": q} records.
- PROOF.md remains the sole source of theorem status.
- No change to the generator contract can be made through Pressure Track work alone.

8. Decision Authority

- Purity Track decisions remain with the existing continuity and AGENTS.md process.
- Pressure Track has no authority over Purity Track artifacts.
- Crossing decisions require documented agreement from the current primary operator of the repository.

9. Initial Implementation

The first Pressure Track exercise will be the Object Elevation trial on the carrier/lock_carrier/lower_d_threat mechanism currently embedded in pgs_chamber_reset_state_certificate.

This document takes effect upon adoption. Until adoption, the single-track rules in AGENTS.md remain the only governing document.