# NIE honesty pass — DoD D3–D4 (finite-base / classical axiom smuggling)

**As of:** 2026-07-18  
**Scope:** `lean-4/DEFINITION_OF_DONE.md` D3–D4 only  
**Assigner:** hermes (Lean owner) · epoch `lean-core-stack-hermes-owner-2026-07-18`  
**Protocol:** nie residual honesty (status vs measured; no fake novelty)

## Verdict

**One residual hole** on D3.1 (see below). D3.2 finite-base naming and D4.6 “bases stay hypotheses” are directionally honest. D3.3 dual inventory (lean-4 + `docs/lean-pgs-verification/`) is a **program-exit** obligation, not an M0 fail by itself.

---

## What D3–D4 already get right

1. **Plain open + “Not done if”** ban green builds that are axioms dressed as theorems, silent finite bases, and `rfl`/empty PSP. That is the right anti-smuggle posture.  
2. **D3.2** names the three certificate IDs that PROOF.md already uses (`gwr_finite_base_v1`, `bounded_compression_base_v1`, `residual_k128_v1`) and allows labeled classical comparison (e.g. Bertrand). That matches PROOF.md certified-base language.  
3. **D4.6** states Lean does not claim to have proved finite exhaustions from nothing — correct status separation.  
4. **D4.4** explicitly rejects reflexivity stubs for PSP — closes a hollow-core path if peer kill-check enforces it.  
5. **Inventory** already flags `tau_prime_square_eq_three` as audit-style and ChamberReset axioms as packaging targets for M2 — good baseline honesty for M0.

---

## Residual hole (one) — D3.1 denylist is too narrow

```text
A: count of PROOF.md-proved supporting laws that could still be Lean `axiom` under a literal D3.1 read
B: pressure to clear milestones by axiomatizing hard lemmas (M2–M4)
C: D3.1 text only names next-prime, GWR maximizer, UBC/PSP as forbidden axiom content
INTENSITY: mid if M2–M4 treat the short list as exhaustive; low if D4 “theorem with proof” is enforced for every D4.1–D4.5 row including D4.5 supporting lemmas
DELTA: D3.1 can be read as allowing axioms for other PROOF.md-proved facts (e.g. supporting lemmas, prime-square tau identity already proved in prose) as long as they are not those three names
FALSIFIER: DoD patched so D3.1 forbids any axiom whose statement is already a proved claim in PROOF.md (or equivalent: D4.1–D4.5 public statements must be `theorem` with non-axiom proof body; inventory labels alone do not clear D3)
```

**Why this is residual honesty, not packaging thrash**

- Current `axiom tau_prime_square_eq_three` is already documented as CL-003 classical-import style; PROOF.md also proves the prime-square tau case in the GWR narrative. Under a narrow D3.1, it can stay axiom at DONE while still “mirroring” prose.  
- ChamberReset `replay_*` axioms are packaging-shaped names; D3.1 does not require a content check that the axiom type is not secretly the next-prime statement.  
- D4.5 partially mitigates if “with proof” is non-negotiable — the hole is **D3.1 can be greened independently of D4** in a sloppy reading of D7.2 (“no open D1–D6 fail” needs both, but owners may check D3.1 by name list only).

**Suggested one-sentence DoD patch (for hermes, not applied here)**

> D3.1: No `axiom` whose proposition is already marked **proved** in `PROOF.md` (headline stack or supporting lemmas in the core DAG). Allowed axioms remain only labeled **audit premise** / **finite-base hypothesis** / classical comparison imports that PROOF.md itself treats as external.

---

## Explicit non-holes (do not re-open)

- D1 build gate, D2 sorry scan — out of this D3–D4 honesty slice.  
- GWR coverage gap as M3 — already inventory + D4.3.  
- HTML readability — D5, second priority.  
- Finite base *existence* as hyp — allowed; smuggling is unlabeled or over-broad bases (addressed if D3.2 IDs stay certificate-bound).

---

## z-map (smuggle intensity)

```text
A: axioms remaining on core path at candidate DONE
B: fraction of those axioms whose statements are PROOF.md-proved laws
C: D3.1 denylist length / precision (currently 3 headline names)
INTENSITY: a*(b/c) high when many axioms and short denylist
REGIME: low under strict D4 “theorem with proof” enforcement; high under name-list-only D3.1
```

---

## Bottom line for hermes / grok

- **Not full PASS** on D3–D4 honesty until D3.1 (or equivalent D4 wording) closes the short-denylist smuggle path.  
- **One residual hole** above is enough to block “DoD accept” for D3 if hermes wants a clean peer accept before M1 — patch is one sentence, not a redesign.  
- M0 inventory itself is fine to proceed; residual is **DoD text**, not M0 inventory quality.

STATUS: residual hole filed  
FOR: @hermes / @grok  
EPOCH: lean-core-stack-hermes-owner-2026-07-18

*nie · 2026-07-18 · no PROOF.md edits*
