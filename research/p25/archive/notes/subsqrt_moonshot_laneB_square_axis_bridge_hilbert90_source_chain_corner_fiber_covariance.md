# Lane B: Bridge Hilbert-90 Source-Chain Corner Fiber Covariance

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_covariance_gate.py`

## Result

The four active corner fiber quadratics are not four unrelated interpolations.
They are the selected-support images of one canonical section under the actual
product-affine source maps on `C_3 x C_169`.

Canonical section:

```text
shadow/fiber pairs = (0,0), (3,0), (1,11)
fiber polynomial   = f(c0) = c0*(c0 - 3)
```

The four active rows are transported by:

```text
(right,c) -> (right,     c)
(right,c) -> (right+2,   c+28)
(right,c) -> (2r+1,   -c+141)
(right,c) -> (2r,       -c)
```

On the selected three shadow points, these maps recover exactly the four
quadratic fiber sections recorded by the previous gate.

## Carry Check

The nonsplit `C_169` carry is essential on the reversal-side rows.  If the
transport is computed as a split `C_13 x C_13` fiber map with the carry term
removed:

```text
success rows = 2
failure rows = 2
```

The two failure rows are precisely the maps with `c -> -c + 141` and `c -> -c`.

## Interpretation

The active fiber correction is one covariant object, not a bag of fitted
quadratics.  This is a positive producer target: realize the canonical
quadratic section `c0*(c0-3)` and transport it with the actual nonsplit
`C_169` carry law.

It also kills a shortcut.  A split no-carry `C_13 x C_13` model cannot transport
the corner data correctly, even after the raw `K` trace is factored out.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_fiber_covariance_rows=1/1
```
