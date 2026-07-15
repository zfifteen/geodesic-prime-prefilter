# Branch-envelope inversion probe

**Status:** hypothesis / measured on named regimes only  
**Not:** theorem, verified, validated, or historical z≥4⇒g=2 claim revival

## Observable object

For consecutive primes `p < q` with nonempty interior, form the GWR
selected witness `w` (leftmost interior minimum of `tau`). Record the
selected-witness offset `w - p` and the divisor count `tau(w)`.

## Mechanism (ordinary language)

The universal UBC envelope in `PROOF.md` is one number `C(q)` for every
branch. This probe checks whether the **largest** offsets on a regime are
carried by the square branch (`tau(w) = 3`), with the `tau = 4` branch next,
and all higher-`tau` branches strictly smaller.

## Project terms

- GWR selected witness `w`
- Selected-witness offset `w - p` (not raw gap `q - p`)
- Branch label `tau(w)`
- UBC envelope `C(q) = max(64, ceil(0.5 * log(q)^2))` used only for utilization, not as a new bound

## Prediction (falsifiable)

On a fixed regime of consecutive prime gaps with nonempty interior:

```text
max(w - p | tau(w) = 3) > max(w - p | tau(w) = 4) > max(w - p | tau(w) >= 6)
```

## Disconfirmation

Any regime where a non-square GWR branch achieves max offset greater than or
equal to the square-branch max on that same regime.

## Measured regimes (this package)

| Regime | max tau=3 | max tau=4 | max tau>=6 | triple holds |
| --- | ---: | ---: | ---: | --- |
| `p in [11, 200000)` | 30 | 18 | 10 | yes |
| `p in [11, 1000000)` | 48 | 22 | 14 | yes |

Artifact: `measure.json`

## Exact limits

- Local and mid-scale regimes only. No `10^18` surface in this package.
- Do not use verified / validated language for this prediction.
- Does not change `PROOF.md` theorem status. UBC remains universal and uniform.
- This is a **branch-stratified effective envelope** hypothesis under a uniform theorem.

## Reproduce

```text
python3 -c "import json; print(json.load(open('research/16-predictions/probes/branch-envelope-inversion-2026-07/measure.json'))['regimes']['11_1000000']['prediction_strict_triple'])"
```

Full re-scan is the inline probe used to write `measure.json` (parent session
insight-ooda-loop, 2026-07).
