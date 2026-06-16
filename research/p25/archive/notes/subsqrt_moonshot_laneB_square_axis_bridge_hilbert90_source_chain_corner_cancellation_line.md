# Lane B: Bridge Hilbert-90 Source-Chain Corner Cancellation Line

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_cancellation_line_gate.py`

## Result

The slope-one line in the line-factor selector is not a free choice. It is
forced by the Hilbert-90 cancellation vertex.

Write the cancellation point as:

```text
c = c0 + 13*f
```

Then the slope-one line is:

```text
f = c0 + (f - c0)
```

The residual roots are:

```text
c0_cancel
c0_cancel + 2*coefficient
```

The recorded edge points from the coefficient-selected diagonal neighbor back
to the cancellation vertex. After multiplying by the chain coefficient, its
tangent is always:

```text
(-2,-2)
```

## Interpretation

The selector can now be staged as:

```text
K-traced row-quadratic corner
  -> Hilbert-90 cancellation vertex
  -> slope-one line through that vertex
  -> coefficient-selected diagonal neighbor at distance 2
  -> recorded edge points back to cancellation
  -> signed S=172 bridge image
```

This packages the half-bridge endpoint pair as “cancellation plus one
coefficient-selected diagonal neighbor” in `C_13` shadow/fiber coordinates.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_cancellation_line_rows=1/1
```
