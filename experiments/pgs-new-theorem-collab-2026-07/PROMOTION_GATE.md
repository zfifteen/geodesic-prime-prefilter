# Promotion Gate: Checklist for PROOF.md

**Status:** Mandatory human-approved gate before any edits to `PROOF.md`.

This checklist ensures no measured hypothesis or unverified claim is smuggled into the core theorem file.

- [ ] **Part A & C (Finite Cases)**: Are the combinatorial proofs for `g=2, 4` written down entirely using basic arithmetic (divisibility, parity), without assuming any unproved properties of primes?
- [ ] **Part B Isolation**: Is the saturation law (Part B) strictly isolated and clearly marked as **HYPOTHESIS**? It must **not** be included in the theorem statement being promoted.
- [ ] **No Super-Signal**: Does the proof rely on any "global harmonic resonance" or "Super-Signal"? If yes, reject.
- [ ] **UBC/PSP Compatibility**: Does the new claim conflict with the Universal Bound on Composites (UBC) or the Prime Signature Partition (PSP)?
- [ ] **No Classical Primality**: Does the proof attempt to derive prime occurrences from divisor laws? (PGS only goes from gaps -> divisors, not divisors -> prime occurrences).
- [ ] **Human Sign-off**: Has the principal reviewed the exact Markdown diff for `PROOF.md` and explicitly approved the promotion?
