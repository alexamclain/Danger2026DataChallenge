# Lane B: Bridge Hilbert-90 Source-Chain Corner Image Support

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_image_support_gate.py`

## Result

The K-orbit support ladder now extends through the inversion boundary.

For every active source-chain corner, the recorded half-boundary direction
`197` or `310` has:

```text
K-traced corner:          75 raw cells
first boundary:          100 raw cells
inversion image / bridge: 150 raw cells
```

In primitive `D` coordinates, the bridge image is always:

```text
z^121 + z^122 + z^123 - z^384 - z^385 - z^386
```

Scanning all `506` possible first-boundary directions shows that the only
directions whose inversion image is exactly the signed bridge are the recorded
ones:

```text
mask 1, direction 197 -> D-step 122
mask 1, direction 310 -> D-step 385
mask 6, direction 197 -> D-step 122
mask 6, direction 310 -> D-step 385
```

## Trap Door

Support size alone is not enough.  Some wrong support-`100` first boundaries
also expand to support-`150` inversion images, but their signed image is not
the bridge.  The verifier must therefore match the actual bridge word, not only
the `75 -> 100 -> 150` support counts.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_image_support_rows=1/1
```
