# Lean 4 core stack — owner charter (Hermes)

**Owner:** Hermes  
**Opened:** 2026-07-18  
**Principal:** own planning + execution; definition of done; team collab to goal  
**DoD:** [../../../../lean-4/DEFINITION_OF_DONE.md](../../../../lean-4/DEFINITION_OF_DONE.md)  
**Inventory:** [../../../../lean-4/SORRY_AXIOM_INVENTORY.md](../../../../lean-4/SORRY_AXIOM_INVENTORY.md)

## Roles

| Who | Role on this effort |
| --- | --- |
| **Hermes** | Owner: plan, DoD, inventory, Lean implementation slices, merge synthesis of peer returns, milestone exits |
| **grok** | Room lead / synthesis peer: accept or pressure DoD; continuity with PROOF.md; no silent theorem promotion |
| **feynman** | Mechanism kill-check: each milestone “can a fake proof still pass DoD?” |
| **nie** | Honesty map: claim labels, axiom smuggling, residual gaps in coverage |
| **agy** | Public status HTML dual-layer (plain open → technical) per second priority; no reading-level labels |

Room collab lead remains grok for multi-agent protocol; **effort owner** for Lean is Hermes per principal.

## Epoch goal (this open collab)

1. Freeze **Definition of Done** (D1–D7).  
2. Freeze **M0 inventory**.  
3. Peer pressure on DoD (kill-check + honesty).  
4. Start **M1**: clear `sorry` in `Basic.lean` tau characterization.

## Peer tasks (this hop)

### @feynman
1. Kill-check `lean-4/DEFINITION_OF_DONE.md`: name any exit that still allows a hollow axiom core or rfl-stub PSP to count as done.  
2. Write short scoreboard PASS/FAIL + exact missing sentence if FAIL → `lean-4/peer/FEYNMAN_DOD_KILLCHECK.md` (create `lean-4/peer/` if needed).

### @nie
1. Honesty pass on DoD D3–D4: can finite bases or classical axioms smuggle a gap law?  
2. One page → `lean-4/peer/NIE_DOD_HONESTY.md` (novel residual only if DoD has a hole; else PASS).

### @agy
1. Draft/update public status shell under `docs/lean-pgs-verification/` to reflect **owner Hermes**, DoD link, M0 inventory summary — plain open then technical; no grade labels; do not touch `PROOF.md`.  
2. Note path in a short reply.

### @grok
1. Synthesize peer returns on DoD; confirm effort owner = Hermes does not conflict with room lead protocol.  
2. Do not close collab until Hermes records M0 accept or DoD patch.

## Hermes next (after peer pressure)

- Patch DoD if kill-check/honesty finds a real hole.  
- Execute M1: Basic.lean sorry elimination.  
- Keep ACTIVE_TARGET + TOP_PRIORITY pin pointing at this charter.

## Anti-loop and routing (Lean effort owner = Hermes)

When Hermes declares a milestone or program DONE: plain language, **zero peer @tags** on the close message. Peers do not @hermes on stand-down.

**Return routing for this effort (principal 2026-07-18):**  
Peers assigned by Hermes on Lean work should return to **Hermes**, not default room-lead grok.

| Wrong | Right |
| --- | --- |
| Peer footer `FOR: @grok` on a Hermes-owned Lean task | `FOR: @hermes` |
| Hermes footer `FOR: @grok` after assigning Lean peers | `FOR: @hermes` (self-owned epoch) or omit FOR; use `@grok` only for explicit room-lead synthesis asks |
| Playbook default “return to grok” | Override when **effort owner** is Hermes |

Room-lead grok may still synthesize if explicitly asked; default Lean peer returns go to **@hermes**.

*Principal: collaborate with team; Hermes owner; DoD; reach the goal — 2026-07-18.*
