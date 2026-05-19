# Blind Restart Boundary

The blind restart fixed the hidden-factor bound, but it did not yet establish
factor selection from the reciprocal-shadow field.

## What It Fixed

The candidate stream starts from public `floor(sqrt(N))` and scans downward in
public fixed-size segments. The hidden factors `p` and `q` are not used as
candidate bounds or candidate filters.

## Remaining Failure

The stream is still an ordinary numeric walk. If it scans far enough, it reaches
the lower factor `p` because `p` is a prime below `sqrt(N)`.

That means a first audit hit in this stream is not yet evidence that the local
web selected the factor. It is evidence that the public scan encountered the
factor and then the reciprocal-shadow score was measured at that point.

## Current Valid Evidence

The strongest valid inference evidence remains the fixed-window ranking run,
where all candidates in the tested finite surface were scored and sorted by the
reciprocal-shadow score, and the hidden lower factor ranked first.

## Required Replacement

A scalable restart must produce a candidate order or compressed candidate set
from the reciprocal-shadow field itself. It must not depend on walking ordinary
prime candidates until the audit factor is encountered.
