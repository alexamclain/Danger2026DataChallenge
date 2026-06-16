# p25 Lane B Square-Axis Bridge Carry Cocycle

Updated: 2026-06-12

## Result

The accepted 150-cell bridge is not just a `C_13` shadow plus an independent
fiber choice.  It uses the carry cocycle of the nonsplit cyclic extension
`0 -> C_13 -> C_169 -> C_13 -> 0`.

Write `c = c0 + 13*f`.  For the true bridge:

- `D_c = 3` from base `c = 25` has carries `(1,0)`, giving positive fibers
  `1,2,2`.
- `T_c = 113 = 9 + 13*8` has carries `(1,0,1)`, giving negative fibers
  `10,10,11`.
- The `T` translate is the reversed inversion of the lifted `D` segment.

The split no-carry model `C_13 x C_13` is a useful rejected control.  It has:

- support `150`, degree `0`, and the same `C_13` projection as the true bridge;
- kernel mode `{0}` and raw `D^3=Y` mismatches `0`;
- full quotient character payload: `168` pure C and `336` mixed right/C
  characters;
- but wrong fibers, trace failure, and no inversion-compatible `T` lift.

So frequency support, kernel-triviality, raw relation, and the cheap shadow are
still insufficient.  A serious arithmetic producer must realize the cyclic
`C_169` carry law itself.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_carry_cocycle_gate.py
```

Expected row:

```text
square_axis_bridge_carry_cocycle_rows=1/1
```

## Continue / Kill

Continue the bridge route, but require future CM-Artin, Jacobi, or modular-unit
candidates to explain the nonsplit `C_169` carry cocycle.  Kill candidates that
model the lift as a split `C_13 x C_13` fiber, even if they reproduce the
`C_13` shadow and full mixed character support.
