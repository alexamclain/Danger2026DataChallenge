# Lane B: Bridge Hilbert-90 Source-Chain Corner Triangle Edge

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_triangle_edge_gate.py`

## Result

The six one-cancellation first-boundary directions are exactly the six directed
edges of the three-point row-quadratic corner.

For every active corner, the directed edge set is:

```text
{25, 172, 197, 310, 335, 482}
```

The three undirected C-axis edge lengths are:

```text
3, 25, 28
```

The half-bridge edge is the `197/310` pair, i.e. the edge of C-length `28`.
The recorded branch is the orientation of that edge with coefficient-weighted
signed C-step `-28`; the opposite short branch is the same undirected edge
with coefficient-weighted signed C-step `+28`.

## Interpretation

The C-axis polarity selector is not an independent statistic. It is a directed
edge selector on the row-quadratic corner:

```text
K-traced row-quadratic corner
  -> choose the half-bridge triangle edge
  -> choose its negative C-axis polarity
  -> signed S=172 bridge image
```

This sharpens the producer target: realize the negative-polarity half-bridge
edge of the three-point source graph, not just any one-cancellation boundary
or the opposite orientation of the same edge.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_triangle_edge_rows=1/1
```
