# Lane B: Bridge Hilbert-90 Source-Chain Corner Monotone Edge

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_monotone_edge_gate.py`

## Result

The half-bridge edge is the unique C-axis monotone long edge of the
three-point row-quadratic corner.

For the selected triangle, the directed one-cancellation edges have C-axis
lengths:

```text
±3, ±25, ±28
```

The `±28` half-bridge edge is special because its two-leg path through the
third corner vertex has same-sign centered C-increments:

```text
25 + 3 = 28
-25 - 3 = -28
```

The edges of C-length `3` and `25` have mixed-sign two-leg decompositions.

The recorded branch is the negative-polarity orientation of this monotone long
edge.  The opposite short `197/310` branch is the positive-polarity orientation
of the same undirected edge.

## Interpretation

The producer target can now be stated without a table scan:

```text
K-traced row-quadratic corner
  -> unique monotone long C-edge of the source triangle
  -> negative orientation of that edge
  -> signed S=172 bridge image
```

This is still a finite payload, not a certificate, but the local branch debt is
now a recognizable geometric selector: choose the monotone long side of the
row triangle and orient it negatively.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_monotone_edge_rows=1/1
```
