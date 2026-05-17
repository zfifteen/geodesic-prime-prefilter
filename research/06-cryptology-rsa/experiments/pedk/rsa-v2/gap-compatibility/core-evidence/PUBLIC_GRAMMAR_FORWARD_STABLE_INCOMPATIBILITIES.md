# Public Grammar Forward-Stable Incompatibilities

## Claim

The multiplication map now has a stable rule-discovery surface.

Under the frozen representation

```text
public_word_gwr_side -> oriented_factor_phase_word
```

high-support public/factor cells that were independently present but jointly
absent in both the training band and the calibration band remained absent as
supported cells in the next independent forward band. The strongest measured
result is that the top `5000` selected absent cells produced `0` supported
forward falsifications.

This is measured sidecar evidence. It is not a theorem and it is not live PEDK
factor recovery.

## Object

Each row starts with the public prime-gap neighborhood containing `N`. That
public side records:

```text
previous reduced gap type
containing exact gap subtype and phase of N inside that gap
following reduced gap type
whether N is before, at, or after the GWR winner point inside the containing gap
```

The factor side records the oriented gap neighborhoods around the two factor
endpoints:

```text
p left/right reduced gap types with phase
q left/right reduced gap types with phase
```

The tested cell is therefore:

```text
(public composite-gap word with GWR side, oriented factor-neighborhood word)
```

The factor labels are corpus-construction labels only. They do not enter a live
inference rule.

## Representation Stability

The representation was selected after comparing intermediate projection
surfaces across two independent transitions.

| train band | fresh band | support | rank | testable absent cells | falsified cells | falsification rate |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `7501..9000` | `9001..11000` | `3/3` | `1` | `805221` | `7299` | `9` per mille |
| `7501..9000` | `9001..11000` | `5/5` | `2` | `285387` | `4744` | `16` per mille |
| `9001..11000` | `11001..13000` | `3/3` | `1` | `1264275` | `8517` | `6` per mille |
| `9001..11000` | `11001..13000` | `5/5` | `2` | `476566` | `5960` | `12` per mille |

The representation is not chosen because every absent cell survives. It is
chosen because it keeps enough repeated structure for rule discovery while
avoiding the large collapses that falsified the earlier residue/phase
compression.

## Forward Stability Test

The forward test used:

```text
train band = 9001..11000
calibration band = 11001..13000
forward band = 13001..15000
min_public_support = 5
min_factor_support = 5
supported_observation_threshold = 5
```

Candidate cells were selected as follows:

1. The public word and factor word each had support at least `5` in the train
   band.
2. The pair was absent in the train band.
3. The public word and factor word each had support at least `5` in the
   calibration band.
4. The pair was absent in the calibration band.
5. Surviving cells were ranked by
   `calibration_public_support * calibration_factor_support`, then by the same
   train support product.

Forward results:

| selected cells | forward testable | stayed absent | thin observations | supported falsifications | supported falsification rate |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `200` | `200` | `170` | `30` | `0` | `0` per mille |
| `500` | `500` | `427` | `73` | `0` | `0` per mille |
| `1000` | `999` | `875` | `124` | `0` | `0` per mille |
| `5000` | `4951` | `4601` | `350` | `0` | `0` per mille |

The top `5000` surface did admit thin observations, but no cell reached the
forward support threshold of `5`. Under the stated boundary, the extraction
passed:

```text
falsification boundary:
representation/extraction is insufficient if at least 15 percent of
forward-testable selected cells become supported observations

observed supported falsification rate:
0 / 4951
```

## First Proto-Rule Families

The top `5000` forward-stable cells were profiled into compact family shapes.
The profile found:

```text
profile_count = 556
clean_proto_family_count = 192
mixed_proto_family_count = 364
min_survived = 10
```

A clean proto-family has at least `10` survived absent cells, no thin forward
observations, and no supported forward falsifications inside the selected
surface.

The leading clean families include:

| survived absent cells | public family | factor family |
| ---: | --- | --- |
| `48` | `containing=o2_d4_a2_d4_odd@mid`, `after_winner` | `o4_higher_divisor_odd@early:1`, `o4_higher_divisor_odd@mid:2`, `o6_higher_divisor_odd@mid:1` |
| `47` | `containing=o4_d4_a6_d4_odd@mid`, `after_winner` | q-side `L=o6_higher_divisor_odd@mid`, `R=o4_higher_divisor_odd@mid` |
| `43` | `containing=o2_d4_a2_d4_odd@early`, `at_winner` | `o2_higher_divisor_odd@mid:2`, `o4_higher_divisor_odd@mid:2` |
| `41` | `containing=o6_d4_a6_d4_odd@mid`, `after_winner` | q-side `L=o2_higher_divisor_odd@mid`, `R=o6_higher_divisor_odd@mid` |
| `38` | `containing=o2_d4_a2_d4_odd@mid`, `after_winner` | `o4_higher_divisor_odd@mid:2`, `o6_higher_divisor_odd@late:1`, `o6_higher_divisor_odd@mid:1` |

These are not final laws. They are compact candidates extracted from stable
absent cells. Their value is that they turn a large lookup surface into
families that can be forward-tested directly.

## Current Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = forward-stable incompatibility surface found
active_representation = public_word_gwr_side -> oriented_factor_phase_word
next_rule_object = clean proto-families over public containing subtype/GWR side
                   and oriented factor-neighborhood phase structure
```

The current result supports the gap compatibility hypothesis in a sharper
form: the public gap grammar around `N` and the oriented gap grammar around
`p` and `q` do not combine freely. Large regions of the multiplication map are
stable absences under repeated fresh-band tests.

## Reproduction

Build the third enriched band:

```text
python3 enriched_multiplication_map_corpus.py \
  --band 13001:15000 \
  --output-dir output/enriched_multiplication_map_corpus_13001_15000
```

Run the forward stability test:

```text
python3 absent_cell_forward_stability.py
```

Run wider cuts:

```text
python3 absent_cell_forward_stability.py \
  --top-n 500 \
  --output-dir output/absent_cell_forward_stability_9001_11000_to_11001_13000_to_13001_15000_top500

python3 absent_cell_forward_stability.py \
  --top-n 1000 \
  --output-dir output/absent_cell_forward_stability_9001_11000_to_11001_13000_to_13001_15000_top1000

python3 absent_cell_forward_stability.py \
  --top-n 5000 \
  --output-dir output/absent_cell_forward_stability_9001_11000_to_11001_13000_to_13001_15000_top5000
```

Profile compact families:

```text
python3 stable_absent_family_profile.py
```

The scripts write:

```text
output/absent_cell_forward_stability_*/summary.json
output/absent_cell_forward_stability_*/forward_stability_rows.jsonl
output/stable_absent_family_profile_*/summary.json
output/stable_absent_family_profile_*/family_profile_rows.jsonl
```
