# Hypothesis: Gap Winner as One-Way Complexity Valve

## Source

Grok Novel Insight Engine share (2026-07):

- URL: https://grok.com/share/bGVnYWN5_774d61ad-5f04-40b6-9ea3-0c906426684f
- Title in share: *The Gap Winner as One-Way Complexity Valve*
- Status in source: insight / framing layered on proved GWR, No-Later-Simpler, and compression structure; residual-mean elevation not published as a measured surface.

## PGS frame

```text
ordered prime-gap (p, q)
  -> divisor-count field tau on the interior
  -> Gap Winner w = leftmost interior argmin tau
  -> pre-valve interval (p, w) and residual interval (w, q)
  -> residual complexity elevation (prediction) or counter-example
```

Classical sieve / divisor accumulation is field preparation only. It does not choose the valve or the decision.

## Claims under test

### H1 — Residual mean elevation (primary)

For every prime gap with **nonempty interior** and with **both** pre-valve and residual intervals nonempty:

```text
mean(tau on (w, q))  >  mean(tau on (p, w))
```

where

- pre-valve integers = `{p+1, ..., w-1}`
- residual integers = `{w+1, ..., q-1}`
- `w` = leftmost interior `n` with `tau(n) = min tau on (p, q)`

**Falsifier F1:** any such gap with `mean_residual <= mean_pre`.

### H2 — Ratio scales with valve tau (secondary)

Define

```text
ratio = mean_residual / mean_pre
```

Across nonempty-both-side gaps, the ratio is an **increasing function of `tau(w)`** in the bulk sense:

- bucketed mean ratio by `tau(w)` is nondecreasing across adjacent tau buckets with enough samples;
- Spearman correlation of `(tau(w), ratio)` over all eligible gaps is strictly positive.

**Falsifier F2:** Spearman correlation of `(tau_w, ratio) <= 0` on a regime with at least 1000 eligible gaps, **or** any adjacent high-sample tau buckets where mean ratio strictly decreases.

### H3 — No later strictly simpler composite (consistency)

No later interior integer has `tau(n) < tau(w)`.

This restates No-Later-Simpler-Composite as an implementation surface check. It is **not** an attempt to re-prove the theorem.

**Falsifier F3:** any gap with a later interior `n > w` and `tau(n) < tau(w)`.

### H4 — Compression-window localization (scope / decision-rule support)

The share decision rule assumes the valve often sits inside

```text
C(q) = max(64, ceil(0.5 * log(q)^2))
```

so residual length may be ignored for lower-complexity search once `offset = w - p <= C(q)`.

**Falsifier F4 (soft):** not a theorem falsifier. Report fraction of eligible gaps with `offset > C(q)`. A high out-of-window rate weakens the practical decision rule without falsifying H1.

## Explicit non-claims

| Item | Status |
| --- | --- |
| GWR maximizer, NLS, Prime-Square Proximity / compression | **theorem** under `PROOF.md` hypotheses; not demoted by this probe |
| Residual mean elevation | **hypothesis** until measured; never "verified/validated" without executed `10^18` surface |
| Valve metaphor as organizational principle | **hypothesis / framing** |
| Twin gaps (`q - p = 2`) and one-sided empty intervals | **out of scope** for H1/H2 means |

## Success language for outcomes

| Outcome word | When allowed |
| --- | --- |
| **falsified** | F1, F2, or F3 met under the stated regime |
| **did not falsify** | zero F1/F3 hits and F2 correlation positive on that regime |
| **measured on regime R** | always pair with exact `p_max` / gap count |
| **verified / validated** | **forbidden** in this package (no `10^18` surface planned here) |
