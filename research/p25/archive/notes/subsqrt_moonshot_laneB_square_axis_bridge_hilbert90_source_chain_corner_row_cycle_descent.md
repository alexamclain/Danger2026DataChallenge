# Lane B: Bridge Hilbert-90 Source-Chain Corner Row-Cycle Descent

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_cycle_descent_gate.py`

## Result

In the fixed source-row cycle `0 -> 1 -> 2 -> 0`, every active
row-quadratic corner has exactly two C-axis ascents and one C-axis descent:

```text
{3, 25, -28}
```

The descent is always the `q=310` edge; the reverse descent is `q=197`.

The recorded branch is the coefficient-negative orientation of this descent:
coefficient `+1` records the descent itself (`q=310`), while coefficient `-1`
records the reverse descent (`q=197`).

## Interpretation

The selector can now be phrased as:

```text
K-traced row-quadratic corner
  -> row cycle with one C-axis descent of size 28
  -> choose the coefficient-negative orientation of that descent
  -> signed S=172 bridge image
```

This is still finite payload structure rather than an arithmetic certificate,
but it gives a very local row-cycle target for a producer.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_row_cycle_descent_rows=1/1
```
