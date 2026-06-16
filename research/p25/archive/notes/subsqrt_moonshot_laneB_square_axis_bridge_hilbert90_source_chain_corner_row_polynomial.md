# Lane B: Bridge Hilbert-90 Source-Chain Corner Row Polynomial

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_gate.py`

## Result

The canonical active corner can be written directly in the `C_3` source-row
coordinate.

For source row `r = 0,1,2`, write:

```text
c = c0 + 13*f
```

Then the canonical corner is:

```text
c0(r) = 4*r^2 - r
f(r)  = r*(1-r)
```

This gives:

```text
r:       0   1    2
c0:      0   3    1
f:       0   0   11
c mod169 0   3  144
q:       0 172  482
```

It is the same section as the previous checkpoint:

```text
f(c0) = c0*(c0 - 3)
```

on the selected `C_13` shadow values `{0,3,1}`.

The shadow polynomial `4*r^2-r` has the additional root `r=10` over `F_13`;
that root is off the selected source rows and is recorded by the gate.

## Interpretation

This is a more producer-facing normal form.  The target is no longer only
“some quadratic fiber section over three shadow points”; the canonical corner
is a single quadratic row graph in `C_169`, plus the forced raw `K` trace.

The covariance checkpoint still matters: transporting this row polynomial to
the other active corners requires the actual nonsplit `C_169` carry law.  The
split no-carry model fails on the reversal-side transports.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_rows=1/1
```
