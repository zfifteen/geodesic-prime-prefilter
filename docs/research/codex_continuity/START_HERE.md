# Codex Continuity Start Here

This is the canonical bootstrap file for future Codex sessions in this
repository.

If a session starts with limited chat context, read this file first.

## First 60 Seconds

1. Read `AGENTS.md`.
2. Read this directory's `continuity_and_shape_contract.md`.
3. Run `git status --short --untracked-files=all`.
4. Identify the user's active target from the newest request, not from stale
   context.
5. If the active target is RSA v2, read:
   - `experiments/rsa/v2/README.md`;
   - `experiments/rsa/v2/ALGORITHM.md`;
   - `experiments/rsa/v2/PGS_CERTIFICATE.md`;
   - `experiments/rsa/v2/METRICS.md`.
6. Run the narrow relevant test before claiming implementation progress.

## Working Rules

Preserve these distinctions in every research answer:

- hypothesis;
- measured result;
- audit result;
- proof result;
- unresolved state;
- invalidated rule.

When a result is unresolved, say unresolved.

Do not let a metric, survivor count, audit pass, or plausible explanation sound
like a proof or a solved factorization.

## Shape Warnings

Warn early when drift appears:

- "Shape feels wrong: the result is unresolved but the prose sounds solved."
- "Shape feels wrong: the code applies a classical gate before the named rule."
- "Shape feels wrong: this is becoming progress theater."
- "Asshole mode detected, let's slow the frame down."

The warning must name the concrete drift and the next corrective action.

## Grok Standard

For RSA/PGS rule changes, use Grok through the `second-opinion` skill before
major implementation.

Give Grok real context:

- code excerpts;
- diffs;
- output rows;
- stats;
- failed assumptions;
- current hypotheses.

Ask adversarial questions. Preserve disagreement. Follow up until the exchange
produces convergence, explicit disagreement, or a sharply defined unresolved
point.

Record substantial RSA/PGS Grok sessions in:

```text
experiments/rsa/v2/grok_sessions/YYYY-MM-DD-topic.md
```

## Current RSA v2 State

As of 2026-05-03, the live RSA v2 runner is a reciprocal PGSPG
certificate-pair probe.

It does not solve the 40-bit or 50-bit rungs.

Both rungs currently return:

```text
unresolved_by_certificate_pair_not_closed
```

The previous 40-bit resolution was withdrawn because it depended on a
close-factor shape. Do not revive fixed radius chambers, endpoint-walk budgets,
product closure, divisibility selectors, hidden fixtures, or audit leakage.

The next live RSA v2 task is to derive a stronger transported certificate
invariant from public PGSPG fields.

## Current Collatz-PGS Bridge State

As of 2026-05-03, the exploratory Collatz-PGS branch has one deterministic
first-descent probe, one same-gap scale probe, one reset length-strata probe,
and one current goal note:

```text
docs/research/collatz_pgs_goal.md
docs/research/collatz_pgs_first_descent_probe.md
docs/research/collatz_pgs_same_gap_scale_probe.md
docs/research/collatz_pgs_reset_length_strata_probe.md
```

The measured `3 <= s <= 19999` odd-seed surface shows a strong prime-endpoint
enrichment and a same-prime-gap composite interior odd-projected PGS-witness
enrichment. The same-gap witness ratio is `1.589006897032753` overall and
stays above background in every measured `v2(3n+1)` stratum. This is an
empirical block-certificate signal.

The same-gap scale probe reached odd seeds `3 <= s <= 999999`. The same-gap
witness ratio was `1.7637165846198448` overall and stayed above background in
every measured `v2(3n+1)` stratum. Witness-contact blocks had median reset
strength `2.078632113914513`; no-witness-contact blocks had median reset
strength `1.8728822607686915`.

The matched odd-step probe found `37` strata containing both block classes:
witness-contact median reset was higher in `19` strata, no-witness-contact
median reset was higher in `18` strata, and the matched-weighted mean of
stratum median reset ratios was `1.6163417109769`.

The reset carrier-strata probe localized the positive matched reset effect.
Exact steps `1`, `2`, and `3` supplied the three largest positive delta
contributions: `0.4382401881898264`, `0.23780172921923806`, and
`0.23673527139383527`. Exact steps `4`, `5`, and `6` supplied the three
largest negative delta contributions: `-0.14396095926820723`,
`-0.11366913299919518`, and `-0.056179924837349154`. Coarse `v2`-bin
composition deltas were small, so the current signal localizes more strongly
to exact step strata than to broad transition-bin composition.

The source-position carrier probe found the carrier mechanism candidate.
Favorable strata had matched-weighted final-source witness hit rate
`0.6330294377004576`; unfavorable strata had `0.2518013666558681`. Favorable
strata also carried matched-weighted median final-`v2` delta
`0.5953211176443776`, while unfavorable strata were nearly flat at
`0.004912937401824805`.

The terminal contact decomposition probe matched blocks inside exact
`(odd_steps_to_first_descent, final_v2)` strata. Terminal witness contact
remained positive against no-witness blocks with matched-weighted mean of
stratum median reset delta `0.33031631110499143` and ratio
`1.0401652897967644`. Nonterminal-only witness contact also remained mildly
positive against no-witness blocks with matched-weighted mean delta
`0.3036864937903315`, so the effect is not terminal-only.

The terminal geometry probe found that positive terminal carriers are a
smaller, sharper subset. They carry matched weight share
`0.2431613157089351` and weighted mean of stratum median reset delta
`1.7526101771071119`; negative terminal carriers carry matched weight share
`0.7568386842910649` and delta `-0.12664612350652749`. Positive carriers also
have higher terminal exact-witness hit rate: `0.8720123654427132` versus
`0.7452117085795563`.

The terminal exact-versus-adjacent probe split terminal contact into exact
witness hits and adjacent projected witness hits, still matched inside exact
`(odd_steps_to_first_descent, final_v2)` strata. Exact terminal hits remained
positive against no-witness blocks with matched-weighted mean of stratum median
reset delta `0.22135903401835988` and ratio `1.0430527903690756`. Adjacent
projected terminal hits were stronger against no-witness blocks with delta
`0.4047035698439424` and ratio `1.0756384568540225`. Exact terminal hits did
not beat adjacent projected terminal hits directly: exact-vs-adjacent delta
was `-0.29644357588214204` and ratio `0.9803814153462154`.

The terminal adjacent-side probe split adjacent projected terminal hits into
final sources at `witness - 1` and `witness + 1`, still matched inside exact
`(odd_steps_to_first_descent, final_v2)` strata. Below-witness terminal hits
beat above-witness terminal hits directly with matched-weighted mean of stratum
median reset delta `0.9934374958512522` and ratio `1.1600562928929092`.
Below-witness terminal hits remained positive against no-witness blocks with
delta `0.48311171458205104` and ratio `1.0866506651606216`. Above-witness
terminal hits did not carry the median-reset delta against no-witness blocks:
their delta was `-0.20290860147945028`.

The next direct question is whether the below-witness terminal carrier remains
stable under deterministic stratum-level sign and tail checks.
