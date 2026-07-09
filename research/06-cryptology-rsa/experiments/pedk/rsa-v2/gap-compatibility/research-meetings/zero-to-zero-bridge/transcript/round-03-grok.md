**Round 3 Response**

Codex, the load-equality reduction is the right next compression. It does not feel too coarse; it is the smallest local invariant that the probe chain already converged on and that directly supplies the "no residual" mechanism we need for Rung 2.

### Why the Reduction Holds (and Where a One-Word Polish Is Still Needed)

The corpus already uses exactly this language in the shared-load probes:

- Under `public_at_winner`, the divisor count at the selected position is always 4 (the first minimum for a semiprime `N = pq`, `p ≠ q`).
- The clean endpoint right boundary is also the number 4 (`max(a, b) = 4`).
- The measured identity is `endpoint right boundary = public selected divisor count`.
- The transport defect is simply the normalized form of the signed difference of those two numbers.

Your proposed statement therefore recovers the actual measured object:

```text
public_selected_load = 4          (divisor count at GWR winner)
right_endpoint_load = max(a, b)   (first right-open offset value)
```

When the two numerical values are equal, the right side has zero residual *within the grammar* for any reentry move that would preserve the equality. The only right-side changes the wheel permits are the two deviations that take the right-endpoint number to 2 or to 6; both break the equality. Hence any reentry that is forced to keep the right load matched to the public load of 4 cannot be carried by a right-boundary adjustment. The directed movement must come from the opposite side: the immediate-left slot of the lower factor.

The off-zero cases fall out cleanly as ordinary inequalities, exactly as you wrote:

- `max(a, b) = 2` → right load below public selected load (shortfall gives the cell right-side room that the public zero does not protect).
- `max(a, b) = 6` → right load above public selected load (overshoot likewise gives right-side room).

The single place the phrasing needs the smallest correction is the identification "public selected load = public selected offset = 4". The *offset* (the distance from the left endpoint of the public gap to N) is what is zero under `public_selected_defect = 0`. The *load* that equals 4 is the divisor count attained at that offset position. They are distinct attributes of the same public object. The equality we care about is between two loads:

- public divisor-count load at the winner position, and
- numerical value of the endpoint right boundary.

Once that distinction is kept explicit, the rest of the reduction is exact and minimal. We do not yet need public gap width; the numerical match of the two 4’s is the local pinning condition.

This also makes the "transport budget" concrete without extra grammar: it is simply the residual `right_endpoint_load − public_selected_load`. Zero residual on the right forces the reentry carrier to the left.

### Updated Rung 2 for the Deliverable (Load-Equality Form)

**Rung 2. Load-Equality Transport Obstruction**  
When `public_selected_load = 4` (divisor count at the GWR winner) equals `right_endpoint_load = max(first right-open after p, first right-open after q)`, the right side has no residual load available for reentry while preserving the equality. Any reentry of a prior-absent supported cell that keeps the two loads matched must therefore be carried by the opposite directed side: the lower-factor immediate-left slot, realized as terminal-twin lift (immediate-left distance exactly 2 inside a preceding gap wide enough to contain four interior wheel-open slots).  
*Exact falsification predicate:* Any row in which public selected divisor count = 4, right boundary value = 4, the cell is prior-absent and supported, and the cell re-enters as an exact endpoint pair without the lower factor satisfying terminal-twin lift.

This version of Rung 2 is now a pure load-equality statement plus the forced left-side carrier. It removes the last layer of "defect" and "budget" language while staying inside the two PGS objects (public winner load and directed endpoint right-open values).

The full three-rung ladder is now ready to be written in final one-sentence form with its three predicates. The only remaining work inside the deliverable is to confirm that the numerical coincidence (both loads = 4) is treated as an identity of the current wheel rather than a universal numerical law, and to attach the predicates.

---

**Exactly one next question:**

With Rung 2 now reduced to the load-equality statement above, do you want the final deliverable to be the complete three-rung ladder written out with the one-sentence form and falsification predicate for each rung (so the meeting ends with an explicit, copy-ready proof object), or do you first want a one-paragraph check that the two observed reentry rows in the reentry-cell probe are exactly the cases that would violate the Rung 2 predicate under load equality?
