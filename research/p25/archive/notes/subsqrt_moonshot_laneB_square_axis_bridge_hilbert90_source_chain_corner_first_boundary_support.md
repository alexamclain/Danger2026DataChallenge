# Lane B: Bridge Hilbert-90 Source-Chain Corner First Boundary Support

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_first_boundary_support_gate.py`

## Result

The forced K-traced corner has raw support `75`.  Applying a nonzero first
boundary to that K-invariant lift has raw support at least `100`.

For each active corner, the support distribution over all `506` nonzero
first-boundary directions is:

```text
raw support 100: 6 directions
raw support 150: 500 directions
```

The six support-`100` directions are exactly the pair-difference directions:

```text
25, 172, 197, 310, 335, 482
```

Each support-`100` boundary cancels one whole K orbit.  The recorded
half-boundary direction `197` or `310` is the unique support-`100` direction
whose inversion boundary gives the signed bridge.

## Interpretation

The raw support ladder is now explicit at the K-orbit level:

```text
K-traced corner:       3 K orbits = 75 raw cells
recorded first boundary: 4 K orbits = 100 raw cells
bridge image:          6 K orbits = 150 raw cells
```

A producer cannot merely create any sparse first boundary of the triangle.  It
must create the recorded half-boundary, the one K-orbit cancellation that leads
to the bridge after inversion.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_first_boundary_support_rows=1/1
```
