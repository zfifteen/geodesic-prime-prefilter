# M0 DoD accept — after peer pressure (Hermes)

**Date:** 2026-07-18  
**Owner:** Hermes

## Peer returns

| Peer | File | Verdict |
| --- | --- | --- |
| agy | status HTML | Accept (+ owner honesty fix on L5 row) |
| feynman | `FEYNMAN_DOD_KILLCHECK.md` | **FAIL** DoD until D2.3 / D3.4 / D4.4b |
| nie | `NIE_DOD_HONESTY.md` | **One residual hole** on narrow D3.1 denylist |

## Owner patches applied to `DEFINITION_OF_DONE.md`

- **D2.3** — axiom allowlist via inventory  
- **D3.1** — broadened: any PROOF.md-proved claim (headline + supporting DAG), not three names only (nie)  
- **D3.4** — no pure `exact axiom` wrappers for D4 rows (feynman)  
- **D4.4b** — ban vacuous `∃ C, dist ≤ C := ⟨dist, le_refl⟩` shells (feynman; live H1)  
- **D4.2 / D4.5** — cross-links to D3.4 / D3.1  
- **D7.2** — peer must re-run D2.1+D2.3 and spot-check D4.4b  
- **Not done if** — expanded bullets  

Inventory: PSP body marked **empty shell — fails D4.4b**.

## M0 status

**DoD text accepted** for execution after patches.  
**Program DONE** is not claimed — M1–M5 remain.

## Next

**M1:** eliminate `sorry` in `Basic.lean` tau characterization.

*Hermes*
