# Lane B: Bridge Hilbert-90 Source-Chain Corner Skew Image Orbit

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_image_orbit_gate.py`

## Result

The `197/310` short skew-derivative near miss has a clean image-orbit
obstruction.

For the recorded branch, applying the Hilbert-90 inversion boundary gives the
signed bridge:

```text
+(25,197,369) -(138,310,482)
```

This is the unique complete signed `S`-orbit decomposition with `S = 172`.

For the opposite short skew derivative:

```text
two rows: support 6, but as wrong q=25 orbit pairs
two rows: support 8, with no length-three constant-orbit decomposition
```

So the attractive local data:

```text
one cancellation
short residuals 31 and 53
sometimes q=0 endpoint
```

does not certify the Hilbert-90 image.  The branch must land on the signed
`S=172` orbit image.

## Interpretation

The finite target is now:

```text
row-quadratic source corner
  -> oriented 197/310 skew derivative
  -> selected 31/53 residual edges
  -> signed S=172 orbit image
```

The opposite `197/310` branch is an executable near-miss control: it has the
same short residual lengths but the wrong image-orbit geometry.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_skew_image_orbit_rows=1/1
```
