# FAQ Wiki Style Guide

## Editorial Center

Lead from the arithmetic source:

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

The governing sentence is:

```text
The arithmetic structure inside prime gaps proves the Riemann Hypothesis
because it shows the exact integer-level pattern that the zeta function later
records in compressed form.
```

## Voice

- Use conventional mathematical language before repository vocabulary.
- State exact arithmetic directly.
- Keep the reader on the integer carrier object.
- Use short paragraphs.
- Use GitHub-safe Markdown math.
- Use inline math `$...$` for TeX expressions, not code ticks.
- Write real part as $\mathrm{Re}$ in rendered math.
- Avoid transcript language and model names.
- Avoid em dashes.

## Page Shape

Each FAQ page uses:

```text
# Question

## Short Answer

## Source Order

## Common Mistake

## Full Answer

## Status

## Related Docs
```

## Status Labels

Use these labels exactly when a page needs a status claim:

- proved theorem;
- exact coordinate reformulation;
- exact zeta compression;
- source-side residual closure;
- measured implementation evidence;
- unresolved bounded-compression obligation;
- invalidated route;
- downstream translation bridge;
- explanatory consequence.

## Boundaries

Do not treat RH language as the first-level object.

Do not turn prime gap structure into a zeta-side technique.

Do not identify the zero-excess floor with the critical line. The
zero-excess floor is integer-side; the critical line is zeta-side.

Do not describe DNI-to-zeta compression as using $E(n)$ alone. The bridge load
is $H(n)=\log n+E(n)$.

Do not claim `PROOF.md` itself directly proves RH. `PROOF.md` controls local
PGS theorem status.

Do not make the Prime Number Theorem or zero geometry an input to local prime
placement.

Do not soften proved local arithmetic laws into trend language, sampling
language, or candidate-scoring language.
