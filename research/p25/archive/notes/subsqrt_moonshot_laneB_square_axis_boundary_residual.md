# Subsqrt Moonshot Lane B Square-Axis Boundary Residual

Date: 2026-06-12

## Result

The `C_169` square-axis target splits exactly into:

```text
C_169 mask = deterministic C_13 fiber background + 18-point boundary residual
```

Write:

```text
j = a + 13*b
h = right - a mod 3
```

Then:

```text
base(right,a,b) = C_13 half-arc row h at b
residual(right,a,b) = C_13 trace bit at (right,a), if b = 9 - 3*h
                      0 otherwise
```

Observed:

```text
residual_prediction_hits = 507 / 507
decomposition_hits = 507 / 507
residual_ones = 18
residual_by_row = [6, 6, 6]
residual_by_h = [3, 6, 9]
residual_by_fiber = [0, 0, 0, 9, 0, 0, 6, 0, 0, 3, 0, 0, 0]
boundary_positive_hits = 18 / 18
boundary_zero_hits = 21 / 21
nonboundary_zero_hits = 468 / 468
base_trace_hits = 39 / 39
residual_trace_hits = 39 / 39
square_trace_hits = 39 / 39
```

The component profiles are:

```text
base:
  coordinate_support = 234
  row_sums = [78, 78, 78]
  Fourier support = scalar 1, pure nonlift 156, mixed nonlift 312

residual:
  coordinate_support = 18
  row_sums = [6, 6, 6]
  Fourier support = scalar 1, pure lift 12, pure nonlift 156,
                    mixed lift 24, mixed nonlift 312

square:
  coordinate_support = 252
  row_sums = [84, 84, 84]
  Fourier support = scalar 1, pure lift 12, pure nonlift 156,
                    mixed lift 24, mixed nonlift 312
```

All three components have right-row rank `3` over both `F_2` and an odd field.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_boundary_residual_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_boundary_residual_gate.py
```

Observed:

```text
square_axis_boundary_residual_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_boundary_residual_gate
```

## Consequence

The square-axis route now has a sharper positive target than the full opaque
`507`-point mask:

```text
1. produce the deterministic C_13 fiber background;
2. produce the 18 boundary injections;
3. ensure the boundary residual traces down to the C_13 trace shadow.
```

The catch is also explicit: the 18-point residual is coordinate-sparse but
Fourier-dense.  It already carries the full non-right character support of the
square-axis mask, including the lifted pure and mixed characters missing from
the base component.  So this is not a low-frequency compression; it is a
ray-local boundary producer target.

A proposed square-axis CM-Artin or modular-unit candidate should therefore be
tested first against this residual law.  Reject it if it does not put the
boundary bit at `b = 9 - 3*h` exactly on the `18` carrying `C_13` trace slots,
or if its residual trace-down is not the `C_13` trace-shadow mask.

The finer graph-lift and per-slice Fourier fingerprint is recorded in:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_graph_lift_fourier.md
```
