# p25 Lane B Square-Axis Bridge Primitive Affine Symmetry

Updated: 2026-06-12

## Result

The primitive `D`-coordinate bridge word has no hidden quotient affine
symmetry beyond the known bridge reversal.

After collapsing the `C_25` trace, the signed bridge in `C_507` has:

```text
++: 121, 122, 123
---: 384, 385, 386
```

An exhaustive affine scan on `C_507` finds:

```text
sign-preserving: (a,b) = (1,0)
sign-reversing: (a,b) = (506,0), i.e. e -> -e
```

There are no unsigned support symmetries that mix signs in a new way.

On the raw `C_12675` primitive coordinate, these lift to:

- `500` sign-preserving affine maps, all with `a = 1 mod 507` and
  `b = 0 mod 507`;
- `500` sign-reversing affine maps, all with `a = -1 mod 507` and
  `b = 0 mod 507`.

The count is exactly `20` trace-fiber multiplier reindexings times `25` trace
translations for each orientation.  Thus the raw freedom is only the `C_25`
trace gauge, plus the known bridge reversal.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_primitive_affine_symmetry_gate.py
```

Expected row:

```text
square_axis_bridge_primitive_affine_symmetry_rows=1/1
```

## Continue / Kill

Continue treating the primitive coordinate as a producer target, but kill
claims that a new quotient-level diamond, Frobenius, or affine averaging trick
creates the bridge.  A producer may use trace-fiber gauge freedom and may
reverse the bridge orientation; those are already accounted for and do not
change the arithmetic problem.
