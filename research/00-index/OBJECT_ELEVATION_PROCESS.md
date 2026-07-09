OBJECT_ELEVATION_PROCESS.md

Date: 2026-05-27
Status: Draft for review
Purpose: This document defines the required process for elevating empirically powerful mechanisms into named PGS objects. It is a companion to TWO_TRACK_GOVERNANCE.md and FRAME_GOVERNANCE_REVIEW.md.

1. Purpose

The current system has no formal path for mechanisms that first appear in working code (such as the carrier/threat cut) to become named objects with invariants and research obligations. This process creates that path.

The goal is to force consolidation of load-bearing behavior rather than allowing it to remain as unnamed implementation details indefinitely.

2. Trigger Conditions

A mechanism must enter the Object Elevation Process when any of the following occur:

- It demonstrably affects the output of the generator on more than 10% of tested chambers at any scale.
- Multiple independent probes converge on the same pattern and treat it as a reliable signal (examples: carrier_offset, lock_carrier_offset, lower_d_threat_offset).
- The mechanism is responsible for the difference between a high rate of unresolved states and the current near-zero unresolved rate.
- A Pressure Track mismatch report explicitly names the mechanism as a gap in the current object inventory.

The carrier/lock_carrier/lower_d_threat logic inside pgs_chamber_reset_state_certificate meets all four triggers and is the first required candidate.

3. Required Elements for Elevation

When a mechanism enters the process, the following must be produced within 90 days:

- A provisional name for the mechanism (e.g., "Chamber Reset Carrier Cut Rule" or "GWR Threat Closure").
- A clear description of the observable behavior in ordinary language, followed by formal definition.
- A minimal set of provisional invariants (even if unproved).
- A status declaration using one of the categories below.
- A dedicated entry in pgs-unsolved-problems/ with the same status.
- A one-page "elevation card" summarizing the above.

4. Status Categories

The following statuses are permitted:

- Empirically Load-Bearing, No Proof Yet: The mechanism is active in the generator and affects results at scale. It has no theorem.
- Provisional Invariant Established: Clear invariants have been stated; no proof.
- Under Active Proof: Formal work in progress.
- Elevated to Theorem: Moved to PROOF.md (this is the only path into PROOF.md for new objects).
- Invalidated: The mechanism has been shown not to hold under stated conditions.

"Implementation detail" is no longer an acceptable long-term status for any mechanism that meets a trigger condition.

5. Process Steps

Step 1: Identification
Any session or probe author may flag a mechanism. The flag must include concrete evidence (file paths, line numbers, performance impact).

Step 2: Assignment
The mechanism is assigned to a 90-day elevation window. One primary owner is named.

Step 3: Documentation
The owner produces the required elements listed in section 3.

Step 4: Review
A crossing-style review (see TWO_TRACK_GOVERNANCE.md) checks that the elevation does not weaken the generator contract or introduce classical framing into the object definition.

Step 5: Publication
The elevation card and pgs-unsolved-problems/ entry are published. The mechanism is now a first-class (even if provisional) PGS object.

6. Timeline and Enforcement

- 90-day clock starts on the date the mechanism is formally flagged.
- If the required elements are not produced within the window, the mechanism must be documented as "Elevation Overdue" in status-map.md and pgs-unsolved-problems/.
- Repeated overdue elevations trigger a mandatory Frame Stress Test.

7. Safeguards

- Elevation does not grant the mechanism any authority over the generator until it has crossed into PROOF.md status via the normal theorem process.
- The generator contract remains unchanged during elevation.
- Pressure Track material may propose elevations, but only Purity Track review can approve them.

8. First Application

The carrier/lock_carrier/lower_d_threat mechanism (src/python/z_band_prime_predictor/simple_pgs_generator.py:48 to 95 and src/c/high-scale-pgs/include/pgs_high_scale.h:56 to 60) is hereby flagged as the first mechanism subject to this process.

Its 90-day elevation window begins on the adoption date of this document.

9. Relation to Existing Documents

This process does not replace AGENTS.md or the continuity contracts. It adds a required consolidation step for mechanisms that have already proven their importance through code behavior.

Until this document is adopted, no formal obligation exists to elevate such mechanisms.