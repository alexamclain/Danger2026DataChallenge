# p25 Lane B Square-Axis Bridge Subfield Descent

Updated: 2026-06-12

## Result

The formal bridge cannot be made into a proper-subfield rational signed
divisor by ordinary Frobenius descent.

The collapsed bridge on `C_507` has six signed quotient cells and `150` raw
cells after the `C_25` trace.  Since `p mod 507 = 218` has order `78`, the
only relevant subfield degrees are:

```text
1, 2, 3, 6, 13, 26, 39, 78
```

The ordinary trace/closure profile is:

```text
d=1   trace support 0    closure 234 / 5850 raw
d=2   trace support 234  closure 234 / 5850 raw
d=3   trace support 0    closure 78  / 1950 raw
d=6   trace support 78   closure 78  / 1950 raw
d=13  trace support 0    closure 18  / 450 raw
d=26  trace support 18   closure 18  / 450 raw
d=39  trace support 0    closure 6   / 150 raw
d=78  trace support 6    closure 6   / 150 raw
```

Thus every proper nonzero ordinary trace is already too large: the minimum is
`18` quotient cells / `450` raw cells at degree `26`.

The tempting degree-`39` shadow keeps the unsigned support, but `p^39 = -1`
reverses the signed bridge.  Its ordinary trace is zero.  Extracting the
orientation from this anti-invariant shadow requires a coefficient with
`alpha^(p^39) = -alpha`, so the coefficient field has degree `78`.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_subfield_descent_gate.py
```

Expected row:

```text
square_axis_bridge_subfield_descent_rows=1/1
```

## Continue / Kill

Continue treating the primitive bridge as the main producer target, but kill
proper-subfield rational explanations.  A successful producer must supply the
full degree-`78` orientation of the signed bridge, or an equivalent nonsplit
finite-field identity that does not reduce to ordinary Frobenius trace descent.
