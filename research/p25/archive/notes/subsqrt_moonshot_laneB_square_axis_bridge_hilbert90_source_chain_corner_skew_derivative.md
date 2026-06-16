# Lane B: Bridge Hilbert-90 Source-Chain Corner Skew Derivative

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_gate.py`

## Result

The selected half-source-edge is now tied directly to the curved three-point
corner.  It is the skew row derivative of the source graph under the recorded
`197/310` first-boundary translation:

```text
delta_c(R) = c(R - d_row) + d_c - c(R)  in C_169
```

For mask `1`, the cancellation row is `1`; for mask `6`, the cancellation row
is `2`.  The two nonzero residual rows are exactly the selected half-potential
edges:

```text
short C_169 residuals: 31 and 53
C_13 shadows:          5 and 1
```

The reconstructed skew derivative matches the recorded half-source-edge in all
four active orientations.

## Interpretation

The two-edge half-potential is not a free two-edge source mask.  It is forced
by:

```text
row-quadratic source corner
  + recorded +/-122 primitive boundary
  + one Newton-vertex cancellation
  -> two oriented 31/53 source-row residual edges
```

A producer must therefore realize the skew derivative of the curved corner, not
just any pair of primitive row-local C_169 edges with the same short lengths.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_rows=1/1
```
