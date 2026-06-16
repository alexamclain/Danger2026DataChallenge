# P25 Lane B: Robert KSY-y Half-Edge Footprint

Updated: 2026-06-13 13:58 PDT

## Purpose

This gate fixes the edge convention for the live Koo-Shin-Yoon normalized
`y/wp'` route.  The finite bridge has edge

```text
T = (38,113)
```

but the analytic odd quotient has symmetric form

```text
y(P+h) / y(P-h)
```

so the analytic shift is a half-edge, not the bridge edge itself.

## Result

The required half-edge is:

```text
H = (19,141)
2H = T
```

For the accepted orientation use `h=-H=(56,28)` and center base `base+H`.
This produces the exact 150-cell bridge.  The controls fail:

```text
using +H                  -> inverse orientation
using T as the half-shift -> edge 2T, wrong bridge
```

Expanding the normalized Koo-Shin-Yoon coordinate

```text
y(Q) = -g(2Q) / g(Q)^4
```

over the accepted centers gives an upstream Siegel-exponent footprint:

```text
support = 300
degree = 0
coefficient counts = (-4,75), (-1,75), (1,75), (4,75)
quotient support = 12
bridge payload ok = false
```

This is not a failure of the `y` route.  It says the raw Siegel-exponent
footprint is not itself the 150-cell bridge payload; a theorem candidate must
use the `y` values or `dlog` identity, with the half-edge convention, before
emitting signs, the primitive triangle, or sparse bridge triples.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_y_half_edge_footprint_gate.py
```

Expected marker:

```text
robert_ksy_y_half_edge_footprint_rows=1/1
```
