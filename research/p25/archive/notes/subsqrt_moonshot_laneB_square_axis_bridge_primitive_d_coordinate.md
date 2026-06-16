# p25 Lane B Square-Axis Bridge Primitive D-Coordinate

Updated: 2026-06-12

## Result

The finite bridge payload has a useful one-generator normal form.  In raw
source coordinates `C_75 x C_169`, the D-segment step

```text
D = (22,3)
```

is primitive of order `12675`.  With `z` denoting this primitive source
coordinate, the accepted bridge is exactly

```text
z^11275 * (sum_{j=0}^{24} z^(4056*j)) * (1 + z + z^2) * (1 - z^6854).
```

The source factors translate as:

- `base = D^11275`;
- `K = (57,0) = D^4056`, order `25`;
- `T = (38,113) = D^6854`, order `12675`;
- `Y_raw = (9,9) = D^8622`, with `D^3 = K * Y_raw`.

The word has `150` signed raw source cells, degree zero, coefficient counts
`75` positive and `75` negative, and passes the bridge candidate harness.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_primitive_d_coordinate_gate.py
```

Expected row:

```text
square_axis_bridge_primitive_d_coordinate_rows=1/1
```

## Continue / Kill

Continue with this as a positive producer target: an arithmetic realization may
try to build one primitive local source coordinate and the cyclic word above,
rather than treating `K`, `D`, and `T` as unrelated axes.

Do not misread this as a low-order quotient escape.  The generator `D` and the
edge `T` remain primitive of order `12675`, and the `K` trace is an order-`25`
subtrace inside that primitive coordinate.  Any successful producer still has
to account for the full raw Kummer/monodromy cost or replace it by a genuine
finite-field identity.
