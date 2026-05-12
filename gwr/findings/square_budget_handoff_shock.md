# Prime-Square Interval Utilization and Next-Gap Semiprime Return

A prime gap has a left endpoint prime, a right endpoint prime, and interior composite integers. For each gap, take the first interior integer whose divisor count is minimal among the gap interior. When that integer has divisor count `d = 4`, the location of the right endpoint carries measurable information about the factorization type selected in the following gap.

For the current minimum-divisor interior integer $w$ and current right endpoint $q$, let $S_{+}(w)$ be the next prime square after $w$. The prime-square interval utilization is:

$$U_{\square}(w, q) = \frac{q - w}{S_{+}(w) - w}.$$

Rows with lower $U_{\square}$ close after using less of the interval before the next prime square. On the retained `10^12..10^18` catalog surface, those rows are followed more often by a gap whose minimum-divisor interior integer is an odd semiprime with divisor count `4` and first admissible offset `2`, `4`, or `6` modulo `30`.

## Matched Transition Surface

The existing matched comparison separates lower and higher utilization halves while holding fixed the current factorization type, the offset of the selected interior integer, and the first admissible offset modulo `30`.

- low-utilization share followed by the odd-semiprime `d = 4` offset class: `0.6994`
- high-utilization share followed by the odd-semiprime `d = 4` offset class: `0.6595`
- matched lift: `+0.0399`
- matched half-pairs per side: `652`

That establishes the transition signal after controlling for the current factorization type and offset data already present in [prime-square interval findings](square_phase_handoff_findings.md).

## Decade-Normalized Check

The pooled split is vulnerable to scale drift, so this demonstration recomputes the low/high split separately inside each decade and matched arithmetic cell. The cell key is `(decade, factorization type, selected-interior-integer offset, first admissible offset modulo 30)`.

- low-utilization `d = 4` support: `618`
- low-utilization next-gap odd-semiprime share: `0.703883`
- high-utilization `d = 4` support: `803`
- high-utilization next-gap odd-semiprime share: `0.666252`
- decade-normalized lift: `+0.037632`

The decade-normalized median split also remains competitive in the log-loss readout:

- decade-normalized median-split gain: `0.015049`
- parity of the selected interior integer gain: `0.014128`
- parity plus previous gap-class gain: `0.108789`
- parity plus previous gap-class plus median-split gain: `0.124778`

Per-decade median-split gains are positive across the retained surface:

- `10^12`: `0.044290`
- `10^13`: `0.034960`
- `10^14`: `0.036995`
- `10^15`: `0.026145`
- `10^16`: `0.017490`
- `10^17`: `0.028707`
- `10^18`: `0.018099`

## Bounded-Method Note

ChatGPT's adversarial critique identified the correct pressure point: the original pooled median-split table is an in-surface result. That does not erase the signal, but it changes the public wording. The decade-normalized result is the headline demonstration. The held-out test remains a frozen train-below-target test where medians and probability tables are learned below the target decade and scored forward.

This is not a next-prime rule. The quantity $U_{\square}(w, q)$ uses the already-known current endpoint $q$, so it is a transition observable for the next gap, not a mechanism for choosing the current endpoint.

## Held-Out Test

The next direct test is: train the matched-cell medians and probability tables on lower retained decades, freeze them, and score a later target decade. The claim is weakened if the low-utilization `d = 4` group does not exceed the high-utilization `d = 4` group on the held-out target, or if adding the median split to the parity plus previous gap-class model gives zero or negative held-out log-loss improvement.

## Artifacts

- [demo script](../../benchmarks/python/predictor/gwr_square_budget_handoff_shock_demo.py)
- [summary JSON](../../output/gwr_square_budget_handoff_shock_summary.json)
- [source catalog detail CSV](../../research/03-gap-types/output/gwr_dni_gap_type_catalog_details.csv)
