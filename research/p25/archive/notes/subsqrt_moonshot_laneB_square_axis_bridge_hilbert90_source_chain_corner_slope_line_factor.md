# Lane B: Bridge Hilbert-90 Source-Chain Corner Slope-Line Factor

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_slope_line_factor_gate.py`

## Result

The slope-one chord selector is equivalent to a factored line intersection of
the active quadratic fiber section.

Write each active `C_169` source value as:

```text
c = c0 + 13*f
```

For each active corner there is a slope-one line:

```text
f = c0 + s
```

such that subtracting the line from the active quadratic section gives a
quadratic residual whose two roots are exactly the two `C_13` shadows of the
half-bridge endpoints.

The line intercepts are:

```text
orientation mask 1: s = 10
orientation mask 6: s = 2
```

The remaining selected row point is off the line and is an explicit control.

## Interpretation

The selector can now be staged as:

```text
K-traced row-quadratic corner
  -> active quadratic fiber section f(c0)
  -> subtract the slope-one line f = c0 + s
  -> take the two roots of the residual as the half-bridge chord
  -> orient by coefficient-weighted negative tangent (-2,-2)
  -> signed S=172 bridge image
```

This still does not supply the arithmetic producer, but it packages the
half-bridge edge as a factored quadratic-minus-line condition over `F_13`.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_slope_line_factor_rows=1/1
```
