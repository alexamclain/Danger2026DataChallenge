# Lane B: Bridge Hilbert-90 Source-Chain Corner S-Layer Image

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_s_layer_image_gate.py`

## Result

The bridge image is not merely a six-point inversion image.  It is the unique
signed pair of full `S`-orbits that appears from the active source-chain
corners:

```text
+ (25, 197, 369)
- (138, 310, 482)
```

Here `S_STEP = 172`, so each triple is an orbit of `S = 1 + D + D^2`.

Scanning all `506` nonzero first-boundary directions for each active chain
shows:

```text
mask 1, direction 197: 10 support-six images, 1 signed S-layer image
mask 1, direction 310:  3 support-six images, 1 signed S-layer image
mask 6, direction 197:  3 support-six images, 1 signed S-layer image
mask 6, direction 310: 10 support-six images, 1 signed S-layer image
```

In every row, the unique signed `S`-layer direction is the recorded half-boundary
direction:

```text
197 -> primitive D-step 122
310 -> primitive D-step 385 = -122
```

## Interpretation

The last checkpoint showed that support `150` is not enough: some wrong
support-`100` first boundaries also have support-`150` inversion images.  This
checkpoint inserts a structural selector between support count and exact bridge
equality.  A producer must recover the constant `S`-orbit pair, not just any
six-point anti-invariant image.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_s_layer_image_rows=1/1
```
