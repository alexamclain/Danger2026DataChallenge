# Lane B: Bridge Hilbert-90 Source-Chain Corner Slope-One Chord

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_slope_one_chord_gate.py`

## Result

The half-bridge edge is exactly the slope-one chord of the active quadratic
fiber section.

For each active row-quadratic corner, write the `C_169` value as:

```text
c = c0 + 13*f
```

with `c0` the `C_13` shadow and `f` the fiber coordinate.  Among the six
directed one-cancellation triangle edges, the only directed edges with:

```text
(f_to - f_from) / (c0_to - c0_from) = 1 in F_13
```

are exactly:

```text
q = 197, 310
```

These are the two orientations of the half-bridge edge.  The tangent-descent
law then orients this slope-one chord by requiring coefficient-weighted tangent
`(-2,-2)`.

## Interpretation

The selector can now be staged as:

```text
K-traced row-quadratic corner
  -> active quadratic fiber section c = c0 + 13*f
  -> choose the slope-one chord of that section
  -> orient by coefficient-weighted negative tangent (-2,-2)
  -> signed S=172 bridge image
```

This is still a finite payload target, but it turns the half-bridge edge into a
quadratic-section secant condition before the full `C_169` edge scan.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_slope_one_chord_rows=1/1
```
