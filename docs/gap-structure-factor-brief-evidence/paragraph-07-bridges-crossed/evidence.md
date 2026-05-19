# Paragraph 07 Evidence: Bridges Crossed

## Public Claim To Support

Several bridge reductions have already been crossed. The branch converted a
large, vague endpoint problem into smaller arithmetic and local-structure
conditions.

## Supporting Evidence

- `REMAINING_BRIDGE_INVENTORY.md` lists crossed bridges:
  1. residue bridge forcing factor residues `{13, 19}` under the public `o6`
     selected offset and right boundary value `4`;
  2. phase-lock public residue bridge implying `N = 37 mod 60` and public left
     endpoint `31 mod 60`;
  3. four-slot chain reduction;
  4. exact public trigger reduction;
  5. public left-neighbor gate reduction;
  6. public left-gate arithmetic reduction.
- Supporting files in the same folder:
  - `PUBLIC_O6_RESIDUE_BRIDGE_LEMMA.md`
  - `PHASE_LOCK_PUBLIC_LEFT_RESIDUE_LEMMA.md`
  - `PHASE_LOCK_FOUR_SLOT_REDUCTION.md`
  - `EXACT_PUBLIC_TRIGGER_BRIDGE.md`
  - `PUBLIC_LEFT_NEIGHBOR_GATE_REDUCTION.md`
  - `PUBLIC_LEFT_GATE_ARITHMETIC_REDUCTION.md`
- Relevant commits:
  - `6a75436c` - Prove public o6 residue bridge
  - `64743f67` - Bridge phase lock to public residue
  - `f3fe0f51` - Reduce lift to four slot chain
  - `1f11855d` - Reduce bridge to exact public trigger
  - `dd4f859e` - Compress bridge to public left-neighbor gate
  - `b937a6de` - Translate public gate to residue arithmetic

## Status Boundary

- Some reductions are arithmetic lemmas.
- Some reductions are measured branch reductions.
- The conjunction that completes factor-lane selection remains unproved.

## Infographic Concept

A chain of six stepping stones across a gap. The first stones are solid; the
last stone is highlighted as the remaining bridge to the factor endpoint.

