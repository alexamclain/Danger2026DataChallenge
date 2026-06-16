# Lane B: Bridge Hilbert-90 Source-Chain Corner Graph Selector

Date: 2026-06-12

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_graph_selector_gate.py`

## Result

The corner-normal-form gate left four formal cyclic `C_507` antiderivatives.
All four recover the bridge, but only two are valid source graphs.  This gate
shows that the selector is exactly the forced `C_3` row-balance condition.

For the four formal corners:

```text
graph     (0, 172, 482): row sums (-1,-1,-1), row chars (-3,0,0)
non-graph (0, 138, 335): row sums (-2, 0,-1), row chars (-3,974,-977)
non-graph (0, 172, 369): row sums ( 2, 1, 0), row chars ( 3,977,-974)
graph     (0, 25, 335):  row sums ( 1, 1, 1), row chars ( 3,0,0)
```

Thus, inside the bridge-recovering corner family:

```text
source graph
  <=> equal C_3 row sums
  <=> vanishing nontrivial C_3 row characters.
```

All four active source-chain rows satisfy this selector.  Their row sums are
`(-1,-1,-1)`, `(1,1,1)`, `(-1,-1,-1)`, `(1,1,1)`.

## Interpretation

The producer target is now slightly cleaner:

```text
half-bridge corner + C_3 row-balance
```

rather than an opaque curved support-three graph.  This does not select the
specific `C_169` lift, solve the raw `K` trace, or lower the Kummer cost.  It
only removes the two cyclic antiderivatives that collapse source rows.

