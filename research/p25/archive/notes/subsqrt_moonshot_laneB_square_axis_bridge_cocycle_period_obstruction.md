# p25 Lane B Square-Axis Bridge Cocycle-Period Obstruction

Updated: 2026-06-12

## Result

The latest split-contrast checkpoint says the right source can be factored into
a visible `C_3` part and a `C_25` trace, while the C source remains cyclic
`C_169`.  This checkpoint records the corresponding period obstruction.

Write a C-source exponent as

```text
c = low + 13*fiber,  low,fiber in C_13.
```

For a visible step with low part `s`, the carry vector over all `13` low
classes has total `s mod 13`.  Changing the visible section changes the carry
vector by a coboundary, whose total around the visible cycle is zero.  So if
`s != 0`, no section change can make the step a constant fiber translation.

For the bridge:

- `D_c = 3` has carry positions `10,11,12`, total `3`, and monodromy
  `D_c^13 = g^39`;
- `T_c = 113 = 9 + 13*8` has carry positions `4,...,12`, total `9`, and
  monodromy `T_c^13 = g^117`;
- enumerating all affine and quadratic section changes gives zero constant
  section repairs for both steps.

The local samples used by the bridge are exactly the measured nonsplit carries:

- D carries `(1,0)`, giving positive fibers `1,2,2`;
- T carries `(1,0,1)`, giving negative fibers `10,10,11`.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_cocycle_period_obstruction_gate.py
```

Expected row:

```text
square_axis_bridge_cocycle_period_obstruction_rows=1/1
```

## Continue / Kill

Kill producer candidates that try to recover the C bridge edge from a cheap
`C_13` shadow plus a clever section.  The obstruction is global around the
visible `C_13` period, not an artifact of the chosen coordinates.  Continue
only with candidates that encode the primitive cyclic `C_169` monodromy, or an
equivalent nonsplit finite-field identity.
