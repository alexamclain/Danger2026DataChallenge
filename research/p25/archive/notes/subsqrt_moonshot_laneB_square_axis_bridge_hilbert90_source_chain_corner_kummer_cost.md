# Lane B: Bridge Hilbert-90 Source-Chain Corner Kummer Cost

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_kummer_cost_gate.py`

## Result

The forced raw `K` trace is cheap, but the active half-bridge corner is not.

The `K` trace factor is the right-kernel shift:

```text
K = (57, 0) in C_75 x C_169
right order = 25
C order     = 1
combined    = 25
```

So the `K` factor itself is a right-side trace cost.

The four active corner chains all have the same six sparse pair directions:

```text
25, 172, 197, 310, 335, 482
```

For every one of these directions, across all `25` raw kernel gauges:

```text
right-source order histogram = {3: 1, 15: 4, 75: 20}
minimum combined source order = 507
C-source order values         = {169}
C_169 Kummer degree           = 169
C_13 shadow Kummer degree     = 13
```

Thus one gauge can make the right side look order `3`, but no gauge lowers the
primitive `C_169` motion.

## Interpretation

The current target has separated into two different costs:

```text
cheap/right-only:
  forced 25-point K trace

still expensive:
  primitive C_169 corner directions
```

This rules out the most tempting escape after the raw `K`-trace selector: a
producer cannot explain the half-bridge corner by choosing a clever right-kernel
gauge alone.  The remaining arithmetic debt is to realize the source-graph
corner with its block `K` trace while still paying, avoiding, or reframing the
primitive `C_169` Kummer cost.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_kummer_cost_rows=1/1
```
