# Public Grammar Representation Reset

## Claim

The recent rule-chasing failures are representation failures, not evidence that
the multiplication-map signal is gone.

The previous working representation compressed each row too early:

```text
public_word around N
factor_residue_multiset
factor_phase_multiset
```

That projection is useful for finding coarse signal, but it is too lossy for
stable rule discovery. The next research object is the enriched multiplication
map: row-level public structure around `N` paired with factor-side grammar that
preserves phase, orientation, and position before compression.

## New Corpus Object

The enriched corpus keeps:

```text
public previous / containing / following gap structure
public containing exact subtype
N position inside its containing gap
GWR signed distance and side
factor residue multiset
factor phase multiset
full factor phased word
full factor positioned word
oriented p-side and q-side phase words
oriented p-side and q-side positioned words
```

The `p` and `q` fields remain corpus-construction labels only. They are not
public inference inputs.

## Two-Band Projection Comparison

The enriched corpus was built on two independent fresh bands:

```text
7501..9000
9001..11000
```

The projection table measures how many distinct keys each representation
produces and how much row collision remains. Collision is not automatically bad:
some collision is necessary for rule discovery. A projection with almost no
collision is near row-identity and cannot support reusable grammar rules.

### Band `7501..9000`

```text
row_count = 13861
public_word_count = 4818
factor_residue_phase_class_count = 230
factor_phased_word_count = 1466
factor_positioned_word_count = 10317
```

| projection | distinct keys | collision keys | keys >= 3 rows | keys >= 5 rows | max rows/key |
| --- | ---: | ---: | ---: | ---: | ---: |
| current compressed | `12895` | `763` | `141` | `11` | `9` |
| current + GWR side | `13150` | `587` | `97` | `3` | `7` |
| current + GWR distance | `13605` | `224` | `31` | `0` | `4` |
| factor phased word | `13691` | `157` | `13` | `0` | `3` |
| factor positioned word | `13857` | `4` | `0` | `0` | `2` |
| oriented factor phase word | `13758` | `99` | `4` | `0` | `3` |
| oriented factor position word | `13852` | `9` | `0` | `0` | `2` |

### Band `9001..11000`

```text
row_count = 23653
public_word_count = 6512
factor_residue_phase_class_count = 300
factor_phased_word_count = 1926
factor_positioned_word_count = 13569
```

| projection | distinct keys | collision keys | keys >= 3 rows | keys >= 5 rows | max rows/key |
| --- | ---: | ---: | ---: | ---: | ---: |
| current compressed | `21167` | `1786` | `447` | `66` | `8` |
| current + GWR side | `21743` | `1469` | `297` | `32` | `8` |
| current + GWR distance | `22972` | `594` | `68` | `3` | `5` |
| factor phased word | `23142` | `466` | `40` | `1` | `5` |
| factor positioned word | `23639` | `14` | `0` | `0` | `2` |
| oriented factor phase word | `23372` | `268` | `11` | `1` | `5` |
| oriented factor position word | `23629` | `24` | `0` | `0` | `2` |

## Interpretation

The old compressed map has enough collision to produce attractive survivor
clusters, but those clusters are unstable because distinct factor structures
have been collapsed into the same residue-phase class.

The positioned-word projections preserve almost everything. They are too close
to row identity, so they are not the next rule-discovery surface.

The useful intermediate region is:

```text
factor_phased_word
oriented_factor_phase_word
current_plus_gwr_distance
```

Those projections recover most of the distinctions lost by the old compressed
map while still leaving some repeated keys for grammar discovery.

## New Working Direction

Stop forward-testing the old compressed candidate rows as the main research
engine.

The next working object is:

```text
GWR-enriched public word around N
  ->
factor phased word, with orientation tracked separately
```

This means the next phase should derive compatibility surfaces at an
intermediate grammar scale, then test those surfaces forward. The old
residue-phase multiset map remains useful as a coarse exploratory lens, but it
is no longer the rule layer.

## Reproduction

Run the enriched corpus on `7501..9000`:

```text
python3 enriched_multiplication_map_corpus.py
```

Run the enriched corpus on `9001..11000`:

```text
python3 enriched_multiplication_map_corpus.py \
  --band 9001:11000 \
  --output-dir output/enriched_multiplication_map_corpus_9001_11000
```

The script writes:

```text
output/enriched_multiplication_map_corpus_*/enriched_rows.jsonl
output/enriched_multiplication_map_corpus_*/projection_rows.jsonl
output/enriched_multiplication_map_corpus_*/summary.json
```

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
status = measured_representation_reset
next_object = GWR-enriched public word -> factor phased word with orientation tracked
```
