# p25 Lane B Square-Axis Bridge Base-Section Obstruction

Updated: 2026-06-12

## Result

The previous cocycle-period checkpoint ruled out C-only section repairs.  This
checkpoint rules out the next escape: let the `C_169` fiber section depend on
the whole visible base `C_3 x C_13`, including the right coordinate.

The visible bridge steps are:

```text
D = (right + 1, c_low + 3)
T = (right + 2, c_low + 9)
```

Both act as a single `39`-cycle on `C_3 x C_13`.  A section change on that
base contributes a coboundary, so its sum around the cycle is zero.  But the
actual nonsplit `C_169` carry totals are nonzero:

- `D` has total fiber carry `9` around the `39`-cycle;
- `T` has total fiber carry `1` around the `39`-cycle.

A constant fiber translation would have total `39*c = 0 mod 13`, so no
right-dependent section can make either bridge step split as a constant
fiber move.  The gate also scans all right-dependent affine sections
(`13^3`) and all right/C bilinear sections (`13^4`), finding zero repairs.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_base_section_obstruction_gate.py
```

Expected row:

```text
square_axis_bridge_base_section_obstruction_rows=1/1
```

## Continue / Kill

Kill producer candidates that treat the C-side lift as a low `C_13` shadow
plus a right-dependent fiber gauge.  The obstruction is on the full visible
base period, so the producer still has to realize the nonsplit cyclic
`C_169` extension globally on `C_3 x C_13`, or produce an equivalent identity
with the same monodromy.
