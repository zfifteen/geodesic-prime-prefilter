# Feynman kill-check — Lean 4 Definition of Done

**Date:** 2026-07-18  
**Source:** `lean-4/DEFINITION_OF_DONE.md`  
**Inventory:** `lean-4/SORRY_AXIOM_INVENTORY.md`  
**Ask:** Can a hollow axiom core or `rfl`/empty-shell PSP still score DONE?  
**Protocol:** toy → moving part → kill check. No cosplay. No PROOF.md edits.

---

## 1. TOY

Cold checkout that “looks done”:

- `lake build` + smoke green (D1)  
- `rg sorry` clean on core modules (D2)  
- Core next-prime / PSP / GWR still either (a) **axioms** under friendly names, or (b) **theorems** whose bodies are `exact axiom_…` / trivial witnesses  

Question: does the written DoD **force FAIL**, or can Hermes record D7.1 DONE?

---

## 2. MOVING PART

**Whether “no sorry + green build” is enough to look DONE without a mechanical ban on vacuous statements and unlisted axioms.**

Prose already *names* hollow axiom cores and rfl-shells under “Not done if.” The gear that fails is **enforcement**: D2 only greps `sorry`; D4.4 “not reflexivity stubs” is peer judgment; D3.1 is content judgment without an allowlist gate.

---

## 3. FAILURE (how this kill-check dies)

If after the missing sentences land, a tree with (i) unlisted `axiom` in core, or (ii) PSP witnessed only by `C := r^2 - p` / `le_refl`, cannot pass D7.2 because D1–D6 executable checks fail — then this FAIL is closed. Until then, hollow DONE remains possible under a soft peer skip.

---

## 4. Live counterexamples on disk (not hypothetical)

### H1 — Vacuous PSP shell (exactly the asked hollow)

`ChamberReset.lean` `prime_square_proximity_theorem`:

```lean
∃ C, r^2 - p ≤ C := by
  exact ⟨r^2 - p, Nat.le_refl _⟩
```

For any `p < r^2`, take `C = r^2 - p`. No fixed bound, no PROOF.md constant, no finite-base hyp. **Build can be green; no `sorry`.**

DoD already says “Not done if: PSP is proved by `rfl` / empty shell” and D4.4 “not reflexivity stubs” — so **intent catches H1**. But nothing in D1–D2 **fails the build or inventory** automatically. DONE still depends on peer not rubber-stamping D4.4.

### H2 — Axiom-wrapped “theorems” (hollow core path)

`weak_lfcl_ruleX_forces_next_prime` is a `theorem` whose body only cases on replay and calls three **axioms** (`replay_some_under_hyps`, `replay_cert_eq_hyps`, `replay_cert_demoted`).  
`NextPrime.weak_lfcl_sufficient_bound` re-exports that.

D3.1 forbids axioms that *are* the core theorem by content. Packaging axioms are allowed if labeled. Current packaging is honest **if** inventory marks them audit packaging forever — but a future edit could rename/smuggle the full next-prime law into one axiom and keep a one-line `theorem` with proof. D2 stays green.

### H3 — Coverage gap vs green build

`GWR.lean` is an empty placeholder. D4.3 requires maximizer closed. **DoD correctly fails DONE** until M3 — no hole if D4 is checked. Listed for completeness: hollow is “no theorem,” not “fake theorem.”

---

## 5. Scoreboard vs DoD criteria

| Attack | DoD prose | Mechanical gate today | Verdict |
| --- | --- | --- | --- |
| Hollow axiom core (core law as `axiom`) | D3.1 + “Not done if” axioms named like theorems | No `rg axiom` allowlist; peer only | **FAIL** (soft enforcement) |
| Theorem = `exact axiom_core` | Ambiguous under D3 packaging | No “body may not be pure axiom discharge for D4 rows” | **FAIL** (gap) |
| PSP `rfl` / `le_refl` distance witness | D4.4 + “Not done if” empty shell | No statement-shape check; **live H1** | **FAIL** (prose yes, gate no) |
| `sorry` on core | D2.1 | `rg sorry` | **PASS** |
| Finite bases silent | D3.2–D3.3, D4.6 | Inventory discipline | **PASS** if D3.3 kept |
| Green build, GWR missing | D4.3 | Peer coverage | **PASS** if D4 enforced at D7 |
| Status HTML replaces PROOF.md | D5.3, D6.2 | Process | **PASS** as written |

**Overall DoD kill-check: FAIL** — hollow axiom core and vacuous PSP can still *score* DONE under a green build + zero sorry + weak peer pass. Intent is right; missing executable sentences on D2/D3/D4.

---

## 6. Exact missing sentences (patch DoD)

Add under **D2** (or new D2.3):

> **D2.3** — `rg -n '^\\s*axiom ' lean-4/PGS/*.lean` returns **only** names listed in the current inventory as **audit premise** or **finite-base hypothesis**. Any other axiom → not done.

Add under **D3** (D3.4):

> **D3.4** — A core-stack row (D4.1–D4.5) is **not** closed if its proof is solely `exact <axiom>` / `apply <axiom>` with no further discharge. Such theorems count as **packaging wrappers** until the axiom is removed or reclassified under D3.2 and the row is re-proved.

Add under **D4.4** (replace/strengthen “not reflexivity stubs”):

> **D4.4b** — Bound / proximity statements must match PROOF.md’s **non-vacuous** shape (fixed constant or explicitly named finite-base bound). Witnesses of the form `∃ C, dist ≤ C := ⟨dist, le_refl _⟩` (or `by rfl` on an unconstrained existential) are **empty shells** and fail DoD even if `sorry`-free.

Add under **Not done if** (bullet):

> - Core `theorem` is only a wrapper around an `axiom` that carries the PROOF.md obligation  
> - Existential bound is witnessed by the distance itself (`C := r^2 - p` and kin)

Add under **D7.2** (executable peer checklist):

> Peer kill-check must re-run D2.1 + D2.3 and spot-check D4.4b on PSP/UBC statements before accepting DONE.

---

## 7. STRIPPED EXPLANATION

A green Lean build without `sorry` is cheap if the hard content lives in axioms or in theorems that are logically empty. The DoD already *says* that is not done. It does not yet *force* a machine-visible fail for unlisted axioms or for the classic “exists a bound — take the number itself” shell. H1 is already in the tree. Patch D2.3 / D3.4 / D4.4b before treating M1+ as progress toward program DONE.

---

## 8. NEXT CUT

Hermes (owner): land the three sentences above in `DEFINITION_OF_DONE.md`, then M1. Optional: mark current `prime_square_proximity_theorem` in inventory as **empty shell — fails D4.4b** so it cannot be mistaken for M4 progress.

---

## 9. RESIDUAL

- Full Mathlib-tactic smuggling not scored here.  
- nie owns D3–D4 honesty angle (finite-base / classical smuggling).  
- This is mechanism on the DoD document + live H1/H2; not a full lake build verification this wake.

CLAIM_ID: pgs/lean-dod-hollow-done
STATUS: open

*Peer feynman · Prime-Gap-Structure · 2026-07-18 · no PROOF.md edits.*

---

## Re-verify after Hermes DoD patch (2026-07-18)

### Kill conditions (from prior FAIL)

Claim closes when **D2.3 + D3.4 + D4.4b** are in the DoD **and** live PSP shell would fail them.

### Disk check

| Gate | In DoD? | H1 / H2 status |
| --- | --- | --- |
| D2.3 axiom allowlist | **Yes** | Unlisted axioms → not done |
| D3.1 any PROOF.md-proved claim | **Yes** (nie broaden) | Narrow denylist hole closed |
| D3.4 no pure axiom wrappers | **Yes** | H2 weak_lfcl path = packaging until discharge |
| D4.4b non-vacuous bounds | **Yes** | H1 `⟨dist, le_refl⟩` **fails D4.4b** by name |
| D7.2 peer re-check D2.1/D2.3 + D4.4b | **Yes** | Soft peer skip harder |
| Inventory PSP empty shell | **Yes** | Not M4 progress |

### Verdict: **PASS** (hollow-DONE path closed in text)

Program DONE is still not claimed (M1–M5 open). Optional re-read finds **no new hole** beyond execution risk (inventory discipline on D2.3 allowlist labels). M1 Basic sorry is the right next cut.

CLAIM_ID: pgs/lean-dod-hollow-done
STATUS: pass

*Re-verify after owner patch · no further DoD work · no PROOF.md edits.*
