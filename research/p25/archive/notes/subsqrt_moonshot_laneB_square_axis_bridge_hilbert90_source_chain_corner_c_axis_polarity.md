# Lane B: Bridge Hilbert-90 Source-Chain Corner C-Axis Polarity

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_c_axis_polarity_gate.py`

## Result

The skew-orientation score has a simple local formula.  For every
one-cancellation source translation:

```text
orientation_score = 3 * chain_coefficient * centered_C169_direction_component
```

So the score set

```text
{-84, -75, -9, 9, 75, 84}
```

is just three times the coefficient-weighted C-axis polarity set

```text
{-28, -25, -3, 3, 25, 28}
```

The recorded branch is the unique coefficient-weighted signed C-step `-28`.
The opposite short `197/310` branch is the unique coefficient-weighted signed
C-step `+28`.

## Interpretation

The local selector no longer needs to be phrased as a residual-sum scan.  A
producer can target:

```text
K-traced row-quadratic corner
  -> one-cancellation skew boundary
  -> coefficient-weighted signed C-axis step -28
  -> signed S=172 bridge image
```

This is still not an arithmetic certificate, but it makes the branch-selection
debt smaller and more local: realize the one-cancellation boundary with the
negative C-axis polarity.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_c_axis_polarity_rows=1/1
```
