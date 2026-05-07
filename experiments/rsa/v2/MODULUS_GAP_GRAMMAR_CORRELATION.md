# Modulus Gap Grammar Correlation Probe

## Purpose

This note records the first RSA v2 experiment built from the corrected frame:

```text
read the PGS grammar around N first,
then compare downstream target-side gap grammar only after public grammar is
computed
```

The experiment does not search for `p` or `q`. It measures whether the
gap/chamber grammar around a public modulus `N` constrains the grammar around
the known target-side prime chambers after audit labels are attached.

## Prior PGS Grammar Work Re-Examined

The earlier gap-type work defines a gap type as:

```text
o{first_open}_d{winner_d}_a{winner_offset}_{carrier_family}
```

where:

- `first_open` is the first wheel-open even offset after the left endpoint;
- `winner_d` is the GWR-selected divisor class;
- `winner_offset` is the leftmost arrival offset of that selected class;
- `carrier_family` is the selected integer family.

The exact type alphabet grows by accretion, but the scaffold is stable. On the
cataloged surface through sampled `10^18`, exact types grew from `224` to
`274`, while all observed types stayed inside the same six-family scaffold.

The stronger grammar object is not the exact type key. It is the reduced state:

```text
open_family|d_bucket
```

with divisor buckets:

```text
d<=4
5<=d<=16
17<=d<=64
d>64
```

The persistent reduced grammar closes to a `14`-state core on the high-scale
sampled surface. The dominant object is the Semiprime Wheel Attractor:

```text
o2_odd_semiprime|d<=4
o4_odd_semiprime|d<=4
o6_odd_semiprime|d<=4
```

The prior grammar line also found the same pattern that later appeared in the
transported ledger:

```text
one-step state is weak
lag-2 / recursive state is materially stronger
reset or re-entry structure matters
```

## Current Probe

The implemented sidecar is:

```text
modulus_gap_grammar_correlation_v1
```

Script:

```text
experiments/rsa/v2/modulus_gap_grammar_probe.py
```

Public artifact:

```text
experiments/rsa/v2/output/modulus_gap_grammar/public_grammar_rows.jsonl
```

Downstream target-label artifact:

```text
experiments/rsa/v2/output/modulus_gap_grammar/target_correlation_rows.jsonl
```

Summary artifact:

```text
experiments/rsa/v2/output/modulus_gap_grammar/summary.json
```

Expanded catalog artifact:

```text
experiments/rsa/v2/output/modulus_gap_grammar_catalog/public_grammar_rows.jsonl
experiments/rsa/v2/output/modulus_gap_grammar_catalog/target_correlation_rows.jsonl
experiments/rsa/v2/output/modulus_gap_grammar_catalog/summary.json
```

The public row records only grammar around `N`:

```text
previous gap
containing gap
following gap
```

The downstream row joins known target-side labels only after the public grammar
row exists:

```text
target left gap
target right gap
transition:
  N containing reduced state -> target left reduced state / target right reduced state
```

## First Measured Surface

Current surface:

```text
public cases: 2
target-side rows: 4
```

Summary:

```text
distinct_transition_count: 4
n_containing_match_target_left_count: 1
n_containing_match_target_right_count: 0
n_previous_match_target_left_count: 0
n_following_match_target_right_count: 1
```

Observed transitions:

```text
o4_d4_odd|d<=4 -> o4_d4_odd|d<=4 / o2_d4_odd|d<=4
o4_d4_odd|d<=4 -> o6_d4_odd|d<=4 / o2_d4_odd|d<=4
o6_d4_odd|d<=4 -> o4_d4_odd|d<=4 / o2_higher_divisor_even|17<=d<=64
o6_d4_odd|d<=4 -> o6_d4_even|d<=4 / o2_d4_odd|d<=4
```

## Expanded Catalog Surface

The catalog was expanded through the exact divisor-count backend using:

```text
benchmarks/python/predictor/midscale_balanced_corpus.json
benchmarks/python/predictor/scaleup_corpus.json
```

with:

```text
max_case_bits: 62
```

The current exact backend is `int64`-bounded in the divisor-count segment path,
so larger catalog rows are deliberately excluded until the backend can measure
larger coordinates directly.

Measured surface:

```text
public cases: 24
target-side rows: 48
distinct transitions: 40
```

Match counts:

```text
N containing == target left: 8
N containing == target right: 6
N previous == target left: 9
N following == target right: 9
```

Public `N` containing chambers:

```text
o2_d4_odd|d<=4: 9
o4_d4_odd|d<=4: 9
o6_d4_odd|d<=4: 4
o2_d4_even|d<=4: 2
```

Target-side higher-divisor intrusions:

```text
public N-containing higher-divisor rows: 0 / 24
target-side rows with a higher-divisor chamber: 10 / 48
```

Endpoint-side split:

```text
p rows: 24
q rows: 24

p with d4 on both sides: 19 / 24
q with d4 on both sides: 19 / 24

p touching higher-divisor chamber: 5 / 24
q touching higher-divisor chamber: 5 / 24
```

Directional higher-divisor placement:

```text
p left higher-divisor:  4 / 24
p right higher-divisor: 1 / 24

q left higher-divisor:  1 / 24
q right higher-divisor: 4 / 24
```

Most repeated transition:

```text
o2_d4_odd|d<=4 -> o4_d4_odd|d<=4 / o4_d4_odd|d<=4
count: 3
```

## Significant Finding: Directional Target-Side Intrusion

On the current `24`-case exact catalog, the public modulus coordinate `N`
always sits inside a `d4` containing chamber. The known target-side endpoint
neighborhoods mostly sit inside `d4` chambers as well, but the higher-divisor
exceptions are not placed symmetrically.

For `p`, the higher-divisor chamber appears primarily on the left side:

```text
p left higher-divisor:  4
p right higher-divisor: 1
```

For `q`, the higher-divisor chamber appears primarily on the right side:

```text
q left higher-divisor:  1
q right higher-divisor: 4
```

The observed high-divisor rows are:

```text
mid_47_anchor_2  q  left d4                 right o2_higher_divisor_even|17<=d<=64
mid_50_anchor_1  p  left o2_higher...       right d4
mid_50_anchor_2  p  left d4                 right o2_higher_divisor_odd|5<=d<=16
mid_50_anchor_2  q  left o2_higher...       right d4
mid_52_anchor_2  q  left d4                 right o4_higher_divisor_even|5<=d<=16
mid_54_anchor_1  p  left o2_higher...       right d4
mid_54_anchor_3  p  left o2_higher...       right d4
mid_57_anchor_4  q  left d4                 right o2_higher_divisor_even|17<=d<=64
mid_60_anchor_2  q  left d4                 right o2_higher_divisor_odd|5<=d<=16
mid_60_anchor_4  p  left o6_higher...       right d4
```

This is significant because it is an orientation-bearing grammar feature. The
public `N` containing chamber does not itself carry a higher-divisor intrusion
on this exact surface, but the target-side neighborhoods do, and their placement
leans outward:

```text
left side of p
right side of q
```

That gives the next experiment a concrete PGS-native elimination object:

```text
derive which transported or recursively adjacent chambers cannot contain the
outward higher-divisor intrusion pattern required by the target-side grammar
```

The result remains a catalog finding. It does not identify `p` or `q`, and it
does not use divisibility, product closure, `gcd`, primality APIs, or audit
labels as inference. The known `p` and `q` values enter only after the public
`N` grammar rows are computed, as downstream labels.

## Hypothesis: Prime Multiplication Creates Outward Gap Bias

The xAI interpretation of the measured result is:

```text
Prime multiplication creates outward gap bias.
```

In plain terms:

```text
N = p * q
```

does not place the public coordinate and the two secret prime coordinates into
independent local gap neighborhoods. On the measured surface, the public
coordinate `N` occupies a `d4` containing chamber, while the more complicated
higher-divisor chambers near the secret primes appear preferentially on the
outside of the factor pair:

```text
left of p
right of q
```

Measured support:

```text
N containing higher-divisor rows: 0 / 24

p left higher-divisor:  4 / 24
p right higher-divisor: 1 / 24

q left higher-divisor:  1 / 24
q right higher-divisor: 4 / 24
```

The proposed PGS-native reading is:

```text
public N grammar constrains admissible factor-side grammar orientation
```

The inference target is not a factor candidate. The inference target is a set
of impossible chamber setups around a factor-side endpoint. If the outward bias
persists across larger exact catalogs, the decomposer can use public gap grammar
to eliminate factor-side chambers whose local grammar places higher-divisor
intrusions on the wrong side.

Compact rule candidate:

```text
For N = p*q with p < q, a higher-divisor intrusion adjacent to a factor-side
endpoint is admissible first on the outward side:

p: left side
q: right side

Inward higher-divisor intrusion is the exception class and must be explained by
recursive neighboring grammar before it is admitted.
```

This is not yet a theorem. It is a falsifiable PGS grammar hypothesis supported
by the current exact catalog. The next catalog expansion should test whether
the same outward placement dominates when the exact grammar backend is extended
beyond the current `62`-bit coordinate boundary.

## Grok Variant: Outward Grammatical Twist

Grok's sharper phrasing names the same object as:

```text
outward grammatical twist from prime multiplication
```

In the oriented pair:

```text
p < q
```

there are two inner sides and two outer sides:

```text
outer side of p: left of p
inner side of p: right of p

inner side of q: left of q
outer side of q: right of q
```

The measured higher-divisor intrusions split as:

```text
outward higher-divisor intrusions: 8
inward higher-divisor intrusions:  2

outward : inward = 4 : 1
```

That ratio is the current exact-catalog form of the twist. It is stronger than
the proposed `3:1` continuation threshold, but the sample is still small.

The strong raw statement:

```text
complex clusters always appear outward
```

is not the current row-level rule, because the catalog contains `2` inward
higher-divisor intrusions:

```text
p right higher-divisor: 1
q left higher-divisor:  1
```

The supported rule is:

```text
complex clusters preferentially appear outward, and inward appearances form an
exception class that must be explained by neighboring or recursive grammar
before they are admitted.
```

This changes the search frame. The first object is no longer a factor candidate.
The first object is the orientation of a chamber:

```text
does this chamber face inward or outward relative to an admissible factor-side
pair?
```

A future decomposer-side filter should therefore treat an inner-side
higher-divisor intrusion as structurally suspect, not merely less frequent. The
filter is valid only after it is derived from public grammar and recursive
neighboring grammar, without divisibility, product closure, `gcd`, primality
APIs, random search, or audit labels as inference.

Internal consistency check:

```text
If the smaller/larger factor labels are swapped, the named left/right sides
must flip, but the inner/outward orientation must remain invariant.
```

This check distinguishes an oriented PGS grammar law from an accidental
left/right frequency imbalance.

## Gemini Variant: Grammatical Vacuum Of The Semiprime

Gemini's phrasing names the center-side effect as:

```text
the grammatical vacuum of the semiprime
```

The measured object is the contrast between the public product chamber and the
factor-side endpoint neighborhoods:

```text
public N containing chamber: clean d4 layer
factor-side outer neighborhoods: higher-divisor intrusions concentrate here
```

On the current exact catalog:

```text
N containing higher-divisor rows: 0 / 24
target-side higher-divisor rows: 10 / 48
outward target-side higher-divisor rows: 8 / 10
```

The word `vacuum` is useful because the public product does not simply share
the local complexity observed near its hidden factors. On this measured surface,
the product coordinate occupies the simplest grammar layer while the more
complicated higher-divisor chambers appear in the factor-side neighborhoods,
mostly on the outer sides.

In oriented notation:

```text
p < q

center interval:       p ... q
outer side of p:       left of p
outer side of q:       right of q
```

The candidate grammar picture is:

```text
N sits in a d4 chamber
outer factor-side walls carry the higher-divisor intrusion
inner factor-side walls usually remain d4-admissible
```

The next rule family should test this as an elimination law:

```text
wrong orientation = complexity wall facing inward
admissible orientation = complexity wall facing outward or no complexity wall
```

The current support is exact but small. The live claim is not that every factor
has an outer higher-divisor wall. The live claim is:

```text
when a higher-divisor wall appears near a known factor endpoint, it is
outward-biased at 8:2 on the current exact catalog, while the public N
containing chamber remains 0:24 for higher-divisor complexity.
```

This supplies a concrete catalog target for the decomposer:

```text
find public grammar rules that make inward complexity walls impossible before
testing factor candidates
```

## Copilot Variant: Outward Divergence Constraint

Copilot's version turns the grammar observation into the first explicit
constraint:

```text
Outward Divergence Constraint for Semiprime Gap Grammar
```

When the public semiprime coordinate `N` sits inside a low-divisor containing
chamber, the local grammar imposes an orientation constraint. Higher-divisor
clusters appear preferentially on the outward-facing sides of the factor pair.
Inward higher-divisor intrusions are structurally suppressed unless recursive
neighbor grammar explains them.

Definitions:

```text
p < q

outward intrusion:
  higher-divisor chamber left of p
  higher-divisor chamber right of q

inward intrusion:
  higher-divisor chamber right of p
  higher-divisor chamber left of q
```

Outward Intrusion Index:

```text
OII = outward_higher_divisor_intrusions / inward_higher_divisor_intrusions
```

Current exact catalog:

```text
outward_higher_divisor_intrusions = 8
inward_higher_divisor_intrusions  = 2
OII = 4.0
```

Candidate decision rule:

```text
If:
  N containing reduced state is in the d<=4 layer
  N previous reduced state is in the d<=4 layer
  N following reduced state is in the d<=4 layer

Then:
  reject a factor-side chamber hypothesis that places a higher-divisor
  intrusion on the inner side

Unless:
  a lag-2 or deeper recursive neighbor chain supplies compensating
  higher-divisor grammar
```

This rule uses only reduced PGS grammar orientation and recursive neighbor
states. It does not use divisibility, smoothness, product closure, `gcd`,
primality APIs, factor APIs, audit labels, or random search.

Prediction:

```text
Exact catalogs beyond the current 62-bit coordinate boundary should preserve
OII > 2.5 under the same measurement protocol.
```

Clear falsifier:

```text
A larger exact catalog under identical measurement rules yields OII near 1,
or inward intrusions occur systematically without recursive neighbor
explanations.
```

The significance is the shift in object:

```text
from searching for factor values
to testing chamber orientation compatibility
```

The public `N` chamber acts as a grammar anchor. Under the stated preconditions,
it forbids certain high-divisor placements on the inner sides of the hidden
factor pair unless recursive grammar supplies a public compensating structure.

## Claude Variant: Grammar Orientation Operator

Claude's analysis isolates the core signal from the background surface:

```text
Prime multiplication acts as a grammar orientation operator.
```

The background observation is:

```text
N sits in a d4 containing chamber on the current exact catalog.
```

The core observation is stronger:

```text
higher-divisor factor-side intrusions are directionally wound toward the
outside of the ordered factor pair.
```

For:

```text
N = p*q
p < q
```

the public product is a compression event in grammar space. Two factor-side
local grammars collapse into one public coordinate. On the measured surface,
that public coordinate occupies a low-complexity chamber, while the higher-
divisor residue appears preferentially on the exterior sides of the factor
pair:

```text
left of p
right of q
```

Claude's useful metric is the winding ratio:

```text
outward_fraction = outward_intrusions / total_higher_divisor_intrusions
winding_ratio = (outward_fraction - 0.5) / 0.5
```

Current exact catalog:

```text
outward_intrusions = 8
inward_intrusions = 2
total_higher_divisor_intrusions = 10

outward_fraction = 8 / 10 = 0.80
winding_ratio = (0.80 - 0.50) / 0.50 = 0.60
```

The `d4` containment of `N` is background. The winding ratio is the candidate
inference object.

Falsifiable prediction:

```text
On an expanded exact catalog of at least 200 balanced RSA-style semiprimes in
the 64-128 bit range:

outward_fraction >= 0.70
winding_ratio >= 0.40
```

Disconfirmation:

```text
If outward_fraction falls below 0.60, or becomes indistinguishable from 0.50,
the topological winding hypothesis fails.
```

Decision rule for backend expansion:

```text
After the exact grammar backend is extended beyond the 62-bit coordinate
boundary, compute the winding ratio on the first 100 new cases.

If winding_ratio >= 0.40:
  treat outward higher-divisor placement as a grammar-native elimination signal
  and build the inward-exception explanation layer.

If winding_ratio < 0.40:
  discard the orientation hypothesis and return to unoriented grammar
  transition analysis.
```

Adversarial status:

```text
d4 dominance alone is not the discovery.
directional winding is the discovery.
current sample size is small.
current utility is as one recursive elimination layer, not a standalone
decomposer.
```

Predicted failure regimes:

```text
unbalanced semiprimes
non-prime factors
special cases where recursive neighbor grammar explains inward intrusions
```

The current conclusion is therefore:

```text
The measured catalog supports a PGS-native orientation signal. It does not yet
prove a universal law. The next proof-relevant experiment is a larger exact
catalog plus recursive explanation of the inward exception class.
```

## Mets Variant: Outward Reset Gate

Mets' version names the public-product role as:

```text
outward reset gate at the public modulus
```

The public product is treated as a low-complexity center that cannot hold the
higher-divisor intrusions observed near some factor-side endpoints. Under this
picture, the higher-divisor intrusions are directed outward:

```text
p: left side
q: right side
```

The useful new claim is about the exception class. Inward higher-divisor
intrusions should require a public three-gap reset rhythm around `N`.

Current inward exceptions:

```text
mid_50_anchor_2  p  right higher-divisor
mid_50_anchor_2  q  left higher-divisor
```

Both inward exceptions occur in the same modulus row. The public three-gap
grammar around that `N` is:

```text
N previous:    o2_higher_divisor_even|5<=d<=16
N containing:  o4_d4_odd|d<=4
N following:   o4_d4_odd|d<=4
```

Exact public keys:

```text
N previous:    o2_d8_a3_higher_divisor_even
N containing:  o4_d4_a2_d4_odd
N following:   o4_d4_a14_d4_odd
```

This is important because the only current inward exception row is not a clean
`d4 / d4 / d4` public neighborhood. It carries a higher-divisor public previous
gap immediately before the `N` containing chamber.

Candidate reset-rhythm condition:

```text
An inward factor-side higher-divisor intrusion is admissible only when the
public three-gap neighborhood around N contains a reset rhythm, currently
observed as:

higher-divisor previous gap -> d4 containing gap -> d4 following gap
```

Reset-gate falsifier:

```text
If a future exact catalog contains inward factor-side higher-divisor intrusions
while the public N previous, containing, and following reduced states are all
d<=4 and no lag-2 recursive reset rhythm appears, the reset-gate rule is
invalidated.
```

Decision use:

```text
read the three public gaps around N first;
if no reset rhythm is present, reject inward higher-divisor chamber hypotheses;
if a reset rhythm is present, send the row to recursive exception analysis.
```

## Deepseek Variant: Inward Intrusion Means Proximity

Deepseek's version assigns meaning to the inward exception class:

```text
Inward higher-divisor chambers require factor proximity.
```

The current catalog supports this direction exactly in the measured surface.
There is one modulus row with inward higher-divisor intrusions:

```text
mid_50_anchor_2
```

It is the closest factor pair in the `24`-case exact catalog:

```text
p = 23734751
q = 23734759
q - p = 8
rank by q-p: 1 / 24
```

The inward intrusions for that row are:

```text
p right higher-divisor
q left higher-divisor
```

The public grammar around `N` for the same row is:

```text
N previous:    o2_higher_divisor_even|5<=d<=16
N containing:  o4_d4_odd|d<=4
N following:   o4_d4_odd|d<=4
```

So the current evidence links the two exception markers:

```text
inward factor-side higher-divisor intrusion
public previous-gap higher-divisor reset rhythm
smallest observed factor separation
```

The supported rule direction is:

```text
inward higher-divisor intrusion -> proximity signal
```

The reverse direction is not supported:

```text
proximity signal -> inward higher-divisor intrusion
```

Several close factor pairs do not show inward higher-divisor intrusions, so
proximity is not sufficient. The current claim is that inward complexity is a
proximity marker when it appears.

Candidate decomposer use:

```text
If external public bounds or prior PGS elimination exclude close-factor
structure, reject factor-side chamber hypotheses that require inward
higher-divisor intrusions.

If inward higher-divisor intrusion appears together with a public reset rhythm,
route the row to a close-factor chamber analysis instead of treating it as a
generic outward-bias violation.
```

Clear falsifier:

```text
An expanded exact catalog contains inward higher-divisor intrusions next to a
factor pair with wide separation and no public recursive reset rhythm.
```

## Strongest Supported Finding

The expanded exact catalog establishes the next object:

```text
N-containing chamber grammar and target-side chamber grammar can be represented
in the same reduced PGS grammar alphabet without searching for p or q
```

On the current `24`-case exact surface, every public `N` containing chamber is
in the `d<=4` grammar layer:

```text
o2_d4_odd|d<=4
o4_d4_odd|d<=4
o6_d4_odd|d<=4
o2_d4_even|d<=4
```

The target-side labels stay inside the same reduced grammar scaffold, but
`10` of `48` target-side rows include a higher-divisor chamber adjacent to the
known target coordinate.

```text
N side:       no higher-divisor containing chamber observed
target side: higher-divisor chamber appears as a left or right neighbor
```

That asymmetry is the first concrete elimination handle for the next phase. It
does not identify `p` or `q`. It identifies a grammar feature that is absent
from the public `N` containing chamber on this surface but present near known
target chambers.

## Boundary

This is not a resolver result.

This is not a factor search result.

This is not an RSA-hardness argument.

The result is a PGS-native correlation surface:

```text
public N grammar first,
target-side grammar only as downstream labels,
then search for impossible grammar transitions
```

## Next Valid Step

The next experiment should expand this from a one-row grammar comparison to a
recursive grammar-neighborhood comparison:

```text
N previous / containing / following grammar
-> target left / target right grammar labels
-> lag-2 or recursive reduced-state relation
-> eliminate impossible target-side chamber grammar
```

The operating target is not `p` or `q` directly. The target is the admissible
factor-side chamber type.
