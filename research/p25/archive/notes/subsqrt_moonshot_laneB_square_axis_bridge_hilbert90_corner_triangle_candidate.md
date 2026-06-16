# P25 Lane B: Bridge Hilbert-90 Corner Triangle Candidate Intake

Updated: 2026-06-13 13:45 PDT

## Purpose

This is the producer-facing intake between the two-sign target and the full
sparse-source table.  A theorem candidate can emit the primitive `C_169`
corner as three row-labeled `C_13` low/fiber points, optionally with equal
branch coefficients.  The harness checks whether that triangle is one of the
four active Hilbert-90 corners and then promotes it through the existing
sign-to-sparse-source bridge.

## Candidate Format

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_triangle_candidate_harness.py \
  --point ROW LOW FIBER [COEFF] \
  --point ROW LOW FIBER [COEFF] \
  --point ROW LOW FIBER [COEFF]
```

Rows must be exactly `0`, `1`, and `2`.  `LOW` and `FIBER` are in `C_13`.
If coefficients are supplied, each must agree with the matched branch sign.

## Result

The default gate checks all four active triangles.  Each matches a unique
`eps,branch` pair, has quotient support ladder `3 -> 4 -> 6`, expands to raw
sparse support `150`, equals the recorded target sparse entries, and passes
the existing Robert sparse-source bridge harness.

Positive control:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_triangle_candidate_harness.py \
  --point 0 0 0 -1 \
  --point 1 3 0 -1 \
  --point 2 1 11 -1
```

Negative control:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_triangle_candidate_harness.py \
  --point 0 0 0 -1 \
  --point 1 3 0 -1 \
  --point 2 1 10 -1
```

Expected rows:

```text
square_axis_bridge_hilbert90_corner_triangle_candidate_harness_rows=1/1
square_axis_bridge_hilbert90_corner_triangle_candidate_rows=1/1
square_axis_bridge_hilbert90_corner_triangle_candidate_rows=0/1
```

This does not solve the producer problem.  It makes the next finite falsifier
cleaner: a Robert/Siegel/Hilbert-90 identity may emit the primitive source
triangle before explaining how the two signs arise.
