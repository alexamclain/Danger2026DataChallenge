# Lane B: Bridge Hilbert-90 Source-Chain Corner Skew Image Affine Obstruction

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_image_affine_obstruction_gate.py`

## Result

The opposite `197/310` short skew derivative is not a relabeled copy of the
bridge.

For each of the four active corner rows, the gate scans:

```text
158184 affine unit maps q -> a*q+b on C_507
158184 product-affine source maps on C_3 x C_169
```

The hit counts are all zero:

```text
quotient-affine support hits: 0,0,0,0
quotient-affine signed exact hits: 0,0,0,0
source-affine support hits: 0,0,0,0
source-affine signed exact hits: 0,0,0,0
```

So the near miss cannot be saved by a diamond/Frobenius/unit reindexing or by
changing product-affine source coordinates.

## Interpretation

The previous image-orbit gate showed that the recorded branch is selected by
landing on the signed `S=172` bridge image:

```text
+(25,197,369) -(138,310,482)
```

This gate strengthens the rejection of the opposite branch.  It is not merely
the right bridge seen in the wrong coordinates; it has genuinely different
affine and source-affine geometry.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_skew_image_affine_obstruction_rows=1/1
```
