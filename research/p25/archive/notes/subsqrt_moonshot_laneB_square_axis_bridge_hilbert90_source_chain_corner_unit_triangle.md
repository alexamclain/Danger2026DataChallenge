# Lane B: Bridge Hilbert-90 Source-Chain Corner Unit Triangle

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_triangle_gate.py`

## Result

The primitive unit sign `eps` and branch coefficient `a` determine the whole
row-labeled low/fiber triangle, not just the cancellation line or the two
half-bridge roots.

The cancellation and neighbor are:

```text
cancellation = (3*eps, (eps - 1)/2)
neighbor     = cancellation + 2*a*(1,1)
```

The off-line control point is:

```text
off_line_x = eps + a
off_line_y = off_line_x + s + R_{eps,a}(off_line_x)
```

where:

```text
s = (eps - 1)/2 - 3*eps
R_{eps,a}(x) = lambda_{eps,a} * (x - 3*eps) * (x - (3*eps + 2*a))
lambda_{eps,a} = -1 + 2*eps - a + eps*a
```

The source rows are also forced:

```text
cancel_row  = (3 - eps)/2
neighbor_row = cancel_row - a  mod 3
off_row      = cancel_row + a  mod 3
```

## Interpretation

The current local producer target is now:

```text
primitive D-unit sign eps
  -> branch coefficient a
  -> row-labeled three-point low/fiber triangle
  -> forced slope-one line and two-sign residual
  -> coefficient-selected edge back to cancellation
  -> signed S=172 bridge image
```

This kills the remaining “third point as passive control” interpretation. A
candidate arithmetic producer must place the off-line control in the correct
source row with the correct fiber value.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_unit_triangle_rows=1/1
```
