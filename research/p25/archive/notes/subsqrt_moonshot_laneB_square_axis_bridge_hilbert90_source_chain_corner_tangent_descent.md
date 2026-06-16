# Lane B: Bridge Hilbert-90 Source-Chain Corner Tangent Descent

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_tangent_descent_gate.py`

## Result

The row-cycle descent splits cleanly in `C_13` shadow plus fiber tangent
coordinates:

```text
-28 = -2 + 13*(-2)
```

Across every active corner, the fixed source-row cycle has tangent set:

```text
{(-2,-2), (-1,2), (3,0)}
```

The `q=310` edge is the unique negative diagonal tangent `(-2,-2)`. Its reverse
`q=197` is the positive diagonal tangent `(2,2)`. After multiplying by the
chain coefficient, the recorded branch is always the negative diagonal tangent
`(-2,-2)`.

## Interpretation

The selector can now be stated one level below the full `C_169` scalar:

```text
K-traced row-quadratic corner
  -> split row-cycle C step into C_13 shadow + fiber tangent
  -> choose the coefficient-weighted negative diagonal tangent (-2,-2)
  -> signed S=172 bridge image
```

This does not produce an arithmetic certificate, but it turns the half-bridge
edge into a local tangent-plane condition. The other row-cycle edges are now
explicit controls: a pure-shadow step `(3,0)` and a mixed step `(-1,2)`.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_tangent_descent_rows=1/1
```
