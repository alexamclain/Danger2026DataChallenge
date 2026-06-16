# P25 KSY-y H0 X1(16) Chart-Payload Intake

Updated: 2026-06-14 17:52 PDT

## Purpose

This gate checks the first fully numeric extraction payload after a same-j
H0/order-`8112` bridge claim:

```text
y, x, A, xP16, optional z/x32, optional x0
```

It verifies the production `x16halvenonsplit` chart over `F_p`, rather than
just classifying the claim shape.

## Checked Equations

```text
p = 10^25 + 13
k = 42
active mode = x16halvenonsplit

(y^2 - 2y)x^2 + (2y^2 - y^3)x + (1 - y) = 0

A = N(y) / (4*(y-1)^4)
N(y) =
  y^8 - 8y^7 + 24y^6 - 32y^5 + 8y^4
  + 32y^3 - 48y^2 + 32y - 8

xP16 = x / (x - y)

(y^2 - 2)*(y^2 - 4y + 2) is nonsquare
```

For the optional first-half d-gate, it also checks:

```text
z^2 = (y - 1)*(y^2 - 2)*(y^2 - 2y + 2)
computed x32 doubles back to xP16
```

## Regression Sample

The built-in positive chart sample is:

```text
y     = 21
x     = 3056787867540315204387750
A     = 5001921875000000000039606
xP16  = 5641277106015054878246206
z     = 7810871300106318158204546
x32   = 8473620875806245623307779
```

The gate recomputes `A`, `xP16`, and `x32` from the chart equations.

## Regression Rows

```text
no_chart_payload:
  decision = reject_no_chart_payload

valid_y_only:
  decision = y_chart_missing_model_root

valid_y_x_without_bridge:
  decision = conditional_chart_payload_without_order8112_bridge

valid_y_x_active_surface:
  decision = active_surface_reached_halving_missing

valid_y_x_bad_A:
  decision = reject_A_or_xP16_mismatch

valid_y_x_optional_dgate:
  decision = optional_depth5_surface_reached_halving_missing

direct_A_xP16_surface:
  decision = active_surface_reached_halving_missing

direct_A_x0_no_vpp:
  decision = extraction_ready_vpp_missing

direct_A_x0_vpp_fails:
  decision = reject_vpp_failed
```

## Counts

```text
row_count             = 9
rejected_rows         = 3
bridge_missing_rows   = 1
y_only_rows           = 1
x16_surface_rows      = 4
optional_dgate_rows   = 1
extraction_ready_rows = 1
vpp_executed_rows     = 1
submission_ready_rows = 0
```

## CLI Examples

Active depth-4 surface:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x16_chart_payload_intake_gate.py \
  --candidate --name sample_surface --h0-order8112-bridge \
  --y 21 --x 3056787867540315204387750
```

Optional depth-5 d-gate surface:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x16_chart_payload_intake_gate.py \
  --candidate --name sample_dgate --h0-order8112-bridge \
  --y 21 --x 3056787867540315204387750 \
  --A 5001921875000000000039606 \
  --xP16 5641277106015054878246206 \
  --z 7810871300106318158204546 \
  --x32 8473620875806245623307779
```

Official verifier rejection control:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x16_chart_payload_intake_gate.py \
  --candidate --name bad_vpp_demo --h0-order8112-bridge \
  --A 5001921875000000000039606 --x0 42 --run-vpp
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x16_chart_payload_intake_gate.py
```

Marker:

```text
ksy_y_h0_x16_chart_payload_intake_rows=1/1
```

## Interpretation

This closes another ambiguity in the moonshot handoff.  A future answer that
only says "we have an X_1(16) point" is not enough.  It must pass this finite
chart verifier, carry H0/order-`8112` provenance, then supply a depth-4
halving chain or direct `x0`, and finally pass official `vpp.py`.
