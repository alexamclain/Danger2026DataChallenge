# P25 Lane B: Robert KSY-y Projection Gate

Updated: 2026-06-13 14:03 PDT

## Purpose

The half-edge footprint gate showed that the normalized Koo-Shin-Yoon
coordinate has a 300-cell Siegel-exponent footprint, not the 150-cell bridge
payload.  This gate records the useful structure of that footprint:

```text
y(Q) = -g(2Q) / g(Q)^4
footprint(y(P+h)/y(P-h)) = double_pushforward(bridge) - 4*bridge
```

## Result

The coefficient layers are sharply separated:

```text
abs(coefficient)=4 layer, scaled by -1/4 -> exact 150-cell bridge
abs(coefficient)=1 layer                  -> doubled bridge, wrong trace
coefficient-blind 300-cell footprint      -> fails bridge contract
```

This is a positive clue and a warning.  The normalized `y` quotient contains
the bridge as a labeled theorem-side layer, but it also contains a doubled
bridge layer that cannot be ignored.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_y_projection_gate.py
```

Expected marker:

```text
robert_ksy_y_projection_rows=1/1
```

## Interpretation

A successful KSY `y` or Kato-Siegel `dlog` route must explain the
theorem-side separation or cancellation of the `g(2Q)` layer.  Feeding the full
normalized-`y` exponent footprint directly to the sparse bridge harness is
wrong, but extracting the `g(Q)^-4` layer is exactly the desired finite object.
