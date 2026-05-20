# Documentation Correction Project

Prime Gap Structure proves the exact integer-level arithmetic structure of
prime placement. That structure proves the Riemann Hypothesis because RH
language is the zeta-compressed description of the same source, not the source
object. The repository documentation must preserve that order:

```text
divisor counts -> DNI normalization -> fixed-line prime returns -> ordered gap interiors -> zeta compression -> RH language
```

The correction project exists to remove wording that inverts that order,
demotes proved PGS structure into statistics, or treats RH pole language as the
first-level object.

Primary audit:

- [Documentation Correction Audit](index.html)

## Contract

- `PROOF.md` controls theorem status.
- PGS source structure is stated before zeta, RH, PNT, or asymptotic language.
- Measurement and audit language stays attached to implementation surfaces.
- Bounded-compression obligations stay separate from the universal local
  theorems.
- GitHub-rendered math must use supported Markdown and math notation.
