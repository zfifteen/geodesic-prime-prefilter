# Mandatory 10^18 Evidence Surface (HARD RULE)

Canonical prose lives in root `AGENTS.md` under **Mandatory 10^18 Evidence
Surface**. This file is the short machine-facing restatement.

## Non-negotiable

Everything tested in the PGS program that is presented as verified, validated,
or as a program-level measured/audit pass must include testing at `10^18`.

## Theorem separation

- `PROOF.md` universal theorems remain theorem under stated hypotheses and
  finite premises.
- This rule does **not** bound or downgrade proved theorems.
- Finite proof premises named inside `PROOF.md` are proof machinery, not
  implementation validation.
- Do not rewrite proved laws as "only verified up to `10^18`."

## Bound claim words

These words require an **executed** `10^18` surface in the same evidence
package:

- verified
- validated
- validation pass
- implementation verified / validated
- measured pass (program-level)
- audit pass (program-level verification of an implementation or regime)
- any claim that an implementation "validates" a theorem

## Allowed without 10^18

Local-only checks, smoke tests, intermediate probes, and audit corroboration on
named bands below `10^18`, if and only if:

- the exact regime is stated;
- the bound claim words above are not used;
- status stays measured / partial / audit-on-band / unresolved as appropriate.

## Minimum executed surface

Configured-but-not-run ladders do not count. Minimum forms:

1. **Decade ladder** (generator / walk class): sampled consecutive primes at
   decade anchors including `10^18`. Production reference:
   `256` primes per decade, decades `10^8` through `10^18`.
2. **`10^18` anchor band** (other probes): executed band with upper magnitude
   at least `10^18` and committed artifacts.
3. **Domain-specific `10^18` equivalent** only when the experiment contract
   defines a concrete executed `10^18`-scale artifact path.

## Forbidden

- Verified / validated from any surface that stops below `10^18`
- Treating planned or configured ladders as executed
- Promoting small-band audit green to implementation validation
- RH / PNT / RSA-scale inflation from a `10^18` measured pass

## Shape warning

"Shape feels wrong: this is called verified or validated without an executed
`10^18` surface."
