# Prime Gap Generative Model v1.0

Prime gaps are usually introduced by their sizes. One gap has size `2`, another has size `6`, another has size `8`, and so on. From that point of view the sequence looks irregular, and the first question is usually how large the next raw gap will be.

The generative model in this repository studies a different surface.

Instead of treating each gap only as a raw distance, it reduces gaps into types that preserve local prime-gap structure. On that reduced surface, the stream does not look like unrelated jumps. It settles into persistent structure.

## The Reduced Surface

The model is not a theorem about the full raw gap-size sequence.

It is a frozen model on the persistent reduced gap-type surface.

That distinction matters. Raw gap sizes still vary. The model asks what remains stable after the gaps are read through the reduced type vocabulary. On that surface, the type stream closes to a persistent `14`-state core.

The point is not that every raw gap becomes easy. The point is that a stable reduced structure appears when the right features are tracked.

## The Semiprime Wheel Attractor

The dominant dynamical object on the settled reduced surface is the Semiprime Wheel Attractor.

It is carried by this triad:

- `o2_odd_semiprime|d<=4`
- `o4_odd_semiprime|d<=4`
- `o6_odd_semiprime|d<=4`

The names are compact because they carry the reduced type information. The story behind them is the same one the README begins with: the gap is not only a size. Its internal arithmetic structure matters, and repeated structure can be tracked from gap to gap.

## The Three Layers

The frozen `v1.0` model has three layers.

The first layer is the core grammar. It describes the stable reduced states that recur.

The second layer is the transition rule. It describes how the model moves from one reduced state to the next.

The third layer is the higher-divisor-triggered long-horizon controller. It records the longer-range control behavior that appears when higher divisor structure enters the stream.

Together, those layers turn the reduced gap-type surface into a finite-state generative model.

## Reference Profiles

The frozen model carries these reference operating profiles:

- local fidelity: pooled-window concentration L1 `0.0116`
- balanced operating profile: pooled-window concentration L1 `0.0150`, full-walk three-step concentration `0.5564`
- long-horizon study: full-walk three-step concentration `0.6278`

Those values describe model behavior on the documented surfaces. They are part of the model’s measured profile, not a proof that the raw gap-size sequence itself has been reduced to a finite-state theorem.

## Where To Read More

The release and model notes give the detailed construction:

- [Prime Gap Generative Model v1.0 release note](docs/releases/prime_gap_generative_engine_v1_0.md)
- [Gap-type model v1.0 freeze note](gwr/findings/gap_type_engine_v1_freeze.md)
- [Gap-type model v1.0 rulebook](gwr/findings/gap_type_engine_v1_rulebook.md)
- [Hierarchical model paper draft](research/02-gwr-dni/docs/prime_gap_hierarchical_engine_paper_draft.md)
- [Model overview figure](output/gwr_dni_gap_type_engine_v1_overview.png)
