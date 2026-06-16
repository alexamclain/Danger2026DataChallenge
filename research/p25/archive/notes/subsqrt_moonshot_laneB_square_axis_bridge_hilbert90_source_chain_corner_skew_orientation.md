# Lane B: Bridge Hilbert-90 Source-Chain Corner Skew Orientation

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_orientation_gate.py`

## Result

The recorded `197/310` branch has a local selector before the Hilbert-90 image
is taken.

For each one-cancellation source translation, compute the centered signed
`C_169` skew residuals and multiply their sum by the constant source-chain
coefficient:

```text
orientation_score = chain_coefficient * sum(centered_delta_c)
```

Across the six one-cancellation directions, the score set is always:

```text
{-84, -75, -9, 9, 75, 84}
```

The recorded branch is the unique score `-84`; the opposite short branch is
the unique score `+84`.

## Interpretation

This is a positive selector, not just an obstruction.  The branch can be
chosen locally from the skew derivative of the row-quadratic corner, before
asking whether the inversion image is the signed `S=172` bridge.

The producer target is now:

```text
row-quadratic K-traced corner
  -> one-cancellation skew derivative
  -> coefficient-weighted signed orientation score -84
  -> signed S=172 bridge image
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_skew_orientation_rows=1/1
```
